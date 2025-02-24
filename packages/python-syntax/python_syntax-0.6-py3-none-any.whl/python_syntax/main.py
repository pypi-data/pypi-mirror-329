import argparse
import os

# Predefined Python Syntax Templates
SYNTAX_TEMPLATES = {
    "list": """
# Python List Syntax
my_list = [1, 2, 3, 4, 5]
print(my_list)
    """,
    "tuple": """
# Python Tuple Syntax
my_tuple = (1, 2, 3, 4, 5)
print(my_tuple)
    """,
    "dictionary": """
# Python Dictionary Syntax
my_dict = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
print(my_dict)
    """,
    "function": """
# Python Function Syntax
def greet(name):
    return f"Hello, {name}!"
print(greet("Alice"))
    """,
    "if_else": """
# Python If-Else Syntax
x = 10
if x > 5:
    print("x is greater than 5")
else:
    print("x is less than or equal to 5")
    """
}

def save_to_file(message, file_path):
    """Writes the selected syntax template to the specified file."""
    try:
        with open(file_path, "a") as f:  # Open the file in append mode
            f.write(f"\n# Saved Syntax: {message[:20]}...\n")  # Write the first part of the message as a comment
            f.write(message)
        print(f"Syntax saved to {file_path}:\n{message}")
    except Exception as e:
        print(f"Error saving to file: {e}")

def show_syntax_options():
    """Displays the syntax options to the user."""
    print("Welcome to QuickStart CLI!")
    print("Please select a Python syntax template to include in your file:")
    print("1. List Syntax")
    print("2. Tuple Syntax")
    print("3. Dictionary Syntax")
    print("4. Function Syntax")
    print("5. If-Else Syntax")
    
    choice = input("Enter your choice (1-5): ").strip()
    
    if choice == "1":
        message = SYNTAX_TEMPLATES["list"]
    elif choice == "2":
        message = SYNTAX_TEMPLATES["tuple"]
    elif choice == "3":
        message = SYNTAX_TEMPLATES["dictionary"]
    elif choice == "4":
        message = SYNTAX_TEMPLATES["function"]
    elif choice == "5":
        message = SYNTAX_TEMPLATES["if_else"]
    else:
        print("Invalid choice. Please try again.")
        return
    
    print(f"\nYou selected option {choice}. Here is your syntax:")
    print(message)
    
    # Ask the user for the file path
    file_path = input("Enter the file path where you want to save this syntax (e.g., main.py): ").strip()
    
    # Validate the file path and save the syntax
    if not file_path:
        print("Invalid file path. Please try again.")
        return
    save_to_file(message, file_path)

def main():
    """Handles CLI arguments and calls the appropriate function."""
    parser = argparse.ArgumentParser(description="QuickStart CLI Tool for Python Syntax Templates")
    parser.add_argument("command", nargs="?", help="Select a command to run")
    
    args = parser.parse_args()

    if args.command:
        if args.command in SYNTAX_TEMPLATES:
            message = SYNTAX_TEMPLATES[args.command]  # Get the syntax template based on the command
            print(f"\nYou selected the '{args.command}' command. Here is your syntax:")
            print(message)
            
            # Ask the user for the file path
            file_path = input("Enter the file path where you want to save this syntax (e.g., main.py): ").strip()
            
            # Validate the file path and save the syntax
            if not file_path:
                print("Invalid file path. Please try again.")
                return
            save_to_file(message, file_path)
        else:
            print("Invalid command. Type 'quickstart-cli' for options.")
    else:
        # No arguments provided, show the interactive prompt
        show_syntax_options()

if __name__ == "__main__":
    main()
