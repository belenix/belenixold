#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

Name:                SFElibasyncns
Summary:             Asynchronous Name Service Library
Version:             0.7
License:             LGPLv2+
Group:               System Environment/Libraries
Source:              http://0pointer.de/lennart/projects/libasyncns/libasyncns-%{version}.tar.gz
URL:                 http://0pointer.de/lennart/projects/libasyncns/

SUNW_BaseDir:        %{_basedir}
#SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%description
A small and lightweight library that implements easy to use asynchronous
wrappers around the libc NSS functions getaddrinfo(), res_query() and related.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%prep
%setup -q -c -n %name-%version

%ifarch amd64 sparcv9
cp -rp libasyncns-%version libasyncns-%{version}-64
%endif


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

%ifarch amd64 sparcv9
cd libasyncns-%{version}-64

export CFLAGS="%optflags64"
#export CPPFLAGS="-Du_int64_t=uint64_t -Du_int32_t=uint32_t -Du_int16_t=uint16_t -Du_int8_t=uint8_t"
export LDFLAGS="%_ldflags64 %{gnu_lib_path64} -lstdc++"

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir}/%{_arch64} \
            --libdir=%{_libdir}/%{_arch64} \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir} \
            --includedir=%{_includedir} \
            --mandir=%{_mandir} \
            --disable-static

gmake -j$CPUS

cd ..
%endif

cd libasyncns-%{version}
export CFLAGS="%optflags"
#export CPPFLAGS="-Du_int64_t=uint64_t -Du_int32_t=uint32_t -Du_int16_t=uint16_t -Du_int8_t=uint8_t"
export LDFLAGS="%_ldflags %{gnu_lib_path} -lstdc++"

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --libdir=%{_libdir} \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir} \
            --includedir=%{_includedir} \
            --mandir=%{_mandir} \
            --disable-static 

gmake -j$CPUS
cd ..


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd libasyncns-%{version}-64

gmake install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/*.la
cd ..
%endif

cd libasyncns-%{version}
gmake install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT \( -name *.a -o -name *.la \) -exec rm {} \;
rm -rf $RPM_BUILD_ROOT%{_datadir}
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*.h
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%changelog
* Sat Aug 29 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Initial version.
