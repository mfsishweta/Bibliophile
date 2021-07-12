import httplib2
from googleapiclient.discovery import build
from oauth2client import file, client, tools


class BookVolumeInfo:
    def __init__(self, volume_id, title, list_of_authors, publish_date, description):
        self.volume_id = volume_id
        self.title = title
        self.list_of_authors = list_of_authors
        self.publish_date = publish_date
        self.description = description


class GoogleApiClientGenerator:
    def __init__(self):
        self.scope_list = ["https://www.googleapis.com/auth/books", 'https://www.googleapis.com/auth/gmail.send']
        self.book_credential_path = "google_apps/google_apps_testing_account/book_credentials.json"
        self.gmail_credential_path = "google_apps/google_apps_testing_account/gmail_credentials.json"
        self.api_specific_dict = {"books": {"credentials_file": self.book_credential_path,
                                            "version": 'v1'},
                                  "gmail": {"credentials_file": self.book_credential_path,
                                            "version": 'v1'}
                                  }
        self.book_service = None
        self.gmail_service = None

    def get_service_instance(self, api_name):
        credentials_file = self.api_specific_dict[api_name]['credentials_file']
        version = self.api_specific_dict[api_name]['version']

        token = "google_apps/google_apps_testing_account/{token_name}.json".format(token_name=api_name)
        store = file.Storage(token)
        creds = store.get()
        if not creds or creds.invalid:
            print("Starting the authorization of flow: ")
            flow = client.flow_from_clientsecrets(credentials_file, self.scope_list)
            creds = tools.run_flow(flow, store)
        http = creds.authorize(httplib2.Http())
        service = build(api_name, version, credentials=creds, cache_discovery=False)
        return service

    def authorize_the_apis(self):
        self.populate_service_instances()

    def populate_service_instances(self):
        self.book_service = self.get_service_instance('books')
        self.gmail_service = self.get_service_instance('gmail')


class GoogleBooksManager:
    def search_books_by_name(self, search_str):
        book_client = self._setup_apps_attributes()
        return GoogleBooksExplorer().search_by_volume(book_client.book_service, search_str)

    def _setup_apps_attributes(self):
        book_client = GoogleApiClientGenerator()
        book_client.authorize_the_apis()
        return book_client


class GoogleBooksExplorer:
    def search_by_volume(self, book_service, search_str):
        res = book_service.volumes().list(q=search_str, maxResults=20).execute()
        print('#############', res)
        return self._extract_book_volume_objects(res['items'])

    def _extract_book_volume_objects(self, list_of_items):
        book_volume_info_list = list()
        for item in list_of_items:
            book_volume = self._get_book_volume(item)
            book_volume_info_list.append(book_volume)
        return book_volume_info_list

    def _get_book_volume(self, item):
        volume_id = item['id']
        title = item['volumeInfo']['title']
        authors = item.get('volumeInfo').get('authors', None)
        published_date = item['volumeInfo']['publishedDate']
        description = item.get('volumeInfo').get('description', None)
        return BookVolumeInfo(volume_id, title, authors, published_date, description)


if __name__ == "__main__":
    GoogleApiClientGenerator().authorize_the_apis()
    # GoogleBooksManager().search_books_by_name()
