import requests
import threading
import json
from bs4 import BeautifulSoup
import util
from util import Comment, Reddit

print("Starting Script")
# type hints
comment: Comment
reddit: Reddit


data=[]

reddit = Reddit()
# username = "samaltman"
with open("./config.json", "r") as config_file:
    config = json.loads(config_file.read())

if not config['username']:
    print("Please add a username to scrape to the config.json file")
    exit()

username=config['username']
url = f"https://old.reddit.com/user/{username}/comments/"
filename = f"./data/{username}.txt"
util.delete_file(filename)


def get_page_comment_list(url):
    comment_page_info = reddit.fetch_reddit_page(url)
    print(comment_page_info["status_code"], " : ", comment_page_info["url"])
    soup = comment_page_info["soup"]


    local_comment_list = reddit.fetch_full_comment_page_as_list(soup)


    def thread_func(comment):
        context_page_info = reddit.fetch_reddit_page(comment.comment_context_link)
        print(context_page_info["status_code"], " : ", context_page_info["url"])
        parent = reddit.get_parent_comment_element(context_page_info, comment.comment_id)

        if parent == "removed":
            parent = "The child comment was most likely shadow removed."
        elif parent is not None:
            parent = parent.find(class_="usertext-body").get_text().strip()

        comment.comment_parent = parent

    threads = []
    for comment in local_comment_list:
        the_thread = threading.Thread(target=thread_func, args=(comment,))
        the_thread.start()
        threads.append(the_thread)

    for thread in threads:
        thread.join()
    
    # delete file?
    with open(filename, "a") as file:
        out = []
        for comment in local_comment_list:
            values = comment.__dict__
            out.append(values)
        file.write(json.dumps(out))

    next_page = reddit.get_next_page(soup)
    if next_page:
        get_page_comment_list(next_page)


get_page_comment_list(url)
