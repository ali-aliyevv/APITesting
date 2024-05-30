import wikipedia
import requests

def test_suggest():
    query = "Python"
    suggestions_library = wikipedia.search(query)
    suggestions_api = requests.get(f"https://en.wikipedia.org/w/api.php?action=opensearch&search={query}&limit=10&namespace=0&format=json").json()[1]
    
    overlap = set(suggestions_library) & set(suggestions_api)
    assert len(overlap) >= min(len(suggestions_library), len(suggestions_api)) * 0.3, \
        f"Library suggestions: {suggestions_library} API suggestions: {suggestions_api}"
    print("FAILED test_suggest")

def test_page_title():
    page_title = "Python (programming language)"
    page_library = wikipedia.page(page_title).title
    page_api = requests.get(f"https://en.wikipedia.org/w/api.php?action=query&format=json&titles={page_title}").json()['query']['pages']
    assert list(page_api.values())[0]['title'] == page_library
    print("FAILED test_page_title")

def test_geosearch():
    latitude = 37.7749
    longitude = -122.4194
    places_library = wikipedia.geosearch(latitude, longitude)
    places_api = requests.get(f"https://en.wikipedia.org/w/api.php?action=query&list=geosearch&gscoord={latitude}|{longitude}&format=json").json()['query']['geosearch']
    places_api_titles = [place['title'] for place in places_api]
    assert places_library == places_api_titles
    print("FAILED test_geosearch")

def test_page_url():
    page_title = "Python (programming language)"
    page_url_library = wikipedia.page(page_title).url
    page_url_api = requests.get(f"https://en.wikipedia.org/w/api.php?action=query&prop=info&inprop=url&titles={page_title}&format=json").json()['query']['pages']
    page_url_api = list(page_url_api.values())[0]['fullurl']
    assert page_url_library == page_url_api
    print("FAILED test_page_url")

if __name__ == "__main__":
    try:
        test_suggest()
    except AssertionError:
        print("FAILED test_suggest")
        
    try:
        test_page_title()
    except AssertionError:
        print("FAILED test_page_title")
        
    try:
        test_geosearch()
    except AssertionError:
        print("FAILED test_geosearch")
        
    try:
        test_page_url()
    except AssertionError:
        print("FAILED test_page_url")

    print("All tests passed!")
