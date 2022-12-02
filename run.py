#!/usr/bin/env python
import signal
import os
from flask import Flask, render_template, request, session
import argparse
import time
import threading
import random
import sys
from mtcnn.mtcnn import MTCNN
import cv2
import json
import random
from instabotai import ai
import subprocess
from shutil import copyfile
import re, io

try:
    input = raw_input
except NameError:
    pass

COOKIES = {}
app = Flask(__name__)

bot = ai.Bot(do_logout=True)

app.secret_key = str(random.random())
def logoutput_open(username):
    with open("static/" + username + "info.txt", "r+") as read_file:
        logoutput = read_file.read()
        return logoutput

def open_file(filename):
    username = session.get("username")
    with open(username + filename + ".txt", "r+") as f:
        filename = f.read()
        return filename

@app.route("/")
def index():
    return render_template("index.html");

@app.route("/login")
def login():
    return render_template("login.html");

@app.route("/challenge_solved", methods=['GET', 'POST'])
def challenge_solved():
    username = session.get("username")

    code = request.form['code']
    code = str(code)
#    process.communicate(input=code.encode())[1]
    time.sleep(5)
    profile_pic = open_file("profilepic")
    follower_count = open_file("followers_count")
    following_count = open_file("following_count")
    media_count = open_file("media_count")
    session["profile_pic"] = profile_pic
    session["follower_count"] = follower_count
    session["following_count"] = following_count
    session["media_count"] = media_count
    profile_pic = session.get("profile_pic")
    followers = session.get("follower_count")
    following = session.get("following_count")
    logoutput = logoutput_open(username)
    media_count = session.get("media_count")

    return render_template("logged_in.html", username=username,
                       profile_pic=profile_pic, followers=followers,
                       following=following, media_count=media_count);




@app.route("/start_logged_in", methods=['GET', 'POST'])
def start_logged_in():
    username = request.form['username']
    if username == "":
        logoutput = "Wrong Username"
        return render_template("login.html", username=username, logoutput=logoutput);
    password = request.form['password']
    if password == "":
        logoutput = "Wrong Password"
        return render_template("login.html", username=username, logoutput=logoutput);
    session["username"] = username
    session["password"] = password
    username = session.get("username")

    try:
        ai.Bots.user_login(username=username, password=password, proxys=None)
        time.sleep(5)
        ai.bot.api.get_self_username_info()
        profilepic = ai.bot.api.last_json["user"]["profile_pic_url"]
        followers_count = ai.bot.api.last_json["user"]["follower_count"]
        following_count = ai.bot.api.last_json["user"]["following_count"]
        media_count = ai.bot.api.last_json["user"]["media_count"]

        def write_file(filename, text):
            with open(username + filename + ".txt", "w+") as f:
                f.write(text)

        write_file("profilepic", str(profilepic))
        write_file("followers_count", str(followers_count))
        write_file("following_count", str(following_count))
        write_file("media_count", str(media_count))

        with open("check_password.txt", "r") as f:
            check_password = f.read()
            f.close()
            if check_password == "True":
                logoutput = "Wrong Password or username"
                with open("check_password.txt", "w+") as f:
                    f.write("False")
                    f.close()
                return render_template("login.html", logoutput=logoutput);

        with open("checkpoint.txt", "r") as f:
            checkpoint = f.read()
            f.close()
            if checkpoint == "True":
                logoutput = "Challenge send to your email"
                with open("checkpoint.txt", "w+") as f:
                    f.write("False")
                    f.close()
                return render_template("challenge_required.html", logoutput=logoutput);
#
    except Exception as e:
        ai.bot.logger.info(str(e))

    profile_pic = open_file("profilepic")
    follower_count = open_file("followers_count")
    following_count = open_file("following_count")
    media_count = open_file("media_count")
    session["profile_pic"] = profile_pic
    session["follower_count"] = follower_count
    session["following_count"] = following_count
    session["media_count"] = media_count
    profile_pic = session.get("profile_pic")
    followers = session.get("follower_count")
    following = session.get("following_count")
    logoutput = logoutput_open(username)
    media_count = session.get("media_count")
    return render_template("logged_in.html", username=username,
                       profile_pic=profile_pic, followers=followers,
                       following=following, media_count=media_count);

#    return render_template("logged_in.html", username=username,
#                           profile_pic=profile_pic, followers=followers,
#                           following=following, media_count=media_count, logoutput=logoutput);

@app.route("/activate")
def activate():
    username = session.get("username")
    profile_pic = session.get("profile_pic")
    followers = session.get("follower_count")
    following = session.get("following_count")
    media_count = session.get("media_count")
    return render_template("activate.html", username=username,
                           profile_pic=profile_pic, followers=followers,
                           following=following, media_count=media_count);

@app.route("/start_activate", methods=['GET', 'POST'])
def start_activate():
    x = 0
    username = session.get("username")
    profile_pic = session.get("profile_pic")
    followers = session.get("follower_count")
    following = session.get("following_count")
    media_count = session.get("media_count")
    code = request.form['code']
    ai.Bots.activate_code(code)
    return render_template("activate.html", username=username,
                       profile_pic=profile_pic, followers=followers,
                       following=following, media_count=media_count);

#@app.route("/like_comments")
#def like_comments():
#    ai.bot.api.get_self_username_info()
#    profile_pic = ai.bot.api.last_json["user"]["profile_pic_url"]
#    followers = ai.bot.api.last_json["user"]["follower_count"]
#    following = ai.bot.api.last_json["user"]["following_count"]
#    media_count = ai.bot.api.last_json["user"]["media_count"]
#
#    return render_template("like_comments.html", username=username,
#                           profile_pic=profile_pic, followers=followers,
#                           following=following, media_count=media_count);

@app.route("/watch_infinity_stories")
def watch_infinity_stories():
#    ai.bot.api.get_self_username_info()
    username = session.get("username")
    profile_pic = session.get("profile_pic")
    followers = session.get("follower_count")
    following = session.get("following_count")
    media_count = session.get("media_count")

    return render_template("watch_stories.html", username=username,
                           profile_pic=profile_pic, followers=followers,
                           following=following, media_count=media_count);

#@app.route("/multibot")
#def multibots():
#    ai.bot.api.get_self_username_info()
#    profile_pic = ai.bot.api.last_json["user"]["profile_pic_url"]
#    followers = ai.bot.api.last_json["user"]["follower_count"]
#    following = ai.bot.api.last_json["user"]["following_count"]
#    media_count = ai.bot.api.last_json["user"]["media_count"]

#    return render_template("multibot.html", username=username,
#                           profile_pic=profile_pic, followers=followers,
#                           following=following, media_count=media_count);

#@app.route("/like_followers")
#def like_followers():
#    ai.bot.api.get_self_username_info()
#    profile_pic = ai.bot.api.last_json["user"]["profile_pic_url"]
#    followers = ai.bot.api.last_json["user"]["follower_count"]
#    following = ai.bot.api.last_json["user"]["following_count"]
#    media_count = ai.bot.api.last_json["user"]["media_count"]

#    return render_template("like_followers.html", username=username,
#                           profile_pic=profile_pic, followers=followers,
#                           following=following, media_count=media_count);

#@app.route("/like_following")
#def like_following():
#    ai.bot.api.get_self_username_info()
#    profile_pic = ai.bot.api.last_json["user"]["profile_pic_url"]
#    followers = ai.bot.api.last_json["user"]["follower_count"]
#    following = ai.bot.api.last_json["user"]["following_count"]
#    media_count = ai.bot.api.last_json["user"]["media_count"]

#    return render_template("like_following.html", username=username,
#                           profile_pic=profile_pic, followers=followers,
#                           following=following, media_count=media_count);

@app.route("/repost_images_ai")
def repost_images_ai():
    username = session.get("username")
    profile_pic = session.get("profile_pic")
    followers = session.get("follower_count")
    following = session.get("following_count")
    media_count = session.get("media_count")
    logoutput = logoutput_open(username)

    return render_template("repost_users_images.html", username=username,
                           profile_pic=profile_pic, followers=followers,
                           following=following, media_count=media_count, logoutput=logoutput);

@app.route("/unfollow_non_followers")
def unfollow_non_followers():
    username = session.get("username")
    profile_pic = session.get("profile_pic")
    followers = session.get("follower_count")
    following = session.get("following_count")
    media_count = session.get("media_count")
    logoutput = logoutput_open(username)

    return render_template("unfollow_non_followers.html", username=username,
                           profile_pic=profile_pic, followers=followers,
                           following=following, media_count=media_count, logoutput=logoutput);

@app.route("/like_followingai")
def like_followingai():
    username = session.get("username")
    profile_pic = session.get("profile_pic")
    followers = session.get("follower_count")
    following = session.get("following_count")
    media_count = session.get("media_count")
    logoutput = logoutput_open(username)

    return render_template("like_followingai.html", username=username,
                           profile_pic=profile_pic, followers=followers,
                           following=following, media_count=media_count, logoutput=logoutput);

@app.route("/like_followersai")
def like_followersai():
    username = session.get("username")
    profile_pic = session.get("profile_pic")
    followers = session.get("follower_count")
    following = session.get("following_count")
    media_count = session.get("media_count")
    return render_template("like_followersai.html", username=username,
                           profile_pic=profile_pic, followers=followers,
                           following=following, media_count=media_count);

#@app.route("/like_hashtags")
#def like_hashtags():
#    ai.bot.api.get_self_username_info()
#    profile_pic = ai.bot.api.last_json["user"]["profile_pic_url"]
#    followers = ai.bot.api.last_json["user"]["follower_count"]
#    following = ai.bot.api.last_json["user"]["following_count"]
#    media_count = ai.bot.api.last_json["user"]["media_count"]

#    return render_template("like_hashtags.html", username=username,
#                           profile_pic=profile_pic, followers=followers,
#                           following=following, media_count=media_count);

@app.route("/like_hashtagsai")
def like_hashtagsai():
    username = session.get("username")
    profile_pic = session.get("profile_pic")
    followers = session.get("follower_count")
    following = session.get("following_count")
    media_count = session.get("media_count")
    hashtag = "fitness"

    return render_template("like_hashtagsai.html", username=hashtag,
                           profile_pic=profile_pic, followers=followers,
                           following=following, media_count=media_count);

@app.route("/follow_followers")
def follow_followers():
    profile_pic = session.get("profile_pic")
    followers = session.get("follower_count")
    following = session.get("following_count")
    media_count = session.get("media_count")
    username = session.get("username")

    return render_template("follow_followers.html", username=username,
                           profile_pic=profile_pic, followers=followers,
                           following=following, media_count=media_count);

@app.route("/follow_following")
def follow_following():
    profile_pic = session.get("profile_pic")
    followers = session.get("follower_count")
    following = session.get("following_count")
    media_count = session.get("media_count")
    username = session.get("username")

    return render_template("follow_following.html", username=username,
                           profile_pic=profile_pic, followers=followers,
                           following=following, media_count=media_count);

#@app.route("/comment_followers")
#def comment_followers():
 #   ai.bot.api.get_self_username_info()
  #  profile_pic = ai.bot.api.last_json["user"]["profile_pic_url"]
   # followers = ai.bot.api.last_json["user"]["follower_count"]
  #  following = ai.bot.api.last_json["user"]["following_count"]
  #  media_count = ai.bot.api.last_json["user"]["media_count"]

   # return render_template("comment_followers.html", username=username,
    #                       profile_pic=profile_pic, followers=followers,
     #                      following=following, media_count=media_count);

#@app.route("/comment_following")
#def comment_following():
#    ai.bot.api.get_self_username_info()
 #   profile_pic = ai.bot.api.last_json["user"]["profile_pic_url"]
  #  followers = ai.bot.api.last_json["user"]["follower_count"]
   # following = ai.bot.api.last_json["user"]["following_count"]
   # media_count = ai.bot.api.last_json["user"]["media_count"]

   # return render_template("comment_following.html", username=username,
    #                       profile_pic=profile_pic, followers=followers,
     #                      following=following, media_count=media_count);

#@app.route("/like_self_media_comments")
#def like_self_media_comments():
#    ai.bot.api.get_self_username_info()
 #   profile_pic = ai.bot.api.last_json["user"]["profile_pic_url"]
  #  followers = ai.bot.api.last_json["user"]["follower_count"]
   # following = ai.bot.api.last_json["user"]["following_count"]
#    media_count = ai.bot.api.last_json["user"]["media_count"]

 #   x = 0
  #  y = 0
   # while True:
    #    try:
     #       ai.bot.api.get_total_self_user_feed(min_timestamp=None)
      #      item = ai.bot.api.last_json["items"][x]["caption"]["media_id"]
       #     ai.bot.like_media_comments(item)
        #    print("sleeping for 120 seconds")
         #   time.sleep(120)
          #  x += 1
#            y = 0
#            print("Like comments on next picture")
#        except:
#            time.sleep(120)
#            print("Like comments on next picture")
#            x += 1
#            if y == 4:
#                x = 0
#    return render_template("like_self_media_comments.html", username=username,
#                       profile_pic=profile_pic, followers=followers,
#                       following=following, media_count=media_count);

@app.route("/start_repost_images", methods=['GET', 'POST'])
def start_repost_images():
    username = session.get("username")
    profile_pic = session.get("profile_pic")
    followers = session.get("follower_count")
    following = session.get("following_count")
    media_count = session.get("media_count")
    password = session.get("password")
    followers_username = request.form['following_username']
    img_caption = request.form['img_caption']
    time_sleep = request.form['time_sleep']
    time_sleep = int(time_sleep)
    ai.Bots.repost_users_images(followers_username, img_caption, time_sleep)
#    process = subprocess.Popen(["python repost_users_images.py " "-u " + username + " -p " + password + " -user " + "'" + followers_username + "'" + " -caption " + "'" + img_caption + "'" + " -sleep " + time_sleep], shell=True)

    return render_template("repost_users_images.html", username=username)


@app.route("/start_unfollow_non_followers", methods=['GET', 'POST'])
def start_unfollow_non_followers():
    username = session.get("username")
    profile_pic = session.get("profile_pic")
    followers = session.get("follower_count")
    following = session.get("following_count")
    media_count = session.get("media_count")
    password = session.get("password")
    ai.Bots.unfollow_non_followers()
#    process = subprocess.Popen(["python unfollow_nonfollowers.py " "-u " + username + " -p " + password], shell=True)

    return render_template("unfollow_non_followers.html", username=username)


@app.route("/start_like_followingai", methods=['GET', 'POST'])
def start_like_followingai():
    x = 0
    username = session.get("username")
    profile_pic = session.get("profile_pic")
    followers = session.get("follower_count")
    following = session.get("following_count")
    media_count = session.get("media_count")
    password = session.get("password")
    followers_username = request.form['following_username']
    time_sleep = request.form['time_sleep']
    time_sleep = int(time_sleep)
    ai.Bots.like_following(followers_username, time_sleep)
#    process = subprocess.Popen(["python like_followingai.py " "-u " + username + " -p " + password + " -user " + followers_username + " -sleep " + time_sleep], shell=True)

    return render_template("like_followingai.html", username=username)


@app.route("/stop_like_followingai", methods=['GET', 'POST'])
def stop_like_followingai():
    username = session.get("username")
    subprocess = session.get("subprocess")
    os.kill(subprocess, signal.SIGTERM)
    profile_pic = ai.bot.api.last_json["user"]["profile_pic_url"]
    followers = ai.bot.api.last_json["user"]["follower_count"]
    following = ai.bot.api.last_json["user"]["following_count"]
    media_count = ai.bot.api.last_json["user"]["media_count"]

    return render_template("like_followingai.html", username=username,
                       profile_pic=profile_pic, followers=followers,
                       following=following, media_count=media_count);

@app.route("/comment_hashtagai")
def comment_hashtag_ai():
    username = session.get("username")
    profile_pic = session.get("profile_pic")
    followers = session.get("follower_count")
    following = session.get("following_count")
    media_count = session.get("media_count")
    pre_hashtag = "fitness, follow4follow"
    main_comment = "hello awesome profile, wow nice profile, follow me pls"
    return render_template("comment_hashtagai.html", username=pre_hashtag,
                           profile_pic=profile_pic, followers=followers,
                           following=following, media_count=media_count,
                           main_comment=main_comment);

@app.route("/start_comment_hashtagsai", methods=['GET', 'POST'])
def start_comment_hashtagsai():
    username = session.get("username")
    password = session.get("password")
    profile_pic = session.get("profile_pic")
    followers = session.get("follower_count")
    following = session.get("following_count")
    media_count = session.get("media_count")
    x = 0
    number_last_photos = 1
    hashtags = request.form['following_username']
    comment = request.form['comment']
    time_sleep = request.form['time_sleep']
    time_sleep = int(time_sleep)
    ai.Bots.user_hashtag_comment(hashtags, comment, time_sleep)
#    process = subprocess.Popen(["python comment_hashtagsai.py " "-u " + username + " -p " + password + " -hashtags " + "'" + hashtags + "'" + " -comment " + "'" + comment + "'" + " -sleep " + time_sleep], shell=True)
#    session["subprocess"] = process.pid
#    ai.Bots.user_hashtag_comment(hashtags, comment, time_sleep)
    return render_template("comment_hashtagai.html", username=username,
                       profile_pic=profile_pic, followers=followers,
                       following=following, media_count=media_count);

@app.route("/stop_comment_hasgtahai", methods=['GET', 'POST'])
def stop_comment_hashtagai():
    username = session.get("username")
    subprocess = session.get("subprocess")
    os.kill(subprocess, signal.SIGTERM)
    profile_pic = ai.bot.api.last_json["user"]["profile_pic_url"]
    followers = ai.bot.api.last_json["user"]["follower_count"]
    following = ai.bot.api.last_json["user"]["following_count"]
    media_count = ai.bot.api.last_json["user"]["media_count"]

    return render_template("like_followingai.html", username=username,
                       profile_pic=profile_pic, followers=followers,
                       following=following, media_count=media_count);

@app.route("/start_like_following", methods=['GET', 'POST'])
def start_like_following():
    username = session.get("username")
    password = session.get("password")
    profile_pic = session.get("profile_pic")
    followers = session.get("follower_count")
    following = session.get("following_count")
    media_count = session.get("media_count")
    following_username = request.form['following_username']
    ai.bot.like_following(following_username)
    return render_template("like_following.html", username=username,
                       profile_pic=profile_pic, followers=followers,
                       following=following, media_count=media_count);

@app.route("/start_like_followersai", methods=['GET', 'POST'])
def start_like_followersai():
    x = 0
    username = session.get("username")
    profile_pic = session.get("profile_pic")
    followers = session.get("follower_count")
    following = session.get("following_count")
    media_count = session.get("media_count")
    password = session.get("password")
    followers_username = request.form['following_username']
    time_sleep = request.form['time_sleep']
    time_sleep = int(time_sleep)
    ai.Bots.like_followers(followers_username, time_sleep)
#    process = subprocess.Popen(["python like_followersai.py " "-u " + username + " -p " + password + " -user " + followers_username + " -sleep " + time_sleep], shell=True)
#    session["subprocess"] = process.pid
    return render_template("like_followersai.html", username=username,
                       profile_pic=profile_pic, followers=followers,
                       following=following, media_count=media_count);

@app.route("/stop_like_followersai", methods=['GET', 'POST'])
def stop_like_followers():
    username = session.get("username")
    subprocess = session.get("subprocess")
    os.kill(subprocess, signal.SIGTERM)
    profile_pic = ai.bot.api.last_json["user"]["profile_pic_url"]
    followers = ai.bot.api.last_json["user"]["follower_count"]
    following = ai.bot.api.last_json["user"]["following_count"]
    media_count = ai.bot.api.last_json["user"]["media_count"]

    return render_template("like_followingai.html", username=username,
                       profile_pic=profile_pic, followers=followers,
                       following=following, media_count=media_count);


@app.route("/start_like_hashtagsai", methods=['GET', 'POST'])
def start_like_hashtagsai():
    username = session.get("username")
    password = session.get("password")
    profile_pic = session.get("profile_pic")
    followers = session.get("follower_count")
    following = session.get("following_count")
    media_count = session.get("media_count")
    x = 0
    number_last_photos = 1
    hashtags = request.form['following_username']
    time_sleep = request.form['time_sleep']
    time_sleep = int(time_sleep)
    ai.Bots.like_hashtags(hashtags, time_sleep)
#    process = subprocess.Popen(["python like_hashtagsai.py " "-u " + username + " -p " + password + " -user " + hashtags + " -sleep " + time_sleep], shell=True)
#    session["subprocess"] = process.pid

    return render_template("like_followersai.html", username=username,
                       profile_pic=profile_pic, followers=followers,
                       following=following, media_count=media_count);

@app.route("/stop_like_hasgtahai", methods=['GET', 'POST'])
def stop_like_hashtagai():
    username = session.get("username")
    subprocess = session.get("subprocess")
    os.kill(subprocess, signal.SIGTERM)
    profile_pic = ai.bot.api.last_json["user"]["profile_pic_url"]
    followers = ai.bot.api.last_json["user"]["follower_count"]
    following = ai.bot.api.last_json["user"]["following_count"]
    media_count = ai.bot.api.last_json["user"]["media_count"]

    return render_template("like_followingai.html", username=username,
                       profile_pic=profile_pic, followers=followers,
                       following=following, media_count=media_count);

@app.route("/start_like_followers", methods=['GET', 'POST'])
def start_like_followers():
    username = session.get("username")
    password = session.get("password")
    profile_pic = session.get("profile_pic")
    followers = session.get("follower_count")
    following = session.get("following_count")
    media_count = session.get("media_count")

    followers_username = request.form['followers_username']
    ai.bot.like_followers(followers_username)
#    process = subprocess.Popen(["python like_followersgai.py " "-u " + username + " -p " + password + " -user " + followers_username + " -sleep " + time_sleep], shell=True)
#    session["subprocess"] = process.pid

    return render_template("like_followers.html", username=username,
                       profile_pic=profile_pic, followers=followers,
                       following=following, media_count=media_count);

@app.route("/start_follow_followers", methods=['GET', 'POST'])
def start_follow_followers():
    username = session.get("username")
    password = session.get("password")
    profile_pic = session.get("profile_pic")
    followers = session.get("follower_count")
    following = session.get("following_count")
    media_count = session.get("media_count")

    time_sleep = request.form['time_sleep']
    time_sleep = str(time_sleep)
    followers_username = request.form['followers_username']
#    ai.bot.follow_followers(followers_username)
    followers_username = str(followers_username)
    time_sleep = int(time_sleep)
    ai.Bots.follow_users_followers_ai(followers_username, time_sleep)
#    process = subprocess.Popen(["python follow_followers.py " "-u " + username + " -p " + password + " -user " + followers_username + " -sleep " + time_sleep], shell=True)
 #   session["subprocess"] = process.pid

    return render_template("follow_followers.html", username=username,
                       profile_pic=profile_pic, followers=followers,
                       following=following, media_count=media_count);

@app.route("/start_follow_following", methods=['GET', 'POST'])
def start_follow_following():
    username = session.get("username")
    password = session.get("password")
    profile_pic = session.get("profile_pic")
    followers = session.get("follower_count")
    following = session.get("following_count")
    media_count = session.get("media_count")
    time_sleep = request.form['time_sleep']
    time_sleep = str(time_sleep)
    followers_username = request.form['followers_username']
    followers_username = str(followers_username)
    time_sleep = int(time_sleep)
    ai.Bots.follow_users_following_ai(followers_username, time_sleep)
#    ai.bot.follow_following(followers_username)
#    process = subprocess.Popen(["python follow_following.py " "-u " + username + " -p " + password + " -user " + followers_username + " -sleep " + time_sleep], shell=True)
#    session["subprocess"] = process.pid

    return render_template("follow_followings.html", username=username,
                       profile_pic=profile_pic, followers=followers,
                       following=following, media_count=media_count);

@app.route("/start_comment_followers", methods=['GET', 'POST'])
def start_comment_followers():
    username = session.get("username")
    password = session.get("password")

    ai.bot.api.get_self_username_info()
    profile_pic = ai.bot.api.last_json["user"]["profile_pic_url"]
    followers = ai.bot.api.last_json["user"]["follower_count"]
    following = ai.bot.api.last_json["user"]["following_count"]
    media_count = ai.bot.api.last_json["user"]["media_count"]

    followers_username = request.form['followers_username']
    comment = request.form['comment']
    user_id = ai.bot.get_user_id_from_username(followers_username)
    total_followings = ai.bot.api.get_total_followers(user_id)
    for user in ai.bot.api.last_json["users"]:
        userid = ai.bot.get_user_id_from_username(user["username"])
        for user_id in userid:
            for media_id in ai.bot.get_last_user_medias(user_id, 2):
                print(ai.bot.api.comment(media_id, comment))
                print("Commented " + ai.bot.get_link_from_media_id(media_id))
                time.sleep(20)

    return render_template("comment_followers.html", username=username,
                        profile_pic=profile_pic, followers=followers,
                        following=following, media_count=media_count);

@app.route("/start_comment_following", methods=['GET', 'POST'])
def start_comment_following():
    username = session.get("username")
    password = session.get("password")

    ai.bot.api.get_self_username_info()
    profile_pic = ai.bot.api.last_json["user"]["profile_pic_url"]
    followers = ai.bot.api.last_json["user"]["follower_count"]
    following = ai.bot.api.last_json["user"]["following_count"]
    media_count = ai.bot.api.last_json["user"]["media_count"]

    followers_username = request.form['followers_username']
    comment = request.form['comment']
    user_id = ai.bot.get_user_id_from_username(followers_username)
    total_followings = ai.bot.api.get_total_followings(user_id)
    for user in ai.bot.api.last_json["users"]:
        userid = ai.bot.get_user_id_from_username(user["username"])
        for user_id in userid:
            for media_id in ai.bot.get_last_user_medias(user_id, 2):
                print(ai.bot.api.comment(media_id, comment))
                print("Commented " + ai.bot.get_link_from_media_id(media_id))
                time.sleep(20)

    return render_template("comment_following.html", username=username,
                       profile_pic=profile_pic, followers=followers,
                       following=following, media_count=media_count);

@app.route("/start_like_hashtags", methods=['GET', 'POST'])
def start_like_hashtag():
    username = session.get("username")
    password = session.get("password")

    ai.bot.api.get_self_username_info()
    profile_pic = ai.bot.api.last_json["user"]["profile_pic_url"]
    followers = ai.bot.api.last_json["user"]["follower_count"]
    following = ai.bot.api.last_json["user"]["following_count"]
    media_count = ai.bot.api.last_json["user"]["media_count"]

    hashtag = request.form['hashtag']
    ai.bot.like_following(hashtag)
    return render_template("like_hashtags.html", username=username,
                       profile_pic=profile_pic, followers=followers,
                       following=following, media_count=media_count);

@app.route("/start_watch_stories", methods=['GET', 'POST'])
def watch_all_stories():
    username = session.get("username")
    password = session.get("password")
    profile_pic = session.get("profile_pic")
    followers = session.get("follower_count")
    following = session.get("following_count")
    media_count = session.get("media_count")

    number_last_photos = 1
    following_username = request.form['following_username']
    time_sleep = request.form['time_sleep']
    time_sleep = int(time_sleep)
    ai.Bots.watch_stories(following_username, time_sleep)
#    ai.Bots.like_following(following_username, time_sleep)
#    process = subprocess.Popen(["python watch_stories.py " "-u " + username + " -p " + password + " -user " + following_username + " -sleep " + time_sleep], shell=True)
#    session["subprocess"] = process.pid

    return render_template("watch_stories.html", username=username,
                           profile_pic=profile_pic, followers=followers,
                           following=following, media_count=media_count);


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=False)
