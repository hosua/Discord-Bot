from googlesearch import search

class Google_search:
    def search(self, arg, end=10):
        rtn_str = ""
        for i in search(arg,
                        tld="com",
                        lang="en",
                        tbs="0",
                        safe="off",
                        num=10,
                        start=0,
                        stop=end,
                        pause=2.0):
            rtn_str += i + "\n"
        print("Searching Google...")
        return rtn_str

gs = Google_search()