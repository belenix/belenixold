#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

Name:                SFElibmp4v2
Summary:             Library for working with files using the mp4 container format
Version:             1.5.0.1
License:             MPLv1.1
Source:              http://resare.com/libmp4v2/dist/libmp4v2-%{version}.tar.bz2
URL:                 http://resare.com/libmp4v2/
Patch1:              libmp4v2-01-consts.diff

SUNW_BaseDir:        %{_basedir}
#SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%description
The libmp4v2 library provides an abstraction layer for working with files
using the mp4 container format. This library is developed by mpeg4ip project
and is an exact copy of the library distributed in the mpeg4ip package.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%prep
%setup -q -c -n %name-%version
cd libmp4v2-%version
%patch1 -p1
cd ..

%ifarch amd64 sparcv9
cp -rp libmp4v2-%version libmp4v2-%{version}-64
%endif


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

%ifarch amd64 sparcv9
cd libmp4v2-%{version}-64

export CFLAGS="%optflags64"
export CXXFLAGS="%cxx_optflags64"
export CPPFLAGS="-Du_int64_t=uint64_t -Du_int32_t=uint32_t -Du_int16_t=uint16_t -Du_int8_t=uint8_t"
export LDFLAGS="%_ldflags64 %{gnu_lib_path64} -lstdc++"

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir}/%{_arch64} \
            --libdir=%{_libdir}/%{_arch64} \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir} \
            --includedir=%{_includedir} \
            --mandir=%{_mandir} \
            --disable-static \
            --disable-dependency-tracking

cp mp4util.h mp4util.h.orig 
cat mp4util.h.orig | sed 's/#ifndef ASSERT/#define __STRING(x) #x\n#ifndef ASSERT/' > mp4util.h
cp mp4.h mp4.h.orig
cat mp4.h.orig | sed 's/#include <stdio.h>/#include <stdio.h>\n#include <limits.h>/' > mp4.h

gmake -j$CPUS

cd ..
%endif

cd libmp4v2-%{version}
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export CPPFLAGS="-Du_int64_t=uint64_t -Du_int32_t=uint32_t -Du_int16_t=uint16_t -Du_int8_t=uint8_t"
export LDFLAGS="%_ldflags %{gnu_lib_path} -lstdc++"

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --libdir=%{_libdir} \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir} \
            --includedir=%{_includedir} \
            --mandir=%{_mandir} \
            --disable-static \
            --disable-dependency-tracking

cp mp4util.h mp4util.h.orig 
cat mp4util.h.orig | sed 's/#ifndef ASSERT/#define __STRING(x) #x\n#ifndef ASSERT/' > mp4util.h
cp mp4.h mp4.h.orig
cat mp4.h.orig | sed 's/#include <stdio.h>/#include <stdio.h>\n#include <limits.h>/' > mp4.h

gmake -j$CPUS
cd ..


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd libmp4v2-%{version}-64

gmake install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/*.la
cd ..
%endif

cd libmp4v2-%{version}
gmake install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

mkdir -p $RPM_BUILD_ROOT%{_docdir}/libmp4v2-%{version}
cp README TODO INTERNALS API_CHANGES $RPM_BUILD_ROOT%{_docdir}/libmp4v2-%{version}
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
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
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, other) %{_docdir}/libmp4v2-%{version}
%{_docdir}/libmp4v2-%{version}/*

%changelog
* Sat Aug 29 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Initial version.
