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

        # Getting the webpage, creating a Response object.
        response = requests.get(final_url)
        # Extracting the source code of the page.
        data = response.text
        # print(data)
        # Passing the source code to Beautiful Soup to create a BeautifulSoup object for it.
        soup = BeautifulSoup(data, features='html.parser')
        # Extracting all the <a> tags whose class name is 'result-title' into a list.
        titles = soup.findAll('a', {'class': 'result-title'})

        images = soup.find_all("a", {"class": "result-image"})

        image_url = "https://images.craigslist.org/{}_300x300.jpg"

        final_image_urls = []
        for image in images:
            if image.get('data-ids'):
                # append the image URL to final images list
                final_image_urls.append(image_url.format((image.get('data-ids').split(',')[0].split(':')[1])))
            else:
                # append a "NOT AVAILABLE" image URL to final images list
                final_image_urls.append('https://craigslist.org/images/peace.jpg')

        print(final_image_urls)

        stuff_for_frontend = {
            'titles': [(title.text, title.get('href')) for title in titles],
            'search': search,
            'final_image_urls': final_image_urls,
        }

        return render(request, 'my_app/new_search.html', stuff_for_frontend)
    return render(request, 'my_app/new_search.html')
