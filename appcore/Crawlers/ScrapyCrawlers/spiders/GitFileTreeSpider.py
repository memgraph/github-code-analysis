from scrapy.http import Request
from scrapy.spiders import Spider
from json import loads


class GitFileTreeApiSpider(Spider):
    name = "git_filetree_api"
    url = ""
    auth_header = {}

    def start_requests(self):
        yield Request(url=self.url, headers=self.auth_header, callback=self.parse)

    def parse(self, response, **kwargs):
        response_data = loads(response.text)
        for tree in response_data["tree"]:
            if tree["type"] == "blob":
                print(tree["url"])
            else:
                yield Request(url=tree["url"], headers=self.auth_header, callback=self.parse)

    def insert_file_data_to_db(self, response):
        pass
