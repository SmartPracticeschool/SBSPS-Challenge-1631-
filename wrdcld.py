import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import nltk
from nltk.tokenize import word_tokenize
import pickle

# Download 'punkt' by uncommenting and executing the command below 
#nltk.download('punkt')


def words_plot( text , MAX = 70 , minsize = 4 ):

    infile = open("stopsetwords",'rb')
    stopset = pickle.load(infile)

    tokens_without_sw = [word for word in word_tokenize(text) if not word in stopset]

    wordcount = {}
    for a in tokens_without_sw:
        if a  in wordcount:
            wordcount[a] +=1
        else:
            wordcount[a] = 1

    wc = WordCloud(background_color = 'white',max_words= MAX , min_font_size= minsize)
    wc.generate_from_frequencies(frequencies=wordcount)
    fig = plt.figure()
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")

    #plt.savefig('test.png')

    return fig
    

if __name__ == "__main__":
    text = "q w s e s a w q d t w d r t d g f d g v e g e fdf sc sfg tyjh yuk ui hn gbt"
    fig = words_plot(text, 3)
    
    

