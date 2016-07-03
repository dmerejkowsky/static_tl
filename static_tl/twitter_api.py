import twitter

def get_api(config):
    auth_dict = config["auth"]
    keys = ["token", "token_secret",
            "api_key", "api_secret"]
    auth_values = (auth_dict[key] for key in keys)
    auth = twitter.OAuth(*auth_values)
    return twitter.Twitter(auth=auth)
