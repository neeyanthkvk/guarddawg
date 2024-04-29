import re
import os
import argparse

# Scan through files, marking errors in a results tuple of (str: err_type, str: file_name, int: line)

x_disable_found = False

def list_files(directory):
    files_list = []

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            files_list.append(file_path)

    return files_list

def is_binary(file):
    textchars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})
    is_binary_string = lambda bytes: bool(bytes.translate(None, textchars))
    try:
        return is_binary_string(open(file, 'rb').read(1024))
    except:
        return True
    
def scan_file(file, root):
    global x_disable_found
    if is_binary(file):
        return []
    num_dirs_in = file.count('/')-root.count('/')
    dir_regex = '\.\./' * (num_dirs_in) + '[^/]+'
    x_disable_regex = '^(?!\/\/)*app\.disable\([\'\"]x-powered-by[\'\"]\)'
    fd = open(file, 'r')
    filetext = fd.read()
    if not x_disable_found and re.search(x_disable_regex, filetext):
        x_disable_found = True
    result = []
    for i, line in enumerate(filetext.split('\n')):
        if re.search(dir_regex, line):
            result.append(("Directory escaping", i+1, line))
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', '-d', help='Directory path', required=True)
    args = parser.parse_args()
    root = args.dir
    root = root.strip('/')
    files = list_files(root)

    for file in files:
        matches = scan_file(file, root)
        for match in matches:
            print(f"{match[0]} found in {file} on line {match[1]}: {match[2]}")
    if(not x_disable_found):
        print("Default express response header not disabled. This increases vulnerability to fingerprinting attacks and can be removed with app.disable(\"x-powered-by\").")
