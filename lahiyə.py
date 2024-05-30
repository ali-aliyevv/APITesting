import wikipedia
import requests
from colorama import init, Fore, Style

init(autoreset=True)

def test_suggest():
    query = "Python"
    suggestions_library = wikipedia.search(query)
    suggestions_api = requests.get(f"https://en.wikipedia.org/w/api.php?action=opensearch&search={query}&limit=10&namespace=0&format=json").json()[1]
    
    overlap = set(suggestions_library) & set(suggestions_api)
    overlap_count = len(overlap)
    min_count = min(len(suggestions_library), len(suggestions_api))
    print(f"Suggestions Library: {suggestions_library}")
    print(f"Suggestions API: {suggestions_api}")
    print(f"Overlap: {overlap}, Count: {overlap_count}, Min Count: {min_count}")
    assert overlap_count >= min_count * 0.3, \
        f"Not enough overlap. Library: {suggestions_library} API: {suggestions_api}"
    print(Fore.GREEN + "PASSED test_suggest")

def test_page_title():
    page_title = "Python (programming language)"
    page_library = wikipedia.page(page_title).title
    page_api = requests.get(f"https://en.wikipedia.org/w/api.php?action=query&format=json&titles={page_title}").json()['query']['pages']
    page_api_title = list(page_api.values())[0]['title']
    print(f"Library title: {page_library}")
    print(f"API title: {page_api_title}")
    assert page_api_title == page_library, f"Titles do not match. Library: {page_library}, API: {page_api_title}"
    print(Fore.GREEN + "PASSED test_page_title")

def test_geosearch():
    latitude = 37.7749
    longitude = -122.4194
    places_library = wikipedia.geosearch(latitude, longitude)
    places_api = requests.get(f"https://en.wikipedia.org/w/api.php?action=query&list=geosearch&gscoord={latitude}|{longitude}&format=json").json()['query']['geosearch']
    places_api_titles = [place['title'] for place in places_api]
    print(f"Library places: {places_library}")
    print(f"API places: {places_api_titles}")
    assert places_library == places_api_titles, f"Places do not match. Library: {places_library}, API: {places_api_titles}"
    print(Fore.GREEN + "PASSED test_geosearch")

def test_page_url():
    page_title = "Python (programming language)"
    page_url_library = wikipedia.page(page_title).url
    page_url_api = requests.get(f"https://en.wikipedia.org/w/api.php?action=query&prop=info&inprop=url&titles={page_title}&format=json").json()['query']['pages']
    page_url_api = list(page_url_api.values())[0]['fullurl']
    print(f"Library URL: {page_url_library}")
    print(f"API URL: {page_url_api}")
    assert page_url_library == page_url_api, f"URLs do not match. Library: {page_url_library}, API: {page_url_api}"
    print(Fore.GREEN + "PASSED test_page_url")

if __name__ == "__main__":
    try:
        test_suggest()
    except AssertionError as e:
        print(Fore.RED + str(e))
        print(Fore.RED + "Test not passed")
        
    try:
        test_page_title()
    except AssertionError as e:
        print(Fore.RED + str(e))
        print(Fore.RED + "Test not passed")
        
    try:
        test_geosearch()
    except AssertionError as e:
        print(Fore.RED + str(e))
        print(Fore.RED + "Test not passed")
        
    try:
        test_page_url()
    except AssertionError as e:
        print(Fore.RED + str(e))
        print(Fore.RED + "Test not passed")

    print(Fore.GREEN + "All tests completed!")
