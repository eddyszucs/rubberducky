import os
import time
import re
from slackclient import SlackClient

# instantiate the slack client
slackClient = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
botId = None

# consts
RTM_READ_DELAY = 1
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"



def parseBotCommands(slackEvents):
    for event in slackEvents:
        if event["type"] == "message" and not "subtype" in event:
            userId, message = parseDirectMention(event["text"])
            if userId == botId:
                return message, event["channel"]
    return None, None


def parseDirectMention(messageText):
    matches = re.search(MENTION_REGEX, messageText)

    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)


def handleCommand(command, channel):
    defaultResponse = "What? Quack."

    # find and executes commands
    response = None
    if command == "commands":
        response = "You can use the following commands \"command\", \"help\", \"bye\"."
    elif command == "help":
        response = "Tell me your problem... quack"
    elif command == "bye":
        response = "K bye... :("

    slackClient.api_call("chat.postMessage",
                         channel=channel,
                         text=response or defaultResponse
                         )


if (__name__ == "__main__"):
    if (slackClient.rtm_connect(with_team_state=False)):
        print("Rubber Ducky connected and running!")
        botId = slackClient.api_call("auth.test")["user_id"]
        while True:
            command, channel = parseBotCommands(slackClient.rtm_read())
            if (command):
                handleCommand(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed!")


