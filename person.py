from flask import request
from flask_restful import Resource

persons = {}

class Person(Resource):
    def get(self, person_id):
        return {person_id: persons[person_id]}

    def put(self, person_id):
        persons[person_id] = request.form['data']
        return {person_id: persons[person_id]}


