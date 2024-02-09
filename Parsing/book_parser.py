#!/usr/bin/python3


fileObj = open('books.csv', 'r', encoding="utf-8")
text_file = list(fileObj)
author_id = 0
author_list = []
for line in text_file[1:21]:
    print('-' * 80)
    line = line.strip()
    column_list = line.split('\t')
    # print(column_list)
    isbn13 = column_list[1]
    title = column_list[2]
    authors = column_list[3]
    print("INSERT INTO Books VALUES (\"" + isbn13 + "\",\"" + title + "\");")
    authors = authors.split(',')
    for author in authors:
        author_id += 1
        if (author in author_list):
            # Deal with duplicate author
            print(author + " already exists")
            # Lookup existing author_id and populate author_id variable
        else:
            # Add author to list
            author_list += [author]
            # Be sure to look up existing author if applicable
            print("INSERT INTO Authors VALUES (\"" + str(author_id) + "\",\"" + author + "\");")

        print("INSERT INTO Book_authors VALUES (\"" + str(author_id) + "\",\"" + isbn13 + "\");")

    
print('=' * 80)
print(author_list)
    
fileObj.close()
