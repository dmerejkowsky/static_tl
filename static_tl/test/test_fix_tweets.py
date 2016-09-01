from static_tl.gen import replace_t_co_urls

def test_replace_t_co_urls_href():
    tweet = {
        "entities" : {
            "urls" : [
                {
                    "expanded_url" : "http://long-url-at-example.com",
                    "display_url" : "http://long-url-...",
                    "indices": [15, 23],
                }
            ]
        },
        "fixed_text" : "Here's a link: t.co/foo. I like it"
    }
    replace_t_co_urls(tweet)
    assert tweet["fixed_text"] ==  """
Here's a link: <a href="http://long-url-at-example.com">http://long-url-...</a>. I like it
""".strip()


def test_replace_t_co_urls_img():
    tweet = {
        "entities" : {
            "media" : [
                {
                    "type" : "photo",
                    "media_url_https" : "https://twitter/pic.png",
                    "indices": [18, 26],
                }
            ]
        },
        "fixed_text" : "Here's a picture: t.co/foo. It's pretty"
    }
    replace_t_co_urls(tweet)
    assert tweet["fixed_text"] ==  """
Here's a picture: <img src="https://twitter/pic.png"></img>. It's pretty
""".strip()
