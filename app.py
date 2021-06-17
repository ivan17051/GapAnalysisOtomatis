from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import csv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class InputUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lvl_existing = db.Column(db.Integer, nullable=False)
    lvl_tujuan = db.Column(db.Integer, nullable=False)
    it_res = db.Column(db.String(100), nullable=False)
    it_process = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/input', methods=['GET', 'POST'])
def input():
    if request.method == 'POST':
        
        lvl_existing = request.form['lvl_existing']
        lvl_tujuan = request.form['lvl_tujuan']
        it_res = request.form['it_res']
        it_process = request.form['it_process']
        
        try:
            # db.session.add(new_input)
            # db.session.commit()

            with open('data_level.csv') as data_file:
                data = csv.reader(data_file, delimiter=';')
                first_line = True
                gap_analysis = []
                for row in data:
                    if not first_line and row[1]==it_process and row[3]>=lvl_existing and row[4]<=lvl_tujuan:
                        gap_analysis.append({
                            "it_pro": row[2],
                            "awal": row[3],
                            "tujuan": row[4],
                            "task": row[5]
                        })
                    else:
                        first_line=False
            
            return render_template('hasil.html', gap_analysis=gap_analysis)
        except:
            return redirect('/input')
    else:
        return render_template('input.html')

@app.route('/hasil')
def hasil():
    return render_template('hasil.html')

if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0')