import json


def save_setting(setting: str, value: str) -> None:
    with open('stuff/settings.json', 'r+') as file:
        settings = json.load(file)
        settings[setting] = value
        file.seek(0)
        json.dump(settings, file, indent=4)
        file.truncate()


def get_setting(setting: str) -> str:
    with open('stuff/settings.json', 'r') as file:
        settings = json.load(file)
        return settings.get(setting, "")


def death_count(increment: bool = True) -> None:
    """
    Increment or decrement the death counter.
    :param increment: If True, increment the counter; if False, decrement it.
    """
    try:
        with open('deaths.txt', 'r+') as file:
            count = int(file.read().strip())
            if increment:
                count += 1
                print("Death count +1, total:", count)
            else:
                count = max(0, count - 1)  # It will always be >=0
                print("Death count -1, total:", count)

            file.seek(0)
            file.write(str(count))
            file.truncate()
    except FileNotFoundError:
        with open('deaths.txt', 'w') as file:
            file.write('0')
        death_count(increment)
