class EventPrinter:
    def __init__(self):
        self._printed = set()

    def print_event(self, event: dict, max_length=1500):
        current_state = event.get("dialog_state")
        if current_state:
            print("Currently in: ", current_state[-1])
        message = event.get("messages")
        if message:
            if isinstance(message, list):
                message = message[-1]
            if message.id not in self._printed:
                msg_repr = message.pretty_repr(html=True)
                if len(msg_repr) > max_length:
                    msg_repr = msg_repr[:max_length] + " ... (truncated)"
                print(msg_repr)
                self._printed.add(message.id)
