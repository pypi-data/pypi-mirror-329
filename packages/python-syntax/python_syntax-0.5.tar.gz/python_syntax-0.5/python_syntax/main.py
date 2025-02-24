import argparse

def hello():
    """Prints a greeting message."""
    message = "Hello, World!"
    print(message)
    return message

def test():
    """Prints a test message."""
    message = "This is a test function!"
    print(message)
    return message

def prompt():
    """Displays the interactive menu and shows the messages."""
    print("Welcome to QuickStart CLI!")
    print("Please select a command:")
    print("1. hello - Prints 'Hello, World!'")
    print("2. test  - Prints 'This is a test function!'")
    
    choice = input("Enter your choice (1 or 2): ").strip()
    
    if choice == "1":
        message = hello()  # Call hello function and store the returned message
    elif choice == "2":
        message = test()  # Call test function and store the returned message
    else:
        print("Invalid choice. Please try again.")
        prompt()  # Recursively prompt if the input is invalid
        return
    
    print(f"\nYou selected option {choice}. Here is your message: '{message}'")

def main():
    """Handles CLI arguments and calls the appropriate function."""
    parser = argparse.ArgumentParser(description="QuickStart CLI Tool")
    parser.add_argument("command", nargs="?", help="Select a command to run")
    
    args = parser.parse_args()

    if args.command:
        if args.command == "hello":
            message = hello()  # Call hello and store the message
            print(f"\nYou selected the 'hello' command. Here is your message: '{message}'")
        elif args.command == "test":
            message = test()  # Call test and store the message
            print(f"\nYou selected the 'test' command. Here is your message: '{message}'")
        else:
            print("Invalid command. Type 'quickstart-cli' for options.")
    else:
        # No arguments provided, show the interactive prompt
        prompt()

if __name__ == "__main__":
    main()
