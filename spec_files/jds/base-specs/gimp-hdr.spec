#
# spec file for package gimp-hdr
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: bewitche
#
Name:    gimp-hdrtools
Summary: GIMP high dynamic range image plugin
Version: 0.1
Release: 1
License: GPL
Group:   System/GUI/GNOME
Source:  http://nifelheim.dyndns.org/~cocidius/files/gimp-hdrtools-%{version}.tar.bz2
URL:     http://nifelheim.dyndns.org/~cocidius/hdrtools/
# date:2008-07-18 owner:bewitche type:branding
Patch1:       gimp-hdr-01-compile.diff
# date:2008-08-28 owner:fujiwara type:feature
Patch2:       gimp-hdr-02-textdomain.diff
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description

%prep
%setup -q
%patch1 -p1
%patch2 -p1

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

make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, root)

%changelog
* Thu Aug 28 2008 - takao.fujiwara@sun.com
- Added gimp-hdrtools-02-textdomain.diff to seprate the domain from gimp.

* Mon Jul 21 2008 - damien.carbery@sun.com
- Correct source URL.

* Thu Jul 17 2008 - chris.wang@sun.com
- Initial build.


