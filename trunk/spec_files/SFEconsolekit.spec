#
# spec file for package SUNWconsolekit
#
# includes module(s): ConsoleKit
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#
%include Solaris.inc

# Option to decide whether or not build library pam_ck_connector,
# which implements pam_sm_open_session(3PAM) and pam_sm_close_session(3PAM).
# By default, we don't build it.
#
# Note: To enable this pam module, you have to manually add 
# an entry to /etc/pam.conf after installing SUNWconsolekit-pam,
# like this.
# "login   session required       pam_ck_connector.so debug"
#
%define build_pam_module 1

%use ck = ConsoleKit.spec

Name:                    SFEconsolekit
Summary:                 Framework for tracking users, login sessions, and seats.
Version:                 %{ck.version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Source1:                 consolekit.xml

%include default-depend.inc

Requires: SUNWglib2
Requires: SUNWdbus-libs
Requires: SUNWdbus-glib
Requires: %{name}-root
BuildRequires: SUNWglib2-devel
BuildRequires: SUNWdbus-devel
BuildRequires: SUNWdbus-glib-devel

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%if %build_pam_module
%package pam
Summary:		 %{summary} - PAM module to register simple text logins.
SUNW_BaseDir:		 %{_basedir}
%include default-depend.inc
Requires: %name
%endif

%prep
rm -rf %name-%version
mkdir %name-%version
%ck.prep -d %name-%version

%build
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="%_ldflags"

%ck.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%ck.install -d %name-%version

# These programs are intended to be used if you want ConsoleKit to be
# like utmp/wtmp and log system start/restart/stop events.  There are
# no plans to support using ConsoleKit like utmp/wtmp, so do not
# install these for now.
#
rm $RPM_BUILD_ROOT/%{_sbindir}/ck-log-system-start
rm $RPM_BUILD_ROOT/%{_sbindir}/ck-log-system-restart
rm $RPM_BUILD_ROOT/%{_sbindir}/ck-log-system-stop

install -d $RPM_BUILD_ROOT/var/svc/manifest/system
install --mode=0444 %SOURCE1 $RPM_BUILD_ROOT/var/svc/manifest/system

%clean
rm -rf $RPM_BUILD_ROOT

%pre root
#!/bin/sh
#
# Copyright 2009 Sun Microsystems, Inc.  All rights reserved.
# Use is subject to license terms.
#

# Presence of this temp file will tell postinstall script
# that the consolekit service is already installed, in which case
# the current service state will be preserved, be it enabled
# or disabled.
rm -f $PKG_INSTALL_ROOT/var/consolekit_installed.tmp > /dev/null 2>&1

if [ -f $PKG_INSTALL_ROOT/var/svc/manifest/system/consolekit.xml ]; then
        touch $PKG_INSTALL_ROOT/var/consolekit_installed.tmp
fi

exit 0

%post root
#!/bin/sh
#
# Copyright 2009 Sun Microsystems, Inc.  All rights reserved.
# Use is subject to license terms.
#

# Preinstall script will create this file if consolekit service was 
# already installed, in which case we preserve current service state,
# be it enabled or disabled.
if [ -f $PKG_INSTALL_ROOT/var/consolekit_installed.tmp ]; then
        rm -f $PKG_INSTALL_ROOT/var/consolekit_installed.tmp
else
        # enable consolekit:
        # - PKG_INSTALL_ROOT is / or empty when installing onto a live system
        #   and we can invoke svcadm directly;
        # - otherwise it's upgrade, so we append to the upgrade script
        if [ "${PKG_INSTALL_ROOT:-/}" = "/" ]; then
                if [ `/sbin/zonename` = global ]; then
                        /usr/sbin/svcadm enable -r svc:/system/consolekit:default
                fi
        else
                cat >> ${PKG_INSTALL_ROOT}/var/svc/profile/upgrade <<-EOF
                if [ \`/sbin/zonename\` = global ]; then
                        /usr/sbin/svcadm enable -r svc:/system/consolekit:default
                fi
EOF
        fi
fi

exit 0

%files
%doc -d ConsoleKit-%{ck.version} README AUTHORS
%doc(bzip2) -d ConsoleKit-%{ck.version} COPYING NEWS
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr (-, root, bin)
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/lib*.so*
%{_libdir}/ConsoleKit
%{_libexecdir}/ck-collect-session-info
%{_libexecdir}/ck-get-x11-server-pid
%{_libexecdir}/ck-get-x11-display-device
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/dbus-1

%files root
%defattr (-, root, sys)
%{_sysconfdir}/ConsoleKit
%dir %attr (0755, root, bin) %{_sysconfdir}/dbus-1
%dir %attr (0755, root, bin) %{_sysconfdir}/dbus-1/system.d
%{_sysconfdir}/dbus-1/system.d/ConsoleKit.conf
%dir %attr (0755, root, sys) %dir %{_localstatedir}
# don't use %_localstatedir here, because this is an absolute path
# defined by another package, so it has to be /var/svc even if this
# package's %_localstatedir is redefined
/var/svc/*
%dir %attr (0755, root, sys) %{_localstatedir}/log
%dir %attr (0755, root, root) %{_localstatedir}/log/ConsoleKit

%files devel
%defattr (-, root, bin)
%{_includedir}/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%if %build_pam_module
%files pam
%defattr (-, root, bin)
%{_libdir}/security/pam*.so*
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}/man8/*
%endif

%changelog
* Thu Jul 30 2009 - halton.huo@sun.com
- Add %pre and %post for -root pkg.
* Mon Jul 27 2009 - halton.huo@sun.com
- Move from SFE and spilit base part to ConsoleKit.spec
* Thu Jul 23 2009 - halton.huo@sun.com
- Bump to 0.3.1
- Remove upstreamed patch: emptystruct.diff, pam.diff, solaris-getpwnamr.diff
  and reorder rest
- Add patch dev-console.diff to change owner of /dev/console for console login
* Tue Jun 23 2009 - halton.huo@sun.com
- Add copyright
* Wed Apr 08 2009 - halton.huo@sun.com
- Add patch8: solaris-getpwnamr.diff to fix bug #22361
* Wed Apr 08 2009 - halton.huo@sun.com
- Add patch5: add-sunray-type.diff to add Sunray for display-typs.conf.in
- Add patch6: dynamic-tty.diff to add --tty for ck-dynaminc
- Add patch7: solaris-vtdaemon.diff to check vtdaemon service code for Solaris
* Thu Mar 26 2009 - halton.huo@sun.com
- Add all files under etc/ConsoleKit/ to %files root
* Sat Feb 07 2009 - brian.cameron@sun.com
- Package should not install anything to  /var/run.
* Tue Dec 30 2008 - halton.huo@sun.com
- Add patch ck-dynamic.diff to fix bug #19333
* Tue Oct 21 2008 - halton.huo@sun.com
- Add standard patch comment
* Thu Aug 07 2008 - brian.cameorn@sun.com
- Bump to 0.3.0.
* Tue Jun 24 2008 - simon.zheng@sun.com
- Add patch 05-getcurrentsession.diff for freedesktop bug #15866.
* Tue Mar 11 2008 - brian.cameron@sun.com
- Minor cleanup
* Tue Mar 04 2008 - simon.zheng@sun.com
- Add patch 04-ck-history.diff to fix crash.
* Sat Mar 01 2008 - simon.zheng@sun.com
- Add patch 03-pam.diff to build pam module library 
  pam-ck-connector that registers text login session into 
  ConsoleKit. And this library is packed as a separate 
  package called SFEconsolekit-pam.
* Mon Feb 25 2008 - brian.cameron@sun.com
- Bump release to 0.2.10.  Worked with the maintainer to get seven
  recent patches upstream.
* Mon Feb 25 2008 - simon.zheng@sun.com
- Rework ConsoleKit-06-fixvt.diff for better macro definition.
* Fri Feb 22 2008 - brian.cameron@sun.com
- Add the patch ConsoleKit-05-devname.diff that Simon wrote, patch
  ConsoleKit-06-fixvt.diff so that patch 4 builds properly when you
  do not have VT installed, patch ConsoleKit-07-fixactiveconsole.diff
  so that Active device is set to "/dev/console" when not using VT,
  ConsoleKit-08-fixseat.diff to correct a crash due to a NULL string
  in a printf, and ConsoleKit-09-novt.diff to fix ConsoleKit so that
  it sets x11-display-device to "/dev/console" when not using
  VT.
* Tue Feb 19 2008 - simon.zheng@sun.com
- Add patch ConsoleKit-04-vt.diff. Use sysnchronous event notification
  in STREAMS to monitor VT activation. 
* Fri Feb 15 2008 - brian.cameron@sun.com
- Rework ConsoleKit-03-paths.diff so it makes better use of #ifdefs.
* Fri Feb 15 2008 - simon.zheng@sun.com
- Bump to 0.2.9. Add ConsoleKit-03-noheaderpaths.diff because there's not
  header paths.h on Solaris.
* Thu Feb 07 2008 - Brian.Cameron@sun.com
- Add /var/log/ConsoleKit/history file to packaging.
* Thu Jan 31 2008 - Brian.Cameron@sun.com
- Bump to 0.2.7.  Remove two upstream patches added on January 25,
  2007.
* Fri Jan 25 2008 - Brian.Cameron@sun.com
- Bump to 0.2.6.  Rework patches.  Add patch ConsoleKit-02-RBAC.diff
  to make ConsoleKit use RBAC instead of PolicyKit on Solaris.
  Patch ConsoleKit-03-fixbugs.diff fixes some bugs I found.
* Tue Sep 18 2007 - Brian.Cameron@sun.com
- Bump to 0.2.3.  Remove upstream ConsoleKit-01-head.diff
  patch and add ConsoleKit-02-fixsolaris.diff to fix some
  issues building ConsoleKit when VT is not present.
* Mon Aug 16 2007 - Brian.Cameron@sun.com
- Created.
