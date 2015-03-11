import requests
import os
import shutil
import constants
FLICKER_URL = "https://api.flickr.com/services/rest"


def request_stream(tag=None, data=None):
    if not tag and not data:
        print "Please Mention a tag."
        return
    response = requests.post(FLICKER_URL, data)
    return response.json()


def make_url(**kwargs):
    FLICKR_PHOTO_URL = "https://farm{farm}.staticflickr.com/{server}/{id}_{secret}.jpg"
    return FLICKR_PHOTO_URL.format(**kwargs)

def test_request(tags=None):
    """
    Test the request.
    """
    if tags is None:
        return
    data = {
        "api_key": constants.FLICKR_KEY,
        "method": "flickr.photos.search",
        "tags": tags,
        "format": "json",
        "nojsoncallback": 1,
        "per_page": 500
    }
    response = request_stream(data=data)
    photos = response["photos"]["photo"]
    for photo in photos:
        try:
            get_image(tag=tags, **photo)
        except:
            errors = open('errors.txt', 'a+')
            errors.write(make_url(**photo)+"\n")


def get_image(tag="misc", **kwargs):
    """
    Given urls, download the image.
    """
    if not kwargs.get("id"):
        return
    photo_url = make_url(**kwargs)
    file_ext = photo_url[-4:]
    print photo_url
    response = requests.get(photo_url, stream=True)
    folder_path = os.path.join(os.getcwd(), "photos", tag)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    photo_file_url = os.path.join(folder_path, kwargs.get("id")+ file_ext)
    with open(photo_file_url, 'w') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response



if __name__ == "__main__":
    test_request(tags="dogs")
