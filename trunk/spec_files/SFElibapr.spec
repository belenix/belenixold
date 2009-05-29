#
# spec file for package SFElibapr
#
#
%include Solaris.inc
%include usr-gnu.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

Name:			SFElibapr
License:		Apache,LGPL,BSD
Group:			system/dscm
Version:		1.3.3
Summary:		Apache Portable Runtime
Source:			http://apache.ziply.com/apr/apr-%{version}.tar.gz
Patch1:                 apr-01-voidp_sizeof.diff

URL:			http://apr.apache.org/
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:		%{_prefix}
Requires: SFEgawk

%description
Apache Portable Runtime (APR) provides software libraries
that provide a predictable and consistent interface to
underlying platform-specific implementations.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
Requires:                SUNWhea

%prep
%setup -q -c -n %name-%version
%ifarch amd64 sparcv9
cp -pr apr-%{version} apr-%{version}-64
%endif

%build

%ifarch amd64 sparcv9
cd apr-%{version}-64
export PATH=/usr/ccs/bin:/usr/gnu/bin:/usr/bin:/usr/sbin:/bin:/usr/sfw/bin:/opt/SUNWspro/bin:/opt/jdsbld/bin
export CFLAGS="%optflags64 -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"
export LD=/usr/ccs/bin/ld
export LDFLAGS="%_ldflags64 -L/lib/%{_arch64} -R/lib/%{_arch64} -L$RPM_BUILD_ROOT%{_libdir}"
./configure \
    --prefix=%{_prefix} \
    --sysconfdir=%{_sysconfdir} \
    --libdir=%{_libdir}/%{_arch64} \
    --disable-static \
    --with-pic \
    --with-installbuilddir=%{_datadir}/apr/build \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --enable-threads

make
cd ..
%endif

cd apr-%{version}
export PATH=/usr/ccs/bin:/usr/gnu/bin:/usr/bin:/usr/sbin:/bin:/usr/sfw/bin:/opt/SUNWspro/bin:/opt/jdsbld/bin
export CFLAGS="%optflags -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"
export LD=/usr/ccs/bin/ld
export LDFLAGS="%_ldflags -L/lib -R/lib -L$RPM_BUILD_ROOT%{_libdir}"
./configure \
    --prefix=%{_prefix} \
    --sysconfdir=%{_sysconfdir} \
    --libdir=%{_libdir} \
    --disable-static \
    --with-pic \
    --with-installbuilddir=%{_datadir}/apr/build \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --enable-threads
 
%patch1 -p1

make

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
cd apr-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/lib*a
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/*.exp
rm -rf $RPM_BUILD_ROOT%{_datadir}
rm -rf $RPM_BUILD_ROOT%{_includedir}
mkdir -p $RPM_BUILD_ROOT%{_bindir}/%{_arch64}
mv $RPM_BUILD_ROOT%{_bindir}/apr-1-config $RPM_BUILD_ROOT%{_bindir}/%{_arch64}
cd ..
%endif

cd apr-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_infodir}

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.exp

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/apr-1-config
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/apr/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/apr-1-config
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Fri May 29 2009 - Moinak Ghosh <moinakg@belenix(dot)org>
- Add patch for building with Gcc 4.4.
- Add lib paths to properly detect some libs.
* Tue Feb 10 2009 - moinakg@gmail.com
- Bump version to 1.3.3.
- Add 64Bit build.
* Tue Jan 22 2008 - moinak.ghosh@sun.com
- Initial spec.
