import requests
import base64
import hashlib
import random

data = open('tests/20200109-OHT1I50077-L.jpg', 'rb')

styles = ['https://video-images.vice.com/_uncategorized/1554346499928-02.jpeg',
          'https://casie.jp/media/wp-content/uploads/2020/09/Van_Gogh_Self-Portrait_with_Straw_Hat_1887-Detroit.jpg',
          'https://auctions.c.yimg.jp/images.auctions.yahoo.co.jp/image/dr000/auc0105/users/ff8558e1fe2b4810b6f62ca52a22e93fb5949a71/i-img900x1200-1590300556xwpbcw11877.jpg',
          'https://www.artbank.co.jp/stockillust/vol8_image/visualgenerallaboratory/1-S-CHD107.jpg',
          'https://images-na.ssl-images-amazon.com/images/I/619cmE%2B4EUL._AC_.jpg',
          'https://pbs.twimg.com/profile_images/1065419302256275456/y1oe1dOQ.jpg'
          ]

r = requests.post(
    "https://api.deepai.org/api/CNNMRF",
    data={
        'content': base64.b64encode(data.read()),
        # 'style': random.choice(styles),
        'style': styles[5],
    },
    headers={'api-key': 'ca6dafe3-27ec-4ed0-9c87-b11380bb396c'}
)

print(r.json())

# response = requests.get(r.json()['output_url'])
# image = response.content
#
# file_name = "tests/" + hashlib.md5(image).hexdigest() + ".jpg"
#
# with open(file_name, "wb") as aaa:
#     aaa.write(image)