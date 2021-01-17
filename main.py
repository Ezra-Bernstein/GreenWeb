from flask import Flask, render_template, request, url_for, session, redirect
from dotenv import load_dotenv
import os

from auth import get_resource_token, twitter_get_access_token, twitter_get_user_data, twitter_tweet
from google_functions import get_labels
from databse_functions import addUser, get_access_token_list, getPoints, updatePoints, get_recent_activity

app = Flask(__name__)
load_dotenv()
# API_KEY=os.getenv("API_KEY")
# API_SECRET_KEY=os.getenv("API_SECRET_KEY")
app.secret_key=os.environ.get("SECRET_KEY")
conversion_dict={'Plastic bottle': -1.0, 'Plastic': -1.0, 'Paper': -0.5, 'Glass': -3.0}

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/login')
def login():
    resource = get_resource_token()
    # f = open("data.txt", "a")
    # for item in resource:
    #     f.write(item + '\n')
    # f.close()
    session['oauth_token']=resource[0]
    session['oauth_secret']=resource[1]
    session['points']=0.0
    link = "https://api.twitter.com/oauth/authenticate?oauth_token=" + resource[0]
    return render_template('login.html', href_link=link)

@app.route('/auth')#?oauth_token=<oauth_token>&oauth_verifier=<oauth_verifier>')
def authenticated():
    oauth_token=request.args.get('oauth_token')
    oauth_verifier=request.args.get('oauth_verifier')
    print(oauth_token, oauth_verifier)
    session['oauth_verifier']=oauth_verifier
    resource=[]
    # with open("data.txt", encoding="utf-8") as file:
    #     resource = [l.rstrip("\n") for l in file]
    # with open('data.txt', 'a') as file:
    #     file.write(oauth_verifier)
    access_token_list = twitter_get_access_token(oauth_verifier, session['oauth_token'], session['oauth_secret'])
    print(access_token_list)
    session['access_token_list'] = access_token_list
    # twitter_tweet()
    response = twitter_get_user_data(access_token_list)
    #print(response)
    session['user_id'] = response['screen_name']
    addUser(session['user_id'], session['oauth_token'], session['oauth_secret'], session['oauth_verifier'], session['access_token_list'])
    for item in list(session):
        if item!='user_id':
            session.pop(item)
    return redirect(url_for('dashboard'))

@app.route('/tweet', methods=['GET','POST'])
def tweet():
    if request.method=='POST':
        tweet = request.form['tweet']
        # with open("data.txt", encoding="utf-8") as file:
        #     data = [l.rstrip("\n") for l in file]

        # access_token_list = twitter_get_access_token(session['oauth_verifier'], session['oauth_token'], session['oauth_secret'])
        # print(access_token_list)

        # info = twitter_get_user_data(access_token_list)
        response = twitter_tweet(get_access_token_list(session['user_id']), tweet)
        print(response)
        updatePoints(session['user_id'], 0.2, classification='')
        return redirect(url_for('dashboard')) 
    elif request.method=='GET':
        return render_template('tweet.html', score=getPoints(session['user_id']))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', user_id=session['user_id'], points=getPoints(session['user_id']), recent_activity=get_recent_activity(session['user_id']))

@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method=='POST':
        if 'file' not in request.files:
                return "NO FILE"
        file = request.files['file']
        filename = "image.jpg"
        file.save('/tmp/' + filename)
        labels = get_labels('/tmp/' + filename)
        classification=''
        for label in labels:
            if label.description in conversion_dict.keys():
                classification=label.description
                print("classified as: " + classification)
                score = conversion_dict[classification]
                print(conversion_dict[classification])
                
        if classification=='':
            classification='Non-recyclable'
            score = 0.0
        print("classified as: " + classification)
        updatePoints(session['user_id'], score, classification)

        return render_template('display_labels.html', labels=labels, classification=classification, score=score)
    elif request.method=='GET':
        return render_template('upload.html')