import os
import pandas as pd

from nltk.corpus import stopwords
from string import punctuation
from nltk.stem import RSLPStemmer
from unicodedata import normalize


## [load_data] TO-DO
## Coletar pelo menos 100 textos de cada classe

## [preprocessing] TO-DO:
## remover numeros
## remover numeros por extenso
## criar grid search de pre-processamento


## Load Data Functions
def get_categories(path):
    return [f for f in os.listdir(path) if not f.startswith('.')]

def array_to_pandas(array, column_names):
    """
    create dataset in the format 
    :param path: caminho da pasta raiz contendo as pastas de cada classe com os respectivos resumos
    :return: array with three columns
    """
    return pd.DataFrame(array, columns = column_names)
         
    
def format_dataset(path, pandas_dataframe=True):
    """
    create dataset in the format 
    :param path: caminho da pasta raiz contendo as pastas de cada classe com os respectivos resumos
    :return: array with three columns
    """
    categories = get_categories(path)
    dataset = []
    for category in categories:
        for abstract in os.listdir(path+category):
            if not abstract.startswith("."):
                text = ""
                row = []
                with open("{}/{}".format(path+category, abstract)) as f: 
                        for line in f: 
                            text += line 
                row.append(abstract) #file_name
                row.append(category) #category
                row.append(text)
                dataset.append(row)  
                
    if pandas_dataframe:
        column_names = ['file_name', 'category', 'text']
        dataset = array_to_pandas(dataset, column_names)
        
    return dataset


## Preprocessing functions

def remove_stopwords(text):
    commom_words = ['10', '11', '12', '13', '14', '15', '16', '17', '18', '20', '21', '24', '95', 'tambem', 'sido', 
                    'todas', 'todos', 'assim', 'alguns', 'alem', 'ainda', 'dois', 'duas', 'desses', 'deste', 'nao', 
                    'tres', 'quatro', 'cinco', 'seis', 'sete', 'oito', 'nove', 'dez', 'sao', 'pode', 'podem', '10', 
                    '11', '14', '15', '16', '19', '20', '21', '95']
    stopword = set(stopwords.words('portuguese') + list(punctuation) + commom_words)
    text = [word for word in text.split() if word not in stopword]
    return ' '.join(text)

def stemmer(text):
    stemmer = RSLPStemmer()
    new_text = []
    for word in text.split():
        new_text.append(stemmer.stem(word.lower()))
    return ' '.join(new_text)

def remove_special_character(text):
    text = normalize('NFKD', text).encode('ASCII','ignore').decode('ASCII')
    return text

def text_preprocess(category_text_list, category_position=0, text_position=1, to_pandas=True):
    ind_lower = 1
    ind_remove_special_character = 1
    ind_tokenizer = 1
    ind_remove_stopwords = 1
    ind_stemmer = 1
    dataset = []
    
    for row in category_text_list:
        text = row[text_position]
        category = row[category_position]

        if ind_lower:
            text = text.lower()

        if ind_remove_special_character:
            text = remove_special_character(text)

        if ind_remove_stopwords:
            text = remove_stopwords(text)

        if ind_stemmer:
            text = stemmer(text)

        dataset.append([category, text])
        
    if to_pandas:
        column_names = ['category', 'text']
        dataset = array_to_pandas(dataset, column_names)
        
    return dataset

def enumerate_category(path):
    # Transform Label in number
    categories = get_categories(path)
    category_enumerated = {}
    n = 1
    for category in categories:
        category_enumerated[category] = n
        n += 1
    return category_enumerated