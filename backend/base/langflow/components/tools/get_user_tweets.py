import requests
from langflow.schema import Data
from langflow.inputs import MessageTextInput, IntInput, SecretStrInput
from langflow.custom import Component
from langflow.template import Output

class GetUserTweetsComponent(Component):
    display_name = "Get User Tweets"
    description = "This component retrieves recent tweets from a specified Twitter user using the Tweetscout API. Given a Twitter username, it first fetches the user’s unique ID and, if fully implemented, would then use that ID to retrieve their latest tweets."
    icon = "ShadowForge"
    name = "GetUserTweets"

    inputs = [
        MessageTextInput(
            name="username",
            display_name="Twitter Username",
            info="Enter the Twitter username of the user whose tweets you want to fetch. "
                 "Do not include the '@' symbol. For example, to fetch tweets from @elonmusk, enter 'elonmusk'.",
            required=True,
            tool_mode=True
        ),
        IntInput(
            name="tweet_count",
            display_name="Number of Tweets",
            value=10,
            info="Specify the number of recent tweets to retrieve. The default is 10. "
                 "The API will return up to this number of the latest tweets posted by the user.",
            required=True,
            tool_mode=True
        ),
        SecretStrInput(
            name="api_key",
            display_name="API Key",
            info="Provide your Tweetscout API key for authentication. "
                 "This key is required to access the API and fetch user tweet data.",
            required=True,
        )
    ]

    outputs = [
        Output(name="tweets_data", display_name="User Tweets Data", method="fetch_tweets"),
    ]

    def fetch_tweets(self) -> Data:
        """
            The task is to fetch the most recent tweets from a given Twitter username. This process involves two main steps:
                1.	Retrieve the User ID:
                •	Start by using the provided username to query the Twitter API to get user information. The username should be stripped of extra spaces before the request.
                •	Once the user information is retrieved, extract the user ID, which will be used to request their tweets.
                2.	Fetch Tweets:
                •	Using the retrieved user ID, query the API again to fetch a list of recent tweets.
                •	You should limit the number of tweets based on a configurable parameter (e.g., 20 tweets).
                •	For each tweet, include the following details:
                •	The full tweet text.
                •	The date and time when the tweet was posted.
                •	If available, include any quoted tweets and media links (such as images and videos).
            The output should present the tweets in a structured, readable format, showing:
                •	Each tweet’s text with a label (Tweet).
                •	The date when the tweet was posted.
                •	If the tweet includes any quoted content, it should be labeled and displayed.
                •	If there are any media files (e.g., video or image), include the media URL along with a label indicating whether it’s a video or image.

            The final output should summarize the tweets in a friendly and informative way. The result should include the formatted tweet data in a natural language prompt, ready for further use.
        """
        username = self.username
        tweet_count = self.tweet_count
        api_key = self.api_key

        tweets = []  # Store all the fetched tweets
        cursor = None  # Initialize cursor as None

        try:
            # Step 1: Get user info to retrieve user ID
            user_response = requests.get(f"https://api.tweetscout.io/v2/info/{username}", headers={
                "accept": "application/json",
                "ApiKey": api_key,
            })
            user_response.raise_for_status()

            user_data = user_response.json()
            user_id = user_data.get("id")

            # Step 2: Fetch tweets with pagination
            while len(tweets) < tweet_count:
                # If we already have a cursor, include it in the request to fetch next set of tweets
                user_tweets_payload = {
                    "user_id": user_id,
                    "limit": min(tweet_count - len(tweets), 10),  # Fetch remaining required tweets (max 10 per request)
                }

                if cursor:
                    user_tweets_payload["cursor"] = cursor

                user_tweets_response = requests.post("https://api.tweetscout.io/v2/user-tweets", json=user_tweets_payload, headers={
                    "accept": "application/json",
                    "ApiKey": api_key,
                })
                user_tweets_response.raise_for_status()

                user_tweets_data = user_tweets_response.json()

                # Step 3: Add the tweets to the result list
                tweets.extend(user_tweets_data.get("tweets", []))

                # Step 4: Check for next_cursor and update it if exists
                cursor = user_tweets_data.get("next_cursor")

                # If there's no next_cursor, we've reached the end of the results
                if not cursor:
                    break

            return Data(value={"result": tweets[:tweet_count]})

        except requests.exceptions.RequestException as e:
            return Data(value={"error": f"API request failed: {e}"})
        except Exception as e:
            return Data(value={"error": f"Unexpected error: {e}"})