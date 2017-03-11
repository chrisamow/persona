from flask import request
from flask_restful import Resource, fields

persons = {}

class PersonResource(Resource):
    def get(self, person_id):
        return {person_id: persons[person_id]}

    def put(self, person_id):
        persons[person_id] = request.form['data']
        return {person_id: persons[person_id]}


class PersonListResource(Resource):
    def get(self):
        return persons

#    def post

