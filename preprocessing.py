#This is for preprocessing the data from the twitter retrieval stage

class preprocessing():
    import preprocessor as p
    import pandas as pd
    import re
    def __init__(self,data):
        self.data = data
    def clean(self):
        processed_tweet= [self.p.clean(tweet) for tweet in self.data]
        self.clean_tweets = [self.re.sub(r'\(|\)|,|:|;|\'|\.+?|-','', tweet).lower() for tweet in processed_tweet]
        return self.clean_tweets
    def csv_convert(self,name):
        DF = self.pd.DataFrame(columns = ['Tweets'])
        DF['Tweets'] = self.clean_tweets
        DF.to_csv('{}'.format(name),index=False)

processing_object = preprocessing(tweets) # This accepts a list of tweets
clean_tweets = processing_object.clean() # For cleaning 
processing_object.csv_convert('processed_tweets.csv') # For importing 