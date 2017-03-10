from flask import Flask
from flask_restful import Resource, Api
from person import Person

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

#REST part
api.add_resource(HelloWorld, '/api')
api.add_resource(Person, '/api/person/<person_id>')


#starting static front end part
@app.route('/')
def root():
    """expected user entry point redirect to our html file"""
    return app.send_static_file('index.html')


if __name__ == '__main__':
    app.run(debug=True)

