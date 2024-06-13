from config.env import env

GOOGLE_OAUTH2_CLIENT_ID = env.str("DJANGO_GOOGLE_OAUTH2_CLIENT_ID", default="")
GOOGLE_OAUTH2_CLIENT_SECRET = env.str("DJANGO_GOOGLE_OAUTH2_CLIENT_SECRET", default="")
GOOGLE_OAUTH2_PROJECT_ID = env.str("DJANGO_GOOGLE_OAUTH2_PROJECT_ID", default="")
