import requests, os
from bs4 import BeautifulSoup


# this header needed so that reddit doesn't rate limit as a bot!
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
}

def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"File {file_path} has been deleted.")
    except FileNotFoundError:
        return
    except Exception as e:
        print(f"An error occurred: {e}")


class Comment:
    comment_text: str
    comment_id: str
    comment_context_link: str 
    comment_parent: str
    comment_title: str


class Reddit:

    # pass in the comment page soup object of a user 
    # will return the comments as a list of comment objects
    def fetch_full_comment_page_as_list(self, soup) -> list:
        comments = soup.find_all(class_="thing")

        if not comments:
            return None
        
        out = []

        for comment in comments:
            comment_class = Comment()
            comment_class.comment_title = comment.find(class_="title").get_text()
            comment_class.comment_text = comment.find(class_="usertext-body").get_text().strip()
            comment_class.comment_id = comment.get("data-fullname")
            comment_class.comment_context_link = comment.find(attrs={"data-event-action":"context"}).get("href")
            out.append(comment_class)
        return out

    # pass in a comment_id and will return the soup object for that comment
    # good for extracting data about that comment and the text
    # returns a python soup object
    def get_comment_element(self, soup, comment_id) -> BeautifulSoup:
        return soup.find(attrs={"data-fullname": comment_id})

    # pass in a comment id and will return the parent comment element of that comment
    # good for getting the parent comment in a thread
    def get_parent_comment_element(self, context_page_info, comment_id)-> BeautifulSoup:
        
        parent_search=None
        full_page_soup = context_page_info["soup"]
        try:
            comment_element = full_page_soup.find(attrs={"data-fullname": comment_id})
            if comment_element is None:
                return "removed"
            parent_search = comment_element.find(attrs={"data-event-action":"parent"})
        except Exception as e:
            print(comment_id)
            print(e)
            print(context_page_info["url"])


        if parent_search is None:
            return None
        
        parent_id = parent_search.get("href").replace("#", "t1_")

        return full_page_soup.find(attrs={"data-fullname": parent_id})

    def sanitize_text(self, element) -> str:
        return element.find(class_="usertext-body").get_text().strip()

    def fetch_reddit_page(self, url) -> BeautifulSoup:
        global headers
        response  = requests.get(url, headers=headers)
        return {
            "soup": BeautifulSoup(response.text, 'html.parser'), 
            "status_code": response.status_code,
            "url":url
        }
    
    def get_next_page(self, soup):
        next_button = soup.find(class_="next-button")
        if next_button:
            return next_button.a.get("href")
        return None
        

# def hash_page(self, item_list):
#     item_list.sort()
#     y = str(item_list)
#     z = re.sub('[^a-zA-Z]+', '', y).strip()
#     # print(z)
#     # print(len(z))
#     the_hash = hash(z)
#     # print(the_hash)
#     return the_hash
