Name:    gmp
Summary: GNU Multiple Presicion Arithmetic Library
Group:   libraries/math
Version: 4.3.2
Release: 2%{?dist}
Source:  http://ftp.gnu.org/pub/gnu/gmp/gmp-%{version}.tar.bz2
Source1: gmp.h
Source2: gmp-mparam.h
URL:     http://swox.com/gmp/
License: LGPLv3+
Group:   System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The gmp package contains GNU MP, a library for arbitrary precision
arithmetic, signed integers operations, rational numbers and floating
point numbers. GNU MP is designed for speed, for both small and very
large operands. GNU MP is fast because it uses fullwords as the basic
arithmetic type, it uses fast algorithms, it carefully optimizes
assembly code for many CPUs' most common inner loops, and it generally
emphasizes speed over simplicity/elegance in its operations.

%package devel
Summary:                 %{summary} - development files
Requires: %name

%description devel
The libraries, header files and documentation for using the GNU MP 
arbitrary precision library in applications.

If you want to develop applications which will use the GNU MP library,
you'll need to install the gmp-devel package.  You'll also need to
install the gmp package.

%prep
%setup -q -c -n %name-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

%if %cc_is_gcc
CFLAGS_GEN="-fno-builtin -finline-functions -std=c99 -D_REENTRANT -D__EXTENSIONS__=1 -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64 -D_XOPEN_SOURCE=600 -D_XPG6 -D_POSIX_PTHREAD_SEMANTICS -D_POSIX_C_SOURCE=200112L -D__XOPEN_OR_POSIX -D_STRICT_STDC -D_STRICT_STDC__ -D_STDC_C99 -D_ISOC99_SOURCE -DNDEBUG -DPIC -fPIC -z combreloc -z redlocsym -z ignore -z rescan -z absexec -s"
export CPPFLAGS="-fexceptions"

#
# Our Gcc wrappers to kick out -lc.
#
cat <<EOT1 > gcc
#!/bin/sh

args=\`echo "\$@" | sed 's/\-lc//g'\`
exec $CC \$args
EOT1

cat <<EOT2 > g++
#!/bin/sh

args=\`echo "\$@" | sed 's/\-lc//g'\`
exec $CXX \$args
EOT2

chmod +x ./gcc ./g++
CC=`pwd`/gcc
CXX=`pwd`/g++
export CC CXX

%else
CFLAGS_GEN="-features=extinl -xbuiltin=%none -xcsi -xinline=%auto -xustr=ascii_utf16_ushort -xalias_level=std -xthreadvar=%all -mt -D_REENTRANT -D__EXTENSIONS__=1 -xF=%none -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64 -D_XOPEN_SOURCE=600 -D_XPG6 -D_POSIX_PTHREAD_SEMANTICS -D_POSIX_C_SOURCE=200112L -D__XOPEN_OR_POSIX -D_STRICT_STDC -D_STRICT_STDC__ -D_STDC_C99 -D_ISOC99_SOURCE -DNDEBUG -DPIC -KPIC -z combreloc -z redlocsym -z ignore -z rescan -z absexec -s"
%endif

export LDFLAGS="%_ldflags -lgcc_s"
cd gmp-%{version}

%if %{build_64bit}
export CFLAGS="-m64 -mfpmath=sse,387 -msse2 -fPIC -DPIC -mtune=opteron -O3 -fomit-frame-pointer -fno-builtin -finline-functions -D_REENTRANT -D__EXTENSIONS__=1"
export CXXFLAGS="-m64 -mfpmath=sse,387 -msse2 -fPIC -DPIC -mtune=opteron -O2 -fno-builtin -finline-functions -D_REENTRANT -D__EXTENSIONS__=1"
export ABI=64

cp configure configure.orig
cat configure.orig | gsed 's/cclist="gcc cc"/cclist="gcc cc"; host_cpu="x86_64"/
/# PATH needs CR/a archive_cmds_need_lc=no; archive_cmds_need_lc_CXX=no
/archive_cmds_need_lc=yes/archive_cmds_need_lc=no/g
/archive_cmds_need_lc_CXX=yes/archive_cmds_need_lc_CXX=no/g' > configure
%else

export CFLAGS="-fPIC -DPIC -O2 -march=pentium3 -fno-builtin -finline-functions -D_REENTRANT -D__EXTENSIONS__=1"
export CXXFLAGS="-fPIC -DPIC -O2 -march=pentium3 -fno-builtin -finline-functions -D_REENTRANT -D__EXTENSIONS__=1"
export ABI=32

cp configure configure.orig
cat configure.orig | gsed '/# PATH needs CR/a archive_cmds_need_lc=no; archive_cmds_need_lc_CXX=no
/archive_cmds_need_lc=yes/archive_cmds_need_lc=no/g
/archive_cmds_need_lc_CXX=yes/archive_cmds_need_lc_CXX=no/g' > configure
%endif


./configure --prefix=%{_prefix}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}         \
            --infodir=%{_infodir}       \
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --includedir=%{_includedir}/gmp             \
            --enable-cxx --enable-mpbsd
make -j $CPUS 

%install
rm -rf $RPM_BUILD_ROOT
cd gmp-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*la
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

#
# For GMP 64Bit headers are different from 32Bit headers
#
%if %{build_64bit}
mv $RPM_BUILD_ROOT/%{_includedir}/gmp.h $RPM_BUILD_ROOT/%{_includedir}/gmp/gmp-64.h
cp gmp-mparam.h $RPM_BUILD_ROOT/%{_includedir}/gmp/gmp-mparam-64.h
chmod 0644 $RPM_BUILD_ROOT/%{_includedir}/gmp/gmp-mparam-64.h
%else

mv $RPM_BUILD_ROOT/%{_includedir}/gmp.h $RPM_BUILD_ROOT/%{_includedir}/gmp/gmp-i386.h
cp gmp-mparam.h $RPM_BUILD_ROOT/%{_includedir}/gmp/gmp-mparam-i386.h
chmod 0644 $RPM_BUILD_ROOT/%{_includedir}/gmp/gmp-mparam-i386.h
%endif

cp %{SOURCE1} $RPM_BUILD_ROOT/%{_includedir}/gmp/gmp.h
chmod 0644 $RPM_BUILD_ROOT/%{_includedir}/gmp/gmp.h
cp %{SOURCE2} $RPM_BUILD_ROOT/%{_includedir}/gmp/gmp-mparam.h
chmod 0644 $RPM_BUILD_ROOT/%{_includedir}/gmp/gmp-mparam.h

mv $RPM_BUILD_ROOT/%{_includedir}/mp.h $RPM_BUILD_ROOT/%{_includedir}/gmp/

%clean
rm -rf $RPM_BUILD_ROOT

%post devel
PATH=/usr/bin:/usr/sfw/bin; export PATH
retval=0
for info in gmp.info gmp.info-1 gmp.info-2
do
  install-info --quiet --info-dir=%{_infodir} %{_infodir}/$info
done
exit $retval

%preun devel
PATH=/usr/bin:/usr/sfw/bin; export PATH
retval=0
for info in gmp.info gmp.info-1 gmp.info-2
do
  install-info --quiet --info-dir=%{_infodir} --delete %{_infodir}/$info
done

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/info

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, bin) %{_includedir}/gmp
%{_includedir}/gmp/*.h

%changelog
* Wed May 06 2009 - moinakg@belenix.org
- Enable building C++ library, build with Gcc4.4.
- Fix installation of 64Bit headers.
* Fri Apr 17 2009 - moinakg@gmail.com
- Bump version and remove upstreamed patch.
* Sun Feb 24 2008 - moinakg@gmail.com
- Change to avoid wierd error from make.
* Fri Nov 02 2007 - nonsea@users.sourceforge.net
- Remove Requires/BuildRequires to SFEreadline
* Fri Aug 17 2007 - trisk@acm.jhu.edu
- Fix x86_64 build
* Sat Jun 30 2007 - nonsea@users.sourceforge.net
- Use http url in Source.
* Tue Mar 07 2007 - dougs@truemail.co.th
- enabled 64-bit build and added speedup patch for AMD64
* Fri Jun 23 2006 - laca@sun.com
- rename to SFEgmp
- bump to 4.2.1
- create devel subpkg
- update attributes
* Thu Nov 17 2005 - laca@sun.com
- create
