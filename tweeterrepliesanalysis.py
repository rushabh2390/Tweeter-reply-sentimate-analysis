
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import unicodedata2
import sys
from tkinter import *
import tkinter

import nltk.classify.util
from nltk.corpus import names
from nltk.corpus import stopwords
import numpy as np
from matplotlib import pylab
from textblob.classifiers import NaiveBayesClassifier
acrp=0
plid,lid=None,None
parsed_tweet={}
tweets=[]
choice=None
def word_feats(words):
    return dict([(word, True) for word in words])
positive_vocab = [  ]
negative_vocab = [ ]
neutral_vocab = [ ]    
positive_features = []
negative_features = []
neutral_features = []
train_set = None
classifier = None
train = [
    ('I love this sandwich.', 'pos'),
    ('This is an amazing place!', 'pos'),
    ('I feel very good about these beers.', 'pos'),
    ('This is my best work.', 'pos'),
    ("What an awesome view", 'pos'),
    ('I do not like this restaurant', 'neg'),
    ('I am tired of this stuff.', 'neg'),
    ("I can't deal with this", 'neg'),
    ('He is my sworn enemy!', 'neg'),
    ('My boss is horrible.', 'neg')
]
c1 = NaiveBayesClassifier(train)
def trainset(ch):
    global positive_vocab,negative_vocab,neutral_vocab
    global positive_features,negative_features,neutral_features
    global train_set
    global classifier
    if str(ch)=="Chracter":
        positive_vocab = [ 'awesome', 'outstanding', 'fantastic', 'terrific', 'good', 'nice', 'great', ':)' ]
        negative_vocab = [ 'bad', 'terrible','useless', 'hate', ':(' ]
        neutral_vocab = [ 'movie','the','sound','was','is','actors','did','know','words','not' ]
    elif str(ch)=="Product":
        positive_vocab = [ 'bad', 'outstanding', 'fantastic', 'terrific', 'good', 'nice', 'great', ':)' ]
        negative_vocab = [ 'awesome', 'terrible','useless', 'hate', ':(' ]
        neutral_vocab = [ 'movie','the','sound','was','is','actors','did','know','words','not' ]
    else:
        positive_vocab = [ 'awesome', 'outstanding', 'fantastic', 'terrific', 'good', 'nice', 'great', ':)' ]
        negative_vocab = [ 'bad', 'terrible','useless', 'hate', ':(' ]
        neutral_vocab = [ 'movie','the','sound','was','is','actors','did','know','words','not' ]    
    positive_features = [(word_feats(pos), 'pos') for pos in positive_vocab]
    negative_features = [(word_feats(neg), 'neg') for neg in negative_vocab]
    neutral_features = [(word_feats(neu), 'neu') for neu in neutral_vocab]
    train_set = negative_features + positive_features + neutral_features
    classifier = nltk.NaiveBayesClassifier.train(train_set)

class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''
    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = ''
        consumer_secret = ''
        access_token = ''
        access_token_secret = ''
 
        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth, wait_on_rate_limit=True)
        except:
            print("Error: Authentication Failed")
 
    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
 
    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet),classifier=c1)
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
 
    def get_tweets(self, query,sid,no,mid=None):
        '''
        Main function to fetch tweets and parse them.
        '''
        
        global acrp,plid
        
        if acrp!=no:
            if mid==None:
                plid=None
                lid=None
            else:
                lid=int(mid)
            try:
                
                non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
                fetched_tweets = self.api.search_tweets(q ="@"+query,since_id=sid,max_id=mid,count=200)
                
                try:
                    i=0
                    emoji_pattern = re.compile("["u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)
                    f=open("replies.txt","a",encoding="utf-8")
                    for status in fetched_tweets:
                        
                        parsed_tweet={}
                        if str(acrp)==str(no):
                            break
                        if(status._json['in_reply_to_status_id_str']==sid):
                            try:
                                
                                print("geo",status._json['geo'],' ')
                                print("place",status._json['place'],' ')
                                print("location",status.user.location,'<br/>')
##                                txt=str(status.text).translate(non_bmp_map)
                                txt=emoji_pattern.sub(r'',status.text)
                                txt=txt.lower()
                                txt=re.sub(r'(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w\.-]*)*\/?\S', '', txt)
                                txt= re.sub(r'#','', txt)
##                                txt=txt.replace("@"+query,'')
                                txt=' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",txt).split())
                                if txt!='' or txt==None:
                                    parsed_tweet['text']=txt
                                    parsed_tweet['sentiment'] = self.get_tweet_sentiment(txt)
                                    acrp+=1
                                    f.write(txt)
                                    
                                    if len(tweets)>0:
                                        if parsed_tweet not in tweets:
                                            tweets.append(parsed_tweet)
                                    else:
                                        tweets.append(parsed_tweet)
    ##                            print(status.text)
##                                print("acrp",acrp)
                                        
                                
                                
                            except UnicodeEncodeError:
                                print("---------------------------------------error here-------------------------------------------------------")
                                print(status.text)
                                
                        if(lid==None or lid>int(status._json['id'])):
                            lid=int(status._json['id'])
                            
                        i+=1
                        
                
                finally:
                    f.close();
                if(lid==None or lid!=int(sid)+1):
                    if(plid!=lid and acrp!=no):
                        plid=lid
                        self.get_tweets(query,sid,no,lid)
                        return
                    else:
                        return
     
            except Exception as e:
                print("Error : " + str(e))
        else:
            return
        
        return
    def get_tweets_wtno(self, query,sid,mid=None):
        '''
        Main function to fetch tweets and parse them.
        '''
        
        global acrp,plid
        
        
        if mid==None:
            plid=None
            lid=None
        else:
            lid=int(mid)
        try:
            
            non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
            fetched_tweets = self.api.search(q ="@"+query,since_id=sid,max_id=mid,count=200)
            try:
                i=0
                emoji_pattern = re.compile("["u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
                f=open("replies.txt","a",encoding="utf-8")
                for status in fetched_tweets:
                    parsed_tweet={}
                    if(status._json['in_reply_to_status_id_str']==sid):
                        try:
                            print(status._json['place'])
##                                txt=str(status.text).translate(non_bmp_map)
                            txt=emoji_pattern.sub(r'',status.text)
                            txt=txt.lower()
                            txt=re.sub(r'(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w\.-]*)*\/?\S', '', txt)
                            txt= re.sub(r'#','', txt)
##                                txt=txt.replace("@"+query,'')
                            txt=' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",txt).split())
                            if txt!='' or txt==None:
                                parsed_tweet['text']=txt
                                parsed_tweet['sentiment'] = self.get_tweet_sentiment(txt)
                                acrp+=1
                                f.write(txt)
                                
                                if len(tweets)>0:
                                    if parsed_tweet not in tweets:
                                        tweets.append(parsed_tweet)
                                else:
                                    tweets.append(parsed_tweet)
##                            print(status.text)
##                                print("acrp",acrp)
                                    
                            
                            
                        except UnicodeEncodeError:
                            print("---------------------------------------error here-------------------------------------------------------")
                            print(status.text)
                            
                    if(lid==None or lid>int(status._json['id'])):
                        lid=int(status._json['id'])
                        
                    i+=1
                    
            
            finally:
                f.close();
            if(lid==None or lid!=int(sid)+1):
                if(plid!=lid):
                    plid=lid
                    self.get_tweets_wtno(query,sid,lid)
                    return
                else:
                    return
 
        except Exception as e:
            print("Error : " + str(e))
        
        
        return
 
def main(uname,sid,no):
    # creating object of TwitterClient Class
    api = TwitterClient()
    f=open('replies.txt','w',encoding="utf-8")
    f.close()
    global acrp
    acrp=0
    # calling function to get tweets
    if(str(no)==0):
        api.get_tweets_wtno(uname,sid)
    else:
        api.get_tweets(uname,sid,no)
    
    print("Total replies are:",acrp)
    ptweets=[tweet for tweet in tweets if tweet['sentiment']=='positive']
    ntweets=[tweet for tweet in tweets if tweet['sentiment']=='negative']
    netweets=[tweet for tweet in tweets if tweet['sentiment']=='neutral']
##    print(tweets)
    positive=(len(ptweets)/len(tweets))*100
    negative=(len(ntweets)/len(tweets))*100
    neutral=(len(netweets)/len(tweets))*100
    print('<br/><b>Positive tweets: </b><br/>')
    for tweet in ptweets:
        print(tweet['text'],"<br/>")
    
    print('<br/><b>Negative tweets:</b><br/> ')
    for tweet in ntweets:
        print(tweet['text'],"<br/>")
        
    print('<br/><b>Neutral tweets: </b><br/>')
    for tweet in netweets:
        print(tweet['text'],"<br/>")
    label="positive","negative","neutral"
    size=[positive,negative,neutral]
    explode=(0.05,0.05,0.05)
    color=["#00CC00","#CC0000","#0000CC"]
    p,tx,autotexts=pylab.pie(size,explode=explode,autopct='%1.1f%%',labels=label,startangle=90,colors=color)
    pylab.axis('equal')
    for autotext in autotexts:
        autotext.set_color('white')
    pylab.title("Twitter replies analysis sentencewise")
    pylab.savefig(sid)
    print('<br/><b>Twitter analysis sentencewise : </b>','<br/><b>Positive: </b>' , positive,'<br/><b>Negative:</b> ' , negative,'<br/><b>Neutral:</b> ' , neutral)
    print('<br/><b>Twitter analysis wordwise : </b>')
    sentimateanalysis(uname,sid)
    
def sentimateanalysis(unm,sid):
    
    # Predict
    neg = 0
    pos = 0
    neu = 0
    pos_word=[]
    neg_word=[]
    neu_word=[]
    sentence=None;
    f=open('replies.txt','r',encoding="utf-8")
    for i in f:
        if(sentence==None):
            sentence=str(i)
            
        else:
            sentence+=" "+str(i)
    ##sentence = "I hate you like a love you"
    f.close()
    if(sentence!=None):
        sentence = sentence.lower()
        sentence=sentence.replace("@"+unm,'')
        stop=set(stopwords.words('english'))
        sentence=' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",sentence).split())
        words = [i for i in sentence.split(' ') if i not in stop]
        for word in words:
            classResult = classifier.classify( word_feats(word))
            if classResult == 'neg':
                neg_word.append(word)
                neg = neg + 1
            if classResult == 'pos':
                pos_word.append(word)
                pos = pos + 1
            if classResult == 'neu':
                neu_word.append(word)
                neu = neu + 1
        positive=(float(pos)/len(words))*100
        negative=(float(neg)/len(words))*100
        neutral=(float(neu)/len(words))*100
        print('<br/><b>Positive: </b>' , str(positive),'<br/><b>Negative:</b> ' , str(negative),'<br/><b>Neutral:</b> ' , str(neutral))
        print("<br/><b>positive words are:</b>",pos_word,"<br/><b>negative words are:</b>",neg_word,"<br/><b>neutral words are:</b>",neu_word)
        
##        label="positive","negative","neutral"
##        size=[positive,negative,neutral]
##        explode=(0.05,0.05,0.05)
##        color=["#00CC00","#CC0000","#0000CC"]
##
##        p,tx,autotexts=pylab.pie(size,explode=explode,autopct='%1.1f%%',labels=label,startangle=90,colors=color)
##        pylab.axis('equal')
##        for autotext in autotexts:
##            autotext.set_color('white')
##        pylab.title("Twitter replies analysis wordwise")
##        name="wordwise_"+str(sid)
##        pylab.savefig(name)
##        pylab.show()

 
if __name__ == "__main__":
    link=sys.argv[1]
    no=sys.argv[2]
    ch=sys.argv[3]
    trainset(ch)
##    link="https://twitter.com/sambitswaraj/status/969231057542352898"
##    no=10
    
##    print(link)
    link=link.replace('//','/')
    a=link.replace('/',' ')
    
    a=a.split(' ')

##    print(a)
##    print(a[2],a[4],"<br>",no)
    main(a[2],a[4],no)
##    sentimateanalysis(a[2],a[4])
