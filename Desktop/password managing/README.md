# Simple Password Manager

A secure command-line password manager built with Python that uses encryption to protect your passwords.

## Features

- **Secure Encryption**: Uses Fernet encryption with PBKDF2 key derivation
- **Master Password Protection**: Single master password protects all stored passwords
- **Password Generation**: Generate secure random passwords with customizable length and character sets
- **Simple CLI Interface**: Easy-to-use command-line interface
- **Local Storage**: All data stored locally on your machine

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the password manager:
```bash
python password_manager.py
```

2. On first run, you'll be prompted to create a master password
3. Use the menu options to:
   - Add new passwords
   - Retrieve existing passwords
   - List all stored services
   - Generate secure passwords
   - Update or delete passwords

## Security Features

- Passwords are encrypted using Fernet (AES 128 in CBC mode)
- Master password is used with PBKDF2 (100,000 iterations) to derive encryption key
- Salt is randomly generated and stored separately
- No passwords are stored in plain text

## Files Created

- `passwords.enc`: Encrypted password database
- `salt.key`: Salt file for key derivation

## Important Notes

- **Remember your master password**: There is no way to recover your passwords if you forget the master password
- **Keep backups**: Consider backing up your encrypted files to prevent data loss
- **Secure your system**: This tool is only as secure as your computer - keep your system updated and secure