from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

#REST part
api.add_resource(HelloWorld, '/api')


#starting static front end part
@app.route('/')
def root():
    """expected user entry point redirect to our html file"""
    return app.send_static_file('index.html')


if __name__ == '__main__':
    app.run(debug=True)

