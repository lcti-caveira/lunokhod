def handle_response(message) -> str:
    print(f'Handling {message}')
    p_message = message.lower()
    if p_message == 'hello':
        return "What's up!"
    if p_message == '!help':
        return "Just say hello"
