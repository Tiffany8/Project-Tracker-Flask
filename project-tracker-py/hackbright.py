"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""

import sqlite3

db_connection = sqlite3.connect("hackbright.db", check_same_thread=False)
db_cursor = db_connection.cursor()

def handle_input():
    """Main loop.

    Repeatedly prompt for commands, performing them, until 'quit' is received as a
    command."""

    command = None

    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            github = args[0]
            get_student_by_github(github)

        elif command == "new_student":
            first_name, last_name, github = args   # unpack!
            make_new_student(first_name, last_name, github)

        elif command == "get_project_info":
            title = args[0]
            get_project_info(title)

        elif command == "get_project_grade":
            github_username, project = args
            get_project_grade(github_username, project)

        elif command == "grade_assign":
            github_username, project_title, grade = args
            grade_assign(github_username, project_title, grade)

def get_student_by_github(github):
    """Given a github account name, print information about the matching student."""

    QUERY = """
        SELECT first_name, last_name, github
        FROM Students
        WHERE github = ?
        """
    db_cursor.execute(QUERY, (github,))
    row = db_cursor.fetchone()
    print row
    print "Student: %s %s\nGithub account: %s" % (
        row[0], row[1], row[2])




def make_new_student(first_name, last_name, github):
    """Add a new student and print confirmation.

    Given a first name, last name, and Github account, add student to the 
    database and print a confirmation message.
    """

    QUERY = """ 
    INSERT INTO Students VALUES (?, ?, ?)"""

    db_cursor.execute(QUERY, (first_name, last_name, github))

    db_connection.commit()
    print "Successfully added student: %s %s" % (first_name, last_name)

def get_project_info(title):
    """Given a project title, print info about the project (title, description,
    max grade. 
    """

    QUERY = """
    SELECT title, description, max_grade
    FROM Projects
    WHERE title = ?
    """

    db_cursor.execute(QUERY, (title,))
    row = db_cursor.fetchone()
    print "Project title: %s\nDescription: %s\nMax Grade: %s"  % (row[0], row[1], row[2])

def get_project_grade(github_username, project):
    """Given a student's github username and project title, print student's grade. 
    """

    QUERY = """
    SELECT grade 
    FROM Grades
    WHERE student_github = ? AND project_title = ?
    """

    db_cursor.execute(QUERY, (github_username, project))
    row = db_cursor.fetchone()
    # print row
    print "Grade: %s" % (row[0])

def grade_assign(github_username, project_title, grade):
    """Give a grade to a student. 
    """

    QUERY = """
    INSERT INTO Grades VALUES (?, ?, ?)
    """

    db_cursor.execute(QUERY, (github_username, project_title, grade))
    db_connection.commit()

    print "You have Successfully added student %s's project %s with grade %s" % (github_username, project_title, grade)


if __name__ == "__main__":
    handle_input()

    # To be tidy, we'll close our database connection -- though, since this
    # is where our program ends, we'd quit anyway.

    db_connection.close()
