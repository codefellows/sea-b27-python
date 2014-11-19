"""
A simple attempt at trying to classify images.
"""
import os
from os.path import join
from PIL import Image
from numpy import array, histogram, interp
from sklearn.linear_model import LogisticRegression


def histeq(image, num_bins=256):
    """
    Image histogram equalization of a greyscale image. Taken from the 
    book 'Programming Computer Vision'.
    """
    image_histogram, bins = histogram(image.flatten(), num_bins, normed=True)
    cdf = image_histogram.cumsum()
    cdf = 255 * cdf / cdf[-1]
    equalized_image = interp(image.flatten(), bins[:-1], cdf)
    return equalized_image.reshape(image.shape), cdf


def convert_image_to_greyscale(filename):
    """
    Using PIL, convert an image to a greyscale image. Taken from the book
    'Programming Computer Vision'.
    """
    return array(Image.open(filename).convert("L"))
    

def load_images_for_learning(directory):
    """
    Loads the image data, converts the image to greyscale and then normalizes the
    historgram of the image for processing by my learning library. It will return
    a list of numpy array's for every image file in the directory.
    """
    data = [] 
    is_cat = []
    for image_names in os.listdir(directory):
        greyscale_data = convert_image_to_greyscale(join(directory, image_names))
        new_image, _ = histeq(greyscale_data)
        data.append(new_image)

        training_result = 0
        if image_names.startswith("cat_"):
            training_result = 1
        is_cat.append(training_result)
    return data, is_cat


def construct_learning_engine():
    import pdb
    pdb.set_trace()
    clf = LogisticRegression()
    training_images, training_results = load_images_for_learning("training")
    #for image, result in zip(training_images, training_results):
    #    clf.fit(image, result)
    clf.fit(training_images[0], training_results[0])
    return clf
