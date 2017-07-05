import requests,urllib

ACCESS_TOKEN = "4067103159.e02ced5.354ea1cd0a9648469c69eadcbffa65b8"

BASE_URL = "https://api.instagram.com/v1/"


def my_info():

    request_url = BASE_URL + 'users/self/?access_token=%s' % ACCESS_TOKEN
    print 'GET request url : %s' % request_url
    my_info = requests.get(request_url).json()

    if my_info['meta']['code'] == 200:
        if len(my_info['data']):
            print 'Username: %s' % (my_info['data']['username'])
            print 'No. of followers: %s' % (my_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (my_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (my_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 received'
my_info()


def get_friend_id(insta_user):
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_user, ACCESS_TOKEN)
    print 'GET request url : %s' % request_url
    friend_info = requests.get(request_url).json()
    if friend_info['meta']['code'] == 200:
        if len(friend_info['data']):
            return friend_info['data'][0]['id']
        else:
            return None
    else:
        print 'Network Problem'


def get_friend_info(insta_user):
    friend_id = get_friend_id(insta_user)
    if friend_id == None:
        print 'User does not exist!'
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (friend_id, ACCESS_TOKEN)
    print 'GET request url : %s' % request_url
    friend_info = requests.get(request_url).json()

    if friend_info['meta']['code'] == 200:
        if len(friend_info['data']):
            print 'Username: %s' % (friend_info['data']['username'])
            print 'No. of followers: %s' % (friend_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (friend_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (friend_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'

def get_my_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'








insta_user = raw_input('enter the user name')





get_friend_info(insta_user)
