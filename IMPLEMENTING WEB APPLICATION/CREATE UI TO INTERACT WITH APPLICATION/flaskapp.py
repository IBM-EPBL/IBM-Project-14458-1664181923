from flask import Flask,render_template,request
from mydb import connection as db


app = Flask(__name__)


@app.route("/",methods=['GET', 'POST'])
@app.route("/register",methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        Gender = request.form["Gender"]
        age = request.form["age"]
        height = request.form["height"]
        weight = request.form["weight"]
        BMI = request.form["BMI"]
        print(username, password, email, Gender, age, height, weight, BMI)
        db.register(username, password, email, Gender, age, height, weight, BMI)
        return render_template('login.html', msg = msg) 
    else:
        return render_template('register.html', msg = msg)

@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        result_dict = db.login(username, password)
        if result_dict != False:
            return render_template('welcome.html',msg = msg)
        return render_template('login.html', msg = msg)

    else:
        return render_template('login.html', msg = msg)

@app.route('/welcome', methods =['GET', 'POST'])
def welcome():
    msg = ''
    return render_template('welcome.html', msg = msg)

# @app.route('/about') 
# def about():
#     return render_template("about.html")



# @app.route('/https://nutri1b.s3.jp-tok.cloud-object-storage.appdomain.cloud/about.html', methods =['GET', 'POST'])
# def about():
#     msg = ''
#     if request.method == 'POST':
#         return render_template('https://nutri1b.s3.jp-tok.cloud-object-storage.appdomain.cloud/about.html', msg = msg)
#     else:
#         return render_template('welcome.html', msg = msg)


if __name__=="__main__":
    app.run(debug=True)

# app = Flask(__name__)


# @app.route("/", methods=['GET', 'POST'])
# @app.route("/register", methods=['GET', 'POST'])
# def register():
#     msg = ''
#     if request.method == 'POST':
#         name = request.form["username"]
#         email = request.form["email"]
#         rollno = request.form["rollno"]
#         password = request.form["password"]
#         print(name, email, rollno, password)
#         db.register(name, email, rollno, password)
#         return render_template('login.html', msg=msg)
#     else:
#         return render_template('register.html', msg=msg)


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     msg = ''
#     if request.method == 'POST':
#         name = request.form["username"]
#         password = request.form["password"]
#         result_dict = db.login(name, password)
#         if result_dict != False:
#             return render_template('welcome.html', msg=msg)
#         return render_template('login.html', msg=msg)

#     else:
#         return render_template('login.html', msg=msg)


# @app.route('/welcome', methods=['GET', 'POST'])
# def welcome():
#     msg = ''
#     return render_template('welcome.html', msg=msg)


# if __name__ == "__main__":
#     app.run(debug=True)

