import os
import django
from django.core.files.images import ImageFile

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Book_Lib_Project.settings")
django.setup()


import pandas as pd
from api.models import Book, Author, AbstractBook, Category

path = "C:\\Users\\User\\Downloads\\onurdan_gelenler\\webScraping"
data_path = path + "\\book_detail_dataframe.csv"

col_names = [ 'Column1', 'book_name', 'author', 'publisher', 'translator', 'page_number', 'isbn',
            'description', 'category']

data = pd.read_csv(data_path, encoding='utf-16', skiprows=1, names=col_names,
                   converters={"author": lambda x: x.strip("[]").split(", "), "category": lambda x: x.strip("[]").split(", "), })

# dtype={'book_name':str, 'author':str, 'publisher':str, 'translator':str, 'page_number':np.int32, 'isbn':np.int32,
#        'description':str, 'category':str, 'image_id':str}  # commented out since fields may have arrays of their kinds


for i in range(len(data)):
    if not data['author'][i]:
        pass

    authors = []
    for name in data['author'][i]:
        try:
            author = Author.objects.get(name=name.strip("'"))
        except:
            author = Author.objects.create(name=name.strip("'"))

        authors.append(author)

    category_names = data['category'][i]
    categories = []
    for ind in range(len(category_names)):
        try:
            category = Category.objects.get(name=category_names[ind].strip("'"))
        except:
            if ind == 0:
                category = Category.objects.create(name=category_names[ind].strip("'"))
                parent = category
            else:
                category = Category.objects.create(name=category_names[ind].strip("'"), parent=category)

        categories.append(category)

    try:
        abstractBook = AbstractBook.objects.filter(authors__in=authors).get(name=data['book_name'][i])
    except:
        abstractBook = AbstractBook.objects.create(name=data['book_name'][i])
        abstractBook.authors.set(authors)
        abstractBook.category.set(categories)

    if not abstractBook:
        abstractBook = AbstractBook.objects.create(name=data['book_name'][i])
        abstractBook.authors.set(authors)
        abstractBook.category.set(categories)


    rel_path = data['isbn'][i]

    new_image = ImageFile(open('C:/Users/User/Downloads/onurdan_gelenler/webScraping/%s.jpg' %rel_path, "rb"))

    try:
        book = Book.objects.filter(isbn_13 = data['isbn'][i]).first()
    except:
        name = data['book_name'][i]
        book = Book.objects.create( name = data['book_name'][i],
                                    description = data['description'][i],
                                    isbn_13 = data['isbn'][i],
                                    publisher = data['publisher'][i],
                                    translator = data['translator'][i],
                                    image = new_image,
                                    abstract_book = abstractBook,
                                    page_number = data['page_number'][i],
                                    )
        book.authors.set(authors)

    if not book:
        book = Book.objects.create( name = data['book_name'][i],
                                    description = data['description'][i],
                                    isbn_13 = data['isbn'][i],
                                    publisher = data['publisher'][i],
                                    translator = data['translator'][i],
                                    image = new_image,
                                    abstract_book = abstractBook,
                                    page_number = data['page_number'][i],
                                    )
        book.authors.set(authors)

    if not abstractBook.pop_child_book:
        abstractBook.pop_child_book = book
        abstractBook.save()
