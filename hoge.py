import requests
import base64
import hashlib

data = open('tests/00.jpg', 'rb')

r = requests.post(
    "https://api.deepai.org/api/CNNMRF",
    data={
        'content': base64.b64encode(data.read()),
        'style': 'https://video-images.vice.com/_uncategorized/1554346499928-02.jpeg',
    },
    headers={'api-key': 'ca6dafe3-27ec-4ed0-9c87-b11380bb396c'}
)

response = requests.get(r.json()['output_url'])
image = response.content

file_name = "tests/" + hashlib.md5(image).hexdigest() + ".jpg"

with open(file_name, "wb") as aaa:
    aaa.write(image)