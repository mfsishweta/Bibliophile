import datetime

import dateparser as dateparser

from apps.authors.models import Author
from apps.books.models import Book
from common.utils.google_api_utils import BookVolumeInfo
from common.utils.google_api_utils import GoogleBooksManager


def try_dateparser(date: str) -> datetime.datetime:
    return dateparser.parse(date)


class BODOAdapter:
    def adapt_to_book_model_as_dict(self, book_volume_info: BookVolumeInfo) -> dict:
        # book = Book()
        book = dict()
        book['volume_id'] = book_volume_info.volume_id
        book['title'] = book_volume_info.title
        book['publish_date'] = try_dateparser(book_volume_info.publish_date) if book_volume_info.publish_date else None
        book['authors'] = book_volume_info.list_of_authors
        desc = book_volume_info.description
        book['description'] = desc if desc else None
        return book

    def adapt_to_book_model(self, book_volume_info: dict) -> Book:
        book = Book()
        book.volume_id = book_volume_info['volume_id']
        book.title = book_volume_info['title']
        book.publish_date = book_volume_info['publish_date']

        desc = book_volume_info['description']
        book.description = desc if desc else None
        book.save()
        authors_obj_list = self.adapt_authors_to_model(book_volume_info['authors'])
        book.authors.add(*authors_obj_list)
        return book

    def adapt_authors_to_model(self, list_of_authors):
        list_of_objects = list()
        for author in list_of_authors:
            list_of_objects.append(Author.objects.create(name=author))
        return list_of_objects

    def _extract_date(self, book_volume_info):
        date = book_volume_info.publish_date
        timestamp_format = "%Y-%m-%d"
        return datetime.datetime.strptime(date, timestamp_format)


class BooksDataExtractor:

    def search_books_by_name(self, search_str):
        book_volume_info_list = GoogleBooksManager().search_books_by_name(search_str)
        # getting list of all book result set in list of dict format
        book_models_list = self._adapt_volume_info_to_list_of_dict(book_volume_info_list)
        # self._save_models(book_models_list)
        return book_models_list

    def search_books_by_volume_id(self, volume_id):
        """
        Method to get book data by volume_id and convert it to model object to save it in th db
        """

        book_info = GoogleBooksManager().search_books_by_volume_id(volume_id)
        # pass data to create a book model object
        book_model = BODOAdapter().adapt_to_book_model_as_dict(book_info)
        # save the data
        # book_model.save()
        print(book_model, 'book model ###################333')
        return book_model

    def _adapt_volume_info_to_list_of_dict(self, book_volume_info_list):
        book_models_list = list()
        for book_volume_info in book_volume_info_list:
            book_models_list.append(BODOAdapter().adapt_to_book_model_as_dict(book_volume_info))
        return book_models_list

    def _save_models(self, book_models_list):
        for book_model in book_models_list:
            book_model.save()
