import random
import tweepy
from api_keys import *
import os
import re

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

quoi = 'trouve moi' + 'quoi'
reply_feur = 'Feur'
mentions = api.mentions_timeline(retrieve_id(Last_id), mention_mode = "extended")
has_no_number = "Please check if you've enter a number and if it's under 10 and retry"

def has_numbers(inputString):
    return bool(re.search(r'\d', inputString))

for mention in reversed(mentions):
    tweet_text = mention.text
    if has_numbers(tweet_text) == True:       
        print(colored(tweet_text, 'yellow'))
        numbers = max(re.findall('\d', tweet_text))
        print(colored(numbers, 'green'))

    else:
        api.update_status("@" + mention.user.screen_name + str(has_no_number), mention.id)