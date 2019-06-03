import requests
from bs4 import BeautifulSoup
import re

class Get_Python_Code:
    
    def get_list_of_urls_from_geeksforgeeks(self):
        """
        Crawling "geeksforgeeks" webpage to get links where there are many python examples.
        :return: self.links attribute is a list containing a bunch of links inside "geekforgeeks"
        """
        self.url_full = "https://www.geeksforgeeks.org/python-programming-examples/"
        self.url_full_content = requests.get(self.url_full).content
        self.full_soup =BeautifulSoup(self.url_full_content)
        
        self.classes = ['simple', 'array', 'list', 'string', 'dictionary', 'tuple', 'searchingandsorting', 'pattern', 
                        'datetime', 'moreprograms']
        
        self.links = []
        for web_class in self.classes:
            self.links_soup = self.full_soup.find("div",{"class":web_class})
            self.links_li = self.links_soup.find_all('li')
            self.links.extend([self.link.find('a')['href'] for self.link in self.links_li])

    def get_code_from_url(self, web_url):
        """
        Using list of links from geeksforgeeks, crawl python code.
        If you want to use some other webpage(s) to crawsl the code in here needs to be adapted.
        :param web_url: should be a list of links to be crawled
        :return: list of lists, with each list containing full raw code from webpage
        """

        self.code = []
        
        if self.links:
            self.web_url = self.links
        else:
            self.web_url = web_url
            
        if isinstance(self.web_url,list):
            for element in self.web_url:
                self.url_content = requests.get(element).content
                self.soup = BeautifulSoup(self.url_content)

                self.code_block = self.soup.find("div", {"class": "code-container"})
                self.code_block = self.code_block.find("div",{"class":"container"})

                self.code_partial = []
                for line in self.code_block.find_all('div'):
                    self.code_partial.append(" ".join(element.text.strip() for element in line.find_all('code')))
                
                self.code_partial = [x.replace(u'\xa0', u'').strip() for x in self.code_partial]
                self.code_partial = filter(lambda x: x, self.code_partial)
                self.code.append(self.code_partial)

    def clean_out_comments(self):
        """
        Remove comments
        """
        self.code_no_comments = []
        for self.block_code in self.code:
            self.block_code = filter(lambda x: not(x.strip().startswith('#')), self.block_code)
            self.block_code = filter(lambda x: not(x.strip().startswith('//')), self.block_code)
            
            self.code_no_comments.append(self.block_code)
        self.code = self.code_no_comments
    
    
    def clean_out_punctuation(self):
        """
        Remove punctuation symbols
        """
        # TODO: Remove symbols but counting them, and add keep this number along with the sentence it correlates to.
        #       Text with more symbols are more likely code. This number can be used in the model. Add to this counting
        #       =, ' and " ( which are not removed here because we need them for later cleaning
        self.code_no_punct = []
        for self.block_code in self.code:
            self.code_no_punct.append([re.subn(r"[()<>{}[\]*&\+\*\\\/:;,]", "", x.strip().lower())[0].strip() for x in self.block_code])
        self.code = self.code_no_punct
    
    def remove_inside_brackets(self):
        """
        Remove everything inside brackets, parenthesis etc.
        """
        self.code_no_brackets = []
        for self.block_code in self.code:
            self.block_code = [re.subn(r'\((.*?)\)', ' ', x)[0].strip() for x in self.block_code]
            self.block_code = [re.subn(r'\{(.*?)\}', ' ', x)[0].strip() for x in self.block_code]
            self.code_no_brackets.append([re.subn(r'\[(.*?)\]', ' ', x)[0].strip() for x in self.block_code])
        self.code = self.code_no_brackets
        
    def remove_inside_quotes(self):
        """Remove everything inside brackets. Stuff in comments will be misleading since it's normal text"""
        self.code_no_quotes = []
        for self.block_code in self.code:
            self.block_code = [re.subn(r"\'(.*?)\'",' ',x)[0].strip() for x in self.block_code]
            self.code_no_quotes.append([re.subn(r'\"(.*?)\"', ' ', x)[0].strip() for x in self.block_code])
        self.code = self.code_no_quotes
        
    def remove_variables(self):
        """Remove everything to the left of something with an assignment.
           These will be variable names, so it would only add noise to they model.
        """
        self.code_no_variables = []
        for self.block_code in self.code:
            self.block_code = [x.split('=')[0] for x in self.block_code]
            self.code_no_variables.append(self.block_code)
        self.code = self.code_no_variables
    
    def clean_out_digits(self):
        """Remove digits"""
        # TODO: Keep count of the amount of digits removed. This number can be used in the model.
        self.code_no_digits = []
        for self.block_code in self.code:
            self.block_code = [re.subn(r'\d',' ',x)[0].strip() for x in self.block_code]
            self.code_no_digits.append(self.block_code)
        self.code = self.code_no_digits
        
    def split_values(self, split_element=" "):
        """Function to split elements by split_element defined"""
        self.split_element = split_element
        self.splited_list = []
        for self.block_code in self.code:
            self.splited_sublist = []
            for self.element in self.block_code:
                self.splited_sublist.extend(self.element.split(self.split_element))
            self.splited_list.append(self.splited_sublist)
        self.code = self.splited_list
        
    def clean_out_empty(self):
        """
        Remove empty strings and strings with length = 1
        """
        self.code = [list(set(filter(lambda x:x, self.cleaned_list))) for self.cleaned_list in self.code]
        self.code = [list(set(filter(lambda x: len(x)>1, self.cleaned_list))) for self.cleaned_list in self.code]
        self.code = [" ".join(x) for x in self.code]
        

