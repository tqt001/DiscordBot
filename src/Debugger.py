def debug(self, on):
    def print_message(msg):
        print(msg)
    if on:
        return print_message
    else:
        return
