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
def get_stopwords():
    commom_words = ['tambem', 'sido', 'todas', 'todos', 'assim', 'alguns', 'alem', 'ainda', 'duas', 'desses', 'deste',
                    'nao', 'um', 'dois', 'tres', 'quatro', 'cinco', 'seis', 'sete', 'oito', 'nove', 'dez', 'onze', 'doze', 
                    'treze', 'quartoze', 'quinze', 'dezesseis', 'dezesete', 'dezoito', 'dezenove', 'vinte', 'trinta', 
                    'quarenta', 'cinquente', 'sessenta', 'setenta', 'oitenta', 'noventa', 'cem', 'sao', 'pode', 'podem',
                    'resultados', 'pacientes', 'objetivo', 'metodo', 
                    'conclusoes', 'conclusao', 'dados', 'et', 'al']
    
    stopword = set(stopwords.words('portuguese') + list(punctuation) + commom_words)
    return stopword
def remove_stopwords(text):
    stopword = get_stopwords()
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
    ind_remove_number = 1
    dataset = []
    
    for row in category_text_list:
        text = row[text_position]
        category = row[category_position]

        if ind_lower:
            text = text.lower()
            
        if ind_remove_stopwords:
            text = remove_stopwords(text)

        if ind_remove_special_character:
            text = remove_special_character(text)

        if ind_stemmer:
            text = stemmer(text)
            
        if ind_remove_number:
            text = ''.join(i for i in text if not i.isdigit())

        dataset.append([category, text])
        
    if to_pandas:
        column_names = ['category', 'text']
        dataset = array_to_pandas(dataset, column_names)
        
    return dataset