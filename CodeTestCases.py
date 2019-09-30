#!/usr/bin/env python3.7

from BaseCodes import BaseCode, BaseCodeStatic, NaiveCode
from MultiCodes import MultiCode
from ClusterCodes import OriginalCodeStatic
import random
import argparse
import pickle




def main():
    ALL_CODES = {'naive':NaiveCode, 
                 'multi':MultiCode, 
                 'original':OriginalCodeStatic}

    ALL_TESTS = {'simple1':test1,
                 'simple2':test2}

    codeChoices = list(ALL_CODES.keys()) + ['all']
    testChoices = list(ALL_TESTS.keys()) + ['all', 'none']

    parser = argparse.ArgumentParser(description="Test cases for encoding schemes")
    parser.add_argument('-c', dest='codes', nargs='+', default=["all"], choices=codeChoices, help='Types of codes to test')
    parser.add_argument('-t', dest='tests', nargs='+', default=["all"], choices=testChoices, help='Unit tests to run on the chosen codes')
    parser.add_argument('-f', dest='matrixPickles', nargs='+', default=[], help='Pickle files corresponding to matrices to evaluate.')
    parser.add_argument('--verbose', '-v', action='count', default=0)
    args = parser.parse_args()

    codeClasses = []
    if 'all' in args.codes:
        codeClasses = ALL_CODES.values()
    else:
        codeClasses = [ALL_CODES[codeName] for codeName in args.codes]

    codeTests = []
    if 'none' in args.tests:
        codeTests = []
    elif 'all' in args.tests:
        codeTests = ALL_TESTS.values()
    else:
        codeTests = [ALL_TESTS[testName] for testName in args.tests]


    for codeTest in codeTests:
        for codeClass in codeClasses:
            codeTest(codeClass, verbosity=args.verbose)

    for filename in args.matrixPickles:
        print("Loading matrix from file %s..." %filename)
        matrix = None
        with open(filename, 'rb') as fp:
            matrix = pickle.load(fp)
        print("Done. Testing...")
        for codeClass in codeClasses:
            baseTest(codeClass, matrix, verbosity=args.verbose)


    



def baseTest(CodeClass, matrix, **kwargs):
    """ Verify a code class on a given matrix.
    """
    print("="*80)
    code = CodeClass(matrix=matrix, **kwargs)
    code.timeMake()
    code.verifyCompression()
    code.printInfo()
    print("="*80)



def test1(CodeClass, **kwargs):
    """ Simple test. Small matrix.
    """
    matrix = [[1,2,3], [3,4,5], [6,7]]

    baseTest(CodeClass, matrix, **kwargs)



def test2(CodeClass, rows=100, columns=100, density=0.1, **kwargs):
    """ Simple test. Uniformly random sparse matrix.
    """

    matrixSize = rows * columns 

    matrix = [set() for _ in range(rows)]
    for _ in range(int(matrixSize * density)):
        row = random.randint(0, rows-1)
        col = random.randint(0, columns-1)

        matrix[row].add(col)

    baseTest(CodeClass, matrix, **kwargs)



if __name__ == "__main__":
    main()






