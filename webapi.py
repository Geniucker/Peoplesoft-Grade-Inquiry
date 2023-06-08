import peoplesoft

import flask

app = flask.Flask(__name__, static_folder="mainpage")

@app.route("/")
def mainpage():
    return app.send_static_file("index.html")
# route for mainpage
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return app.send_static_file(path)


@app.route('/grade')
def grade():
    username = flask.request.args.get('username')
    password = flask.request.args.get('password')
    choice = flask.request.args.get('choice')
    choice = int(choice) if choice is not None else 1
    user = peoplesoft.User(username, password)
    grade = user.grade(choice)

    if choice == 2:
        result = "<html><body><table>"
        result += "<tr><th>Class</th><th>Description</th><th>Units</th><th>Grading</th><th>Grade</th><th>Grade Points</th></tr>"
        for i in grade:
            result += f"""
<tr>
    <td>{i['class']}</td>
    <td>{i['description']}</td>
    <td>{i['units']}</td>
    <td>{i['grading']}</td>
    <td>{i['grade']}</td>
    <td>{i['grade_points']}</td>
</tr>"""
        result += "</table>"
        result += "<style>table, th, td {border: 1px solid black;}</style>"
        result += "</body></html>"
    else:
        result = "还没写完"
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50080)