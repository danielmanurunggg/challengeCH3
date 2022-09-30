from flask import Flask, request, jsonify
import re
import pandas as pd

app = Flask(__name__) # deklarasi Flask

kamus = pd.read_csv('data/new_kamusalay.csv', names = ['sebelum', 'sesudah'], encoding='latin-1')

number = 0

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

def text_processing(s):
    s = _toLower(s)
    s = _remove_link(s)
    s = _remove_another(s)
    s = _remove_punct(s)
    s = _normalization(s)
    return s

def file_processing(df):
    df['lower'] = df['Tweet'].apply(_toLower)
    df['remove_punct'] = df['lower'].apply(_remove_punct)
    df['remove_link'] = df['remove_punct'].apply(_remove_link)
    df['remove_another'] = df['remove_link'].apply(_remove_another)
    df['normalization'] = df['remove_another'].apply(_normalization)
    df['normalization'].to_csv('output.csv', index=False, header=False)
    dataframe = pd.DataFrame(df['normalization'])
    result = dataframe.to_json(orient="columns")
    return result

@app.route("/clean_text/v1", methods=['POST'])
def text_cleaning():
    s = request.get_json()
    text_clean = text_processing(s['text'])
    return jsonify({"hasil_bersih":text_clean})

@app.route("/cleaning_file/v1", methods=['POST'])
def file_cleaning():
    file = request.files['file']
    df = pd.read_csv(file, encoding=('latin-1'))
    file_clean = file_processing(df)
    return jsonify(file_clean)

if __name__ == "__main__":
    app.run(port=1234, debug=True) # debug ==> kode otomatis update ketika ada perubahan