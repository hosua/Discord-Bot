from youtubesearchpython import VideosSearch

class Youtube_Searcher:

    def search(self, text, max=5):
        rtn_str = ""
        vid_search = VideosSearch(text, limit=max)
        print("Searching youtube...")
        for i in range(max):
            title = vid_search.result()["result"][i]["title"]
            link = vid_search.result()["result"][i]["link"]
            rtn_str += title + " " + link + "\n"
        return rtn_str
