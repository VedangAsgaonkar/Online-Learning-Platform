# CS251_GroupProject_3rdSem

Hello and Welcome to our CS251 Project, Moodle by Team BlueFire. Here we will briefly go over the features which our app supports, which we plan to further elaborate on in the demo.

We have the option to Create Courses, wherein the creator is assigned Teacher role directly. He/She can then decide on the access codes for joining the course at various other authority levels. We have the other 2 levels as TA and Student. Also, the power that a TA can have on a course, can be decided at course creation time as well.

Anyone can create announcements in the course and reply to any announcement created. The announcements are displayed in order of creation and the replies are indented properly. Also, the Teacher can choose to disable announcements page, whenever they wish. After this, until resumed, no more announcements/replies can be added.

There is also an option to view the list of Participants in the course according to their authority levels. We have actually implemented a ManyToMany field in django which allows us to seamlessly link between courses and participants.
Several other models give us the strength to model and use the data efficiently.

There are options to change password as well as forgot password, which promptly sends you an email reviving you back from the loss of our beautiful website.

Following the features of review meet 1, you can create assignment in a course with deadline and weightage. Everyone receives a mail for a new assignment as well. The deadlines can be changed by the professor, but the students can only submit before deadline.

Following this is the feature of todo list and percentage of course completed. These give a glance at your performance in the courses from the dashboard itself.

Also, the feedback and marks for courses can be uploaded by a csv file, as well as manually from the website itself.

All data fields are interactive. Any changes in the marks and deadline are reflected throughout the website.

The student can see their marks and grades and the professor can also see the class average and standard deviation in the form of graphs including a box and whisker plot (credits CS215)

A poorly performing student is well reminded of his performance on the grades page, as demanded

Apart from announcements, teachers can add course content and embed links in to our website. Thus we enter the world of embedded videos, forms and interactive links. Much like the moodle we all know and love.

There are also options to change some of one's entries via the Settings page, and a brief summary of profile can be accessed by, you guessed it, the Profile button (and also by the profile icon you see on the top right)

The changeable settings include password, email and institution.

Finally we also have the options to chat with anyone on the website, with a familiar GUI experience. These are also available in an intuitive manner on the website

In the end, our website boasts the evergreen CLI support as well. A single python script seemingly launches you into a new terminal, where you can use some simple arguments to view the list of courses, your todo list, upload your assignments, feedback etc. For teachers, there is also option upload csv file for grading an assignment as well.

These highlight the main features of our website, there are some minor features we have not mentioned here, best to keep it for the viva.

We invite you to experience our creation.

Have Fun \
Signing off

Arpon Basu\
Prathamesh Sachin Pilkhane\
Shashwat Garg\
Vedang Dhirendra Asgaonkar
