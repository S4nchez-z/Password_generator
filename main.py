import secrets
import argparse
import string
import requests


# Загрузка списка общих паролей из URL
COMMON_PASSWORDS_URL = 'https://kali.tools/files/passwords/password_dictionaries/10-char-common-passwords.txt'

def load_common_passwords(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return set(response.text.splitlines())
    except requests.RequestException as e:
        print(f"Error loading common passwords: {e}")
        return set()

def generate_password(length=16, common_passwords=set()):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    while True:
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        if (any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and any(c.isdigit() for c in password)
            and any(c in string.punctuation for c in password)
            and password not in common_passwords):
            break
    return password

def main():
    parser = argparse.ArgumentParser(description='Генерируйте пароли с определенными правилами.')
    parser.add_argument('-l', '--length', type=int, default=16)
    parser.add_argument('-c', '--count', type=int, default=1)
    parser.add_argument('-w', '--write', type=str, default='')
    args = parser.parse_args()

    common_passwords = load_common_passwords(COMMON_PASSWORDS_URL)

    passwords = [generate_password(args.length, common_passwords) for _ in range(args.count)]

    if args.write:
        with open(args.write, 'w') as f:
            for password in passwords:
                f.write(password + '\n')
        print(f"{args.count} пароль записан в {args.write}")
    else:
        for password in passwords:
            print(password)

if __name__ == "__main__":
    main()
