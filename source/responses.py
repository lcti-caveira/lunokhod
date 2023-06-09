def handle_response(message) -> str:
    print(f'Handling {message}')
    p_message = message.lower()
    if p_message == 'hello':
        return "What's up! Dude"
    if p_message == '!help':
        return "Just say hello"
    return "I can't understand that..."
