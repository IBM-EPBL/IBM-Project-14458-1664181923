from distutils.log import debug
from flask import Flask,flash, request,redirect,render_template, url_for, session
import ibm_db
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from sendgrid.helpers.mail import *
from dotenv import load_dotenv
import re
import urllib.request
from werkzeug.utils import secure_filename
from flask import Flask,render_template
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
import requests
import base64
import sendgrid


#connection with db
try:
    conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=fbd88901-ebdb-4a4f-a32e-9822b9fb237b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PROTOCOL=TCPIP;PORT=32731;UID=ytl80962;PWD=9VzjxssPbixN82n5;Security=SSL;SSLSecurityCertificate=DigiCertGlobalRootCA.crt", "", "")
    print(conn)
    print("connection successfull")
except:
    print("Error in connection, sqlstate = ")
    errorState = ibm_db.conn_error()
    print(errorState)

app = Flask(__name__,static_url_path='/static')
app.secret_key = 'foodrecognition'


#to load env
load_dotenv()



@app.route('/')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
#Clarifai api
C_USER_ID = os.getenv('C_USER_ID')
# Your PAT (Personal Access Token) can be found in the portal under Authentification
C_PAT = os.getenv('C_PAT')
C_APP_ID = os.getenv('C_APP_ID')
C_MODEL_ID = 'food-item-recognition'

@app.route('/plans')
def plans():
    return render_template('plans.html')
@app.route('/nutrition')
def nutrition():
    return render_template('nutrition.html')
@app.route('/readmore')
def readmore():
    return render_template('Readmore.html')
@app.route('/login',methods=['GET','POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        checkuser = "SELECT * FROM USERS WHERE email=? AND password=?"
        stmt1 = ibm_db.prepare(conn,checkuser)
        ibm_db.bind_param(stmt1,1,email)
        ibm_db.bind_param(stmt1,2,password)
        ibm_db.execute(stmt1)
        account = ibm_db.fetch_tuple(stmt1)
        if account:
            #user has an account
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            # msg = "logged in successfull" ( Need to set timoeout to display this message )
            return redirect(url_for('home'))
        else:
            msg = "Invalid email-id or password!"
    return render_template("sign_in.html",msg=msg)

# Helper function to send confirmation mail on sign in
def send_confirmation_mail( email):

    
    # print(os.environ.get('SENDGRID_API_KEY'))
    # print(os.getenv('SENDGRID_API_KEY'))
    sg = sendgrid.SendGridAPIClient(api_key=os.getenv('SENDGRID_API_KEY'))
    from_email = Email("devika742002@gmail.com")
    to_email = To(email)
    subject = "Welcome to Nutro"
    content = Content("Nutroscan helps you to identify your food items nutritional values.It provide you with detailed plans and by uploading images you can identify your nutritional values.")
    mail = Mail(from_email, to_email, subject, content)
    # mail_json=mail.get()
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)
    


# http://localhost:5000/python/logout - this will be the logout page
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/signup',methods=['GET','POST'])
def sign_up():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        print(username,email,password)
        checkuser = "SELECT email FROM USERS WHERE email=?"
        stmt1 = ibm_db.prepare(conn,checkuser)
        ibm_db.bind_param(stmt1,1,email)
        ibm_db.execute(stmt1)
        account = ibm_db.fetch_tuple(stmt1)
        print(account)
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            sql = "INSERT INTO USERS(username,password,email) VALUES(?,?,?)"
            stmt = ibm_db.prepare(conn,sql)
            ibm_db.bind_param(stmt, 1, username)
            ibm_db.bind_param(stmt, 2, password)
            ibm_db.bind_param(stmt, 3, email)
            ibm_db.execute(stmt)
            print(username,email,password)
            msg = 'You have successfully registered!'
            send_confirmation_mail(email)
            return redirect(url_for('home'))
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('sign_up.html', msg=msg)
    
UPLOAD_FOLDER = 'assets/uploads/'
 
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
API_URL="https://api.imgbb.com/1/upload"

@app.route('/upload', methods=['POST','GET'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        print(file)
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename=secure_filename(file.filename)
            api_data = {
                'key': "7dfb136dd63e7888412ca2ba061135c9",
                'image': base64.b64encode(file.read()),
                'name': filename
            }
            r = requests.post(url = API_URL, data = api_data)
            rj = r.json()        
            url = rj.get('data').get('display_url')
            #print('upload filename: ' + filename)
            print('Image successfully uploaded and displayed below')
            predict(url)
            return render_template('upload.html', filename=url)
        else:
            flash('Allowed image types are - png, jpg, jpeg, gif')
            return redirect(request.url)
    elif request.method == 'GET':
        return render_template('upload.html')

@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(filename, code=301)
    #return render_template('food.html')


def predict(filename):

        channel = ClarifaiChannel.get_grpc_channel()
        stub = service_pb2_grpc.V2Stub(channel)

        metadata = (('authorization', 'Key ' + C_PAT),)

        userDataObject = resources_pb2.UserAppIDSet(user_id=C_USER_ID, app_id=C_APP_ID)

        post_model_outputs_response = stub.PostModelOutputs(
            service_pb2.PostModelOutputsRequest(
                user_app_id=userDataObject,
                model_id=C_MODEL_ID,
                # version_id={MODEL_VERSION},  # This is optional. Defaults to the latest model version.
                inputs=[
                    resources_pb2.Input(
                        data=resources_pb2.Data(
                            image=resources_pb2.Image(
                                url=filename
                            )
                        )
                    )
                ]
            ),
            metadata=metadata
        )

        if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
            print(post_model_outputs_response.status)
            raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)

        # Since we have one input, one output will exist here.
        output = post_model_outputs_response.outputs[0]

        flash("Predicted ingredients:")
        for concept in output.data.concepts:
            flash("%s     %.2f" % (concept.name, concept.value))

        # Uncomment this line to print the full Response JSON
        #print(post_model_outputs_response)

 
if __name__ == '__main__':
    app.run(debug=True)