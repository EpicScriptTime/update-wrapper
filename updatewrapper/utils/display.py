import sys
import termcolor
import time


def ask_yes_no(question, default=True):
    """
    Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of True or False.
    """
    valid = {'yes': True, 'y': True, 'ye': True, 'no': False, 'n': False}

    if default is None:
        prompt = ' [y/n] '
    elif default is True:
        prompt = ' [Y/n] '
    elif default is False:
        prompt = ' [y/N] '
    else:
        raise ValueError('invalid default answer: `%s`' % default)

    while True:
        choice = input(question + prompt).strip().lower()

        print()  # Required for spacing

        if default is not None and choice == '':
            return default
        elif choice in valid.keys():
            return valid[choice]
        else:
            print('Please respond with `yes` or `no`.')


def print_banner():
    print("                 _       _                                                             _   ___   ___  ")
    print(" _   _ _ __   __| | __ _| |_ ___     __      ___ __ __ _ _ __  _ __   ___ _ __  __   _/ | / _ \ / _ \ ")
    print("| | | | '_ \ / _` |/ _` | __/ _ \____\ \ /\ / / '__/ _` | '_ \| '_ \ / _ \ '__| \ \ / / || | | | | | |")
    print("| |_| | |_) | (_| | (_| | ||  __/_____\ V  V /| | | (_| | |_) | |_) |  __/ |     \ V /| || |_| | |_| |")
    print(" \__,_| .__/ \__,_|\__,_|\__\___|      \_/\_/ |_|  \__,_| .__/| .__/ \___|_|      \_/ |_(_)___(_)___/ ")
    print("      |_|                                               |_|   |_|                                     ")
    print()


def print_info(text):
    termcolor.cprint(text, 'cyan', attrs=['bold'])
    print()


def print_notice(text):
    termcolor.cprint(text, 'magenta', attrs=['bold'])
    print()


def print_success(text):
    termcolor.cprint(text, 'green', attrs=['bold'])
    print()


def print_warning(text):
    termcolor.cprint(text, 'yellow', attrs=['bold'])
    print()


def spinner_list(texts, ticks=10):
    max_size = len(max(texts, key=len)) + 4

    for text in texts:
        baseline = '\r' + text + '...'

        for i in range(ticks):
            if i % 4 == 0:
                sys.stdout.write(baseline + '/')
                sys.stdout.flush()
            elif i % 4 == 1:
                sys.stdout.write(baseline + '-')
                sys.stdout.flush()
            elif i % 4 == 2:
                sys.stdout.write(baseline + '\\')
                sys.stdout.flush()
            elif i % 4 == 3:
                sys.stdout.write(baseline + '|')
                sys.stdout.flush()

            time.sleep(0.1)

        # Clear leftover
        sys.stdout.write('\r' + ' ' * max_size)
        sys.stdout.flush()

    # Allow last line to be erased
    sys.stdout.write('\r')
    sys.stdout.flush()
