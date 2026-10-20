from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

# Load file Excel saat aplikasi pertama kali berjalan
EXCEL_FILE = 'EXCEL bng icon.xlsx'

def load_data():
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
        df['VLAN'] = df['VLAN'].astype(str).str.strip()
        df['HOSTNAME BNG'] = df['HOSTNAME BNG'].fillna('-')
        df['RADIUS'] = df['RADIUS'].fillna('-')
        df['SBU'] = df['SBU'].fillna('-')
        return df
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    search_query = ""
    error_message = None

    df = load_data()
    if df is None:
        error_message = f"File {EXCEL_FILE} tidak ditemukan di direktori!"
        return render_template('index.html', results=results, search_query=search_query, error_message=error_message)

    if request.method == 'POST':
        search_query = request.form.get('vlan', '').strip()
        if search_query:
            filtered_df = df[df['VLAN'].str.contains(search_query, case=False, na=False)]

            for _, row in filtered_df.iterrows():
                results.append({
                    'VLAN': row['VLAN'],
                    'BNG': row['HOSTNAME BNG'],
                    'NAS': row['RADIUS'],
                    'SBU': row['SBU']
                })

    return render_template('index.html', results=results, search_query=search_query, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
