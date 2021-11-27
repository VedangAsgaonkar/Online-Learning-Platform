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
    if (cmd =='feedback'):
        try:
            file_name = input('Enter file name- ')
            course_name = input('Enter course name- ')
            asgn_name = input('Enter assignment name- ')
            files = {'upload_file': ('grades.csv', open(file_name,'rb'), 'text/csv')}
            response = requests.post('http://127.0.0.1:8000/rest/feedback/', data = {'username':'Teacher1', 'password':'BlueFire', 'course_name' : course_name, 'asgn_name' : asgn_name }, files=files)
            print(response.json())
        except Exception as e:
            print("Error-",e)
    elif (cmd=='exit'):
        break
    else:
        pass

    
