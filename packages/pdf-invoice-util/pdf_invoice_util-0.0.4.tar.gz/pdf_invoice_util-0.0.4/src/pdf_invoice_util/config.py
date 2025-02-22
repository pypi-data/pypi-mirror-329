import yaml

class Config:
    def __init__(self, config=None, config_overwrites=None):
        if config is None:
            try:
                with open('config/config.yaml', 'r') as config_file:
                    config = yaml.safe_load(config_file)
            except FileNotFoundError as e:
                print(f'No config file found: {e}')
                exit()
        self.config = config
        if config_overwrites is not None:
            self.update(config_overwrites)

    def update(self, config_overwrites):
        for key, value in config_overwrites.items():
            if type(value) is dict:
                for value_key, value_value in value.items():
                    self.config[key][value_key] = value_value
            else:
                self.config[key] = value

    def load(self):
        return self.config
