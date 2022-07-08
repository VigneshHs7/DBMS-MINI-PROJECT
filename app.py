from flask import Flask,render_template,request, redirect,session, url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import mysql.connector
cnx = mysql.connector.connect(user='root', password='',
                              host='localhost',
                              database='stocks')
cnx.close()


app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/stocks'
db=SQLAlchemy(app)

local_server= True

app.secret_key='kusumachandashwini'

@app.route("/")
def index():
    return render_template('index.html')
    
@app.route("/ipo")
def ipo():
    return render_template('ipo.html')

@app.route("/admin")
def admin():
    return render_template('admin.html')


@app.route("/abt1")
def abt1():
    return render_template('abt1.html')

@app.route("/data")
def data():
    return render_template('data.html')

@app.route("/account")
def account():
    return render_template('account.html')



@app.route("/high")
def high():
    return render_template('high.html')

@app.route("/low")
def low():
    return render_template('low.html')

@app.route("/logo")
def logo():
    return render_template('logo.html')

@app.route("/data1")
def data1():
    return render_template('data1.html')

@app.route("/user")
def user():
    return render_template('user.html')





class User(UserMixin ,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50))
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(1000))

    # this is for getting unique user access
login_manager=LoginManager(app)
login_manager.login_view='login'



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
        

    return render_template('signup.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password,password):
            login_user(user)
            flash("Login Success","primary")
            return redirect(url_for('data'))
        else:
            flash("invalid credentials","danger")
            return render_template('login.html')    

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout SuccessFul","warning")
    return redirect(url_for('login'))
#------------------------------------------------------------------ADD STOCKS---------------------------------------------------------

class stockadd(db.Model):
    slno= db.Column(db.Integer, primary_key=True)
    sname= db.Column(db.String(200),nullable=False)
    syname= db.Column(db.String(200),nullable=False)
    oprice = db.Column(db.Float,nullable=False)
    hprice = db.Column(db.Float,nullable=False)
    lprice = db.Column(db.Float,nullable=False)
    setype = db.Column(db.String(200),  nullable=False)
    
    def __repr__(self) -> str:
        return f"{self.  slno} - {self.sname} - {self.syname} - {self.oprice} - {self.hprice} - {self.lprice}- {self.setype}"

@app.route("/add",methods=['GET','POST'])
def add():
    if request.method=='POST':
           
        sn = request.form['sname']
        sy= request.form['syname']
        op = request.form['oprice']
        hp = request.form['hprice']
        lp = request.form['lprice']
        setype=request.form['setype']
        add = stockadd( sname=sn, syname=sy , oprice=op , hprice=hp , lprice=lp , setype=setype)
        db.session.add(add)
        db.session.commit()
    astock = stockadd.query.all()    
    return render_template('add.html',astock=astock)  

@app.route('/upstocks/<int:slno>', methods=['GET', 'POST'])
def upstocks(slno):
    if request.method=='POST':
        sn = request.form['sname']
        sy= request.form['syname']
        op = request.form['oprice']
        hp = request.form['hprice']
        lp = request.form['lprice']
        setype=request.form['setype']
        add= stockadd.query.filter_by(slno=slno).first()
        add.sname=sn
        add.syname=sy
        add.oprice=op
        add.hprice=hp
        add.lprice=lp
        add.setype=setype
        db.session.add(add)
        db.session.commit()
        return redirect("/add")
        
    add= stockadd.query.filter_by(slno=slno).first()
    return render_template('upstocks.html', add=add)

@app.route('/delete/<int:slno>')
def delete(slno):
    add = stockadd.query.filter_by(slno=slno).first()
    db.session.delete(add)
    db.session.commit()
    return redirect("/add")

@app.route("/read",methods=['GET','POST'])
def read():
    if request.method=='POST':
           
        sn = request.form['sname']
        sy= request.form['syname']
        op = request.form['oprice']
        hp = request.form['hprice']
        lp = request.form['lprice']
        setype=request.form['setype']
        add = stockadd( sname=sn, syname=sy , oprice=op , hprice=hp , lprice=lp , setype=setype)
        db.session.add(add)
        db.session.commit()
    astock = stockadd.query.all()    
    return render_template('read.html',astock=astock)  



#-----------------------------------------------gainer---------------------------------------------------------------------------------------
class loser(db.Model):
    slno= db.Column(db.Integer, primary_key=True)
    sname= db.Column(db.String(200),nullable=False)
    syname= db.Column(db.String(200),nullable=False)
    sprice = db.Column(db.Float,nullable=False)
    
    setype = db.Column(db.String(200),  nullable=False)
    
    def __repr__(self) -> str:
        return f"{self.  slno} - {self.sname} - {self.syname} - {self.sprice} -  {self.setype}"

@app.route("/loser",methods=['GET','POST'])
def loss():
    if request.method=='POST':
           
        sn = request.form['sname']
        sy= request.form['syname']
        sp = request.form['sprice']
       
        setype=request.form['setype']
        loss=loser( sname=sn, syname=sy , sprice=sp ,  setype=setype)
        db.session.add(loss)
        db.session.commit()
    lss=loser.query.all()    
    return render_template('loser.html',lss=lss)

@app.route('/uploser/<int:slno>', methods=['GET', 'POST'])

def uploser(slno):
    if request.method=='POST':
        sn = request.form['sname']
        sy= request.form['syname']
        sp = request.form['sprice']
       
        setype=request.form['setype']
        add= loser.query.filter_by(slno=slno).first()
        add.sname=sn
        add.syname=sy
        add.sprice=sp
       
        add.setype=setype
        db.session.add(add)
        db.session.commit()
        return redirect("/loser")
        
    add=loser.query.filter_by(slno=slno).first()
    return render_template('uploser.html', add=add)

@app.route('/deleter/<int:slno>')
def deleter(slno):
    add = loser.query.filter_by(slno=slno).first()
    db.session.delete(add)
    db.session.commit()
    return redirect("/loser")

@app.route("/readl",methods=['GET','POST'])
def los():
    if request.method=='POST':
           
        sn = request.form['sname']
        sy= request.form['syname']
        sp = request.form['sprice']
       
        setype=request.form['setype']
        loss=loser( sname=sn, syname=sy , sprice=sp ,  setype=setype)
        db.session.add(loss)
        db.session.commit()
    lss=loser.query.all()    
    return render_template('readl.html',lss=lss)
class gainer(db.Model):
    slno= db.Column(db.Integer, primary_key=True)
    sname= db.Column(db.String(200),nullable=False)
    syname= db.Column(db.String(200),nullable=False)
    sprice = db.Column(db.Float,nullable=False)
    
    setype = db.Column(db.String(200),  nullable=False)
    
    def __repr__(self) -> str:
        return f"{self.  slno} - {self.sname} - {self.syname} - {self.sprice} -  {self.setype}"

@app.route("/gainer",methods=['GET','POST'])
def gai():
    if request.method=='POST':
           
        sn = request.form['sname']
        sy= request.form['syname']
        sp = request.form['sprice']
       
        setype=request.form['setype']
        gain =gainer( sname=sn, syname=sy , sprice=sp ,  setype=setype)
        db.session.add(gain)
        db.session.commit()
    again=gainer.query.all()    
    return render_template('gainer.html',again=again)

     
     

@app.route('/upgainer/<int:slno>', methods=['GET', 'POST'])
def upgainer(slno):
    if request.method=='POST':
        sn = request.form['sname']
        sy= request.form['syname']
        sp = request.form['sprice']
       
        setype=request.form['setype']
        add= gainer.query.filter_by(slno=slno).first()
        add.sname=sn
        add.syname=sy
        add.sprice=sp
       
        add.setype=setype
        db.session.add(add)
        db.session.commit()
        return redirect("/gainer")
        
    add= gainer.query.filter_by(slno=slno).first()
    return render_template('upgainer.html', add=add)


@app.route('/deleten/<int:slno>')
def deleten(slno):
    add = gainer.query.filter_by(slno=slno).first()
    db.session.delete(add)
    db.session.commit()
    return redirect("/gainer")

@app.route("/readg",methods=['GET','POST'])
def readg():
    if request.method=='POST':
           
        sn = request.form['sname']
        sy= request.form['syname']
        sp = request.form['sprice']
        
        setype=request.form['setype']
        add = gainer( sname=sn, syname=sy , sprice=sp , setype=setype)
        db.session.add(add)
        db.session.commit()
    again=gainer.query.all() 
    return render_template('readg.html', again=again)  
    

#------------------------------------------------------------------loser-----------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
    