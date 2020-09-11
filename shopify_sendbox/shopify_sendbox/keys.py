import environ


env = environ.Env()
environ.Env.read_env()

SENDBOX_AUTHORIZATION_KEY = env('SENDBOX_AUTHORIZATION_KEY')
SETTINGS_SECRET_KEY = env('SETTINGS_SECRET_KEY')
