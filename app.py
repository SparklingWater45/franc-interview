from flask import Flask, render_template, jsonify, Response, request
import datetime

app = Flask(__name__)


# converts the json string (time) into a python datetime object
def convertTime(strTime):
    format = "%Y-%m-%dT%H:%M:%SZ"
    convertedTime = datetime.datetime.strptime(strTime, format)
    return convertedTime


@app.route('/')
def index_view():
    
    username = request.args.get('username')
    tweets = []

    
    if(username): # if username provided

        all_users = users_view().get_json() # retrieve all users (for followers data)        
        followers = all_users[username] # create list of followers for main user
        followers.append(username)  # add user to list of followers (used to find all tweets)) 
        all_tweets = posts_view().get_json()  # retrieve all posts

        for follower in followers: # get tweets from each follower
            follower_tweets = all_tweets[follower]
            for tweet in follower_tweets:
                tweets.append([convertTime(tweet['time']),
                              tweet['status'], follower])

        tweets.sort(reverse=True) # sorts the tweets for each subarray index[0] (the date column)

    return render_template('index.html', username=username, tweets=tweets)

@app.route('/users')
def users_view():
    with open('./users.json', 'r') as f:
        users = f.read()
    return Response(users, mimetype="application/json")

@app.route('/posts')
def posts_view():
    with open('./posts.json', 'r') as f:
        posts = f.read()
    return Response(posts, mimetype="application/json")

if __name__ == '__main__':
    app.run(host='127.0.0.1')