from flask import jsonify #this jsonify function is used to convert the response object into a json string
from marshmallow.exceptions import ValidationError #this is the new import statement that we need to add to our server.py file to handle the ValidationError exception that we are raising in our assertions.py file in the assert_valid() function.
from core import app
from core.apis.assignments import student_assignments_resources, teacher_assignment_resources 
from core.libs import helpers
from core.libs.exceptions import FyleError #this FyleError exception is defined in the core\libs\exceptions.py file
from werkzeug.exceptions import HTTPException

from sqlalchemy.exc import IntegrityError #this IntegrityError exception is raised when we try to insert a duplicate record into the database

app.register_blueprint(student_assignments_resources, url_prefix='/student')
app.register_blueprint(teacher_assignment_resources, url_prefix='/teacher')


@app.route('/')
def ready():
    response = jsonify({
        'status': 'ready',
        'time': helpers.get_utc_now()
    })

    return response

@app.errorhandler(Exception) # type: ignore
def handle_error(err):
    if isinstance(err, FyleError):
        return jsonify(
            error=err.__class__.__name__, message=err.message
        ), err.status_code
    elif isinstance(err, ValidationError):
        return jsonify(
            error=err.__class__.__name__, message=err.messages
        ), 400
    elif isinstance(err, IntegrityError):
        return jsonify(
            error=err.__class__.__name__, message=str(err.orig)
        ), 400
    elif isinstance(err, HTTPException):
        return jsonify(
            error=err.__class__.__name__, message=str(err)
        ), err.code

    raise err
