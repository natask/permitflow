from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    return jsonify({
        'zipcode': data.get('zipcode', ''),
        'address': data.get('address', ''),
        'roofArea': data.get('roofArea', '')
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)