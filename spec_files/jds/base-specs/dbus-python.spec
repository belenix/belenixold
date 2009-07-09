#
# spec file for package dbus-python
#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: yippi
# bugdb: bugzilla.freedesktop.org
#
%{?!pythonver:%define pythonver 2.4}

Name:         dbus-python
License:      MIT
Group:        System/Libraries
Version:      0.83.0
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Python bindings for D-Bus
Source:       http://dbus.freedesktop.org/releases/dbus-python/%{name}-%{version}.tar.gz
URL:          http://www.freedesktop.org/wiki/Software_2fdbus
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
Autoreqprov:  on
Prereq:       /sbin/ldconfig

%define python_version 2.4
BuildRequires: glib2-devel >= %glib2_version
BuildRequires: libxml2-devel >= %libxml2_version
BuildRequires: python-devel >= %{pythonver}
Requires: glib2 >= %glib2_version
Requires: libxml2 >= %libxml2_version
Requires: python >= %{pythonver}

%description
Python bindings for D-Bus.

%package devel
Summary:      Simple IPC library based on messages
Group:        Development/Libraries
Requires:     %{name} = %{version}

%description devel
Python bindings for D-Bus.

%prep
%setup -q

%build
export PYTHON=/usr/bin/python%{pythonver}
export PYTHON_VERSION=%{pythonver}
aclocal $ACLOCAL_FLAGS -I ./m4
autoconf
automake -a -c -f
export CFLAGS="%optflags -D_REENTRANT"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix}			\
            --includedir=%{_includedir}		\
            --sysconfdir=%{_sysconfdir}		\
            --libdir=%{_libdir}			\
            --bindir=%{_bindir}			\
            --localstatedir=%{_localstatedir}	\
            --with-dbus-user=root		\
            --with-dbus-daemondir=%{_basedir}/lib \
            --mandir=%{_mandir}			\
            --datadir=%{_datadir}		\
            --disable-static
make

%install
make install DESTDIR=$RPM_BUILD_ROOT

# move to vendor-packages
PYLIBDIR=$RPM_BUILD_ROOT%{_libdir}/python%{pythonver}
[ ! -d ${PYLIBDIR}/vendor-packages ] && mkdir -p ${PYLIBDIR}/vendor-packages
(
    cd ${PYLIBDIR}/site-packages
    find . -print | cpio -pdm ${PYLIBDIR}/vendor-packages
)
rm -rf ${PYLIBDIR}/site-packages


find $RPM_BUILD_ROOT%{_prefix} -type f -name "*.la" -exec rm {} ';'
find $RPM_BUILD_ROOT%{_prefix} -type f -name "*.a" -exec rm {} ';'

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
* Thu Mar 19 2009 - brian.cameron@sun.com
- Remove patch dbus-python-01-fix-wrong-python25-includes.diff and instead
  set PYTHON_VERSION, which also ensures that the right python includes are
  used.
* Thu Mar 05 2009 - brian.cameron@sun.com
- Made it possible to build both Python 2.4 and 2.6 bindings.
* Mon Aug 15 2008 - patrick.ale@gmail.com
- Remove method to find python headers by means of python-config from
  configure (Patch1) and add -I/usr/python2.4 to CFLAGS.
* Thu Jul 24 2008 - brian.cameron@sun.com
- bump to 0.83.0.
* Mon Dec 10 2007 - brian.cameron@sun.com
- Bump to 0.82.4.
* Wed Nov 07 2007 - padraig.obriain@sun.com
- Add -D_REENTRANT to CFLAGS. It was removed from SUNW spec file on Sep 28.
  See bugster 6615221
* Wed Oct 10 2007 - damien.carbery@sun.com
- Don't delete *.pyc files - they are needed.
* Fri Sep 28 2007 - laca@sun.com
- convert to new style multi-ISA build
* Mon Aug 06 2007 - brian.cameron@sun.com
- Bump to 0.82.2 add "-I ./m4" to aclocal calls.
* Sun Apr  1 2007 - laca@sun.com
- add missing aclocal calls
* Wed Mar 15 2007 - dougs@truemail.co.th
- Removed CC64 and CC32. They are not needed anymore
* Sat Feb 25 2007 - dougs@truemail.co.th
- updated to include 64-bit build RFE: #6480511
* Wed Feb 14 2007 - damien.carbery@sun.com
- Bump to 0.80.2.
* Thu Jan 25 2007 - damien.carbery@sun.com
- Bump to 0.80.1. Use configure/make to build, not setup.py.
* Thu Nov 27 2006 - brian.cameron@sun.com
- Created.
