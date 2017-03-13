from flask import Flask
from flask_restful import Api, abort
from resources import PersonResource, PersonListResource
from webargs.flaskparser import parser


app = Flask(__name__)
api = Api(app)


#REST part
api.add_resource(PersonListResource, '/api/persons')
api.add_resource(PersonResource, '/api/person/<person_id>')

# webargs: This error handler is necessary for usage with Flask-RESTful.
@parser.error_handler
def handle_request_parsing_error(err):
    abort(422, errors=err.messages)

#starting static front end part
@app.route('/')
def root():
    """expected user entry point redirect to our html file"""
    return app.send_static_file('index.html')


if __name__ == '__main__':
    app.run(debug=True)

