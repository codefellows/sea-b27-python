# A web scraping script to get the product info for
# an item based on UPC.
import sys


def get_item_name_and_ingreidents(upc):
    """
    Given a UPC number, fetches a friendly name and ingredients for the given
    item. Returns this as a dict with keys name and ingredients.
    """
    print "Looking for UPC %s" % (upc,)


if __name__ == "__main__":
    upc = sys.argv[1]
    get_item_name_and_ingreidents(upc)
