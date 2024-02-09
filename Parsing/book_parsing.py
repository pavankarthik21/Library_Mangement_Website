f = open("C:\\Users\\VAMSI RAGHAV\\Downloads\\books.csv", "r", encoding="utf8")

text_file = list(f)
author_id = 0
author_list = []

all_books_operations = []
all_author_operations = []
all_book_authors_operations = []
ch = '"'
for line in text_file[1:]:
    line = line.strip()
    column_list = line.split('\t')
    isbn13 = column_list[1]
    title = column_list[2]
    authors = column_list[3]
    if(ch in title) : 
        title = title.replace('"',"'")
    st1  = "INSERT INTO Book VALUES (\"" + isbn13 + "\",\"" + title + "\");"
    all_books_operations.append(st1)
    # print(sql_statement)

    authors = authors.split(',')
    for author in authors:
        if (author in author_list) : 
            #  print("Author already in Table")
            pass
        else :
             author_id += 1
             if(ch in author) : 
                 author = author.replace('"', "'")
             author_list.append(author)
             st2 = "INSERT INTO Authors VALUES (\"" + str(author_id) + "\",\"" + author + "\");"
             if st2 not in all_author_operations:
                all_author_operations.append(st2)
        
        list_id = author_list.index(author)+ 1
        st3 = "INSERT INTO Book_authors VALUES (\"" + str(list_id) + "\",\"" + isbn13 + "\");"
        if st3 not in all_book_authors_operations :
            all_book_authors_operations.append(st3)
        



# --------------------------------------------- SQL CONNECTOR -------------------------------------------------------------- #


import mysql.connector

# Replace these with your MySQL database details
host = "localhost"
user = "root"
password = "Karthik@2001"
database = "DB1"

try:
    # Connect to the MySQL server
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    if connection.is_connected():
        print("Connected to the MySQL database")

        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        print("--------AUTHORS---------------")
        for st in all_author_operations : 
            insert_query = st
            print(st)
            # Execute the INSERT query with data
            cursor.execute(insert_query)

            # Commit changes to the database
            connection.commit()

            print("Data inserted successfully")
            
        print("-------------BOOK------------------------")

        for st in all_books_operations : 
            insert_query = st
            print(st)
            # Execute the INSERT query with data
            cursor.execute(insert_query)

            # Commit changes to the database
            connection.commit()

            print("Data inserted successfully")
        
        print("---------------------BOOK-AUTHORS----------------------------")

        for st in all_book_authors_operations : 
            insert_query = st
            print(st)
            # Execute the INSERT query with data
            cursor.execute(insert_query)

            # Commit changes to the database
            connection.commit()

            print("Data inserted successfully")
        

except mysql.connector.Error as err:
    print(f"Error: {err}")

# finally:
#     # Close the cursor and connection
#     if 'cursor' in locals():
#         cursor.close()
#     if 'connection' in locals() and connection.is_connected():
#         connection.close()
#         print("MySQL connection closed")


# -------------------------------  