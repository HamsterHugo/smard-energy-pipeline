from pathlib import Path
import datetime

import duckdb
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Set paths to the preprocessed data.
DATA_PATH: Path = Path(__file__).parent.parent.parent / 'data' / 'preprocessed_data'
POWER_GENERATION_PATH: Path = DATA_PATH / 'combined_historical.parquet'
PRICE_PATH: Path = DATA_PATH / '4169_historical.parquet'
NUCLEAR_PATH: Path = DATA_PATH / '1224_historical.parquet'

x = datetime.datetime.now()
y = x - datetime.timedelta(days=7)
TODAY: str = str(x.date())
LAST_WEEK: str = str(y.date())

def query_parquet(path: Path, date_from: str, date_to: str) -> list:
    con = duckdb.connect()
    df = con.execute(f"""
        SELECT *
        FROM read_parquet('{path}')
        WHERE timestamps BETWEEN '{date_from}' AND '{date_to}'
        ORDER BY timestamps
    """).fetchdf()
    con.close()
    return df.to_dict(orient='records')

@app.route('/data')
def get_data():
    date_from = request.args.get('from', LAST_WEEK)
    date_to = request.args.get('to', TODAY)
    return jsonify(query_parquet(POWER_GENERATION_PATH, date_from, date_to))

@app.route('/price')
def get_price():
    date_from = request.args.get('from', LAST_WEEK)
    date_to = request.args.get('to', TODAY)
    return jsonify(query_parquet(PRICE_PATH, date_from, date_to))

@app.route('/nuclear')
def get_nuclear():
    date_from = request.args.get('from', '2023-04-01')
    date_to = request.args.get('to', '2023-04-15')
    return jsonify(query_parquet(NUCLEAR_PATH, date_from, date_to))

@app.route('/')
def index():
    return send_file(Path(__file__).parent.parent / 'frontend' / 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_file(Path(__file__).parent.parent / 'frontend' / filename)

if __name__ == '__main__':
    app.run(debug=True)