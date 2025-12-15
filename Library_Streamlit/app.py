import streamlit as st
from services.library_services import Library
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(BASE_DIR, "assets", "logo.jpg")

st.set_page_config(page_title="Digital Library System",
                   layout="wide")

# Session State
if "library" not in st.session_state:
    st.session_state.library = Library()

library = st.session_state.library


col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image(IMAGE_PATH, width=450)
st.divider()

st.markdown(
    "<h3 style='text-align: center;'>WELCOME TO DIGITAL LIBRARY SYSTEM</h3>",
    unsafe_allow_html=True
)
st.divider()

action = st.sidebar.selectbox(
    "Select your choice:",
    [
        "Add Book",
        "Search Book By Title",
        "Search Book By Author",
        "Borrow Book",
        "Return Book",
        "View Borrowed Books",
        "View All Books",
        "Exit"
    ]
)


def add_book():
    with st.form("add_book_form"):
        book_id = st.text_input("Book ID")
        title = st.text_input("Book Title")
        author = st.text_input("Author Name")
        total = st.number_input("Total Copies", min_value=1)
        submit = st.form_submit_button("Add Book")

        if submit:
            if library.add_book(book_id, title, author, total):
                st.success("Book added successfully")
            else:
                st.error("Book ID already exists")


def search_by_title():
    title = st.text_input("Enter Book Title")
    if st.button("Search"):
        results = library.search_by_title(title)
        if results:
            for book in results:
                st.write(
                    f"{book.book_id} | {book.title} | "
                    f"{book.author} | "
                    f"{book.available_copies}/{book.total_copies}"
                )
        else:
            st.error("No Book Found")



def search_by_author():
    author = st.text_input("Enter Author Name")
    if st.button("Search"):
        results = library.search_by_author(author)
        if results:
            for book in results:
                st.write(
                    f"{book.book_id} | {book.title} | "
                    f"{book.author} | "
                    f"{book.available_copies}/{book.total_copies}"
                )
        else:
            st.error("No Book Found")


def borrow_book():
    with st.form("borrow_form"):
        name = st.text_input("Your Name")
        book_id = st.text_input("Book ID")
        submit = st.form_submit_button("Borrow Book")

        if submit:
            due_date, error = library.borrow_book(name, book_id)
            if error:
                st.error(error)
            else:
                st.success("Book borrowed successfully")
                st.info(f"Due Date: {due_date.date()}")



def return_book():
    with st.form("return_form"):
        name = st.text_input("Your Name")
        book_id = st.text_input("Book ID")
        submit = st.form_submit_button("Return Book")

        if submit:
            fine = library.return_book(name, book_id)
            if fine is None:
                st.error("No borrowing record found")
            else:
                st.success("Book returned successfully")
                st.info(f"Fine: Rs {fine}")



def view_borrowed_books():
    borrowed = library.get_borrowed_books()
    if not borrowed:
        st.info("No Borrowed Books")
    else:
        for (name, book_id), due_date in borrowed.items():
            st.write(
                f"User: {name} | Book ID: {book_id} | Due Date: {due_date.date()}"
            )



def view_all_books():
    books = library.get_all_books()
    if not books:
        st.info("No Books Available")
    else:
        for book in books:
            st.write(
                f"{book.book_id} | {book.title} | "
                f"{book.author} | "
                f"{book.available_copies}/{book.total_copies}"
            )



if action == "Add Book":
    add_book()
elif action == "Search Book By Title":
    search_by_title()
elif action == "Search Book By Author":
    search_by_author()
elif action == "Borrow Book":
    borrow_book()
elif action == "Return Book":
    return_book()
elif action == "View Borrowed Books":
    view_borrowed_books()
elif action == "View All Books":
    view_all_books()
elif action == "Exit":
    st.success("👋 Thank you for using Digital Library System")

