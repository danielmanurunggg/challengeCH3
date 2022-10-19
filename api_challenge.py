from flask import Flask, request, jsonify
from flasgger import Swagger, LazyString, LazyJSONEncoder, swag_from
import pandas as pd
import time
from clean_data import _toLower, _remove_punct, _remove_space, _remove_link, _remove_hastag, _normalization, _remove_another_text, _remove_another_file, _stopword_removal, _stemming
from database import checkTableText, checkTableFile, _insertTextString, _insertTextFile

app = Flask(__name__) # deklarasi Flask
app.json_encoder = LazyJSONEncoder

swagger_template = dict(
    info = {
        'title': LazyString(lambda: 'API TESTER'),
        'version': LazyString(lambda: '1'),
        'description': LazyString(lambda: 'API Tester for challenge')
    },
    host = LazyString(lambda: request.host)
)

swagger_config = {
    "headers":[],
    "specs": [
        {
            "endpoint":"docs",
            "route":"/docs.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True
        }
    ],
    "static_url_path":"/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}

swagger = Swagger(app, template=swagger_template,config=swagger_config)

def text_processing(s):
    text = s
    s = _toLower(s)
    s = _remove_link(s)
    s = _remove_another_text(s)
    s = _remove_hastag(s)
    s = _remove_punct(s)
    s = _normalization(s)
    s = _stemming(s)
    s = _stopword_removal(s)
    s = _remove_space(s)
    _insertTextString(text, s)
    return s

def file_processing(df):
    df['lower'] = df['Tweet'].apply(_toLower)
    df['link'] = df['lower'].apply(_remove_link)
    df['binary'] = df['link'].apply(_remove_another_file)
    df['hastag'] = df['binary'].apply(_remove_hastag)
    df['punct'] = df['hastag'].apply(_remove_punct)
    df['normalization'] = df['punct'].apply(_normalization)
    df['stemming'] = df['normalization'].apply(_stemming)
    df['stopword'] = df['stemming'].apply(_stopword_removal)
    df['space'] = df['stopword'].apply(_remove_space)
    df['space'].to_csv('output.csv', index=False, header=False)
    a = pd.DataFrame(df[['Tweet','space']])
    _insertTextFile(a)
    # return True

#test funtion for string
text = "test www.google.com http:asd https: USER Ya akan bani\ntaplak \n dkk \xf0\x9f\x98\x84\xf0\x9f\x98\x84\xf0\x9f\x98\x84 membuang  hahah kalo bgt #jokowi3 ?? saya'"
hasil = text_processing(text)
print(hasil)

@swag_from("docs/swagger_config_text.yml", methods=['POST'])
@app.route("/api/v1/text", methods=['POST'])
def text_cleaning():
    checkTableText()
    s = request.get_json()
    text_clean = text_processing(s['text'])
    return jsonify({"result":text_clean})

@swag_from("docs/swagger_config_file.yml", methods=['POST'])
@app.route("/api/v1/file", methods=['POST'])
def file_cleaning():
    checkTableFile()
    start_time = time.time()
    file = request.files['file']
    df = pd.read_csv(file, encoding=('ISO-8859-1'))
    file_processing(df)
    return jsonify({"result":"file berhasil diupload ke database","time_exc":"--- %s seconds ---" % (time.time() - start_time)})

if __name__ == "__main__":
    app.run(port=1234, debug=True) # debug ==> kode otomatis update ketika ada perubahan