import mysql.connector

# Replace these with your MySQL database details
host = "localhost"
user = "root"
password = "Karthik@2001"
database = "DB1"

f = open("C:\\Users\\VAMSI RAGHAV\\Downloads\\borrowers.csv", "r", encoding="utf8")

text_file = list(f)


for line in text_file[1: ]:
    column_list = line.split(',')
    Card_id = column_list[0]
    ssn = column_list[1]
    Bname = column_list[2]+" "+ column_list[3]
    Address = column_list[5] + "," + column_list[6] + "," + column_list[7]
    Phone = column_list[8]

    #print(Card_id + "| "+ ssn + "| "+ Bname + "| "+Address +"| "+ Phone)
    st  = "INSERT INTO Borrower VALUES (\"" + Card_id + "\",\"" + ssn+ "\",\"" + Bname + "\",\"" + Address + "\",\"" + Phone +"\");"
    print(st)
    
    # ---------------------------- SQL CONNECTOR ------------------------------ # 
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
            cursor.execute(st)
            connection.commit()
            print("Data inserted successfully")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

print("--------------------------DONE---------------------------------")