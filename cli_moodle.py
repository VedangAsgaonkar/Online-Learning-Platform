import requests
from requests.models import HTTPBasicAuth

username = input('Please Enter Username- ')
password = input('Please Enter Password- ')
while True:
    cmd = input('>>')
    if (cmd =='courses'):
        response = requests.post('http://127.0.0.1:8000/rest/courses/', data = {'username':username, 'password':password})
        try:
            i=1
            for course in response.json()['courses']:
                print(i, course)
                i+=1
        except Exception as e:
            print("Error- ", e)
    if (cmd =='todo'):
        try:
            response = requests.post('http://127.0.0.1:8000/rest/todo/', data = {'username':username, 'password':password})
            i=1
            for task in response.json()['todo']:
                print(i,task)
                i+=1
        except Exception as e:
            print("Error- ", e)
    elif (cmd=='exit'):
        break
    else:
        pass

    
