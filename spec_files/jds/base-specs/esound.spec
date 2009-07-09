#
# spec file for package esound
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: yippi
#
Name:         esound
License:      LGPL v2
Group:        System/Library/GNOME
Version:      0.2.40
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      esound - The Enlightened Sound Daemon
Source:       http://ftp.gnome.org/pub/GNOME/sources/esound/0.2/esound-%{version}.tar.bz2
# This patch works with the audiofile-01-uninstalled-config.diff to
# allow esound to be built when audiofile isn't acutally installed on the
# system.
#owner:yippi date:2004-05-07 type:feature
Patch1:       esound-01-esd-config.diff
URL:          http://www.tux.org/~ricdude/overview.html
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/%{name}
Autoreqprov:  on
Requires:     audiofile

%description
The Enlightened Sound Daemon (ESD or EsounD) is the sound server for
Enlightenment and GNOME. It mixes several sound streams into one for output.
It can also manage network-transparent audio.

%prep
%setup -q
%patch1 -p1 -b .orig

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

%if %debug_build
%define debug_opt --enable-debugging
%else
%define debug_opt --disable-debugging
%endif

libtoolize --force
aclocal $ACLOCAL_FLAGS -I .
autoconf
automake -a -c -f
./configure --prefix=%{_prefix}				\
	    --sysconfdir=%{_sysconfdir} 		\
            --with-esd-dir=%{_prefix}/lib		\
            --libdir=%{_libdir}                         \
            --bindir=%{_bindir}                         \
            --libexecdir=%{_prefix}/lib                 \
            --disable-audiofiletest                     \
	    --mandir=%{_mandir} %{debug_opt}
make -j$CPUS


%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, root)
%{_bindir}/*
%{_libdir}/*
%{_sysconfdir}/*

%changelog
* Thu Sep 04 2008 - christian.kelly@sun.com
- Bump to 0.2.40.
* Wed Jul 16 2008 - damien.carbery@sun.com
- Bump to 0.2.39.
* Fri May 04 2007 - damien.carbery@sun.com
- Bump to 0.2.38.
* Wed Apr  4 2007 - laca@sun.com
- convert to new style 64-bit build
* Wed Mar 15 2007 - dougs@truemail.co.th
- Removed adding ccdir to PATH
* Wed Feb 28 2007 - laca@sun.com
- need to run automake because the maintainer's version is incompatible with
  our version of autoconf
* Wed Feb 28 2007 - damien.carbery@sun.com
- Bump to 0.2.37.
* Sun Feb 18 2007 - laca@sun.com
- create (split from SUNWgnome-audio.spec)
