from celery import shared_task
from time import sleep
import datetime
from .models import db, User
from smtplib import SMTP
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.encoders import encode_base64

from jinja2 import Template


import csv

from io import StringIO

from appln.models import db, User, BookRequest, Section, BookIssue, Book


@shared_task
def hello():
    print("Hello World from celery")


@shared_task
def another_task():
    print("crontab hello")

@shared_task
def daily_reminder_email():
    print("Daily reminder email")
    users = User.query.all()
    # users.last_active is a date time object, check if the different between now and last_active is 1 day or greater, make a list of users that satisfy this condition\

    inactive_users = [user for user in users if (datetime.datetime.now() - user.last_active).days >= 1]

    server = SMTP(host='localhost', port=1025)

    # server.login()

    for user in inactive_users:
        message = MIMEMultipart()
        message["From"] = "admin@elib.com"
        message["To"] = user.email
        message["Subject"] = "eLib Reminder email!"
        message.attach(MIMEText("Looks like you havent't been active for a while, login to find interesting reads!"))

        server.sendmail( 
                            from_addr="admin@elib.com",
                            to_addrs=user.email,
                            msg=message.as_string(),
                        )
    return True


@shared_task
def export_user_data():
    print("Exporting data")
    # export data to a csv file
    content = StringIO()
    writer = csv.writer(content)



    users = User.query.all()

    writer.writerow(["User ID", "First Name", "Last Name", "Email", "Last Active", "Issued Books", "Requested Books Remaining", "Issued Books Count", "Review Count"])

    for user in users:
        data = [user.id, user.fname, user.lname, user.email, user.last_active]
        issued_books = [book.title for book in user.issued_books]
        data.append(issued_books)
        requested_books_remaining = user.active_requests_count
        data.append(requested_books_remaining)
        issued_books_count = len(user.issued_books)
        data.append(issued_books_count)
        review_count = len(user.reviews)
        data.append(review_count)
        print(data)
        writer.writerow(data)
    


    content.seek(0)
    return content.read()

@shared_task
def export_books_data():
    print("Exporting data")
    # export data to a csv file
    content = StringIO()
    writer = csv.writer(content)

    books = Book.query.all()

    writer.writerow(["Book ID", "Title", "Date Added", "Last_Issued", "Section", "Issue Count"])

    for book in books:
        data = [book.id, book.title, book.date_added, book.last_issued]
        section = Section.query.get(book.section_id).name
        issue_count = len(BookIssue.query.filter_by(book_id=book.id).all())
        data.append(section)
        data.append(issue_count)
        print(data)
        writer.writerow(data)
    


    content.seek(0)
    return content.read()

@shared_task
def user_monthly_report():
    with open("templates/report.html") as file:
        template = Template(file.read())

    print("Monthly report")
    users = User.query.all()
    server = SMTP(host='0.0.0.0', port=1025)

    for user in users:
        book_titles_issued = [[book.id, book.title] for book in user.issued_books]
        for book in book_titles_issued:
            author_fname = Book.query.get(book[0]).authors[0].fname
            author_lname = Book.query.get(book[0]).authors[0].lname
            book_titles_issued[book_titles_issued.index(book)].append(author_fname + " " + author_lname)
            issue_date = BookIssue.query.filter_by(book_id=book[0]).order_by(BookIssue.date_issues.desc()).first().date_issues
            book_titles_issued[book_titles_issued.index(book)].append(issue_date)

        book_reviews_by_user = [[review.book_id, review.review_title, review.review_desc, review.rating] for review in user.reviews]
        for review in book_reviews_by_user:
            book_title = Book.query.get(review[0]).title
            book_reviews_by_user[book_reviews_by_user.index(review)].append(book_title)
        
        content = template.render(user=user, books=book_titles_issued, reviews=book_reviews_by_user)
        message = MIMEMultipart()
        message["From"] = "admin@elib.com"
        message["To"] = user.email
        message["Subject"] = "eLib Monthly Report"
        html = MIMEText(content, "html")
        message.attach(html)

        server.sendmail("admin@elib.com",
                        user.email,
                        message.as_string())
        

@shared_task
def auto_return_books():
    print("Auto returning books")
    book_issues = BookIssue.query.all()

    for issue in book_issues:
        if (datetime.datetime.now() > issue.issue_expiry_date) and (issue.issue_status == "issued"):
            issue.issue_status = "returned"
            issue.return_date = datetime.datetime.now()
            user = User.query.get(issue.user_id)
            user.active_requests_count -= 1
            db.session.commit()
    return True







