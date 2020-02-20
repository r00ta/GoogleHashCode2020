import json 

import sys

class Book():
    def __init__(self, book_id, score):
        self.book_id = book_id
        self.score = score
        self.libraries = []
    
    def add_library(self, library_id):
        self.libraries.append(library_id)

class Library():
    def __init__(self, library_id, signup_time, books_shipped_in_one_day, books):
        self.library_id = library_id
        self.books = books
        self.total_books_score = 0
        self.signup_time = signup_time
        self.books_shipped_in_one_day = books_shipped_in_one_day
        self.best_score_in_remaining_time = 0
        self.waited = -1
        self.shooted_books_ordered = []
        self.books_dict = {}

    def calculate_book_score(self):
        self.total_books_score = reduce(lambda x, y: x + y.score, self.books, 0)
        self.books_ids = map(lambda x: x.book_id, self.books)

    def sort_books_by_score(self):
        self.books = sorted(self.books, key = lambda x: x.score, reverse = True)
        self.books_dict = {book.book_id : book for book in self.books}

    # The strategy
    def calculate_best_score_for_remaining_time(self, days):
        return self.signup_time
        #b = sorted(self.books, key = lambda x: x.score, reverse = True)
        return sum(map(lambda x: x.score, self.books[:self.books_shipped_in_one_day*days]))

    def shot_books(self):
        books_to_shot = self.books[:self.books_shipped_in_one_day]
        self.shooted_books_ordered += books_to_shot
        self.books = self.books[self.books_shipped_in_one_day:]
        map(lambda x: self.books_ids.remove(x.book_id), books_to_shot)
        return map(lambda x: x.book_id, books_to_shot)

    def remove_books_by_id(self, books_id):
        doit = False
        for bookId in books_id:
            if bookId in self.books_dict:
                del self.books_dict[bookId]
        if doit:
            self.books = filter(lambda x: x.book_id not in books_id, self.books)
    

def solve(books, libraries, days):
    already_shipped_book_ids = set()
    signed_library_ordered = []

    i = 0

    libraries_in_queue = []

    while i < days:
        sys.stderr.write(str(i) + " " + str(days) + "\n")
        if len(libraries_in_queue) != 0 and libraries_in_queue[-1].waited != 0:
            libraries_in_queue[-1].waited -= 1
        if (len(libraries_in_queue) == 0 or libraries_in_queue[-1].waited == 0) and len(libraries) != 0:
            current_situation = map(lambda x: [x, libraries[x].calculate_best_score_for_remaining_time(days - i)], libraries.keys()) 
            choice = sorted(current_situation, key = lambda x: x[1], reverse = True)[0]
            next_library =  libraries.pop(choice[0])
            next_library.waited = next_library.signup_time - 1
            libraries_in_queue.append(next_library)
            signed_library_ordered.append(next_library)

        libraries_done = []
        for library in filter(lambda library: library.waited == 0, libraries_in_queue):
            fired_books = library.shot_books()
            if len(fired_books) != 0:
                map(lambda x: x.remove_books_by_id(fired_books), libraries_in_queue)
                map(lambda x: libraries[x].remove_books_by_id(fired_books), libraries.keys())
                already_shipped_book_ids.union(fired_books)
            else:
                libraries_done.append(library)
        
        if len(libraries_done) != 0:
            for lib in libraries_done:
                libraries_in_queue.remove(lib)
        i += 1
    
    signed_library_ordered = filter(lambda x: len(x.shooted_books_ordered) != 0, signed_library_ordered)
    sys.stderr.write(" ".join(map(lambda x: str(libraries[x].total_books_score), libraries.keys())))
    print len(signed_library_ordered)
    for x in signed_library_ordered:
        print str(x.library_id) + " " + str(len(x.shooted_books_ordered))
        print ' '.join(map(lambda y: str(y.book_id), x.shooted_books_ordered))
    return


if __name__ == '__main__':
    # init objects 
    libraries = {}

    books_number, library_number, days_number = map(lambda x: int(x), raw_input().split(" "))

    books_award = map(lambda x: int(x), raw_input().split(" "))

    books = {i : Book(i, score) for (i, score) in enumerate(books_award) }

    i = 0
    while i < library_number:
        sys.stderr.write(str(i) + "\n")
        _, signup_time, books_shipped_in_one_day = map(lambda x: int(x), raw_input().split(" "))
        books_id_in_library = map(lambda x: int(x), raw_input().split(" "))

        books_in_library = []
        for idx in books_id_in_library:
               books_in_library.append(books[idx])
               books[idx].add_library(i) 

        # populate objects
        libraries.update({i: Library(i, signup_time, books_shipped_in_one_day, books_in_library)})

        i += 1

    # update structures
    map(lambda x: libraries[x].calculate_book_score(), libraries.keys())
    map(lambda x: libraries[x].sort_books_by_score(), libraries.keys())
    
    solve(books, libraries, days_number)



