from config.env import env, env_to_enum
from socialblog.emails.enums import EmailSendingStrategy

# local | mailtrap
EMAIL_SENDING_STRATEGY = env_to_enum(EmailSendingStrategy, env("EMAIL_SENDING_STRATEGY", default="local"))

EMAIL_SENDING_FAILURE_TRIGGER = env.bool("EMAIL_SENDING_FAILURE_TRIGGER", default=False)
EMAIL_SENDING_FAILURE_RATE = env.float("EMAIL_SENDING_FAILURE_RATE", default=0.2)

if EMAIL_SENDING_STRATEGY == EmailSendingStrategy.LOCAL:
    #EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = 'user' #env.str("GOOGLE_EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = 'pass'#env.str("GOOGLE_EMAIL_HOST_PASSWORD")

if EMAIL_SENDING_STRATEGY == EmailSendingStrategy.MAILTRAP:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = env("MAILTRAP_EMAIL_HOST")
    EMAIL_HOST_USER = env("MAILTRAP_EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = env("MAILTRAP_EMAIL_HOST_PASSWORD")
    EMAIL_PORT = env("MAILTRAP_EMAIL_PORT")
