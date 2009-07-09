#
# spec file for package dbus
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: yippi
# bugdb: bugzilla.freedesktop.org
#
Name:         dbus
License:      GPL v2, AFL v2.1
Group:        System/Libraries
Version:      1.2.12
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Simple IPC library based on messages
Source:       http://dbus.freedesktop.org/releases/dbus/%{name}-%{version}.tar.gz
URL:          http://www.freedesktop.org/wiki/Software_2fdbus
#owner:yippi date:2007-09-06 type:feature 
# System services are disabled in default Solaris configuration since they are
# not yet supported on Solaris.
Patch1:       dbus-01-nosystemservice.diff
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
Autoreqprov:  on
Prereq:       /sbin/ldconfig

%define glib2_version 2.6.4
%define libxml2_version 2.6.19
BuildRequires: glib2-devel >= %glib2_version
BuildRequires: libxml2-devel >= %libxml2_version
# FIXME: get python rpm: BuildRequires: python >= %python_version
Requires: glib2 >= %glib2_version
Requires: libxml2 >= %libxml2_version

%description
D-Bus is a message bus system, a simple way for applications to talk to one
another.
D-Bus supplies both a system daemon (for events such as "new hardware device 
added" or "printer queue changed") and a per-user-login-session daemon (for 
general IPC needs among user applications). Also, the message bus is built on
top of a general one-to-one message passing framework, which can be used by
any two apps to communicate directly (without going through the message bus
daemon). 

%package devel
Summary:      Simple IPC library based on messages
Group:        Development/Libraries
Requires:     %{name} = %{version}

%description devel
D-Bus is a message bus system, a simple way for applications to talk to one 
another.

D-Bus supplies both a system daemon (for events such as "new hardware device
added" or "printer queue changed") and a per-user-login-session daemon (for
general IPC needs among user applications). Also, the message bus is built on
top of a general one-to-one message passing framework, which can be used by
any two apps to communicate directly (without going through the message bus
daemon). 

%prep
%setup -q
%patch1 -p1

%build
%ifos linux
if [ -x /usr/bin/getconf ]; then
  CPUS=`getconf _NPROCESSORS_ONLN`
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f
autoconf
export CFLAGS="%optflags -D_REENTRANT"
export LDFLAGS="%_ldflags"
export PKG_CONFIG_PATH="%{_libdir}/pkgconfig"
./configure --prefix=%{_prefix}				\
            --includedir=%{_includedir} 		\
            --sysconfdir=%{_sysconfdir} 		\
            --libdir=%{_libdir}		 		\
            --libexecdir=%{_libexecdir}			\
            --bindir=%{_bindir}				\
            --localstatedir=%{_localstatedir}		\
            --with-dbus-user=root       		\
            --with-dbus-daemondir=%{_basedir}/lib	\
	    --mandir=%{_mandir}				\
	    --datadir=%{_datadir}			\
	    --disable-static
make -j $CPUS \
    pyexecdir=%{_libdir}/python%{python_version}/vendor-packages
cd ../%{name}-%{version}

%install
make DESTDIR=$RPM_BUILD_ROOT install \
    pyexecdir=%{_libdir}/python%{python_version}/vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_datadir}/dbus-1/services
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.pyo" -exec rm -f {} ';'
# Disable system services.
rm $RPM_BUILD_ROOT%{_libexecdir}/dbus-daemon-launch-helper

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean 
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-, root, root)
%config %{_sysconfdir}/dbus-1/session.conf
%config %{_sysconfdir}/dbus-1/system.conf
%{_bindir}/*
%{_libdir}/libdbus*.so*
%{_datadir}/man/*
%{_datadir}/dbus-1/*

%files devel
%defattr(-, root, root)
%{_libdir}/*.so
%{_includedir}/dbus-1.0/*
%{_libdir}/dbus-1.0/*
%{_libdir}/pkgconfig/*
%{_libdir}/python?.?/vendor-packages/*

%changelog
* Thu Jan 08 2009 - brian.cameron@sun.com
- Bump to 1.2.12.
* Wed Dec 10 2008 - brian.cameron@sun.com
- Bump to 1.2.8
* Mon Dec 08 2008 - dave.lin@sun.com
- Bump to 1.2.6.
* Thu Oct 09 2008 - brian.cameron@sun.com
- Bump to 1.2.4. 
  D-Bus if it fails to connect the first time.
* Thu Aug 07 2008 - brian.cameron@sun.com
- Bump to 1.2.3.  Remove upstream dbus-02-getauditsessiondata.diff patch.
* Wed May 07 2008 - simon.zheng@sun.com
- Add patch 02-getauditsessiondata.diff to add a interface 
  "GetAdtAuditSessionData", getting audit data from socket connection.
* Sun Apr 06 2008 - brian.cameron@sun.com
- Bump to 1.2.1
* Wed Feb 27 2008 - brian.cameron@sun.com
- Bump to 1.1.20
* Thu Jan 17 2008 - brian.cameron@sun.com
- Bump to 1.1.4.
* Thu Jan 17 2008 - brian.cameron@sun.com
- Bump to 1.1.3.  Remove upstream patches.
* Wed Nov 07 2007 - padraig.obriain@sun.com
- Add -D_REENTRANT to CFLAGS. It was removed from SUNW spec file on Sep 28.
  See bugster 6615221.
* Fri Oct 12 1007 - laca@sun.com
- delete some env variable settings forgotten in the previous commit
* Fri Sep 28 2007 - laca@sun.com
- convert to new style multi-ISA build
* Thu Sep 06 2007 - brian.cameron@sun.com
- Add patch dbus-04-nosystemservice.diff and do not ship
  dbus-daemon-launch-helper to disable D-Bus system services completely.
  Nothing in Solaris currently needs the D-Bus system service.  The Linux
  solution specifies that --with-dbus-user is "messagebus".  The idea is
  that the system daemon runs as this user and uses the root setgid 
  script dbus-daemon-launch-helper to gain privilege when needed.  It is
  likely that Sun would instead want to use a more secure least-privilege
  RBAC style solution for doing this, if we ever need to add this feature
  back.
* Mon Aug 06 2007 - brian.cameron@sun.com
- Bump to 0.74.  Update patches.
* Fri Jun 08 2007 - brian.cameron@sun.com
- Remove dbus-01-dbus-launch.diff since it is no longer needed now
  that we've reworked the SUNWdtlogin-integration package to call
  dbus-launch from /usr/dt/config/Xsession.jds instead of Xinitrc.jds.
* Sun Apr  1 2007 - laca@sun.com
- add missing aclocal calls
* Wed Mar 15 2007 - dougs@truemail.co.th
- Removed CC64 and CC32. They are not needed anymore
* Sun Feb 25 2007 - dougs@truemail.co.th
- updated to include 64-bit build RFE: #6480511
- patch to stop Sun Studio compiling GCC asm specific code
* Wed Dec 13 2006 - damien.carbery@sun.com
- Bump to 1.0.2.
* Thu Nov 27 2006 - brian.cameron@sun.com
- Minor cleanup.  Remove python build dependancy since now python bindings
  are built in separate module.
* Thu Nov 23 2006 - damien.carbery@sun.com
- Removed upstream patches, 01, 02, 04, 05 and 06. Renumber remainder.
* Wed Nov 22 2006 - damien.carbery@sun.com
- Bump to 1.0.1.
* Fri Nov 17 2006 - ghee.teo@sun.com
- Added patch dbus-06-proxy-change-owner-crash.diff. This patch is only
  for 0.6x release of dbus, when dbus 1.0 is incorporated, this patch
  can be dropped.
* Fri Oct 13 2006 - damien.carbery@sun.com
- Delete .a and .la files.
* Wed Aug 30 2006 - damien.carbery@sun.com
- Add --datadir to configure call so that path in session.conf is expanded.
* Thu Aug 03 2006 - padraig.obriain@sun.com
- Updated dbus-03-dbus-launch.diff to avoid chewing idle CPU.
* Wed Aug 02 2006 - brian.cameron@sun.com
- Rewrote libexec patch based on Havoc's comments.  Now pass in 
  --with-daemondir to set daemon location.
* Fri Jul 28 2006 - laca@sun.com
- add patch priv.spec (from Artem Kachitchkine), makes dbus run as user
  'daemon' and also with least privileges
* Fri Jul 21 2006 - brian.cameron@sun.com
- Add patch to move dbus-daemon to /usr/lib, required by ARC.
* Tue May 02 2006 - laca@sun.com
- add patch console.diff that allows D-Bus to authenticate console user
* Sun Feb 26 2006 - laca@sun.com
- Bump to 0.61.
- move python stuff to vendor-packages, remove .pyo and *.la
* Thu Jan 19 2006 - damien.carbery@sun.com
- Remove upstream patch, 01-auth-external. Renumber remaining.
* Tue Jan 17 2006 - damien.carbery@sun.com
- Bump to 0.60.
* Tue Oct 25 2005 - damien.carbery@sun.com
- Remove patch3 as an include dir under _libdir is okay. Bump to 0.50. Disable
  python bindings as they fail. Bug 4878 files at freedesktop.org.
* Fri Oct 21 2005 - damien.carbery@sun.com
- Add patches to build on Solaris.
* Tue Aug 30 2005 - glynn.foster@sun.com
- Create the dbus-1 services directory
* Tue Aug 16 2005 - damien.carbery@sun.com
- Add python >= 2.4 dependency. Reformat description text.
* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 0.35.2.
* Mon Jun 20 2005 - matt.keenan@sun.com
- dbus 0.23 is actually shipped with gnome 2.10 so bumping down tarball
* Thu Jun 09 2005 - laca@sun.com
- add buildrequires glib2, libxml2
* Thu May 12 2005 - glynn.foster@sun.com
- Initial spec file for dbus.
