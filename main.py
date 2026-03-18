from TestUtils import TestUtils
from TestSuite import TestSymbolTable
import unittest
from colorama import Fore, Style
import sys

def getAndTest(cls):
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(cls)
    test(suite)

def getAndTestFucntion(cls, nameFunction):
    suite = unittest.TestSuite()
    suite.addTest(cls(nameFunction))
    test(suite)

def generate_repeating_sequence(size):
    base_sequence = "1234567890"
    repeated_sequence = (base_sequence * ((size // len(base_sequence)) + 1))[:size]
    return repeated_sequence

def printMiniGo(stream, result):
    print("----------------------------------------------------------------------")
    print(f'{Fore.RED}Assignment BTL3 - LTNC - HK242{Style.RESET_ALL} ')
    print(f'Tests run: {Fore.MAGENTA}{result.testsRun}{Style.RESET_ALL}')
    
    stream.seek(0)
    expect = stream.readline()
    print(generate_repeating_sequence(len(expect) - 1))
    
    styled_expect = ''.join(
        f"{Fore.RED}{c}{Style.RESET_ALL}" if c == 'E' else
        f"{Fore.YELLOW}{c}{Style.RESET_ALL}" if c == 'F' else
        f"{Fore.GREEN}{c}{Style.RESET_ALL}" if c == '.' else c
        for c in expect
    )
    print(styled_expect, end='')
    
    listErrors = []
    listFailures = []
    for i in range(1, len(expect)):
        if expect[i - 1] == 'E': listErrors.append(i)
        elif expect[i - 1] == 'F': listFailures.append(i)
    
    errors_str = ", ".join(map(str, listErrors))
    failures_str = ", ".join(map(str, listFailures))

    if len(listFailures) + len(listErrors):
        Pass = 100.0 * (1 - (len(listFailures) + len(listErrors)) / (len(expect) - 1))
        print(f"\n{Fore.GREEN}Pass     : {Pass:.2f} %{Style.RESET_ALL}")
        print(f"{Fore.RED}Errors   : {errors_str}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Failures : {failures_str}{Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}Pass full 10.{Style.RESET_ALL}")
    print("----------------------------------------------------------------------")

def test(suite):
    from pprint import pprint
    from io import StringIO
    stream = StringIO()
    runner = unittest.TextTestRunner(stream=stream)
    result = runner.run(suite)
    print('Tests run ', result.testsRun)
    print('Errors ', result.errors)
    pprint(result.failures)
    stream.seek(0)
    print('Test output\n', stream.read())
    printMiniGo(stream, result)


def printUsage():
    print("Usage:")
    print("  python3 run.py  [test_case]   # Run tests (test_case is optional)")
    print()
    print("Notes:")
    print("  - Replace [test_case] with the specific test you want to run, e.g., test_1.")
    print("  - If [test_case] is not provided, all tests in the suite will be executed.")

if __name__ == "__main__":
    TestUtils.clean()
    argv = sys.argv[1:]
    if len(argv) > 1:
        printUsage()
    elif len(argv) == 0:
        getAndTest(TestSymbolTable)
    else:
        getAndTestFucntion(TestSymbolTable, argv[0])
