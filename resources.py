from datetime import datetime
#from flask import request
from flask_restful import Resource, fields, reqparse, marshal_with, abort
from db import session
from models import Person
import webargs
from webargs.flaskparser import use_kwargs
from string import ascii_lowercase


#datetime works across the stack better so we will ignore the time component
#note that RFC3339 is a profile of ISO8601

#outgoing
person_fields = {
    'id': fields.Integer,
    'lastname': fields.String,
    'firstname': fields.String,
    'dateofbirth': fields.DateTime(dt_format='iso8601'),     #'rfc822')
        #will not have the Z at the end for UTC, but javascript will still accept this in a new Date() 
    'zipcode': fields.String
}

#incoming
person_parser = reqparse.RequestParser()
person_parser.add_argument('lastname', type=str)
person_parser.add_argument('firstname', type=str)
person_parser.add_argument('dateofbirth', type=lambda x: datetime.strptime(x,'%Y-%m-%dT%H:%M:%S.%fZ'))
person_parser.add_argument('zipcode', type=str)
#expecting  RFC3339 date format, e.g. javascript: new Date("2015-03-25").toISOString()-->'2015-03-25T00:00:00.000Z'



class PersonResource(Resource):
    @marshal_with(person_fields)
    def get(self, person_id):
        person = session.query(Person).filter(Person.id == person_id).one()
        if not person:
            abort(404, message="Person {} doesn't exist".format(person_id))
        return person

    def delete(self, person_id):
        #import pudb; pu.db
        person = session.query(Person).filter(Person.id == person_id).one()
        if not person:
            abort(404, message="Person {} doesn't exist".format(person_id))
        session.delete(person)
        session.commit()
        return person_id, 200   #note, a 204 does not allow return info


    @marshal_with(person_fields)
    def put(self, person_id):
        parsed_args = person_parser.parse_args()
        person = session.query(Person).filter(Person.id == person_id).first()
        person.lastname = parsed_args['lastname']
        person.firstname = parsed_args['firstname']
        person.dateofbirth = parsed_args['dateofbirth']
        session.add(person)
        session.commit()
        return person, 201



class PersonListResource(Resource):
    args = {
        'startid': webargs.fields.Int(required=False, validate=webargs.validate.Range(min=1)),
        'letter': webargs.fields.Str(required=False, 
            validate=webargs.validate.OneOf(list(ascii_lowercase))),
        'search': webargs.fields.Str(required=False)
    }

    @marshal_with(person_fields)
    @use_kwargs(args)
    def get(self, startid, letter, search):
        #import pudb; pu.db  #pyflakes gets confused (webargs related?) throws an error, ignore
        if search:
            persons=session.query(Person).filter(Person.lastname.ilike('%{}%'.format(search))).order_by('lastname','firstname').all()
                #all needs to be last
        else:
            persons = session.query(Person).order_by('lastname', 'firstname').all()   #all needs to be last
        return persons

    @marshal_with(person_fields)
    def post(self):
        parsed_args = person_parser.parse_args()
        person = Person(    lastname=parsed_args['lastname'],
                            firstname=parsed_args['firstname'],
                            dateofbirth=parsed_args['dateofbirth'],
                            zipcode=parsed_args['zipcode'])
        session.add(person)
        session.commit()
        return person, 201


