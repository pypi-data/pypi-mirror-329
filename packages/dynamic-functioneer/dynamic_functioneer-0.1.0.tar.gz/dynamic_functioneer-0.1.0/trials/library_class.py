from dynamic_functioneer.dynamic_decorator import dynamic_function

class LibraryManager:
    """
    A class to manage a library's collection of books.
    """
    def __init__(self):
        """
        Initializes the LibraryManager with an empty collection of books.
        The books are stored in a dictionary where the key is the book title,
        and the value is a dictionary containing the book's details such as author,
        publication year, and the number of copies available.
        """
        self.books = {}

    @dynamic_function(
        model="meta-llama/llama-3.2-3b-instruct:free",
        extra_info="Adds a new book to the library. If a book with the same title already exists, "
                   "increments the number of available copies.",
        # error_model="meta-llama/llama-3.2-3b-instruct:free"
    )
    def add_book(self, title, author, year, copies=1):
        """
        Adds a new book to the library's collection or increases the number of copies
        if the book already exists.

        Args:
            title (str): The title of the book.
            author (str): The author of the book.
            year (int): The publication year of the book.
            copies (int, optional): The number of copies to add. Defaults to 1.

        Returns:
            str: A confirmation message indicating that the book was added or updated.
        """
        pass  # Implementation will be dynamically generated.

    @dynamic_function(
        model="meta-llama/llama-3.2-3b-instruct:free",
        extra_info="Removes a book from the library by title. If multiple copies exist, decrements the copy count. "
                   "If only one copy exists, removes the book entry entirely.",
        # error_model="meta-llama/llama-3.2-3b-instruct:free"
    )
    def remove_book(self, title):
        """
        Removes a book from the library's collection by title.

        Args:
            title (str): The title of the book to remove.

        Returns:
            str: A message indicating whether the book was removed or updated.

        Raises:
            KeyError: If the book is not found in the collection.
        """
        pass  # The dynamic_function decorator will generate the removal logic.

    @dynamic_function(
        model="meta-llama/llama-3.2-3b-instruct:free",
        extra_info="Searches for a book in the library by title. Returns the book details if found; "
                   "otherwise, raises an error.",
        # error_model="meta-llama/llama-3.2-3b-instruct:free"
    )
    def search_book(self, title):
        """
        Searches for a book in the library's collection by title.

        Args:
            title (str): The title of the book to search for.

        Returns:
            dict: A dictionary with details of the book (author, year, copies).

        Raises:
            KeyError: If the book is not found.
        """
        pass  # The decorator will dynamically generate this function.

    @dynamic_function(
        # model="meta-llama/llama-3.2-3b-instruct:free",
        extra_info="Lists all the books available in the library, along with their details.",
        # error_model="meta-llama/llama-3.2-3b-instruct:free"
    )
    def list_books(self):
        """
        Lists all books in the library's collection.

        Returns:
            list: A list of dictionaries, each representing a book's details.
        """
        pass  # DynamicFunctioneer will supply the code to compile the list.

# Example usage and testing of the LibraryManager class
if __name__ == '__main__':
    library = LibraryManager()

    # Add books to the library.
    print(library.add_book("1984", "George Orwell", 1949, 3))
    print(library.add_book("To Kill a Mockingbird", "Harper Lee", 1960, 2))
    # Adding an existing book ("1984") should update the number of copies.
    print(library.add_book("1984", "George Orwell", 1949, 1))

    # List all books in the library.
    print("\nCurrent Library Collection:")
    for book in library.list_books():
        print(book)

    # Search for a specific book.
    try:
        book_details = library.search_book("1984")
        print("\nDetails for '1984':", book_details)
    except KeyError as error:
        print("Search error:", error)

    # Remove a book from the library.
    try:
        print("\n", library.remove_book("To Kill a Mockingbird"))
    except KeyError as error:
        print("Removal error:", error)

    # List books after removal to see the updated collection.
    print("\nLibrary Collection after removal:")
    for book in library.list_books():
        print(book)
