import os

def format_dataset(path):
    """
    create dataset in the format 
    :param path: caminho da pasta raiz contendo as pastas de cada classe com os respectivos resumos
    :return: array with three columns
    """
    categories = [f for f in os.listdir(path) if not f.startswith('.')]
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
    return dataset
    
# class MedicalTextClassifier:
#     def __init__(self):
        

    