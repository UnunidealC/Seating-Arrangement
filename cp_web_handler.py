from flask import Flask, render_template, url_for, request, redirect
from SQLiteGenerator.SQLiteOOP import Class, Student, StudentRecords, Subject, SeatingArrangement, User, CurrentUser, SavedSeatArr, Comment, UserInfo, SubjectAbbrev, SubjectFull
from database_handler import execute_sql
import random
from datetime import date

app = Flask(__name__)

'''
#google signin
@app.route("/w")
def google_sign_in():
    return render_template("google_sign_in.html")


#Default Home Page: display user login page
@app.route("/")
def display_login():
    credentials = execute_sql("SELECT * FROM UserInfo")  # Read SQL
    #print(credentials)
    if request.method == 'POST':
        #if request.form['username'].strip() != '' and request.form['password'].strip() != '':
        for i in credentials:
            if request.form['username'] == i[0] and request.form['password'] == i[1]:
                #nonlocal current_user
                #current_user = request.form['username']
                #print(current_user)
                return redirect(url_for('display_all_student_records'))

        return render_template("login_page.html",credentials=credentials, error = "Invalid Username or Password, please try again.")

    return render_template("login_page.html",credentials=credentials, error = False)

@app.route("/create_account", methods=['GET','POST'])
def create_account():
    if request.method == 'POST':
        accounts = execute_sql("SELECT * FROM UserInfo") #Read SQL
        account_names = []
        for each_username in accounts:
            account_names.append(each_username[0])
        if request.form.get('username') in account_names:
            return render_template("create_account.html", error = "This username is taken!")
        elif request.form.get('username').strip() == "" or request.form.get('password').strip() == "":
            return render_template("create_account.html", error = "Username/Password should not be empty spaces.")
        else:
            new_account = UserInfo(None,None)
            new_account.set_username(request.form.get('username'))
            new_account.set_password(request.form.get('password'))
            execute_sql(new_account.create_new_account())
            #new_account_info = ClassInfo(request.form.get('username'),None,None)
            #execute_sql(new_account_info.create_new_info())
        return redirect(url_for("display_login"))
    else:
        return render_template("create_account.html", error = False)

@app.route("/Welcome!")
def login_success():
    nonlocal current_user
    user = execute_sql("SELECT * FROM UserInfo WHERE username = current_user")
    username, password = user
    user_info = UserInfo(username,password)
    #print(user)
    return render_template("login_success.html")
    '''


#display page
@app.route("/")
def display_all_student_records():
    classes = execute_sql("SELECT * FROM Class")
    students = execute_sql("SELECT * FROM Student")
    records = execute_sql("SELECT * FROM StudentRecords")
    subjects = execute_sql("SELECT * FROM Subject")

    for x in range(len(classes)-1): #to sort classes in order, so that when displayed will be according to class.
        smallest = x
        for y in range(x+1,len(classes)):
            if classes[y][0] < classes[smallest][0]:
                smallest = y
        if smallest != x:
            classes[smallest],classes[x] = classes[x],classes[smallest]

    for i in range(len(students)-1): #to sort reg.no in order, so that when displayed will be according to reg.no.
        smallest = i
        for j in range(i+1,len(students)):
            if students[j][1] < students[smallest][1]:
                smallest = j
        if smallest != i:
            students[smallest],students[i] = students[i],students[smallest]


    classes_oop = list(map(lambda a: Class(a[0],a[1]), classes))
    students_oop = list(map(lambda b: Student(b[0],b[1],b[2],b[3],b[4],b[5]), students ))
    records_oop = list(map(lambda c: StudentRecords(c[0],c[1],c[2]),records))
    subjects_oop = list(map(lambda d: Subject(d[0],d[1]), subjects ))

    # collating all grades and adding it as attribute to Students as AllSubjectGrades
    for student in students_oop:
        if student.get_AllSubjectGrades() == '':
            temp = ''
            index = 0
            while len(temp.split(' ')) - 1 != len(student.get_StudentSubjectCombi().split(' ')):
                for record in records:
                    if student.get_StudentName() == record[0] and student.get_StudentSubjectCombi().split(' ')[index] == record[2]:
                        temp += '{} '.format(record[1])
                index +=1
            temp = temp[:-1]
            student.set_AllSubjectGrades(temp)
            execute_sql(student.update_record())

    # Adding to WeakSubjects and StrongSubjects for seating arrangement
    # done in display so that after editing new strong subjects will be added and some removed as well
    # same for weak subjects
    for student in students_oop:
        student_seating_arrangement = execute_sql('SELECT * FROM SeatingArrangement WHERE StudentName = "{}"'.format(student.get_StudentName()))[0]
        StudentName, CannotSeatNextTo, SeatInFront, WeakSubjects, StrongSubjects, ClassLst, SeatByGrades, RowNo, ColumnNo = student_seating_arrangement
        student_seating_arrangement = SeatingArrangement(StudentName, CannotSeatNextTo, SeatInFront, WeakSubjects, StrongSubjects, ClassLst, SeatByGrades, RowNo, ColumnNo)
        StrongSubjects = ''
        WeakSubjects = ''
        for i in range(len(student.get_AllSubjectGrades().split(' '))):
            if student.get_AllSubjectGrades().split(' ')[i] < 'C': #'A', 'B'
                StrongSubjects += student.get_StudentSubjectCombi().split(' ')[i] + ' '
            elif student.get_AllSubjectGrades().split(' ')[i] > 'D':
                WeakSubjects += student.get_StudentSubjectCombi().split(' ')[i] + ' '
        student_seating_arrangement.set_StrongSubjects(StrongSubjects[:-1])
        student_seating_arrangement.set_WeakSubjects(WeakSubjects[:-1])
        execute_sql(student_seating_arrangement.update_record())

    reset_seating_arrangement()

    return render_template("display_all_records.html", classes = classes_oop, students = students_oop, records = records_oop, subjects = subjects_oop)

#edit records
@app.route("/edit_student_records/<string:student_name>", methods = ["GET","POST"])
def edit_student_record(student_name):
    student_details = execute_sql("SELECT * FROM Student WHERE StudentName = '{}'".format(student_name))[0]
    StudentName, StudentRegNo, ClassName, StudentSubjectCombi, StudentGender, AllSubjectGrades = student_details
    edit_student_details = Student(StudentName, StudentRegNo, ClassName, StudentSubjectCombi, StudentGender, AllSubjectGrades)

    #StudentName cannot be changed as its the Primary Key
    if request.method == 'POST':
        #Update Student Object
        edit_student_details.set_StudentRegNo(request.form.get('StudentRegNo').strip())
        edit_student_details.set_StudentGender(request.form.get('StudentGender').strip())

        new_StudentSubjectCombi = ''
        new_AllSubjectGrades = ''
        for i in range(len(StudentSubjectCombi.split(' '))):
            new_StudentSubjectCombi += request.form.get('SubjectName{}'.format(i).strip()) + ' '
            new_AllSubjectGrades += request.form.get('SubjectGrade{}'.format(i).strip()) + ' '
        new_StudentSubjectCombi = new_StudentSubjectCombi[:-1]
        new_AllSubjectGrades = new_AllSubjectGrades[:-1]

        edit_student_details.set_StudentSubjectCombi(new_StudentSubjectCombi)
        edit_student_details.set_AllSubjectGrades(new_AllSubjectGrades)

        # Update the database of Student
        execute_sql(edit_student_details.update_record())

        #Update StudentRecords object when change in grade
        index = 0
        if index < len(StudentSubjectCombi.split(' ')) and new_StudentSubjectCombi != StudentSubjectCombi:
            if new_StudentSubjectCombi.split(' ')[index] != StudentSubjectCombi.split(' ')[index]:
                student_subject = execute_sql("SELECT * FROM StudentRecords WHERE SubjectName = '{}'".format(StudentSubjectCombi.split(' ')[index]))[0]
                StudentName, SubjectGrade, SubjectName = student_subject
                edit_student_subject = StudentRecords(StudentName, SubjectGrade, SubjectName)
                edit_student_subject.set_SubjectName(new_StudentSubjectCombi.split(' ')[index])

                #Update the database of StudentRecords
                execute_sql(edit_student_subject.update_record())
            index += 1

        index = 0
        if index < len(AllSubjectGrades.split(' ')) and new_AllSubjectGrades != AllSubjectGrades:
            if new_AllSubjectGrades.split(' ')[index] != AllSubjectGrades.split(' ')[index]:
                student_grade = execute_sql("SELECT * FROM StudentRecords WHERE SubjectName = '{}'".format(StudentSubjectCombi.split(' ')[index]))[0]
                StudentName, SubjectGrade, SubjectName = student_grade
                edit_student_grade = StudentRecords(StudentName, SubjectGrade, SubjectName)
                edit_student_grade.set_SubjectName(new_AllSubjectGrades.split(' ')[index])
                #Update the database of StudentRecords
                execute_sql(edit_student_grade.update_record())
            index += 1

        #return to main page
        return redirect(url_for("display_all_student_records"))

    else:
        return render_template('edit_student_record.html', edit_student_details = edit_student_details, range = range(len(edit_student_details.get_AllSubjectGrades().split(' '))))

#delete student record
@app.route("/delete_student_record", methods = ['POST'])
def delete_student_record():
    student_name = request.form.get('delete')
    student_details = execute_sql("SELECT * FROM Student WHERE StudentName = '{}'".format(student_name))[0]
    StudentName, StudentRegNo, ClassName, StudentSubjectCombi, StudentGender, AllSubjectGrades = student_details
    delete_student_details = Student(StudentName, StudentRegNo, ClassName, StudentSubjectCombi, StudentGender, AllSubjectGrades)

    student_records = execute_sql("SELECT * FROM StudentRecords WHERE StudentName = '{}'".format(student_name))

    seating_arrangement_record = execute_sql("SELECT * FROM SeatingArrangement WHERE StudentName = '{}'".format(student_name))[0]
    StudentName, CannotSeatNextTo, SeatInFront, WeakSubjects, StrongSubjects, ClassLst, SeatByGrades, RowNo, ColumnNo = seating_arrangement_record
    delete_seating_arrangement_record = SeatingArrangement(StudentName, CannotSeatNextTo, SeatInFront, WeakSubjects, StrongSubjects, ClassLst, SeatByGrades, RowNo, ColumnNo)

    #Delete the database
    execute_sql(delete_student_details.delete_record())
    execute_sql(delete_seating_arrangement_record.delete_record())
    for i in range(len(student_records)):
        StudentName, SubjectGrade, SubjectName = student_records[i]
        delete_student_record = StudentRecords(StudentName, SubjectGrade, SubjectName)
        execute_sql(delete_student_record.delete_record())

    #remove class if the class no longer has any students in it
    students_from_class = execute_sql("SELECT * FROM Student WHERE ClassName == '{}'".format(ClassName))
    if students_from_class == []:
        class_details = execute_sql("SELECT * FROM Class WHERE ClassName == '{}'".format(ClassName))[0]
        ClassName, TotalStudents = class_details
        delete_class = Class(ClassName, TotalStudents)
        execute_sql(delete_class.delete_record())

    #Return to the main page
    return redirect(url_for("display_all_student_records"))


#TODO Adjust this function to make it be like the delete seating arrangement one (only window pops up asking user if want to delete)


#Define subject names to their description:
def subject_description(subject_name):
    def subject(name):
        if name == 'CM':
            return 'Chemistry'
        elif name == 'BI':
            return "Biology"
        elif name == 'PH':
            return 'Physics'
        elif name == 'CP':
            return 'Computing'
        elif name == 'MA':
            return 'Mathematics'
        elif name == 'EC':
            return 'Economics'
        elif name == 'HI':
            return 'History'
        elif name == 'GE':
            return 'Geography'
        elif name == 'GP':
            return 'General Paper'
        elif name == 'CSC':
            return 'China Studies in Chinese'
        elif name == 'CSE':
            return 'China Studies in English'
        elif name == 'CLL':
            return 'Chinese Language and Literature'
        elif name == 'LIT':
            return 'Literature in English'
        elif name == 'FM':
            return "Further Mathematics"
        elif name == 'TS':
            return 'Translation'
        else:
            return ''

    if '(' in subject_name:
        if '1' in subject_name:
            h = 'H1'
        if '3' in subject_name:
            h = 'H3'
    else:
        h = 'H2'

    name = subject(subject_name.strip().split('(')[0])

    if name == '':
        return ''
    else:
        return h + ' ' + name


#function to check if any character in a string is a digit
def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


#Create Student Record
@app.route("/create_student_record", methods = ['GET','POST'])
def create_student_record():

    if request.method == 'POST':
        error = False
        if request.form['ClassName'].strip() == "":
            error = "Invalid Class, Please write something for Class..."

        elif len(request.form['ClassName'].strip()) != 2:
            error = "Invalid Class, Class should consist of one number and one letter (e.g. 6M)"

        elif len(request.form['ClassName'].strip()) == 2:
            if not (request.form['ClassName'].strip()[0].isdigit() and request.form['ClassName'][1].strip().isalpha() and
                    ord(request.form['ClassName'][1].strip()) >= 65 and ord(request.form['ClassName'][1].strip()) <= 90 ):
                error = "Invalid Class, Class should consist of one number and one capital letter (e.g. 6M)"
                return render_template('create_student_record.html', SubjectAbbrev=SubjectAbbrev,
                                    SubjectFull=SubjectFull, error=error)

        existing_students = execute_sql("SELECT * FROM Student WHERE ClassName = '{}'".format(request.form['ClassName'].strip()))
        existing_regno = list(map(lambda tuple: tuple[1], existing_students))

        if request.form['StudentName'].strip() == "":
            error = "Invalid Name, Please write something for Name..."
            return render_template('create_student_record.html', SubjectAbbrev=SubjectAbbrev,
                                    SubjectFull=SubjectFull, error=error)

        elif hasNumbers(request.form['StudentName']):
            error = "Invalid Name, Name should not contain numbers"
            return render_template('create_student_record.html', SubjectAbbrev=SubjectAbbrev,
                                    SubjectFull=SubjectFull, error=error)

        elif request.form['StudentRegNo'].strip() == "":
            error = "Invalid Register No., Please write something for Register No..."
            return render_template('create_student_record.html', SubjectAbbrev=SubjectAbbrev,
                                    SubjectFull=SubjectFull, error=error)

        elif not request.form['StudentRegNo'].strip().isdigit():
            error = "Invalid Register No., Register No. should only consist of numbers"
            return render_template('create_student_record.html', SubjectAbbrev=SubjectAbbrev,
                                    SubjectFull=SubjectFull, error=error)

        if request.form['StudentRegNo'].strip().isdigit():
            if int(request.form['StudentRegNo'].strip()) in existing_regno:
                error = "Register No. has already been used, please key in another register no."
                return render_template('create_student_record.html', SubjectAbbrev=SubjectAbbrev,
                                    SubjectFull=SubjectFull, error=error)

        if request.form['StudentGender'].strip() == "":
            error = "Invalid Gender, Please write something for Gender..."

        elif request.form['StudentGender'].strip() not in ["F","M"]:
            error = "Invalid Gender, Gender should only be M or F"

        elif request.form['StudentSubjectCombi'].strip() == "":
            error = "Invalid Subject Combination, Please write something for Subject Combination..."

        for SubCom in list(request.form['StudentSubjectCombi'].split(' ')):
            if SubCom[:3:] not in SubjectAbbrev:
                error = 'Invalid Subject Combination, An impossible subject was entered'

        for SubGrade in (list(filter(lambda x: x != ' ', request.form['AllSubjectGrades'].strip()))):
            if SubGrade not in ['A', 'B', 'C', 'D', 'E', 'S', 'U']:
                print(SubGrade, 'Subgrade')
                error = 'Invalid Grades, An impossible grade was entered'

        if request.form['AllSubjectGrades'].strip() == "":
            error = "Invalid Grades, Please write something for Grades..."

        elif len(request.form['StudentSubjectCombi'].strip().split(" ")) != len(request.form['AllSubjectGrades'].strip().split(" ")):
            error = "Number of grades should correspond to number of subjects keyed in"

        if error != False:
            return render_template('create_student_record.html', SubjectAbbrev=SubjectAbbrev,
                                    SubjectFull=SubjectFull, error=error)

        #Create Class object
        new_class = Class(request.form.get('ClassName').strip(),'')
        execute_sql(new_class.create_new_record())

        #Create Student object
        new_student_details = Student(request.form.get('StudentName').strip(), request.form.get('StudentRegNo').strip(), request.form.get('ClassName').strip(),request.form.get('StudentSubjectCombi').strip(), request.form.get('StudentGender').strip(), request.form.get('AllSubjectGrades').strip())
        execute_sql(new_student_details.create_new_record())

        #Create StudentRecords object
        StudentSubjectCombi = request.form.get('StudentSubjectCombi').strip().split(' ')
        AllSubjectGrades = request.form.get('AllSubjectGrades').strip().split(' ')
        for i in range(len(StudentSubjectCombi)):
            new_student_record = StudentRecords(request.form.get('StudentName').strip(), AllSubjectGrades[i], StudentSubjectCombi[i])
            execute_sql(new_student_record.create_new_record())

        subject_lst = execute_sql('SELECT * FROM Subject')
        subject_lst = list(map(lambda tuple: tuple[0],subject_lst))
        for subject in StudentSubjectCombi:
            if subject not in subject_lst:
                new_subject = Subject(subject, subject_description(subject))
                execute_sql(new_subject.create_new_record())

        #Create Seating Arrangement object
        new_seating_arrangement = SeatingArrangement(request.form.get('StudentName').strip(), CannotSeatNextTo = '', SeatInFront = False, WeakSubjects = '', StrongSubjects = '', ClassLst= '', SeatByGrades='', RowNo=0, ColumnNo=0)
        execute_sql(new_seating_arrangement.create_new_record())

        return redirect(url_for('display_all_student_records'))

    else:
        return render_template('create_student_record.html', SubjectAbbrev=SubjectAbbrev,
           SubjectFull=SubjectFull)

@app.route("/set_seating_arrangement")
def set_seating_arrangement():
    reset_seating_arrangement()
    return render_template('set_seating_arrangement.html')

@app.route("/class_seating_arrangement", methods = ['GET', 'POST'])
def class_seating_arrangement():
    valid_classes = execute_sql("SELECT * FROM Class")
    valid_classes = list(map(lambda x: x[0], valid_classes))

    if request.method == 'POST':
        ClassName = request.form.get('ClassName')
        return ClassName
    else:
        return render_template('class_seating_arrangement.html', valid_classes=valid_classes)

@app.route("/special_class_seating_arrangement", methods = ['GET', 'POST'])
def special_class_seating_arrangement():
    valid_classes = execute_sql("SELECT * FROM Class")
    valid_classes = list(map(lambda x: x[0], valid_classes))
    valid_subjects = execute_sql("SELECT * FROM Subject")
    valid_subjects = list(map(lambda x: x[0], valid_subjects))

    if request.method == 'POST':
        subject_taken = request.form.get('SubjectName')
        classes = ''
        for i in range(len(valid_classes)):
            ClassName = request.form.get('ClassName{}'.format(i))
            if ClassName != None:
                classes += ClassName + ' '
        classes = classes[:-1]
        return classes,subject_taken

    else:
        return render_template('special_class_seating_arrangement.html', valid_classes = valid_classes, class_range = range(len(valid_classes)), valid_subjects = valid_subjects)


@app.route("/set_student_details", methods=['GET', 'POST'])
def set_student_details():
    Subject = None
    lst = []

    if class_seating_arrangement() != None:
        ClassName = class_seating_arrangement()
        print(ClassName)
        lst = execute_sql("SELECT * FROM Student WHERE ClassName = '{}'".format(ClassName))
        lst = list(map(lambda x : x[0], lst)) #lst with all names of valid students
        print(lst)

    if special_class_seating_arrangement()[1] != None:
        ClassList, Subject = special_class_seating_arrangement()
        ClassList = ClassList.split(' ')
        lst = []
        for i in ClassList:
            temp = execute_sql("SELECT * FROM Student WHERE ClassName = '{}'".format(i))
            for student in temp:
                if Subject in student[3].split(' '):
                    lst.append(student)
        lst = list(map(lambda x : x[0], lst))

    if lst != []:
        string = ''
        for i in lst:
            string += i + ','
        string = string[:-1]

        for i in lst:
            #To identify, whether students belong to class which seating arrangement is generated for
            #set._ClassLst to lst for students in that class and set the rest of the students' ClassLst to default = []

            #set._ClassLst to lst for students in this class
            temp = execute_sql("SELECT * FROM SeatingArrangement WHERE StudentName = '{}'".format(i))[0]
            StudentName, CannotSeatNextTo, SeatInFront, WeakSubjects, StrongSubjects, ClassLst, SeatByGrades, RowNo, ColumnNo = temp
            new_classlst = SeatingArrangement(StudentName, CannotSeatNextTo, SeatInFront, WeakSubjects, StrongSubjects, ClassLst, SeatByGrades, RowNo, ColumnNo)
            new_classlst.set_ClassLst(string)
            execute_sql(new_classlst.update_record())

        #setting rest to default ClassLst = []
        student_lst = execute_sql("SELECT * FROM SeatingArrangement WHERE ClassLst != '{}'".format(string))
        print(student_lst)
        student_lst = list(map(lambda x: x[0], student_lst))
        for i in student_lst:
            temp = execute_sql("SELECT * FROM SeatingArrangement WHERE StudentName = '{}'".format(i))[0]
            StudentName, CannotSeatNextTo, SeatInFront, WeakSubjects, StrongSubjects, ClassLst,  SeatByGrades, RowNo, ColumnNo = temp
            new_classlst = SeatingArrangement(StudentName, CannotSeatNextTo, SeatInFront, WeakSubjects,StrongSubjects, ClassLst, SeatByGrades, RowNo, ColumnNo)
            new_classlst.set_ClassLst('')
            execute_sql(new_classlst.update_record())

        return render_template('set_student_details.html', Students=lst, student_range=range(len(lst)), range=range(5),Subject=Subject)

    if request.method == 'POST':
        seatbygrades = request.form.get('SeatByGrades')  # strong pupils will seat next to weak pupils
        rowno = request.form.get('RowNo')
        columnno = request.form.get('ColumnNo')
        print('set_student_details', seatbygrades, rowno, columnno)

        lst = execute_sql("SELECT * FROM SeatingArrangement WHERE ClassLst != ''")
        for student in lst:
            StudentName, CannotSeatNextTo, SeatInFront, WeakSubjects, StrongSubjects, ClassLst, SeatByGrades, RowNo, ColumnNo = student
            student = SeatingArrangement(StudentName, CannotSeatNextTo, SeatInFront, WeakSubjects, StrongSubjects, ClassLst, SeatByGrades, RowNo, ColumnNo)
            if seatbygrades == 'Yes':
                student.set_SeatByGrades(seatbygrades)
            if rowno != 0:
                student.set_RowNo(rowno)
                student.set_ColumnNo(columnno)
            execute_sql(student.update_record())

        lst = list(map(lambda x : x[0], lst)) #To get valid names

        for i in range(len(lst)):
            StudentName = lst[i]
            SeatInFront = request.form.get('SeatInFront{}'.format(i))
            if SeatInFront != None:
                student = execute_sql('SELECT * FROM SeatingArrangement WHERE StudentName = "{}"'.format(StudentName))[0]
                StudentName, CannotSeatNextTo, SeatInFront, WeakSubjects, StrongSubjects, ClassLst, SeatByGrades, RowNo, ColumnNo = student
                set_student = SeatingArrangement(StudentName, CannotSeatNextTo, SeatInFront, WeakSubjects, StrongSubjects, ClassLst, SeatByGrades, RowNo, ColumnNo)
                set_student.set_SeatInFront(True)
                execute_sql(set_student.update_record())

            StudentName1 = request.form.get('StudentName1{}'.format(i))
            StudentName2 = request.form.get('StudentName2{}'.format(i))

            if StudentName1 != '' and StudentName1 != None:
                print(StudentName1)
                print(execute_sql('SELECT * FROM SeatingArrangement WHERE StudentName = "{}"'.format(StudentName1)))
                student1 = execute_sql('SELECT * FROM SeatingArrangement WHERE StudentName = "{}"'.format(StudentName1))[0]
                StudentName, CannotSeatNextTo, SeatInFront, WeakSubjects, StrongSubjects, ClassLst, SeatByGrades, RowNo, ColumnNo = student1
                set_student = SeatingArrangement(StudentName, CannotSeatNextTo, SeatInFront, WeakSubjects,StrongSubjects, ClassLst, SeatByGrades, RowNo, ColumnNo)
                set_student.set_CannotSeatNextTo(StudentName2)
                execute_sql(set_student.update_record())

                student2 = execute_sql('SELECT * FROM SeatingArrangement WHERE StudentName = "{}"'.format(StudentName2))[0]
                StudentName, CannotSeatNextTo, SeatInFront, WeakSubjects, StrongSubjects, ClassLst, SeatByGrades, RowNo, ColumnNo = student2
                set_student = SeatingArrangement(StudentName, CannotSeatNextTo, SeatInFront, WeakSubjects, StrongSubjects, ClassLst, SeatByGrades,RowNo, ColumnNo)
                set_student.set_CannotSeatNextTo(StudentName1)
                execute_sql(set_student.update_record())


    else:
        return render_template('set_student_details.html', Students = lst, student_range = range(len(lst)), range = range(5), Subject = Subject)
def sort_by_grades(student_lst):
    #best scenario: Student A can help Student B and vice versa
    #strong and weak subjects of one must be opposite of the other student

    def mutual_benefit(weak, weak1, strong, strong1):
        #subject in weak must appear in strong1 and subject in strong must appear in weak1
        student1_benefit, student2_benefit = False, False

        for subject in weak:
            if subject in strong1:
                student1_benefit = True

        for subject in strong:
            if subject in weak1:
                student2_benefit = True

        if student1_benefit == True and student2_benefit == True:
            return True
        else:
            return False

    def only_one_benefit(weak, weak1, strong, strong1):
        student1_benefit, student2_benefit = False, False

        for subject in weak:
            if subject in strong1:
                student1_benefit = True

        for subject in strong:
            if subject in weak1:
                student2_benefit = True

        if student1_benefit == True or student2_benefit == True:
            return True
        else:
            return False

    grade_lst = []
    temp = []

    for i in range(len(student_lst)):
        Weak = student_lst[i][3].split(' ')
        Strong = student_lst[i][4].split(' ')

        for j in range(i+1, len(student_lst)):
            Weak1 = student_lst[j][3].split(' ')
            Strong1 = student_lst[j][4].split(' ')

            if mutual_benefit(Weak, Weak1, Strong, Strong1) == True:
                temp.append([student_lst[i],student_lst[j],'A']) #'A' will signify that it is the optimum pair
            elif only_one_benefit(Weak, Weak1, Strong, Strong1) == True and temp == [] :
                temp.append([student_lst[i], student_lst[j]])

        temp1 = list(filter(lambda x: 'A' in x, grade_lst))
        if temp1 == []: #if no optimum scenario for this student then it is okay to have pairs where only one can benefit
            grade_lst.extend(temp)
        else: #otherwise should only have optimum scenario for that student
            list(map(lambda x:x.remove(x[2]),temp1))
            grade_lst.extend(temp1)

        temp = []
    return grade_lst


#TODO Adjust whiteboard length accordingly
@app.route("/generate_seating_arrangement", methods=['GET', 'POST'])
def generate_seating_arrangement():
    SeatInFront_lst = []
    not_SeatInFront_lst = [] #for students who do not need to seat in front, separate lst to randomly shuffle these students and then append it to SeatingArrangement_lst
    CannotSeatNextTo_lst = []
    SeatingArrangement_lst = []
    result = []

    student_lst = execute_sql("SELECT * FROM SeatingArrangement WHERE ClassLst != ''")
    StudentName_lst = list(map(lambda x:x[0], student_lst))
    ClassSize = len(StudentName_lst)

    StudentName, CannotSeatNextTo, SeatInFront, WeakSubjects, StrongSubjects, ClassLst, SeatByGrades, RowNo, ColumnNo = student_lst[0]
    if RowNo == 0:
        set_student_details()

    student_lst = execute_sql("SELECT * FROM SeatingArrangement WHERE ClassLst != ''")
    StudentName, CannotSeatNextTo, SeatInFront, WeakSubjects, StrongSubjects, ClassLst, SeatByGrades, RowNo, ColumnNo = student_lst[0]

    for student in student_lst:
        StudentName, CannotSeatNextTo, SeatInFront, WeakSubjects, StrongSubjects, ClassLst, SeatByGrades, RowNo, ColumnNo = student
        student = SeatingArrangement(StudentName, CannotSeatNextTo, SeatInFront, WeakSubjects, StrongSubjects, ClassLst, SeatByGrades, RowNo, ColumnNo)
        if student.get_CannotSeatNextTo() != '' and [student.get_StudentName(),student.get_CannotSeatNextTo()][::-1] not in SeatInFront_lst: #Assuming only one person cannot seat to that student
            CannotSeatNextTo_lst.append([student.get_StudentName(),student.get_CannotSeatNextTo()])
        if student.get_SeatInFront() == True:
            SeatInFront_lst.append(student.get_StudentName())


    if SeatByGrades == 'Yes':
        grade_lst = sort_by_grades(student_lst)
        #find pairs in cannotseatnextto_lst  that are also in grade_lst as those pairs can't seat next to each other
        for i in grade_lst:
            if i in CannotSeatNextTo_lst:
                grade_lst.remove(i)
            if i[::-1] in CannotSeatNextTo_lst:
                grade_lst.remove(i[::-1])

        #find pairs in grade_lst that are also in SeatInFrontLst to arrange the pairs in the front by appending confirmed pairs into SeatingArrangement_lst
        for a in range(len(SeatInFront_lst)):
            for b in range(a+1, len(SeatInFront_lst)):
                temp = [SeatInFront_lst[a], SeatInFront_lst[b]]
                if temp in grade_lst and temp[0] in StudentName_lst and temp[1] in StudentName_lst:
                    grade_lst.remove(temp)
                    SeatingArrangement_lst.append(temp) #added into confirmed seating arrangement
                    StudentName_lst.remove(temp[0])
                    StudentName_lst.remove(temp[1])

                if temp[::-1] in grade_lst and temp[0] in StudentName_lst and temp[1] in StudentName_lst:
                    grade_lst.remove(temp)
                    SeatingArrangement_lst.append(temp[::-1]) #added into confirmed seating arrangement
                    StudentName_lst.remove(temp[0])
                    StudentName_lst.remove(temp[1])

        # shuffle lst so that there will be more varieties of seating arrangement
        random.shuffle(CannotSeatNextTo_lst)
        random.shuffle(SeatInFront_lst)
        random.shuffle(grade_lst)

        # pair up those who are suppose to seat in front, seating in front prioritised to seating with those that can help with grades
        for s in range(len(SeatInFront_lst)):
            for r in range(s+1, len(SeatInFront_lst)):
                temp = [SeatInFront_lst[s], SeatInFront_lst[r]]
                if temp[0] in StudentName_lst and temp[1] in StudentName_lst:
                    SeatingArrangement_lst.append(temp)
                    StudentName_lst.remove(temp[0])
                    StudentName_lst.remove(temp[1])

        # all students supposed to seat in front are added
        random.shuffle(SeatingArrangement_lst)  # so that pairs in grade_lst won't always be in front

        # choose pairs from grade_lst
        for c in grade_lst:
            if c[0] in StudentName_lst and c[1] in StudentName_lst:
                not_SeatInFront_lst.append(c)
                StudentName_lst.remove(c[0])
                StudentName_lst.remove(c[1])


    else:
        # shuffle lst so that there will be more varieties of seating arrangement
        random.shuffle(CannotSeatNextTo_lst)
        random.shuffle(SeatInFront_lst)

        # pair up those who are suppose to seat in front
        for s in range(len(SeatInFront_lst)):
            for r in range(s + 1, len(SeatInFront_lst)):
                temp = [SeatInFront_lst[s], SeatInFront_lst[r]]
                if temp[0] in StudentName_lst and temp[1] in StudentName_lst:
                    SeatingArrangement_lst.append(temp)
                    StudentName_lst.remove(temp[0])
                    StudentName_lst.remove(temp[1])

    # pairing up any remaining students
    random.shuffle(StudentName_lst)
    while len(StudentName_lst) > 1:  # possible to have 1 student left if no pair for that student
        temp = [StudentName_lst[0], StudentName_lst[1]]
        if temp not in CannotSeatNextTo_lst and temp[::-1] not in CannotSeatNextTo_lst: #cannot be paired up if not suppose to seat next to each other
            not_SeatInFront_lst.append(temp)
            StudentName_lst.remove(temp[0])
            StudentName_lst.remove(temp[1])

    random.shuffle(not_SeatInFront_lst)
    SeatingArrangement_lst.extend(not_SeatInFront_lst)
    if StudentName_lst != []:
        SeatingArrangement_lst.append([StudentName_lst[0]])

    count = 0
    temp = []

    for row in range(RowNo):
        for column in range(ColumnNo):
            if count < ClassSize:
                temp.append(SeatingArrangement_lst[row*ColumnNo + column])
                if len(SeatingArrangement_lst[row*ColumnNo + column] ) == 2:
                    count += 2
                if len(SeatingArrangement_lst[row*ColumnNo + column]) == 1:
                    count += 1
        result.append(temp)
        temp = []

    return render_template('generate_seating_arrangement.html', SeatingArrangement_lst = result, RowNo = RowNo, ColumnNo = ColumnNo, RowNoRange = range(RowNo), ColumnNoRange = range(ColumnNo), ClassSize = ClassSize)

@app.route("/generate_seating_arrangement_again")
def generate_seating_arrangement_again():
    return generate_seating_arrangement()

def reset_seating_arrangement():
    #reset seating arrangement object when go back to display, and various setting menus (set_seating_arrangement, class_seating_arrangement, special_class_seating_arrangement)
    student_lst = execute_sql("SELECT * FROM SeatingArrangement WHERE ClassLst != ''")
    for student in student_lst:
        StudentName, CannotSeatNextTo, SeatInFront, WeakSubjects, StrongSubjects, ClassLst, SeatByGrades, RowNo, ColumnNo = student
        student = SeatingArrangement(StudentName, CannotSeatNextTo, SeatInFront, WeakSubjects, StrongSubjects, ClassLst, SeatByGrades, RowNo, ColumnNo)
        student.set_CannotSeatNextTo('')
        student.set_SeatInFront(False)
        student.set_ClassLst('')
        student.set_SeatByGrades('')
        student.set_RowNo(0)
        student.set_ColumnNo(0)
        execute_sql(student.update_record())

def show_current_seating_arrangement(seatarrseq, RowNo, ColumnNo):
    ClassSize = len(seatarrseq.split(','))
    seatarrseq = seatarrseq.split(',')
    SeatingArrangement_lst = []
    pair = []
    for i in seatarrseq:
        i = i.replace("'",'"').strip('"[]"')
        index = 0
        for x in i:
            if x.isalpha():
                break
            else:
                index += 1
        i = i[index:]
        pair.append(i)

        if len(pair) == 2:
            SeatingArrangement_lst.append(pair)
            pair = []
    if len(pair) == 1:
        SeatingArrangement_lst.append(pair)


    count = 0
    temp, result = [],[]

    for row in range(RowNo):
        for column in range(ColumnNo):
            if count < ClassSize:
                temp.append(SeatingArrangement_lst[row * ColumnNo + column])
                if len(SeatingArrangement_lst[row * ColumnNo + column]) == 2:
                    count += 2
                if len(SeatingArrangement_lst[row * ColumnNo + column]) == 1:
                    count += 1
        result.append(temp)
        temp = []
    return render_template('generate_seating_arrangement.html', SeatingArrangement_lst = result, RowNo = RowNo, ColumnNo = ColumnNo, RowNoRange = range(RowNo), ColumnNoRange = range(ColumnNo), ClassSize = ClassSize)

@app.route("/save_seatarr", methods = ['POST'])
def save_seatarr():
    seatarrname = request.form.get('savedname')
    seatarrseq = request.form.get('SeatingArrangement_lst')
    RowNo = int(request.form.get('RowNo'))
    ColumnNo = int(request.form.get('ColumnNo'))

    if seatarrname != '':
        currentuser = execute_sql('SELECT * FROM CurrentUser')[0][0]
        save = SavedSeatArr(currentuser, seatarrname, seatarrseq.replace("'", '"'), RowNo, ColumnNo)
        execute_sql(save.create_new_record())
    return show_current_seating_arrangement(seatarrseq, RowNo, ColumnNo)

@app.route("/show_saved_seatingarr", methods = ['GET', 'POST'])
def show_saved_seatingarr():
    username = execute_sql('SELECT * FROM CurrentUser')[0][0]
    username_details = execute_sql("SELECT * FROM SavedSeatArr WHERE UserName == '{}'".format(username))
    seatarrname_lst = list(map(lambda x: x[1], username_details))
    return render_template('show_saved_seatingarr.html', seatarrname_lst = seatarrname_lst)

@app.route("/edit_saved_seatingarr", methods = ['POST'])
def edit_saved_seatingarr(): #only can rename
    newname = request.form.get('newname')
    replace = True
    if len(newname.split(',')) == 2:
        newname, seatarrname = newname.split(',')
        replace = False
    else:
        newname, seatarrname, replace = newname.split(',')
        replace = True

    username = execute_sql('SELECT * FROM CurrentUser')[0][0]
    if replace == True: #will have to delete all the comments and seating arrangement of the one that will be replaced
        replace_seatarrs = execute_sql("SELECT * FROM SavedSeatArr WHERE UserName == '{}' AND SeatArrName == '{}'".format(username, newname))[0]
        UserName, SeatArrName, SeatArrSeq, RowNo, ColumnNo, CommentIDs = replace_seatarrs
        replace_seatarr = SavedSeatArr(UserName, SeatArrName, SeatArrSeq, RowNo, ColumnNo, CommentIDs)
        #delete SavedSeatArr obj
        execute_sql(replace_seatarr.delete_record())
        #delete_SavedSeatArr_obj
        for commentid in CommentIDs.split(','):
            replace_comments = execute_sql("SELECT * FROM Comment WHERE CommentID == '{}'".format(commentid))[0]
            SeatArrName, CommentID, CommentText, CommentDatetime, UserName = replace_comments
            replace_comment = Comment(SeatArrName, CommentID, CommentText, CommentDatetime, UserName)
            execute_sql(replace_comment.delete_record())

    seatarr_details = execute_sql("SELECT * FROM SavedSeatArr WHERE UserName == '{}' AND SeatArrName == '{}'".format(username, seatarrname))[0]
    #print(seatarr_details)
    UserName, SeatArrName , SeatArrSeq, RowNo, ColumnNo, CommentIDs = seatarr_details
    seatarr = SavedSeatArr(UserName,SeatArrName, SeatArrSeq, RowNo, ColumnNo, CommentIDs)
    seatarr.set_SeatArrName(newname)
    #Update SavedSeatArr
    execute_sql('''UPDATE SavedSeatArr SET\nUserName = '{}', SeatArrName = "{}", SeatArrSeq = '{}', RowNo = '{}', ColumnNo = '{}', CommentIDs = '{}'\nWHERE \nUserName = '{}' and SeatArrName = "{}"'''.format(UserName, newname, SeatArrSeq, RowNo, ColumnNo, CommentIDs, UserName, seatarrname))

    #Update Comment
    if CommentIDs != '':
        for commentid in CommentIDs.split(','):
            print(execute_sql('SELECT * FROM Comment WHERE CommentID = "{}"'.format(commentid)))
            comment_details = execute_sql('SELECT * FROM Comment WHERE CommentID = "{}"'.format(commentid))[0]
            SeatArrName, CommentID, CommentText, CommentDatetime, UserName = comment_details
            comment = Comment(SeatArrName, CommentID, CommentText, CommentDatetime, UserName)
            comment.set_SeatArrName(newname)
            execute_sql(comment.update_record())

    return show_saved_seatingarr()

@app.route("/delete_saved_seatingarr", methods=['POST'])
def delete_saved_seatingarr():
    delete = request.form.get('delete')
    print('delete', delete)
    seatarrname = delete
    username = execute_sql('SELECT * FROM CurrentUser')[0][0]
    seatarr_details = execute_sql("SELECT * FROM SavedSeatArr WHERE UserName == '{}' AND SeatArrName == '{}'".format(username, seatarrname))[0]
    UserName, SeatArrName , SeatArrSeq, RowNo, ColumnNo, CommentIDs = seatarr_details
    seatarr = SavedSeatArr(UserName,SeatArrName, SeatArrSeq, RowNo, ColumnNo, CommentIDs)

    #Delete SavedSeatArr object
    execute_sql(seatarr.delete_record())

    #Delete Comments linked to the SavedSeatArr
    if CommentIDs != '':
        for commentid in CommentIDs.split(','):
            comment_details = execute_sql('SELECT * FROM Comment WHERE CommentID = "{}"'.format(commentid))[0]
            SeatArrName, CommentID, CommentText, CommentDatetime, UserName = comment_details
            comment = Comment(SeatArrName, CommentID, CommentText, CommentDatetime, UserName)
            execute_sql(comment.delete_record())

    return show_saved_seatingarr()

@app.route("/show_seatarr_by_name/<string:seatarrname>")
def show_seatarr_by_name(seatarrname):
    seatarr = execute_sql("SELECT * FROM SavedSeatArr WHERE SeatArrName = '{}'".format(seatarrname))[0]
    #print(seatarr)
    UserName, SeatArrName, SeatArrSeq, RowNo, ColumnNo, CommentIDs = seatarr
    seatarr_oop = SavedSeatArr(UserName, SeatArrName, SeatArrSeq, RowNo, ColumnNo)
    ClassSize = len(SeatArrSeq.split(","))
    comments = execute_sql("SELECT * FROM Comment WHERE SeatArrName = '{}'".format(seatarrname))  # SQL ReadF
    # print(comments)
    comments_oop = list(map(lambda t: Comment(t[0], t[1], t[2], t[3], t[4]), comments))
    # print(comments_oop)
    # process to find SeatingArrangement_lst
    #print(SeatArrSeq)
    seatarrseq = SeatArrSeq.split(',')
    SeatingArrangement_lst = []
    pair = []
    for i in seatarrseq:
        i = i.replace("'", '"').strip('"[]"')
        index = 0
        for x in i:
            if x.isalpha():
                break
            else:
                index += 1
        i = i[index:]
        pair.append(i)
        if len(pair) == 2:
            SeatingArrangement_lst.append(pair)
            pair = []
    if len(pair) == 1:
        SeatingArrangement_lst.append(pair)

    #print("SeatingArrangement_lst",SeatingArrangement_lst)

    count = 0
    temp, result = [], []

    for row in range(RowNo):
        for column in range(ColumnNo):
            if count < ClassSize:
                temp.append(SeatingArrangement_lst[row * ColumnNo + column])
                if len(SeatingArrangement_lst[row * ColumnNo + column]) == 2:
                    count += 2
                if len(SeatingArrangement_lst[row * ColumnNo + column]) == 1:
                    count += 1
        result.append(temp)
        temp = []

    return render_template("show_seatarr_by_name.html", seatarrname=seatarrname, comments=comments_oop, SeatingArrangement_lst = result, RowNoRange = range(RowNo), ColumnNoRange = range(ColumnNo), ColumnNo = ColumnNo, ClassSize = ClassSize)


# create comment
@app.route("/create_comment/<string:seatarrname>", methods = ['GET', 'POST'])
def create_comment(seatarrname):
    if request.method == 'POST':
        error = False
        if request.form['UserName'].isspace() or request.form['UserName'] == "":
            error = "Invalid UserName, Please write something for UserName..."

        elif request.form['CommentText'].isspace() or request.form['CommentText'] == "":
            error = "Invalid Comment Text, Please write something for Comment Text..."

        if error != False:
            return render_template("create_comment.html", seatarrname = seatarrname, new_CommentID = request.form['CommentID'],
                                   today = request.form['CommentDatetime'], error = error)

        new_comment = Comment(seatarrname,
                        request.form['CommentID'],
                        request.form['CommentText'],
                        request.form['CommentDatetime'],
                        request.form['UserName'])
        execute_sql(new_comment.create_new_record())

        UserName, SeatArrName, SeatArrSeq, RowNo, ColumnNo, CommentIDs = execute_sql("SELECT * FROM SavedSeatArr WHERE SeatArrName = '{}'".format(seatarrname))[0]
        edit_ssr = SavedSeatArr(UserName, SeatArrName, SeatArrSeq, RowNo, ColumnNo, CommentIDs)
        edit_ssr.set_CommentIDs(request.form['CommentID'])
        execute_sql(edit_ssr.update_record())

        return redirect(url_for("show_seatarr_by_name", seatarrname = seatarrname))
    else:
        # GET
        CommentID = execute_sql("SELECT Max(CommentID) FROM Comment")[0][0]
        new_CommentID = "{:0>6}".format(int(CommentID) + 1)
        today = "{:%Y-%m-%d}".format(date.today())

        return render_template("create_comment.html", seatarrname = seatarrname, new_CommentID = new_CommentID, today = today)

# edit comment
#TODO edit such that a window pops up and asks for new comment text (ref edit seatarr)
@app.route("/edit_comment", methods=['POST'])
def edit_comment():
    error = False
    if request.form['CommentText'].isspace() or request.form['CommentText'] == "":
        error = "Invalid Comment Text, Please write something for Comment Text..."

    comment_id = request.form['CommentID']
    comment = execute_sql('SELECT * FROM Comment WHERE CommentID = "{}"'.format(comment_id))[0]
    SeatArrName, CommentID, CommentText, CommentDatetime, UserName = comment
    edit_comment = Comment(SeatArrName, CommentID, CommentText, CommentDatetime, UserName)

    if error == False:
        # Update Comment Object
        edit_comment.set_CommentText(request.form['CommentText'])

        # Update the database
        execute_sql(edit_comment.update_record())

    # Return to mainpage
    print(error)
    return redirect(url_for("show_seatarr_by_name", error = error, seatarrname=SeatArrName))



# delete comment
#TODO edit such that function only popsup a window asking user if want to delete (ref delete seatarr)
@app.route("/delete_comment", methods=['POST'])
def delete_comment():
    comment_id = request.form.get('delete')
    comment = execute_sql("SELECT * FROM Comment WHERE CommentID = '{}'".format(comment_id))[0]
    #print(comment)
    SeatArrName, CommentID, CommentText, CommentDatetime, UserName = comment
    delete_comment = Comment(SeatArrName, CommentID, CommentText, CommentDatetime, UserName)

    # Update DB
    execute_sql(delete_comment.delete_record())

    UserName, SeatArrName, SeatArrSeq, RowNo, ColumnNo, CommentIDs = execute_sql("SELECT * FROM SavedSeatArr WHERE SeatArrName = '{}'".format(SeatArrName))[0]
    edit_ssr = SavedSeatArr(UserName, SeatArrName, SeatArrSeq, RowNo, ColumnNo, CommentIDs)
    edit_ssr.delete_CommentIDs(comment_id)
    execute_sql(edit_ssr.update_record())

    # Return to mainpage
    return redirect(url_for("show_seatarr_by_name", seatarrname = SeatArrName))


@app.route("/show_saved_seatingarr/search_filter")
def search_filter():
    seatarr = execute_sql('SELECT * FROM SavedSeatArr')  # SQL Read
    # print(seatarr)
    seatarr_oop = list(map(lambda t: SavedSeatArr(t[0], t[1], t[2], t[3], t[4], t[5]), seatarr))
    # print(seatarr_oop)
    return render_template("search_filter.html", seatarr=seatarr_oop)


#TODO Adjust all html pages' UI
#TODO Validation for create student record


# run app
if __name__ == "__main__":
    app.debug = True
    app.run()
