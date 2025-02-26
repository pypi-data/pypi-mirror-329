from winrm.protocol import Protocol
from winrm.exceptions import WinRMOperationTimeoutError
import argparse
import sys
import harness_pywinrm.parsedict as ParseDict

def run_command(endpoint, username, server_cert_validation, command, environment, workingDir, timeout):
    p = Protocol(
        endpoint=endpoint,
        transport='kerberos',
        username=username,
        server_cert_validation=server_cert_validation,
        operation_timeout_sec=timeout,
        read_timeout_sec=timeout + 10)

    shell_id = p.open_shell(env_vars=environment, working_directory=workingDir)
    command_id = p.run_command(shell_id, command)

    command_done = False
    while not command_done:
        try:
           stdout, stderr, return_code, command_done = \
           p._raw_get_command_output(shell_id, command_id)
           sys.stdout.buffer.write(stdout)
           sys.stdout.flush()
           sys.stderr.buffer.write(stderr)
           sys.stderr.flush()
        except WinRMOperationTimeoutError:
                    # this is an expected error when waiting for a long-running process, just silently retry
            pass

    p.cleanup_command(shell_id, command_id)
    p.close_shell(shell_id)

    if return_code != 0:
        sys.exit(1)


@DeprecationWarning
def splitEnvironmentArgumentToDict(environment):
    if environment is None or len(environment) == 2:
        return None
    environmentList = environment[1:-1].split(', ')
    env_vars = {}
    for s in environmentList:
        [key, value] = s.split('=', 1)
        env_vars[key.strip()] = value
    return env_vars


def parse_arguments(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', action="store_true")
    parser.add_argument('-e', '--endpoint', help="windows remote server endpoint (should be complete)")
    parser.add_argument('-u', '--username', help="user principal for the kerberos auth")
    parser.add_argument('-s', '--server_cert_validation', help="should validate server certificates or not")
    parser.add_argument("-env", "--environment",
                        metavar="KEY=VALUE",
                        nargs='+',
                        help="Environment variables stored in the form of java map#toString function.Set a number of "
                             "key-value pairs "
                             "(do not put spaces before or after the = sign). "
                             "If a value contains spaces, you should define "
                             "it with double quotes: "
                             'foo="this is a sentence". Note that '
                             "values are always treated as strings.",
                        action=ParseDict.ParseDict)
    parser.add_argument('-w', '--workingDir', help='working directory in remote where commands should run')
    parser.add_argument('-t', '--timeout', help='Connection timeout while running commands')
    parser.add_argument('-cfile', '--commandFilePath', help='File containing the commands to run')

    args = parser.parse_args(args)

    if args.version:
        print('0.4.4')
        sys.exit(0)

    if args.endpoint is None or args.username is None or args.server_cert_validation is None or args.commandFilePath is None or args.timeout is None:
        print(
            'Value required for endpoint, username, server_cert_validation, commandFilePath, timeout. See help for '
            'more information')
        sys.exit(1)

    commandFilePath = args.commandFilePath
    endpoint = args.endpoint
    username = args.username
    server_cert_validation = 'validate' if args.server_cert_validation == 'true' else 'ignore'
    env_vars = args.environment
    timeout = None if args.timeout == None else int(args.timeout) / 1000
    command = open(commandFilePath, 'r').read()
    workingDir = args.workingDir

    return command, endpoint, username, server_cert_validation, env_vars, workingDir, timeout

def main():
    (command, endpoint, username, server_cert_validation, env_vars, workingDir, timeout) = parse_arguments(sys.argv[1:])
    run_command(endpoint, username, server_cert_validation, command, env_vars, workingDir, timeout)

if __name__ == '__main__':
    main()
