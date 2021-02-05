"""Contains utility functions for the gauss package"""
import pickle5 as pickle


def save_obj(obj, filename):
    """
    Saves an object as a pkl file.

    :param obj: The object to save.
    :param filename: The name of the file to save the object to.
    :type filename: str or path
    """
    with open(filename, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(filename):
    """
    Loads an object from a given file.

    :param filename: The file where the object is located.
    :return: The stored object.
    """
    with open(filename, 'rb') as f:
        return pickle.load(f)
