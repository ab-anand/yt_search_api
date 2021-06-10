#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib.request import urlopen


BASE_URL = "https://youtube.com"


class YTChannel:

    def get_channel_info(self, channel_url):
        
        channel_info = {
            "playAll_url": "",
            "subscribers_count": ""
        }
        
        try:
            ENDPOINT = f"{channel_url}/videos"
            # print(ENDPOINT)
            page = urlopen(ENDPOINT)
            html_bytes = page.read()
            response = html_bytes.decode("utf-8")

            playAll_url = self.__get_playAll_url(response)
            subscribers_count = self.__get_subscribers_count(response)
            
            channel_info["playAll_url"] = playAll_url
            channel_info["subscribers_count"] = subscribers_count
            
        except Exception as e:
            print(str(e))
            
        return channel_info

    def __get_subscribers_count(self, response):
        try:
            subscribers_value = -1

            subscribers_text = "subscriberCountText"
            if subscribers_text in response:
                subs_idx = response.index(subscribers_text)
                start = (
                    response.index("simpleText", subs_idx)
                    + len("simpleText")
                    + 3
                )

                stop = response.index("}", start) - 1
                subscribers_count = response[start:stop]
                subscribers_value = self.__parse_subscribers_count(subscribers_count)
            return subscribers_value
        except Exception as e:
            print(str(e))
            return -1

    @staticmethod
    def __get_playAll_url(response):
        try:
            if "watchPlaylistEndpoint" in response:
                start = (
                    response.index("watchPlaylistEndpoint")
                    + len("watchPlaylistEndpoint")
                    + 17
                )
                stop = (
                    response.index("}}", start) - 1
                )
                playlistId = response[start:stop]
                return f"{BASE_URL}/playlist?list={playlistId}"
            else:
                return "NOT FOUND"
        except Exception as e:
            print(str(e))
            return "NOT FOUND"

    @staticmethod
    def __parse_subscribers_count(subscribers_text):
        value_conversion = {'K': 10**3, 'M': 10**6}
        result = -1
        if "subscribers" in subscribers_text:
            subs = subscribers_text.replace("subscribers", "").strip()
            if subs[-1] in value_conversion:
                value = subs[-1]
                subs = float(subs[:-1])*value_conversion[value]

            result = int(subs)
        return result

