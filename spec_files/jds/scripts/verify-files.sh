#!/bin/sh

# do some mapping for the naimng convention of the two lists
# gtk2 -> gtk+
# glib2 -> glib
# GConf -> gconf
# control-center -> gnome-control-center
# 
base_initial=""

case "$1" in
	*gtk2*) base_initial="gtk+"
		;;
	"glib2") base_initial="glib"
		;;
	"GConf") base_initial="gconf"
		;;
	"control-center") base_initial="gnome-control-center"
		;;
	*) base_initial=$1
		;;
esac

echo "base_initial is $base_initial"

# Need to merge all the rpms into one
# Strip out all the locale stuff

ls /usr/src/packages/RPMS/*/$1* > /tmp/rpms.$$
cat /tmp/rpms.$$ | while read rpm
do
	rpm -qpl $rpm | grep -v locale >> /tmp/$1.myfiles
done

# sort the content to make comparison more meaningful

sort -u /tmp/$1.myfiles > /tmp/$1.myfiles.sorted


# Take the reference files list and substitute prefix and sysconfdir

cat /sgnome/pkgs/gnome-2.2/misc/files-2.2/$base_initial.lst | sed 's/opt\/gnome-2.2/usr/' | sed 's/usr\/etc/etc/' >> /tmp/$base_initial.ref-files-2.2

sort -u /tmp/$1.ref-files-2.2 > /tmp/$base_initial.ref-files-2.2.sorted
diff -u /tmp/$1.myfiles.sorted /tmp/$base_initial.ref-files-2.2.sorted

# clean up
rm /tmp/rpms.$$ /tmp/$1.myfiles /tmp/$1.ref-files-2.2
