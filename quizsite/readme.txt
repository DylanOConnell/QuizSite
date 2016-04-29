Dylan O'Connell Quizsite Readme, Updated 04/29/2016
Submitted in fulfillment of the CS306 Final Project 

This readme is intended to help any reader understand the structure and organization of the website as well as its files. 
We will discuss 1. the flow of the website, and how each page is used, and 2. the organization of its files.

=================================================
1. The structure of the Django models/SQL Database.

We begin with a brief overview of the models which form the backbone of the database. The models
are contained in quizcreator/models.py. For details about this structure, view the comments and 
docstrings in that document.

Each quiz is represented by a Quiz object, which has a name. Each Question object  has a text attribute, for the
text of the question. Quiz and Question objects have a many-to-many relationship using a through table, QuestionOrdering (which stores a
numerical value, ordering', for each quiz+question combo). The m2m relationship is used so that instructors do not need to repeat themselves
 as they build many quizzes, as good questions may be relevant in many quizzes. QuestionOrdering is necessary because we must keep 
track of a unique ordering for questions for each quiz.

We use the built in Django user system. Each user can begin a quiz attempt, which is stored as a QuizResult object, which tracks whether the attempt
is 'finished'. As they take the quiz, they submit AnswerResult objects for each answer to each question, which stores whether the user selected that 
answer. Thus, the entire quiz attempt is represented by one QuizResult, and an AnswerResult for every possible question. Once the user has completed the
quiz, we set QuizResult finished to be true, and they are scored based on their AnswerResult.

There are also BugReport objects, which can be submitted by users, which store text relating to any bug that they found in the website.
Users can have superuser privileges, which are necessary to 1. see QuizResults 2. add Quizzes, Questions, or Answers, and 3. view submitted
bug report forms.

=================================================
2. The structure of the website.
Each page will list its name, URL, and full description.
Each page extends "base.html", which offers links to 'home', and 'login' if they are not logged in,
and 'logout' if they are logged in.

a. home, URL = /, 
The homepage gathers links to navigate the site. 
Guests see links to 'login' and 'register'. They also see the link to the list of quizzes,
so they can see what is available. However, they cannot begin a quiz until they are logged in.
Logged in users see 'logout' instead, and all see 'submit a bug report'.

If the page detects that you are a superuser, it also displays the 'superuser tools' section. This
allows for the creation of new quizzes, questions, and answers, a link to the 'checkresults' page, and
a link to 'checkbugreports', to view previous bug reports.

The user can always click the 'home' link in the header to get back to this page, and this allows them to quickly and effectively 
navigate the website.

b. quizzes, URL = /quizzes/,
This page can be viewed by anyone, and lists all available quizzes. Each quiz provides a link to the 'beginquiz' page 
for that quiz.:w

c. beginquiz, URL = /quizzes/quiz_id/beginquiz
If the user is not logged in, this page just displays a link to the first question of the quiz.
If the user is logged in, it will also display a "Begin Quiz" button. This submits a modelform of a QuizResult to this page,
which allows the user to begin a quiz attempt. The page processes the form, and ensures that the information is correct.

d. question, URL = /quizzes/quiz_id/qustion_id
This page displays a question and its answers, and allows for user input. It displays an AnswerResult formset which allows
for the submission of an AnswerResult for each Answer at once. For each Answer, it displays that Answer text, followed by a checkbox
for whether the user selects that answer. When the user presses submit, the entire answer formset (containing a boolean for each answer
depending on if  they selected it) is submitted, to the submitanswer page.


e. submitanswer, URL = /quizzes/quiz_id/question_id/submitanswer
This page processes a POST request from the question page. It takes in an AnswerResult formset, and examines each AnswerResult in turn.
It validates the data in the form, and if it correct, it saves the data. If that user has already submitted answers to that question, but
they have not yet finished the quiz attempt, it deletes the old answer and replaces it with a new one. Once the QuizResult is finished, this 
is prevented. If the answers are successfully submitted, then it redirects the user to the next question in this quiz. If there is no next
question, it redirects the user to the endofquiz page.

f. endofquiz, URL = /quizzes/quiz_id/endofquiz
If the user is logged in, this provides them with two options. If they would like to continue taking the quiz, and further update their answers,
they can follow the link to the beginning of the quiz. If they are done, they can submit this quizresult, which follows the link to finishquiz.

g. finishquiz, URL = /quizzes/quiz_id/finishquiz
This page attempts to 'finish' the given quiz for the current user. It checks that the user is logged in, and then checks that there is exactly one
QuizResult for this quiz and user which is not yet finished (otherwise, it throws an error). Then, it verifies that the user has submitted one 
AnswerResult for every question in the quiz. If they have not, they are told which answer has not yet been submitted. If there is no issue, then QuizResult
is set to finished, and the user has completed the Quiz.

A regular user cannot view the results of their quiz, and they are just redirected to the home page. This is because if a class is taking
the same quiz, the professor may not want to reveal the correct answers until all testtakers are complete.
When the user submits the quiz successfully, they are redirected to the submittedquiz page, which explains this to them.

h. listquizresults, URL = quizzes/listquizresults
This page is for superusers only. It displays a list of links, which link to the checkresults page for each quiz. 

i. checkresults, URL = quizzes/quiz_id/checkresults
This page is for superusers only. For a given quiz, it displays a list of all users who have completed this quiz. It provides a 
link to the quizresults page for each valid combination of user and quiz.

j. quizresults, URL = quizzes/username/quiz_id/checkresults
This page allows a superuser to view the results for a given user and quiz. It can only be viewed if that user has submitted that quiz.
This is the first time the score for a quiz is calculated. The scoring works as follows. For each question, the user gets 1 point for a selected 
correct answer, then they only get half of those total points if they select a partially wrong answer, and they get 0 points if they select a fully
wrong answer. Thus, they get 0 if any fully wrong answers, and get (num_correct)*(1/2)^(num_partially_correct) points per question if they don't get 
any fully wrong.

This page displays a full set of results so that the instructor can easily check. For each question, it displays its text, then a table of the 
answer text, whether the user selected it, and whether the answer was correct. It then displays the final user score at the bottom of the quiz.

k. submittedquiz, URL = quizzes/quiz_id/submittedquiz
This page tells the user that they have successfully submitted a quiz, and that they will find out their score
when contacted by the instructor.

l. addquestion, url = quizzes/addquestion
Only for superusers, this form displays three forms, addquiz, addquestion, addanswer. Submitting an addquestion form sends
the result as a POST request to this page, which also processes the request, and adds the question to the system. Submitting
an addquiz or addanswer form sends those POST requests to their respective pages for processing. If a form is submitted successfully,
the superuser is redirected back to this page to add more objects to the database.

m. addanswer, url = quizzes/addanswer
This processes an addanswer form from addquestion, and adds the result (if validated) to the database.

m. addquiz, url = quizzes/quiz
This processes an addquiz form from addquestion, and adds the result (if validated) to the database.

n. register, url = account/register
This page handles user registration, using the tools provided by Django. Registration just requires a username
and password.

o. bugreport, url = quizzes/bugreport
To a POST request, this page will process a bugreportform, and add it to the database if it is validated. Otherwise,
it displays a bugreport form, which can only be submitted if a user is logged in.

p. viewbugreports, url = quizzes/viewbugreports
Only for a superuser, this allows the superuser to view a list of all previously submitted bugreports.
