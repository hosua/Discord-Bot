from youtubesearchpython import VideosSearch
import youtube_dl
import discord

class Youtube_Searcher:
    def search(self, text, max=5):
        rtn_str = ""
        vid_search = VideosSearch(text, limit=max)
        print("Searching youtube...")
        for i in range(max):
            title = vid_search.result()["result"][i]["title"]
            link = vid_search.result()["result"][i]["link"]
            length = vid_search.result()["result"][i]["duration"]
            print(length)
            rtn_str += title + " " + link + "\n"
        return rtn_str

    def get_first_link(self, text):
        print("Searching for " + text)
        vid_search = VideosSearch(text, limit=1)
        link = vid_search.result()["result"][0]["link"]

        return link

c = Youtube_Searcher()

c.search("pringles")