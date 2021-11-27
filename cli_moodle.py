import requests
from colorama import init, Fore, Back, Style
init()

username = input(Fore.YELLOW+'Please Enter Username- ' + Style.RESET_ALL)
password = input(Fore.YELLOW+'Please Enter Password- ' + Style.RESET_ALL)
while True:
    cmd = input(Fore.CYAN +'BlueFire ' + Fore.MAGENTA+'$ ' + Style.RESET_ALL)
    if (cmd =='courses'):
        response = requests.post('http://127.0.0.1:8000/rest/courses/', data = {'username':username, 'password':password})
        try:
            i=1
            for course in response.json()['courses']:
                print(i, course)
                i+=1
        except Exception as e:
            print("Error- ", e)
    elif (cmd =='todo'):
        try:
            response = requests.post('http://127.0.0.1:8000/rest/todo/', data = {'username':username, 'password':password})
            i=1
            for task in response.json()['todo']:
                print(i,task)
                i+=1
        except Exception as e:
            print("Error- ", e)
    elif (cmd =='feedback'):
        try:
            file_name = input(Fore.YELLOW+'Enter file name- '+ Style.RESET_ALL)
            course_name = input(Fore.YELLOW+'Enter course name- '+ Style.RESET_ALL)
            asgn_name = input(Fore.YELLOW+'Enter assignment name- '+ Style.RESET_ALL)
            files = {'upload_file': ('grades.csv', open(file_name,'rb'), 'text/csv')}
            response = requests.post('http://127.0.0.1:8000/rest/feedback/', data = {'username':username, 'password':password, 'course_name' : course_name, 'asgn_name' : asgn_name }, files=files)
            print(response.json())
        except Exception as e:
            print("Error-",e)
    if (cmd =='submit_assignment'):
        try:
            files = []
            num_files = int(input('Numer of files to be uploaded- '))
            for i in range(num_files):
                file_name = input('Enter file name- ')
                files.append(('file' ,open(file_name , 'rb') ))

            course_name = input('Enter course name- ')
            asgn_name = input('Enter assignment name- ')
            response = requests.post('http://127.0.0.1:8000/rest/submit_assignment/', data = {'username':username, 'password':password, 'course_name' : course_name, 'asgn_name' : asgn_name }, files=files)
            print(response.json())
        except Exception as e:
            print("Error-",e)
    elif (cmd=='exit'):
        print(Fore.YELLOW+'Terminating'+Style.RESET_ALL)
        break
    else:
        print(Fore.RED +'Failed'+Style.RESET_ALL)
        pass

    
