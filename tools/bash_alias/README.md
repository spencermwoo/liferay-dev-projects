I'll leave the standard aliases to develop from your own preference.

Here are ones that intersect usefulness and uniqueness.  Highly recommend the first section.


----
# Develop

Open windows explorer with `dir`
> `"C:\Windows\explorer.exe" "$@"`

Open sublime via args with `sub`
> `"C:\Program Files\Sublime Text 3\sublime_text.exe" "$@"`

Open Windows `hosts` with `host`
> `eval "powershell -c start -verb runas notepad.exe 'C:\Windows\System32\drivers\etc\hosts'"`

Open `.bashrc` with `rc`
> `"C:\Program Files\Sublime Text 3\sublime_text.exe" "C:\Users\liferay\.bashrc"`

Refresh aliases with `sb`
> `source ~/.bash_profile`


# Liferay

I'm a reviewer
```
pr(){
	eval "git fetch origin pull/$@/head:pr-$@"
}
```



Tomcat - clear temporary directories
```
dc(){
	if ["$1" = ""]; then
		echo "USAGE: dc <tomcat-directory>"
	else
		echo "RUNNING: 'rm -rf work; rm -rf osgi/state; rm -rf $@/temp; rm -rf $@/work'"
		eval "rm -rf work; rm -rf osgi/state; rm -rf $@/temp; rm -rf $@/work"
	fi
}

full_dc(){
	dc $@; db_re;
}
```


# Standard Usage
```
alias nc='ncat'

alias dl='youtube-dl'

ghidra(){
	"C:\Users\liferay\Desktop\SEC\ghidra_9.0\ghidraRun.bat"
}

pyserver(){
	echo "py -m http.server"
	eval "py -m http.server"
}

phpserver(){
	echo "php -S localhost:9000"
	eval "php -S localhost:9000"
}
```