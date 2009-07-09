#
# spec file for package opal
#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: elaine
#
Name:         opal
License:      MPL
Group:        System/Libraries
Version:      3.4.2
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      OPAL - Open Phone Abstraction Library
Source:       http://www.ekiga.org/admin/downloads/latest/sources/ekiga_3.0.1/%{name}-%{version}.tar.gz

# owner:davelam date:2006-04-14 type:branding
# change library naming rule to fit unix style
Patch1:       opal-01-libname.diff

# owner:elaine date:2008-11-11 type:branding
# help ekiga find opal.pc
Patch2:       opal-02-no-public-pc.diff

# owner:hawklu date:2006-05-15 type:bug
# bugster:6416969
# updated by elaine
Patch3:       opal-03-jitter.diff

# owner:elaine date:2008-11-11 type:bug
# bugzilla:560478
Patch5:       opal-05-option-err.diff

Patch6:       opal-06-gcc-opt.diff

URL:          http://www.ekiga.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/%{name}
Autoreqprov:  on
Requires:     speex
Requires:     ptlib

%description
OPAL is an Open Source class library for the development of
applications that use SIP / H.323 protocols for multimedia
communications over packet based networks.

%package devel
Summary: Headers for developing programs that will use opal
Group:      Development/Libraries
Requires:   %{name}

%description   devel
This package contains the headers that programmers will need to develop
applications which will use opal.

%prep
%setup -q -n %{name}-%{version}
#%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch5 -p1
%patch6 -p1

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

export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags"
%{?ekiga_libdir:export LDFLAGS="$LDFLAGS -R%{ekiga_libdir}"}

cd plugins
aclocal
autoconf
cd ..
aclocal
autoconf
./configure \
	--prefix=%{_prefix} \
        --libdir=%{?ekiga_libdir}%{?!ekiga_libdir:%{_libdir}} \
        --bindir=%{_bindir} \
	--sysconfdir=%{_sysconfdir} \
	--mandir=%{_mandir} \
	--disable-iax
make -j $CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr (-, root, root)
%{ekiga_libdir}/*.so.*

%files devel
%defattr(-, root, root)
%{ekiga_libdir}/*.so

%changelog
* Thu Nov 20 2008 - elaine.xiong@sun.com
- Bump to 3.4.2. Remove upstreamed opal-04-endian patch.
* Fri Nov 14 2008 - elaine.xiong@sun.com
- Bump to 3.4.1. Add new patches and remove obsolete patches.
- Update build options for new version.
* Wed Sep 03 2008 - elaine.xiong@sun.com
- Add note to not bump to 3.3.1 as ekiga depends on it.
* Sun Dec 23 2007 - patrick.ale@gmail.com
- Download tar.gz instead of tar.bz2. bz2 tarball is N/A
* Fri Nov 02 2007 - elaine.xiong@sun.com
- Fix a typo.
* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 2.2.11.
* Thu May 17 2007 - elaine.xiong@sun.com
- Disable IAX feature support per OPAL ECCN requirement.
* Wed Apr 25 2007 - elaine.xiong@sun.com
- Update owner name for opal-04-pack-addr.diff
* Thu Apr 19 2007 - elaine.xiong@sun.com
- Bump to 2.2.8, move upstream patch opal-02-illegal-payloadtype.diff.
* Tue Apr 17 2007 - elaine.xiong@sun.com
- move the -Lpath that could specify the /usr/lib/ as the search directory
  when link time.
* Fri Apr  6 2007 - elaine.xiong@sun.com
- Add patch opal-04-pack-addr.diff to fix bugster6538068
  Actually it works for pwlib-05-medialib.diff. It makes the YUV420P payload
  buffer packed by 8 Byte. If pwlib-05-media.diff is upstream, it should be
  upstream. If not, the performance brougnt by medialib is hurt.
* Thu Apr  5 2007 - laca@sun.com
- Create
