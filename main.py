"""
Program:    Internship Database
Creators:   Ragy Costa de jesus, Kaden Carr, Ben Heins
Course:     Intro to Data Engineering
Date:       Mat 5th, 2022
Desc:       Internship Database to store and find internship for students
"""


import sqlite3
from sqlite3 import Error
import PySimpleGUI as sg

sg.theme('BlueMono')

internship_heading = ['Internship ID', 'Job Title', 'Job Description', 'Salary']

internship_data = [[]]

layout = [
    [sg.Text('Internship ID: '), sg.InputText(key='-Internship-'), sg.Button('SEARCH')],
    [sg.Table(values=internship_data,
              background_color="LightBlue",
              headings=internship_heading,
              header_background_color="Green",
              header_text_color='White',
              auto_size_columns=False,
              col_widths=[20, 120],
              justification='left',
              num_rows=6,
              alternating_row_color='LightGrey',
              key='-INTERNSHIP_DISPLAY-',
              row_height=80,
              tooltip='Respondent ranked films')]
]



def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)


    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
       :param conn: Connection object
       :param create_table_sql: a CREATE TABLE statement
       :return:
       """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_person(conn, person):
    """
    Create a new person into the Person table
    :param conn:
    :param Person:
    :return: person id
    """
    sql = ''' INSERT INTO Person(personID, firstName, middleName, lastName, gender, address, dateOfBirth, phoneNumber, email )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    cur = conn.cursor()
    cur.execute(sql, person)
    conn.commit()
    return cur.lastrowid


def create_student(conn, student):
    """
    Create a new Student into the Student table
    :param conn:
    :param Student:
    :return: Student id
    """
    sql = ''' INSERT INTO Student(studentID, skills, major, minor )
                VALUES (?, ?, ?, ?)'''
    cur = conn.cursor()
    cur.execute(sql, student)
    conn.commit()
    return cur.lastrowid


def create_internship(conn, internship):
    """
    Create a new Internship into the Internship table
    :param conn:
    :param Internship:
    :return: Internship id
    """
    sql = ''' INSERT INTO Internship(internshipID, jobTitle, jobDesc, salary, ft_or_pt, os_or_re, requirement )
                VALUES (?, ?, ?, ?, ?, ?, ?)'''
    cur = conn.cursor()
    cur.execute(sql, internship)
    conn.commit()
    return cur.lastrowid


def create_major(conn, major):
    """
    Create a new major into the major table
    :param conn:
    :param Major:
    :return: major id
    """
    sql = ''' INSERT INTO Major(majorID, minorID, majorName )
                VALUES (?, ?, ?)'''
    cur = conn.cursor()
    cur.execute(sql, major)
    conn.commit()
    return cur.lastrowid


def create_company(conn, company):
    """
    Create a new company into the Company table
    :param conn:
    :param company:
    :return: company id
    """
    sql = ''' INSERT INTO Company(companyID, companyNAme, address, linkToWeb )
                VALUES (?, ?, ?, ?)'''
    cur = conn.cursor()
    cur.execute(sql, company)
    conn.commit()
    return cur.lastrowid


def update_person(conn, person):
    """
        update priority, begin_date, and end date of a task
        :param conn:
        :param task:
        :return: project id
        """
    sql = ''' UPDATE Person
                  SET firstName = ? ,
                      middleName = ? ,
                      lastName = ?,
                      address = ?,
                      phoneNumber = ?,
                      email = ?
                  WHERE personID = ?
                  '''
    cur = conn.cursor()
    cur.execute(sql, person)
    conn.commit()

def display_internship(conn, internship, window):
    """
        Select all rows from the intership table and print them
        :param conn:
        :return:
        """

    cur = conn.cursor()


    if internship == '':
        cur.execute("select * from Internship")
    else:
        cur.execute("select * from Internship where internshipID = ?", (internship,))

    rows = cur.fetchall()
    window['-INTERNSHIP_DISPLAY-'].update(values=rows)

    for row in rows:
        print(row)


def main():
    database = r"C:\Users\ragyc\OneDrive\COP3710\Project\InterhsipDB\internshipDB.db"

    # create a database connection
    conn = create_connection(database)


    inputVar = input('Enter (1) to Search Internship, (2) to insert Internship, and (3) to exit:')



    if inputVar == '2':
         with conn:
            internshipID = input('Enter internship ID: ')
            internshipTitle = input('Enter internship Title: ')
            internshipDesc = input('Enter Description for internship: ')
            internshipSalary = input('Enter Salary: ')
            internshipTime = input ('Full-time or Part-time: ')
            intershipSite = input ('On-site or Remote: ')
            internshipReq = input ('Requirements for Internship:')

            internship = (internshipID, internshipTitle, internshipDesc, internshipSalary, internshipTime,intershipSite, internshipReq)
            internship_id = create_internship(conn, internship)


    if inputVar == '1':
        window = sg.Window('Internship Database', layout)

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
            if event == 'SEARCH':
                display_internship(conn, values['-Internship-'], window)

        window.close()


if __name__ == '__main__':
    main()