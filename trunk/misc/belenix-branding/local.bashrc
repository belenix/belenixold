#
# Simple profile places /usr/gnu/bin at front,
# adds /usr/X11/bin, /usr/sbin and /sbin to the end.
#
# Use less(1) as the default pager for the man(1) command.
#
export PATH=/usr/gnu/bin:/usr/bin:/usr/X11/bin:/usr/sbin:/sbin:/usr/sfw/bin
export MANPATH=/usr/gnu/share/man:/usr/share/man:/usr/X11/share/man:/usr/sfw/share/man:/opt/DTraceToolkit/Man
export PAGER="/usr/bin/less -ins"
export MAPAGER="/usr/bin/less -ins"

#
# Define default prompt to <username>@<hostname>:<path><"($|#) ">
# and print '#' for user "root" and '$' for normal users.
#
PS1='${LOGNAME}@$(hostname):$(
    [[ "$LOGNAME" = "root" ]] && printf "${PWD/${HOME}/~}# " ||
    printf "${PWD/${HOME}/~}\$ ")'

#
# Enable color ls only for some known terminal types and
# if we are having GNU ls in PATH.
#
if [ "$TERM" = "xterm" -o "$TERM" = "xterm-color" -o "$TERM" = "sun-color" -o "$TERM" = "vt100"  -o "$TERM" = "dtterm" ]
then
	ls --version 2>&1 > /dev/null
	if [ $? -eq 0 ]
	then
		[ -e "$HOME/.dircolors" ] && DIR_COLORS="$HOME/.dircolors"
		[ -e "$HOME/.dir_colors" ] && DIR_COLORS="$HOME/.dir_colors"
		[ -e "$DIR_COLORS" ] || DIR_COLORS=""
		eval "`dircolors -b $DIR_COLORS`"
		alias ls='ls --color=auto'
	fi
fi

