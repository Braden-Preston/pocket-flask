class Config(object):
    SECRET_KEY = '192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
    SESSION_TYPE = "filesystem"
    SESSION_FILE_DIR = "output/pb_data/sessions"
    PERMANENT_SESSION_LIFETIME = 1209600  # 2 weeks (seconds)
    SESSION_PERMANENT = False