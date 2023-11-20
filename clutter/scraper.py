import scrapy, re
from base64 import b64encode 

class QuoteSpider(scrapy.Spider):
    name = 'redditquote-spider'
    start_urls = ['https://old.reddit.com/user/DrBiscuit01/comments/']
    page_hash_dict = {}

    def hash_page(self, item_list):
        item_list.sort()
        y = str(item_list)
        z = re.sub('[^a-zA-Z]+', '', y).strip()
        # print(z)
        # print(len(z))
        the_hash = hash(z)
        # print(the_hash)
        return the_hash
    
    def get_parent_comment(self, response,  url, ):
        awiayield scrapy.Request(
                        url, 
                        callback=self.parse,
                        meta={
                            'request_type': "parent",
                            'current_page_count': current_page_count
                        }
                    )
        

    def parse(self, response):
        # f = open("./comments.txt", "w")
        current_page_count = response.meta.get('current_page_count', 0)
        current_page_count += 1

        if response.meta.get('request_type', 0):


        out=[]
        for item in response.css('.usertext-body'):
            item = str(item.css("::text").getall()[0])
            out.append(item)
        page_hash = self.hash_page(out)
        print(out)

        if page_hash not in self.page_hash_dict:
            self.page_hash_dict[page_hash]=current_page_count
        else:
            raise Exception("Found duplicate page!!!")
        
        
        next_page = response.css('.next-button > a::attr("href")').extract_first()
        
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page), 
                callback=self.parse,
                meta={
                    'request_type': "parent",
                    'current_page_count': current_page_count
                }
            )
        else:
            print(self.page_hash_dict)