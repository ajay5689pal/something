from flask import Flask , request , redirect , flash , url_for , jsonify , session
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField , TextAreaField , SubmitField , PasswordField , RadioField , IntegerField
from wtforms.validators import Email , DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin , LoginManager , login_user , current_user , login_required , logout_user
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from questions  import *
import random
import razorpay
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
admin = Admin(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
bcrypt = Bcrypt()

app.config["SECRET_KEY"] = "@VCS72xppdv"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = True
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'bcawallaorg@gmail.com'  # Your email address
app.config['MAIL_PASSWORD'] = 'rcbv dohs voeu tjgv'  # Your email password
app.config['MAIL_DEFAULT_SENDER'] = 'bcawallaorg@gmail.com'
mail_instance = Mail(app)
db = SQLAlchemy(app)


@login_manager.user_loader
def load_user(user_id):
    return mydatabase.query.get(int(user_id))



#database 
class mydatabase(UserMixin , db.Model):
    id = db.Column(db.Integer , primary_key = True)
    Name = db.Column(db.String(120) , unique = False , index  = True)
    College = db.Column(db.String(200) , unique = False , index = True)
    Email = db.Column(db.String(200) , unique = True , index = True)
    Password = db.Column(db.String(20) , unique = False , index = True)
    Premium = db.Column(db.String(12) , unique = False , index = True , default = "NO")
    Wallet = db.Column(db.Integer , unique = False , index = True , default = 0)
    Email_Verify = db.Column(db.String(100) , unique = False , index = True , default = "unverified")

admin = Admin(app, url='/Ajayadmin--6393myadminpanel8840', endpoint='Ajayadmin--6393myadminpanel8840')
admin.add_view(ModelView(mydatabase, db.session))
#Signin from
class myform(FlaskForm):
    name = StringField("Name" , validators=[DataRequired()])
    email = StringField("Email" , validators=[DataRequired() , Email()])
    college = StringField("College")
    password = PasswordField("Password" , validators=[DataRequired()])
    referal = StringField("Refer code")
    submit = SubmitField("Submit")


#login form
class loginform(FlaskForm):
    email = StringField("Email" , validators=[DataRequired() , Email()])
    password = PasswordField("Password" , validators=[DataRequired()])
    submit = SubmitField("Submit")


#update form
class updateform(FlaskForm):
    premium = StringField("Update or Degrade to Premium = YES or No" , validators=[DataRequired()])
    submit = SubmitField("Submit")



#home route
@app.route('/')
def home():
    return render_template('home.html')

#signin route
@app.route('/signin' , methods = ['GET' , 'POST'])
def signin():
    if current_user.is_authenticated:
        return redirect('home')
    formdata = myform()
    if formdata.validate_on_submit():
        user = mydatabase.query.filter_by(Email = request.form['email']).first()
        refer_code = mydatabase.query.filter_by(Email = request.form['referal']).first()
        if user:
           flash("Sorry this Email already exist" , "success")

        else:
            db.session.add(mydatabase(Name = request.form['name'] , College = request.form['college'] , Email = request.form['email'] , Password = request.form['password'] , Wallet = 50))
            db.session.commit()
            if refer_code:
                refer_code.Wallet += 200
                db.session.commit()
            flash("Account Created , You Can login now!" , "success")
            return redirect('login')
            
    return render_template('signin.html' , template_form = formdata)


#login route
@app.route('/login' , methods = ['GET' , 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = loginform()
    if form.validate_on_submit():
        user = mydatabase.query.filter_by(Email=request.form['email'] , Password = request.form['password']).first()
        if user:
            login_user(user)
            return redirect('/')
        else:
            flash('Please check email and password again', 'danger')
    return render_template('login.html' , template_form = form)



#update route
@app.route('/updateajay5689pal@VCS72xppdv' , methods = ["GET" , "POST"])
@login_required
def update():
    form = updateform()
    if form.validate_on_submit():
        current_user.Premium = request.form['premium']
        db.session.commit()
        return redirect('account')
    return render_template('update.html' , template_form = form)

#logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('login')


#account route
@app.route('/account')
@login_required
def account():
    return render_template('account.html')




#creating database:
with app.app_context():
   db.create_all()

#notes route
@app.route('/tests/<id>')
@login_required
def tests(id):
   return render_template('notes.html'  , id = id)


##test route
@app.route('/test/<data>', methods=['POST' , 'GET'])
def test(data):
    global questions
    if data == "Computer Fundamental1":
        questions = Computer_Fundamental1
    elif data == 'Computer Fundamental2':
        questions = Computer_Fundamental2
    elif data == 'Computer Fundamental3':
        questions = Computer_Fundamental3
    elif data == 'Computer Fundamental4':
        questions = Computer_Fundamental4
    elif data == 'Computer Fundamental5':
        questions = 'Computer_Fundamental5'
    elif data == 'C Programming1':
        questions = C_Programming1
    elif data == 'C Programming2':
        questions = C_Programming2
    elif data == 'C Programming3':
        questions = C_Programming3
    elif data == 'C Programming4':
        questions = C_Programming4
    elif data == 'C Programming5':
        questions = C_Programming5 
    elif data == 'Mathematics -I1':
        questions = MathematicsI1
    elif data == 'Mathematics -I2':
        questions = MathematicsI2
    elif data == 'Mathematics -I3':
        questions = MathematicsI3
    elif data == 'Mathematics -I4':
        questions = MathematicsI4
    elif data == 'Mathematics -I5':
        questions = MathematicsI5
    elif data == 'Business Communication1':
        questions = Business_Communication1
    elif data == 'Business Communication3':
        questions = Business_Communication3
    elif data == 'Business Communication4':
        questions = Business_Communication4
    elif data == 'Business Communication5':
        questions = Business_Communication5
    elif data == 'Financial Accounting Management1':
        questions = Financial_Accounting_Management1
    elif data == 'Financial Accounting Management2':
        questions = Financial_Accounting_Management2
    elif data == 'Financial Accounting Management3':
        questions = Financial_Accounting_Management3
    elif data == 'Financial Accounting Management4':
        questions = Financial_Accounting_Management4
    elif data == 'Financial Accounting Management5':
        questions = Financial_Accounting_Management1
    elif data == 'OOP Using C++1':
        questions = C1
    elif data == 'OOP Using C++2':
        questions = C2
    elif data == 'OOP Using C++3':
        questions = C3
    elif data == 'OOP Using C++4':
        questions = C4
    elif data == 'OOP Using C++5':
        questions = C5
    elif data == 'Organization Behavior1':
        questions = OB1
    elif data == 'Organization Behavior2':
        questions = OB2
    elif data == 'Organization Behavior3':
        questions = OB3
    elif data == 'Organization Behavior4':
        questions = OB4
    elif data == 'Organization Behavior5':
        questions = OB5
    elif data == 'Organization Behavior6':
        questions = OB6
    elif data == 'Mathematics -II1':
        questions = MII1
    elif data == 'Mathematics -II2':
        questions = MII2
    elif data == 'Mathematics -II3':
        questions = MII3
    elif data == 'Mathematics -II4':
        questions = MII4
    elif data == 'Mathematics -II5':
        questions = MII5
    elif data == 'Python1':
        questions = py1
    elif data == 'Python2':
        questions = py2
    elif data == 'Python3':
        questions = py3
    elif data == 'Python4':
        questions = py4
    elif data == 'Python5':
        questions = py5
    elif data == 'Data Structure Using C & C++1':
        questions = dsa1
    elif data == 'Data Structure Using C & C++2':
        questions = dsa2
    elif data == 'Data Structure Using C & C++3':
        questions = dsa3
    elif data == 'Data Structure Using C & C++4':
        questions = dsa4
    elif data == 'Data Structure Using C & C++5':
        questions = dsa5
    elif data == 'Elements of Statistics1':
        questions = Elements_of_Statistics1
    elif data == 'Elements of Statistics2':
        questions = Elements_of_Statistics2
    elif data == 'Elements of Statistics3':
        questions = Elements_of_Statistics3
    elif data == 'Elements of Statistics4':
        questions = Elements_of_Statistics4
    elif data == 'Elements of Statistics5':
        questions = Elements_of_Statistics5
    elif data == 'Computer Graphics & Animation1':
        questions = graphic1
    elif data == 'Computer Graphics & Animation2':
        questions = graphic2
    elif data == 'Computer Graphics & Animation3':
        questions = graphic3
    elif data == 'Computer Graphics & Animation4':
        questions = graphic4
    elif data == 'Computer Graphics & Animation5':
        questions = graphic5
    elif data == 'Software Engineering1':
        questions = se1
    elif data == 'Software Engineering2':
        questions = se2
    elif data == 'Software Engineering3':
        questions = se3
    elif data == 'Software Engineering4':
        questions = se4
    else:
        questions = questions

    
    return render_template('test.html', questions=questions , data = data)


##result route

wrong_questions = {}


def initialize_session():
    if 'wrong_questions' not in session:
        session['wrong_questions'] = {}




@app.route('/submit/<data>', methods=['POST' , 'GET'])
def submit(data):
    initialize_session()
    session['wrong_questions'].clear()

    if data == "Computer Fundamental1":
        questions = Computer_Fundamental1
    elif data == 'Computer Fundamental2':
        questions = Computer_Fundamental2
    elif data == 'Computer Fundamental3':
        questions = Computer_Fundamental3
    elif data == 'Computer Fundamental4':
        questions = Computer_Fundamental4
    elif data == 'Computer Fundamental5':
        questions = Computer_Fundamental5
    elif data == 'C Programming1':
        questions = C_Programming1
    elif data == 'C Programming2':
        questions = C_Programming2
    elif data == 'C Programming3':
        questions = C_Programming3
    elif data == 'C Programming4':
        questions = C_Programming4
    elif data == 'C Programming5':
        questions = C_Programming5
    elif data == 'Mathematics -I1':
        questions = MathematicsI1
    elif data == 'Mathematics -I2':
        questions = MathematicsI2
    elif data == 'Mathematics -I3':
        questions = MathematicsI3
    elif data == 'Mathematics -I4':
        questions = MathematicsI4
    elif data == 'Mathematics -I5':
        questions = MathematicsI5  
    elif data == 'Business Communication1':
        questions = Business_Communication1
    elif data == 'Business Communication3':
        questions = Business_Communication3
    elif data == 'Business Communication4':
        questions = Business_Communication4
    elif data == 'Business Communication5':
        questions = Business_Communication5
    elif data == 'Financial Accounting Management1':
        questions = Financial_Accounting_Management1
    elif data == 'Financial Accounting Management2':
        questions = Financial_Accounting_Management2
    elif data == 'Financial Accounting Management3':
        questions = Financial_Accounting_Management3
    elif data == 'Financial Accounting Management4':
        questions = Financial_Accounting_Management4
    elif data == 'Financial Accounting Management5':
        questions = Financial_Accounting_Management5
    elif data == 'OOP Using C++1':
        questions = C1
    elif data == 'OOP Using C++2':
        questions = C2
    elif data == 'OOP Using C++3':
        questions = C3
    elif data == 'OOP Using C++4':
        questions = C4
    elif data == 'OOP Using C++5':
        questions = C5
    elif data == 'Organization Behavior1':
        questions = OB1
    elif data == 'Organization Behavior2':
        questions = OB2
    elif data == 'Organization Behavior3':
        questions = OB3
    elif data == 'Organization Behavior4':
        questions = OB4
    elif data == 'Organization Behavior5':
        questions = OB5
    elif data == 'Organization Behavior6':
        questions = OB6
    elif data == 'Mathematics -II1':
        questions = MII1
    elif data == 'Mathematics -II2':
        questions = MII2
    elif data == 'Mathematics -II3':
        questions = MII3
    elif data == 'Mathematics -II4':
        questions = MII4
    elif data == 'Mathematics -II5':
        questions = MII5
    elif data == 'Python1':
        questions = py1
    elif data == 'Python2':
        questions = py2
    elif data == 'Python3':
        questions = py3
    elif data == 'Python4':
        questions = py4
    elif data == 'Python5':
        questions = py5
    elif data == 'Data Structure Using C & C++1':
        questions = dsa1
    elif data == 'Data Structure Using C & C++2':
        questions = dsa2
    elif data == 'Data Structure Using C & C++3':
        questions = dsa3
    elif data == 'Data Structure Using C & C++4':
        questions = dsa4
    elif data == 'Data Structure Using C & C++5':
        questions = dsa5
    elif data == 'Elements of Statistics1':
        questions = Elements_of_Statistics1
    elif data == 'Elements of Statistics2':
        questions = Elements_of_Statistics2
    elif data == 'Elements of Statistics3':
        questions = Elements_of_Statistics3
    elif data == 'Elements of Statistics4':
        questions = Elements_of_Statistics4
    elif data == 'Elements of Statistics5':
        questions = Elements_of_Statistics5
    elif data == 'Computer Graphics & Animation1':
        questions = graphic1
    elif data == 'Computer Graphics & Animation2':
        questions = graphic2
    elif data == 'Computer Graphics & Animation3':
        questions = graphic3
    elif data == 'Computer Graphics & Animation4':
        questions = graphic4
    elif data == 'Computer Graphics & Animation5':
        questions = graphic5
    elif data == 'Software Engineering1':
        questions = se1
    elif data == 'Software Engineering2':
        questions = se2
    elif data == 'Software Engineering3':
        questions = se3
    elif data == 'Software Engineering4':
        questions = se4
    else:
        questions = questions

    
    your_response = []
    total = -1
    total_marks = 0
    score = 0
    for question in questions:
        total +=1
        total_marks +=1
        selected_option = request.form.get(question['question'])
        if selected_option == question['answer']:
            score += 1
        else:
            session['wrong_questions'][questions[total].get('question')]  = questions[total].get('answer')
            your_response.append(request.form.get(question['question']))
    return render_template('result.html', score=score , total_marks = total_marks , wrong_questions = session['wrong_questions']  ,  your_response = your_response)
#practice_chapter name
@app.route('/practice_sub_name')
@login_required
def practice_sub_name():
    return render_template('practice_sub.html')
#chapter name
@app.route('/chapter_name/<id>')
@login_required
def chapter_name(id):
    return render_template('chapter_name.html' , id = id)


#Carrer Center
@app.route('/career')
@login_required
def career():
    return render_template('carrer.html')

topic = []
Python = ['Lecture 1 Intro' , 'Lecture2' , 'Lecture-3']
html = ['Lecture 1 Intro' , 'Lecture2' , 'Lecture-3']
Webdevelopment = ['Lecture 1 Intro' , 'Lecture2' , 'Lecture-3']
JavaScript = ['Lecture 1 Intro' , 'Lecture2' , 'Lecture-3']

#Career Center / topic
@app.route('/learn/<topic>' ,  methods = ['GET' , 'POST'] )
@login_required
def learn(topic):
    heading = topic
    if topic == "Python":
        topic = Python
    if topic == "html":
        topic = html
    if topic == "webdevelopment":
        topic = Webdevelopment
    if topic == "JavaScript":
        topic = JavaScript
    return render_template('learn_topic.html' , topic = topic , heading = heading)


# Video Player
@app.route('/video/<video_id>')
@login_required
def video(video_id):
   return render_template('video.html' , video_id = video_id)



#color Trading

class colorform(FlaskForm):
    color = RadioField('Label' , choices=[('1' , '1') , ('2' , '2') ,('3' , '3') ,('4' , '4')])
    amount = IntegerField('Enter the Betting Amount:' , validators=[DataRequired()])
    submit = SubmitField('submit')

user_choice = ''
comp = ''

@app.route('/earn')
@login_required
def earn():
    return render_template('earn.html')

@app.route('/game' , methods = ['GET' , 'POST'])
@login_required
def game():
    form = colorform()
    colours = [0 , 1 , 2 , 3 , 4]
    #Amount = request.form['amount']
    if form.validate_on_submit():
        user_choice = request.form['color']
        comp = random.choice(colours)
        balance = current_user.Wallet
        Amount = request.form['amount']
        if int(Amount)<100:
            flash("Min. Bet should be 100.")
        elif int(balance)<=int(Amount):
            flash("You don't  have sufficient Coins")
        else:
            if int(user_choice) == comp:
                Amount = request.form['amount']
                profit = int(Amount)/2
                current_user.Wallet += profit
                db.session.commit()
                return redirect('win')
            else:
                Amount = request.form['amount']
                loss = current_user.Wallet - int(Amount)
                current_user.Wallet = loss
                db.session.commit() 
                return redirect('loss' )
    return render_template('game.html' , form = form )
 
@app.route('/win')
@login_required
def win():
    return render_template('win.html')
@app.route('/loss')
@login_required
def loss():
    return render_template('loss.html')


##Payemnt

razorpay_client = razorpay.Client(auth=('rzp_test_cQCRSrPmXpnQyN', '7tMgufYsi6mnLmanQc46n9jX'))

@app.route('/payment')
@login_required
def payment():
    return render_template('payment.html')

@app.route('/charge', methods=['POST'])
def charge():
    if request.method == 'POST':
        amount = 299 * 100  # Amount in paise (299 INR)
        payment_data = {
            'amount': amount,
            'currency': 'INR',
            'receipt': 'receipt_order_123'
        }
        try:
            # Create Razorpay Order
            order = razorpay_client.order.create(data=payment_data)
            order_id = order['id']
            return render_template('payment.html', order_id=order_id, amount=amount)
        except Exception as e:
            return str(e)
    return "Invalid request."

@app.route('/success', methods=['POST'])
def success():
    razorpay_payment_id = request.form['razorpay_payment_id']
    razorpay_order_id = request.form['razorpay_order_id']
    current_user.Premium = 'YES'
    db.session.commit()
    try:
        # Capture the payment
        razorpay_client.payment.capture(razorpay_payment_id, amount=None)
        return jsonify({'status': 'success', 'message': 'Payment successful!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


# Configure Flask-Mail
def generate_otp():
    return random.randint(1000, 9999)

@app.route('/sendgmail', methods=['GET', 'POST'])
@login_required
def sendgmail():
    if request.method == 'POST':
        # Check if current_user.email is being fetched correctly
        email = current_user.Email
        if not email:
            flash('Error: User email not found. Please ensure you are logged in.', 'danger')
            return redirect(url_for('login'))  # Or any other appropriate route
        
        # Print the email to the console for debugging
        print(f"Sending OTP to: {email}")
        
        otp = generate_otp()
        session['otp'] = otp
        
        # Send OTP email
        msg = Message('BCA-Walla Verify your Email', recipients=[email])
        msg.body = f'Welcome to BCA-Wala!!.Your OTP code is {otp} and your Password is {current_user.Password}. Please keep this for future refrence.!!'
        
        try:
            mail_instance.send(msg)
            flash(f'OTP sent to {email}. Please check your inbox.', 'info')
        except Exception as e:
            flash(f'Failed to send email. Error: {str(e)}', 'danger')
            print(str(e))  # Print the error to the console for debugging
        
        return redirect(url_for('verify_otp'))
    
    return render_template('mail.html')
@app.route('/verify', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        otp = request.form['otp']
        if 'otp' in session and otp == str(session['otp']):
            flash('OTP verified successfully!', 'success')
            current_user.Email_Verify = "Verify"
            db.session.commit()
            return redirect(url_for('home'))
        else:
            flash('Invalid OTP. Please try again.', 'danger')
            return redirect(url_for('verify_otp'))
    
    return render_template('verify.html')


##Forgot Password
@app.route('/forgot_pass', methods=['GET', 'POST'])
def forgot_pass():
    if request.method == 'POST':
        email = request.form['email']
        email_check = mydatabase.query.filter_by(Email=email).first()
        
        if not email_check:
            flash('Error: User email not found. Please ensure you are logged in.', 'danger')
            return redirect(url_for('forgot_pass'))  # Corrected route name
        
        # Store the email in the session
        session['user_email'] = email
        
        # Print the email to the console for debugging
        print(f"Sending OTP to: {email}")
        
        otp = generate_otp()
        session['otp'] = otp  # Consider hashing the OTP
        
        # Send OTP email
        msg = Message('BCA-Walla Verify your Email', recipients=[email])
        msg.body = f'Welcome to BCA-Wala!!. Your OTP code is {otp}'
        
        try:
            mail_instance.send(msg)
            flash(f'OTP sent to {email}. Please check your inbox.', 'info')
        except Exception as e:
            flash(f'Failed to send email. Error: {str(e)}', 'danger')
            print(str(e))  # Print the error to the console for debugging
        
        return redirect(url_for('forgot_verify_otp'))
    
    return render_template('forpass.html')

@app.route('/forgot_verify_otp', methods=['GET', 'POST'])
def forgot_verify_otp():
    if request.method == 'POST':
        otp = request.form['otp']
        if 'otp' in session and otp == str(session['otp']):
            flash('OTP verified successfully!', 'success')
            return redirect(url_for('resetpass'))
        else:
            flash('Invalid OTP. Please try again.', 'danger')
            return redirect(url_for('forgot_verify_otp'))
    
    return render_template('forgetverify.html')

@app.route('/resetpass', methods=['GET', 'POST'])
def resetpass():
    user_email = session.get('user_email')
    if not user_email:
        flash('Error: Session expired or email not found.', 'danger')
        return redirect(url_for('forgot_pass'))
    
    if request.method == 'POST':
        user = mydatabase.query.filter_by(Email=user_email).first()
        if user:
            user.Password = request.form['password']
            db.session.commit()
            flash('Password reset successfully.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Error: User not found.', 'danger')
    
    return render_template('new_pass.html')



if __name__ == '__main__':
    app.run(debug=True)