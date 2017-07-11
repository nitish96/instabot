import requests
import termcolor
import urllib
from wordcloud import WordCloud
import matplotlib.pyplot as plt

caption = []
ACCESS_TOKEN = "4067103159.e02ced5.354ea1cd0a9648469c69eadcbffa65b8"

BASE_URL = "https://api.instagram.com/v1/"

#this method will fetch my personal information
def my_info():

    request_url = BASE_URL + 'users/self/?access_token=%s' % ACCESS_TOKEN

    my_info = requests.get(request_url).json()

    if my_info['meta']['code'] == 200:
        if len(my_info['data']):
            print 'Username: %s' % (my_info['data']['username'])
            print 'No. of followers: %s' % (my_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (my_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (my_info['data']['counts']['media'])
        else:
            print 'Please Check the name'
    else:
        print 'STATUS NOT OK'


#this method is getting the id of my one of my friends
def get_friend_id(insta_user):
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_user, ACCESS_TOKEN)
    friend_info = requests.get(request_url).json()
    if friend_info['meta']['code'] == 200:
        if len(friend_info['data']):
            return friend_info['data'][0]['id']
        else:
            return None
    else:
        print 'STATUS NOT OK'

#this method will gather the information of the user using their unique id
def get_friend_info(insta_user):
    friend_id = get_friend_id(insta_user)
    if friend_id == None:
        print 'User does not exist!'
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (friend_id, ACCESS_TOKEN)
    friend_info = requests.get(request_url).json()

    if friend_info['meta']['code'] == 200:
        if len(friend_info['data']):
            print 'Username: %s' % (friend_info['data']['username'])
            print 'No. of followers: %s' % (friend_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (friend_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (friend_info['data']['counts']['media'])
        else:
            print 'oops! no data found'
    else:
        print 'STATUS NOT OK'

#this method will show my recent post
def get_my_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % ACCESS_TOKEN
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

#this method will get the recent post from one of your friends
def friend_media():
    friend_name=raw_input('enter the name of your frnd :')
    url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (friend_name, ACCESS_TOKEN)
    friend_details = requests.get(url).json()
    if friend_details['meta']['code'] == 200:
        if len(friend_details['data']):
            id = (friend_details['data'][0]['id'])
            request_url=(BASE_URL+'users/%s/media/recent/?access_token=%s'%(id,ACCESS_TOKEN))
            details_frnd=requests.get(request_url).json()
            if len(details_frnd['data']):
                image_name = details_frnd['data'][0]['id'] + '.jpeg'
                image_url = details_frnd['data'][0]['images']['standard_resolution']['url']
                urllib.urlretrieve(image_url, image_name)
                print 'image has been downloaded'

            else:
                 print 'data does not exist'
        else:
            print 'user not exist'
    else:
        print 'status error occured'

#this method will like your friend's post
def like_a_post():
    name = raw_input('enter your friend name')
    search_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (name, ACCESS_TOKEN)
    friend_details=requests.get(search_url).json()
    if friend_details['meta']['code'] == 200:
        if len(friend_details['data']):
            id = (friend_details['data'][0]['id'])
            request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s' % (id, ACCESS_TOKEN))
            post_details = requests.get(request_url).json()
            if post_details['meta']['code']==200:
                if len(post_details['data']):
                    post_id=post_details['data'][0]['id']
                    set_url=(BASE_URL+'media/%s/likes')%(post_id)
                    payLoad={'access_token':ACCESS_TOKEN}
                    post_like=requests.post(set_url,payLoad).json()
                    if post_like['meta']['code']==200:
                        print('Post liked')
                    else:
                        print 'Try again later'

                else:
                    print 'Try again later'

            else:
                print 'STATUS NOT OK'
        else:
            print 'wrong input name '
    else:
        print 'STATUS NOT OK'

#this method will post a comment on your friend's posts
def post_a_comment():
    name = raw_input('enter the name of the user :')
    url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (name, ACCESS_TOKEN)
    friend_details = requests.get(url).json()
    if friend_details['meta']['code'] == 200:

        if len(friend_details['data']):

            id = (friend_details['data'][0]['id'])
            request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s' % (id, ACCESS_TOKEN))
            show_media_details = requests.get(request_url).json()
            if show_media_details['meta']['code'] == 200:

                if len(show_media_details['data']):
                    media_id = show_media_details['data'][0]['id']
                    set_url = (BASE_URL + 'media/%s/comments') % (media_id)
                    comment_input = raw_input('enter your comment: ')
                    comment_payLoad = {'access_token': ACCESS_TOKEN, 'text': comment_input}
                    post_comment = requests.post(set_url, comment_payLoad).json()
                    if post_comment['meta']['code'] == 200:

                        print('Comment added successfully!')
            else:
                print 'STATUS NggOT OK'
        else:
            print 'oops! no data found'
    else:
        print 'STATUS NOT OK '
#this method will fetch the subtrends and plot a wordcloud for the same
def plot_wordcloud():
    name = raw_input('enter the name of the user :')
    url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (name, ACCESS_TOKEN)
    friend_details = requests.get(url).json()
    if friend_details['meta']['code'] == 200:
        if len(friend_details['data']):
            #id = []
            id = (friend_details['data'][0]['id'])
            if id == None:
                print 'user id does not exist : '
            else:
                url = (BASE_URL + 'users/%s/media/recent/?access_token=%s' % (id, ACCESS_TOKEN))
                posts_details = requests.get(url).json()
                if len(posts_details['data']):
                     k = posts_details['data'][0]['tags']
                     caption.append(k)

                print caption
                thefile = open('test.txt','w')

                for item in caption:
                    thefile.write("%s\n" % item)
                    thefile.close()
                    with open('test.txt', 'r') as myfile:

                        data = myfile.read()
                    print len(data)


                    # Generate a word cloud image
                    wordcloud = WordCloud().generate(data)

                    # Display the generated image:
                    plt.figure()
                    plt.imshow(wordcloud, interpolation="bilinear")
                    plt.axis("off")
                    plt.show()


        else:
            print 'data does not exist '
    else:
        print 'status error '



def start_app():
    print termcolor.colored('Welcome to instabot','red')
    pass_key = int(raw_input('Enter your pass key to access'))
    if pass_key == 1234 :
        print termcolor.colored('a. Look into your own account','blue')
        print termcolor.colored('b. Look into your friends account','blue')
        print termcolor.colored('c. Look at your recent media','blue')
        print termcolor.colored('d. Look at your friends recent media','blue')
        print termcolor.colored('e. Want to like your friends post?','blue')
        print termcolor.colored('f. Wish to comment on your friends picture?','blue')
        print termcolor.colored('g. Wish to plot a wordcloud of subtrends from your friends activity?','blue')

        your_choice = raw_input("Enter your choice")
        if your_choice == "a":
            my_info()
        if your_choice == "b":
            insta_user = raw_input('enter the user name')
            get_friend_info(insta_user)
        if your_choice == "c":
            get_my_post()
        if your_choice == "d":
            friend_media()
        if your_choice == "e":
            like_a_post()
        if your_choice == "f":
            post_a_comment()
        if your_choice == "g":
            plot_wordcloud()
    else:
        print 'Enter first four natural numbers'
start_app()