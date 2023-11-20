util.get_reddit_user_comment_page("samaltman")


soup = util.fetch_reddit_page()
comments = util.get_comments(soup) 



for comment in comments:
    
    context_page = util.fetch_reddit_page(comment.comment_parent)
    parent_id = get_parent_element_id(element)
    comment.



for item in soup.select(".entry"):
    item_dict = {
        "text": item.select(".usertext-body")[0].text.replace("\n", ""),
        "context_url": item.find(
            attrs={'data-event-action':"context"}
            ).get('href')
    }

    fetch_parent_comment(item_dict)
    data.append(item_dict)