"""
Helper for consult archive(such as Google search, Bing search, Twitter search, etc.)
"""
from dataclasses import dataclass
from typing import Annotated, Union
from googleapiclient import discovery


@dataclass
class ResultItem:
    """
    Represents a standard search result item
    """
    title: str
    link: str
    snippet: str
    content: Annotated[Union[str, None], "The content of the link, maybe we cannot get the content"] = None
    image: Union[str, None] = None
    published_date: Union[str, None] = None


@dataclass
class SearchResult:
    """
    Represents a standard search result
    """
    items: list[ResultItem]
    total_results: Union[int, None] = None
    start_index: Union[int, None] = None
    all_count: Union[int, None] = None
    next_start_index: Union[int, None] = None
    next_all_count: Union[int, None] = None

    def get_items(self) -> list[ResultItem]:
        return self.items


class SearchBase:
    def search(self, query, **kwargs):
        raise NotImplementedError


class GoogleSearchHelper(SearchBase):
    google_service_instance = None

    def __init__(self, customsearchid: str, apikey: Union[str, None] = None):
        super().__init__()
        self.service = self._get_search_service(apikey)
        self.customsearchid = customsearchid
        self.last_search_result: Annotated[Union[SearchResult, None], "Last search result, if the search query is the same as the previous one, return the result directly"] = None

    def _get_search_service(self, api_key: Union[str, None] = None):
        if GoogleSearchHelper.google_service_instance:
            if api_key:
                # update the api key
                service = discovery.build("customsearch", "v1",
                                          developerKey=api_key)
                GoogleSearchHelper.google_service_instance = service
                return service
            else:
                return GoogleSearchHelper.google_service_instance
        else:
            if not api_key:
                return None

            service = discovery.build("customsearch", "v1",
                                      developerKey=api_key)
            GoogleSearchHelper.google_service_instance = service
            return service

    def search(self, query, **kwargs) -> SearchResult:
        if not self.service:
            raise Exception("Service not initialized")

        search_result = self.service.cse().list(q=query, cx=self.customsearchid, **kwargs).execute()
        self._parse_search_result(query, search_result)
        return self.last_search_result

    def _parse_search_result(self, query: Annotated[str,
                                                    "Send the query content and the web page content of the query results to the llm model to find a better way to summarize the results."],
                             search_result) -> SearchResult:
        """
        Get the link content of each search item
        """
        # Iterate all search items, and get the content of each link
        search_result = SearchResult(items=[])
        search_result.total_results = int(search_result.get("searchInformation", {}).get("totalResults", 0))
        search_result.start_index = search_result.get("queries", {}).get("request", [{}])[0].get("startIndex", 1)
        search_result.all_count = search_result.get("queries", {}).get("request", [{}])[0].get("count", 10)
        search_result.next_start_index = search_result.get("queries", {}).get("nextPage", [{}])[0].get("startIndex", 1)
        search_result.next_all_count = search_result.get("queries", {}).get("nextPage", [{}])[0].get("count", 10)

        for item_data in search_result.get("items", []):
            item = ResultItem(title=item_data.get("title", ""),
                              link=item_data.get("link", ""),
                              snippet=item_data.get("snippet", ""))
            search_result.items.append(item)

        # try to read the link content

        self.last_search_result = search_result
