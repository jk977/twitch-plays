import config
import json
import os

from chat.user import User

class Settings:
    destination = 'settings.json'

    def save(path=None):
        if not path:
            path = os.path.join(config.data_dir, Settings.destination)

        fields = {'users': [u.serialize() for u in config.users.values()]}
        ser = json.dumps(fields)

        with open(path, 'w') as file:
            file.write(ser)

    def load(path=None):
        if not path:
            path = os.path.join(config.data_dir, Settings.destination)

        try:
            with open(path, 'r') as file:
                ser = file.read().strip()
        except FileNotFoundError:
            return

        fields = json.loads(ser)
        config.users = {}

        for ser in fields['users']:
            user = User.deserialize(ser)
            config.users[user.name] = user