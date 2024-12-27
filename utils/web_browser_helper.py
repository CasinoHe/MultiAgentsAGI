"""
Helper for get content from a web url
"""
import requests
from typing import Annotated


class WebBrowser:
    def __init__(self, url: Annotated[str, ""]):
        self.url = url
        self.content = self._get_web_content(url)

    def _get_web_content(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
            return response.text
        except requests.exceptions.HTTPError as errh:
            return f"HTTP Error: {errh}"
        except requests.exceptions.ConnectionError as errc:
            return f"Error Connecting: {errc}"
        except requests.exceptions.Timeout as errt:
            return f"Timeout Error: {errt}"
        except requests.exceptions.RequestException as err:
            return f"Error: {err}"
        except Exception as err:
            return f"Error: {err}"

    def get_content(self):
        return self.content


def test():
    # Example usage
    url = 'https://github.com/microsoft/autogen'  # Replace with your URL
    browser = WebBrowser(url=url)
    print(dir(browser))
    print(browser.get_content())


if __name__ == "__main__":
    test()
