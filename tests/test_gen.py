from twitt_back.gen_html import *

def test_fix_urls():
    expanded_url = "http://example.com"
    urls = [
      { "expanded_url" : expanded_url,
        "indices" : [20, 43]
      }
    ]
    entities = dict()
    entities["urls"] = urls
    tweet = dict()
    tweet["entities"] = entities
    t_co_url = 'https://t.co/hpxC6xgHs0'
    tweet["text_as_html"] = "I now have a blog : %s See you there :)" % t_co_url
    fix_urls(tweet)
    expected = '<a href="{0}">{0}</a>'.format(expanded_url)
    assert tweet["text_as_html"] == "I now have a blog : %s See you there :)" % expected
