#
# spec file for package flac
#
# Copyright (c) 2003 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: yippi
# bugdb: http://sourceforge.net/tracker/index.php?func=detail&group_id=13478&atid=313478&aid=
#
Name:         flac
License:      Xiph.org BSD-style, GPL v2, LGPL v2.1, FDL v1.2
Group:        Application/Devel
Version:      1.2.1
Release:      3
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      An Open Source Lossless Audio Codec
Source:       http://downloads.us.xiph.org/releases/%{name}/%{name}-%{version}.tar.gz
#owner:yippi date:2005-08-12 type:bug bugid:1701960
%if %cc_is_gcc
%else
Patch1:       flac-01-forte.diff
%endif
#owner:mattman date:2009-02-26 type:branding
Patch2:       flac-02-manpages.diff
URL:          http://flac.sourceforge.net/
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_docdir}/%{name}
Autoreqprov:  on
Prereq:       /sbin/ldconfig

%description
FLAC stands for Free Lossless Audio Codec. Grossly oversimplified, 
FLAC is similar to MP3, but lossless, meaning that audio is compressed 
in FLAC without any loss in quality. This is similar to how Zip works, 
except with FLAC you will get much better compression because it is 
designed specifically for audio, and you can play back compressed FLAC 
files in your favorite player (or your car or home stereo, see supported 
devices) just like you would an MP3 file.

%package devel
Summary:	flac development files
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
flac development files.

%prep
%setup -q
perl -pi -e 's/^M$//' src/share/replaygain_analysis/replaygain_analysis.c
%ifos solaris
%if %cc_is_gcc
%else
%patch1 -p1
%endif
%endif
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

export CFLAGS="%{optflags}"
export CXXFLAGS="%{?cxx_optflags}"
export LDFLAGS="%{?_ldflags}"
#aclocal $ACLOCAL_FLAGS -I ./m4
#libtoolize --force --copy
#autoheader
#automake -a -c -f
#autoconf
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --libdir=%{_libdir}		\
            --sysconfdir=%{_sysconfdir} \
            --disable-xmms-plugin	\
	    --disable-cpplibs		\
            --enable-sse		\
            --mandir=%{_mandir}

make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install

#Clean up unpackaged files
rm $RPM_BUILD_ROOT%{_libdir}/*.a
rm $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_datadir}/doc/*
%{_datadir}/man/man1/flac*
%{_datadir}/man/man1/metaflac*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/libFLAC.so*
%attr(755,root,root) %{_libdir}/libFLAC++.so*
%attr(755,root,root) %{_libdir}/libOggFLAC.so*
%attr(755,root,root) %{_libdir}/libOggFLAC++.so*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_datadir}/aclocal/*.m4

%changelog
* Thu Feb 26 2009 - matt.keenan@sun.com
- Add manpages patch for Attributes and ARC Comment
* Thu Feb 19 2009 - brian.cameron@sun.com
- Remove patch flac-02-map.diff.  Got feedback from the person who submitted
  the bug that this didn't resolve the issue.
* Wed Feb 18 2009 - brian.cameron@sun.com
- Add patch flac-02-map.diff and add "-Wl,-Mmap.remove_all to LDFLAGS, so that
  FLAC builds without HWCAP enabled.  This fixes bug #6653080.
* Fri Mar 14 2008 - irene.huang@sun.com
- change --disable-cplusplus to --disable-cpplibs
* Mon Nov 05 2007 - brian.cameron@sun.com
- Fix Source URL.
* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 1.2.1. Change --disable-cpp option to --disable-cplusplus as
  configure.in has been changed. Remove upstream patches 02-c++ and
  03-ogg-build-fix.
* Thu Aug 02 2007 - damien.carbery@sun.com
- Add upstream patch, 03-ogg-build-fix, to fix build error.
* Tue Jul 31 2007 - brian.cameron@sun.com
- Bump to 1.2.0.
* Fri Jun 29 2007 - irene.huang@sun.com
- add patch 02-c++.diff, add configuration option --disable-cpp
* Tue Apr 17 2007 - brian.cameron@sun.com
- Add autoheader call since the patch now modifies configure.ac and
  adds FLAC_INLINE.
* Thu Mar 15 2007 - laca@sun.com
- add some configure options and set environment variables to support
  building the same spec for multiple ISAs
* Thu Feb 15 2006 - damien.carbery@sun.com
- Bump to 1.1.4.
* Thu Nov 30 2006 - damien.carbery@sun.com
- Bump to 1.1.3.
* Fri Aug 12 2005 - balamurali.viswanathan@wipro.com
- Add patch flac-01-forte.diff
* Tue Aug 02 2005 - balamurali.viswanathan@wipro.com
- Initial spec file checkin
