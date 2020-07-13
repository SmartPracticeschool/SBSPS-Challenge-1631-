import tweepy as tw
import re
from time import time
from preprocessor import clean
import model_utility as ML

class Extractor:
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer
        self.auth = tw.OAuthHandler('NbCf69utHFy0FpMsvOYIxdEm7vX' , 'hXAD7OoQRYeLbOntfCzRVmSg72gqJwa2ZjJbXv779k5TpuM4jEG4')
        self.auth.set_access_token('1272478803051200512-nMmqCtpfYyhxnOu9K7vh7HLqqg69ViE','5zaos8CU69bUbKIAVSdgUBnae6PLOlw5wUGee5c5psfwG6')
        self.api = tw.API(self.auth, wait_on_rate_limit=True)

        self.check_auth()
    
    def check_auth(self):
        try:
            self.api.verify_credentials()
            print("Authentication OK")
        except:
            print("Error during authentication")
    
    def get_data(self, date, keyword, limit):
        d = False
        if __name__ == "__main__":
            d = True

        tweets = tw.Cursor(self.api.search, q=keyword, lang="en", since=date).items(limit)

        if d: print('Data Extracted')
        
        emo_map = {
            0: "sadness",
            1: "joy",
            2: "love",
            3: "anger",
            4: "fear",
            5: "surprise",
            6: "null"
        }
        result = {
            "sadness": 0,
            "joy": 0,
            "love": 0,
            "anger": 0,
            "fear": 0,
            "surprise": 0,
            "null": 0
        }

        tw_list = []

        r_str = ''
        
        if d: print('Cleaning and predicting...')

        t0 = time()

        for i in tweets:
            s = clean(i.text).lower()
            s = re.sub(r'[^A-Za-z\s|n\'t]', '', s)

            r_str += s

            pred = emo_map[ML.predict(self.model, self.tokenizer, s)]
            
            result[pred] += 1

            if pred != 'null':
                tw_list.append([i.text,pred])
                
        t1 = time()

        if d : print('')

        if __name__ == "__main__":
            print('Done.')
            print('Analysis Time :', t1-t0, "s")

        return (result, r_str, tw_list)

if __name__ == "__main__":
    tokenizer = ML.load_tokenizer()
    model = ML.load_model()
    print('Tokenizer and Model loaded.')

    obj = Extractor(model, tokenizer)
    buffer, r_str, tw_list = obj.get_data("2020-6-1", "covid", 1000)
    
    for i,j in buffer.items():
        print(i,j)
  
    





