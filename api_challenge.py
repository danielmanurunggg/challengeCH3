from flask import Flask, request, jsonify
import pandas as pd
import time
from clean_data import _toLower, _remove_punct, _remove_space, _remove_link, _remove_hastag, _normalization, _remove_another_text, _remove_another_file, _stopword_removal, _stemming
import sqlite3
from database import checkTableText, checkTableFile, _insertTextString

app = Flask(__name__) # deklarasi Flask

checkTableText()
checkTableFile()

def text_processing(s):
    s = _toLower(s)
    s = _remove_link(s)
    s = _remove_another_text(s)
    s = _remove_hastag(s)
    s = _remove_punct(s)
    s = _normalization(s)
    s = _stemming(s)
    s = _stopword_removal(s)
    s = _remove_space(s)
    return s

def file_processing(df):
    df['lower'] = df['Tweet'].apply(_toLower)
    df['link'] = df['lower'].apply(_remove_link)
    df['binary'] = df['link'].apply(_remove_another_file)
    df['hastag'] = df['binary'].apply(_remove_hastag)
    df['punct'] = df['hastag'].apply(_remove_punct)
    # df['normalization'] = df['punct'].apply(_normalization)
    # df['stemming'] = df['normalization'].apply(_stemming)
    # df['stopword'] = df['stemming'].apply(_stopword_removal)
    # df['space'] = df['stopword'].apply(_remove_space)
    # df['space'].to_csv('output.csv', index=False, header=False)
    return df['punct']

text = "test www.google.com http:asd https: USER Ya akan bani\ntaplak \n dkk \xf0\x9f\x98\x84\xf0\x9f\x98\x84\xf0\x9f\x98\x84 membuang  hahah kalo bgt #jokowi3 ?? saya'"
hasil = text_processing(text)
print(hasil)

@app.route("/clean_text/v1", methods=['POST'])
def text_cleaning():
    s = request.get_json()
    text_clean = text_processing(s['text'])
    _insertTextString(s['text'], text_clean)
    return jsonify({"result":text_clean})

@app.route("/clean_file/v1", methods=['POST'])
def file_cleaning():
    start_time = time.time()
    file = request.files['file']
    df = pd.read_csv(file, encoding=('ISO-8859-1'))
    file_clean = file_processing(df)
    return jsonify({"result":"file berhasil diupload ke database","time_exc":"--- %s seconds ---" % (time.time() - start_time)})

if __name__ == "__main__":
    app.run(port=1234, debug=True) # debug ==> kode otomatis update ketika ada perubahan