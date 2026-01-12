MAX_HISTORY = 10
_chat_history = []

def add_message(role, message):
    _chat_history.append(f"{role}: {message}")
    if len(_chat_history) > MAX_HISTORY:
        _chat_history[:] = _chat_history[-MAX_HISTORY:]

def get_history():
    return _chat_history

def reset_history():
    _chat_history.clear()
