# Book Reviewer

The website has a **_register page_** for new users to register, a **_login page_** to log into their sessions and make reviews and rate books. The site uses goodreads-api to get information about information about the books.

## Files hierarchy

`application.py` contains the main backend of the site. 
`helpers.py` contains the **login_required** function to facilitate required logins. 
`import.py` contains function to import the books in **book.csv** to the **books** database.

**`/static`** contains the css file and the images used.

**`/templates`** contains the html pages used. **layout.html** is the basic template which is extended on all other pages.

**`/venv`** is the virtual environment file containing the required libraries and environments used in the website.

`setenv.sh` is a bash script used to set environment during development.

## Usage

- Go to the [website](https://limitless-journey-50511.herokuapp.com/) 
- Register
- Login 
- Search Books
- Open a book page to rate them and write a review.
- Use the api feature request the information of books in JSON format.

## Installation 

To use and modify this app in your local environment:

```
# Clone repo
$ git clone https://github.com/sachinkumarsingh092/book-reviewer.git

$ cd book-reviewer

# Create a virtualenv (Optional but reccomended)
$ python3 -m venv myvirtualenv

# Activate the virtualenv
On Linux and macOS:
$ source myvirtualenv/bin/activate 

On Windows:
.\myvirtualenv\Scripts\activate

# Install all dependencies
$ pip3 install -r requirements.txt

# Environment Variables
$ export FLASK_APP = application.py 
$ export FLASK_DEBUG = 1
$ export DATABASE_URL = Heroku_Postgres_URI
$ export API_KEY = Goodreads API Key. # More info: https://www.goodreads.com/api

or 

. ./setenv.sh

```

