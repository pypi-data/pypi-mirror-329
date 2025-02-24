# __init__.py

from .main import main  # Importing the 'main' function from main.py

__version__ = "0.1.0"
__author__ = "Sandeepan Mohanty"
__description__ = "QuickStart CLI tool for including different Python syntax templates into your file."

# Optional: You could allow the CLI tool to be executed directly from the package
# This can be helpful if users prefer to import the module and call the CLI directly

if __name__ == "__main__":
    main()
