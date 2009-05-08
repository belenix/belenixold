#!/bin/bash
#
# Start/Stop the func server
#

. /lib/svc/share/smf_include.sh

# Get the value of a property defined in the service xml.
getproparg() {
	val=`svcprop -p $1 func`
	[ -n "$val" ] && echo $val
}

PROGNAME=funcd
DATADIR=`getproparg func/data`
PROFILE=`getproparg func/profile`
LOGDIR=`getproparg func/logdir`
USER=func
GROUP=func

if [ -z ${DATADIR} ]; then
	echo "func/data property not set"
	exit $SMF_EXIT_ERR_CONFIG
fi

if [ ! -d ${DATADIR} ]; then
	echo "func/data directory ${DATADIR} is not a valid directory"
	exit $SMF_EXIT_ERR_CONFIG
fi

#
# Initial processing.
#
/usr/lib/func/func-initchk "$USER" "$GROUP" "$DATADIR" "$LOGDIR" "$PROFILE"
[ $? -ne 0 ] && exit $SMF_EXIT_ERR_FATAL

RETVAL=0

start() {
	echo "Starting: " /usr/bin/$PROGNAME --daemon
	su - $USER -c "pfexec $PROGNAME --daemon"
	RETVAL=$?
	return $RETVAL
}

stop() {
	echo "Stopping: " $PROGNAME
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
reload)
	reload
	;;
restart)
	restart
	;;
*)
	INITNAME=`basename $0`
	printf "Usage: %s {start|stop|restart|reload}\n" "$INITNAME"
	exit 1
esac

exit $RETVAL
