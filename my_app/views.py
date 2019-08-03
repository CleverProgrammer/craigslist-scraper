import requests
from requests.compat import quote_plus
from django.shortcuts import render
from .models import Search
from bs4 import BeautifulSoup
from bs4.element import Tag

page = requests.get(
    'https://forecast.weather.gov/MapClick.php?lat=41.8843&lon=-87.6324#.XIRQYFNKgUE'
)


# Create your views here.
def home(request):
    return render(request, 'my_app/index.html')


# access the search model
# create new search
# save & commit that to database
# then redirect to homepage

def new_search(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        Search.objects.create(search=search)

        url = "https://losangeles.craigslist.org/search/?query={}&min_price={}&max_price={}"
        # print(urljoin(url, quote_plus(search)))
        min_price = request.POST.get('min_price', 0)
        max_price = request.POST.get('max_price', 1000)
        final_url = url.format(quote_plus(search), min_price, max_price)
        print(final_url)

        # Getting the webpage, creating a Response object.
        response = requests.get(final_url)
        # Extracting the source code of the page.
        data = response.text
        # print(data)
        # Passing the source code to Beautiful Soup to create a BeautifulSoup object for it.
        soup = BeautifulSoup(data, features='html.parser')
        # Extracting all the <a> tags whose class name is 'result-title' into a list.
        titles = soup.findAll('a', {'class': 'result-title'})
        print(titles[0].get('href'))
        stuff_for_frontend = {
            'titles': [(title.text, title.get('href')) for title in titles],
            'search': search,
        }
        print(stuff_for_frontend)
        # Extracting text from the the <a> tags, i.e. class titles.
        for title in titles:
            print(title.text)

        rowArray = soup.find_all("li", {"class": "result-row"})
        print(rowArray[0].find('a', class_='result-image gallery'))
        # test_images = soup.find_all("img", {"class": "swipe"})
        test_images = soup.find_all("a", {"class": "result-image"})
        image_id = test_images[0].get('data-ids').split(',')[0].split(':')[1]
        final_image_url = "https://images.craigslist.org/{}_300x300.jpg".format(image_id)
        print(final_image_url)
        # print(soup)
        # print(rowArray[0])
        # print(rowArray[0].find('div', class_='swipe-wrap'))
        # print(rowArray)

        for row in rowArray:
            img = row.find("img")
            if img is None:
                continue
            if isinstance(img, Tag) and img.has_attr("src"):
                print(img['src'])
                print("----------------")

        return render(request, 'my_app/new_search.html', stuff_for_frontend)
    return render(request, 'my_app/new_search.html')
