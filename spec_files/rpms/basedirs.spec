Summary: Base filesystem directory layout
Name: basedirs
Version: 1
Release: 1%{?dist}
Group: System Environment/Base
License: CDDL

%description
The base filesystem directory layout of the OpenSolaris/Illumos platform.

%prep

%build

%install
cd ${RPM_BUILD_ROOT}
mkdir -p dev
mkdir -p etc
mkdir -p etc/certs
mkdir -p etc/cron.d
mkdir -p etc/crypto
mkdir -p etc/crypto/certs
mkdir -p etc/crypto/crls
mkdir -p etc/default
mkdir -p etc/dev
mkdir -p etc/devices
mkdir -p etc/dfs
mkdir -p etc/dhcp
mkdir -p etc/fs
mkdir -p etc/fs/dev
mkdir -p etc/fs/hsfs
mkdir -p etc/fs/ufs
mkdir -p etc/ftpd
mkdir -p etc/inet
mkdir -p etc/init.d
mkdir -p etc/lib
mkdir -p etc/logadm.d
mkdir -p etc/mail
mkdir -p etc/net
mkdir -p etc/net/ticlts
mkdir -p etc/net/ticots
mkdir -p etc/net/ticotsord
mkdir -p etc/opt
mkdir -p etc/rc0.d
mkdir -p etc/rc1.d
mkdir -p etc/rc2.d
mkdir -p etc/rc3.d
mkdir -p etc/rcS.d
mkdir -p etc/rpcsec
mkdir -p etc/saf
mkdir -p etc/saf/zsmon
mkdir -p etc/sasl
mkdir -p etc/security
mkdir -p etc/security/audit
mkdir -p etc/security/audit/localhost
mkdir -p etc/security/auth_attr.d
mkdir -p etc/security/dev
mkdir -p etc/security/exec_attr.d
mkdir -p etc/security/lib
mkdir -p etc/security/prof_attr.d
mkdir -p etc/skel
mkdir -p etc/svc
mkdir -p etc/svc/profile
mkdir -p etc/svc/profile/site
mkdir -p etc/svc/volatile
mkdir -p etc/sysevent
mkdir -p etc/sysevent/config
mkdir -p etc/tm
mkdir -p etc/user_attr.d
mkdir -p lib
mkdir -p lib/crypto
mkdir -p lib/inet
mkdir -p lib/svc
mkdir -p lib/svc/bin
mkdir -p lib/svc/capture
mkdir -p lib/svc/manifest
mkdir -p lib/svc/manifest/application
mkdir -p lib/svc/manifest/application/management
mkdir -p lib/svc/manifest/application/security
mkdir -p lib/svc/manifest/device
mkdir -p lib/svc/manifest/milestone
mkdir -p lib/svc/manifest/network
mkdir -p lib/svc/manifest/network/dns
mkdir -p lib/svc/manifest/network/ipsec
mkdir -p lib/svc/manifest/network/ldap
mkdir -p lib/svc/manifest/network/routing
mkdir -p lib/svc/manifest/network/rpc
mkdir -p lib/svc/manifest/network/shares
mkdir -p lib/svc/manifest/network/ssl
mkdir -p lib/svc/manifest/platform
mkdir -p lib/svc/manifest/site
mkdir -p lib/svc/manifest/system
mkdir -p lib/svc/manifest/system/device
mkdir -p lib/svc/manifest/system/filesystem
mkdir -p lib/svc/manifest/system/security
mkdir -p lib/svc/manifest/system/svc
mkdir -p lib/svc/method
mkdir -p lib/svc/monitor
mkdir -p lib/svc/seed
mkdir -p lib/svc/share
mkdir -p mnt
mkdir -p opt
mkdir -p proc
mkdir -p root
mkdir -p sbin
mkdir -p system
mkdir -p system/contract
mkdir -p system/object
mkdir -p tmp
mkdir -p usr
mkdir -p usr/bin
mkdir -p usr/bin/i86
mkdir -p usr/bin/%{_arch64}
mkdir -p usr/ccs
mkdir -p usr/ccs/bin
mkdir -p usr/demo
mkdir -p usr/games
mkdir -p usr/has
mkdir -p usr/has/bin
mkdir -p usr/has/lib
mkdir -p usr/kernel
mkdir -p usr/kernel/drv
mkdir -p usr/kernel/drv/%{_arch64}
mkdir -p usr/kernel/exec
mkdir -p usr/kernel/exec/%{_arch64}
mkdir -p usr/kernel/fs
mkdir -p usr/kernel/fs/%{_arch64}
mkdir -p usr/kernel/pcbe
mkdir -p usr/kernel/pcbe/%{_arch64}
mkdir -p usr/kernel/sched
mkdir -p usr/kernel/sched/%{_arch64}
mkdir -p usr/kernel/strmod
mkdir -p usr/kernel/strmod/%{_arch64}
mkdir -p usr/kernel/sys
mkdir -p usr/kernel/sys/%{_arch64}
mkdir -p usr/kvm
mkdir -p usr/lib
mkdir -p usr/lib/sse2
mkdir -p usr/lib/sse4
mkdir -p usr/lib/%{_arch64}
mkdir -p usr/lib/%{_arch64}/sse4
mkdir -p usr/lib/audit
mkdir -p usr/lib/class
mkdir -p usr/lib/class/FX
mkdir -p usr/lib/class/IA
mkdir -p usr/lib/class/RT
mkdir -p usr/lib/class/SDC
mkdir -p usr/lib/class/TS
mkdir -p usr/lib/crypto
mkdir -p usr/lib/devfsadm
mkdir -p usr/lib/devfsadm/linkmod
mkdir -p usr/lib/fs
mkdir -p usr/lib/fs/autofs
mkdir -p usr/lib/fs/autofs/%{_arch64}
mkdir -p usr/lib/fs/cachefs
mkdir -p usr/lib/fs/ctfs
mkdir -p usr/lib/fs/dev
mkdir -p usr/lib/fs/fd
mkdir -p usr/lib/fs/hsfs
mkdir -p usr/lib/fs/lofs
mkdir -p usr/lib/fs/mntfs
mkdir -p usr/lib/fs/nfs
mkdir -p usr/lib/fs/nfs/%{_arch64}
mkdir -p usr/lib/fs/objfs
mkdir -p usr/lib/fs/proc
mkdir -p usr/lib/fs/sharefs
mkdir -p usr/lib/fs/tmpfs
mkdir -p usr/lib/fs/ufs
mkdir -p usr/lib/help
mkdir -p usr/lib/help/auths
mkdir -p usr/lib/help/auths/locale
mkdir -p usr/lib/help/auths/locale/C
mkdir -p usr/lib/help/profiles
mkdir -p usr/lib/help/profiles/locale
mkdir -p usr/lib/help/profiles/locale/C
mkdir -p usr/lib/iconv
mkdir -p usr/lib/inet
mkdir -p usr/lib/inet/i86
mkdir -p usr/lib/inet/%{_arch64}
mkdir -p usr/lib/inet/dhcp
mkdir -p usr/lib/inet/dhcp/nsu
mkdir -p usr/lib/inet/dhcp/svc
mkdir -p usr/lib/locale
mkdir -p usr/lib/locale/C
mkdir -p usr/lib/locale/C/LC_COLLATE
mkdir -p usr/lib/locale/C/LC_CTYPE
mkdir -p usr/lib/locale/C/LC_MESSAGES
mkdir -p usr/lib/locale/C/LC_MONETARY
mkdir -p usr/lib/locale/C/LC_NUMERIC
mkdir -p usr/lib/locale/C/LC_TIME
mkdir -p usr/lib/localedef
mkdir -p usr/lib/localedef/extensions
mkdir -p usr/lib/localedef/src
mkdir -p usr/lib/netsvc
mkdir -p usr/lib/pci
mkdir -p usr/lib/rcm
mkdir -p usr/lib/rcm/modules
mkdir -p usr/lib/rcm/scripts
mkdir -p usr/lib/reparse
mkdir -p usr/lib/saf
mkdir -p usr/lib/secure
mkdir -p usr/lib/secure/%{_arch64}
mkdir -p usr/lib/security
mkdir -p usr/lib/sysevent
mkdir -p usr/lib/sysevent/modules
mkdir -p usr/net
mkdir -p usr/net/nls
mkdir -p usr/net/servers
mkdir -p usr/old
mkdir -p usr/platform
mkdir -p usr/sadm
mkdir -p usr/sadm/bin
mkdir -p usr/sadm/install
mkdir -p usr/sadm/install/scripts
mkdir -p usr/sadm/sysadm
mkdir -p usr/sadm/sysadm/add-ons
mkdir -p usr/sadm/sysadm/bin
mkdir -p usr/sbin
mkdir -p usr/sbin/i86
mkdir -p usr/sbin/%{_arch64}
mkdir -p usr/share
mkdir -p usr/share/doc
mkdir -p usr/share/doc/ksh
mkdir -p usr/share/doc/ksh/images
mkdir -p usr/share/doc/ksh/images/callouts
mkdir -p usr/share/lib
mkdir -p usr/share/lib/mailx
mkdir -p usr/share/lib/pub
mkdir -p usr/share/lib/tabset
mkdir -p usr/share/lib/terminfo
mkdir -p usr/share/lib/terminfo/3
mkdir -p usr/share/lib/terminfo/A
mkdir -p usr/share/lib/terminfo/a
mkdir -p usr/share/lib/terminfo/s
mkdir -p usr/share/lib/terminfo/u
mkdir -p usr/share/lib/terminfo/v
mkdir -p usr/share/lib/terminfo/x
mkdir -p usr/share/lib/xml
mkdir -p usr/share/lib/xml/dtd
mkdir -p usr/share/lib/xml/style
mkdir -p usr/share/lib/zoneinfo
mkdir -p usr/share/lib/zoneinfo/Africa
mkdir -p usr/share/lib/zoneinfo/America
mkdir -p usr/share/lib/zoneinfo/America/Argentina
mkdir -p usr/share/lib/zoneinfo/America/Indiana
mkdir -p usr/share/lib/zoneinfo/America/Kentucky
mkdir -p usr/share/lib/zoneinfo/America/North_Dakota
mkdir -p usr/share/lib/zoneinfo/Antarctica
mkdir -p usr/share/lib/zoneinfo/Arctic
mkdir -p usr/share/lib/zoneinfo/Asia
mkdir -p usr/share/lib/zoneinfo/Atlantic
mkdir -p usr/share/lib/zoneinfo/Australia
mkdir -p usr/share/lib/zoneinfo/Brazil
mkdir -p usr/share/lib/zoneinfo/Canada
mkdir -p usr/share/lib/zoneinfo/Chile
mkdir -p usr/share/lib/zoneinfo/Etc
mkdir -p usr/share/lib/zoneinfo/Europe
mkdir -p usr/share/lib/zoneinfo/Indian
mkdir -p usr/share/lib/zoneinfo/Mexico
mkdir -p usr/share/lib/zoneinfo/Mideast
mkdir -p usr/share/lib/zoneinfo/Pacific
mkdir -p usr/share/lib/zoneinfo/US
mkdir -p usr/share/lib/zoneinfo/src
mkdir -p usr/share/lib/zoneinfo/tab
mkdir -p usr/share/src
mkdir -p usr/xpg4
mkdir -p usr/xpg4/bin
mkdir -p var
mkdir -p var/adm
mkdir -p var/adm/exacct
mkdir -p var/adm/log
mkdir -p var/adm/streams
mkdir -p var/audit
mkdir -p var/cores
mkdir -p var/cron
mkdir -p var/games
mkdir -p var/idmap
mkdir -p var/inet
mkdir -p var/ld
mkdir -p var/ld/%{_arch64}
mkdir -p var/log
mkdir -p var/logadm
mkdir -p var/mail
mkdir -p var/mail/:saved
mkdir -p var/news
mkdir -p var/opt
mkdir -p var/preserve
mkdir -p var/run
mkdir -p var/sadm
mkdir -p var/sadm/system
mkdir -p var/sadm/system/admin
mkdir -p var/saf
mkdir -p var/saf/zsmon
mkdir -p var/spool
mkdir -p var/spool/cron
mkdir -p var/spool/cron/atjobs
mkdir -p var/spool/cron/crontabs
mkdir -p var/spool/locks
mkdir -p var/svc
mkdir -p var/svc/log
mkdir -p var/svc/manifest
mkdir -p var/svc/manifest/application
mkdir -p var/svc/manifest/application/management
mkdir -p var/svc/manifest/application/print
mkdir -p var/svc/manifest/application/security
mkdir -p var/svc/manifest/device
mkdir -p var/svc/manifest/milestone
mkdir -p var/svc/manifest/network
mkdir -p var/svc/manifest/network/dns
mkdir -p var/svc/manifest/network/ipsec
mkdir -p var/svc/manifest/network/ldap
mkdir -p var/svc/manifest/network/nfs
mkdir -p var/svc/manifest/network/nis
mkdir -p var/svc/manifest/network/routing
mkdir -p var/svc/manifest/network/rpc
mkdir -p var/svc/manifest/network/security
mkdir -p var/svc/manifest/network/shares
mkdir -p var/svc/manifest/network/ssl
mkdir -p var/svc/manifest/platform
mkdir -p var/svc/manifest/site
mkdir -p var/svc/manifest/system
mkdir -p var/svc/manifest/system/device
mkdir -p var/svc/manifest/system/filesystem
mkdir -p var/svc/manifest/system/security
mkdir -p var/svc/manifest/system/svc
mkdir -p var/svc/profile
mkdir -p var/tmp
mkdir -p boot
mkdir -p boot/acpi
mkdir -p boot/acpi/tables
mkdir -p boot/solaris
mkdir -p boot/solaris/bin
mkdir -p etc/sock2path.d
mkdir -p kernel
mkdir -p kernel/%{_arch64}
mkdir -p kernel/crypto
mkdir -p kernel/crypto/%{_arch64}
mkdir -p kernel/dacf
mkdir -p kernel/dacf/%{_arch64}
mkdir -p kernel/drv
mkdir -p kernel/drv/%{_arch64}
mkdir -p kernel/exec
mkdir -p kernel/exec/%{_arch64}
mkdir -p kernel/fs
mkdir -p kernel/fs/%{_arch64}
mkdir -p kernel/ipp
mkdir -p kernel/ipp/%{_arch64}
mkdir -p kernel/kiconv
mkdir -p kernel/kiconv/%{_arch64}
mkdir -p kernel/mac
mkdir -p kernel/mac/%{_arch64}
mkdir -p kernel/misc
mkdir -p kernel/misc/%{_arch64}
mkdir -p kernel/misc/scsi_vhci
mkdir -p kernel/misc/scsi_vhci/%{_arch64}
mkdir -p kernel/sched
mkdir -p kernel/sched/%{_arch64}
mkdir -p kernel/socketmod
mkdir -p kernel/socketmod/%{_arch64}
mkdir -p kernel/strmod
mkdir -p kernel/strmod/%{_arch64}
mkdir -p kernel/sys
mkdir -p kernel/sys/%{_arch64}

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%dir %attr(0755, root, sys) /dev
%dir %attr(0755, root, sys) /etc
%dir %attr(0755, root, sys) /etc/certs
%dir %attr(0755, root, sys) /etc/cron.d
%dir %attr(0755, root, sys) /etc/crypto
%dir %attr(0755, root, sys) /etc/crypto/certs
%dir %attr(0755, root, sys) /etc/crypto/crls
%dir %attr(0755, root, sys) /etc/default
%dir %attr(0755, root, sys) /etc/dev
%dir %attr(0755, root, sys) /etc/devices
%dir %attr(0755, root, sys) /etc/dfs
%dir %attr(0755, root, sys) /etc/dhcp
%dir %attr(0755, root, sys) /etc/fs
%dir %attr(0755, root, sys) /etc/fs/dev
%dir %attr(0755, root, sys) /etc/fs/hsfs
%dir %attr(0755, root, sys) /etc/fs/ufs
%dir %attr(0755, root, sys) /etc/ftpd
%dir %attr(0755, root, sys) /etc/inet
%dir %attr(0755, root, sys) /etc/init.d
%dir %attr(0755, root, sys) /etc/lib
%dir %attr(0755, root, sys) /etc/logadm.d
%dir %attr(0755, root, mail) /etc/mail
%dir %attr(0755, root, sys) /etc/net
%dir %attr(0755, root, sys) /etc/net/ticlts
%dir %attr(0755, root, sys) /etc/net/ticots
%dir %attr(0755, root, sys) /etc/net/ticotsord
%dir %attr(0755, root, sys) /etc/opt
%dir %attr(0755, root, sys) /etc/rc0.d
%dir %attr(0755, root, sys) /etc/rc1.d
%dir %attr(0755, root, sys) /etc/rc2.d
%dir %attr(0755, root, sys) /etc/rc3.d
%dir %attr(0755, root, sys) /etc/rcS.d
%dir %attr(0755, root, sys) /etc/rpcsec
%dir %attr(0755, root, bin) /etc/saf
%dir %attr(0755, root, sys) /etc/saf/zsmon
%dir %attr(0755, root, sys) /etc/sasl
%dir %attr(0755, root, sys) /etc/security
%dir %attr(0755, root, sys) /etc/security/audit
%dir %attr(0755, root, sys) /etc/security/audit/localhost
%dir %attr(0755, root, sys) /etc/security/auth_attr.d
%dir %attr(0755, root, sys) /etc/security/dev
%dir %attr(0755, root, sys) /etc/security/exec_attr.d
%dir %attr(0755, root, sys) /etc/security/lib
%dir %attr(0755, root, sys) /etc/security/prof_attr.d
%dir %attr(0755, root, sys) /etc/skel
%dir %attr(0755, root, sys) /etc/svc
%dir %attr(0755, root, sys) /etc/svc/profile
%dir %attr(0755, root, sys) /etc/svc/profile/site
%dir %attr(0755, root, sys) /etc/svc/volatile
%dir %attr(0755, root, sys) /etc/sysevent
%dir %attr(0755, root, sys) /etc/sysevent/config
%dir %attr(0755, root, sys) /etc/tm
%dir %attr(0755, root, sys) /etc/user_attr.d
%dir %attr(0755, root, bin) /lib
%dir %attr(0755, root, bin) /lib/crypto
%dir %attr(0755, root, bin) /lib/inet
%dir %attr(0755, root, bin) /lib/svc
%dir %attr(0755, root, bin) /lib/svc/bin
%dir %attr(0755, root, bin) /lib/svc/capture
%dir %attr(0755, root, sys) /lib/svc/manifest
%dir %attr(0755, root, sys) /lib/svc/manifest/application
%dir %attr(0755, root, sys) /lib/svc/manifest/application/management
%dir %attr(0755, root, sys) /lib/svc/manifest/application/security
%dir %attr(0755, root, sys) /lib/svc/manifest/device
%dir %attr(0755, root, sys) /lib/svc/manifest/milestone
%dir %attr(0755, root, sys) /lib/svc/manifest/network
%dir %attr(0755, root, sys) /lib/svc/manifest/network/dns
%dir %attr(0755, root, sys) /lib/svc/manifest/network/ipsec
%dir %attr(0755, root, sys) /lib/svc/manifest/network/ldap
%dir %attr(0755, root, sys) /lib/svc/manifest/network/routing
%dir %attr(0755, root, sys) /lib/svc/manifest/network/rpc
%dir %attr(0755, root, sys) /lib/svc/manifest/network/shares
%dir %attr(0755, root, sys) /lib/svc/manifest/network/ssl
%dir %attr(0755, root, sys) /lib/svc/manifest/platform
%dir %attr(0755, root, sys) /lib/svc/manifest/site
%dir %attr(0755, root, sys) /lib/svc/manifest/system
%dir %attr(0755, root, sys) /lib/svc/manifest/system/device
%dir %attr(0755, root, sys) /lib/svc/manifest/system/filesystem
%dir %attr(0755, root, sys) /lib/svc/manifest/system/security
%dir %attr(0755, root, sys) /lib/svc/manifest/system/svc
%dir %attr(0755, root, bin) /lib/svc/method
%dir %attr(0755, root, bin) /lib/svc/monitor
%dir %attr(0755, root, bin) /lib/svc/seed
%dir %attr(0755, root, bin) /lib/svc/share
%dir %attr(0755, root, sys) /mnt
%dir %attr(0755, root, sys) /opt
%dir %attr(0555, root, root) /proc
%dir %attr(0700, root, root) /root
%dir %attr(0755, root, sys) /sbin
%dir %attr(0755, root, root) /system
%dir %attr(0555, root, root) /system/contract
%dir %attr(0555, root, root) /system/object
%dir %attr(1777, root, sys) /tmp
%dir %attr(0755, root, sys) /usr
%dir %attr(0755, root, bin) /usr/bin
%dir %attr(0755, root, bin) /usr/bin/i86
%dir %attr(0755, root, bin) /usr/bin/%{_arch64}
%dir %attr(0755, root, bin) /usr/ccs
%dir %attr(0755, root, bin) /usr/ccs/bin
%dir %attr(0755, root, bin) /usr/demo
%dir %attr(0755, root, bin) /usr/games
%dir %attr(0755, root, bin) /usr/has
%dir %attr(0755, root, bin) /usr/has/bin
%dir %attr(0755, root, bin) /usr/has/lib
%dir %attr(0755, root, sys) /usr/kernel
%dir %attr(0755, root, sys) /usr/kernel/drv
%dir %attr(0755, root, sys) /usr/kernel/drv/%{_arch64}
%dir %attr(0755, root, sys) /usr/kernel/exec
%dir %attr(0755, root, sys) /usr/kernel/exec/%{_arch64}
%dir %attr(0755, root, sys) /usr/kernel/fs
%dir %attr(0755, root, sys) /usr/kernel/fs/%{_arch64}
%dir %attr(0755, root, sys) /usr/kernel/pcbe
%dir %attr(0755, root, sys) /usr/kernel/pcbe/%{_arch64}
%dir %attr(0755, root, sys) /usr/kernel/sched
%dir %attr(0755, root, sys) /usr/kernel/sched/%{_arch64}
%dir %attr(0755, root, sys) /usr/kernel/strmod
%dir %attr(0755, root, sys) /usr/kernel/strmod/%{_arch64}
%dir %attr(0755, root, sys) /usr/kernel/sys
%dir %attr(0755, root, sys) /usr/kernel/sys/%{_arch64}
%dir %attr(0755, root, bin) /usr/kvm
%dir %attr(0755, root, bin) /usr/lib
%dir %attr(0755, root, bin) /usr/lib/sse2
%dir %attr(0755, root, bin) /usr/lib/%{_arch64}
%dir %attr(0755, root, bin) /usr/lib/%{_arch64}/sse4
%dir %attr(0755, root, bin) /usr/lib/audit
%dir %attr(0755, root, bin) /usr/lib/class
%dir %attr(0755, root, bin) /usr/lib/class/FX
%dir %attr(0755, root, bin) /usr/lib/class/IA
%dir %attr(0755, root, bin) /usr/lib/class/RT
%dir %attr(0755, root, bin) /usr/lib/class/SDC
%dir %attr(0755, root, bin) /usr/lib/class/TS
%dir %attr(0755, root, bin) /usr/lib/crypto
%dir %attr(0755, root, sys) /usr/lib/devfsadm
%dir %attr(0755, root, sys) /usr/lib/devfsadm/linkmod
%dir %attr(0755, root, sys) /usr/lib/fs
%dir %attr(0755, root, sys) /usr/lib/fs/autofs
%dir %attr(0755, root, sys) /usr/lib/fs/autofs/%{_arch64}
%dir %attr(0755, root, sys) /usr/lib/fs/cachefs
%dir %attr(0755, root, sys) /usr/lib/fs/ctfs
%dir %attr(0755, root, sys) /usr/lib/fs/dev
%dir %attr(0755, root, sys) /usr/lib/fs/fd
%dir %attr(0755, root, sys) /usr/lib/fs/hsfs
%dir %attr(0755, root, sys) /usr/lib/fs/lofs
%dir %attr(0755, root, sys) /usr/lib/fs/mntfs
%dir %attr(0755, root, sys) /usr/lib/fs/nfs
%dir %attr(0755, root, sys) /usr/lib/fs/nfs/%{_arch64}
%dir %attr(0755, root, sys) /usr/lib/fs/objfs
%dir %attr(0755, root, sys) /usr/lib/fs/proc
%dir %attr(0755, root, sys) /usr/lib/fs/sharefs
%dir %attr(0755, root, sys) /usr/lib/fs/tmpfs
%dir %attr(0755, root, sys) /usr/lib/fs/ufs
%dir %attr(0755, root, bin) /usr/lib/help
%dir %attr(0755, root, bin) /usr/lib/help/auths
%dir %attr(0755, root, bin) /usr/lib/help/auths/locale
%dir %attr(0755, root, bin) /usr/lib/help/auths/locale/C
%dir %attr(0755, root, bin) /usr/lib/help/profiles
%dir %attr(0755, root, bin) /usr/lib/help/profiles/locale
%dir %attr(0755, root, bin) /usr/lib/help/profiles/locale/C
%dir %attr(0755, root, bin) /usr/lib/iconv
%dir %attr(0755, root, bin) /usr/lib/inet
%dir %attr(0755, root, bin) /usr/lib/inet/i86
%dir %attr(0755, root, bin) /usr/lib/inet/%{_arch64}
%dir %attr(0755, root, bin) /usr/lib/inet/dhcp
%dir %attr(0755, root, bin) /usr/lib/inet/dhcp/nsu
%dir %attr(0755, root, bin) /usr/lib/inet/dhcp/svc
%dir %attr(0755, root, bin) /usr/lib/locale
%dir %attr(0755, root, bin) /usr/lib/locale/C
%dir %attr(0755, root, bin) /usr/lib/locale/C/LC_COLLATE
%dir %attr(0755, root, bin) /usr/lib/locale/C/LC_CTYPE
%dir %attr(0755, root, bin) /usr/lib/locale/C/LC_MESSAGES
%dir %attr(0755, root, bin) /usr/lib/locale/C/LC_MONETARY
%dir %attr(0755, root, bin) /usr/lib/locale/C/LC_NUMERIC
%dir %attr(0755, root, bin) /usr/lib/locale/C/LC_TIME
%dir %attr(0755, root, bin) /usr/lib/localedef
%dir %attr(0755, root, bin) /usr/lib/localedef/extensions
%dir %attr(0755, root, bin) /usr/lib/localedef/src
%dir %attr(0755, root, sys) /usr/lib/netsvc
%dir %attr(0755, root, bin) /usr/lib/pci
%dir %attr(0755, root, bin) /usr/lib/rcm
%dir %attr(0755, root, bin) /usr/lib/rcm/modules
%dir %attr(0755, root, bin) /usr/lib/rcm/scripts
%dir %attr(0755, root, bin) /usr/lib/reparse
%dir %attr(0755, root, bin) /usr/lib/saf
%dir %attr(0755, root, bin) /usr/lib/secure
%dir %attr(0755, root, bin) /usr/lib/secure/%{_arch64}
%dir %attr(0755, root, bin) /usr/lib/security
%dir %attr(0755, root, bin) /usr/lib/sysevent
%dir %attr(0755, root, bin) /usr/lib/sysevent/modules
%dir %attr(0755, root, sys) /usr/net
%dir %attr(0755, root, sys) /usr/net/nls
%dir %attr(0755, root, sys) /usr/net/servers
%dir %attr(0755, root, bin) /usr/old
%dir %attr(0755, root, sys) /usr/platform
%dir %attr(0755, root, bin) /usr/sadm
%dir %attr(0755, root, bin) /usr/sadm/bin
%dir %attr(0755, root, bin) /usr/sadm/install
%dir %attr(0755, root, bin) /usr/sadm/install/scripts
%dir %attr(0755, root, bin) /usr/sadm/sysadm
%dir %attr(0755, root, bin) /usr/sadm/sysadm/add-ons
%dir %attr(0755, root, bin) /usr/sadm/sysadm/bin
%dir %attr(0755, root, bin) /usr/sbin
%dir %attr(0755, root, bin) /usr/sbin/i86
%dir %attr(0755, root, bin) /usr/sbin/%{_arch64}
%dir %attr(0755, root, sys) /usr/share
%dir %attr(0755, root, other) /usr/share/doc
%dir %attr(0755, root, bin) /usr/share/doc/ksh
%dir %attr(0755, root, bin) /usr/share/doc/ksh/images
%dir %attr(0755, root, bin) /usr/share/doc/ksh/images/callouts
%dir %attr(0755, root, sys) /usr/share/lib
%dir %attr(0755, root, bin) /usr/share/lib/mailx
%dir %attr(0755, root, bin) /usr/share/lib/pub
%dir %attr(0755, root, bin) /usr/share/lib/tabset
%dir %attr(0755, root, bin) /usr/share/lib/terminfo
%dir %attr(0755, root, bin) /usr/share/lib/terminfo/3
%dir %attr(0755, root, bin) /usr/share/lib/terminfo/A
%dir %attr(0755, root, bin) /usr/share/lib/terminfo/a
%dir %attr(0755, root, bin) /usr/share/lib/terminfo/s
%dir %attr(0755, root, bin) /usr/share/lib/terminfo/u
%dir %attr(0755, root, bin) /usr/share/lib/terminfo/v
%dir %attr(0755, root, bin) /usr/share/lib/terminfo/x
%dir %attr(0755, root, sys) /usr/share/lib/xml
%dir %attr(0755, root, sys) /usr/share/lib/xml/dtd
%dir %attr(0755, root, sys) /usr/share/lib/xml/style
%dir %attr(0755, root, bin) /usr/share/lib/zoneinfo
%dir %attr(0755, root, bin) /usr/share/lib/zoneinfo/Africa
%dir %attr(0755, root, bin) /usr/share/lib/zoneinfo/America
%dir %attr(0755, root, bin) /usr/share/lib/zoneinfo/America/Argentina
%dir %attr(0755, root, bin) /usr/share/lib/zoneinfo/America/Indiana
%dir %attr(0755, root, bin) /usr/share/lib/zoneinfo/America/Kentucky
%dir %attr(0755, root, bin) /usr/share/lib/zoneinfo/America/North_Dakota
%dir %attr(0755, root, bin) /usr/share/lib/zoneinfo/Antarctica
%dir %attr(0755, root, bin) /usr/share/lib/zoneinfo/Arctic
%dir %attr(0755, root, bin) /usr/share/lib/zoneinfo/Asia
%dir %attr(0755, root, bin) /usr/share/lib/zoneinfo/Atlantic
%dir %attr(0755, root, bin) /usr/share/lib/zoneinfo/Australia
%dir %attr(0755, root, bin) /usr/share/lib/zoneinfo/Brazil
%dir %attr(0755, root, bin) /usr/share/lib/zoneinfo/Canada
%dir %attr(0755, root, bin) /usr/share/lib/zoneinfo/Chile
%dir %attr(0755, root, bin) /usr/share/lib/zoneinfo/Etc
%dir %attr(0755, root, bin) /usr/share/lib/zoneinfo/Europe
%dir %attr(0755, root, bin) /usr/share/lib/zoneinfo/Indian
%dir %attr(0755, root, bin) /usr/share/lib/zoneinfo/Mexico
%dir %attr(0755, root, bin) /usr/share/lib/zoneinfo/Mideast
%dir %attr(0755, root, bin) /usr/share/lib/zoneinfo/Pacific
%dir %attr(0755, root, bin) /usr/share/lib/zoneinfo/US
%dir %attr(0755, root, bin) /usr/share/lib/zoneinfo/src
%dir %attr(0755, root, bin) /usr/share/lib/zoneinfo/tab
%dir %attr(0755, root, sys) /usr/share/src
%dir %attr(0755, root, bin) /usr/xpg4
%dir %attr(0755, root, bin) /usr/xpg4/bin
%dir %attr(0755, root, sys) /var
%dir %attr(0775, root, sys) /var/adm
%dir %attr(0755, adm, adm) /var/adm/exacct
%dir %attr(0755, adm, adm) /var/adm/log
%dir %attr(0755, root, sys) /var/adm/streams
%dir %attr(0755, root, sys) /var/audit
%dir %attr(0755, root, sys) /var/cores
%dir %attr(0755, root, sys) /var/cron
%dir %attr(0755, root, bin) /var/games
%dir %attr(0755, daemon, daemon) /var/idmap
%dir %attr(0755, root, sys) /var/inet
%dir %attr(0755, root, bin) /var/ld
%dir %attr(0755, root, bin) /var/ld/%{_arch64}
%dir %attr(0755, root, sys) /var/log
%dir %attr(0755, root, bin) /var/logadm
%dir %attr(1777, root, mail) /var/mail
%dir %attr(0775, root, mail) /var/mail/:saved
%dir %attr(0755, root, bin) /var/news
%dir %attr(0755, root, sys) /var/opt
%dir %attr(1777, root, bin) /var/preserve
%dir %attr(0755, root, sys) /var/run
%dir %attr(0755, root, sys) /var/sadm
%dir %attr(0755, root, sys) /var/sadm/system
%dir %attr(0755, root, sys) /var/sadm/system/admin
%dir %attr(0755, root, bin) /var/saf
%dir %attr(0755, root, sys) /var/saf/zsmon
%dir %attr(0755, root, bin) /var/spool
%dir %attr(0755, root, sys) /var/spool/cron
%dir %attr(0755, root, sys) /var/spool/cron/atjobs
%dir %attr(0755, root, sys) /var/spool/cron/crontabs
%dir %attr(0755, uucp, uucp) /var/spool/locks
%dir %attr(0755, root, sys) /var/svc
%dir %attr(0755, root, sys) /var/svc/log
%dir %attr(0755, root, sys) /var/svc/manifest
%dir %attr(0755, root, sys) /var/svc/manifest/application
%dir %attr(0755, root, sys) /var/svc/manifest/application/management
%dir %attr(0755, root, sys) /var/svc/manifest/application/print
%dir %attr(0755, root, sys) /var/svc/manifest/application/security
%dir %attr(0755, root, sys) /var/svc/manifest/device
%dir %attr(0755, root, sys) /var/svc/manifest/milestone
%dir %attr(0755, root, sys) /var/svc/manifest/network
%dir %attr(0755, root, sys) /var/svc/manifest/network/dns
%dir %attr(0755, root, sys) /var/svc/manifest/network/ipsec
%dir %attr(0755, root, sys) /var/svc/manifest/network/ldap
%dir %attr(0755, root, sys) /var/svc/manifest/network/nfs
%dir %attr(0755, root, sys) /var/svc/manifest/network/nis
%dir %attr(0755, root, sys) /var/svc/manifest/network/routing
%dir %attr(0755, root, sys) /var/svc/manifest/network/rpc
%dir %attr(0755, root, sys) /var/svc/manifest/network/security
%dir %attr(0755, root, sys) /var/svc/manifest/network/shares
%dir %attr(0755, root, sys) /var/svc/manifest/network/ssl
%dir %attr(0755, root, sys) /var/svc/manifest/platform
%dir %attr(0755, root, sys) /var/svc/manifest/site
%dir %attr(0755, root, sys) /var/svc/manifest/system
%dir %attr(0755, root, sys) /var/svc/manifest/system/device
%dir %attr(0755, root, sys) /var/svc/manifest/system/filesystem
%dir %attr(0755, root, sys) /var/svc/manifest/system/security
%dir %attr(0755, root, sys) /var/svc/manifest/system/svc
%dir %attr(0755, root, sys) /var/svc/profile
%dir %attr(1777, root, sys) /var/tmp
%dir %attr(0755, root, sys) /boot
%dir %attr(0755, root, sys) /boot/acpi
%dir %attr(0755, root, sys) /boot/acpi/tables
%dir %attr(0755, root, sys) /boot/solaris
%dir %attr(0755, root, sys) /boot/solaris/bin
%dir %attr(0755, root, sys) /etc/sock2path.d
%dir %attr(0755, root, sys) /kernel
%dir %attr(0755, root, sys) /kernel/%{_arch64}
%dir %attr(0755, root, sys) /kernel/crypto
%dir %attr(0755, root, sys) /kernel/crypto/%{_arch64}
%dir %attr(0755, root, sys) /kernel/dacf
%dir %attr(0755, root, sys) /kernel/dacf/%{_arch64}
%dir %attr(0755, root, sys) /kernel/drv
%dir %attr(0755, root, sys) /kernel/drv/%{_arch64}
%dir %attr(0755, root, sys) /kernel/exec
%dir %attr(0755, root, sys) /kernel/exec/%{_arch64}
%dir %attr(0755, root, sys) /kernel/fs
%dir %attr(0755, root, sys) /kernel/fs/%{_arch64}
%dir %attr(0755, root, sys) /kernel/ipp
%dir %attr(0755, root, sys) /kernel/ipp/%{_arch64}
%dir %attr(0755, root, sys) /kernel/kiconv
%dir %attr(0755, root, sys) /kernel/kiconv/%{_arch64}
%dir %attr(0755, root, sys) /kernel/mac
%dir %attr(0755, root, sys) /kernel/mac/%{_arch64}
%dir %attr(0755, root, sys) /kernel/misc
%dir %attr(0755, root, sys) /kernel/misc/%{_arch64}
%dir %attr(0755, root, sys) /kernel/misc/scsi_vhci
%dir %attr(0755, root, sys) /kernel/misc/scsi_vhci/%{_arch64}
%dir %attr(0755, root, sys) /kernel/sched
%dir %attr(0755, root, sys) /kernel/sched/%{_arch64}
%dir %attr(0755, root, sys) /kernel/socketmod
%dir %attr(0755, root, sys) /kernel/socketmod/%{_arch64}
%dir %attr(0755, root, sys) /kernel/strmod
%dir %attr(0755, root, sys) /kernel/strmod/%{_arch64}
%dir %attr(0755, root, sys) /kernel/sys
%dir %attr(0755, root, sys) /kernel/sys/%{_arch64}
