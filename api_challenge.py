from flask import Flask, request, jsonify
import re
import pandas as pd

app = Flask(__name__) # deklarasi Flask

kamus = pd.read_csv('data/new_kamusalay.csv', names = ['sebelum', 'sesudah'], encoding='latin-1')

def _toLower(s):
    return s.lower()

def _remove_punct(s):
    return re.sub(r"[^\w\d\s]+", "", s)

def _remove_link(s):
    return re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))',' ',s)

def _remove_another(s):
    s = re.sub(r"rt", "", s)
    s = re.sub(r"user", "", s)
    s = (re.sub(r'[^\x00-\x7f]',r'', s))
    return s

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

if __name__ == "__main__":
    app.run(port=1234, debug=True) # debug ==> kode otomatis update ketika ada perubahan