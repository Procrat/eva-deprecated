import subprocess
import platform

APP_NAME = 'Eva'


def notify(message):
    os_notify = {
        'Linux': _notify_nix,
        'Darwin': _notify_mac
    }[platform.system()]
    os_notify(message)


def _notify_nix(message):
    subprocess.check_call(['notify-send', '-a', APP_NAME, message])


# TODO implement this, @Silox
def _notify_mac(message):
    pass
