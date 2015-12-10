"""
This is a fake (noop) cython file to make setuptools thinks the build wheels
are python specific
"""

def say_hello_to(name):
    print("Hello %s!" % name)
