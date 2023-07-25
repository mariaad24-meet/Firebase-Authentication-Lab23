from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config={ 
"apiKey": "AIzaSyBT7Vv53CuezkK0aFMkic4fayLLmMTWTGI",
  "authDomain": "fir-1-3ee27.firebaseapp.com",
  "projectId": "fir-1-3ee27",
  "storageBucket": "fir-1-3ee27.appspot.com",
  "messagingSenderId": "542593584125",
  "appId": "1:542593584125:web:9ba7d5adc3bb3a6c05a794",
  "measurementId": "G-TK6Y4KT32T",
  "databaseURL":"https://fir-1-3ee27-default-rtdb.europe-west1.firebasedatabase.app/"
  }

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db=firebase.database()

@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
    return render_template("signin.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        username= request.form['username']
        bio= request.form['bio']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user = {"username": username, "email": eamail ,"password":password,"bio":bio,"full_name":full_name}
            db.child("Users").child(UID).set(user)
            return redirect(url_for('signin'))
        except :
            error = "Authentication failed"
    return render_template("signup.html",error=error)



@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    error = ""
    if request.method == 'POST':
        Title=request.form['Title']
        Text=request.form['Text']
        try:
            tweet = {"Title": Title, "Text": Text}
            db.child("Tweet").push(tweet)
            return redirect(url_for('all_tweets'))
        except:
            print("Couldn't add tweet")
    return render_template("add_tweet.html",error=error)


@app.route('/all_tweets', methods=['GET', 'POST'])
def all_tweets():
    tweet= db.child("Tweets").get().val()
    return render_template("tweets.html", tweet=tweet)




if __name__ == '__main__':
    app.run(debug=True)