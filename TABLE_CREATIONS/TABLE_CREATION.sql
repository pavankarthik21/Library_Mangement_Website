USE DB1;
CREATE TABLE BOOK(
	ISBN varchar(13) NOT NULL PRIMARY KEY,
	Title varchar(255),
	Age int
);

CREATE TABLE AUTHORS(
	
	Author_id varchar(255) NOT NULL PRIMARY KEY,
	Name varchar(255),
	Age int 
);
CREATE TABLE BORROWER(
	
	Card_id varchar(255) NOT NULL PRIMARY KEY,
	Ssn varchar(255),
	BName varchar(255),
	Address varchar(255),
	Phone int
);

CREATE TABLE BOOK_AUTHORS(
	
	Author_id varchar(255) NOT NULL,
	ISBN varchar(13),
	
CONSTRAINT PK_isbn PRIMARY KEY (Author_id,ISBN),
FOREIGN KEY (Author_id) REFERENCES AUTHORS(Author_id),
FOREIGN KEY (Author_id) REFERENCES BOOK(ISBN)
);
CREATE TABLE BOOK_LOANS(
	
	Loan_id varchar(255) NOT NULL,
	ISBN varchar(13),
	Card_id varchar(255),
	Date_out varchar(255),
	Due_date varchar(255),
	Date_in varchar(255),
	
	
    CONSTRAINT PK_isbn PRIMARY KEY (Loan_id),
FOREIGN KEY (Card_id) REFERENCES BORROWER(Card_id),
FOREIGN KEY (ISBN) REFERENCES BOOK(ISBN)
);

CREATE TABLE FINES(
	
	Loan_id varchar(255) NOT NULL,
	Fine_amt int,
	Paid int,

	
    CONSTRAINT PK_isbn PRIMARY KEY (Loan_id),
FOREIGN KEY (Loan_id) REFERENCES BOOK_LOANS(Loan_id)

);


