from cmdbox.app import app
from usound import version


def main(args_list:list=None):
    _app = app.CmdBoxApp.getInstance(appcls=UsoundApp, ver=version)
    return _app.main(args_list)[0]

class UsoundApp(app.CmdBoxApp):
    pass
