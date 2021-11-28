import requests
from colorama import init, Fore, Back, Style
import os
from getpass import getpass
init()

HOST = 'http://127.0.0.1:8000'

while True:
    username = input(Fore.YELLOW+'Please Enter Username- ' + Style.RESET_ALL)
    password = getpass(Fore.YELLOW+'Please Enter Password- ' + Style.RESET_ALL)
    response = requests.post(HOST+'/rest/courses/', data = {'username':username, 'password':password})
    if response.status_code == 200:
        break
    else:
        print("Incorrect Credentials, Please try again")

while True:
    cmd = input(Fore.CYAN +'BlueFire ' + Fore.MAGENTA+'$ ' + Style.RESET_ALL)
    if (cmd =='courses'):
        response = requests.post(HOST+'/rest/courses/', data = {'username':username, 'password':password})
        try:
            for i,course in enumerate(response.json()['courses']):
                print(i+1, course)
        except Exception as e:
            print("Error- ", e)
    elif (cmd =='todo'):
        try:
            response = requests.post(HOST+'/rest/todo/', data = {'username':username, 'password':password})
            for i,task in enumerate(response.json()['todo']):
                print(i+1,task)
        except Exception as e:
            print("Error- ", e)
    elif (cmd =='feedback'):
        try:
            file_name = input(Fore.YELLOW+'Enter file name- '+ Style.RESET_ALL)
            course_name = input(Fore.YELLOW+'Enter course name- '+ Style.RESET_ALL)
            asgn_name = input(Fore.YELLOW+'Enter assignment name- '+ Style.RESET_ALL)
            files = {'upload_file': ('grades.csv', open(file_name,'rb'), 'text/csv')}
            response = requests.post(HOST+'/rest/feedback/', data = {'username':username, 'password':password, 'course_name' : course_name, 'asgn_name' : asgn_name }, files=files)
            print(response.json())
        except Exception as e:
            print("Error-",e)
    elif (cmd =='submit_assignment'):
        try:
            files = []
            num_files = int(input(Fore.YELLOW+'Numer of files to be uploaded- '+ Style.RESET_ALL))
            for i in range(num_files):
                file_name = input(Fore.YELLOW+'Enter file name- '+ Style.RESET_ALL)
                files.append(('file' ,open(file_name , 'rb') ))

            course_name = input(Fore.YELLOW+'Enter course name- '+ Style.RESET_ALL)
            asgn_name = input(Fore.YELLOW+'Enter assignment name- '+ Style.RESET_ALL)
            response = requests.post(HOST+'/rest/submit_assignment/', data = {'username':username, 'password':password, 'course_name' : course_name, 'asgn_name' : asgn_name }, files=files)
            print(response.json())
        except Exception as e:
            print("Error-",e)
    elif (cmd =='download_assignment'):
        try:
            course_name = input(Fore.YELLOW+'Enter course name- '+ Style.RESET_ALL)
            asgn_name = input(Fore.YELLOW+'Enter assignment name- '+ Style.RESET_ALL)
            response = requests.post(HOST+'/rest/assignment_download/', data = {'username':username, 'password':'NuSRpTRdUQWDL6m', 'course_name' : course_name, 'asgn_name' : asgn_name })
            if response.status_code == 200:
                with open(""+course_name+"- "+asgn_name+" submissions.zip", 'wb') as file:
                    file.write(response.content)
                print("Success")
                print("Saved as- "+course_name+"- "+asgn_name+" submissions.zip")
            else:
                print("Error- No submissions present or you do not have access")
        except Exception as e:
            print("Error-",e)
    elif (cmd=='exit'):
        print(Fore.YELLOW+'Terminating'+Style.RESET_ALL)
        break
    else:
        print(Fore.RED +'Failed'+Style.RESET_ALL)
        pass

    
