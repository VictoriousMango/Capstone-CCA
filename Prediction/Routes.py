from flask import Flask, render_template, request, session, redirect, jsonify
import requests
import json
import pandas as pd

app = Flask(__name__)
app.secret_key = "Hello World"

## Definition of ML Algorithms
def RandomForest(Data):
    return len(Data)

## Defining all session variables
def VarDefinition():
    MLTechniques = ['Random Forest', 'Linear Regression', 'Logistic Regression', 'SVM']
    return MLTechniques

## Home Page
@app.route("/")
def HomePage():
    session['MLTechniques'] = VarDefinition()
    if 'OutputFields' not in session:
        session['OutputFields'] = 'Not Selected yet'
    if 'MLOutput' not in session:
        session['MLOutput'] = 'Not Yet Trained'
    return render_template('HomePage.html')


## Preparation
@app.route("/mlTrainer")
def Preparation():
    try:
        df = pd.read_excel('ChurnAnalysis.xlsx')
        session['ChoosingOutputFields'] = [i for i in df.columns]
    except:
        session['ChoosingOutputFields'] = 'Empty'
    print(session['MLOutput'])
    return render_template('MLTrainer.html', MLTechniques=session['MLTechniques'], OutputFields=session['OutputFields'], MLOutput=session['MLOutput'])

@app.route("/preparation/<Option>", methods=['GET', 'POST'])
def prepOption(Option):
    if Option == "1":
        if request.method == 'POST':
            file = request.files['file']
            if file:
                file.save("ChurnAnalysis.xlsx")
                session['ShowData'] = 1
                return redirect("/mlTrainer")
    

    return f'{Option} : {Option == "1"}'


## Generating Training Data API
@app.route("/TrainData/<MLTechnique>")
def Prediction(MLTechnique):
    df = pd.read_excel('ChurnAnalysis.xlsx')
    # Prepare the dataframe for the API call
    df_json = df.to_json(orient='records')

    session['MLOutput'] = requests.get(f"http://127.0.0.1:8080/TrainData/{session['OutputFields']}/{df_json}").json()
    return redirect("/mlTrainer")


## Report
@app.route("/report")
def Report():
    return render_template('Report.html')


## Login
@app.route("/login")
def Login():
    return render_template('Login.html')


## Show Table
@app.route("/showData/<Option>")
def showTable(Option):
    if Option == '1':
        try:
            df = pd.read_excel('ChurnAnalysis.xlsx')
            return df.to_html()
        except:
            return redirect('/preparation')
    elif Option == '2':
        try:
            df = pd.read_excel('ChurnAnalysis.xlsx')
            return df.describe().to_html()
        except:
            return redirect('/preparation')
    

## ChoosingOutputFields
@app.route("/MLTechniques/<Option>")
def MLTechniques(Option):
    session['OutputFields'] = Option
    return redirect('/mlTrainer')


## Train Data on Models
@app.route("/TrainData/<MLTechnique>/<Data>")
def DataTrainer(MLTechnique, Data):
    data = {
        'MLTechnique': MLTechnique,
        'Data': [1, 2, 3, 4],
        'Weights': [1, 2, 3, 4],
        'SavedModel': 'Blablabla',
        'Hello World': 'Yo',
        'Model Return': RandomForest(Data),
    }
    print(type(json.dumps(data)))
    return json.dumps(data)


## Train Data on Models
@app.route("/ML_Available")
def ML_Available():
    return json.dumps(VarDefinition())

if __name__ == '__main__':
    app.run(debug=True, port=8080)