Rubberducky

Configuration:

Install the requirements from the requirements.txt file.

You need to create a Slack App to recieve an API token for your bot. Create a bot user in the SlackApp go to Bot Users => Features and click "Add a Bot User". Click on the "Install App" under the "Settings" section. Once the App is installed, it displays a bot user oauth access token for authentication as the bot user.
Back in your terminal, export the Slack token with the name SLACK_BOT_TOKEN:

```export SLACK_BOT_TOKEN='your bot user access token here'```

Run the Bot on the command line with the ```python main.py``` command.
