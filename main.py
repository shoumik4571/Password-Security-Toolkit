"""Terminal interface for the Python Password Security Toolkit."""

import getpass
import warnings

from password_checker import (
    analyze_password,
    is_common_password,
    load_common_passwords,
)
from password_generator import DEFAULT_LENGTH, MAX_LENGTH, MIN_LENGTH, generate_password


SEPARATOR = "=" * 40


def display_menu():
    print("\n" + SEPARATOR)
    print("PASSWORD SECURITY TOOLKIT")
    print(SEPARATOR)
    print("Educational checks. Offline only.\n")
    print("1. Check Password Strength")
    print("2. Generate Strong Password")
    print("3. Check Common Password")
    print("4. Exit")


def read_hidden_password():
    # Stop instead of letting getpass fall back to showing the password.
    warnings.simplefilter("error", getpass.GetPassWarning)

    while True:
        password = getpass.getpass("Enter a password (input hidden): ")

        # Spaces can be part of a password, so do not use strip() here.
        if password != "":
            return password
        print("A password cannot be empty. Please try again.")


def run_strength_check(common_passwords):
    print("\nPASSWORD STRENGTH CHECK")
    password = read_hidden_password()
    result = analyze_password(password, common_passwords)

    print("\n" + SEPARATOR)
    print("PASSWORD STRENGTH REPORT")
    print(SEPARATOR)
    print(f"Length: {result['length']} characters")
    print(f"Score: {result['score']}/100")
    print(f"Rating: {result['rating']}")
    print("\nRequirements:")
    for requirement, passed in result["checks"].items():
        if passed:
            print(f"[PASS] {requirement}")
        else:
            print(f"[FAIL] {requirement}")

    print("\nSuggestions:")
    for suggestion in result["suggestions"]:
        print(f"- {suggestion}")
    print("\nEducational estimate only; not a guarantee of security.")


def read_password_length():
    while True:
        answer = input(
            f"Password length ({MIN_LENGTH}-{MAX_LENGTH}, "
            f"Enter for {DEFAULT_LENGTH}): "
        ).strip()
        if answer == "":
            return DEFAULT_LENGTH
        try:
            length = int(answer)
        except ValueError:
            print("Please enter a whole number.")
            continue
        if MIN_LENGTH <= length <= MAX_LENGTH:
            return length
        print(f"Please choose a length from {MIN_LENGTH} to {MAX_LENGTH}.")


def ask_generate_again():
    while True:
        answer = input("\nGenerate another password? (y/n, Enter for n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no", ""):
            return False
        print("Please enter y or n.")


def run_password_generator(common_passwords):
    print("\nSTRONG PASSWORD GENERATOR")
    print("Generated passwords are displayed, but never saved by this program.")
    print("Use a private terminal; the output may remain in its scrollback.\n")
    while True:
        length = read_password_length()
        try:
            password = generate_password(length, common_passwords)
        except RuntimeError:
            print("Could not generate a suitable password. Please try again from the menu.")
            return

        print(f"\nGenerated password: {password}")
        print("Includes all four character types and passes the local strength checks.")
        if not ask_generate_again():
            return


def run_common_password_check(common_passwords):
    print("\nCOMMON PASSWORD CHECK")
    password = read_hidden_password()
    if is_common_password(password, common_passwords):
        print("\n[WARNING] This password is in the local common-password list.")
        print("Avoid it. Choose a completely different, unique password.")
    else:
        print("\nNot found in the bundled example list.")
        print("This does NOT prove it is strong or absent from breached-password lists.")
        print("Option 1 provides a separate, limited strength estimate.")


def main():
    try:
        common_passwords = load_common_passwords()
    except (OSError, ValueError):
        print("[ERROR] Could not read a non-empty, UTF-8 common_passwords.txt.")
        print("Restore the bundled file beside password_checker.py, then try again.")
        print("Checks were not run; an unavailable list is not a safe result.")
        return 1

    try:
        while True:
            display_menu()
            choice = input("\nEnter your choice: ").strip()
            if choice == "1":
                run_strength_check(common_passwords)
            elif choice == "2":
                run_password_generator(common_passwords)
            elif choice == "3":
                run_common_password_check(common_passwords)
            elif choice == "4":
                print("\nGoodbye. Keep your passwords unique and private.")
                return 0
            else:
                print("\nInvalid choice. Please enter 1, 2, 3, or 4.")
    except getpass.GetPassWarning:
        print("\n[ERROR] This environment cannot hide password input.")
        print("No password was read. Use a standard terminal on your computer.")
        return 1
    except (KeyboardInterrupt, EOFError):
        print("\nInput cancelled. Goodbye.")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
