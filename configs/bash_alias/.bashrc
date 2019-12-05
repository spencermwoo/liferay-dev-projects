_get_git_repo(){
  git remote -v | grep git@github.com | grep fetch | head -1 | cut -f2 | cut -d'.' -f1-2 | sed -e's/:/\//' -e 's/git@/https:\/\//'
}

_get_git_branch(){
  git branch -v | grep '*' | cut -d' ' -f2
}

gh(){
  "path\to\chrome" $(_get_git_repo)/tree/$(_get_git_branch)
}

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

find_in_cwd_or_parent() {
  local slashes=${PWD//[^\/]/};
  local directory=$PWD;

  for (( n=${#slashes}; n>0; --n )); do
    test -e "$directory/$1" && echo "$directory/$1" && return 0

    directory="$directory/.."
  done

  return 1
}

is_cwd_git() {
  if ( git rev-parse --git-dir > /dev/null 2>&1 ); then
    return 0
  fi

  return 1
}

is_cwd_git_liferay() {
  if is_cwd_git; then
    local gitFolderPath="$(git rev-parse --show-toplevel)"

    if [ -d $gitFolderPath/portal-impl ]; then
      return 0
    fi
  fi

  return 1
}

is_cwd_git_liferay_app() {
  if is_cwd_git; then
    local gitFolderPath="$(git rev-parse --show-toplevel)"
    local app_bnd_file_path="${gitFolderPath}/app.bnd"

    if [ -f "${app_bnd_file_path}" ] && \
        [ $(cat "${app_bnd_file_path}" | grep '^Liferay-Releng' | wc -l | xargs) -gt 0 ]; then      
      return 0
    fi
  fi

  return 1
}

is_cwd_git_liferayDXP() {
  if is_cwd_git; then
    local gitFolderPath="$(git rev-parse --show-toplevel)"

    if [ -d $gitFolderPath/portal-kernel ] && [ -d $gitFolderPath/modules ]; then
      return 0
    fi
  fi

  return 1
}

is_cwd_git_liferayDXP_private() {
  if is_cwd_git; then
    local gitFolderPath="$(git rev-parse --show-toplevel)"

    if [ -d $gitFolderPath/modules ] && [ -d $gitFolderPath/working.dir.properties ]; then
      return 0
    fi
  fi
}

cds() {
  local partial_folder_path="$1"

  if [ -n "${partial_folder_path}" ]; then
    local folder_path

    if is_cwd_git_liferayDXP || is_cwd_git_liferay_app; then
      pushd $(git rev-parse --show-toplevel) > /dev/null

      local filtered_file_paths=$(git ls-files | grep "${partial_folder_path}")

      #Search more strictly - match search term exactly in module name
      folder_path="$(echo "${filtered_file_paths}" \
        | awk -v moduleRegex="(/|^)${partial_folder_path}/((app|bnd).bnd|build(.gradle|.xml))" \
          '$0 ~ moduleRegex && (moduleLength == "" || length < moduleLength) {moduleLength = length; module = $0} END{print module}' \
        | xargs dirname 2>/dev/null)"

      #Search not as strictly - contains search term in module name
      if [ -z "${folder_path}" ]; then
        folder_path="$(echo "${filtered_file_paths}" \
          | awk -v moduleRegex="(/|^).*${partial_folder_path}.*/((app|bnd).bnd|build(.gradle|.xml))" \
            '$0 ~ moduleRegex && (moduleLength == "" || length < moduleLength) {moduleLength = length; module = $0} END{print module}' \
          | xargs dirname 2>/dev/null)"
      fi

      if [ -n "${folder_path}" ]; then
        folder_path="$(git rev-parse --show-toplevel)/${folder_path}"
      fi

      popd > /dev/null
    fi

    if [ -z "${folder_path}" ]; then
      if is_cwd_git; then
        pushd $(git rev-parse --show-toplevel) > /dev/null

        folder_path="$(git ls-files | grep -m 1 "${partial_folder_path}/" | xargs -n1 dirname)"

        if [ -n "${folder_path}" ]; then
          folder_path="$(git rev-parse --show-toplevel)/${folder_path}"
        fi

        popd > /dev/null
      fi

      if [ -z "${folder_path}" ]; then
        folder_path="$(find . -type d -name "*${partial_folder_path}*" -print0 -quit)"
      fi
    fi

    if [ -n "${folder_path}" ]; then
      cd -- ${folder_path}
    fi
  fi
}

_cds()
{
  if [ "${#COMP_WORDS[@]}" != "2" ] || (! is_cwd_git); then
    return
  fi

  # keep the suggestions in a local variable
  local suggestions=($(compgen -W "$(pushd $(git rev-parse --show-toplevel) > /dev/null; git ls-files | grep "/.lfrbuild-portal$" | awk -F"/" '{print $(NF-1)}')" -- "${COMP_WORDS[1]}"))

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
  git fetch origin pull/$@/head:pr-$1
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
    echo "RUNNING: 'rm -rf work; rm -rf osgi/state; rm -rf $1/temp; rm -rf $1/work'"
    rm -rf work; rm -rf osgi/state; rm -rf $1/temp; rm -rf $1/work
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