import json
import os


def handle_response(message) -> str:
    print(f'Handling {message}')
    p_message = message.lower()
    if p_message[0] == '!':
        commands = get_simplecommands("commands.json")
        if p_message in commands.keys():
            return commands[p_message]
        return "Sorry, I didn't understand the command. Check if there's any misspelling!"


def get_simplecommands(filepath: str) -> dict:
    commands = dict()
    if os.path.exists(filepath):
        with open(filepath, "r") as json_file:
            commands = json.load(json_file)
            return commands
    else:
        commands["!help"] = "This is the helper command."
        commands["!hello"] = "Hey! What's up?"
        with open(filepath, "w") as json_file:
            json.dump(commands, json_file)
        return commands
