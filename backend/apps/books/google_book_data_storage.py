import datetime

import dateparser as dateparser
from apps.books.models import Book
from common.utils.google_api_utils import GoogleBooksManager

from common.utils.google_api_utils import BookVolumeInfo


def try_dateparser(date: str) -> datetime.datetime:
    return dateparser.parse(date)


class BODOAdapter:
    def adapt_to_book_model(self, book_volume_info: BookVolumeInfo) -> Book:
        book = Book()
        book.volume_id = book_volume_info.volume_id
        book.title = book_volume_info.title[:48]
        book.publish_date = try_dateparser(book_volume_info.publish_date)
        # book.authors = book_volume_info.list_of_authors
        desc = book_volume_info.description
        book.description = desc[:998] if desc else None
        return book

    def _extract_date(self, book_volume_info):
        date = book_volume_info.publish_date
        timestamp_format = "%Y-%m-%d"
        return datetime.datetime.strptime(date, timestamp_format)


class BooksDataExtractor:

    def search_books(self, search_str):
        book_volume_info_list = GoogleBooksManager().search_books_by_name(search_str)
        book_models_list = self._adapt_volume_info_to_model(book_volume_info_list)
        self._save_models(book_models_list)
        return book_models_list

    def _adapt_volume_info_to_model(self, book_volume_info_list):
        book_models_list = list()
        for book_volume_info in book_volume_info_list:
            book_models_list.append(BODOAdapter().adapt_to_book_model(book_volume_info))
        return book_models_list

    def _save_models(self, book_models_list):
        for book_model in book_models_list:
            book_model.save()
