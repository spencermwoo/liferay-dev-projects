_get_git_repo(){
  git remote -v | grep git@github.com | grep fetch | grep $1 | cut -f2 | cut -d'.' -f1-2 | sed -e's/:/\//' -e 's/git@/https:\/\//'
}

_get_git_branch(){
  git branch -v | grep '*' | cut -d' ' -f2
}

gh(){
  REMOTE=$(git branch -v | grep '*' | cut -d' ' -f2)

  if [[ $REMOTE =~ "HEAD" ]]; then
    HEAD=$(git branch -v | grep '*' | cut -d' ' -f5 | sed 's/.$//')

    if [[ $HEAD =~ "/" ]]; then
      BRANCH=$(echo $HEAD | cut -d'/' -f1)
      REPO=$(echo $HEAD | cut -d'/' -f2)

      open $(_get_git_repo $BRANCH)/tree/$REPO
    else
      open $(_get_git_repo origin)/tree/$HEAD
    fi
  else
    open $(_get_git_repo origin)/tree/$(_get_git_branch)
  fi
}

dir(){
  open -F -a "Finder" "$@"
}

sub() {
  open -F -a "Sublime Text" "$@"
}

rc(){
  open -a "Sublime Text" "/Users/liferay/.bash_profile"
}

sb(){
  source ~/.bash_profile
}

_ccc(){
  if [ "${#COMP_WORDS[@]}" != "2" ] || (! _is_cwd_git); then
    return
  fi

  # keep the suggestions in a local variable
  local suggestions=($(compgen -W "$(ls -F /Users/liferay/Desktop/cloud/ | grep \/$ )" -- "${COMP_WORDS[1]}"))

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

ccc(){
  cd /Users/liferay/Desktop/cloud/"$@"
}

complete -F _ccc ccc