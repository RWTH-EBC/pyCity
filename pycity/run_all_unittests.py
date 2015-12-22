"""
run_all_unittests.py runs all unittests, which are stored within paths.

Please run this script before pushing and merging larger changes.
Script should terminate without errors.

If you want to add own unittest, extend paths variable with path to your unittest folder
"""

import itertools
import os
from nose import run
from nose.loader import TestLoader
from nose.suite import LazySuite


basepath = os.path.dirname(__file__)
#  Add further unittest pathes here
paths = (os.path.join(basepath, 'unittests', 'classes', 'demand'),
         os.path.join(basepath, 'unittests', 'classes', 'supply')
         )


def run_tests():
    all_tests = ()
    for path in paths:
        all_tests = itertools.chain(all_tests,
                                    TestLoader().loadTestsFromDir(path))
    suite = LazySuite(all_tests)
    run(suite=suite, argv=['--processes=4',
                             # '--verbose',
                             # '-s',
                           '--process-timeout=30'])

if __name__ == '__main__':
    run_tests()
