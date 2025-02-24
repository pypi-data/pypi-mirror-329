import argparse

def hello():
    print("Hello, World!")

def test():
    print("This is a test function!")

def main():
    parser = argparse.ArgumentParser(description="QuickStart CLI Tool")
    subparsers = parser.add_subparsers(dest="command")

    # Command: hello
    parser_hello = subparsers.add_parser("hello", help="Print a greeting message")
    parser_hello.set_defaults(func=hello)

    # Command: test
    parser_test = subparsers.add_parser("test", help="Run a test function")
    parser_test.set_defaults(func=test)

    # Parse arguments
    args = parser.parse_args()

    if args.command:
        args.func()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
