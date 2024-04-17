from flask import Blueprint, request, send_file
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_security import login_user, auth_token_required, roles_required, logout_user
import re
from .models import db
from datetime import datetime, timedelta
import os
# Database Imports
from .models import Section, Book, Author, AuthorBookMap, BookRequest, User, BookIssue, Review

# Celery Imports
from celery.result import AsyncResult

# file related imports for export job
import io

# Blueprint Configuration
view = Blueprint("view", __name__)

# cache imports
from .cache import cache


# Routes


"""
sign up into the system
"""
@view.route("/signup", methods=["POST"])
def register_new_user():
    fname = request.json.get("fname")
    lname = request.json.get("lname")
    uname = request.json.get("uname")
    email = request.json.get("email")
    passwd = request.json.get("pass")
    cpass = request.json.get("passconf")

    if not fname:
        return {"error": "First name is required"}, 400
    if not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', email):
        return {"error": "Invalid email address"}, 400
    if passwd != cpass:
        return {"error": "Passwords do not match"}, 400
    if app.security.datastore.find_user(email=email):
        return {"error": "Email already exists"}, 400
    if app.security.datastore.find_user(uname=uname):
        return {"error": "Username already exists"}, 400
    
    user = app.security.datastore.create_user(
        fname = fname,
        lname = lname,
        uname = uname,
        email = email,
        password = generate_password_hash(passwd),
    )
    role = app.security.datastore.find_role("user")
    app.security.datastore.add_role_to_user(user, role)

    db.session.commit()

    print(request.json)
    return {"status": "success"}, 201

"""
sign in into an existing account
"""
@view.route("/signin", methods=["POST"])
def user_login():
    uname = request.json.get("uname")
    passwd = request.json.get("pass")

    user = app.security.datastore.find_user(uname=uname)
    
    if not user:
        return {"error": "User not found"}, 404
    if not check_password_hash(user.password, passwd):
        return {"error": "Invalid credentials"}, 401

    login_user(user)
    token = user.get_auth_token()
    roles = [role.name for role in user.roles]
    update_login_time = User.query.get(user.id)
    update_login_time.last_active = datetime.now()
    db.session.commit()

    return {"status": "success",
            "token" : token,
            "roles" : roles,
            "name": uname,
            "id" : user.id
            }, 200



"""
signout
"""
@view.route("/signout", methods=["POST"])
@auth_token_required
def user_logout():
    logout_user()
    return {"status": "success"}, 200



"""
Create a new section
"""
@view.route("/admin/section/create", methods=["POST"])
@roles_required("admin")
@auth_token_required
def createSection():
    name = request.json.get("sectionName")
    desc = request.json.get("sectionDesc")

    if not name:
        return {"error": "Section name is required"}, 400
    if len(name) < 3:
        return {"error": "Section name is too short"}, 400

    section = Section(name=name, description=desc, date_created=datetime.now())
    db.session.add(section)
    db.session.commit()

    return {"status": "success"}, 201


"""
Get List of available sections
"""
@view.route("/admin/section/getList", methods=["GET"])
@roles_required("admin")
@auth_token_required
def getSections():
    sections = Section.query.all()
    result = []

    for section in sections:
        result.append({
            "id": section.id,
            "name": section.name,
            "description": section.description,
            "date_created": section.date_created
        })
    return result

"""
Delete an existing section
"""
@view.route("/admin/section/delete/<int:sectionID>", methods=["DELETE"])
@roles_required("admin")
@auth_token_required
def deleteSection(sectionID):
    section = Section.query.get(sectionID)
    if not section:
        return {"error": "Section not found"}, 404

    db.session.delete(section)
    db.session.commit()

    return {"status": "success"}, 200


"""
Update an existing section
"""
@view.route("/admin/section/update/<int:sectionID>", methods=["PUT"])
@roles_required("admin")
@auth_token_required
def updateSection(sectionID):
    print("This section is being execited")
    section = Section.query.get(sectionID)
    if not section:
        return {"error": "Section not found"}, 404

    name = request.json.get("sectionName")
    desc = request.json.get("sectionDesc")

    if not name:
        return {"error": "Section name is required"}, 400
    if len(name) < 3:
        return {"error": "Section name is too short"}, 400

    section.name = name
    section.description = desc

    db.session.commit()

    return {"status": "success"}, 200


"""
Create a new book
"""
@view.route("/admin/book/create", methods=["POST"])
@roles_required("admin")
@auth_token_required
def createBook():

    title = request.form.get("title")
    desc = request.form.get("description")
    authorFirstName = request.form.get("authorFirstName") or ""
    authorLastName = request.form.get("authorLastName") or ""
    sectionID = request.form.get("section")
    bookCover = request.files.get("bookCover")
    bookFile = request.files.get("bookFile")

    if(len(title) < 3):
        return {"error": "Title is too short"}, 400
    if(authorFirstName == ""):
        return {"error": "Author first name is required"}, 400
    if bookCover == None:
        return {"error": "Book cover is required"}, 400
    if bookFile == None:
        return {"error": "Book file is required"}, 400

    

    if (Author.query.filter_by(fname=authorFirstName, lname=authorLastName).first() == None):
        author = Author(fname=authorFirstName, lname=authorLastName)
        db.session.add(author)
        db.session.flush()

    authorID = Author.query.filter_by(fname=authorFirstName, lname=authorLastName).first().id


    book = Book(title = title, 
                description = desc, 
                # cover_path = "static/covers/" + bookCover.filename, 
                date_added = datetime.now(), 
                section_id = sectionID, 
                # content_path = "static/books/" + bookFile.filename, 
                publication_date = datetime.now(), 
                last_issued = datetime.now()
                )
    db.session.add(book)
    db.session.flush()

    book.cover_path = f"{book.id}_{secure_filename(bookCover.filename)}"
    book.content_path = f"{book.id}_{secure_filename(bookFile.filename)}"

    bookCover.save(os.path.join("static/covers", book.cover_path))
    bookFile.save(os.path.join("static/books", book.content_path))


    authorBookMap = AuthorBookMap(author_id = authorID, book_id = book.id)
    db.session.add(authorBookMap)

    db.session.commit()
    return {"status": "success"}, 201


"""
get list of books
"""
@view.route("/admin/book/getList", methods=["GET"])
@roles_required("admin")
@auth_token_required
def getBooks():
    books = Book.query.all()
    result = []

    for book in books:
        result.append({
            "id": book.id,
            "title": book.title,
            "description": book.description,
            "cover_path": book.cover_path,
            "date_added": book.date_added,
            "section_id": book.section_id,
            "content_path": book.content_path,
            "publication_date": book.publication_date,
            "last_issued": book.last_issued
        })
    print(result)
    for book in result:
        authorID = AuthorBookMap.query.filter_by(book_id=book["id"]).first().author_id
        author = Author.query.get(authorID)
        book["author"] = author.fname + " " + author.lname
        book["author_fname"] = author.fname
        book["author_lname"] = author.lname
    print(result)
    return result



"""
Delete a book entry
"""
@view.route("/admin/book/delete/<int:bookID>", methods=["DELETE"])
@roles_required("admin")
@auth_token_required
def deleteBook(bookID):
    book = Book.query.get(bookID)
    authorBookMap = AuthorBookMap.query.filter_by(book_id=bookID).first()
    if not book:
        return {"error": "Book not found"}, 404

    db.session.delete(book)
    db.session.delete(authorBookMap)
    db.session.commit()

    return {"status": "success"}, 200



"""
Update a book entry
"""
@view.route("/admin/book/update/<int:bookID>", methods=["PUT"])
@roles_required("admin")
@auth_token_required
def updateBook(bookID):
    book = Book.query.get(bookID)
    authorID = AuthorBookMap.query.filter_by(book_id=bookID).first().author_id
    author  = Author.query.get(authorID)
    if not book:
        return {"error": "Book not found"}, 404

    title = request.form.get("title")
    desc = request.form.get("description")
    authorFirstName = request.form.get("authorFirstName")
    authorLastName = request.form.get("authorLastName")
    sectionID = request.form.get("section")
    bookCover = request.files.get("bookCover")
    bookFile = request.files.get("bookFile")

    if(len(title) < 3):
        return {"error": "Title is too short"}, 400
    if(authorFirstName == ""):
        return {"error": "Author first name is required"}, 400

    author.fname = authorFirstName
    author.lname = authorLastName

    if book.title != title:
        book.title = title
    if book.description != desc:
        book.description = desc
    if book.section_id != sectionID:
        book.section_id = sectionID

    if bookCover:
        # print("old cover path: ", book.cover_path)
        os.remove(os.path.join("static/covers", book.cover_path))
        book.cover_path = f"{book.id}_{secure_filename(bookCover.filename)}"
        bookCover.save(os.path.join("static/covers", book.cover_path))
        # print("new cover path: ", book.cover_path)
    if bookFile:
        os.remove(os.path.join("static/books", book.content_path))
        book.content_path = f"{book.id}_{secure_filename(bookFile.filename)}"
        bookFile.save(os.path.join("static/books", book.content_path))
        

    db.session.commit()

    return {"status": "success"}, 200



"""
Get list of book requests from all users
"""
@view.route("/admin/book/request/getList", methods=["GET"])
@roles_required("admin")
@auth_token_required
def getBookRequests():
    bookRequests = BookRequest.query.all()
    result = []

    for bookRequest in bookRequests:
        userName = User.query.get(bookRequest.user_id).uname
        bookTitle = Book.query.get(bookRequest.book_id).title
        result.append({
            "id": bookRequest.id,
            "bookTitle": bookTitle,
            "userName": userName,
            "request_date": bookRequest.request_date,
            "request_duration": bookRequest.request_duration,
            "request_status": bookRequest.request_status
        })

    return result


"""
Process a book request as approved or rejected
"""
@view.route("/admin/book/request/process/<int:requestID>", methods=["POST"])
@roles_required("admin")
@auth_token_required
def processRequest(requestID):
    status = request.json.get("status")
    bookRequest = BookRequest.query.get(requestID)
    if not bookRequest:
        return {"error": "Request not found"}, 404
    
    book_id = bookRequest.book_id
    user_id = bookRequest.user_id
    date_issues = datetime.now()
    date_due = date_issues + timedelta(seconds=bookRequest.request_duration)
    print("Date due", date_due)
    print("Date issues", date_issues)


    if status == "approved":

        bookIssue = BookIssue(
                              book_request_id=requestID, 
                              book_id=book_id, 
                              user_id=user_id, 
                              date_issues=date_issues, 
                              issue_expiry_date=date_due, 
                              issue_status="issued")
        db.session.add(bookIssue)

    if status == "rejected":
        user = User.query.get(user_id)
        user.active_requests_count -= 1

    bookRequest.request_status = status
    db.session.commit()

    return {"status": "success"}, 200


"""
Get list of issued books to various users
"""
@view.route("/admin/book/issue/getList", methods=["GET"])
@roles_required("admin")
@auth_token_required
def getBookIssues():
    bookIssues = BookIssue.query.all()
    result = []

    for bookIssue in bookIssues:
        userName = User.query.get(bookIssue.user_id).uname
        bookTitle = Book.query.get(bookIssue.book_id).title
        result.append({
            "id": bookIssue.id,
            "bookTitle": bookTitle,
            "userName": userName,
            "issue_date": bookIssue.date_issues,
            "expiry_date": bookIssue.issue_expiry_date,
            "return_date": bookIssue.return_date,
            "issue_status": bookIssue.issue_status
        })

    return result


"""
Get all reviews by all users
"""
@view.route("/admin/getreviews")
@roles_required("admin")
@auth_token_required
def getReviews():
    reviews = Review.query.all()
    result = []

    for review in reviews:
        userName = User.query.get(review.user_id).uname
        bookTitle = Book.query.get(review.book_id).title
        result.append({
            "id": review.id,
            "book_title": bookTitle,
            "userName": userName,
            "review_date": review.review_date,
            "review_title": review.review_title,
            "review_desc": review.review_desc,
            "rating": review.rating
        })

    return result

"""
Get admin statistics for the dashboard
"""
@view.route("/admin/dashboard/get_data")
# @roles_required("admin")
# @auth_token_required
@cache.cached(10)
def AdminDashboardData():

    book_count_by_section = {}
    for section in Section.query.all():
        book_count_by_section[section.name] = len(Book.query.filter_by(section_id=section.id).all())
    
    top_requested_books = {}
    for bookRequest in BookRequest.query.all():
        book = Book.query.get(bookRequest.book_id)
        if book.title in top_requested_books:
            top_requested_books[book.title] += 1
        else:
            top_requested_books[book.title] = 1
    # only take the top 5 books from the dictionary
    top_requested_books = dict(sorted(top_requested_books.items(), key=lambda item: item[1], reverse=True)[:5])

    top_rated_books = {}
    for review in Review.query.all():
        book = Book.query.get(review.book_id)
        if book.title in top_rated_books:
            top_rated_books[book.title].append(review.rating)
        else:
            top_rated_books[book.title] = [review.rating]
    # calculate the average rating for each book
    for key in top_rated_books:
        top_rated_books[key] = sum(top_rated_books[key]) / len(top_rated_books[key])
    # only take the top 5 books from the dictionary
    top_rated_books = dict(sorted(top_rated_books.items(), key=lambda item: item[1], reverse=True)[:5])


    section_counts = {}
    for key in book_count_by_section:
        section_counts["books"] = list(book_count_by_section.keys())
        section_counts["counts"] = list(book_count_by_section.values())
    
    top_requested_books_data = {}
    for key in top_requested_books:
        top_requested_books_data["books"] = list(top_requested_books.keys())
        top_requested_books_data["counts"] = list(top_requested_books.values())

    top_rated_books_data = {}
    for key in top_rated_books:
        top_rated_books_data["books"] = list(top_rated_books.keys())
        top_rated_books_data["rating"] = list(top_rated_books.values())

    total_requests = len(BookRequest.query.all())
    total_issues = len(BookIssue.query.all())
    overdue_issues = len(BookIssue.query.filter(BookIssue.issue_expiry_date < datetime.now()).all())

    result = [
        {"book_count_by_section": section_counts},
        {"top_requested_books": top_requested_books_data},
        {"top_rated_books": top_rated_books_data},
        {"total_requests": total_requests},
        {"total_issues": total_issues},
        {"overdue_issues": overdue_issues}
    ]

    return result




# ======================== User Routes ========================
"""
Get User Details
"""
@view.route("/user/get/<int:userID>", methods=["GET"])
@auth_token_required
def getUser(userID):
    user = User.query.get(userID)
    if not user:
        return {"error": "User not found"}, 404
    
    result = {
        "id": user.id,
        "fname": user.fname,
        "lname": user.lname,
        "uname": user.uname,
        "email": user.email,
        "active_requests_count": user.active_requests_count,
        "last_active": user.last_active
    }

    return result


"""
Update User Details
"""
@view.route("/user/update", methods=["PUT"])
@auth_token_required
def updateUser():
    userID = request.json.get("userID")
    user = User.query.get(userID)
    if not user:
        return {"error": "User not found"}, 404

    fname = request.json.get("fname")
    lname = request.json.get("lname")
    email = request.json.get("email")
    passwd = request.json.get("pass")
    cpass = request.json.get("passconf")

    if not fname:
        return {"error": "First name is required"}, 400
    if not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', email):
        return {"error": "Invalid email address"}, 400
    if passwd != cpass:
        return {"error": "Passwords do not match"}, 400

    user.fname = fname
    user.lname = lname
    user.email = email
    user.password = generate_password_hash(passwd)

    db.session.commit()

    return {"status": "success"}, 200


"""
Get list of all books available to the user
"""
@view.route("/book/getList", methods=["GET"])
# @roles_required("admin")
@auth_token_required
def getBooksClient():
    books = Book.query.all()
    result = []

    for book in books:
        result.append({
            "id": book.id,
            "title": book.title,
            "description": book.description,
            "cover_path": book.cover_path,
            "date_added": book.date_added,
            "section_id": book.section_id,
            "content_path": book.content_path,
            "publication_date": book.publication_date,
            "last_issued": book.last_issued
        })
    for book in result:
        authorID = AuthorBookMap.query.filter_by(book_id=book["id"]).first().author_id
        author = Author.query.get(authorID)
        book["author"] = author.fname + " " + author.lname
        book["author_fname"] = author.fname
        book["author_lname"] = author.lname
        book["section"] = Section.query.get(book["section_id"]).name
    # print(result)
    return result 



"""
Get Details of one book through book ID
"""
@view.route("/book/get/<int:bookID>", methods=["GET"])
@auth_token_required
def getBookClient(bookID):
    book = Book.query.get(bookID)
    if not book:
        return {"error": "Book not found"}, 404
    
    authorID = AuthorBookMap.query.filter_by(book_id=bookID).first().author_id
    author = Author.query.get(authorID)
    result = {
        "id": book.id,
        "title": book.title,
        "description": book.description,
        "cover_path": book.cover_path,
        "date_added": book.date_added,
        "section_id": book.section_id,
        "content_path": book.content_path,
        "publication_date": book.publication_date,
        "last_issued": book.last_issued,
        "author": author.fname + " " + author.lname,
        "author_fname": author.fname,
        "author_lname": author.lname,
        "section": Section.query.get(book.section_id).name
    }
    return result



"""
Request a book
"""
@view.route("/book/request", methods=["POST"])
@auth_token_required
def requestBook():
    # print("The function has been called")
    bookID = request.json.get("bookID")
    userID = request.json.get("userID")
    # print("UserID: ", userID)
    time = request.json.get("time")
    # print("time: ", time)

    # increment active_requests in user table
    user = User.query.get(userID)
    user.active_requests_count += 1

    def inSeconds(time):
        seconds = 0
        seconds += int(time["days"]) * 86400
        seconds += int(time["hours"]) * 3600
        seconds += int(time["minutes"]) * 60
        return seconds

    book = Book.query.get(bookID)
    if not book:
        return {"error": "Book not found"}, 404
    
    if(BookRequest.query.filter_by(book_id=bookID, user_id=userID, request_status="pending").first()):
        return {"error": "Book already requested"}, 400
    if(BookRequest.query.filter_by(book_id=bookID, user_id=userID, request_status="approved").first()):
        return {"error": "Book already issued"}, 400
    if(user.active_requests_count > 5):
        return {"error": "Maximum requests reached"}, 400

    bookRequest = BookRequest(book_id=bookID, user_id=userID, request_date=datetime.now(), request_duration=inSeconds(time), request_status="pending");
    db.session.add(bookRequest)
    db.session.commit()

    return {"status": "success"}, 201


"""
List of book requests by the user
"""
@view.route("/myrequests", methods=["POST"])
@auth_token_required
@cache.cached(5)
def myRequests():
    userID = request.json.get("userID")
    bookRequests = BookRequest.query.filter_by(user_id=userID).all()
    result = []

    for bookRequest in bookRequests:
        book = Book.query.get(bookRequest.book_id)
        result.append({
            "id": book.id,
            "title": book.title,
            "description": book.description,
            "request_date": bookRequest.request_date,
            "request_duration": bookRequest.request_duration,
            "request_status": bookRequest.request_status
        })
    print("Non cached call")
    return result


"""
List of book issued to the user
"""
@view.route("/mybooks", methods=["POST"])
@auth_token_required
def myBooks():
    userID = request.json.get("userID")
    bookIssues = BookIssue.query.filter_by(user_id=userID).all()
    result = []

    for bookIssue in bookIssues:
        book = Book.query.get(bookIssue.book_id)
        result.append({
            "id": book.id,
            "book_issue_id": bookIssue.id,
            "title": book.title,
            "description": book.description,
            "cover_path": book.cover_path,
            "content_path": book.content_path,
            "issue_date": bookIssue.date_issues,
            "expiry_date": bookIssue.issue_expiry_date,
            "issue_status": bookIssue.issue_status
        })
    # print(result)
    return result

"""
Review a book through the user
"""
@view.route("/book/review/<int:userID>", methods=["POST"])
@auth_token_required
def submitBookReview(userID):
    bookID = request.json.get("bookID")
    reviewTitle = request.json.get("reviewTitle")
    reviewDesc = request.json.get("reviewDesc")
    reviewScore = request.json.get("reviewScore")

    book = Book.query.get(bookID)
    if not book:
        return {"error": "Book not found"}, 404
    
    if(Review.query.filter_by(book_id=bookID, user_id=userID).first()):
        return {"error": "Review already submitted"}, 400

    
    review = Review(book_id=bookID, user_id=userID, review_date=datetime.now(), review_title=reviewTitle, review_desc=reviewDesc, rating=reviewScore)
    db.session.add(review)
    db.session.commit()

    return {"status": "success"}, 201


"""
Get the list of reviews for a book
"""
@view.route("/book/reviews/<int:bookID>", methods=["GET"])
@auth_token_required
def getBookReviewsByBook(bookID):
    # reviews = Review.query.filter_by(book_id=bookID).all()
    book = Book.query.get(bookID)
    if not book:
        return {"error": "Book not found"}, 404
    
    # using relationship is so cool!
    reviews = book.reviews
    
    result = []

    for review in reviews:
        user = User.query.get(review.user_id)
        result.append({
            "id": review.id,
            "user": user.uname,
            "review_date": review.review_date,
            "review_title": review.review_title,
            "review_desc": review.review_desc,
            "rating": review.rating
        })
    # print(result)
    return result


"""
Get the list of reviews by a user
"""
@view.route("/book/reviews/user/<int:userID>", methods=["GET"])
@auth_token_required
def getBookReviewsByUser(userID):
    user = User.query.get(userID)

    reviews = user.reviews
    result = []

    for review in reviews:
        book = Book.query.get(review.book_id)
        result.append({
            "id": review.id,
            "book_title": book.title,
            "review_date": review.review_date,
            "review_title": review.review_title,
            "review_desc": review.review_desc,
            "rating": review.rating
        })
    return result


# ======================== Common Routes ========================

"""
Delete a review by the user, can also be done by admin
"""
@view.route("/book/review/delete/<int:reviewID>", methods=["DELETE"])
@auth_token_required
def deleteBookReview(reviewID):
    review = Review.query.get(reviewID)

    if not review:
        return {"error": "Review not found"}, 404

    db.session.delete(review)
    db.session.commit()

    return {"status": "success"}, 200


"""
Return a book by the user
"""
@view.route("/book/return/<int:userid>", methods=["POST"])
@auth_token_required
def returnBook(userid):
    bookIssueID = request.json.get("bookIssueID")
    bookIssue = BookIssue.query.get(bookIssueID)
    bookrequest = BookRequest.query.filter_by(id=bookIssue.book_request_id).first()
    if not bookIssue:
        return {"error": "Book Issue not found"}, 404
    
    user = User.query.get(userid)

    isUserAdmin = "admin" in [role.name for role in user.roles]

    if (bookIssue.user_id == userid or isUserAdmin):
        bookIssue.issue_status = "returned"
        bookrequest.request_status = "returned"
        bookIssue.return_date = datetime.now()
        user.active_requests_count -= 1
        db.session.commit()
    else:
        return {"error": "Unauthorized"}, 401

    return {"status": "success"}, 200


# from .worker import hello

# @view.route("/check")
# def check():
#     task = request.args.get("task")


#     if task:
#         result = AsyncResult(task)
#         return result.result 
#     else:
#         result = hello()
#         return result


# worker imports
from .worker import export_user_data, export_books_data


@view.route("/export/users")
@roles_required("admin")
@auth_token_required
def exportUserData():
    task = request.args.get("task")

    if not task:
        result = export_user_data.delay()
        return {"id": result.id}
    else:
        result = AsyncResult(task)
        return {"status": result.status}
    
@view.route("/download/users")
def download_user_csv():
    task = request.args.get("task")

    result = AsyncResult(task)
    # print("Type of result.result is", type(result.result))
    file = io.BytesIO(bytes(result.result, "utf-8"))
    # print("FILE IS:::::::::::::::::::::::::::::::")
    file.seek(0)
    # filename should be YYYYMMDDHHMMSS_data.csv
    filename = datetime.now().strftime("%Y%m%d%H%M%S") + "_user_data.csv"
    print(file)
    return send_file(file, download_name=filename)

@view.route("/export/books")
@roles_required("admin")
@auth_token_required
def exportBookData():
    task = request.args.get("task")

    if not task:
        result = export_books_data.delay()
        return {"id": result.id}
    else:
        result = AsyncResult(task)
        return {"status": result.status}
    
@view.route("/download/books")
def download_book_csv():
    task = request.args.get("task")

    result = AsyncResult(task)
    # print("Type of result.result is", type(result.result))
    file = io.BytesIO(bytes(result.result, "utf-8"))
    # print("FILE IS:::::::::::::::::::::::::::::::")
    file.seek(0)
    # filename should be YYYYMMDDHHMMSS_data.csv
    filename = datetime.now().strftime("%Y%m%d%H%M%S") + "_book_data.csv"
    print(file)
    return send_file(file, download_name=filename)

