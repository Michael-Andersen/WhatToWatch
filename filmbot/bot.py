import tweepy
import logging
import re
import lb

logger = logging.getLogger()


def config(consumer_key, consumer_secret, access_token, access_token_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api


def check_mentions(api, keywords, since_id):
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
                               since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue
        logger.info(tweet.text)
        if any(keyword in tweet.text.lower() for keyword in keywords):
            logger.info(f"Answering to {tweet.user.name}")
            tags = tweet.text.split('#')[1].strip()
            words = re.findall('[A-Z][^A-Z0-9]*|[0-9]+', tags)
            film = '-'.join(words)
            reply(api, tweet.user.screen_name, tweet.id_str, film.lower())
    logger.info(f"new since id {new_since_id}")
    return new_since_id


def reply(api, user, user_id, film):
    recommendations = lb.films_with_like_count(film, user_count=10, like_count=5)
    if len(recommendations) == 0:
        api.update_status(
            status=f"@{user} I'm sorry I could not find any recommendations, make sure you've formatted "
                   f"your request correctly and are using the same name that letterboxd uses to identify "
                   f"your film.",
            in_reply_to_status_id=user_id
        )
    else:
        recommendations = [item.split('-') for item in recommendations]
        recommendations = [[item[0].upper() + item[1:] for item in sublist] for sublist in recommendations]
        recommendations = [''.join(item) for item in recommendations]
        recommendations = [f'#{item}' for item in recommendations]
        recommendations[-1] = f'and {recommendations[-1]}'
        film_str = ', '.join(recommendations)
        api.update_status(
            status=f"@{user} I recommend: {film_str}",
            in_reply_to_status_id=user_id
        )
