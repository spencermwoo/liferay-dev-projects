Highly recommend the first two sections.

I'll leave the standar aliases to develop from your own preference.  These are the more unique and useful ones.


----
# Develop

Open windows explorer with [`dir`](https://github.com/SpencerWoo/liferay-dev-projects/blob/master/tools/bash_alias/.bashrc#L1-L3)

Open sublime via args with [`sub`](https://github.com/SpencerWoo/liferay-dev-projects/blob/master/tools/bash_alias/.bashrc#L5-L7)

Open Windows `hosts` file directly with [`host`](https://github.com/SpencerWoo/liferay-dev-projects/blob/master/tools/bash_alias/.bashrc#L9-L11)

Open `.bashrc` file directly with [`rc`](https://github.com/SpencerWoo/liferay-dev-projects/blob/master/tools/bash_alias/.bashrc#L13-L15)

Refresh aliases with [`sb`](https://github.com/SpencerWoo/liferay-dev-projects/blob/master/tools/bash_alias/.bashrc#L17-L19)


# Liferay
Quickly navigate to module (MCD alternative) with [`cds`](https://github.com/SpencerWoo/liferay-dev-projects/blob/master/tools/bash_alias/.bashrc#L41-L97)
Requires [helpers](https://github.com/SpencerWoo/liferay-dev-projects/blob/master/tools/bash_alias/.bashrc#L21-L39)

   * Add [bash autocompletion](https://github.com/SpencerWoo/liferay-dev-projects/blob/master/tools/bash_alias/.bashrc#L99-L120) to the above `cds`

Fetch a pull for direct review with [`pr`](https://github.com/SpencerWoo/liferay-dev-projects/blob/master/tools/bash_alias/.bashrc#L122-L124)

Clear Tomcat directories with [`dc`](https://github.com/SpencerWoo/liferay-dev-projects/blob/master/tools/bash_alias/.bashrc#L150-L157)

Additionally drop and recreate database with [`dcf`](https://github.com/SpencerWoo/liferay-dev-projects/blob/master/tools/bash_alias/.bashrc#L159-L161)
Requires [helpers](https://github.com/SpencerWoo/liferay-dev-projects/blob/master/tools/bash_alias/.bashrc#L126-L148)

# Standard Usage

Additional basic utilities

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