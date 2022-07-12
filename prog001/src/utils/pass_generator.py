import random
from pathlib import PosixPath
import hashlib

PASS_SYMBOL = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890'

passwords_list = [
    'autobot02',
    'autobot03',
    'autobot04',
    'autobot05',
    'autobot06',
    'autobot07',
    'autobot08',
    'autobot09',
    'autobot10']


def encode_password(bot_name: str, primary_password: str):
    return (bot_name + ':' + hashlib.md5(primary_password.encode('ascii')).hexdigest())


def create_primary_password():
    ps = list(PASS_SYMBOL)
    random.shuffle(ps)
    return ''.join([random.choice(ps) for x in range(10)])


def password_generator():
    passwords = []
    for i in range(len(passwords_list)):
        passwords.append(encode_password(passwords_list[i], create_primary_password()))
    return passwords


def write_passwords_to_file(path: PosixPath):
    with open(path, 'w') as f:
        f.write('\n'.join(password_generator()))


def write_password_to_file(path: PosixPath, bot_name: str, secondary_password: str):
    passwords = []
    cur_bot_name = ''
    is_appended = False
    with open(path, 'r') as f:
        for line in f:
            print("line = ", line)
            for i in line:
                if i == ':':
                    break
                cur_bot_name += i
            if bot_name == cur_bot_name:
                is_appended = True
                passwords.append(secondary_password + '\n')
            else:
                passwords.append(line)
            print(passwords)
            cur_bot_name = ''
    if not is_appended:
        passwords.append(secondary_password + '\n')
        passwords.sort()
    with open(path, 'w') as f:
        f.write(''.join(passwords))


if __name__ == '__main__':
    write_passwords_to_file('.htpasswd')
