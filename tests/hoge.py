# import requests
# r = requests.post(
#     "https://api.deepai.org/api/CNNMRF",
#     data={
#         'content': open('mo.jpg', 'rb'),
#         'style': open('style.jpg', 'rb'),
#     },
#     headers={'api-key': 'ca6dafe3-27ec-4ed0-9c87-b11380bb396c'}
# )
# print(r.json())

import requests
r = requests.post(
    "https://api.deepai.org/api/CNNMRF",
    data={
        'content': 'https://i0.wp.com/pikaribox.com/wp-content/uploads/2018/04/maezawayusaku-01.jpeg?fit=390%2C424&ssl=1',
        'style': 'https://video-images.vice.com/_uncategorized/1554346499928-02.jpeg',
    },
    headers={'api-key': 'ca6dafe3-27ec-4ed0-9c87-b11380bb396c'}
)
print(r.json())