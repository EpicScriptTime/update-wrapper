import getopt
import os
import sys

from updatewrapper.host import Host
from updatewrapper.utils.display import ask_yes_no, print_banner, print_info, print_notice, print_success, print_warning, spinner_list
from updatewrapper.utils.file import get_config_file, get_hosts, get_logfile, save_output
from updatewrapper.wrapper import Wrapper


def wrap(hosts, out_dir):
    print_banner()

    logfiles = []

    spinner_list(['Warming up', 'Initializing wrapper', 'Loading host list'])
    print('Wrapping updates for the following hosts:')
    for host in hosts:
        print(' * %s' % host.name)

    print()
    for host in hosts:
        try:
            wrapper = Wrapper(host)

            print_info('BEGIN host %s' % host.addr)
            host.ask_passwords()

            print_success('Updating index cache')
            wrapper.update_cache()

            print_success('Listing available package upgrades')
            returns = wrapper.check_update()

            if wrapper.has_update(*returns):
                print_warning('Some packages need to be upgraded')

                if ask_yes_no('Do you want to continue?'):
                    print_success('Installing available package upgrades')
                    returncode, stdout, stderr = wrapper.perform_update()

                    logfile = get_logfile(host.name, out_dir)
                    save_output(logfile, stdout)

                    logfiles.append(logfile)
            else:
                print_success('All packages are up-to-date')

            print_notice('END host %s' % host.addr)
        except KeyboardInterrupt:
            print()
            print()
            print('bye')
            break

    if logfiles:
        print('The following logfiles were created:')

        for logfile in logfiles:
            print(' * %s' % os.path.basename(logfile))


def main():
    # TODO: Add --dist-upgrade option
    opts, args = getopt.getopt(sys.argv[1:], 'c:h:o', ['config=', 'host=', 'out-dir='])

    config_file = get_config_file()
    hosts = []
    host = None
    out_dir = os.getcwd()

    for opt in opts:
        if opt[0] in ('-c', '--config'):
            config_file = opt[1]
        elif opt[0] in ('-h', '--host'):
            addr = opt[1]
            host = Host(addr=addr)  # TODO: Should allow to input other parameters or search from config
        elif opt[0] in ('-o', '--out-dir'):
            out_dir = opt[1]

    if host:
        hosts.append(host)
    else:
        hosts = get_hosts(config_file)

    wrap(hosts, out_dir)


if __name__ == "__main__":
    main()
