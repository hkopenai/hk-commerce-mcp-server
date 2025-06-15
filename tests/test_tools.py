import unittest

def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = suite()
    runner.run(test_suite)
