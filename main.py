import requests
import base64
from PIL import Image
import time


class Product():
    def __init__(self, id, name, type):
        self.id = id
        self.name = name

        self.type = type


consts = {
    "url": "https://stage00.common.solumesl.com/common/api/v2/common/labels/image?company=JC07&store=1111",
    "headers": {
        'accept': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6Ilg1ZVhrNHh5b2pORnVtMWtsMll0djhkbE5QNC1jNTdkTzZRR1RWQndhTmsiLCJ0eXAiOiJKV1QifQ.eyJpZHAiOiJMb2NhbEFjY291bnQiLCJvaWQiOiIzODliYzBjNy1iMWM3LTRkN2MtODBhNC0yYzI1MGEzMmNjNzIiLCJzdWIiOiIzODliYzBjNy1iMWM3LTRkN2MtODBhNC0yYzI1MGEzMmNjNzIiLCJuYW1lIjoiYmliZWt5ZXNzIiwibmV3VXNlciI6ZmFsc2UsImV4dGVuc2lvbl9BZG1pbkFwcHJvdmVkIjp0cnVlLCJleHRlbnNpb25fQ3VzdG9tZXJDb2RlIjoiSkMwNyIsImV4dGVuc2lvbl9DdXN0b21lckxldmVsIjoiMSIsImVtYWlscyI6WyJiaWJla3llc3NAZ21haWwuY29tIl0sInRmcCI6IkIyQ18xX1JPUENfQXV0aCIsImF6cCI6ImUwOGU1NGZmLTViYjEtNGFlNy1hZmRlLWI5Y2RjOGZhMjNhZSIsInZlciI6IjEuMCIsImlhdCI6MTY5MjQyNTA3NiwiYXVkIjoiZTA4ZTU0ZmYtNWJiMS00YWU3LWFmZGUtYjljZGM4ZmEyM2FlIiwiZXhwIjoxNjkyNTExNDc2LCJpc3MiOiJodHRwczovL3NvbHVtYjJjLmIyY2xvZ2luLmNvbS9iMGM4ZTNkOS0wOGZhLTQ4N2EtYWZmMS04NWJhZTExZmM2YzUvdjIuMC8iLCJuYmYiOjE2OTI0MjUwNzZ9.ZkXG8eMzBX_ZAcFc14RVlB7TbRJmPyp9UuRpw78UFdLqwlHN8zHDr-VD8VOLiqM85FI06f_nDb17Dn44jMRQ3LYVkWR75__eL7qThKjp8lIUQX6N2kOY-9r2lCPpFK14jMbwBybXC6i65xl3q1GHFzKW3XxLALrN-4HI0zKp9Ki4CdV5Z1cxW7Sq6mAo2LKeQZkxfOKhXP4vhu1RBaZQuUQ5Dyfev-84eimjnRy6id2Nk77Tixoble0PrO1cktZoAO3MnnVMWRmuPzEwthQoKjDgW5lLulP8LIjOeTy2HEzEPqixdksw0HgySv1q9A3H-bDLlpIJtXunfWxRW3opvw',
        'Content-Type': 'application/json'
    },

}


def base64encoder(input_path, output_path, w, h):
    try:
        # Open the image file
        with Image.open(input_path) as img:
            # Resize the image
            img = img.resize((w, h))
            # Save the resized image to the output path

            img.save(output_path)

        with open(output_path, 'rb') as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')

        return base64_image
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""


def get_data(product, w, h):
    data = {
        "labelCode": product.id,
        "page": 1,
        "frontPage": 1,
        "image": base64encoder(f"./input_images/{product.name}.{product.type}", f"./output_images/{product.name}.{product.type}", w, h),
        "articleList": [
            {
                "articleId": "B100001",
                "articleName": product.name,
                "nfcUrl": "http://www.solumesl.com",
                "data": {
                    "ARTICLE_ID": "B100001",
                    "ARTICLE_NAME": product.name,
                    "NFC_URL": "http://www.solum.com/p/B100001",
                    "SALE_PRICE": "$100",
                    "DISCOUNT_PRICE": "$90"
                }
            }
        ]
    }
    return data


def upload_picture(w, h, products):
    for product in products:
        data = get_data(product, w, h)
        response = requests.post(
            consts["url"], json=data, headers=consts["headers"])

        if response.status_code == 200:
            print("Request was successful.")
        else:

            print(f"Request failed with status code: {response.status_code}")


if __name__ == "__main__":
    type = 'jpg'
    # for i in range(10):

    products = [Product('085C1A65E1DB', "im4", type),
                Product('085C1A73E1DC', "im4", type),
                Product('085C1B2EE1D5', "im4", type),
                ]

    new_width = 250  # Replace with the desired width
    new_height = 122  # Replace with the desired height

    upload_picture(
        new_width, new_height, products)
    # time.sleep(60)
