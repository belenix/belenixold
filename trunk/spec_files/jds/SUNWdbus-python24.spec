#
# spec file for package SUNWdbus-python24
#
# includes module(s): dbus-python
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: yippi
# bugdb: bugzilla.freedesktop.org
#
%include Solaris.inc

%define pythonver 2.4

%include base.inc
%use dbus_python = dbus-python.spec

Name:                    SUNWdbus-python24
Summary:                 D-Bus Python %{pythonver} bindings
Version:                 %{dbus_python.version}
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:	SUNWdbus
Requires:	SUNWgnome-base-libs
Requires:	SUNWlxml
Requires:       SUNWlexpt
Requires:       SUNWPython-extra
Requires:       SUNWdbus-glib
BuildRequires:	SUNWdbus-devel
BuildRequires:	SUNWgnome-base-libs-devel
BuildRequires:	SUNWlxml
BuildRequires:  SUNWsfwhea
BuildRequires:  SUNWPython-extra
BuildRequires:  SUNWpython-setuptools
BuildRequires:  SUNWdbus-glib-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:       SUNWgnome-base-libs
# the 2.6 devel package is required because it contains the headers
# (they are not duplicated in this package, since they would be identical)
Requires: SUNWdbus-python26-devel

%prep
rm -rf %name-%version
mkdir %name-%version
%dbus_python.prep -d %name-%version

%build
PKG_CONFIG_DISABLE_UNINSTALLED=
unset PKG_CONFIG_DISABLE_UNINSTALLED
export PYTHON=/usr/bin/python%{pythonver}
%dbus_python.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%dbus_python.install -d %name-%version

# included in SUNWgst-python26-devel
rm -r $RPM_BUILD_ROOT%{_includedir}
rm -r $RPM_BUILD_ROOT%{_datadir}/doc/dbus-python

# move to subdir to avoid conflict with python 2.6
mv $RPM_BUILD_ROOT%{_libdir}/pkgconfig \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{pythonver}/vendor-packages
%dir %attr (0755, root, sys) %{_datadir}
%doc -d dbus-python-%{dbus_python.version} AUTHORS
%doc -d dbus-python-%{dbus_python.version} README
%doc(bzip2) -d dbus-python-%{dbus_python.version} COPYING
%doc(bzip2) -d dbus-python-%{dbus_python.version} ChangeLog
%doc(bzip2) -d dbus-python-%{dbus_python.version} NEWS
%dir %attr (0755, root, other) %{_datadir}/doc

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/python%{pythonver}/pkgconfig
%{_libdir}/python%{pythonver}/pkgconfig/*

%changelog
* Tue Mar 10 2009 - brian.cameron@sun.com
- Cleanup based on code review.
* Thu Mar 05 2009 - brian.cameron@sun.com
- Split from SUNWdbus-bindings.spec.  Remove 64 bit support as it is not
  needed for the python bindings.
* Wed Mar 04 2009 - dave.lin@sun.com
- Add /usr/share/man/man1 in %files
* Sun Sep 14 2008 - brian.cameron@sun.com
- Add new copyright files.
* Thu Mar 27 2008 - brian.cameron@sun.com
- Add SUNW_Copyright
* Tue Nov 20 2007 - brian.cameron@sun.com
- Add libdbus-glib-1.3 manpage.
* Fri Sep 28 2007 - laca@sun.com
- convert to new style multi-ISA build
- delete SUNWxwrtl dep
* Sat Feb 25 2007 - dougs@truemail.co.th
- updated to include 64-bit build RFE: #6480511
* Fri Jan 26 2007 - damien.carbery@sun.com
- Set PKG_CONFIG vars in %build because dbus-python use autofoo/configure/make
  process rather than setup.py.
* Thu Jan 25 2007 - damien.carbery@sun.com
- Add %{_datadir}/doc to devel pkg, because of new dbus-python tarball.
* Thu Dec 21 2006 - brian.cameron@sun.com
- Remove references to SUNWdbus-bindings-root since we do not
  build this package.
* Thu Sep 21 2006 - brian.cameron@sun.com
- Created.

