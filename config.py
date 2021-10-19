from ntpath import join
import os
from posixpath import dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')  # Path to .env file
load_dotenv(dotenv_path)
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'MyIDE_secret_key'

    # CLIENT_ID = os.environ.get('CLIENT_ID') or '19e83f4b909394d4387535acce0cb16a403985a01f7d.api.hackerearth.com'
    # CLIENT_SECRET_KEY = os.environ.get('CLIENT_SECRET_KEY') or '4acde50b23e29070bad8ed489b4dcffc488b6169'
    # COMPILE_URL = os.environ.get('COMPILE_URL') or 'https://api.hackerearth.com/v3/code/compile/'
    # RUN_URL = os.environ.get('RUN_URL') or 'https://api.hackerearth.com/v3/code/run/'

    #CLIENT_ID = os.environ.get('CLIENT_ID') or '19e83f4b909394d4387535acce0cb16a403985a01f7d.api.hackerearth.com'
    #CLIENT_ID = os.environ.get('CLIENT_ID') or '64533056ec05b9c18aaadd2dc400dccc8c490818d129.api.hackerearth.com'
    CLIENT_ID = os.environ.get('CLIENT_ID') or '1d167055e97a90457fb88ef36fc814b8'
    #CLIENT_ID = os.environ.get('CLIENT_ID') or '0214c33a'
    #ACCESS_TOKEN = '31a1e40ec6fab583cb8d2ac529ff44f8'
    #CLIENT_SECRET_KEY = os.environ.get('CLIENT_SECRET_KEY') or '4acde50b23e29070bad8ed489b4dcffc488b6169'
    #CLIENT_SECRET_KEY = os.environ.get('CLIENT_SECRET_KEY') or '3865ac3bf22ade323a143ebc7184cc9ed9000e41'
    CLIENT_SECRET_KEY = os.environ.get('CLIENT_SECRET_KEY') or '36547f75e2c06b3f3e62c3d6cc59230253930d0a162ad848fe7c0c9e0c8eada4'
    #COMPILE_URL = os.environ.get('COMPILE_URL') or 'https://api.hackerearth.com/v3/code/compile/'
    COMPILE_URL = os.environ.get('COMPILE_URL') or 'https://api.jdoodle.com/v1/execute'
    #RUN_URL = os.environ.get('RUN_URL') or 'https://api.hackerearth.com/v3/code/run/'
    #RUN_URL = os.environ.get('RUN_URL') or 'https://api.hackerearth.com/v4/partner/code-evaluation/submissions/'
    #RUN_URL = os.environ.get('RUN_URL') or 'https://0214c33a.compilers.sphere-engine.com/api/v4'
    RUN_URL = os.environ.get('RUN_URL') or 'https://api.jdoodle.com/v1/execute'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    WTF_CSRF_ENABLED = True
    CODEMIRROR_LANGUAGES = ['python', 'htmlembedded', 'clike']
    # material-ocean, monokai, dracula, ambiance, blackboard, colorforth
    CODEMIRROR_THEME = 'ambiance'
    CODEMIRROR_ADDONS = (
        ('display', 'placeholder'),
        ('comment', 'comment'),
        ('comment', 'continuecomment'),
        ('scroll', 'simplescrollbars'),
        ('selection', 'active-line'),
        ('fold', 'foldcode'),
        ('edit', 'matchtags'),
        ('edit', 'matchbrackets'),
        ('edit', 'closebrackets'),
        ('fold', 'xml-fold')
    )
