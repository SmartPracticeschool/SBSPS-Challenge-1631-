consumer_key= '************************'
consumer_secret= '***************************'
access_token= '*************************'
access_token_secret= '**********************'

class Twitter_Crawler():
    import datetime
    import tweepy as tw
    import json 
    def __init__(self, consumer_k,consumer_secrt,access,access_secrt):
        self.consumer_k = consumer_k
        self.consumer_secrt = consumer_secrt
        self.access = access
        self.access_secrt = access_secrt
        self.auth()
    def get_tweet(self,search_w,tweet_no,days):
        current = self.datetime.datetime.today()
        previous = self.datetime.datetime.today() - self.datetime.timedelta(days=days)
        tweets = self.tw.Cursor(self.api.search,q=search_w,lang="en",since=str(previous)[:10], until = str(current)[:10]).items(tweet_no)
        if days >=7:
            print("\n WARNING: May not get older tweets.....")
        try:
            tweet_list = [tweet.text for tweet in tweets]
            
        except:
            print('Invalid Twitter Call')
        if len(tweet_list) is 0:
            print('WARNING: No results obtained...')
        return tweet_list
            
    def auth(self): # This checks for authentication 
        auth = self.tw.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = self.tw.API(auth, wait_on_rate_limit=True)
    def get_status_tweets(self,id):
        status =self.api.get_status(id)
        return self.json.loads(status)
    
search_words = "covid AND india OR lockdown OR govt OR happy OR sad OR excited OR glad" + ' -filter:retweets' # For searching the tweets to find the relevant tweets using keywords
twitter_obj = Twitter_Crawler(consumer_key,consumer_secret,access_token,access_token_secret)
tweets = twitter_obj.get_tweet(search_words,1000,10) # This accepts search keyword, tweet count , previous day cout till we need the tweets till
