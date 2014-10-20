# A web scraping script to get the product info for
# an item based on UPC.
import sys
import urllib2


def locate_item_url(upc):
    """
    Query the Walmart.com search URL based on the UPC code. Grab the first item
    listed since we expect a UPC search to only ever return a single item. Returns
    the URL of the item detail page to scrape later.
    """
    item_search_url = "http://www.walmart.com/search/?query=%s" % (upc,)
    resp = urllib2.urlopen(item_search_url)
    if resp.getcode() == 200:
        print resp.read()
    else:
        raise Exception("Search request failed")


def get_item_name_and_ingreidents(upc):
    """
    Given a UPC number, fetches a friendly name and ingredients for the given
    item. Returns this as a dict with keys name and ingredients.
    """
    item_page_url = locate_item_url(upc)


if __name__ == "__main__":
    upc = sys.argv[1]
    item_data = get_item_name_and_ingreidents(upc)
