#!/usr/bin/env python2
import unittest

testmodules = [
    'tests.test_sqlite',
]
suite = unittest.TestSuite()

for test in testmodules:
    try:
        # If the module defines a suite() function, call it to get the suite.
        mod = __import__(test, globals(), locals(), ['suite'])
        suitefn = getattr(mod, 'suite')
        suite.addTest(suitefn())
    except (ImportError, AttributeError):
        # else, just load all the test cases from the module.
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName(test))

if __name__=="__main__":
    unittest.TextTestRunner().run(suite)
