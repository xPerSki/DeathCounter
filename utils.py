import json


def save_action_bind(action: str, value: str) -> None:
    with open('settings.json', 'r+') as file:
        settings = json.load(file)
        settings[action] = value
        file.seek(0)
        json.dump(settings, file, indent=4)
        file.truncate()


def get_action_bind(action: str) -> str:
    with open('settings.json', 'r') as file:
        settings = json.load(file)
        return settings.get(action, "")


def death_count(increment: bool = True) -> None:
    """
    Increment or decrement the death counter.
    :param increment: If True, increment the counter; if False, decrement it.
    """
    try:
        with open('deaths.txt', 'r+') as file:
            count = int(file.read().strip())
            count += 1 if increment else -1
            file.seek(0)
            file.write(str(count))
            file.truncate()
    except FileNotFoundError:
        with open('deaths.txt', 'w') as file:
            file.write('0')
        death_count(increment)
