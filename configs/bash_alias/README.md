Highly recommend the first two sections.

I'll leave the standar aliases to develop from your own preference.  These are the more unique and useful ones.

----
# Develop

[`dir`](https://github.com/SpencerWoo/liferay-dev-projects/blob/master/configs/bash_alias/.bashrc#L1-L3) : Open windows explorer

[`sub`](https://github.com/SpencerWoo/liferay-dev-projects/blob/master/configs/bash_alias/.bashrc#L5-L7) : Open sublime via args 

![](https://github.com/SpencerWoo/liferay-dev-projects/blob/master/configs/bash_alias/gifs/sub2.gif)

[`host`](https://github.com/SpencerWoo/liferay-dev-projects/blob/master/configs/bash_alias/.bashrc#L9-L11) : Open Windows `hosts` file directly

[`rc`](https://github.com/SpencerWoo/liferay-dev-projects/blob/master/configs/bash_alias/.bashrc#L13-L15) : Open `.bashrc` file directly

[`sb`](https://github.com/SpencerWoo/liferay-dev-projects/blob/master/configs/bash_alias/.bashrc#L17-L19) : Refresh aliases 


# Liferay
[`cds`](https://github.com/SpencerWoo/liferay-dev-projects/blob/master/configs/bash_alias/.bashrc#L41-L97) : Instantly navigate to module (similiar to [MCD's](https://github.com/holatuwol/liferay-faster-deploy/tree/master/gitcd#cd-to-module-root)) 
Requires [helpers](https://github.com/SpencerWoo/liferay-dev-projects/blob/master/configs/bash_alias/.bashrc#L21-L39)

   * Add [bash autocompletion](https://github.com/SpencerWoo/liferay-dev-projects/blob/master/configs/bash_alias/.bashrc#L99-L120) to the above `cds`

![](https://github.com/SpencerWoo/liferay-dev-projects/blob/master/configs/bash_alias/gifs/cds2.gif)

[`pr`](https://github.com/SpencerWoo/liferay-dev-projects/blob/master/configs/bash_alias/.bashrc#L122-L124) : Fetch a pull for direct review 

[`dc`](https://github.com/SpencerWoo/liferay-dev-projects/blob/master/configs/bash_alias/.bashrc#L150-L157) : Clear Tomcat directories

![](https://github.com/SpencerWoo/liferay-dev-projects/blob/master/configs/bash_alias/gifs/dc.gif)

 * Additionally drop and recreate database with [`dcf`](https://github.com/SpencerWoo/liferay-dev-projects/blob/master/configs/bash_alias/.bashrc#L159-L161) 
 Requires [helpers](https://github.com/SpencerWoo/liferay-dev-projects/blob/master/configs/bash_alias/.bashrc#L126-L148)

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