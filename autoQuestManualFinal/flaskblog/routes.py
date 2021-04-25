from flaskblog.models import User,Post
from flaskblog.forms import RegistrationForm, LoginForm
from flask import render_template, url_for, flash, redirect,Flask,request,make_response,session
from flaskblog import app
import mysql.connector as mysql
from mysql.connector import Error
from mysql.connector import errorcode
from datetime import date 
from requests.models import Response
from flask import Response
import tkinter
from tkinter import messagebox
import pyautogui as pag
import pdfkit as pdf
from scrapy.selector import Selector 
from scrapy.http import HtmlResponse
import pandas
from io import StringIO
import sys
import random,numpy




#from flask.ext.cache import Cache   
global q1a
global q1b
global q1c
global q2a
global q2b
global q2c
global q2cc
global q3a
global q3b
global q3c
global q3aa
global q3bb
global q3cc
global q4a
global q4b
global q4c
global q4aa
global q4bb
global q4cc
global q5a
global q5b
global q5c
global q5aa
global q5bb
global q5cc
global loggedIn
loggedIn = 0
global dat
dat = date.today()
global semester1
global subject1
global subjectCode
global duration
global totalMarks
totalMarks = 0
global marks1
marks1 = 0
global marks2
marks2=0
global marks3
marks3=0
global difficultyLevel1
global number_of_Ques1
global number_of_Ques2
global number_of_Ques3
global dataA
dataA = ''
global dataB
dataB = ''
global dataC
dataC = ''
global getPdf
getPdf = 0




posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    Response().headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    Response().headers["Pragma"] = "no-cache"
    Response().headers["Expires"] = "0"
    Response().headers['Cache-Control'] = 'public, max-age=0'
    return render_template('home.html', title='Home',posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/contactUs")
def contactUs():
    return render_template('contactUs.html', title='Contact')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        form = RegistrationForm()
        db = mysql.connect(
        host = "localhost",
        user = "root",
        passwd = "",
        database = "mydatabase")
        found = 0
        myName = form.username.data
        myEmail = form.email.data
        cur = db.cursor()
# Select data from table using SQL query.
        cur.execute("SELECT * FROM login")
# print the first and second columns    
        for row in cur.fetchall():
            if row[1]==myName:
                found=1
                flash('Username already exists', 'danger')
                break
            elif row[2]==myEmail:
                found=1
                flash('Email already exists', 'danger')
                break
        if found==0:
            val = (form.username.data,form.email.data,form.password.data)
            query ="INSERT INTO login(Username,Email,Password) VALUES (%s,%s,%s)"
## There is no need to insert the value of rollno 
## because in our table rollno is autoincremented #started from 1
## storing values in a variable
## executing the query with values
            cur.execute(query,val)
## to make final output we have to run 
## the 'commit()' method of the database object
            db.commit()
            flash(f'Account created for {myName} ! ', 'success')
            #return render_template('login.html', title='Login', form=form)
    return render_template('register.html', title='Register', form=form)


@app.route("/welcome", methods=['GET', 'POST'])
def welcome():
    form = RegistrationForm()
    return render_template('welcome.html', title='Welcome',form=form)        
 


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    found = 0
    myName = form.username.data
    myEmail = form.email.data
    myPassword = form.password.data
    if form.validate_on_submit():
        form = LoginForm()
        found = 0
        myPassword = form.password.data
        db = mysql.connect(
        host = "localhost",
        user = "root",
        passwd = "",
        database = "mydatabase")
        cur = db.cursor()
# Select data from table using SQL query.
        cur.execute("SELECT * FROM login")
# print the first and second columns    
        for row in cur.fetchall():
            if row[1]==myName and row[3]==myPassword:
                if row[2]==myEmail:
                    found=2
                    break
                else:
                    found=1
                    flash('Login Unsuccessful. Please check email', 'danger')

        if found==0:
            flash('Login Unsuccessful. Please check username and password', 'danger')
        elif found==2:
            session['username'] = myName
            global loggedIn
            loggedIn = 1
            flash("Login successful",'success')
            response = make_response()
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            Response().headers["Pragma"] = "no-cache"
            Response().headers["Expires"] = "0"
            Response().headers['Cache-Control'] = 'public, max-age=0'
            return redirect(url_for('Index',username=myName))
    return render_template('login.html', title='Login', form=form)

@app.route('/index/<string:username>')
def Index(username):
    if "username" in session:
        return render_template('index.html',username=username)
    else:
        return redirect(url_for('home'))

@app.route('/index/<string:username>/subjects')
def showSubjects(username):
    if "username" in session:
        db = mysql.connect(
            host = "localhost",
            user = "root",
            passwd = "",
            database = "mydatabase")
        cur = db.cursor()
        cur.execute("SELECT subjects.Subject_code,subjects.subject_name,count(questions.question) FROM subjects inner join questions on subjects.Subject_code=questions.Subject_code")
        subjects = cur.fetchall()
        return render_template('subjects.html',username=username,subjects=subjects)
    else:
        return redirect(url_for('home'))        



@app.route('/index/<string:username>/questions')
#@app.cache.cached(timeout=0)
def Index2(username):
    if "username" in session:
        response = make_response()
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        Response().headers["Pragma"] = "no-cache"
        Response().headers["Expires"] = "0"
        Response().headers['Cache-Control'] = 'public, max-age=0'
        db = mysql.connect(
            host = "localhost",
            user = "root",
            passwd = "",
            database = "mydatabase")
        cur = db.cursor()
        cur.execute("SELECT * FROM questions WHERE Username=%s",(username,))
        data = cur.fetchall()
        cur.close()
        return render_template('index2.html', questions=data, username=username)
    else:
        return redirect(url_for('home'))


@app.route('/home', methods = ['POST'])
def logout():
    session.pop('username', None)
    global loggedIn
    loggedIn = 0
    response = make_response()
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    #Response().headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    Response().headers["Pragma"] = "no-cache"
    Response().headers["Expires"] = "0"
    Response().headers['Cache-Control'] = 'public, max-age=0'
    return render_template('home.html', title='Home')




@app.route('/insert/<string:username>', methods = ['POST'])
def insert(username):

    if request.method == "POST":
        recordFound = 0
        
        
        #driver = webdriver.Chrome(executable_path="E:/darshan sem 7/project/flaskTutorial/flaskAutoQuestCRUD/chromedriver.exe")
        #driver = webdriver.get("file:///E:/darshan%20sem%207/project/flaskTutorial/flaskAutoQuestCRUD/templates/addstudent.html")
        #element = driver.find_element_by_id("semesterDropDown")
        #drp = Select(element)
        #semester = drp.first_selected_option.text
        #print(select.first_selected_option.text)
        #print(select.first_selected_option.get_attribute("value"))
        
        subjectCode = int(request.form['subjectCode'])
        unit = int(request.form['unit'])
        #marks = int(request.form['marks'])
        #difficultyLevel = request.form['difficultyLevel']
        marks = int(request.form['marks'])
        
        difficultyLevel = request.form.get('difficultyLevel')
        
        question = request.form['question']

        #if question==" ":
         #   root = tkinter.Tk()
          #  root.withdraw()

# message box display
           # messagebox.showerror("Error", "Please insert the question")
        
        db = mysql.connect(
            host = "localhost",
            user = "root",
            passwd = "",
            database = "mydatabase")
        cur = db.cursor(buffered=True)
        cur.execute("SELECT * FROM questions WHERE Username=%s AND Subject_code=%s AND Question=%s",(username,subjectCode,question))
        r=cur.fetchall()
        recordFound=cur.rowcount
        if recordFound==1:
            flash("Record already exists\n You might want to update it.",'danger')
            return redirect(url_for('Index',username=username))
            

        elif recordFound==0:
            cur = db.cursor(buffered=True)
            cur.execute("INSERT INTO questions (Username,Subject_code,Unit,Marks,Difficulty_level,Question) VALUES (%s, %s, %s, %s , %s, %s)", (username,subjectCode,unit,marks,difficultyLevel,question))
            db.commit()
            flash("Question Inserted Successfully","success")
            return redirect(url_for('Index',username=username))


    


@app.route('/delete/<string:id_data>/<string:username>', methods = ['POST','GET'])
def delete(id_data,username):
    flash("Question Has Been Deleted Successfully","success")
    db = mysql.connect(
        host = "localhost",
        user = "root",
        passwd = "",
        database = "mydatabase")
    cur = db.cursor()
    cur.execute("DELETE FROM questions WHERE id=%s", (id_data,))
    db.commit()
    return redirect(url_for('Index',username=username))



@app.route('/update/<string:username>',methods=['POST','GET'])
def update(username):

    if request.method == 'POST':
        id_data = request.form['id']
        
        #semester = request.form.select['semester']
        subjectCode = int(request.form['subjectCode'])

        unit = int(request.form['unit'])
        marks = request.form['marks']
        difficultyLevel = request.form.get('difficultyLevel')
        question = request.form['question']
        db = mysql.connect(
            host = "localhost",
            user = "root",
            passwd = "",
            database = "mydatabase")
        cur = db.cursor()
        cur.execute("""
               UPDATE questions
               SET Subject_code=%s, Unit=%s, Marks=%s, Difficulty_level=%s, Question=%s
               WHERE id=%s
            """, (subjectCode,unit,marks,difficultyLevel,question, id_data))
        flash("Question Updated Successfully","success")
        db.commit()
        return redirect(url_for('Index',username=username))



@app.route('/index/<string:username>/generate')
def generate(username):
    if "username" in session:
        response = make_response()
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        Response().headers["Pragma"] = "no-cache"
        Response().headers["Expires"] = "0"
        Response().headers['Cache-Control'] = 'public, max-age=0'
        return render_template('generate.html', username=username)
    else:
        return redirect(url_for('home'))
        
        """
    if loggedIn == 0:
        return redirect(url_for('home'))
    elif loggedIn == 1:
        response = make_response()
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        Response().headers["Pragma"] = "no-cache"
        Response().headers["Expires"] = "0"
        Response().headers['Cache-Control'] = 'public, max-age=0'
        return render_template('generate.html', username=username)
        """
        

@app.route('/index/<string:username>/generate/ques_paper',methods=['POST','GET'])
def questionPaperGenerate(username):
   # if request.method == 'POST':
        #semester = request.form.select['semester']
    if "username" not in session:
        return redirect(url_for('home'))
    sectionError = 0
    msg1 = ''
    msg2 = ''
    msg3 = ''
    global semester1
    semester1 = request.form.get('semester')
    global subject1
    subject1 = request.form['subject']
    global subjectCode
    subjectCode = request.form['subjectCode']
    durationHours = request.form['hours']
    durationMinutes = request.form['mins']
    global duration
    duration = durationHours+' hours '+durationMinutes+' minutes'
    #global marks1
    #marks1 = int(request.form['marks1'])
    #difficultyLevel1 = request.form.get('difficultyLevel1')
    #global number_of_Ques1
    #number_of_Ques1 = int(request.form['noOfQues1'])
    db = mysql.connect(
        host = "localhost",
        user = "root",
        passwd = "",
        database = "mydatabase")

    cur1 = db.cursor(buffered=True)
    cur1.execute("SELECT Marks,Question FROM questions WHERE Username=%s AND Subject_code=%s AND Marks='3' order by rand()",(username,subjectCode))
    
    if cur1.rowcount<8:
        sectionError+=1
        msg1+='\n3 Marks Questions:\nInsert desired questions in the AutoQuest system'

    #global dataA
    #dataA = cur1.fetchall()

    
        
    #global marks2
    #marks2 = int(request.form['marks2'])
    #difficultyLevel2 = request.form.get('difficultyLevel2')
    #global number_of_Ques2
    #number_of_Ques2 = int(request.form['noOfQues2'])
    cur2 = db.cursor(buffered=True)
    cur2.execute("SELECT Marks,Question FROM questions WHERE Username=%s AND Subject_code=%s AND Marks='4' order by rand()",(username,subjectCode))
    if cur2.rowcount<8:
        sectionError+=1
        msg2+='\n4 Marks Questions:\nInsert desired questions in the AutoQuest system'
    

    #global marks3
    #marks3 = int(request.form['marks3'])
    #difficultyLevel3 = request.form.get('difficultyLevel3')
    #global number_of_Ques3
    #number_of_Ques3 = int(request.form['noOfQues3'])
    cur3 = db.cursor(buffered=True)
    cur3.execute("SELECT Marks,Question FROM questions WHERE Username=%s AND Subject_code=%s AND Marks='7' order by rand()",(username,subjectCode))
    if cur3.rowcount<9:
        sectionError+=1
        msg3+='\n7 Marks Questions:\nInsert desired questions in the AutoQuest system'
    



    if sectionError==0:
        '''
        global totalMarks
        m1 = marks1*number_of_Ques1
        m2 = marks2*number_of_Ques2
        m3 = marks3*number_of_Ques3
        totalMarks=int(m1+m2+m3)
        '''





        '''
        cur1.execute("SELECT Marks,Question FROM questions WHERE Username=%s AND Semester=%s AND Subject=%s AND Marks='3' order by rand() limit 8",(username,semester1,subject1))
        global q1a
        q1a = cur1.fetchmany(1)
        global q2a
        q2a = cur1.fetchmany(1)
        global q3a
        q3a = cur1.fetchmany(1)
        global q3aa
        q3aa = cur1.fetchmany(1)
        global q4a
        q4a = cur1.fetchmany(1)
        global q4aa
        q4aa = cur1.fetchmany(1)
        global q5a
        q5a = cur1.fetchmany(1)
        global q5aa
        q5aa = cur1.fetchmany(1)
        cur2.execute("SELECT Marks,Question FROM questions WHERE Username=%s AND Semester=%s AND Subject=%s AND Marks='4' order by rand() limit 8",(username,semester1,subject1))
        global q1b
        q1b = cur2.fetchmany(1)
        global q2b
        q2b = cur2.fetchmany(1)
        global q3b
        q3b = cur2.fetchmany(1)
        global q3bb
        q3bb = cur2.fetchmany(1)
        global q4b
        q4b = cur2.fetchmany(1)
        global q4bb
        q4bb = cur2.fetchmany(1)
        global q5b
        q5b = cur2.fetchmany(1)
        global q5bb
        q5bb = cur2.fetchmany(1)
        
        cur3.execute("SELECT Marks,Question FROM questions WHERE Username=%s AND Semester=%s AND Subject=%s AND Marks='7' order by rand() limit 9",(username,semester1,subject1))
        global q1c
        q1c = cur3.fetchmany(1)
        global q2c
        q2c = cur3.fetchmany(1)
        global q2cc
        q2cc = cur3.fetchmany(1)
        global q3c
        q3c = cur3.fetchmany(1)
        global q3cc
        q3cc = cur3.fetchmany(1)
        global q4c
        q4c = cur3.fetchmany(1)
        global q4cc
        q4cc = cur3.fetchmany(1)
        global q5c
        q5c = cur3.fetchmany(1)
        global q5cc
        q5cc = cur3.fetchmany(1)
        cur3.close()
        '''



        cur = db.cursor(buffered=True)
        cur.execute("SELECT Number_of_units FROM subjects WHERE Subject_code=%s",(subjectCode,))
        for Device in cur.fetchmany(1):
            NoOfUnits=Device[0]
   
        finalAns=[]
        subjectCode = '2170710'

    
        for i in range(1,int(NoOfUnits)+1):
            cur.execute("SELECT Weightage FROM units WHERE Subject_code=%s AND Unit=%s",(subjectCode,i))
            for Device in cur.fetchmany(1):
                weightage=Device[0]
            finalWeightage=119*weightage
        #cur.execute("(SELECT  Unit,NULL as question, NULL as marks, NULL AS total FROM questions WHERE ((@total := 0)) UNION SELECT Unit,question,marks, @total := @total + marks AS total FROM questions WHERE Subject_code=%s AND Unit=%s AND marks=3 AND @total<119*0.1/5.5 ORDER BY RAND()) UNION (SELECT  Unit,NULL as question, NULL as marks, NULL AS total FROM questions WHERE ((@total := 0)) UNION SELECT Unit,question,marks, @total := @total + marks AS total FROM questions WHERE Subject_code=%s AND Unit=%s AND marks=4 AND @total<119*0.1/2 ORDER BY RAND()) UNION (SELECT  Unit,NULL as question, NULL as marks, NULL AS total FROM questions WHERE ((@total := 0)) UNION SELECT Unit,question,marks, @total := @total + marks AS total FROM questions WHERE Subject_code=%s AND Unit=%s AND marks=7 AND @total<119*0.1 ORDER BY RAND())",(subjectCode,i,subjectCode,i,subjectCode,i))
            cur.execute("(SELECT  Unit,NULL as question, NULL as marks, NULL AS total FROM questions WHERE ((@total := 0)) UNION SELECT Unit,question,marks, @total := @total + marks AS total FROM questions WHERE Subject_code=%s AND Unit=%s AND marks=3 AND @total<%s ORDER BY RAND()) UNION (SELECT  Unit,NULL as question, NULL as marks, NULL AS total FROM questions WHERE ((@total := 0)) UNION SELECT Unit,question,marks, @total := @total + marks AS total FROM questions WHERE Subject_code=%s AND Unit=%s AND marks=4 AND @total<%s ORDER BY RAND()) UNION (SELECT  Unit,NULL as question, NULL as marks, NULL AS total FROM questions WHERE ((@total := 0)) UNION SELECT Unit,question,marks, @total := @total + marks AS total FROM questions WHERE Subject_code=%s AND Unit=%s AND marks=7 AND @total<%s ORDER BY RAND())",(subjectCode,i,finalWeightage/5.5,subjectCode,i,finalWeightage/2,subjectCode,i,finalWeightage))
            tempAns=cur.fetchall()
            tempAns=list(tempAns)
            finalAns=finalAns+tempAns
        random.shuffle(finalAns)
        finalAns=list(finalAns)
        marks3 = [num for num in finalAns if num[2]==3]
        marks4 = [num for num in finalAns if num[2]==4]
        marks7 = [num for num in finalAns if num[2]==7]
        marks3=list(marks3)
        marks4=list(marks4)
        marks7=list(marks7)
        random.shuffle(marks3)
        random.shuffle(marks4)
        random.shuffle(marks7)
    #ques1a = marks3[0:1]
    #ques1a=list(ques1a)
        global q1a
        q1a=[item[1:3] for item in list(marks3[0:1])]
        q1a=list(q1a)
        global q2a
        q2a=[item[1:3] for item in list(marks3[1:2])]
        q2a=list(q2a)
        global q3a
        q3a=[item[1:3] for item in list(marks3[2:3])]
        q3a=list(q3a)
        global q3aa
        q3aa=[item[1:3] for item in list(marks3[3:4])]
        q3aa=list(q3aa)
        global q4a
        q4a=[item[1:3] for item in list(marks3[4:5])]
        q4a=list(q4a)
        global q4aa
        q4aa=[item[1:3] for item in list(marks3[5:6])]
        q4aa=list(q4aa)
        global q5a
        q5a=[item[1:3] for item in list(marks3[6:7])]
        q5a=list(q5a)
        global q5aa
        q5aa=[item[1:3] for item in list(marks3[7:8])]
        q5aa=list(q5aa)

        global q1b
        q1b=[item[1:3] for item in list(marks4[0:1])]
        q1b=list(q1b)
        global q2b
        q2b=[item[1:3] for item in list(marks4[1:2])]
        q2b=list(q2b)
        global q3b
        q3b=[item[1:3] for item in list(marks4[2:3])]
        q3b=list(q3b)
        global q3bb
        q3bb=[item[1:3] for item in list(marks4[3:4])]
        q3bb=list(q3bb)
        global q4b
        q4b=[item[1:3] for item in list(marks4[4:5])]
        q4b=list(q4b)
        global q4bb
        q4bb=[item[1:3] for item in list(marks4[5:6])]
        q4bb=list(q4bb)
        global q5b
        q5b=[item[1:3] for item in list(marks4[6:7])]
        q5b=list(q5b)
        global q5bb
        q5bb=[item[1:3] for item in list(marks4[7:8])]
        q5bb=list(q5bb)

        global q1c
        q1c=[item[1:3] for item in list(marks7[0:1])]
        q1c=list(q1c)
        global q2c
        q2c=[item[1:3] for item in list(marks7[1:2])]
        q2c=list(q2c)
        global q2cc
        q2cc=[item[1:3] for item in list(marks7[2:3])]
        q2cc=list(q2cc)
        global q3c
        q3c=[item[1:3] for item in list(marks7[3:4])]
        q3c=list(q3c)
        global q3cc
        q3cc=[item[1:3] for item in list(marks7[4:5])]
        q3cc=list(q3cc)
        global q4c
        q4c=[item[1:3] for item in list(marks7[5:6])]
        q4c=list(q4c)
        global q4cc
        q4cc=[item[1:3] for item in list(marks7[6:7])]
        q4cc=list(q4cc)
        global q5c
        q5c=[item[1:3] for item in list(marks7[7:8])]
        q5c=list(q5c)
        global q5cc
        q5cc=[item[1:3] for item in list(marks7[8:9])]
        q5cc=list(q5cc)
        flash("Question paper generated!","success")
        return render_template('quesPaper.html', username=username,q1a=q1a,q1b=q1b,q1c=q1c,q2a=q2a,q2b=q2b,q2c=q2c,q2cc=q2cc,q3a=q3a,q3b=q3b,q3c=q3c,q3aa=q3aa,q3bb=q3bb,q3cc=q3cc,q4a=q4a,q4b=q4b,q4c=q4c,q4aa=q4aa,q4bb=q4bb,q4cc=q4cc,q5a=q5a,q5b=q5b,q5c=q5c,q5aa=q5aa,q5bb=q5bb,q5cc=q5cc, semester=semester1,subject=subject1,subjectCode=subjectCode,duration=duration,date=dat,getPdf=getPdf)

    else:
        #root = tkinter.Tk()
        #root.withdraw()
        #messagebox.showinfo("Title", "Message")
        #win32api.MessageBox(0, 'hello', 'title')
        #pag.alert(text=msg, title="Couldn't generate question paper")
        if msg1!='':
            flash(msg1, 'danger')
        if msg2!='':
            flash(msg2, 'danger')
        if msg3!='':
            flash(msg3, 'danger')
        
        return redirect(url_for('generate',username=username))
    
"""

@app.route('/index/<string:username>/generate',methods=['POST','GET'])
def questionPaperB(username):
   # if request.method == 'POST':
        #semester = request.form.select['semester']
    
    global semester2
    global subject2
    global marks2
    global difficultyLevel2
    global number_of_Ques2
    global sectionB
    sectionB = 1
    semester2 = int(request.form.get('semester'))

    subject2 = request.form['subject']
    
    marks2 = request.form['marks2']
    difficultyLevel2 = request.form.get('difficultyLevel2')
    number_of_Ques2 = int(request.form['noOfQues2'])
    db = mysql.connect(
        host = "localhost",
        user = "root",
        passwd = "",
        database = "mydatabase")
    cur = db.cursor()
    cur.execute("SELECT Marks,Question FROM questions WHERE Username=%s AND Semester=%s AND Subject=%s AND Marks=%s AND Difficulty_level=%s order by rand() limit %s",(username,semester2,subject2,marks2,difficultyLevel2,number_of_Ques2))
    global dataB
    dataB = cur.fetchall()
    cur.close()
    dat = date.today()
    return redirect(url_for('generate',username=username))


@app.route('/index/<string:username>/generate',methods=['POST','GET'])
def questionPaperC(username):
   # if request.method == 'POST':
        #semester = request.form.select['semester']
    
    global sectionC
    sectionC = 1
    
    global semester3
    global subject3
    global marks3
    global difficultyLevel3
    global number_of_Ques3
    semester3 = int(request.form.get('semester'))

    subject3 = request.form['subject']
   
    marks3 = request.form['marks3']
    difficultyLevel3 = request.form.get('difficultyLevel3')
    number_of_Ques3 = int(request.form['noOfQues3'])
    db = mysql.connect(
        host = "localhost",
        user = "root",
        passwd = "",
        database = "mydatabase")
    cur = db.cursor()
    cur.execute("SELECT Marks,Question FROM questions WHERE Username=%s AND Semester=%s AND Subject=%s AND Marks=%s AND Difficulty_level=%s order by rand() limit %s",(username,semester3,subject3,marks3,difficultyLevel3,number_of_Ques3))
    global dataC
    dataC = cur.fetchall()
    cur.close()
    dat = date.today()
    return redirect(url_for('generate',username=username))
"""



@app.route('/index/<string:username>/generate/question_paper',methods=['POST','GET'])
def questionPaper(username):
    if "username" not in session:
        return redirect(url_for('home'))
    global dat 
    dat = date.today()
    return render_template('quesPaper.html', username=username,q1a=q1a,q1b=q1b,q1c=q1c,q2a=q2a,q2b=q2b,q2c=q2c,q2cc=q2cc,q3a=q3a,q3b=q3b,q3c=q3c,q3aa=q3aa,q3bb=q3bb,q3cc=q3cc,q4a=q4a,q4b=q4b,q4c=q4c,q4aa=q4aa,q4bb=q4bb,q4cc=q4cc,q5a=q5a,q5b=q5b,q5c=q5c,q5aa=q5aa,q5bb=q5bb,q5cc=q5cc, semester=semester1,subject=subject1,subjectCode=subjectCode,duration=duration,date=dat,getPdf=getPdf)

@app.route('/index/<string:username>/generate/pdf',methods=['POST','GET'])
def PDFOfQuestionPaper(username,**args):
    if "username" not in session:
        return redirect(url_for('home'))
    config = pdf.configuration(wkhtmltopdf="E:/wkhtmltopdf/bin/wkhtmltopdf.exe")
    dat = date.today()
    #global getPdf
    getPdf = 1
    html = render_template('quesPaper.html',q1a=q1a,q1b=q1b,q1c=q1c,q2a=q2a,q2b=q2b,q2c=q2c,q2cc=q2cc,q3a=q3a,q3b=q3b,q3c=q3c,q3aa=q3aa,q3bb=q3bb,q3cc=q3cc,q4a=q4a,q4b=q4b,q4c=q4c,q4aa=q4aa,q4bb=q4bb,q4cc=q4cc,q5a=q5a,q5b=q5b,q5c=q5c,q5aa=q5aa,q5bb=q5bb,q5cc=q5cc, semester=semester1,subject=subject1,subjectCode=subjectCode,duration=duration,date=dat,getPdf=getPdf)
    #file_class = Pdf()
    from xhtml2pdf import pisa
    from io import BytesIO
    #FileName = 'semester'+semester1+subject1+'question_paper'
    #from StringIO import StringIO

    PDF = BytesIO()
    

    pisa.CreatePDF(BytesIO(html.encode()),PDF)

    valueOfData =  PDF.getvalue()
    headers = {
        'content-type': 'application.pdf',
        'content-disposition': 'attachment; filename=Question_Paper.pdf'}
    return valueOfData, 200, headers
