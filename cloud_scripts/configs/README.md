Highly recommend the first two sections.

I'll leave the standar aliases to develop from your own preference.  These are the more unique and useful ones.

----
# Develop

[`gh`](https://github.com/SpencerWoo/liferay-dev-projects/blob/master/configs/bash_alias/.bashrc#L9-L11) : Open windows explorer

[`dir`](https://github.com/SpencerWoo/liferay-dev-projects/blob/master/configs/bash_alias/.bashrc#L13-L15) : Open windows explorer

[`sub`](https://github.com/SpencerWoo/liferay-dev-projects/blob/master/configs/bash_alias/.bashrc#L17-L19) : Open sublime via args 

![](https://github.com/SpencerWoo/liferay-dev-projects/blob/master/configs/bash_alias/gifs/sub2.gif)

[`host`](https://github.com/SpencerWoo/liferay-dev-projects/blob/master/configs/bash_alias/.bashrc#L21-L23) : Open Windows `hosts` file directly

[`rc`](https://github.com/SpencerWoo/liferay-dev-projects/blob/master/configs/bash_alias/.bashrc#L25-L27) : Open `.bashrc` file directly

[`sb`](https://github.com/SpencerWoo/liferay-dev-projects/blob/master/configs/bash_alias/.bashrc#L29-L31) : Refresh aliases 

# Liferay
[`cds`](https://github.com/SpencerWoo/liferay-dev-projects/blob/master/configs/bash_alias/.bashrc#L53-L109) : Instantly navigate to module (similiar to [MCD's](https://github.com/holatuwol/liferay-faster-deploy/tree/master/gitcd#cd-to-module-root)) 
Requires [helpers](https://github.com/SpencerWoo/liferay-dev-projects/blob/master/configs/bash_alias/.bashrc#L33-L41)

   * Add [bash autocompletion](https://github.com/SpencerWoo/liferay-dev-projects/blob/master/configs/bash_alias/.bashrc#L111-L132) to the above `cds`

![](https://github.com/SpencerWoo/liferay-dev-projects/blob/master/configs/bash_alias/gifs/cds2.gif)

[`pr`](https://github.com/SpencerWoo/liferay-dev-projects/blob/master/configs/bash_alias/.bashrc#L134-L136) : Fetch a pull for direct review 

[`dc`](https://github.com/SpencerWoo/liferay-dev-projects/blob/master/configs/bash_alias/.bashrc#L162-L169) : Clear Tomcat directories

![](https://github.com/SpencerWoo/liferay-dev-projects/blob/master/configs/bash_alias/gifs/dc.gif)

 * Additionally drop and recreate database with [`dcf`](https://github.com/SpencerWoo/liferay-dev-projects/blob/master/configs/bash_alias/.bashrc#L171-L173) 
 Requires [helpers](https://github.com/SpencerWoo/liferay-dev-projects/blob/master/configs/bash_alias/.bashrc#L138-L150)

[`cr`] : [Start tomcat on open port from MCD](https://github.com/holatuwol/liferay-faster-deploy/tree/master/tomcat#start-tomcat)

# Standard

Alias anything!

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





---

TODO : change dcf