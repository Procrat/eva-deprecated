import platform
import subprocess as sp
from exceptions import MissingDependencyException

if platform.system() == "Darwin":
    from datetime import datetime
    import objc
    import Foundation


APP_NAME = 'Eva'


def notify(message):
    """Shows a notification using system notification."""

    os_notify = {
        'Linux': _notify_nix,
        'Darwin': _notify_mac
    }[platform.system()]
    os_notify(message)


def delayed_notify(reminder):
    """Register an at job that generates a notification."""

    os_notify = {
        'Linux': _delayed_notify_nix,
        'Darwin': _delayed_notify_mac
    }[platform.system()]
    os_notify(reminder)


def _notify_nix(message):
    try:
        sp.check_call(['notify-send', '-a', APP_NAME, message])
    except FileNotFoundError:
        raise MissingDependencyException('libnotify')


def _delayed_notify_nix(reminder):
    try:
        # TODO add removal of reminder object to script
        message = 'You asked me to remind you to {}.'.format(reminder.content)
        script = 'notify-send -a "{}" "{}"'
        script = script.format(APP_NAME, message, reminder.id)
        echo = sp.Popen(['echo', script], stdout=sp.PIPE)

        time_str = reminder.when.strftime('%Y%m%d%H%M.%S')
        command = ['at', '-t', time_str]
        sp.check_call(command, stdin=echo.stdout, stderr=sp.DEVNULL)
    except FileNotFoundError:
        raise MissingDependencyException('at')


def _notify_mac(message, sound=True, delay=None):
    NSUserNotification = objc.lookUpClass('NSUserNotification')
    NSUserNotificationCenter = objc.lookUpClass('NSUserNotificationCenter')

    notification = NSUserNotification.alloc().init()
    notification.setTitle_("{} reminds you to:".format(APP_NAME))
    notification.setSubtitle_(message)
    # TODO: Fill this in when we decide what to do with the notifications
    # notification.setInformativeText_()
    # TODO: Fill this in when we decide what actions we'd like to use
    notification.setUserInfo_({})

    if sound:
        notification.setSoundName_("NSUserNotificationDefaultSoundName")
    if delay:
        notification.setDeliveryDate_(
            Foundation.NSDate.dateWithTimeInterval_sinceDate_(
                delay,
                Foundation.NSDate.date()
            )
        )

    NSUserNotificationCenter \
       .defaultUserNotificationCenter() \
       .scheduleNotification_(notification)


def _delayed_notify_mac(reminder):
    td = reminder.when - datetime.now()
    _notify_mac(reminder.content, delay=td.seconds)
