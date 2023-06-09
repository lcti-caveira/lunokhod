# Discord Bot Documentation

## Overview
This is a simple Discord bot written in Python that utilizes the `discord` library. The bot listens for incoming messages in Discord channels and responds to them based on predefined rules using the `responses.py` module.

## Prerequisites
- Python 3.x installed on your system.
- The `discord` library installed. You can install it using `pip install discord`.
- (Optional) [Install PyCharm](https://www.jetbrains.com/help/pycharm/installation-guide.html#toolbox)

## Getting Started
1. Make sure you have created a Discord bot and obtained the bot token. If you haven't done so, follow [this post](https://www.writebots.com/discord-bot-token/) to create a bot and retrieve the token.
2. Set the bot token as an environment variable named `DISCORD_TOKEN`. You can export the variable in your shell or set it in your preferred development environment.
3. Run it by executing `main.py`

## Code Explanation
### Importing Required Libraries

```python
import discord
from source import responses
import os
```
The necessary libraries are imported. discord is the library that provides the functionality to interact with the Discord API. responses contains the logic for handling user messages and generating appropriate responses. os is used to retrieve the Discord bot token from the environment variable.

### Setting the Discord Bot Token
```python
TOKEN = os.environ['DISCORD_TOKEN']
```
The Discord bot token is stored in the TOKEN variable. It is retrieved from the DISCORD_TOKEN environment variable using os.environ.

### Handling Message Sending
```python
async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)
```
The `send_message` function is responsible for sending a response to the user who sent the message. It takes the `message` object, the `user_message` content, and a boolean flag `is_private` indicating whether the response should be sent as a private message or in the channel.

The `responses.handle_response` function generates the appropriate response based on the `user_message`.

### Running the Discord Bot

The `run_discord_bot` function initializes the Discord bot by creating a `discord.Client` instance. It registers event handlers for the `on_ready` and `on_message` events.

The `on_ready` event is triggered when the bot successfully connects to Discord. It prints a message indicating that the bot is running.
The `on_message` event is triggered whenever a new message is received. It checks if the author is not the bot itself, prints the author's name and the content of the message, and then calls the `send_message` function to generate and send a response.

Finally, the bot is run by calling `client.run(TOKEN)`.

## Including further functionalities

You can modify and extend this `handle_response` function at `responses.py` to include additional message patterns and responses based on your desired bot behavior.




