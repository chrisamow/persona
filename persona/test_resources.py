from requests import put, get, post, delete
import json
#from datetime import datetime
from dateutil import parser
from copy import deepcopy



def test_rest():
    #list persons should be 0

    #add a person
    dict1 = {'lastname':'anderson', 'firstname':'arthur','dateofbirth':'2015-03-25T00:00:00.000Z' }
    data1 = json.dumps(dict1)
    print('posting: data={}'.format(data1))
    reply1 = post('http://localhost:5000/api/persons', headers={'Content-Type': 'application/json'}, data=data1)
    assert reply1.ok
    assert 201 == reply1.status_code
    print('returned:{}   content:{}'.format(reply1, reply1.content))
    #print(reply1.json())
    try:
        js1 = reply1.json()
    except ValueError as ve:
        assert not ve

    #list of persons
    reply2 = get('http://localhost:5000/api/persons')
    assert reply2.ok
    assert 200 == reply2.status_code
    try:
        js2 = reply2.json()
    except ValueError as ve:
        assert not ve

    #get specific person
    reply3 = get('http://localhost:5000/api/person/{}'.format(js1['id']))
    assert reply3.ok
    try:
        js3 = reply3.json()
    except ValueError as ve:
        assert not ve
    assert js3['lastname'] == dict1['lastname']
    assert js3['firstname'] == dict1['firstname']
    assert parser.parse(js3['dateofbirth']).date() == parser.parse(dict1['dateofbirth']).date()


    #change person
    #note how awkward it is to simulate client js in python since python datetime.isoformat does this: '2015-03-25T00:00:00+00:00'
    dict4 = deepcopy(dict1)
    #del dict4['id']    #would have preferred modding js3
    dict4['firstname'] = 'changedname'
    reply4 = put('http://localhost:5000/api/person/1', headers={'Content-Type': 'application/json'}, data=json.dumps(dict4))
    assert reply4.ok
    assert 201 == reply4.status_code


    #delete person
    #going to assume noone was added since we got list in js2
    lastguy = max(js2, key=lambda x: x['id'])
    reply5 = delete('http://localhost:5000/api/person/{}'.format(lastguy['id']))
    assert reply5.ok
    assert 204 == reply5.status_code
    #check list of persons
    reply6 = get('http://localhost:5000/api/persons')
    assert reply6.ok
    assert 200 == reply6.status_code
    try:
        js6 = reply6.json()
    except ValueError as ve:
        assert not ve
    assert len(js6) == (len(js2) - 1)



    #list of persons


def test_params():
    pass
"""
>>> payload = {'key1': 'value1', 'key2': 'value2'}
>>> r = requests.get('http://httpbin.org/get', params=payload)

equivalent of
 1881  curl "http://localhost:5000/api/persons?startid=30&letter=a&search=haha"
 1882  curl "http://localhost:5000/api/persons?startid=30&letter=a"
"""



test_rest()

