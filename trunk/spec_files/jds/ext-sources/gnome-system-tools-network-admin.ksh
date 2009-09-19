#!/bin/ksh -ph

APP_TMP_DIR=`mktemp -d -t net_admin_XXXXXX`

trap "rm -rf ${APP_TMP_DIR}" 0 1 2 11 15

#Figure out location of BASEDIR
BASEDIR=${0%/bin/*}
BASEDIR=${BASEDIR:-/usr} 

PATH=/usr/sbin:/sbin:${BASEDIR}/sbin:${PATH}
export PATH

zenity=$BASEDIR/bin/zenity

NET_PHYSICAL_SVC=svc:/network/physical

LING=$LC_ALL
LING=${LING:-$LC_MESSAGES}
LING=${LING:-$LANG}

TEXTDOMAINDIR=${BASEDIR}/share/locale
TEXTDOMAIN=gnome-system-tools
export TEXTDOMAINDIR TEXTDOMAIN


N_() {
    printf "%s\n" "$@"
}

_() {
    if [ x"$LING" = x -o x"$LING" = x"C" -o x"$LING" = x"POSIX" ] ; then
        printf "%s\n" "$@"
    else
        MSGID=`printf "%s\n" "$@" | sed -e 's|\\\\|\\\\\\\\|g'`
        gettext "$MSGID"
    fi
}

isRunningNWAM() {
    state_nwam=`/usr/bin/svcs -H -o state svc:/network/physical:nwam 2>/dev/null`

    if [ "${state_nwam}" = "online" ]
    then
        return 0
    else
        return 1
    fi
}

set_network_physical () {
    if [ "$1" = "auto" ]; then
        to_enable=nwam
        to_disable=default
    else
        to_enable=default
        to_disable=nwam
    fi

    # Try svcadm directly, use might have sufficient auths.
    switch_completed=false
    if pfexec -P all svcadm disable -s "${NET_PHYSICAL_SVC}:${to_disable}" 2>/dev/null; then
        if pfexec -P all svcadm enable -s "${NET_PHYSICAL_SVC}:${to_enable}" 2>/dev/null; then
            switch_completed=true
        else 
            # Restore to previous state.
            pfexec -P all svcadm enable -s "${NET_PHYSICAL_SVC}:${to_disable}" 2>/dev/null
        fi
    fi

    if [ "$switch_completed" = "false" ]; then
        # Try again using gksu since svcadm failed.
        TMPFILE=${APP_TMP_DIR}/switch_to_${1}.$$.sh
        cat > ${TMPFILE} <<_EOF
#!/bin/sh
    if svcadm disable -s "${NET_PHYSICAL_SVC}:${to_disable}"; then
        if svcadm enable -s "${NET_PHYSICAL_SVC}:${to_enable}"; then
            :
        else 
            # Restore to previous state
            svcadm enable -s "${NET_PHYSICAL_SVC}:${to_disable}"
        fi
    fi
_EOF
        chmod 555 ${TMPFILE}
        gksu --title="$TITLE" /bin/sh ${TMPFILE}
    fi

    #Check to see if we successfully completed all tasks.
    sleep 3 # Slight delay to give SMF time to switch.
    if [ "${to_enable}" = "nwam" ]; then
        if isRunningNWAM; then
            rval=0
        else
            # If NWAM is not running then we failed.
            rval=1
        fi
    else
        # NWAM should be disabled in this case.
        if isRunningNWAM; then
            # If NWAM still running we failed.
            rval=1
        else
            rval=0
        fi
    fi

    return $rval
}

# SUN_BRANDING
_TITLE=`N_ "Network Administration"`

# SUN_BRANDING
_MANUAL_OK_BUTTON=`N_ "Manual"`
# SUN_BRANDING
_MANUAL_CANCEL_BUTTON=`N_ "Cancel"`
# SUN_BRANDING
_MANUAL_ERROR=`N_ "An error occured switching to Manual mode."`
# SUN_BRANDING
_MANUAL_MESSAGE_1=`N_ "\
Your system is currently configured to manage the\\n\
network automatically. Click \"%s\" to manually\\n\
configure the network connection."`

# SUN_BRANDING
_AUTO_OK_BUTTON=`N_ "Automatic"`
# SUN_BRANDING
_AUTO_CANCEL_BUTTON=`N_ "Continue"`
# SUN_BRANDING
_AUTO_ERROR=`N_ "An error occured switching to Automatic mode."`
# SUN_BRANDING
_AUTO_MESSAGE=`N_ "\
Your system is currently configured to manage the\\n\
network manually. Click \"%s\" to have the\\n\
network configured automatically.\\n\
\\n\
Otherwise click \"%s\" to continue to\\n\
configure the network manually."`

TITLE=`_ "${_TITLE}"`

if isRunningNWAM; then
    ALTMODE='MANUAL'
    OK_BUTTON=`_ "${_MANUAL_OK_BUTTON}"`
    CANCEL_BUTTON=`_ "${_MANUAL_CANCEL_BUTTON}"`
    ERROR_MSG=`_ "${_MANUAL_ERROR}"`
    MSG=`_ "${_MANUAL_MESSAGE}"`
    MSG=`printf "$MSG\n" "${OK_BUTTON}"`
else
    ALTMODE='AUTO'
    OK_BUTTON=`_ "${_AUTO_OK_BUTTON}"`
    CANCEL_BUTTON=`_ "${_AUTO_CANCEL_BUTTON}"`
    ERROR_MSG=`_ "${_AUTO_ERROR}"`
    MSG=`_ "${_AUTO_MESSAGE}"`
    MSG=`printf "$MSG\n" "${OK_BUTTON}" "${CANCEL_BUTTON}"`
fi


if [ -n "${1}" -a "X${1}" = "X--switch-to-manual" ]; then
    shift
    if [ "$ALTMODE" = "MANUAL" ]; then
        if set_network_physical manual; then
            :
        else
            $zenity --error --title="${TITLE}" --text="${ERROR_MSG}"
        fi
    fi
elif [ -n "${1}" -a "X${1}" = "X--switch-to-auto" ]; then
    shift
    if [ "$ALTMODE" = "AUTO" ]; then
        if set_network_physical auto; then
            :
        else
            $zenity --error --title="${TITLE}" --text="${ERROR_MSG}"
        fi
    fi
else 
    $zenity --question --ok-label="${OK_BUTTON}" --cancel-label="${CANCEL_BUTTON}" \
            --title="${TITLE}" --text="${MSG}"
    response_code=$?

    if [ "$ALTMODE" = "MANUAL" ]; then
        if [ $response_code -eq 0 ]; then   # Switch to Manual
            if set_network_physical manual; then
                exec ${BASEDIR}/lib/network-admin ${1+"$@"}
            else
                $zenity --error --title="${TITLE}" --text="${ERROR_MSG}"
            fi
        else
            exit 0  # Do nothing
        fi
    elif [ "$ALTMODE" = "AUTO" ]; then
        if [ $response_code -eq 0 ]; then   # Switch to Auto
            if set_network_physical auto; then
                :
            else
                $zenity --error --title="${TITLE}" --text="${ERROR_MSG}"
            fi
        else
            exec ${BASEDIR}/lib/network-admin ${1+"$@"}
        fi
    fi
fi
