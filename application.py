import os, json

from flask import Flask, session, render_template, redirect, url_for, request, flash, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import requests

from helpers import login_required

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
@login_required
def index():
    """ The search page """
    return render_template("search.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """ Log user in"""
    session.clear()
    if request.method == "POST":
        if not request.form.get('username'):
            return render_template("error.html", error="Username required")
        if not request.form.get('password'):
            return render_template("error.html", error="Password required")

        
        current_user = db.execute("SELECT * from users \
            where username=:username and password=:password", \
            {"username":request.form.get('username'), "password":request.form.get('password')})

        user_info = current_user.fetchone()
        
        if user_info == None:
            return render_template("error.html", error="Wrong username or password")

        session["user_id"] = user_info[0]

        flash('Welcome', 'info')
        return redirect('/')

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Logs user out"""
    session.clear()
    return redirect('/login')


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register users"""
    session.clear()

    if request.method == "POST":
        if not request.form.get('name'):
            return render_template("error.html", error="Name required")
        if not request.form.get('username'):
            return render_template("error.html", error="Username required")
        if not request.form.get('password'):
            return render_template("error.html", error="Password required")
        if not request.form.get('confirm_password'):
            return render_template("error.html", error="Confirm password")

        new_user = db.execute("SELECT * from users where username = :username", 
            {"username":request.form.get("username")}).fetchone()

        if new_user:
            return render_template("error.html", error="Username already taken. Try another")
        
        db.execute("INSERT INTO users (name, username, password) \
            VALUES (:name, :username, :password)", \
            {"name":request.form.get("name"), \
            "username":request.form.get("username"), \
            "password":request.form.get("password")})

        db.commit()

        flash('Account created', 'info')
        return redirect('/login')
    else:
        return render_template("register.html")


@app.route("/search", methods=["GET"])
@login_required
def search():
    """Search a book by title, author or ISBN number"""

    query = '%' + request.args.get("search") + '%'

    books = db.execute("SELECT * FROM books where isbn like :query or title like :query or author like :query limit 10",
        {"query":query}).fetchall()

    return render_template("result.html", books=books)    


@app.route("/book/<string:isbn>", methods=["GET", "POST"])
@login_required
def book(isbn):
    """The Book page"""
    if request.method == "POST":
        curr_user = session["user_id"]

        ratings = request.form.get("ratings")
        comments = request.form.get("comments")

        this_book=db.execute("SELECT id from books where isbn=:isbn", {"isbn":isbn})

        res = this_book.fetchone()
        res = res[0]

        row1 = db.execute("SELECT * from reviews where user_id=:user_id and book_id=:book_id",\
                        {"user_id":curr_user, "book_id":res})

        if row1.rowcount == 1: 
            flash('You already submitted a review', 'warning')
            return redirect("/book/"+isbn)

        db.execute("INSERT INTO reviews (user_id, comments, ratings, book_id) \
            values (:user_id, :comments, :ratings, :book_id)", \
            {"user_id": curr_user, "comments":comments, "ratings":ratings, "book_id":res})
        
        db.commit()

        flash("Review Submitted", 'info')

        return redirect("/book/"+isbn)

    # when book page is accessed from its result page [GET]
    else:
        row = db.execute("SELECT isbn, title, author, year FROM books WHERE isbn = :isbn",
                {"isbn": isbn})
        
        book_info = row.fetchall()

        key = os.getenv("API_KEY")

        query = requests.get("https://www.goodreads.com/book/review_counts.json", \
                params={"key": key, "isbns": isbn})                                                                                                                                                                                                                                                                                                                          

        response = query.json()

        response = response['books'][0]

        book_info.append(response)

        row2 = db.execute("SELECT id from books where isbn=:isbn", {"isbn":isbn})

        book = row2.fetchone()
        book = book[0]

        results = db.execute("SELECT users.username, comments, ratings FROM users INNER JOIN reviews \
                    ON users.id = reviews.user_id \
                    WHERE book_id = :book", \
                    {"book": book})

        reviews = results.fetchall()

        return render_template("books.html", book_info=book_info, reviews=reviews)
 

@app.route("/api/<string:isbn>", methods=["GET"])
@login_required
def api(isbn):
    """"The API request for book info."""
    
    row = db.execute("SELECT title, author, year, isbn, count(r.ratings) as review_count, avg(r.ratings) as average_score \
        from books b inner join reviews r on b.id=r.book_id where isbn=:isbn \
        group by title, author, year, isbn", {"isbn":isbn})

    if row.rowcount != 1:
        return jsonify({"Error": "Invalid Book"}), 404

    res = row.fetchone()

    # copy of res dict
    result = dict(res)

    result['average_score'] = float('%.2f'%(result['average_score']))

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)