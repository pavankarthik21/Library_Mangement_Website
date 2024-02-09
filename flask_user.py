from flask import Flask, render_template, request, flash,redirect,url_for
from datetime import datetime, timedelta
import mysql.connector
import uuid


app = Flask(__name__)

# MySQL Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Your_Password',
    'database': 'Your_Database_name',
}

def connect_db():
    conn = mysql.connector.connect(**db_config)
    return conn


@app.route('/new_user')
def index():
    return render_template('New_user.html')

@app.route('/input')
def input():
    return render_template('input.html')

@app.route('/process_form', methods=['POST'])
def process_form():
    ssn = request.form['ssn']
    bname = request.form['bname']
    address = request.form['address']
    phone = request.form['phone']
    
    conn = connect_db()
    cursor = conn.cursor()

    q1 = "SELECT COUNT(*) FROM BORROWER;"
    cursor.execute(q1)
    count = cursor.fetchall()
    # print(count[0][0])
    # print(type(count[0][0]))

    c  = count[0][0]
    c = c+1
    id = str(c)
    
    for i in range(6-len(id)):
        id = '0'+id
    id = 'ID' + id
    print(id)

    query = "INSERT INTO Borrower(card_id,ssn, Bname, address, phone) VALUES (%s, %s, %s, %s, %s)"
    data = (id, ssn, bname, address, phone)

    cursor.execute(query, data)
    conn.commit()

    return f"Form submitted successfully! Card_id :{id}, SSN: {ssn}, Bname: {bname}, Address: {address}, Phone: {phone}"


# Route to handle ISBN input and display book information
@app.route('/get_info', methods=['POST'])
def get_info():

    conn = connect_db()
    cursor = conn.cursor()
    isbn = request.form['isbn']
    title = request.form['title']
    if(len(title) != 0):
        title =  '%' +title+'%'
    else :
        title = "0"

    print(title)
    
    # Query to get ISBN, Title, and Authors for a specific ISBN
    query = """
        SELECT
            b.ISBN,
            b.Title,
            GROUP_CONCAT(a.Name ORDER BY ba.Author_id ASC SEPARATOR ', ') AS Authors
        FROM
            Book b
        JOIN
            Book_authors ba ON b.ISBN = ba.ISBN
        JOIN
            Authors a ON ba.Author_id = a.Author_id
        WHERE
            b.ISBN = %s OR b.Title LIKE %s
        GROUP BY
            b.ISBN;
    """
    print(query)

    cursor.execute(query, (isbn,title))
    result = cursor.fetchall()
    print(result)

    cursor.close()

    return render_template('output.html', book_info = result)

####  SECTION 3 - CHECKING IN AND OUT BOOKS  ######

def checkout_book(isbn, card_no):
    conn = connect_db()
    cursor = conn.cursor()
    # Check if the borrower has reached the maximum allowed loans
    cursor.execute("SELECT COUNT(*) FROM BOOK_LOANS WHERE card_id = %s AND date_in IS NULL", (card_no,))
    active_loans_count = cursor.fetchone()[0]
    if active_loans_count >= 3:
        return False, 'Borrower has reached the maximum allowed loans.'

    # Check if the book is already checked out
    cursor.execute("SELECT COUNT(*) FROM BOOK_LOANS WHERE isbn = %s AND date_in IS NULL", (isbn,))
    existing_checkout_count = cursor.fetchone()[0]
    if existing_checkout_count > 0:
        return False, 'Book is already checked out.'

    # Generate a new unique loan_id as a varchar
    new_loan_id = str(uuid.uuid4())

    # Perform the check-out
    due_date = str(datetime.now() + timedelta(days=14))
    cursor.execute("INSERT INTO BOOK_LOANS (loan_id, isbn, card_id, date_out, due_date, date_in) VALUES (%s, %s, %s, %s, %s, NULL)",
                   (new_loan_id, isbn, card_no, datetime.now(), due_date))
    cursor.execute("INSERT INTO FINES (loan_id, fine_amt, paid) VALUES (%s,%s,%s)",(new_loan_id,0.00,0))
    conn.commit()
    cursor.close()

    return True, 'Book checked out successfully.'

# Function to perform book check-in
def checkin_book(isbn, card_no):
    conn = connect_db()
    cursor = conn.cursor()
    # Check if the book is checked out
    cursor.execute("SELECT loan_id FROM BOOK_LOANS WHERE isbn = %s AND card_id = %s AND date_in IS NULL", (isbn, card_no))
    loan = cursor.fetchone()
    if not loan:
        return False, 'Book check-in failed. Check the ISBN and Card Number.'

    # Perform the check-in
    cursor.execute("UPDATE BOOK_LOANS SET date_in = %s WHERE loan_id = %s", (datetime.now(), loan[0]))
    conn.commit()
    cursor.close()
    return True, 'Book checked in successfully.'

# Route for the check-out page
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        isbn = request.form.get('isbn')
        card_no = request.form.get('card_no')
        success, message = checkout_book(isbn, card_no)
        return render_template('checkout_result.html', success=success, message=message)

    return render_template('checkout.html')

# Route for the check-in page
@app.route('/checkin', methods=['GET', 'POST'])
def checkin():
    if request.method == 'POST':
        isbn = request.form.get('isbn')
        card_no = request.form.get('card_no')
        success, message = checkin_book(isbn, card_no)
        return render_template('checkin_result.html', success=success, message=message)

    return render_template('checkin.html')


# @app.route('/')
# def check_fines_page():
#     return render_template('check_fines.html')

@app.route('/check_fines', methods=['POST'])
def check_fines():
    conn = connect_db()
    cursor = conn.cursor()
    card_id = request.form.get('card_id')
    date_in = request.form.get('date_in')
    
    # Convert date_in to datetime object
    date_in = datetime.strptime(date_in, '%Y-%m-%d')
    
    # Fetch fines data based on card_id, date_in, and calculate fine_amt
    query = '''
        SELECT book_loans.loan_id, 
               DATEDIFF(%s,book_loans.due_date)*0.25  AS fine_amt
        FROM book_loans
        LEFT JOIN fines ON book_loans.loan_id = fines.loan_id
        WHERE book_loans.card_id = %s
        AND book_loans.date_in IS NULL
        AND fines.paid = 0
    '''
    cursor.execute(query, (date_in,card_id,))
    fines_data = cursor.fetchall()
    cursor.close()
    conn.commit()


    for fines in fines_data :
        conn = connect_db()
        cursor = conn.cursor()
        update_query = 'UPDATE fines SET Fine_amt = %s WHERE Loan_id = %s'
        cursor.execute(update_query, (fines[1], fines[0]))
        conn.commit()
        cursor.close()


    print("FINES DATA : " , fines_data)


    return render_template('display_fines.html', fines=fines_data)


def update_fine(card_id, isbn, fine_amt):
    # Connect to MySQL
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Get loan_id corresponding to card_id and ISBN
    query = 'SELECT loan_id FROM book_loans WHERE Card_id = %s AND ISBN = %s'
    cursor.execute(query, (card_id, isbn))
    result = cursor.fetchone()

    if result:
        loan_id = result[0]

        # Update Fine_amt in Fines table
        update_query = 'UPDATE fines SET Fine_amt = %s WHERE Loan_id = %s'
        cursor.execute(update_query, (fine_amt, loan_id))
        conn.commit()
        conn.close()
        return "Successfully updated fine."

    return "Loan not found."

# @app.route('/')
# def index():
#     return render_template('input_fine.html')

@app.route('/update_fine', methods=['POST'])
def update_fine_page():
    card_id = request.form.get('card_id')
    isbn = request.form.get('isbn')
    fine_amt = request.form.get('fine_amt')

    message = update_fine(card_id, isbn, fine_amt)

    return render_template('update_fine_result.html', message=message)


def pay_fine(card_id, isbn):
    # Connect to MySQL
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Get loan_id corresponding to card_id and ISBN
    query = 'SELECT loan_id FROM book_loans WHERE Card_id = %s AND ISBN = %s'
    cursor.execute(query, (card_id, isbn))
    result = cursor.fetchone()

    if result:
        loan_id = result[0]

        # Update paid status in Fines table
        update_query = 'UPDATE fines SET paid = 1 WHERE Loan_id = %s'
        cursor.execute(update_query, (loan_id,))
        conn.commit()
        cursor.close()

        return f"Successfully paid for ISBN {isbn}."

    return "Loan not found."


@app.route('/pay_fine', methods=['POST'])
def pay_fine_page():
    card_id = request.form.get('card_id')
    isbn = request.form.get('isbn')

    message = pay_fine(card_id, isbn)

    return render_template('payfines_result.html', message=message)
if __name__ == '__main__':
    app.run(debug=True)
