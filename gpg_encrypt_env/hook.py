import glob
from hashlib import md5
import os
import subprocess


def main():
    for path in glob.glob('./**/.env*.local', include_hidden=True, recursive=True):
        if os.path.islink(path):
            continue

        current_hash = md5(open(path, 'rb').read()).hexdigest()
        hash_path = f'{path}.md5'
        need_to_encrypt = not os.path.exists(hash_path)

        if not need_to_encrypt:
            need_to_encrypt = open(hash_path, 'r').read().strip() != current_hash

        if need_to_encrypt:
            with open(hash_path, 'w') as f:
                f.write(current_hash)

            subprocess.check_output(['gpg', '--symmetric', '--cipher-algo', 'AES256', path])

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
