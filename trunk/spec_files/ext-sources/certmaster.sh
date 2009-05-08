#!/bin/bash
#
# Start/Stop the certmaster server
#

. /lib/svc/share/smf_include.sh

# Get the value of a property defined in the service xml.
getproparg() {
	val=`svcprop -p $1 certmaster`
	[ -n "$val" ] && echo $val
}

PROGNAME=certmaster
DATADIR=`getproparg certmaster/data`
PROFILE=`getproparg certmaster/profile`
USER=certmaster
GROUP=certmaster

if [ -z ${DATADIR} ]; then
	echo "certmaster/data property not set"
	exit $SMF_EXIT_ERR_CONFIG
fi

if [ ! -d ${DATADIR} ]; then
	echo "certmaster/data directory ${DATADIR} is not a valid directory"
	exit $SMF_EXIT_ERR_CONFIG
fi

#
# Initial processing.
#
/usr/bin/certmaster-initchk "$USER" "$GROUP" "$DATADIR" "$PROFILE"

RETVAL=0

start() {
	echo "Starting: " /usr/bin/$PROGNAME -c $CONFIGFILE
	$PROGNAME &
        RETVAL=$?
	return $RETVAL
}

stop() {
        echo "Stopping: /usr/bin/$PROGNAME"
        pkill -P 1 "^$PROGNAME"
        RETVAL=$?
        return $RETVAL
}

restart() {
        $0 stop
        $0 start
}

reload() {
	trap "" SIGHUP
	pkill -HUP $PROGNAME
}

case "$1" in
start)
	start
	;;

stop)
        stop
        ;;
restart)
        restart
        ;;
reload)
	reload
	;;
*)
	INITNAME=`basename $0`
	printf "Usage: %s {start|stop|reload}\n" "$INITNAME"
	exit 1
esac

exit $RETVAL
