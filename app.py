from flask import Flask, request, render_template, send_file
from pymongo import MongoClient
import pandas as pd
from textblob import TextBlob
app = Flask(__name__)

cluster = MongoClient("mongodb+srv://abcd:qwertyuiop@cluster0.0ihqm.mongodb.net/ipl?retryWrites=true&w=majority")
db=cluster['thoughtful']
collection=db['login']

def detail(tb):
    sen_lst=[]
    sent_lst=[]
    sub_lst=[]
    for sentence in tb.sentences:
        sen_lst.append(str(sentence))
        sent_lst.append(TextBlob(str(sentence)).sentiment.polarity)
        sub_lst.append(TextBlob(str(sentence)).sentiment.subjectivity)

    data={
        'Sentences':sen_lst,
        'Sentiments':sent_lst,
        'Subjectivity':sub_lst
    }
    df=pd.DataFrame(data)
    return df

def sent(val):
    if val>0.4:
        return "Happy"
    elif val<-0.4:
        return "Sad"
    else:
        return "Neutral"

@app.route('/predict', methods=['POST','GET'])
def predict():
    if request.method == 'POST':
        global data
        global title
        title=request.form["title"]
        data=request.form['thought']
        tb=TextBlob(data)

        return render_template('pred.html',mood="Mood: "+sent(tb.sentiment.polarity),sent="Sentiment: "+str(tb.sentiment.polarity),sub="Subjectivity: "+str(tb.sentiment.subjectivity),txt=data,title=title)

@app.route('/analysis')
def analysis():
    tb=TextBlob(data)
    return render_template('analysis.html',txt=data,title=title,df=detail(tb))

@app.route('/download')
def download_data():
    filename="{}.txt".format(title)
    file=open("data\\"+filename, "w")
    file.write(data)
    file.close()

    return send_file("data\\"+filename,attachment_filename=filename,as_attachment=True)

@app.route('/login')
def login():


    return render_template('login.html')

@app.route('/register')
def register():


    return render_template('login.html')

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)