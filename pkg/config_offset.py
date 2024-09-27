import os
import json

class Config:
    def __init__(self):
        self.config = self.load_config()

    def get_config_path(self):
        """Get the path to the configuration file."""
        app_data = os.getenv('APPDATA')
        if not app_data:
            raise Exception("APPDATA environment variable not found.")
        config_dir = os.path.join(app_data, 'PyAutoPascoal')
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        return os.path.join(config_dir, 'config.json')

    def load_config(self):
        """Load the configuration from the file."""
        config_path = self.get_config_path()
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        else:
            # Default values if config file doesn't exist
            return {'x_offset': 0, 'y_offset': 0}

    def save_config(self):
        """Save the configuration to the file."""
        config_path = self.get_config_path()
        with open(config_path, 'w') as f:
            json.dump(self.config, f)

    def get_offsets(self):
        """Retrieve the current offsets."""
        return self.config.get('x_offset', 0), self.config.get('y_offset', 0)

    def set_offsets(self, x_offset, y_offset):
        """Update the offsets and save them."""
        self.config['x_offset'] = x_offset
        self.config['y_offset'] = y_offset
        self.save_config()

# Create a global Config instance as a singleton
config = Config()
