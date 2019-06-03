import json
import argparse
import os

from sklearn.feature_extraction.text import CountVectorizer
from tensorflow.keras.models import load_model



parser = argparse.ArgumentParser()
parser.add_argument('--new_sentences', dest='new_sentences', type=str)
args = parser.parse_args()

new_sentences = args.new_sentences
current_path = os.getcwd()
with open('{}/all_sentences'.format(current_path),'rb') as f_obj:
    all_sentences = json.load(f_obj)


def predict(new_sentences):
    
    vectorizer = CountVectorizer()
    vectorizer.fit(all_sentences)
    vector = vectorizer.transform([new_sentences])
    vector_array = vector.toarray()
    model = load_model('nlp_code_python_1000.h5')
    
    output = model.predict_classes(vector_array)
    print('Sentence contains code' if output[0][0] else 'Sentence doesnot contain code')
    #print(output)

predict(new_sentences)