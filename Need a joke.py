import random
import tweepy
from api_keys import *
import os
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

joke = 'tell me a joke'
my_reply2 = ["AH", 'Ahh', 'AHAHAH']
mentions = api.mentions_timeline(retrieve_id(Last_id), mention_mode = "extended")

def joke():
    for mention in reversed(mentions):
        tweet_text = mention.text
        if joke in tweet_text.lower():
            reply_joke = random.choice(my_reply2)
            print('here')
            api.update_status("@" + mention.user.screen_name + ' ' + str(reply_joke), mention.id)
            print(colored('---Commented as :', 'yellow') + colored(reply_joke, 'yellow'))
            store_last_seen(Last_id, mention.id) 
        else:
            store_last_seen(Last_id, mention.id)
            print('no joke here 1')

joke()