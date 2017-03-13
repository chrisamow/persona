from flask import Flask
from flask_restful import Resource, Api
from resources import PersonResource, PersonListResource
app = Flask(__name__)
api = Api(app)


#REST part
api.add_resource(PersonListResource, '/api/persons', '/api/persons/<startingid>')
api.add_resource(PersonResource, '/api/person/<person_id>')


#starting static front end part
@app.route('/')
def root():
    """expected user entry point redirect to our html file"""
    return app.send_static_file('index.html')


if __name__ == '__main__':
    app.run(debug=True)

