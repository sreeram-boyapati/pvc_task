import constants
import os
import requests
import shutil
import sys
import traceback

FLICKER_URL = "https://api.flickr.com/services/rest"


def request_stream(tag=None, data=None):
    if not tag and not data:
        print "Please Mention a tag."
        return
    response = requests.post(FLICKER_URL, data)
    return response.json()


def make_url(**kwargs):
    """
    Generates URL from server, farm.
    """
    FLICKR_PHOTO_URL = "https://farm{farm}.staticflickr.com/{server}/{id}_{secret}.jpg"
    return FLICKR_PHOTO_URL.format(**kwargs)

def test_request(tags=None):
    """
    Test the request.
    """
    if tags is None:
        return
    string_tags = ",".join(tags)
    data = {
        "api_key": constants.FLICKR_KEY,
        "method": "flickr.photos.search",
        "tags": string_tags,
        "format": "json",
        "nojsoncallback": 1,
        "per_page": 500
    }
    response = request_stream(data=data)
    photos = response["photos"]["photo"]
    for photo in photos:
        try:
            get_image(tags=tags, **photo)
        except:
            tb= traceback.format_exc()
            errors = open('errors.txt', 'a+')
            errors.write(make_url(**photo)+"\n")
            errors.write(tb+"\n\n")
        break


def save_image_to_local(photo_url, tag, id):
    """
    Saves locally.
    """
    response = requests.get(photo_url, stream=True)
    folder_path = os.path.join(os.getcwd(), "photos", tag)
    print folder_path
    file_ext = photo_url[-4:]
    photo_file_url = os.path.join(folder_path, id + file_ext)
    print photo_file_url
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    with open(photo_file_url, 'w') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response


def get_image(tags=None, **kwargs):
    """
    Given urls, download the image.
    """
    if not kwargs.get("id") or tags is None:
        return
    photo_url = make_url(**kwargs)
    save_image_to_local(photo_url, tags[0], kwargs.get("id"))

if __name__ == "__main__":
    print sys.argv
    if len(sys.argv)  > 1:
        tags = []
        for i in range(1, len(sys.argv)):
            tags.append(sys.argv[i])
        test_request(tags=tags)
