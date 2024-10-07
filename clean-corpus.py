# boilerplate removal
from bs4 import BeautifulSoup
# regex pour les url
import re
# détection du français
import spacy
from spacy.language import Language
from spacy_langdetect import LanguageDetector

input_file = 'reboisement_reboisement_et_afforestation.txt'
output_file = input_file[:-4] + '_cleaned.txt'

# chargement du modèle
nlp_fr = spacy.load('fr_core_news_lg')

# il faut register le composant avant de l'ajouter dans la pipeline
@Language.factory('language_detector')
def create_language_detector(nlp, name):
    return LanguageDetector()

# ajout dans la pipeline
nlp_fr.add_pipe('language_detector', last=True)

def clean_corpus(corpus, max_size=1000000):
    """
    Split le corpus s'il est trop grand pour être géré par spacy
    la limite actuelle est de 1m de caractères
    """
    chunks = [corpus[i:i + max_size] for i in range(0, len(corpus), max_size)]
    if len(chunks) > 1:
        print(f'Division du corpus en {len(chunks)} chunks.')

    clean_chunks = []
    number = 1
    
    for chunk in chunks:
        if len(chunks) > 1:
            print(f'cleaning chunk {number}...')
        clean_chunks.append(clean_txt(chunk))
        number += 1
      
    print('all done.')
    return ''.join(clean_chunks)
        
def clean_txt(text):
    
    # boilerplate html 
    text = BeautifulSoup(text, "html.parser").get_text()
    
    # Supprime les URL
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)

    text = nlp_fr(text)
    
    # Filtrage par phrase
    cleaned_sentences = []
    for sent in text.sents:
        # ._ = accède a des composants custom
        if sent._.language['language'] == 'fr':
            cleaned_sentences.append(sent.text)
    
    cleaned_text = ' '.join(cleaned_sentences)

    return cleaned_text

print(f'Trying to read {input_file} ...')
with open(input_file, 'r', encoding='utf-8') as file:
    print('reading...')
    corpus = file.read()
    
cleaned = clean_corpus(corpus)

print(f'Trying to write to {output_file} ...')
with open(output_file, 'w', encoding='utf-8') as file:
    print('writing...')
    file.write(cleaned)
