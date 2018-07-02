import sys

from settings import stop
import generate_text as gt

allow_methods = ['text']
allow_methods_string = ' or '.join(allow_methods)

if __name__ == "__main__":
    argv = sys.argv
    if len(argv) < 2:
        stop('Must specify method (either {}).'.format(allow_methods_string))
    method = argv[1]
    if method not in allow_methods:
        stop("{} isn't a valid method (must be either {}).".format(method, allow_methods_string))

    numberError = "Must specify number of elements to generate\n  pipenv run generate [method] -n [number]"

    if "-n" not in argv:
        stop(numberError)
    numberIndex = argv.index("-n")
    if len(argv) < numberIndex + 2:
        stop(numberError)
    number = int(argv[numberIndex + 1])
    
    if method == 'text':
        print(gt.generate(number))

