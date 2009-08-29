#
# spec file for package SUNWdbus
#
# includes module(s): dbus
#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: yippi
#

%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%define _libexecdir %{_basedir}/lib
%use dbus_64 = dbus.spec
%endif

%include base.inc
%use dbus = dbus.spec

Name:                    SUNWdbus
Summary:                 Simple IPC library based on messages
Version:                 %{dbus.version}
Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Source1:        dbus.xml
Source2:        svc-dbus
Source3:        0070.dbus
%include default-depend.inc
Requires:	SUNWxwrtl
Requires:	SUNWdbus-libs
Requires:	SUNWdbus-root
Requires:	SUNWlxml
Requires:	SUNWlexpt
Requires:	SUNWPython-extra
BuildRequires:	SUNWlxml
BuildRequires:	SUNWsfwhea
BuildRequires:	SUNWPython-extra

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc

%package libs
Summary:                 %{summary} - client libraries
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
BuildRequires:	SUNWdbus-devel

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%dbus_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%dbus.prep -d %name-%version/%{base_arch}

cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build
# Put /usr/ccs/lib first in the PATH so that cpp is picked up from there
# note: I didn't put /usr/lib in the PATH because there's too much other
# stuff in there
#
export PATH=/usr/ccs/lib:$PATH
%ifarch amd64 sparcv9
%dbus_64.build -d %name-%version/%_arch64
%endif
 
%dbus.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%dbus_64.install -d %name-%version/%_arch64
%endif

%dbus.install -d %name-%version/%{base_arch}
rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd $RPM_BUILD_ROOT%{_bindir}/%{_arch64}
rm dbus-launch dbus-monitor dbus-cleanup-sockets dbus-send dbus-uuidgen
cd ..
rmdir %{_arch64}
%endif

# The /var/run directory should not be included with the packages.
# D-Bus will create it at run-time.
#
rmdir $RPM_BUILD_ROOT/var/run/dbus
rmdir $RPM_BUILD_ROOT/var/run

# Add SMF integration files.
#
mkdir -p $RPM_BUILD_ROOT/var/svc/manifest/system
chmod -R 755 $RPM_BUILD_ROOT/var/svc
cp %SOURCE1 $RPM_BUILD_ROOT/var/svc/manifest/system/
mkdir -p $RPM_BUILD_ROOT/lib/svc/method
chmod -R 755 $RPM_BUILD_ROOT/lib
cp %SOURCE2 $RPM_BUILD_ROOT/lib/svc/method/

# Add in dbus session launching for gdm
#
install --mode=0755 -d $RPM_BUILD_ROOT/%{_sysconfdir}
install --mode=0755 -d $RPM_BUILD_ROOT/%{_sysconfdir}/X11
install --mode=0755 -d $RPM_BUILD_ROOT/%{_sysconfdir}/X11/xinit
install --mode=0755 -d $RPM_BUILD_ROOT/%{_sysconfdir}/X11/xinit/xinitrc.d
install --mode=0755 %SOURCE3 $RPM_BUILD_ROOT/%{_sysconfdir}/X11/xinit/xinitrc.d/0070.dbus

mkdir -p $RPM_BUILD_ROOT/etc/security
echo 'solaris.smf.manage.dbus:::Manage D-BUS Service States::help=SmfDBUSStates.html' > $RPM_BUILD_ROOT/etc/security/auth_attr
echo 'D-BUS Management:::Manage D-BUS:auths=solaris.smf.manage.dbus;help=RtDBUSMngmnt.html' > $RPM_BUILD_ROOT/etc/security/prof_attr

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%if %(test -f /usr/sadm/install/scripts/i.manifest && echo 0 || echo 1)
%iclass manifest -f i.manifest
%endif

%pre root
#!/bin/sh
#
# Copyright 2006 Sun Microsystems, Inc.  All rights reserved.
# Use is subject to license terms.
#

# Presence of this temp file will tell postinstall script
# that the dbus service is already installed, in which case
# the current service state will be preserved, be it enabled
# or disabled.
rm -f $PKG_INSTALL_ROOT/var/dbus_installed.tmp > /dev/null 2>&1

if [ -f $PKG_INSTALL_ROOT/var/svc/manifest/system/dbus.xml ]; then 
	touch $PKG_INSTALL_ROOT/var/dbus_installed.tmp
fi

exit 0

%post root
#!/bin/sh
#
# Copyright 2006 Sun Microsystems, Inc.  All rights reserved.
# Use is subject to license terms.
#

# Preinstall script will create this file if dbus service was already
# installed, in which case we preserve current service state,
# be it enabled or disabled.
if [ -f $PKG_INSTALL_ROOT/var/dbus_installed.tmp ]; then
	rm -f $PKG_INSTALL_ROOT/var/dbus_installed.tmp
else
	# enable dbus:
	# - PKG_INSTALL_ROOT is / or empty when installing onto a live system
	#   and we can invoke svcadm directly;
	# - otherwise it's upgrade, so we append to the upgrade script
	if [ "${PKG_INSTALL_ROOT:-/}" = "/" ]; then
		if [ `/sbin/zonename` = global ]; then
			/usr/sbin/svcadm enable svc:/system/dbus:default
		fi
	else
		cat >> ${PKG_INSTALL_ROOT}/var/svc/profile/upgrade <<-EOF
		if [ \`/sbin/zonename\` = global ]; then
			/usr/sbin/svcadm enable svc:/system/dbus:default
		fi
EOF
	fi
fi

exit 0

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%{_libexecdir}/dbus-1
%{_libexecdir}/dbus-daemon
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/dbus-1
%doc -d %{base_arch}/dbus-%{dbus.version} AUTHORS README
%doc(bzip2) -d %{base_arch}/dbus-%{dbus.version} ChangeLog ChangeLog.pre-1-0
%doc(bzip2) -d %{base_arch}/dbus-%{dbus.version} ChangeLog.pre-1-2
%doc(bzip2) -d %{base_arch}/dbus-%{dbus.version} COPYING NEWS
%doc(bzip2) -d %{base_arch}/dbus-%{dbus.version} NEWS.pre-1-0 NEWS.pre-1-2
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man1/*
%{_mandir}/man3/*

%files libs
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libdbus*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/libdbus*
%endif

%files root
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_sysconfdir}
%config %{_sysconfdir}/dbus-1
%dir %attr (0755, root, sys) %{_sysconfdir}/X11
%dir %attr (0755, root, sys) %{_sysconfdir}/X11/xinit
%dir %attr (0755, root, sys) %{_sysconfdir}/X11/xinit/xinitrc.d
%{_sysconfdir}/X11/xinit/xinitrc.d/0070.dbus
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, other) %{_localstatedir}/lib
%attr (0755, root, root) %{_localstatedir}/lib/dbus
%dir %attr (0755, root, sys) /var/svc
%dir %attr (0755, root, sys) /var/svc/manifest
%dir %attr (0755, root, sys) /var/svc/manifest/system
%class(manifest) %attr (0444, root, sys) /var/svc/manifest/system/dbus.xml
%attr (0555, root, bin) /lib/svc/method/svc-dbus
%dir %attr (0755, root, sys) /etc/security
%config %class (rbac) %attr (0644, root, sys) /etc/security/auth_attr
%config %class (rbac) %attr (0644, root, sys) /etc/security/prof_attr

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%{_libdir}/dbus*/include
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}/dbus-1.0
%{_libdir}/%{_arch64}/pkgconfig/*.pc
%{_libdir}/%{_arch64}/dbus-1.0/*
%endif

%changelog
* Mon Mar 02 2009 - dave.lin@sun.com
- Add man/man3.
* Thu Feb 05 2009 - brian.cameron@sun.com
- Do not package /var/run files.  Fixes bug #6799059.
* Wed Feb 04 2009 - takao.fujiwara@sun.com
- Renamed 0005.dbus to 0070.dbus.
* Thu Oct 02 2008 - ghee.teo@sun.com
- Add /etc/X11/xinit/xinitrc.d/0005.dbus to fix 6755007 so that gdm can launch
  dbus session for the user. This can be used for both gdm on nevada and
  OpenSolaris.
* Sun Sep 14 2008 - brian.cameron@sun.com
- Add new copyright files.
* Tue Sep 02 2008 - brian.cameron@sun.com
- Place the library in a separate package, so that people who just
  want to write their own D-Bus services don't need to depend on the
  daemon.
* Wed Aug 20 2008 - brian.cameron@sun.com
- Move dbus-daemon.3 manpage to dbus-daemon.1 manpage.
* Thu Mar 27 2008 - brian.cameron@sun.com
- Add SUNW_Copyright.
* Wed Mar 19 2008 - brian.cameron@sun.com
- Remove the symlinks that point from /usr/lib/libdbus-1.so.2 to
  /usr/lib/libdbus-1.so.3.  Now that ON updated their build machines to use the
  new D-Bus library, the symlinks are no longer needed.
* Fri Jan 11 2008 - damien.carbery@sun.com
- Fix amd64/sparcv9 symlink to point to libdbus-1.so.3 (2nd half of Brian's
  change on Aug 6. Fixes 6624762.
* Tue Nov 20 2007 - brian.cameron@sun.com
- Add dbus manpages.
* Mon Oct  8 2007 - damien.carbery@sun.com
- Remove %{_libdir}/dbus-1 line from base package as it only contains a header
  file and is duplicated in the devel package. Fixes 6613798.
* Mon Oct  1 2007 - laca@sun.com
- change 64-bit libexecdir to /usr/lib
* Mon Oct  1 2007 - damien.carbery@sun.com
- Fix %files, adding %{_libdir}/%{_arch64}/dbus-1.
* Sun Sep 30 2007 - laca@sun.com
- fix %install
* Fri Sep 28 2007 - laca@sun.com
- convert to new style multi-ISA build
- delete SUNWxwrtl dep
* Mon Aug 06 2007 - brian.cameron@sun.com
- Fix packaging after bumping to 1.1.2.  Also fix the symlink so we
  link to libdbus-1.so.3 rather than libdbus-1.so.3.# so we don't have
  to update the link each time we upgrade the D-Bus library.
* Sun Feb 25 2007 - dougs@truemail.co.th
- updated to include 64-bit build RFE: #6480511
* Fri Dec 15 2006 - damien.carbery@sun.com
- Create symlink to support hal which was built with an older version of dbus.
* Mon Nov 27 2006 - brian.cameron@sun.com
- Update to 1.0.1.
* Fri Nov 24 2006 - damien.carbery@sun.com
- Update %files - remove python dir, add %{_localstatedir}/lib/dbus.
* Mon Sep 18 2006 - laca@sun.com
- revert to normal optimisation flags, the build problems were caused by
  ld(1) bug 6467925
- change /var/run/dbus permissions to root:root, fixes 6460949
* Mon Aug 28 2006 - damien.carbery@sun.com
- Use '-xO2' optimization (not -xO4) as the latter causes seg faults in build.
* Fri Aug 25 2006 - padraig.obriain@sun.com
- Use c99 compiler
* Fri Jul 28 2006 - laca@sun.com
- add pre and post scripts for enabling the dbus svc upon installation
  but leaving it as is upon upgrade (Artem Kachitchkine, David Bustos)
* Fri Jul 21 2006 - laca@sun.com
- Add dbus RBAC entries to auth_attr and prof_attr
* Mon May 08 2006 - damien.carbery@sun.com
- Add Build/Requires dependency on SUNWPython-extra (for Pyrex) so that python
  bindings are built.
* Tue May 02 2006 - laca@sun.com
- add SMF support (from Artem Kachitchkine)
* Fri Feb 17 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Tue Oct 25 2005 - damien.carbery@sun.com
- Add the include dir under _libdir.
* Fri Oct 21 2005 - damien.carbery@sun.com
- Initial spec file created.

