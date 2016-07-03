import pprint

import static_tl.config
import static_tl.twitter_api

def main():
    print("Getting list of people you follow")
    config = static_tl.config.get_config()
    api = static_tl.twitter_api.get_api(config)
    for user in api.friends.list()["users"]:
        print("@" + user["screen_name"])


if __name__ == "__main__":
    main()
