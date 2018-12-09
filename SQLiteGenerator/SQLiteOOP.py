class Class(object):
    """SQLite OOP class Class"""

    # initializer for classClass
    def __init__(self, ClassName, TotalStudents):
        self._ClassName = ClassName
        self._TotalStudents = TotalStudents

    # Mutator Functions
    def set_ClassName(self, new_ClassName):
        self._ClassName = new_ClassName

    def set_TotalStudents(self, new_TotalStudents):
        self._TotalStudents = new_TotalStudents

    # Accessor Functions
    def get_ClassName(self):
        return self._ClassName

    def get_TotalStudents(self):
        return self._TotalStudents

    # String Representation of Class Class
    def __str__(self):
        result = ""

        return result

    # SQLite: Create Table of Class Class
    @staticmethod
    def create_table():
        result = ""
        result += "CREATE TABLE Class(\n"
        result += "ClassName TEXT NOT NULL,\n"
        result += "TotalStudents INTEGER NOT NULL,\n"
        result += "PRIMARY KEY(ClassName)\n"
        result += ")\n"
        return result

    # SQLite: Create new record
    def create_new_record(self):
        result = ""
        result += "INSERT INTO Class\n"
        result += "(ClassName, TotalStudents)\n"
        result += "VALUES\n"
        result += "('{self._ClassName}', '{self._TotalStudents}')\n".format(self=self)
        return result

    # SQLite: Update record based on primary key
    def update_record(self):
        result = ""
        result += "UPDATE Class SET\n"
        result += "ClassName = '{self._ClassName}', TotalStudents = '{self._TotalStudents}'\n".format(self=self)
        result += "WHERE\n"
        result += "ClassName = '{self._ClassName}'\n".format(self=self)
        return result

    # SQLite: Delete record based on primary key
    def delete_record(self):
        result = ""
        result += "DELETE FROM Class WHERE\n"
        result += "ClassName = '{self._ClassName}'\n".format(self=self)
        return result


class Student(object):
    """SQLite OOP class Student"""

    # initializer for classStudent
    def __init__(self, StudentName, StudentRegNo, ClassName, StudentSubjectCombi, StudentGender, AllSubjectGrades):
        self._StudentName = StudentName
        self._StudentRegNo = StudentRegNo
        self._ClassName = ClassName
        self._StudentSubjectCombi = StudentSubjectCombi
        self._StudentGender = StudentGender
        self._AllSubjectGrades = AllSubjectGrades

    # Mutator Functions
    def set_StudentName(self, new_StudentName):
        self._StudentName = new_StudentName

    def set_StudentRegNo(self, new_StudentRegNo):
        self._StudentRegNo = new_StudentRegNo

    def set_ClassName(self, new_ClassName):
        self._ClassName = new_ClassName

    def set_StudentSubjectCombi(self, new_StudentSubjectCombi):
        self._StudentSubjectCombi = new_StudentSubjectCombi

    def set_StudentGender(self, new_StudentGender):
        self._StudentGender = new_StudentGender

    def set_AllSubjectGrades(self, new_AllSubjectGrades):
        self._AllSubjectGrades = new_AllSubjectGrades

    # Accessor Functions
    def get_StudentName(self):
        return self._StudentName

    def get_StudentRegNo(self):
        return self._StudentRegNo

    def get_ClassName(self):
        return self._ClassName

    def get_StudentSubjectCombi(self):
        return self._StudentSubjectCombi

    def get_StudentGender(self):
        return self._StudentGender

    def get_AllSubjectGrades(self):
        return self._AllSubjectGrades

    # String Representation of Class Student
    def __str__(self):
        result = ""

        return result

    # SQLite: Create Table of Class Student
    @staticmethod
    def create_table():
        result = ""
        result += "CREATE TABLE Student(\n"
        result += "StudentName TEXT NOT NULL,\n"
        result += "StudentRegNo INTEGER NOT NULL CHECK (StudentRegNo > 0),\n"
        result += "ClassName TEXT NOT NULL,\n"
        result += "StudentSubjectCombi TEXT NOT NULL,\n"
        result += "StudentGender TEXT NOT NULL,\n"
        result += "AllSubjectGrades TEXT NOT NULL DEFAULT '',\n"
        result += "PRIMARY KEY(StudentName),\n"
        result += "FOREIGN KEY (ClassName) REFERENCES Class(ClassName)\n"
        result += ")\n"
        return result

    # SQLite: Create new record
    def create_new_record(self):
        result = ""
        result += "INSERT INTO Student\n"
        result += "(StudentName, StudentRegNo, ClassName, StudentSubjectCombi, StudentGender, AllSubjectGrades)\n"
        result += "VALUES\n"
        result += "('{self._StudentName}', '{self._StudentRegNo}', '{self._ClassName}', '{self._StudentSubjectCombi}', '{self._StudentGender}', '{self._AllSubjectGrades}')\n".format(self=self)
        return result

    # SQLite: Update record based on primary key
    def update_record(self):
        result = ""
        result += "UPDATE Student SET\n"
        result += "StudentName = '{self._StudentName}', StudentRegNo = '{self._StudentRegNo}', ClassName = '{self._ClassName}', StudentSubjectCombi = '{self._StudentSubjectCombi}', StudentGender = '{self._StudentGender}', AllSubjectGrades = '{self._AllSubjectGrades}'\n".format(self=self)
        result += "WHERE\n"
        result += "StudentName = '{self._StudentName}'\n".format(self=self)
        return result

    # SQLite: Delete record based on primary key
    def delete_record(self):
        result = ""
        result += "DELETE FROM Student WHERE\n"
        result += "StudentName = '{self._StudentName}'\n".format(self=self)
        return result


class StudentRecords(object):
    """SQLite OOP class StudentRecords"""

    # initializer for classStudentRecords
    def __init__(self, StudentName, SubjectGrade, SubjectName):
        self._StudentName = StudentName
        self._SubjectGrade = SubjectGrade
        self._SubjectName = SubjectName

    # Mutator Functions
    def set_StudentName(self, new_StudentName):
        self._StudentName = new_StudentName

    def set_SubjectGrade(self, new_SubjectGrade):
        self._SubjectGrade = new_SubjectGrade

    def set_SubjectName(self, new_SubjectName):
        self._SubjectName = new_SubjectName

    # Accessor Functions
    def get_StudentName(self):
        return self._StudentName

    def get_SubjectGrade(self):
        return self._SubjectGrade

    def get_SubjectName(self):
        return self._SubjectName

    # String Representation of Class StudentRecords
    def __str__(self):
        result = ""

        return result

    # SQLite: Create Table of Class StudentRecords
    @staticmethod
    def create_table():
        result = ""
        result += "CREATE TABLE StudentRecords(\n"
        result += "StudentName TEXT NOT NULL,\n"
        result += "SubjectGrade TEXT NOT NULL,\n"
        result += "SubjectName TEXT NOT NULL ,\n"
        result += "PRIMARY KEY(StudentName, SubjectName),\n"
        result += "FOREIGN KEY (StudentName) REFERENCES Student(StudentName)\n"
        result += ")\n"
        return result

    # SQLite: Create new record
    def create_new_record(self):
        result = ""
        result += "INSERT INTO StudentRecords\n"
        result += "(StudentName, SubjectGrade, SubjectName)\n"
        result += "VALUES\n"
        result += "('{self._StudentName}', '{self._SubjectGrade}', '{self._SubjectName}')\n".format(self=self)
        return result

    # SQLite: Update record based on primary key
    def update_record(self):
        result = ""
        result += "UPDATE StudentRecords SET\n"
        result += "StudentName = '{self._StudentName}', SubjectGrade = '{self._SubjectGrade}', SubjectName = '{self._SubjectName}'\n".format(self=self)
        result += "WHERE\n"
        result += "StudentName = '{self._StudentName}', SubjectName = '{self._SubjectName}'\n".format(self=self)
        return result

    # SQLite: Delete record based on primary key
    def delete_record(self):
        result = ""
        result += "DELETE FROM StudentRecords WHERE\n"
        result += "StudentName = '{self._StudentName}' and SubjectName = '{self._SubjectName}'\n".format(self=self)
        return result


class Subject(object):
    """SQLite OOP class Subject"""

    # initializer for classSubject
    def __init__(self, SubjectName, Description):
        self._SubjectName = SubjectName
        self._Description = Description

    # Mutator Functions
    def set_SubjectName(self, new_SubjectName):
        self._SubjectName = new_SubjectName

    def set_Description(self, new_Description):
        self._Description = new_Description

    # Accessor Functions
    def get_SubjectName(self):
        return self._SubjectName

    def get_Description(self):
        return self._Description

    # String Representation of Class Subject
    def __str__(self):
        result = ""

        return result

    # SQLite: Create Table of Class Subject
    @staticmethod
    def create_table():
        result = ""
        result += "CREATE TABLE Subject(\n"
        result += "SubjectName TEXT NOT NULL,\n"
        result += "Description TEXT NOT NULL,\n"
        result += "PRIMARY KEY(SubjectName),\n"
        result += "FOREIGN KEY (SubjectName) REFERENCES StudentRecords(SubjectName)\n"
        result += ")\n"
        return result

    # SQLite: Create new record
    def create_new_record(self):
        result = ""
        result += "INSERT INTO Subject\n"
        result += "(SubjectName, Description)\n"
        result += "VALUES\n"
        result += "('{self._SubjectName}', '{self._Description}')\n".format(self=self)
        return result

    # SQLite: Update record based on primary key
    def update_record(self):
        result = ""
        result += "UPDATE Subject SET\n"
        result += "SubjectName = '{self._SubjectName}', Description = '{self._Description}'\n".format(self=self)
        result += "WHERE\n"
        result += "SubjectName = '{self._SubjectName}'\n".format(self=self)
        return result

    # SQLite: Delete record based on primary key
    def delete_record(self):
        result = ""
        result += "DELETE FROM Subject WHERE\n"
        result += "SubjectName = '{self._SubjectName}'\n".format(self=self)
        return result

SubjectAbbrev = ['CM', 'BI', 'PH', 'CP', 'MA', 'EC', 'HI', 'GE',
                 'GP', 'CSC', 'CSE', 'CLL', 'LIT', 'FM', 'TS']

SubjectFull = ['Chemistry', 'Biology', 'Physics', 'Computing', 'Math', 'Economics',
               'History', 'Geography', 'General Paper', 'China Studies in Chinese',
               'China Studies in English', 'Chinese Language and Literature',
               'Literature in English', 'Further Mathematics', 'Translation']


class SeatingArrangement(object):
    """SQLite OOP class SeatingArrangement"""

    # initializer for classSeatingArrangement
    def __init__(self, StudentName, CannotSeatNextTo, SeatInFront, WeakSubjects, StrongSubjects, ClassLst, SeatByGrades, RowNo, ColumnNo):
        self._StudentName = StudentName
        self._CannotSeatNextTo = CannotSeatNextTo
        self._SeatInFront = SeatInFront
        self._WeakSubjects = WeakSubjects
        self._StrongSubjects = StrongSubjects
        self._ClassLst = ClassLst
        self._SeatByGrades = SeatByGrades
        self._RowNo = RowNo
        self._ColumnNo = ColumnNo

    # Mutator Functions
    def set_StudentName(self, new_StudentName):
        self._StudentName = new_StudentName

    def set_CannotSeatNextTo(self, new_CannotSeatNextTo):
        self._CannotSeatNextTo = new_CannotSeatNextTo

    def set_SeatInFront(self, new_SeatInFront):
        self._SeatInFront = new_SeatInFront

    def set_WeakSubjects(self, new_WeakSubjects):
        self._WeakSubjects = new_WeakSubjects

    def set_StrongSubjects(self, new_StrongSubjects):
        self._StrongSubjects = new_StrongSubjects

    def set_ClassLst(self, new_ClassLst):
        self._ClassLst = new_ClassLst

    def set_SeatByGrades(self, new_SeatByGrades):
        self._SeatByGrades = new_SeatByGrades

    def set_RowNo(self, new_RowNo):
        self._RowNo = new_RowNo

    def set_ColumnNo(self, new_ColumnNo):
        self._ColumnNo = new_ColumnNo

    # Accessor Functions
    def get_StudentName(self):
        return self._StudentName

    def get_CannotSeatNextTo(self):
        return self._CannotSeatNextTo

    def get_SeatInFront(self):
        return self._SeatInFront

    def get_WeakSubjects(self):
        return self._WeakSubjects

    def get_StrongSubjects(self):
        return self._StrongSubjects

    def get_ClassLst(self):
        return self._ClassLst

    def get_SeatByGrades(self):
        return self._SeatByGrades

    def get_RowNo(self):
        return self._RowNo

    def get_ColumnNo(self):
        return self._ColumnNo

    # String Representation of Class SeatingArrangement
    def __str__(self):
        result = ""

        return result

    # SQLite: Create Table of Class SeatingArrangement
    @staticmethod
    def create_table():
        result = ""
        result += "CREATE TABLE SeatingArrangement(\n"
        result += "StudentName TEXT NOT NULL,\n"
        result += "CannotSeatNextTo TEXT NOT NULL DEFAULT '',\n"
        result += "SeatInFront BOOLEAN NOT NULL DEFAULT FALSE,\n"
        result += "WeakSubjects TEXT NOT NULL DEFAULT '',\n"
        result += "StrongSubjects TEXT NOT NULL DEFAULT '',\n"
        result += "ClassLst TEXT NOT NULL DEFAULT '',\n"
        result += "SeatByGrades TEXT NOT NULL DEFAULT '',\n"
        result += "RowNo INTEGER NOT NULL DEFAULT 0,\n"
        result += "ColumnNo INTEGER NOT NULL DEFAULT 0,\n"
        result += "PRIMARY KEY(StudentName),\n"
        result += "FOREIGN KEY (StudentName) REFERENCES StudentRecords(SubjectName)\n"
        result += ")\n"
        return result

    # SQLite: Create new record
    def create_new_record(self):
        result = ""
        result += "INSERT INTO SeatingArrangement\n"
        result += "(StudentName, CannotSeatNextTo, SeatInFront, WeakSubjects, StrongSubjects, ClassLst, SeatByGrades, RowNo, ColumnNo)\n"
        result += "VALUES\n"
        result += "('{self._StudentName}', '{self._CannotSeatNextTo}', '{self._SeatInFront}', '{self._WeakSubjects}', '{self._StrongSubjects}', '{self._ClassLst}', '{self._SeatByGrades}', '{self._RowNo}', '{self._ColumnNo}')\n".format(self=self)
        return result

    # SQLite: Update record based on primary key
    def update_record(self):
        result = ""
        result += "UPDATE SeatingArrangement SET\n"
        result += "StudentName = '{self._StudentName}', CannotSeatNextTo = '{self._CannotSeatNextTo}', SeatInFront = '{self._SeatInFront}', WeakSubjects = '{self._WeakSubjects}', StrongSubjects = '{self._StrongSubjects}', ClassLst = '{self._ClassLst}', SeatByGrades = '{self._SeatByGrades}', RowNo = '{self._RowNo}', ColumnNo = '{self._ColumnNo}'\n".format(self=self)
        result += "WHERE\n"
        result += "StudentName = '{self._StudentName}'\n".format(self=self)
        return result

    # SQLite: Delete record based on primary key
    def delete_record(self):
        result = ""
        result += "DELETE FROM SeatingArrangement WHERE\n"
        result += "StudentName = '{self._StudentName}'\n".format(self=self)
        return result


class User(object):
    """SQLite OOP class User"""

    # initializer for classUser
    def __init__(self, UserName, Password):
        self._UserName = UserName
        self._Password = Password

    # Mutator Functions
    def set_UserName(self, new_UserName):
        self._UserName = new_UserName

    def set_Password(self, new_Password):
        self._Password = new_Password

    # Accessor Functions
    def get_UserName(self):
        return self._UserName

    def get_Password(self):
        return self._Password

    # String Representation of Class User
    def __str__(self):
        result = ""

        return result

    # SQLite: Create Table of Class User
    @staticmethod
    def create_table():
        result = ""
        result += "CREATE TABLE User(\n"
        result += "UserName TEXT NOT NULL,\n"
        result += "Password TEXT NOT NULL,\n"
        result += "PRIMARY KEY(UserName)\n"
        result += ")\n"
        return result

    # SQLite: Create new record
    def create_new_record(self):
        result = ""
        result += "INSERT INTO User\n"
        result += "(UserName, Password)\n"
        result += "VALUES\n"
        result += "('{self._UserName}', '{self._Password}')\n".format(self=self)
        return result

    # SQLite: Update record based on primary key
    def update_record(self):
        result = ""
        result += "UPDATE User SET\n"
        result += "UserName = '{self._UserName}', Password = '{self._Password}'\n".format(self=self)
        result += "WHERE\n"
        result += "UserName = '{self._UserName}'\n".format(self=self)
        return result

    # SQLite: Delete record based on primary key
    def delete_record(self):
        result = ""
        result += "DELETE FROM User WHERE\n"
        result += "UserName = '{self._UserName}'\n".format(self=self)
        return result


class SavedSeatArr(object):
    """SQLite OOP class SavedSeatArr"""

    # initializer for classSavedSeatArr
    def __init__(self, UserName, SeatArrName, SeatArrSeq, RowNo, ColumnNo, CommentIDs = ""):
        self._UserName = UserName
        self._SeatArrName = SeatArrName
        self._SeatArrSeq = SeatArrSeq
        self._RowNo = RowNo
        self._ColumnNo = ColumnNo
        self._CommentIDs = CommentIDs

    # Mutator Functions
    def set_UserName(self, new_UserName):
        self._UserName = new_UserName

    def set_SeatArrName(self, new_SeatArrName):
        self._SeatArrName = new_SeatArrName

    def set_SeatArrSeq(self, new_SeatArrSeq):
        self._SeatArrSeq = new_SeatArrSeq

    def set_RowNo(self, new_RowNo):
        self._RowNo = new_RowNo

    def set_ColumnNo(self, new_ColumnNo):
        self._ColumnNo = new_ColumnNo

    def set_CommentIDs(self, new_CommentIDs):
        if self._CommentIDs == "":
            self._CommentIDs = new_CommentIDs
        else:
            self._CommentIDs += "," + new_CommentIDs

    def delete_CommentIDs(self, CommentID):
        temp = (self._CommentIDs.split(","))
        result = ""
        for ID in temp:
            if ID != CommentID:
                if result == "":
                    result += ID
                else:
                    result += "," + ID

        self._CommentIDs = result

    # Accessor Functions
    def get_UserName(self):
        return self._UserName

    def get_SeatArrName(self):
        return self._SeatArrName

    def get_SeatArrSeq(self):
        return self._SeatArrSeq

    def get_RowNo(self):
        return self._RowNo

    def get_ColumnNo(self):
        return self._ColumnNo

    def get_CommentIDs(self):
        return self._CommentIDs

    # String Representation of Class SavedSeatArr
    def __str__(self):
        result = ""

        return result

    # SQLite: Create Table of Class SavedSeatArr
    @staticmethod
    def create_table():
        result = ""
        result += "CREATE TABLE SavedSeatArr(\n"
        result += "UserName TEXT NOT NULL,\n"
        result += "SeatArrName TEXT NOT NULL,\n"
        result += "SeatArrSeq TEXT NOT NULL,\n"
        result += "RowNo INTEGER NOT NULL DEFAULT 0,\n"
        result += "ColumnNo INTEGER NOT NULL DEFAULT 0,\n"
        result += "CommentIDs TEXT ,\n"
        result += "PRIMARY KEY(UserName, SeatArrName),\n"
        result += "FOREIGN KEY (UserName) REFERENCES User(UserName)\n"
        result += ")\n"
        return result

    # SQLite: Create new record
    def create_new_record(self):
        result = ""
        result += "INSERT INTO SavedSeatArr\n"
        result += "(UserName, SeatArrName, SeatArrSeq, RowNo, ColumnNo, CommentIDs)\n"
        result += "VALUES\n"
        result += "('{self._UserName}', '{self._SeatArrName}', '{self._SeatArrSeq}', '{self._RowNo}', '{self._ColumnNo}', '{self._CommentIDs}')\n".format(self=self)
        return result

    # SQLite: Update record based on primary key
    def update_record(self):
        result = ""
        result += "UPDATE SavedSeatArr SET\n"
        result += "UserName = '{self._UserName}', SeatArrName = '{self._SeatArrName}', SeatArrSeq = '{self._SeatArrSeq}', RowNo = '{self._RowNo}', ColumnNo = '{self._ColumnNo}', CommentIDs = '{self._CommentIDs}'\n".format(self=self)
        result += "WHERE\n"
        result += "UserName = '{self._UserName}' and SeatArrName = '{self._SeatArrName}'\n".format(self=self)
        return result

    # SQLite: Delete record based on primary key
    def delete_record(self):
        result = ""
        result += "DELETE FROM SavedSeatArr WHERE\n"
        result += "UserName = '{self._UserName}' and SeatArrName = '{self._SeatArrName}'\n".format(self=self)
        return result


class CurrentUser(object):
    """SQLite OOP class CurrentUser"""

    # initializer for classCurrentUser
    def __init__(self, UserName):
        self._UserName = UserName

    # Mutator Functions
    def set_UserName(self, new_UserName):
        self._UserName = new_UserName

    # Accessor Functions
    def get_UserName(self):
        return self._UserName

    # String Representation of Class CurrentUser
    def __str__(self):
        result = ""

        return result

    # SQLite: Create Table of Class CurrentUser
    @staticmethod
    def create_table():
        result = ""
        result += "CREATE TABLE CurrentUser(\n"
        result += "UserName TEXT NOT NULL,\n"
        result += "PRIMARY KEY(UserName),\n"
        result += "FOREIGN KEY (UserName) REFERENCES User(UserName)\n"
        result += ")\n"
        return result

    # SQLite: Create new record
    def create_new_record(self):
        result = ""
        result += "INSERT INTO CurrentUser\n"
        result += "(UserName)\n"
        result += "VALUES\n"
        result += "('{self._UserName}')\n".format(self=self)
        return result

    # SQLite: Update record based on primary key
    def update_record(self):
        result = ""
        result += "UPDATE CurrentUser SET\n"
        result += "UserName = '{self._UserName}'\n".format(self=self)
        result += "WHERE\n"
        result += "UserName = '{self._UserName}'\n".format(self=self)
        return result

    # SQLite: Delete record based on primary key
    def delete_record(self):
        result = ""
        result += "DELETE FROM CurrentUser WHERE\n"
        result += "UserName = '{self._UserName}'\n".format(self=self)
        return result


class Comment(object):
    """SQLite OOP class Comment"""

    # initializer for classComment
    def __init__(self, SeatArrName, CommentID, CommentText, CommentDatetime, UserName):
        self._SeatArrName = SeatArrName
        self._CommentID = CommentID
        self._CommentText = CommentText
        self._CommentDatetime = CommentDatetime
        self._UserName = UserName

    # Mutator Functions
    def set_SeatArrName(self, new_SeatArrName):
        self._SeatArrName = new_SeatArrName

    def set_CommentID(self, new_CommentID):
        self._CommentID = new_CommentID

    def set_CommentText(self, new_CommentText):
        self._CommentText = new_CommentText

    def set_CommentDatetime(self, new_CommentDatetime):
        self._CommentDatetime = new_CommentDatetime

    def set_UserName(self, new_UserName):
        self._UserName = new_UserName

    # Accessor Functions
    def get_SeatArrName(self):
        return self._SeatArrName

    def get_CommentID(self):
        return self._CommentID

    def get_CommentText(self):
        return self._CommentText

    def get_CommentDatetime(self):
        return self._CommentDatetime

    def get_UserName(self):
        return self._UserName

    # String Representation of Class Comment
    def __str__(self):
        result = ""

        return result

    # SQLite: Create Table of Class Comment
    @staticmethod
    def create_table():
        result = ""
        result += "CREATE TABLE Comment(\n"
        result += "SeatArrName TEXT NOT NULL,\n"
        result += "CommentID INTEGER NOT NULL,\n"
        result += "CommentText TEXT NOT NULL,\n"
        result += "CommentDatetime TEXT NOT NULL,\n"
        result += "UserName TEXT NOT NULL,\n"
        result += "PRIMARY KEY(SeatArrName, CommentID),\n"
        result += "FOREIGN KEY (SeatArrName) REFERENCES SavedSeatArr(SeatArrName),\n"
        result += "FOREIGN KEY (UserName) REFERENCES User(UserName)\n"
        result += ")\n"
        return result

    # SQLite: Create new record
    def create_new_record(self):
        result = ""
        result += "INSERT INTO Comment\n"
        result += "(SeatArrName, CommentID, CommentText, CommentDatetime, UserName)\n"
        result += "VALUES\n"
        result += "('{self._SeatArrName}', '{self._CommentID}', '{self._CommentText}', '{self._CommentDatetime}', '{self._UserName}')\n".format(self=self)
        return result

    # SQLite: Update record based on primary key
    def update_record(self):
        result = ""
        result += "UPDATE Comment SET\n"
        result += "SeatArrName = '{self._SeatArrName}', CommentID = '{self._CommentID}', CommentText = '{self._CommentText}', CommentDatetime = '{self._CommentDatetime}', UserName = '{self._UserName}'\n".format(self=self)
        result += "WHERE\n"
        result += "CommentID = '{self._CommentID}'\n".format(self=self)
        return result

    # SQLite: Delete record based on primary key
    def delete_record(self):
        result = ""
        result += "DELETE FROM Comment WHERE\n"
        result += "SeatArrName = '{self._SeatArrName}' and CommentID = '{self._CommentID}'\n".format(self=self)
        return result


class UserInfo(object):
    def __init__(self,username,password):
        self._username = username
        self._password = password

    def set_username(self,new_username):
        self._username = new_username
    def set_password(self,new_password):
        self._password = new_password

    def get_username(self):
        return self._username
    def get_password(self):
        return self._password

    def __str__(self):
        result = ""
        return result


    @staticmethod
    def create_table():
        result = ""
        result += "CREATE TABLE UserInfo(\n"
        result += "username TEXT ,\n"
        result += "password TEXT NOT NULL,\n"
        result += "PRIMARY KEY(username)\n"
        result += ")\n"
        return result

    def create_new_account(self):
        result = ""
        result += "INSERT INTO UserInfo\n"
        result += "(username,password)\n"
        result += "VALUES\n"
        result += "('{self._username}', '{self._password}')\n".format(self=self)
        return result

    def update_account():
        result = ""
        result += "UPDATE UserInfo SET\n"
        result += "username = '{self._username}', password = '{self._password}'\n".format(self=self)
        result += "WHERE\n"
        result += "VenueName = '{self._VenueName}'\n".format(self=self)
        return result

    def delete_account():
        result = ""
        result += "DELETE FROM UserInfo WHERE\n"
        result += "username = '{self._username}'\n".format(self=self)
        return result
