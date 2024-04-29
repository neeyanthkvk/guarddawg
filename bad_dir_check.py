import re
import os
import mimetypes

def list_files(directory):
    files_list = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            files_list.append(file_path)

    return files_list

def check_bad_dir(file):
    
    num_dirs_in = file.count('/')
    regex = '\.\./' * (num_dirs_in + 1) + '[^/]+'
    fd = open(file, 'r')
    filetext = fd.read()
    return re.search(regex, filetext)

def is_binary(file):
    textchars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})
    is_binary_string = lambda bytes: bool(bytes.translate(None, textchars))
    try:
        return is_binary_string(open(file, 'rb').read(1024))
    except:
        return True

if __name__ == '__main__':
    files = list_files('.')
    for file in files:
        print('DEBUG: Checking file: ' + file)
        if is_binary(file):
            print('Binary file found: ' + file)
            continue
        if check_bad_dir(file):
            print('Bad directory found in file: ' + file)
