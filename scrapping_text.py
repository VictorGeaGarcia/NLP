import requests

from bs4 import BeautifulSoup

from nltk import word_tokenize
from nltk.corpus import stopwords

class Get_Text_Samples:
    
    def get_url(self):
        """
        Crawling "webpage" containing paragraphs with only text.
        :return: self.quotes attribute is a list containing a bunch of quotes
        """
        self.url = 'http://wisdomquotes.com/famous-quotes/'
        self.request = requests.get(self.url).content
        self.soup = BeautifulSoup(self.request)
        self.blockquotes = self.soup.find_all("blockquote")
        self.quotes = [self.quote.find('p').text for self.quote in self.blockquotes]
        self.quotes = [".".join(self.quote.rsplit('.')[:-1]) for self.quote in self.quotes]
        
    def split_to_n_samples(self,amount_of_samples):
        """"
        Method that allows us to get a max. amount of sentences to balance it with the amount of samples with code
        """
        self.amount_of_samples = amount_of_samples
        self.quotes = self.quotes[:self.amount_of_samples]
    
    def clean_stop_words_and_punct(self):
        """
        Remove stopwords and punctuation
        :return:
        """
        
        self.stopwords = stopwords.words('english')
        self.cleaned_sentences = []
        
        for self.sentence in self.quotes:
            self.sentence = word_tokenize(self.sentence)
            
            #Remove punctuation
            self.sentence = [self.word.lower() for self.word in self.sentence if self.word.isalpha()]
            
            #Remove stopwords
            self.sentence = list(set(filter(lambda x: x not in self.stopwords, self.sentence)))
            self.sentence = " ".join(self.sentence)
            
            self.cleaned_sentences.append(self.sentence)
        self.quotes = self.cleaned_sentences