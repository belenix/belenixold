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
LOCKFILE=${DATADIR}/`/usr/bin/uname -n`.lock

if [ -z ${DATADIR} ]; then
	echo "func/data property not set"
	exit $SMF_EXIT_ERR_CONFIG
fi

if [ ! -d ${DATADIR} ]; then
	echo "func/data directory ${DATADIR} is not a valid directory"
	exit $SMF_EXIT_ERR_CONFIG
fi

RETVAL=0

start() {
	# Check if it is already running
	if [ ! -f ${LOCKFILE} ]; then
	    echo "Starting: " /usr/bin/$PROGNAME --daemon
	    $PROGNAME --daemon
	    RETVAL=$?
	    [ ${RETVAL} -eq 0 ] && touch ${LOCKFILE}
	    echo
	fi
	return $RETVAL
}

stop() {
	echo "Stopping: " $PROGNAME
	pkill -f /usr/bin/$PROGNAME
	RETVAL=$?
	[ ${RETVAL} -eq 0 ] && rm -f ${LOCKFILE}
  return $RETVAL
}


restart() {
	$0 stop
	$0 start
}	

reload() {
	trap "" SIGHUP
	killall -HUP $PROGNAME
	rm -f ${LOCKFILE}
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
condrestart)
	if [ -f ${LOCKFILE} ]; then
	    restart
	fi
	;;
status)
	status $PROGNAME 
	;;
*)
	INITNAME=`basename $0`
	gprintf "Usage: %s {start|stop|restart|condrestart|status}\n" "$INITNAME"
	exit 1
esac

exit $RETVAL
