## NLP FOR CHECKING IF A TEXT BLOCK CONTAINS PYTHON CODE

We are going to crawl some webpages where we know that there is text with Python code and text without code.
Once we have the required data, we  will use **CountVectorizer()** from the **scikit-learn** package to 
vectorize our sentences so that we can later on use it in some machine learning models.

-----------------

### SETUP

Pyhton Version:  2.7.15

Install libraries from ``pip_list`` file (recommended to use a virtual environment):

```bash
pip install -r requirements.txt
```

---------

### Info about files in repo

`scrapping_code.py` and `scrapping_text.py` contain the modules to get samples of sentences both containing code
and not containing it.

 `nlp_code.py` uses `scrapping_code.py` and `scrapping_text.py` files to create `all_sentences` file, which
 contains examples with and without python code.
 
 `trying_classif_models.py` creates a model with `nlp_code_python_{}.h5` name, using vectorized sentences coming from
 `nlp_code` module.
 
 `predict_new_sentences.py` applies the created model in new sentences.
 
 --------------
 ## 1. Create model
 
 Run:
 
 ```python
 python trying_classif_models.py
 ```
 
 It takes a bit since it needs to crawl the webpages and later on run the model.
 
 2. Use `predict_new_sentences.py` file to try out the model. i.e run:
 
 ```python
python predict_new_sentences.py --new-sentences 'This should not be taken as code'

```


```python
python predict_new_sentences.py --new_sentences '
def set_pwd():
    x = raw_input("Enter the pwd")
    y = raw_input("Confirm the pwd")
'
```

 
 
 ### Next steps
 
 1. More samples should be added to make a more complete example.
 2. Doing some current TODOs should help improve the model.
 3. Model in `trying_classif_models.py` could be improved by adding more layers.
 4. Use some different input and create a similar model for `sql` and `java` examples.
 