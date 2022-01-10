# dm reader
## description
a curation tool. fetches your DMs using twitter's api v1.1 (reference [here](https://developer.twitter.com/en/docs/twitter-api/v1/direct-messages/sending-and-receiving/api-reference/list-events)). one use case would be to create a "bookmark-specific" twitter account specifically for the purpose of receiving noteworthy tweets.

## instructions
1. clone this repo
2. create a local `.env` file resembling the following: 
```
CONSUMER_KEY=
CONSUMER_SECRET=
ACCESS_TOKEN=
TOKEN_SECRET=
RECIPIENT_ID= # the recipient whose messages you're looking for
```
the first four are self-explanatory and can be fetched using a Twitter developer account.
3. pip install the relevant packages
4. run python script via `python3 app.py`

postman, as in the context of any api-related endeavor, is pretty clutch. for various reasons, use postman's environments to ensure that you don't accidentally publicly share any of your credentials.
https://www.youtube.com/watch?v=3X_rx7b7u2g

## todo
- write to gsheets/persist 