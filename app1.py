from flask import Flask,render_template,request, redirect,session, url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import mysql.connector
cnx = mysql.connector.connect(user='root', password='',
                              host='localhost',
                              database='space')
cnx.close()
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/organ")
def organ():
    return render_template('organ.html')  

@app.route("/event")
def event():
    return render_template('event.html')


@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/read")
def read():
    return render_template('read.html')

    

app.secret_key='kusumachandashwini'
app.config['SECRET_KEY'] = 'kusumachandashwini'
app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:@localhost/space"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'




class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15))
    email= db.Column(db.String(100),unique=True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == "POST":
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()
        if user:
            flash("Email Already Exist","warning")
            return render_template('/signup.html')
        encpassword=generate_password_hash(password)

        new_user=db.engine.execute(f"INSERT INTO `user` (`username`,`email`,`password`) VALUES ('{username}','{email}','{encpassword}')")

        # this is method 2 to save data in db
        # newuser=User(username=username,email=email,password=encpassword)
        # db.session.add(newuser)
        # db.session.commit()
        flash("Signup Succes Please Login","success")
        return render_template('login.html')

          

    return render_template('signupt.html')




@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password,password):
            login_user(user)
            flash("Login Success","primary")
            return redirect(url_for('crud'))
        else:
            flash("invalid credentials","danger")
            return render_template('logint.html')    

    return render_template('logint.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout SuccessFul","warning")
    return redirect(url_for('login'))



#----------------------------------------------------------isro--------------------------------------#


class Isro(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    mname = db.Column(db.String(200),nullable=False)
    launcher = db.Column(db.String(200),  nullable=False)
    mstatus = db.Column(db.String(200),  nullable=False)
    purpose = db.Column(db.String(200),  nullable=False)
    lyear = db.Column(db.Integer,  nullable=False)
    
    def __repr__(self) -> str:
        return f"{self.sno} - {self.mname} - {self.launcher} - {self.mstatus} - {self.purpose} - {self.lyear}"


        
       
@app.route("/isro",methods=['GET','POST'])
def dabse():
    if request.method=='POST':
           
        mn = request.form['mname']
        ln= request.form['launcher']
        ms = request.form['mstatus']
        pu = request.form['purpose']
        ly = request.form['lyear']
        isro = Isro( mname=mn, launcher=ln, mstatus=ms, purpose=pu, lyear=ly)
        db.session.add(isro)
        db.session.commit()
    allIsro = Isro.query.all()    
    return render_template('isro.html',allIsro=allIsro)


@app.route('/upisro/<int:sno>', methods=['GET', 'POST'])
def upisro(sno):
    if request.method=='POST':
        mn = request.form['mname']
        ms = request.form['mstatus']
        isro = Isro.query.filter_by(sno=sno).first()
        isro.mname= mn
        isro.mstatus = ms
        db.session.add(isro)
        db.session.commit()
        return redirect("/isro")
        
    isro = Isro.query.filter_by(sno=sno).first()
    return render_template('upisro.html', isro=isro)

@app.route('/delete/<int:sno>')
def delete(sno):
    isro = Isro.query.filter_by(sno=sno).first()
    db.session.delete(isro)
    db.session.commit()
    return redirect("/isro")


@app.route("/table")
def table():
     if request.method=='POST':
           
        mn = request.form['mname']
        ln= request.form['launcher']
        ms = request.form['mstatus']
        pu = request.form['purpose']
        ly = request.form['lyear']
        isro = Isro( mname=mn, launcher=ln, mstatus=ms, purpose=pu, lyear=ly)
        db.session.add(isro)
        db.session.commit()
     allIsro = Isro.query.all()    
     return render_template('table.html',allIsro=allIsro)


#----------------------------------------nasa--------------------------------------#
class Nasa(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    mname = db.Column(db.String(200),nullable=False)
    launcher = db.Column(db.String(200),  nullable=False)
    mstatus = db.Column(db.String(200),  nullable=False)
    purpose = db.Column(db.String(200),  nullable=False)
    lyear = db.Column(db.Integer,  nullable=False)
    
    def __repr__(self) -> str:
        return f"{self.sno} - {self.mname} - {self.launcher} - {self.mstatus} - {self.purpose} - {self.lyear}"     
       
@app.route("/nasa",methods=['GET','POST'])
def nasa():
    if request.method=='POST':
        
        mn = request.form['mname']
        ln= request.form['launcher']
        ms = request.form['mstatus']
        pu = request.form['purpose']
        ly = request.form['lyear']
        nasa = Nasa( mname=mn, launcher=ln, mstatus=ms, purpose=pu, lyear=ly)
        db.session.add(nasa)
        db.session.commit()
    allNasa = Nasa.query.all()    
    return render_template('nasa.html',allNasa=allNasa)

@app.route('/upnasa/<int:sno>', methods=['GET', 'POST'])
def upnasa(sno):
    if request.method=='POST':
        mn = request.form['mname']
        ms = request.form['mstatus']
        nasa = Nasa.query.filter_by(sno=sno).first()
        nasa.mname= mn
        nasa.mstatus = ms
        db.session.add(nasa)
        db.session.commit()
        return redirect("/nasa")
        
    nasa = Nasa.query.filter_by(sno=sno).first()
    return render_template('upnasa.html', nasa=nasa)

@app.route('/deleten/<int:sno>')
def deleten(sno):
    nasa = Nasa.query.filter_by(sno=sno).first()
    db.session.delete(nasa)
    db.session.commit()
    return redirect("/nasa")

@app.route("/tablen")
def tablen():
     if request.method=='POST':
           
        mn = request.form['mname']
        ln= request.form['launcher']
        ms = request.form['mstatus']
        pu = request.form['purpose']
        ly = request.form['lyear']
        isro = Nasa( mname=mn, launcher=ln, mstatus=ms, purpose=pu, lyear=ly)
        db.session.add(isro)
        db.session.commit()
     allNasa = Nasa.query.all()    
     return render_template('tablen.html',allNasa=allNasa)


#--------------------------------------------------------ros-------------------------------------------------------#

class ROS(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    mname = db.Column(db.String(200),nullable=False)
    launcher = db.Column(db.String(200),  nullable=False)
    mstatus = db.Column(db.String(200),  nullable=False)
    purpose = db.Column(db.String(200),  nullable=False)
    lyear = db.Column(db.Integer,  nullable=False)
    
    def __repr__(self) -> str:
        return f"{self.sno} - {self.mname} - {self.launcher} - {self.mstatus} - {self.purpose} - {self.lyear}"


        
       
@app.route("/ros",methods=['GET','POST'])
def ros():
    if request.method=='POST':
       
        mn = request.form['mname']
        ln= request.form['launcher']
        ms = request.form['mstatus']
        pu = request.form['purpose']
        ly = request.form['lyear']
        ros = ROS( mname=mn, launcher=ln, mstatus=ms, purpose=pu, lyear=ly)
        db.session.add(ros)
        db.session.commit()
    allros = ROS.query.all()    
    return render_template('ros.html',allros=allros)

@app.route('/upros/<int:sno>', methods=['GET', 'POST'])
def upros(sno):
    if request.method=='POST':
        mn = request.form['mname']
        ms = request.form['mstatus']
        ros = ROS.query.filter_by(sno=sno).first()
        ros.mname= mn
        ros.mstatus = ms
        db.session.add(ros)
        db.session.commit()
        return redirect("/ros")
        
    ros = ROS.query.filter_by(sno=sno).first()
    return render_template('upros.html', ros=ros)

@app.route('/deleter/<int:sno>')
def deleter(sno):
    ros = ROS.query.filter_by(sno=sno).first()
    db.session.delete(ros)
    db.session.commit()
    return redirect("/ros")  

@app.route("/tabler")
def tabler():
     if request.method=='POST':
           
        mn = request.form['mname']
        ln= request.form['launcher']
        ms = request.form['mstatus']
        pu = request.form['purpose']
        ly = request.form['lyear']
        ros = ROS( mname=mn, launcher=ln, mstatus=ms, purpose=pu, lyear=ly)
        db.session.add(ros)
        db.session.commit()
     allros = ROS.query.all()    
     return render_template('tabler.html',allros=allros)



 #----------------------------------------------------------jaxa-------------------------------------------#   
class JAXA(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    mname = db.Column(db.String(200),nullable=False)
    launcher = db.Column(db.String(200),  nullable=False)
    mstatus = db.Column(db.String(200),  nullable=False)
    purpose = db.Column(db.String(200),  nullable=False)
    lyear = db.Column(db.Integer,  nullable=False)
    
    def __repr__(self) -> str:
        return f"{self.sno} - {self.mname} - {self.launcher} - {self.mstatus} - {self.purpose} - {self.lyear}"


        
       
@app.route("/jaxa",methods=['GET','POST'])
def jaxa():
    if request.method=='POST':
        
        mn = request.form['mname']
        ln= request.form['launcher']
        ms = request.form['mstatus']
        pu = request.form['purpose']
        ly = request.form['lyear']
        jaxa = JAXA( mname=mn, launcher=ln, mstatus=ms, purpose=pu, lyear=ly)
        db.session.add(jaxa)
        db.session.commit()
    alljaxa = JAXA.query.all()    
    return render_template('jaxa.html',alljaxa=alljaxa)


@app.route('/upjaxa/<int:sno>', methods=['GET', 'POST'])
def upjaxa(sno):
    if request.method=='POST':
        mn = request.form['mname']
        ms = request.form['mstatus']
        jaxa = JAXA.query.filter_by(sno=sno).first()
        jaxa.mname= mn
        jaxa.mstatus = ms
        db.session.add(jaxa)
        db.session.commit()
        return redirect("/jaxa")
        
    jaxa = JAXA.query.filter_by(sno=sno).first()
    return render_template('upjaxa.html', jaxa=jaxa)

@app.route('/deletej/<int:sno>')
def deletej(sno):
    jaxa = JAXA.query.filter_by(sno=sno).first()
    db.session.delete(jaxa)
    db.session.commit()
    return redirect("/jaxa")

@app.route("/crud")
def crud():
    return render_template('crud.html')

@app.route("/tablej")
def tablej():
     if request.method=='POST':
           
        mn = request.form['mname']
        ln= request.form['launcher']
        ms = request.form['mstatus']
        pu = request.form['purpose']
        ly = request.form['lyear']
        jaxa = JAXA( mname=mn, launcher=ln, mstatus=ms, purpose=pu, lyear=ly)
        db.session.add(jaxa)
        db.session.commit()
     alljaxa = JAXA.query.all()    
     return render_template('tablej.html',alljaxa=alljaxa)

    
if __name__ == "__main__":
    app.run(debug=True)
    
  