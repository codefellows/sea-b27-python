# A web scraping script to get the product info for
# an item based on UPC.
import sys
import urllib2
from bs4 import BeautifulSoup


def locate_item_url(upc):
    """
    Query the Walmart.com search URL based on the UPC code. Grab the first item
    listed since we expect a UPC search to only ever return a single item. Returns
    the URL of the item detail page to scrape later.
    """
    item_search_url = "http://www.walmart.com/search/?query=%s" % (upc,)
    resp = urllib2.urlopen(item_search_url)
    if resp.getcode() == 200:
        page_data = BeautifulSoup(resp.read())
        item_page_path = page_data.find(class_="js-product-title")["href"]
        return "http://www.walmart.com%s" % (item_page_path,)
    else:
        raise Exception("Search request failed")


def extract_fields_from_item_page(item_page_url):
    """
    Scrape the details from the item details page. Returns a dictionary with a
    human friendly name and the ingredients used in the product.
    """
    resp = urllib2.urlopen(item_page_url)
    if resp.getcode() == 200:
        page_data = BeautifulSoup(resp.read())
        title = page_data.find(class_="productTitle").get_text()
        ingredients = page_data.find(class_="ProductIngredients").get_text()
        return {"name": title, "ingredients": ingredients}
    else:
        raise Exception("Fetching product page failed")


def get_item_name_and_ingreidents(upc):
    """
    Given a UPC number, fetches a friendly name and ingredients for the given
    item. Returns this as a dict with keys name and ingredients.
    """
    item_page_url = locate_item_url(upc)
    return extract_fields_from_item_page(item_page_url)


if __name__ == "__main__":
    upc = sys.argv[1]
    item_data = get_item_name_and_ingreidents(upc)
    print """
Item: %s

Ingredients: %s
    """ % (item_data["name"], item_data["ingredients"]) 

