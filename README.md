# MS-UnconsciousBiasDetection

# README

## Introduction

Our application is a system that will take in a syllabi and return a score based on ML analysis.
The front end is set up and works, where a user enters in their syllabi and a bias score is
determined.

## Requirements

This code has been run and tested on:

- Python 3.9.6
- virtualenv

## External Deps

- Git - Downloat latest version at https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
- GitHub Desktop (Not needed, but HELPFUL) at https://desktop.github.com/

## Installation

Download this code repository by using git:

`git clone https://github.com/seungjeh39/MS-UnconsciousBiasDetection.git`

## Virtual Environment setup

Make sure that virutalenv is installed before beginning running code.
This can be done by the command: 'pip3 install virtualenv'.
A virtual env has been created and to activate, run the command 'source env/bin/activate'.
If in Windows, run '.\env\Scripts\activate' (in cmd).
to install all of the necessary dependencies and packages, run 'pip3 install -r requirements.txt'.
To view the dependencies and packages, run pip3 list.
The requirements.txt file has all of the necessary libraries and dependencies.

run deactivate to get out of virtual environment.

## Execute Code

The app.py file is the main file that will run all of the proper dependencies
as well as the front end.

To get app.py to run, simply navigate to the home directory (can check by using "pwd"),
and then run "python3 app.py" (or "python app.py" depending on your machine). Finally,
click on hyperlink http://127.0.0.1:5010/ in order to open the system in a web browser.  

## Deployment

We are planning on deploying to Heroku so that anyone can be able to view and use our
system. However, we feel as if it is not of the highest priority as of right now, and
we are focusing more on developing models and getting the system working locally.

After running app.py, go to http://127.0.0.1:5010/ to view the system.