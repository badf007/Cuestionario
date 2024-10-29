import os
from flask import (Flask, render_template, redirect,url_for,request, flash)
import pandas as pd
import gspread



#def create_app(test_config=None):

test_config=None
# create and configure the app
app = Flask(__name__, instance_relative_config=True)

app.config.from_mapping(
    SECRET_KEY='dev',
    DEBUG=True,
    ENVIRONMENT='development'

)

if test_config is None:
    # load the instance config, if it exists, when not testing
    app.config.from_pyfile('config.py', silent=True)
else:
    # load the test config if passed in
    app.config.from_mapping(test_config)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass


#RUTES!!!
@app.route('/')
def index():
    return render_template('index.html'  )

@app.route('/q1')
def q1():
    return render_template('e1.html'  )

@app.route('/q2')
def q2():
    return render_template('e2.html'  )


#authorization
#gc = pygsheets.authorize(service_file='src\cuestionario-418210-94eee3a815de.json')
gc = gspread.service_account('/etc/secrets/connect.json')
#gc = gspread.service_account('src\connect.json')


@app.route('/store_q1', methods=['POST'])
def store_q1():
    error = None
    if request.method == 'POST':
        print(request.form)

        data = {'nombre':[request.form['nombre']], 
                'edad':[request.form['edad']], 
                'sexo':[request.form['q0']], 
                'pregunta 1':[request.form['q1']], 
                'pregunta 2':[request.form['q2']], 
                'pregunta 3':[request.form['q3']], 
                'pregunta 4':[request.form['q4']], 
                'pregunta 5':[request.form['q5']], 
                'pregunta 6':[request.form['q6']], 
                'pregunta 7':[request.form['q7']], 
                'pregunta 8':[request.form['q8']]}
        # Create empty dataframe
        df = pd.DataFrame(data=data)
        
        calc = int(df['pregunta 1'][0]) + int(df['pregunta 2'][0]) + int(df['pregunta 3'][0]) + int(df['pregunta 4'][0]) + int(df['pregunta 5'][0]) + int(df['pregunta 6'][0]) + int(df['pregunta 7'][0]) + int(df['pregunta 8'][0])

        test_result = ""
        
        if calc >= 0 and calc <= 7:
            test_result = "0-7: Es poco probable que tenga un sueño anormal."
        elif calc >= 8 and calc <= 9:
            test_result = "8-9: Tiene una cantidad promedio de somnolencia diurna."
        elif calc >= 10 and calc <= 15:
            test_result = "10-15: Puede que tengas demasiado sueño dependiendo de la situación. Quizás quieras considerar buscando atención médica."
        elif calc >= 16 and calc <= 24:
            test_result = "16-24: Tienes demasiado sueño y deberías considerar buscar atención médica."
            
        full_read = gc.open_by_url('https://docs.google.com/spreadsheets/d/1S9yUmxvo6djOpAWKamh3sHzf2Wi1VJVUezPytuVixsc/edit#gid=0')
        sheet = full_read.get_worksheet(0)
        dataframe = pd.DataFrame(sheet.get_all_records())

        full_data = pd.concat([df,dataframe], ignore_index = True)
        
        #update the first sheet with df, starting at cell B2. 
        #wks.set_dataframe(df,(1,1))
        #print(dataframe.tail())
        #print(full_data.tail())

        sheet.clear()
        sheet.update([full_data.columns.values.tolist()] + full_data.values.tolist())
        
    else:
        error="Invalid information"

    #data = fetch()
    
    flash(test_result)
    return redirect(url_for('index'))
    #return render_template('e1.html'  )

@app.route('/store_q2', methods=['POST'])
def store_q2():
    error = None
    if request.method == 'POST':
        print(request.form)

        data = {'nombre':[request.form['nombre']], 
                'edad':[request.form['edad']], 
                'sexo':[request.form['q0']], 
                'pregunta 1':[request.form['q1']], 
                'pregunta 2':[request.form['q2']], 
                'pregunta 3':[request.form['q3']], 
                'pregunta 4':[request.form['q4']], 
                'pregunta 5':[request.form['q5']], 
                'pregunta 6':[request.form['q6']], 
                'pregunta 7':[request.form['q7']], 
                'pregunta 8':[request.form['q8']]}
        # Create empty dataframe
        df = pd.DataFrame(data=data)
        
        
        responses = df.values.tolist()[0]
        ccount = int(responses.count('SI'))
        print(ccount)

        
        test_result = ""
        
        if ccount >= 0 and ccount <= 2:
            test_result = "0-2: Bajo riesgo de AOS (Apnea Obstructiva del Sueño)"
        elif ccount >= 3 and ccount <= 4:
            test_result = "3-4: Riesgo intermedio de AOS (Apnea Obstructiva del Sueño)"
        elif ccount >= 5 and ccount <= 8:
            test_result = "5-8: Alto riesgo de AOS (Apnea Obstructiva del Sueño)"


        full_read = gc.open_by_url('https://docs.google.com/spreadsheets/d/17B8jnUJ6xLFBALR8uBNVHhP3Ip0AO19_lkpDT4oHxHE/edit#gid=0')
        sheet = full_read.get_worksheet(0)
        dataframe = pd.DataFrame(sheet.get_all_records())

        full_data = pd.concat([df,dataframe], ignore_index = True)
        
        #update the first sheet with df, starting at cell B2. 
        #wks.set_dataframe(df,(1,1))
        #print(dataframe.tail())
        #print(full_data.tail())

        sheet.clear()
        sheet.update([full_data.columns.values.tolist()] + full_data.values.tolist())
        
    else:
        error="Invalid information"

    #data = fetch()
    flash(test_result)
    return redirect(url_for('index'))




