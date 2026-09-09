# Python Password Security Toolkit

A small, offline terminal application for practicing Python fundamentals and learning about password hygiene. It checks passwords, generates random passwords, and searches a local list of common examples.

**This is an educational project, not a professional security tool.** Scores describe a few rules, not cracking time or proof that a password is safe. Use made-up passwords while learning or recording a demo.

## Features

- Check length, uppercase letters, lowercase letters, numbers, and ASCII punctuation.
- Detect three identical characters in a row and a short list of predictable patterns.
- Get a score out of 100, a rating, PASS/FAIL results, and improvement suggestions.
- Generate passwords from 12 to 128 characters; the default is 16.
- Guarantee all four character types in generated passwords and check the result before displaying it.
- Check a small local common-password list without using an online service.
- Hide entered passwords and handle invalid menu choices and lengths.
- Use only Python's standard library: no packages, accounts, databases, or internet connection required.

## Technologies used

Python 3.10 or newer, with these standard-library modules:

| Module | Purpose |
| --- | --- |
| `getpass` | Hide password input in a terminal |
| `warnings` | Stop if `getpass` cannot hide input |
| `pathlib` | Find the bundled text file next to the checker |
| `string` | Supply groups of letters, digits, and punctuation |
| `secrets` | Choose and shuffle characters using randomness suitable for passwords |

## Setup and running

1. Install Python 3.10+ from [python.org](https://www.python.org/downloads/) if needed.
2. Get the code through GitHub (recommended), or extract the downloaded project files.
3. Open your computer's terminal in the folder containing `main.py`.

On macOS or Linux:

```bash
python3 main.py
```

On Windows:

```powershell
py main.py
```

If your installation uses `python`, run `python main.py` instead. No `pip install` step is needed; `requirements.txt` contains comments only.

If you downloaded a larger v0 project, use **only the `password-security-toolkit` folder**. The surrounding web-app files are not needed. This is a terminal application, so v0's web Preview and GitHub Pages will not run it.

Use a normal terminal, such as Terminal, PowerShell, or VS Code's integrated terminal. Output-only consoles and notebooks may not support hidden input. The sample file is found relative to the Python module, so launching `main.py` by its full path works too.

## Project structure

```text
password-security-toolkit/
├── main.py
├── password_checker.py
├── password_generator.py
├── common_passwords.txt
├── requirements.txt
├── README.md
└── .gitignore
```

| File | What it does |
| --- | --- |
| `main.py` | Displays the menu, reads input, prints reports, and handles errors |
| `password_checker.py` | Loads the common-password list and calculates findings |
| `password_generator.py` | Generates and checks random passwords |
| `common_passwords.txt` | Stores public example passwords, one per line; never add real credentials |
| `requirements.txt` | States that no third-party dependencies are needed |
| `README.md` | Explains setup, behavior, learning points, and limitations |
| `.gitignore` | Keeps caches, virtual environments, environment files, and logs out of normal Git commits |

## How the program works

1. Load the common-password sample once. If it cannot be read or is empty, stop rather than claim a successful check.
2. Show the menu and read the user's choice.
3. For checking, read a hidden password and return findings without including the password itself.
4. For generation, choose one character from each of the four groups, fill the remaining positions, securely shuffle the list, and check the result. Try at most 100 candidates.
5. Show the results and return to the menu. The generator also offers to generate another password immediately.

### Beginner-friendly implementation

The code uses ordinary functions, loops, `if`/`elif`/`else`, lists, sets, and dictionaries. Pattern detection is a loop over a short example list, not nested sequence searches or regular expressions. The menu returns automatically after each feature.

A few library calls remain deliberately: `secrets` supplies secure randomness, `getpass` hides input, and a one-line warning rule stops visible-input fallback. Replacing these with ordinary `random` or `input()` would make the password handling less safe, not more beginner-friendly.

### Reading the important functions

Start with `main()` in `main.py`, then follow one menu option at a time.

| Function | Plain-language explanation |
| --- | --- |
| `display_menu()` | Print the four options |
| `read_hidden_password()` | Read a password without echoing it; ask again if it is empty |
| `run_strength_check()` | Ask for a password and display the checker's report |
| `read_password_length()` | Accept a whole number from 12 to 128, or default to 16 |
| `ask_generate_again()` | Keep asking until the user gives a valid yes/no answer |
| `run_password_generator()` | Generate, display, and optionally repeat |
| `run_common_password_check()` | Show whether the password exactly matches a local example, ignoring case |
| `main()` | Load the list and connect the menu options to their functions |
| `load_common_passwords()` | Read the sample file into a set; a set supports quick lookup without duplicates |
| `is_common_password()` | Check membership in that set |
| `has_repeated_characters()` | Compare each character with the next two |
| `has_predictable_pattern()` | Look for any item in `PREDICTABLE_PATTERNS` inside the password |
| `get_strength_label()` | Convert a score to one of the five ratings |
| `analyze_password()` | Collect the checks, score, rating, and suggestions in a dictionary |
| `generate_password()` | Create a candidate using `secrets` and return one that passes the local rules |

At the bottom of `main.py`, the `if __name__ == "__main__":` guard starts the program only when that file is run directly. `SystemExit` passes the return code to the terminal: `0` for a normal exit and `1` for an error.

### What the checks mean

- Repetition means three identical consecutive characters, ignoring case: `aAa` fails, but `aba` does not.
- Patterns are only the examples in `PREDICTABLE_PATTERNS`, such as `1234`, `qwer`, and `password`. Matching ignores case and finds a pattern anywhere inside the input.
- This simple checker does **not** scan all years, all forward/reverse sequences, or repeated multi-character blocks. The short rule list is easier to read but less comprehensive.
- The common-password check is a case-insensitive **exact** match against the bundled sample. A non-match does not mean a password is absent from breach lists.
- Spaces are preserved in entered passwords and count toward length, but are not punctuation. Python's letter/digit checks recognize some non-ASCII characters; generation uses ASCII only. Python's character count can differ from the number of visually displayed symbols.

### Scoring rules

Start with length points:

| Length | Points |
| --- | ---: |
| Fewer than 8 characters | 0 |
| 8-11 characters | 10 |
| 12-15 characters | 25 |
| 16 or more characters | 40 |

Add 10 points for each character type present: uppercase, lowercase, digits, and ASCII punctuation. Add another 10 if no three-character repeat is found, and 10 if no listed pattern is found.

Finally, limit the score for obvious weaknesses. `min(score, limit)` keeps whichever number is smaller; it never adds points.

| Weakness | Maximum score |
| --- | ---: |
| Empty input, when calling the checker directly | 0 |
| Fewer than 8 characters | 19 |
| 8-11 characters | 59 |
| Three identical characters in a row | 59 |
| A listed predictable pattern | 39 |
| A password in the local common-password sample | 19 |

When several limits apply, the lowest wins.

| Score | Rating |
| --- | --- |
| 0-19 | Very Weak |
| 20-39 | Weak |
| 40-59 | Medium |
| 60-89 | Strong |
| 90-100 | Very Strong |

Generated passwords have all four character types and must score at least 60. With these rules they score 85 at lengths 12-15 and 100 at lengths 16-128. The 16-character check is a recommendation, not a requirement for a Strong rating. None of these scores guarantees real-world security.

## Example usage and output

Choose `1` and enter a made-up password. No characters or masking dots appear while typing; that is expected.

This abbreviated example uses a synthetic 16-character password that passes every check. The password is intentionally not included:

```text
========================================
PASSWORD SECURITY TOOLKIT
========================================
Educational checks. Offline only.

1. Check Password Strength
2. Generate Strong Password
3. Check Common Password
4. Exit

Enter your choice: 1

PASSWORD STRENGTH CHECK
Enter a password (input hidden):

========================================
PASSWORD STRENGTH REPORT
========================================
Length: 16 characters
Score: 100/100
Rating: Very Strong

Requirements:
[PASS] At least 12 characters
[PASS] 16 or more characters (recommended)
[PASS] Contains uppercase letters
[PASS] Contains lowercase letters
[PASS] Contains numbers
[PASS] Contains special characters (ASCII punctuation)
[PASS] No three identical characters in a row (case-insensitive)
[PASS] No patterns from the example list
[PASS] Not in the bundled common-password sample
```

The full report also prints improvement suggestions and an educational-use warning, then shows the menu again.

Choose `2` to generate a password. Enter a length or press Enter for 16. Answer `y` to generate another or `n` to return. Generated passwords are deliberately displayed and may remain in terminal scrollback.

Choose `3` and try a public entry from `common_passwords.txt`. The program warns without repeating the input:

```text
[WARNING] This password is in the local common-password list.
Avoid it. Choose a completely different, unique password.
```

## Practice checks

Use synthetic inputs only:

- Try an invalid menu choice and a non-numeric or out-of-range generation length.
- Check an empty input, a short password, a listed pattern, and a common-password sample.
- Check a password with spaces and confirm the spaces count toward length.
- Generate passwords of lengths 12, 16, and 128 and verify their length and character types.
- Press Ctrl+C to check the clean exit message.

There is no permanent automated test suite in this seven-file version; adding one is a useful next exercise.

## Python concepts practiced

- Variables, booleans, comparisons, and `in` membership checks
- Strings, string methods, indexes, and f-strings
- Lists, sets, and dictionaries
- `if`/`elif`/`else`, `for`, and `while`
- Functions, parameters, return values, and imports
- Reading a UTF-8 text file with `with`
- Input validation, `try`/`except`, and raising an exception
- Standard-library helpers and the script entry-point guard

## Security and privacy

- Entered passwords are not printed, saved, logged, or sent anywhere by this program. It makes no network calls. The common-password file is only read.
- If input cannot be hidden, the program stops instead of falling back to visible input. Use a normal terminal.
- Generated passwords are intentionally printed. Terminal history, screenshots, recordings, or external logging can capture them. Do not share credentials you actually use.
- Passwords temporarily exist in process memory; Python strings cannot be reliably erased from memory. This program does not promise protection from malware or monitoring software.
- The sample list and rules are small. They do not detect every leaked password, personal detail, predictable word, or reused credential. A passphrase can be strong without meeting every character-category rule.
- `secrets.choice()` and `secrets.SystemRandom().shuffle()` use operating-system-backed randomness. The generator does not use Python's default non-cryptographic random generator.
- Check a destination site's allowed symbols and length before using a generated password. Prefer a reputable password manager, unique passwords, and multi-factor authentication.

## Share on GitHub and LinkedIn

### Upload to GitHub without using Git commands

1. In v0, open the project block's three-dot menu and choose **Download ZIP**, then extract it on your computer.
2. Open the extracted `password-security-toolkit` folder. Upload **only its seven files**, not the surrounding Next.js starter, the entire download, or the ZIP itself.
3. Sign in to [GitHub](https://github.com/) and open [New repository](https://github.com/new).
4. Name it `password-security-toolkit`. A suitable description is: `An educational Python CLI for password checks and secure random password generation.` Choose **Public** if you want anyone viewing your portfolio to see it. Leave the automatic README and `.gitignore` options off, because these files already exist.
5. Create the repository. On its empty setup page, select **uploading an existing file**. For a repository that already has files, use **Add file > Upload files**.
6. Upload the seven files directly into the repository root. Confirm `main.py` and `README.md` appear at the top level. Include `.gitignore`; if it is hidden on your computer, show hidden files or use **Add file > Create new file** to add it with the supplied contents.
7. Use a commit message such as `Add Python password security toolkit` and confirm the upload. If GitHub proposes a new branch, open and merge the pull request into the default branch.
8. Check that GitHub displays this README below the files. Copy your repository URL to share it.

Do not upload `.env`, `__pycache__`, virtual environments, terminal logs, or real passwords. A `.gitignore` file is not a safety filter for files you manually select in a browser upload.

For later changes, upload the changed files to the same paths and write a short commit message explaining the change. GitHub Desktop is an optional next step when you want to learn version control without the command line.

Official guidance: [Create a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository) and [upload files](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository).

### Present it on LinkedIn

Share the repository link in a post and add it to your profile's Featured section or a project entry. Use a screenshot of the menu or a report from made-up input, not a real password or a generated password you plan to use. A live website is not required for a Python CLI portfolio project.

Suggested caption to adapt:

> I'm learning Python through a Password Security Toolkit: an offline terminal app with password checks, secure random generation, and a local common-password detector. It's an AI-assisted learning project focused on functions, loops, dictionaries, file handling, and input validation. The strength score is educational, not a professional security audit. My next step is to add my own automated tests.
>
> Code: paste your GitHub repository link here.

Only claim skills and work you can explain. Before an interview, practice explaining the score, the use of `secrets`, the hidden input, and why a password not appearing in the sample list is not proof of safety.

## Future improvements

1. Add a `unittest` suite using synthetic inputs and score-boundary cases.
2. Expand the pattern examples and local common-password list, documenting their limitations.
3. Add an option to exclude ambiguous characters such as `O`, `0`, `l`, and `1`.
4. Generate passphrases from a sufficiently large local word list, using `secrets` and explaining why passphrases need different strength assumptions.
5. Add optional terminal colors while keeping the written PASS/FAIL labels.
