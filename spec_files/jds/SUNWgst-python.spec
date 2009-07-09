#
# spec file for package SUNWgst-python
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: yippi
#
%include Solaris.inc

%define pythonver 2.4
%use gstp = gst-python.spec

Name:                    SUNWgst-python
Summary:                 Python %{pythonver} bindings for the GStreamer streaming media framework
URL:                     %{gstp.url}
Version:                 %{gstp.version}
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:                SUNWPython
Requires:                SUNWgnome-python-libs
Requires:                SUNWgnome-media
BuildRequires:           SUNWgnome-python-libs-devel
BuildRequires:           SUNWgnome-media-devel
BuildRequires:           SUNWpython-setuptools

%package devel		
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
# the 2.6 devel package is required because it contains the headers
# (they are not duplicated in this package, since they would be identical)
Requires: SUNWgst-python26-devel

%prep
rm -rf %name-%version
mkdir -p %name-%version
%gstp.prep -d %name-%version

%build
export PYTHON=/usr/bin/python%{pythonver}
export PKG_CONFIG_PATH=/usr/lib/python%{pythonver}/pkgconfig
%gstp.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%gstp.install -d %name-%version

# included in SUNWgst-python25-devel
rm -r $RPM_BUILD_ROOT%{_datadir}/gst-python

# move to subdir to avoid conflict with python 2.5
mv $RPM_BUILD_ROOT%{_libdir}/pkgconfig \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{pythonver}/vendor-packages/gst-0.10/*
%{_libdir}/python%{pythonver}/vendor-packages/pygst.pth
%{_libdir}/python%{pythonver}/vendor-packages/pygst.py
%{_libdir}/python%{pythonver}/vendor-packages/*.so
%doc -d gst-python-%{gstp.version} AUTHORS
%doc -d gst-python-%{gstp.version} README
%doc(bzip2) -d gst-python-%{gstp.version} COPYING
%doc(bzip2) -d gst-python-%{gstp.version} ChangeLog
%doc(bzip2) -d gst-python-%{gstp.version} NEWS
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, sys) %{_datadir}

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/python%{pythonver}/pkgconfig
%{_libdir}/python%{pythonver}/pkgconfig/*

%changelog
* Tue Feb 24 2009 - laca@sun.com
- set PYTHON and PKG_CONFIG_PATH so the correct python version and
  dependencies are picked up
* Mon Nov 24 2008 - laca@sun.com
- update to use base spec file
- add devel pkg
- move pkgconfig files under /usr/lib/python2.4
* Mon Oct 13 2008 - brian.cameron@sun.com
- Bump to 0.10.13.  Remove upstream patch gst-python-01-pipelinetester.diff.
* Fri Sep 12 2008 - matt.keenn@sun.com
- Update copyright
* Wed Jul 16 2008 - damien.carbery@sun.com
- Update %files for newly delivered library.
* Thu Jun 19 2008 - brian.cameron@sun.com
- Bump to 0.10.12.
* Thu Mar 20 2008 - brian.cameron@sun.com
- Bump to 0.10.11.
* Tue Mar 18 2008 - damien.carbery@sun.com
- Add Build/Requires for SUNWgnome-python-libs and SUNWgnome-media.
* Tue Feb 12 2008 - dermot.mccluskey@sun.com
- initial version

