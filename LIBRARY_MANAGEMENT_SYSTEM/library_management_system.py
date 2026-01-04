# ====================================== Library Management System ======================================
import json 
from  functools import wraps 
from typing import  List,Dict


#W decorator to controlled access to certain functions 
def required_role(role:str):
    """Decorator to check user role before alloeing access to a funuction """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not hasattr(self, "current_user") or  self.current_user.role != role:
                raise PermissionError(f"Access denied.Only {role} can perform this action.")
            return func(self, *args, **kwargs)
        return wrapper
    return decorator


# Create a book class 
class Book:
    def __init__(self,isbn : str, title : str, author : str):
        self.isbn = isbn 
        self.title = title
        self.author = author
        self.borrowed = False
    
    def __repr__(self):
        return f"{self.title} by {self.author} (ISBN : {self.isbn})"
class PrintedBook(Book):
    def __init__(self, isbn : str, title : str, author : str, pages : int):
        super().__init__(isbn, title, author)
        self.pages = pages

class EBook(Book):
    def __init__(self, isbn : str, title : str, author : str, file_size : float):
        super().__init__(isbn, title, author)
        self.file_size = file_size  # in MB

# Create a user class
class User:
    def __init__(self, user_id : str, name : str, role : str = "member", password: str = None):
        self.user_id = user_id
        self.name = name
        self.role = role # Admin or member
        self.password = password
    def __repr__(self):
        return f"{self.name}, role : {self.role}"
    


# craete a library management system class
class LibraryManagementSystem:
    def __init__(self):
        self.books : Dict[str, Book] = {}
        self.users : Dict[str,User] = {}
        self.current_user : User = None

    def fetch_all_books(self) -> List[Book]:
        """Return a list of all Book objects in the system."""
        return list(self.books.values())

    def show_all_books(self):
        """Print all books in a simple table format to the console."""
        books = self.fetch_all_books()
        if not books:
            print("No books available.")
            return
        # Prepare table rows
        rows = []
        for b in books:
            kind = "Printed" if isinstance(b, PrintedBook) else "EBook" if isinstance(b, EBook) else "Book"
            extra = ""
            if isinstance(b, PrintedBook):
                extra = str(getattr(b, "pages", "-"))
            elif isinstance(b, EBook):
                extra = f"{getattr(b, 'file_size', '-')} MB"
            else:
                extra = "-"
            rows.append((b.isbn, b.title, b.author, kind, extra, getattr(b, "borrowed", False)))

        # Compute column widths
        headers = ("ISBN", "Title", "Author", "Kind", "Pages/Size", "Borrowed")
        cols = list(zip(*([headers] + rows)))
        widths = [max(len(str(x)) for x in col) for col in cols]

        # Print header
        header_line = " | ".join(h.ljust(w) for h, w in zip(headers, widths))
        sep_line = "-+-".join("-" * w for w in widths)
        print(header_line)
        print(sep_line)

        # Print rows
        for r in rows:
            print(" | ".join(str(x).ljust(w) for x, w in zip(r, widths)))


    def Login(self, user : User):
        self.current_user = user

    @required_role("Admin")
    def add_book(self, book : Book):
        if book.isbn in self.books:
            raise ValueError("Book already exists in the Library.")
        self.books[book.isbn] = book

    @required_role("Admin")
    def remove_book(self, isbn :str):
        if isbn not in self.books:
            raise ValueError("Book not found in the Library.")
        del self.books[isbn]


    def borrow_book(self, isbn : str, user_id : str):
        if isbn not in self.books:
            raise ValueError("Book not found in the Library.")
        book = self.books[isbn]
        if book.borrowed:
            raise ValueError("Book is already Borrowed.")
        book.borrowed = True
        print(f"Book {book.title} borrowed by {self.users[user_id].name}")

    def return_book(self, isbn : str):
        if isbn not in self.books:
            raise KeyError("Book not found in the Library.")
        book = self.books[isbn]
        book.borrowed = False
        print(f"{book.title} returned successfully.")


    def search_books(self, keyword : str) -> List[Book]:
        return [ b for b in self.books.values()  if keyword.lower() in b.title.lower() or keyword.lower() in b.author.lower()]
    
    def add_user(self, user : User):
        if user.user_id in self.users:
            raise ValueError("User already exists.")
        self.users[user.user_id] = user

# Save library data to a file
    def save_data(self, filename = "library_data.json"):

        data = {
            "books" : { isbn : vars(book) for isbn, book in self.books.items()},
            "users" : { user_id : vars(user) for user_id, user in self.users.items()}
        }
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)


# Load library data from a file
    def load_data(self, filename = "library_data.json"):
        with open(filename, "r") as f:
            data = json.load(f)
        for isbn, b in data["books"].items():
            if "pages" in b:
                self.books[isbn] = PrintedBook(**b)
            elif "file_size" in b:
                self.books[isbn] = EBook(isbn=b['isbn'], title=b['title'], author=b['author'], file_size=b['file_size'])
            else:
                self.books[isbn] = Book(**b)
        for user_id, u in data["users"].items():
            self.users[user_id] = User(**u)

# ====================================== End of Library Management System ======================================
if __name__ == "__main__":
    lib = LibraryManagementSystem()

# Crate a user
    admin = User("U1", "Ravindra", role="Admin")
    member = User("U2", "Vinod", role="member")
    lib.add_user(admin)
    lib.add_user(member)


    lib.Login(admin)

    while True:
        print("\n============== Library Menu ==============")
        print("1. Login as User")
        print("2. Add Book (Admin only)")
        print("3. Remove Book (Admin only)")
        print("4. Issue Book")
        print("5. Return Book")
        print("6. Show All Books")
        print("7. Search Books")
        print("8. Save Data")
        print("9. Load Data")
        print("10. Exit")

        choice = input("Enter your choice: ").strip()


        try:
            if choice == "1":
                uid = input("Enter User ID: ").strip()
                if uid in lib.users:
                    lib.Login(lib.users[uid])
                    print(f"Logged in as {lib.current_user}")
                else:
                    print("User not found.")
            elif choice == "2":
                isbn = input("Enter ISBN: ").strip()
                title = input("Enter Title: ").strip()
                author = input("Enter Author: ").strip()
                kind = input("Enter Book Kind (printed/ebook): ").strip().lower()
                if kind == "printed":
                    pages = int(input("Enter Number of Pages: "))
                    lib.add_book(PrintedBook(isbn, title, author, pages))
                
                else:
                    size = float(input("Enter File Size (MB): "))
                    lib.add_book(EBook(isbn, title, author, size))
                print("Book added successfully.")
            elif choice == "3":
                isbn = input("Enter ISBN to remove: ").strip()
                lib.remove_book(isbn)
                print("Book removed successfully.")
            elif choice == "4":
                isbn = input("Enter ISBN to borrow: ").strip()
                uid = input("Enter your User ID: ").strip()
                lib.borrow_book(isbn, uid)
            elif choice == "5":
                isbn = input("Enter ISBN to return: ").strip()
                lib.return_book(isbn)
            elif choice == "6":
                lib.show_all_books()
            elif choice == "7":
                keyword = input("Enter keyword to search: ").strip()
                result = lib.search_books(keyword)
                print(f"Search Results: {result}")
            elif choice == "8":
                lib.save_data()
                print("Data saved successfully.")
            elif choice == "9":
                lib.load_data()
                print("Data loaded successfully.")
            elif choice == "10":
                print("Exiting the system. Goodbye!")
                break

            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"Error: {e}")





    
    
        
            
            









