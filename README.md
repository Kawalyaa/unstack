
[![Build Status](https://travis-ci.org/Kawalyaa/unstack.svg?branch=development_perfect)](https://travis-ci.org/Kawalyaa/unstack)  [![Coverage Status](https://coveralls.io/repos/github/Kawalyaa/unstack/badge.svg?branch=feature)](https://coveralls.io/github/Kawalyaa/unstack?branch=feature)  [![Maintainability](https://api.codeclimate.com/v1/badges/2bfcb5ec433449bbc047/maintainability)](https://codeclimate.com/github/Kawalyaa/unstack/maintainability)

# UNSTACK

Unstack is a platform which enables people to ask question and get answers


The api docs for the app are found [here](https://unstack.herokuapp.com/apidocs/#/)

## Built with

* python 3
* flask

## Features

  1. User can create an account and login
  1. User can post questions
  1. user can delete questions they post
  1. User can post answers
  1. Users can view answers to the questions
  1. Question owner can make answer user user_preferred

## Installing

Step 1

### Clone this repository

```
$ git clone https://github.com/Kawalyaa/ustack.git

$ cd unstack

```

Create and activate the virtual environment

```
$ python3 -m venv venv

$ source venv/bin/activate

```

Install project dependencies

```
pip install -r requirements.txt

```

Step 2

### Setup Databases

Go to postgres terminal and do the following

Main Database

```
# CREATE DATABASE database_name ;
```

Testing Database

```
# CREATE DATABASE test_database ;
```

Step 3

### Storing the environmental variables

```
export FLASK_APP="run.py"
export FLASK_ENV="development"
export DATABASE_URL="your database url"
export DATABASE_TEST_URL="your database url for testing"
export SECRETE="your secrete key"
```

step 4

### Running the application

```
$ flask run
```

Step 5

### Testing the application

```
$ nosetests app/tests
```

## API-ENDPOINTS

 Method | Endpoints | Functionality
 ------ | --------- | -------------
 POST | /api/v2/auth/signup | creat User account
 POST | /api/v2/auth/login | A user can login
 POST | /api/v2/auth/logout | A user can logout
 |      |         Questions endpoints       |
 POST | /api/v2/question | A user can post question
 GET | /api/v2/question | A user can view all the questions
 GET | /api/v2/question/<int:question_id> | A user can view a single question
 GET | /api/v2/question/plus/answers/<int:question_id> | A user can get question with answer
 GET | /api/v2/question/most_answered | A user can get most answered question
 GET | /api/v2/question/<user_name> | A user can get a question by username
 PUT | api/v2/question/<int:question_id> | A user can edit a question
 DELETE | api/v2/question/<int:question_id> | A user can delete a question
 DELETE | /api/v2/question/answer/<int:question_id> | A user can delete a question and its answer
 |      |             Answers Endpoint                    |
 POST | /api/v2/answers/<int:question_id> | A user can post Answers
 PUT | /api/v2/question/<int:question_id>/answers/<int:answer_id> | A user can edit or make answer user_preferred
 PUT | /api/v2/question/<int:question_id>/answers/<int:answer_id>/vote | A user can vote for answer

## Author

*[KAWALYA ANDREW](https://github.com/Kawalyaa)*
