import random
import tweepy
from api_keys import *
import os
import re
import time 

auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(api_access_token, api_access_token_secret)

# Empêche le script de spam alors qu'on reçoit une erreur 401, 404, 500 ou 503
api = tweepy.API(auth, retry_count=3, retry_delay=5,
                 retry_errors=set([401, 404, 500, 503]))

# Cette fonction permet de lire l'id stocké du dernier Tweet
def retrieve_id(Last_id):
    f_read = open(Last_id, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    print(last_seen_id)
    return last_seen_id

# Cette fonction permet d'écrire l'id du Tweet auquel le bot a répondu pour ne pas y répondre 2 fois
def store_last_seen(Last_id, last_seen_id):
    f_write = open(Last_id, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

# Last_id est le fichier txt qui contient l'idée de la dernière mention à laquelle le bot a répondu
file_to_find = "id_last_mention.txt"
Last_id = os.path.abspath(file_to_find)
print(Last_id)

meme = 'send me a meme'
reply_meme = [" Here is your dose of nonsense", " 'Nonsense delivery man knock on the door' ", " Dear customer here is your nonsense dishe", " Don't forget that if you say cusswords you're gonna go in jail and eat VEGETABLES", " Do you know what's nine plus ten ?"]

mentions = api.mentions_timeline(retrieve_id(Last_id), mention_mode = "extended")
while True:
    for mention in reversed(mentions):
        tweet_text = mention.text
        if meme in tweet_text.lower():
            print(str(mention.id) + ' - ' + str(mention.user.screen_name) + ' - ' + mention.text)
            image_bank_path = [os.path.abspath(x) for x in os.listdir(r'D:\Code\Bot Twitter\Twitter_bot\image_bank')]

            content = random.choice(image_bank_path)
            content_path = content.replace("\Twitter_bot", "\Twitter_bot\image_bank")

            text = random.choice(reply_meme)
            media = api.media_upload(content_path)

            api.update_status("@" + mention.user.screen_name + str(text), mention.id, media_ids = [media.media_id_string])
            print(colored('---Mention liked', 'green') + '  ' + colored('commented as :', 'yellow') + colored(text, 'magenta') + ', ' + colored('and the media was : ' + re.sub(r'^.*?image_bank', ' ', content_path) + '---', 'magenta'))
            store_last_seen(Last_id, mention.id)
        else:
            store_last_seen(Last_id, mention.id)
            print(colored('no meme here =C', 'red'))

    time.sleep(20)
    print('sleep')
        