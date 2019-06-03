import os
import json

from sklearn.feature_extraction.text import CountVectorizer

from scrapping_code import Get_Python_Code
from scrapping_text import Get_Text_Samples

class Nlp_Model:

    def get_words_and_sentences(self):
        """Using Get_Python_Code() and  Get_Text_Samples() classes, put all_sentences together"""

        
        self.code_samples_obj = Get_Python_Code()

        self.code_samples_obj.get_list_of_urls_from_geeksforgeeks()
        self.code_samples_obj.get_code_from_url('whatever')

        self.code_samples_obj.clean_out_comments()
        self.code_samples_obj.remove_inside_quotes()
        self.code_samples_obj.remove_inside_brackets()

        self.code_samples_obj.remove_variables()
        self.code_samples_obj.clean_out_digits()
        self.code_samples_obj.clean_out_punctuation()
        self.code_samples_obj.split_values()
        self.code_samples_obj.split_values(split_element=".")

        self.code_samples_obj.clean_out_empty()
        self.code = self.code_samples_obj.code
        
        self.len_code = len(self.code)

        self.text_samples = Get_Text_Samples()

        self.text_samples.get_url()
        self.text_samples.split_to_n_samples(200)
        self.text_samples.clean_stop_words_and_punct()

        self.quotes = self.text_samples.quotes
        self.len_quotes = len(self.quotes)
        
        
        self.all_sentences = self.code + self.quotes
        
        # Save sentences to file:
        self.save_all_sentences()

        
    def save_all_sentences(self):
        """Write all_sentences object to a file"""
        self.current_path = os.getcwd()
        with open('{}/all_sentences'.format(self.current_path),'wb') as f_obj:
            f_obj.write(json.dumps(self.all_sentences))

    def vectorize_fit(self):
        """Build a vocabulary out of all_sentences using CountVectorizer"""
        self.vectorizer = CountVectorizer()
        self.vectorizer.fit(self.all_sentences)

    def vectorize_transform(self):
        """Build a vector out of all sentences and build the corresponding array"""
        self.vector = self.vectorizer.transform(self.all_sentences)
        self.vector_array = self.vector.toarray()