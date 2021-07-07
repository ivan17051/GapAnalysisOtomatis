from flask import Flask, render_template, request, redirect
from datetime import datetime
import csv

app = Flask(__name__)

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
                            "ket": row[3],
                            "awal": row[4],
                            "tujuan": row[5],
                            "task": row[6]
                        })
                    else:
                        first_line=False
            
            with open('it_resource.csv') as data_itres:
                data = csv.reader(data_itres, delimiter=';')
                first_line = True
                hasil = []
                for row in data:
                    for gap in gap_analysis:
                        if not first_line and row[1]==it_res and gap['it_pro']==row[2]:
                            hasil.append({
                                "it_pro": gap['it_pro'],
                                "ket": gap['ket'],
                                "awal": gap['awal'],
                                "tujuan": gap['tujuan'],
                                "task": gap['task']
                            })
                        
                        else:
                            first_line = False

            return render_template('hasil.html', gap_analysis=hasil)
        except:
            return redirect('/input')
    else:
        return render_template('input.html')

@app.route('/hasil')
def hasil():
    return render_template('hasil.html')

if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0')