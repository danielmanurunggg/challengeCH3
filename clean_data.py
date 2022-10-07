import re
import pandas as pd
from unidecode import unidecode
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory, StopWordRemover, ArrayDictionary
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import csv

kamus = pd.read_csv('data/new_kamusalay.csv', names = ['sebelum', 'sesudah'], encoding='latin-1')

number = 0

#Membuat factory dan Melihat kata stop words yang ada di library safari
factory = StopWordRemoverFactory()
stopwords = factory.get_stop_words()
#nambahin stopword jika kurang
#memasukan data untuk proses normalisasi ke dalam variable bentuk array 1D
with open('data/stopword.csv', newline='') as csvfile:
    data_stopword_id = list(csv.reader(csvfile))

data_stopword_id
stopword_more = [item for sublist in data_stopword_id for item in sublist]
data_stopwords = stopwords + stopword_more
dictionary = ArrayDictionary(data_stopwords)
stopword = StopWordRemover(dictionary)

def _stopword_removal(content):
  text_add_space = re.sub(r" ","  ",str(content))
  tweet_remove = stopword.remove(text_add_space)
  text_remove_space = re.sub(r"  "," ",str(tweet_remove))
  tweet_clear = text_remove_space.strip()
  return tweet_clear

def _toLower(s): return s.lower()

def _remove_punct(s): 
    s = re.sub('[()!?]', ' ', s)
    s = re.sub('\[.*?\]',' ', s)
    s = re.sub(r"[^\w\d\s]+", "", s)
    s = re.sub(r"[^a-z0-9]"," ", s)
    return s

def _remove_space(s): 
    s = re.sub(' +', ' ', s)
    s = s.strip()
    return s

def _remove_link(s):
    s = re.sub(r'http\S+', '', s)
    s = re.sub(r"www.\S+", "", s)
    return s

def _remove_hastag(s):
    s = re.sub("@[A-Za-z0-9_]+","", s)
    s = re.sub("#[A-Za-z0-9_]+","", s)
    return s

def _remove_another_text(s):
    s = re.sub(r"rt", "", s)
    s = re.sub(r"user", "", s)
    s = re.sub(r'[^\x00-\x7f]',r'', s)
    return s

def _remove_another_file(s): 
    s = re.sub(r"rt", "", s)
    s = re.sub(r"user", "", s)
    return re.sub(r"\\x[A-Za-z0-9./]+", "", unidecode(s))

def _normalization(s):
  global number
  words = s.split()
  clear_words = ""
  for val in words:
    x = 0
    for idx, data in enumerate(kamus['sebelum']):
      if(val == data):
        clear_words += kamus['sesudah'][idx] + ' '
        print(number,"Transform :",data,"-",kamus['sesudah'][idx])
        x = 1
        number += 1
        break
    if(x == 0):
      clear_words += val + ' '
  return clear_words

factory = StemmerFactory()
stemmer = factory.create_stemmer()
i = 0
def _stemming(content):
  global i
  i +=1
  stem = stemmer.stem(content)
  print(i,"Before :", content)
  print("After :", stem,"\n")
  return stem