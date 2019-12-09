_get_git_repo(){
  git remote -v | grep git@github.com | grep fetch | head -1 | cut -f2 | cut -d'.' -f1-2 | sed -e's/:/\//' -e 's/git@/https:\/\//'
}

_get_git_branch(){
  git branch -v | grep '*' | cut -d' ' -f2
}

gh(){
  open $(_get_git_repo)/tree/$(_get_git_branch)
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

