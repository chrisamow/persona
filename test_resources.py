from requests import put, get, post
import json
import datetime



def test_rest():
    #list persons should be 0

    #add a person
    data = json.dumps({'lastname':'anderson', 'firstname':'arthur','dateofbirth':'2015-03-25T00:00:00.000Z'})
    print('data={}'.format(data))
    reply = post('http://localhost:5000/api/persons', headers={'Content-Type': 'application/json'}, data=data)
    assert 201 == reply.status_code
    print('returned:{}   content:{}'.format(reply, reply.content))
    #print(reply.json())

    #list of persons



    #change person


    #delete person



    #list of persons



test_rest()

