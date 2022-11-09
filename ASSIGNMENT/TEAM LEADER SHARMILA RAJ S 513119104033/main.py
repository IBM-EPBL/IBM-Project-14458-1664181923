from flask import Flask,render_template,request;

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('registration.html')

@app.route('/details',methods = ["POST"])

def details():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    return "Your Name is {}</br>Your Email is {}</br>Your Password is {}".format(username,email,password)
    

if(__name__ == '__main__'):
    app.run(debug=True)