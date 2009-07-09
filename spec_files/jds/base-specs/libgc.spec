#
# spec file for package libgc
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jerrytan
#

%define real_name gc

Name:			libgc
License:		BSD
Group:			System/Libraries
Version:		7.1
Release:	 	4
Distribution:		Java Desktop System
Vendor:			Sun Microsystems, Inc.
Summary:		Boehm-Demers-Weiser garbage collector for C/C++
Source:			http://www.hpl.hp.com/personal/Hans_Boehm/gc/gc_source/gc-%{version}.tar.gz
URL:			http://www.hpl.hp.com/personal/Hans_Boehm/gc/
#date:2008-07-31 owner:jerrytan type:branding
Patch1:                 libgc-01-man.diff
#date:2009-02-16 owner:jerrytan type:branding
Patch2:                 libgc-02-rename-libbgc.diff
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
Docdir:			%{_defaultdocdir}/doc
Autoreqprov:		on
Prereq:                 /sbin/ldconfig

%description
Boehm's GC is a garbage collecting storage allocator that is
intended to be used as a plug-in replacement for C's malloc.


%package devel
Summary:		Header files, libraries and development documentation for %{name}
Group:			Development/Libraries
Requires:		%{name} = %{version}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.


%prep
%setup -q -n %{real_name}-%{version}
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

libtoolize --force
aclocal $ACLOCAL_FLAGS
automake -a -c -f
autoconf

CFLAGS="$RPM_OPT_FLAGS"			\
./configure --prefix=%{_prefix}         \
            --mandir=%{_mandir}         \
            --libdir=%{_libdir}         \
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            %gtk_doc_option

make -j $CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/share/man/man3
cp $RPM_BUILD_ROOT/usr/share/gc/gc.man $RPM_BUILD_ROOT/usr/share/man/man3/gc.3
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%doc README.QUICK
%{_libdir}/lib*.so*

%files devel
%defattr(-, root, root)
%doc doc/*
%doc %{_mandir}/man?/*
%{_libdir}/libgc.so
%{_libdir}/libgccpp.so
%{_libdir}/libcord.so
%{_includedir}/gc/
%{_includedir}/libgc/
%{_libdir}/pkgconfig/bdw-gc.pc

%changelog
* Mon Feb 16 2009 - jerry.tan@sun.com
- change libgc.so to libbgc.so to avoid conflict with sunstudio
* Tue May 27 2008 - halton.huo@sun.com
- Bump to 7.1
* Wed Jan 02 2008 - halton.huo@sun.com
- spilit from SFEbdw-gc.spec
