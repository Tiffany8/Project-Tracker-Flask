from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)

@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github', 'jhacks')
    first, last, github = hackbright.get_student_by_github(github)
    html = render_template('student_info.html', first=first, last=last, github=github)
    return html

if __name__ == "__main__":
    app.run(debug=True)