from flask import Flask, request, jsonify
import re
import pandas as pd

app = Flask(__name__) # deklarasi Flask



if __name__ == "__main__":
    app.run(port=1234, debug=True) # debug ==> kode otomatis update ketika ada perubahan