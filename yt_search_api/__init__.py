#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import urllib.parse
import json

BASE_URL = "https://www.youtube.com"


class YoutubeSearch:
    def search(self, search_terms: str):
        encoded_search = urllib.parse.quote_plus(search_terms)
        url = f"{BASE_URL}/results?search_query={encoded_search}"
        response = requests.get(url).text
        while "ytInitialData" not in response:
            response = requests.get(url).text

        results = self._parse_html(response)
        apiToken = self._parse_token(response)
        context = self._parse_context(response)

        final_result = self._format_result(results, apiToken, context)

        return final_result

    def _parse_html(self, response):
        results = {}

        start = (
            response.index("ytInitialData")
            + len("ytInitialData")
            + 3
        )
        end = response.index("};", start) + 1
        json_str = response[start:end]
        data = json.loads(json_str)

        contents = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"][
            "sectionListRenderer"]["contents"]
        videos = contents[0]["itemSectionRenderer"]["contents"]
        continuation = self._get_continuation_token(contents)

        items = self.__parse_html_videos(videos)
        results["items"] = items
        results["continuation"] = continuation

        return results

    @staticmethod
    def __parse_html_videos(videos):
        items = []

        if len(videos) > 0:
            for video in videos:
                res = {}
                if "videoRenderer" in video.keys():
                    video_data = video.get("videoRenderer", {})
                    res["id"] = video_data.get("videoId", None)
                    res["thumbnails"] = [thumb.get("url", None) for thumb in
                                         video_data.get("thumbnail", {}).get("thumbnails", [{}])]
                    res["title"] = video_data.get("title", {}).get("runs", [[{}]])[0].get("text", None)
                    res["long_desc"] = video_data.get("descriptionSnippet", {}).get("runs", [{}])[0].get("text", None)
                    res["channel"] = video_data.get("longBylineText", {}).get("runs", [[{}]])[0].get("text", None)
                    res["duration"] = video_data.get("lengthText", {}).get("simpleText", 0)
                    res["views"] = video_data.get("viewCountText", {}).get("simpleText", 0)
                    res["publish_time"] = video_data.get("publishedTimeText", {}).get("simpleText", 0)
                    res["url_suffix"] = video_data.get("navigationEndpoint", {}).get("commandMetadata", {}).get(
                        "webCommandMetadata", {}).get("url", None)
                    res["owner_url"] = BASE_URL + video_data.get("ownerText", {}).get("runs", [{}])[0] \
                                                            .get("navigationEndpoint", {}) \
                                                            .get('commandMetadata', {}) \
                                                            .get('webCommandMetadata', {}).get('url', None)
                    items.append(res)

        return items

    @staticmethod
    def _parse_token(response):
        apiToken = None

        if "innertubeApiKey" in response:
            start = (
                response.index("innertubeApiKey")
                + len("innertubeApiKey")
                + 3
            )

            stop = response.index(",", start)
            apiToken = response[start:stop-1]

        return apiToken

    @staticmethod
    def _parse_context(response):
        context = None

        if "INNERTUBE_CONTEXT" in response:
            start = (
                response.index("INNERTUBE_CONTEXT")
                + len("INNERTUBE_CONTEXT")
                + 2
            )

            stop = response.index("INNERTUBE_CONTEXT", start) - 2

            context = json.loads(response[start:stop])

        return context

    @staticmethod
    def _get_continuation_token(contents):
        continuation = None
        if len(contents) > 0:
            for content in contents:
                if "continuationItemRenderer" in content:
                    continuation = content["continuationItemRenderer"]["continuationEndpoint"]["continuationCommand"]["token"]

        return continuation

    @staticmethod
    def _format_result(results, apiToken, context):

        nextPageContext = {
            "context": context,
            "continuation": results["continuation"]
        }

        results = {
            "items": results["items"],
            "nextPage": {
                "nextPageToken": apiToken,
                "nextPageContext": nextPageContext
            }
        }

        return results

    def __next_page_results(self, response):
        continuation = None
        items = []
        if response:
            if "onResponseReceivedCommands" in response:
                contents = response["onResponseReceivedCommands"][0]["appendContinuationItemsAction"]["continuationItems"]
                for item in contents:
                    if "itemSectionRenderer" in item:
                        items = self.__parse_html_videos(item["itemSectionRenderer"]["contents"])

                continuation = self._get_continuation_token(contents)

        return {"items": items, "continuation": continuation}

    def get_next_page_results(self, nextPage):
        ENDPOINT = f"{BASE_URL}/youtubei/v1/search?key={nextPage['nextPageToken']}"
        response = requests.post(ENDPOINT, json=nextPage["nextPageContext"])
        next_results = self.__next_page_results(response.json())
        nextPage["nextPageContext"]["continuation"] = next_results["continuation"]
        return {"items": next_results["items"], "nextPage": nextPage}
