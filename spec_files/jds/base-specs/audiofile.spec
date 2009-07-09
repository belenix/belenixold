#
# spec file for package audiofile
#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: yippi
#
Name:         audiofile
License:      LGPL v2, GPLv2, MIT, Sun Public Domain
Group:        System/Library/GNOME
Version:      0.2.6
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      audiofile - 
Source:       http://www.68k.org/~michael/audiofile/audiofile-%{version}.tar.gz
# Note - I sent this patch to the maintainer and he agreed to accept it
# into their next build.  There is no bug tracking system for this module.
#owner:yippi date:2004-02-25 type:feature
Patch1:       audiofile-01-uninstalled.pc.diff
URL:          http://www.68k.org/~michael/audiofile/
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/%{name}
Autoreqprov:  on
Requires:     audiofile

%description
The Audio File Library provides a uniform and elegant API for accessing
a variety of audio file formats, such as AIFF/AIFF-C, WAVE, NeXT/Sun
.snd/.au, Berkeley/IRCAM/CARL Sound File, Audio Visual Research, Amiga
IFF/8SVX, and NIST SPHERE. Supported compression formats are currently
G.711 mu-law and A-law and IMA and MS ADPCM.

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

libtoolize --force
aclocal
autoconf
automake -a -c -f
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix}				\
            --libdir=%{_libdir}                         \
            --bindir=%{_bindir}                         \
	    --sysconfdir=%{_sysconfdir} 		\
            --with-esd-dir=%{_libexecdir}		\
            --libexecdir=%{_libexecdir}                 \
	    --mandir=%{_mandir}
make -j$CPUS


%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, root)
%{_libdir}/*
%{_bindir}/*

%changelog
* Wed Apr  4 2007 - laca@sun.com
- convert to new style 64-bit build
* Wed Mar 15 2007 - dougs@truemail.co.th
- Removed adding ccdir to PATH
* Wed Feb 28 2007 - laca@sun.com
- update patch to use an uninstalled pkg-config .pc file instead of
  an uninstalled audiofile-config file, because the new esound only
  uses the .pc files
* Sun Feb 18 2007 - laca@sun.com
- create (split from SUNWgnome-audio.spec)
