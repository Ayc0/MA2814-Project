SPACE = ' '

def stop(message, error=True):
    if error:
        print('Error:', end=" ")
        sys.exit(1)
    print(message)
    sys.exit(0)
