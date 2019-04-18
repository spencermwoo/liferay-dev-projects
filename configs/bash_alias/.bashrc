dir(){
  "C:\Windows\explorer.exe" "$@"
}

sub(){
  "C:\Program Files\Sublime Text 3\sublime_text.exe" "$@"
}

host(){
  eval "powershell -c start -verb runas notepad.exe 'C:\Windows\System32\drivers\etc\hosts'"
}

rc(){
  "C:\Program Files\Sublime Text 3\sublime_text.exe" "C:\Users\liferay\.bashrc"
}

sb(){
  source ~/.bash_profile
}

is_cwd_git() {
  if ( git rev-parse --git-dir > /dev/null 2>&1 ); then
    return 0
  fi

  return 1
}

is_cwd_liferayDXP() {
  if is_cwd_git; then
    local gitFolderPath="$(git rev-parse --show-toplevel)"

    if [ -d $gitFolderPath/portal-kernel ] && [ -d $gitFolderPath/modules ]; then
      return 0
    fi
  fi

  return 1
}

cds() {
  if [ -n "$1" ]; then
    local folderPath

    if is_cwd_liferayDXP; then
      pushd $(git rev-parse --show-toplevel) > /dev/null

      #folderPath="$(git ls-files | grep -m 1 "$1/bnd.bnd" | head -1 | xargs -n1 dirname)"
      #folderPath="$(git ls-files \
            #| awk -v moduleRegex=".*$1[^/]*\/(app|bnd).bnd" -v simpleRegex=".*$1" \
            #     '$0 ~ moduleRegex || $0 ~ simpleRegex {print; exit}' \
            #| xargs -n1 dirname)"

      #Search more strictly - match search term exactly in module name
      folderPath="$(git ls-files \
        | awk -v moduleRegex="/$1/((app|bnd).bnd|build(.gradle|.xml))" \
          '$0 ~ moduleRegex {print; exit}' \
        | xargs -n1 dirname)
"
      #Search not as strictly - contains search term in module name
      if [ -z "$folderPath" ]; then
        folderPath="$(git ls-files \
          | awk -v moduleRegex="$1/((app|bnd).bnd|build(.gradle|.xml))" \
            '$0 ~ moduleRegex {print; exit}' \
          | xargs -n1 dirname)"
      fi

      if [ -n "$folderPath" ]; then
        folderPath="$(git rev-parse --show-toplevel)/$folderPath"
      fi

      popd > /dev/null
    fi

    if [ -z "$folderPath" ]; then
      if is_cwd_git; then
        pushd $(git rev-parse --show-toplevel) > /dev/null

        folderPath="$(git ls-files | grep -m 1 "$1/" | xargs -n1 dirname)"

        if [ -n "$folderPath" ]; then
          folderPath="$(git rev-parse --show-toplevel)/$folderPath"
        fi

        popd > /dev/null
      fi

      if [ -z "$folderPath" ]; then
        folderPath="$(find . -type d -name "*$1*" -print0 -quit)"
      fi
    fi

    if [ -n "$folderPath" ]; then
      cd -- $folderPath
    fi
  fi
}

_cds()
{
  if [ "${#COMP_WORDS[@]}" != "2" ] || (! is_cwd_git); then
    return
  fi
  
  # keep the suggestions in a local variable
  local suggestions=($(compgen -W "$(pushd $(git rev-parse --show-toplevel) > /dev/null; git ls-files | awk -F"/" -v moduleRegex="/.lfrbuild-portal$" '$0 ~ moduleRegex {print $(NF-1)}')" -- "${COMP_WORDS[1]}"))

  if [ "${#suggestions[@]}" == "1" ]; then
    # if there's only one match, we remove the command literal
    # to proceed with the automatic completion of the number
    local number=$(echo ${suggestions[0]/%\ */})
    COMPREPLY=("$number")
  else
    # more than one suggestions resolved,
    # respond with the suggestions intact
    COMPREPLY=("${suggestions[@]}")
  fi
}

complete -F _cds cds

pr(){
  eval "git fetch origin pull/$@/head:pr-$@"
}

dbCreate() {
  if [ $# -eq 0 ]; then
    echo "Please enter a database name."
  else
    mysql -u$db_user -p$db_pw -e "create database $1 CHARACTER SET utf8;"
  fi
}

dbDrop() {
  if [ $# -eq 0 ]; then
    echo "Please enter a database name."
  else
    mysql -u$db_user -p$db_pw -e "drop database $1;"
  fi
}

dbRecreate(){
  if [ $# -eq 0 ]; then
    echo "Please enter a database name."
  else
    dbDrop $@; dbCreate $@
  fi
}

dc(){
  if [ -z "$1" ]; then
    echo "USAGE: dc tomcat-9.0.10"
  else
    echo "RUNNING: 'rm -rf work; rm -rf osgi/state; rm -rf $@/temp; rm -rf $@/work'"
    eval "rm -rf work; rm -rf osgi/state; rm -rf $@/temp; rm -rf $@/work"
  fi
}

dcf(){
  dc $@; dbRecreate;
}

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