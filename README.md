# Python Password Security Toolkit

A Python command-line application for checking password strength,
generating secure random passwords, and detecting commonly used
passwords using a local word list.

## Features

- Password strength checker
- Password score from 0–100
- Detection of common patterns
- Secure random password generator
- Local common-password checker
- Hidden password input
- Offline operation
- No third-party dependencies

## Technologies

- Python 3.10+
- getpass
- pathlib
- string
- secrets

## Project Structure

password-security-toolkit/
├── main.py
├── password_checker.py
├── password_generator.py
├── common_passwords.txt
├── requirements.txt
├── README.md
└── .gitignore

## How to Run

Clone or download the repository and open a terminal
inside the project directory.

### macOS / Linux

python3 main.py

### Windows

py main.py

No external packages are required.

## How It Works

The password checker evaluates characteristics such as length,
uppercase and lowercase characters, numbers, special characters,
repeated characters, and predictable patterns.

The password generator uses Python's `secrets` module to create
random passwords.

The common-password checker compares the entered password against
a local list of commonly used examples.

## Example

PASSWORD SECURITY TOOLKIT

1. Check Password Strength
2. Generate Strong Password
3. Check Common Password
4. Exit

Enter your choice: 1

PASSWORD STRENGTH REPORT

Length: 16 characters
Score: 100/100
Rating: Very Strong

## Python Concepts Used

- Functions
- Loops and conditionals
- Strings and lists
- Sets and dictionaries
- File handling
- Exception handling
- Standard library modules

## Security Notes

This project is intended for educational purposes.

Passwords entered into the checker are not stored or transmitted.
The application works offline and uses a local sample password list.

The strength score is based on the rules implemented in this project
and should not be treated as a professional security assessment.

## Future Improvements

- Add automated tests
- Expand the common-password dataset
- Add more password pattern detection
- Add passphrase generation
