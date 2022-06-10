import schedule
import requests
import os
import time
import shutil
from instagrapi import Client
from uuid import uuid4

THIS_PERSON_DOES_NOT_EXIST = 'https://thispersondoesnotexist.com/image'
DEFAULT_CAPTION = f'This Person does not exist!\nCredits to {THIS_PERSON_DOES_NOT_EXIST}'
CACHE_DIR = r'./.cache/'
FILE_EXTENSION = '.jpg'

def store_new_image() -> str:
    image_id = str(uuid4())
    response = requests.get(THIS_PERSON_DOES_NOT_EXIST, stream=True)
    if response.status_code != 200:
        print('Something went wrong when requesting new image.')
        print(f'Status Code = {response.status_code}')
        print(f'Content = {response.text}')
        return store_new_image()
    with open(CACHE_DIR + image_id + FILE_EXTENSION, 'wb') as image:
        shutil.copyfileobj(response.raw, image)
        image.close()
        print('Successfully downloaded new image: ' + image_id)
    return image_id

def post_new_image(client: Client, image: str, caption: str=DEFAULT_CAPTION):
    media = client.photo_upload(CACHE_DIR + image + FILE_EXTENSION, caption).dict()
    image_id, taken_at = media['id'], media['taken_at']
    print(f'Uploaded new Image {image}: \nid = {image_id}\ntaken_at = {taken_at}')

def run_schedule(client):
    image_id = store_new_image()
    post_new_image(client, image_id)
    
if __name__ == '__main__':
    print('Creating Cache storage if not existing...')
    if not os.path.exists(CACHE_DIR):
        os.mkdir(CACHE_DIR)
        print(f'Created {CACHE_DIR} for caching images')
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    client = Client()
    client.login(username, password)
    schedule.every(12).hours.do(run_schedule, client)
    while True:
        schedule.run_pending()
        time.sleep(5)
