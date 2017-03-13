from requests import put, get, post
import json
import datetime



def test_rest():
    #list persons should be 0

    #add a person
    data1 = json.dumps({'lastname':'anderson', 'firstname':'arthur','dateofbirth':'2015-03-25T00:00:00.000Z'})
    print('posting: data={}'.format(data1))
    reply1 = post('http://localhost:5000/api/persons', headers={'Content-Type': 'application/json'}, data=data1)
    assert 201 == reply1.status_code
    print('returned:{}   content:{}'.format(reply1, reply1.content))
    #print(reply1.json())

    #list of persons
    reply2 = get('http://localhost:5000/api/persons')
    assert reply2.ok
    assert 200 == reply2.status_code
    try:
        js2 = reply2.json()
    except ValueError as ve:
        assert not ve


    #change person


    #delete person



    #list of persons



test_rest()

