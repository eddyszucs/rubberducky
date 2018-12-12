import os
import time
import re
from slackclient import SlackClient

# instantiate the slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
bot_id = None

# consts
RTM_READ_DELAY = 1
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"



def parse_bot_commands(slack_events):
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == bot_id:
                return message, event["channel"]
    return None, None


def parse_direct_mention(messageText):
    matches = re.search(MENTION_REGEX, messageText)

    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)


def handle_command(command, channel):
    default_response = "What? Quack."

    # find and executes commands
    response = None
    if command == "commands":
        response = "You can use the following commands \"command\", \"help\", \"bye\"."
    elif command == "help":
        response = "Tell me your problem... quack"
    elif command == "bye":
        response = "K bye... :("

    slack_client.api_call("chat.postMessage",
                         channel=channel,
                         text=response or default_response
                         )


if (__name__ == "__main__"):
    if (slack_client.rtm_connect(with_team_state=False)):
        print("Rubber Ducky connected and running!")
        bot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if (command):
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed!")


