import requests

APP_HOST = '0.0.0.0'
APP_PORT = 8080


def process_single_image(img_id):
    url = f'http://{APP_HOST}:{APP_PORT}/process_image/{img_id}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print('Failed to process image')


def process_multiple_images(img_ids):
    url = f'http://{APP_HOST}:{APP_PORT}/process_images'
    response = requests.post(url, json={'img_ids': img_ids})
    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print('Failed to process images')


if __name__ == '__main__':
    process_single_image(10022)
    process_multiple_images([10022, 9965])