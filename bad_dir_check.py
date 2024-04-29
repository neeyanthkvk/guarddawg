import re
import os
import argparse

def list_files(directory):
    files_list = []

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            files_list.append(file_path)

    return files_list

def check_bad_dir(file, root):
    
    num_dirs_in = file.count('/')-root.count('/')
    regex = '\.\./' * (num_dirs_in) + '[^/]+'
    fd = open(file, 'r')
    filetext = fd.read()
    result = []
    for i, line in enumerate(filetext.split('\n')):
        if re.search(regex, line):
            result.append((i+1, line))
    return result

def is_binary(file):
    textchars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})
    is_binary_string = lambda bytes: bool(bytes.translate(None, textchars))
    try:
        return is_binary_string(open(file, 'rb').read(1024))
    except:
        return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', help='Directory path', required=True)
    args = parser.parse_args()
    root = args.dir

    files = list_files(root)
    for file in files:
        if is_binary(file):
            continue
        matches = check_bad_dir(file, root)
        for match in matches:
            print(f"Match found in {file} on line {match[0]}: {match[1]}")
