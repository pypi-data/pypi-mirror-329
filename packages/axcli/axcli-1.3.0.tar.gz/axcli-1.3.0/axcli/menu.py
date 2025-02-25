from colorama import Fore, Style
import axinite.tools as axtools
import click, os

@click.command(name="menu")
def menu():
    "Helps you navigate the Axinite CLI."
    print(f"Welcome to the {Fore.RED}Axinite CLI{Style.RESET_ALL}!")
    print("Here are the available commands:")
    print("  - catalog: Shows a catalog where you can download templates.")
    print("  - read: Reads a template from a file.")
    print("  - load: Loads a template to a file.")
    print("  - run: Loads and shows a template simultaneously.")
    print("  - show: Shows a file statically.")
    print("  - live: Shows a file live.")
    
    print("\nFor more information, type 'axcli <command> --help'.")
    
    ax_files = [f for f in os.listdir('.') if f.endswith('.ax')]
    print(f"There are {Fore.RED}{len(ax_files)}{Style.RESET_ALL} .ax files:")
    for f in ax_files:
        if f.endswith('.tmpl.ax'):
            print(f"  - {Fore.MAGENTA}{f}{Style.RESET_ALL}")
        else:
            print(f"  - {Fore.RED}{f}{Style.RESET_ALL}")
    
    print("What would you like to do? (quit, exit, or q to leave)")
    def fn():
        choice = input("> ").strip().lower()
        if choice == "catalog":
            url = input("Enter the URL of the catalog (leave blank if you don't know): ")
            print(f"Here's your command: {Fore.BLUE}axcli catalog {f"-u {url}" if url else ''}{Style.RESET_ALL}")
        elif choice == "read":
            filename = input("Enter the filename: ")
            print(f"Here's your command: {Fore.BLUE}axcli read {filename}{Style.RESET_ALL}")
        elif choice == "load":
            filename = input("Enter the filename: ")
            backend = input("Enter the backend name (leave blank if you don't know): ")
            delta = input("Enter the delta (leave blank if you don't know): ")
            limit = input("Enter the limit (leave blank if you don't know): ")
            print(f"Here's your command: {Fore.BLUE}axcli load {filename} {f'-b {backend}' if backend else ''} {f'-d {delta}' if delta else ''} {f'-l {limit}' if limit else ''}{Style.RESET_ALL}")
        elif choice == "run":
            filename = input("Enter the filename: ")
            backend = input("Enter the backend name (leave blank if you don't know): ")
            frontend = input("Enter the frontend name (vpython, mpl, or blank): ")
            print(f"Here's your command: {Fore.BLUE}axcli run {filename} {f'-b {backend}' if backend else ''} {f'-f {frontend}' if frontend else ''}{Style.RESET_ALL}")
        elif choice == "show":
            filename = input("Enter the filename: ")
            frontend = input("Enter the frontend name (vpython, mpl, plotly, or blank): ")
            print(f"Here's your command: {Fore.BLUE}axcli show {filename} {f'-f {frontend}' if frontend else ''}{Style.RESET_ALL}")
        elif choice == "live":
            filename = input("Enter the filename: ")
            frontend = input("Enter the frontend name (vpython, mpl, or blank): ")
            print(f"Here's your command: {Fore.BLUE}axcli live {filename} {f'-f {frontend}' if frontend else ''}{Style.RESET_ALL}")
        elif choice == "exit" or choice == "quit" or choice == "q":
            return "exit"
        else:
            print("Invalid choice. Please try again. (hint: use the available options above)")
    while fn() != "exit": pass