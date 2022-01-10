from dotenv import load_dotenv
from requests_oauthlib import OAuth1
import os
import requests

load_dotenv()

consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
token_secret = os.getenv('TOKEN_SECRET')
recipient_id = os.getenv('RECIPIENT_ID')

auth = OAuth1(consumer_key, consumer_secret, access_token, token_secret)

def get_dms_list(cursor):
  response = requests.get('https://api.twitter.com/1.1/direct_messages/events/list.json', auth = auth, params = {
      'count': 50, # max; default is 20
      'cursor': None if not cursor else cursor # eh... default to none unless next_cursor is truthy
  })

  return response

def get_tweet(tweet_id):
  response = requests.get('https://api.twitter.com/1.1/statuses/show.json?id=%s' % tweet_id, auth = auth)

  print(response.json())
  return response

def fetch_dms():
  next_cursor = False

  msgs = []

  # need a highwater mark to recall where to stop parsing. this can be done using a database, but for now, let's fetch once per day
  # note: watch your rate limits
  # note2: we're only going two layers deep with quote tweets etc
  while next_cursor != None:
    response = get_dms_list(next_cursor)

    dms_json = response.json()

    for elem in dms_json['events']:
      msg_payload = elem['message_create']
      msg_data = msg_payload['message_data']

      if msg_payload['target']['recipient_id'] == recipient_id:
        linked_tweet_url = msg_data['entities']['urls'] and msg_data['entities']['urls'][0]['expanded_url'] # assume the first link is an embedded tweet
        linked_tweet_id = linked_tweet_url and linked_tweet_url.split('/')[-1] # get element following last '/'
        linked_tweet = linked_tweet_id and get_tweet(linked_tweet_id).json()
        linked_quoted_tweet = linked_tweet and linked_tweet['is_quote_status'] and linked_tweet['quoted_status'] # 2 layers deep here: dm --> linked tweet --> linked quoted tweet. there's a method to this madness

        # todo: add times of tweets + appendage; author(s) information
        msgs.append({
          'msg_id': elem['id'],
          'sender': msg_payload['sender_id'],
          'recipient': recipient_id,
          'text': msg_data['text'],
          # a lil nested action
          'linked_tweet': { 
            'tweet_id': linked_tweet_id,
            'text': linked_tweet and linked_tweet['text'],
          },
          'linked_quoted_tweet': {
            'tweet_id': linked_quoted_tweet and linked_quoted_tweet['id'],
            'text': linked_quoted_tweet and linked_quoted_tweet['text'],
          }
        })

    next_cursor = dms_json['next_cursor'] if 'next_cursor' in dms_json.keys() else None

  print(len(msgs))
  print(msgs)

# update a google sheet
def write_sheet():
  return

fetch_dms()
write_sheet()