from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin


db = SQLAlchemy()

class User(db.Model, UserMixin):
    
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String())
    lname = db.Column(db.String())
    uname = db.Column(db.String(), unique=True, nullable=False)
    email = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    active_requests_count = db.Column(db.Integer, default=0)
    last_active = db.Column(db.DateTime())

    active = db.Column(db.Boolean)
    authenticated = db.Column(db.Boolean)
    fs_uniquifier = db.Column(db.String(100))

    #relationships
    roles = db.relationship("Role",
                            secondary="user_roles", 
                            backref=db.backref("users", lazy=True))
    issued_books = db.relationship("Book", secondary="book_issue", backref="issued_to_users", cascade="all")
    book_requests = db.relationship("Book", secondary="book_request", backref="requested_by_users", cascade="all")
    reviews = db.relationship("Review", backref=db.backref('user', lazy=True), cascade="all")

class Role(db.Model, RoleMixin):
    
    __tablename__ = 'role'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    description = db.Column(db.String())

class UserRoles(db.Model):

    __tablename__ = 'user_roles'

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id")) # adding foreign key reference is important! 
    role_id = db.Column(db.Integer(), db.ForeignKey("role.id"))

class Section(db.Model):

    __tablename__ = 'section'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    description = db.Column(db.String())
    date_created = db.Column(db.DateTime())

    books = db.relationship('Book', backref=db.backref('section', lazy=True), cascade="all")


class Author(db.Model):

    __tablename__ = 'author'

    id = db.Column(db.Integer(), primary_key=True)
    fname = db.Column(db.String())
    lname = db.Column(db.String())
    description = db.Column(db.String())
    

class Book(db.Model):

    __tablename__ = 'book'

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    cover_path = db.Column(db.String())
    date_added = db.Column(db.DateTime())
    section_id = db.Column(db.Integer(), db.ForeignKey('section.id'))
    content_path = db.Column(db.String())
    publication_date = db.Column(db.DateTime())
    last_issued = db.Column(db.DateTime())

    # relationships
    # section = db.relationship('Section', backref=db.backref('books', lazy=True), cascade="all")
    authors = db.relationship('Author', secondary='authorbookmap', backref=db.backref('books', lazy=True), cascade="all")
    reviews = db.relationship('Review', backref=db.backref('book', lazy=True), cascade="all")

class AuthorBookMap(db.Model):

    __tablename__ = 'authorbookmap'

    id = db.Column(
        db.Integer(), 
        primary_key=True
        )
    author_id = db.Column(
        db.Integer(), 
        db.ForeignKey('author.id'), 
        )
    book_id = db.Column(
        db.Integer(), 
        db.ForeignKey('book.id'), 

        )

class BookRequest(db.Model):

    __tablename__ = 'book_request'

    id = db.Column(db.Integer(), primary_key=True)
    book_id = db.Column(db.Integer(), db.ForeignKey('book.id'))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    request_date = db.Column(db.DateTime())
    request_duration = db.Column(db.Integer()) # in seconds
    request_status = db.Column(db.String()) # pending, approved, rejected, returned

    #relationships


class BookIssue(db.Model):
    
    __tablename__ = 'book_issue'

    id = db.Column(db.Integer(), primary_key=True)
    book_request_id = db.Column(db.Integer(), db.ForeignKey('book_request.id'))
    book_id = db.Column(db.Integer(), db.ForeignKey('book.id'))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    date_issues = db.Column(db.DateTime())
    issue_expiry_date = db.Column(db.DateTime())
    return_date = db.Column(db.DateTime())
    issue_status = db.Column(db.String()) # issued, returned

    #relationships
    # book = db.relationship('Book', backref=db.backref('book_issues', lazy=True))
    # user = db.relationship('User', backref=db.backref('issued_books', lazy=True))
    # book_request = db.relationship('BookRequest', backref=db.backref('book_issue', lazy=True), cascade="all")

class Review(db.Model):

    __tablename__ = 'review'

    id = db.Column(db.Integer(), primary_key=True)
    book_id = db.Column(db.Integer(), db.ForeignKey('book.id'))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    review_date = db.Column(db.DateTime())
    review_title = db.Column(db.String())
    review_desc = db.Column(db.String())
    rating = db.Column(db.Integer())



