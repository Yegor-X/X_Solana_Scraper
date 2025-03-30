from twikit import Client, TooManyRequests
import asyncio
import time
from datetime import datetime, timedelta
import csv
import re
from configparser import ConfigParser
from random import randint
import pandas as pd
from parse_llm import parse_with_ollama
import os


def split_content(content, max_length=6000):
    return [
        content[i: i + max_length] for i in range(0, len(content), max_length)
    ]

def clean_body_content(body_content):
    cleaned_content = "\n".join(
        line.strip() for line in body_content.splitlines() if line.strip()
    )
    return cleaned_content


end_date = datetime.today().strftime('%Y-%m-%d')
start_date = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')
QUERY = f'solana until:{end_date} since:{start_date} -filter:replies'

config = ConfigParser()
config.read('config.ini')
username = config['X']['username']
email = config['X']['email']
password = config['X']['password']

client = Client(language='en-US')

async def get_tweets(tweets):
    if tweets is None:
        print(f'{datetime.now()} - Getting tweets...')
        tweets = await client.search_tweet(QUERY, product='Latest')
    else:
        wait_time = randint(5, 10)
        print(f'{datetime.now()} - Getting next tweets after {wait_time} seconds...')
        await asyncio.sleep(wait_time)
        tweets = await tweets.next()
    return tweets


async def main():
    client.load_cookies("cookies.json")  # Authenticate (login data is in this cookies file)

    # Create CSV file
    with open("tweets.csv", "w", newline="", encoding="utf-8-sig") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Tweet_count", "Username", "Text", "Created At", "Retweets", "Likes"])

    tweet_count = 0
    tweets = None

    MINIMUM_TWEETS = 10
    while tweet_count < MINIMUM_TWEETS: # if you want to have results for the whole week, put "while True:" instead
        try:
            tweets = await get_tweets(tweets)  # Await the function
        except TooManyRequests as e:
            rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
            wait_time = (rate_limit_reset - datetime.now()).total_seconds()
            print(f'{datetime.now()} - Rate limit reached. Waiting {wait_time:.2f} seconds...')
            await asyncio.sleep(wait_time)  # Use asyncio.sleep()
            continue
        # except Exception as ex:
        #     print(f"Collecting ended. Exception: {ex}")   # log the error

        if not tweets:
            print(f'{datetime.now()} - No more tweets found')
            break

        for tweet in tweets:
            tweet_count += 1
            tweet_data = [tweet_count, tweet.user.name, tweet.text, tweet.created_at, tweet.retweet_count, tweet.favorite_count]

            with open("tweets.csv", "a", newline="", encoding="utf-8-sig") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(tweet_data)

        print(f'{datetime.now()} - Got {tweet_count} tweets')

    print(f'{datetime.now()} - Done! Got {tweet_count} tweets')



if __name__ == '__main__':
    asyncio.run(main())  # Run the async function

    parse_description = "This is text from Twitter post. Score the post based on relevance, risk, and reliability to Solana. Answer, like in the example: **Relevance:** 3/10  **Risk:** 6/10  **Reliability:** 4/10"

    with open("tweets.csv", "r", newline="", encoding="utf-8-sig") as csvfile:
        data = pd.read_csv(csvfile)
    llm_text = []
    for text in data["Text"]:
        cleaned_content = clean_body_content(text)
        dom_chunks = split_content(cleaned_content)
        result = parse_with_ollama(dom_chunks, parse_description)
        result_without_thinking = cleaned_text = re.sub(r"<think>.*?</think>\s*", "", result, flags=re.DOTALL)
        llm_text.append(result_without_thinking)
        print(result_without_thinking)
    data["LLM Analitics"] = llm_text
    data.to_csv("data_with_llm_analitics.csv", index=False)
    os.remove("tweets.csv")






