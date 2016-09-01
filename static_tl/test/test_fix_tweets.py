from static_tl.gen import fix_urls

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
    fix_urls(tweet)
    assert tweet["fixed_text"] ==  """
Here's a link: <a href="http://long-url-at-example.com">http://long-url-...</a>. I like it
""".strip()
