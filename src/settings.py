import sys

SPACE = ' '

def stop(message, error=True):
    if error:
        sys.stderr.write('Error: {} '.format(message))
        sys.exit(1)
    print(message)
    sys.exit(0)
