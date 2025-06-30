import unittest

loader = unittest.TestLoader()
suite = unittest.TestSuite()

tests = [
    "tests.test_users",
    "tests.test_amenities",
    "tests.test_places",
    "tests.test_reviews"
]

for test in tests:
    suite.addTests(loader.loadTestsFromName(test))

runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)
