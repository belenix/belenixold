#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# spec file for package SUNWgmp
#
# includes module(s): GNU gmp
#
%include Solaris.inc

Name:                    SFEgmp
Summary:                 GNU Multiple Presicion Arithmetic Library
Group:                   libraries/math
Version:                 4.2.4
Source:                  http://ftp.gnu.org/gnu/gmp/gmp-%{version}.tar.bz2
%ifarch amd64
Source1:                 http://www.loria.fr/~gaudry/mpn_AMD64/mpn_amd64.42.tgz
%endif
URL:                     http://swox.com/gmp/
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          LICENSE.LGPL
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SFEgccruntime
BuildRequires: SFEgcc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -c -n %name-%version
%ifarch amd64 sparcv9
cp -pr gmp-%{version} gmp-%{version}-64
%endif
%ifarch amd64
gtar fxz %{SOURCE1}
cd mpn_amd64.42
./install ../gmp-%{version}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CC32=${CC32:-$CC}
%if %cc_is_gcc
CFLAGS_GEN="-fno-builtin -finline-functions -std=c99 -D_REENTRANT -D__EXTENSIONS__=1 -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64 -D_XOPEN_SOURCE=600 -D_XPG6 -D_POSIX_PTHREAD_SEMANTICS -D_POSIX_C_SOURCE=200112L -D__XOPEN_OR_POSIX -D_STRICT_STDC -D_STRICT_STDC__ -D_STDC_C99 -D_ISOC99_SOURCE -DNDEBUG -DPIC -fPIC -z combreloc -z redlocsym -z ignore -z rescan -z absexec -s"
export CPPFLAGS="-fexceptions"

%else
CFLAGS_GEN="-features=extinl -xbuiltin=%none -xcsi -xinline=%auto -xustr=ascii_utf16_ushort -xalias_level=std -xthreadvar=%all -mt -D_REENTRANT -D__EXTENSIONS__=1 -xF=%none -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64 -D_XOPEN_SOURCE=600 -D_XPG6 -D_POSIX_PTHREAD_SEMANTICS -D_POSIX_C_SOURCE=200112L -D__XOPEN_OR_POSIX -D_STRICT_STDC -D_STRICT_STDC__ -D_STDC_C99 -D_ISOC99_SOURCE -DNDEBUG -DPIC -KPIC -z combreloc -z redlocsym -z ignore -z rescan -z absexec -s"
%endif

export CFLAGS32="%optflags"
export CFLAGS64="%optflags64"
export CXXFLAGS32="%cxx_optflags"
export CXXFLAGS64="%cxx_optflags64"
export LDFLAGS32="%_ldflags"
export LDFLAGS64="%_ldflags"
export CXX_ORIG64=${CXX64:-$CXX}
export CXX_ORIG32=${CXX32:-$CXX}

%if %cc_is_gcc
export LDFLAGS32="$LDFLAGS32 -L/usr/gnu/lib -R/usr/gnu/lib"
export LDFLAGS64="$LDFLAGS64 -L/usr/gnu/lib/%{_arch64} -R/usr/gnu/lib/%{_arch64}"
%endif

%ifarch sparcv9
export CC=${CC64:-$CC}
export CXX="${CXX_ORIG64}"
export CFLAGS="$CFLAGS64"
export CXXFLAGS="$CXXFLAGS64"
export LDFLAGS="$LDFLAGS64"
%endif

%ifarch amd64
export CC="gcc"
export CFLAGS="-mtune=opteron -m64 -O3 -fomit-frame-pointer -fPIC -DPIC"
export CXXFLAGS="$CXXFLAGS64"
export LDFLAGS="$LDFLAGS64"
%if %cc_is_gcc
export CXX="$CXX_ORIG64 -L/usr/gnu/lib/%{_arch64} -R/usr/gnu/lib/%{_arch64}"
%else
export CXX="$CXX_ORIG64"
%endif
%endif


%ifarch amd64 sparcv9
cd gmp-%{version}-64

libtoolize --copy --force
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f 
autoconf
export ABI=64

cp configure configure.orig
cat configure.orig | sed 's/cclist="gcc cc"/cclist="gcc cc"; host_cpu="x86_64"/' > configure
./configure --prefix=%{_prefix}				\
	    --mandir=%{_mandir}				\
            --libdir=%{_libdir}/%{_arch64}		\
            --infodir=%{_infodir}			\
            --libexecdir=%{_libexecdir}/%{_arch64}      \
            --sysconfdir=%{_sysconfdir}			\
            --enable-cxx
make -j $CPUS 
cd ..
%endif

cd gmp-%{version}

export CC=${CC32:-$CC}
export CXX="${CXX_ORIG32}"
export CFLAGS="$CFLAGS32"
export CXXFLAGS="$CXXFLAGS32"
export LDFLAGS="$LDFLAGS32"
%if %cc_is_gcc
export CXX="$CXX -L/usr/gnu/lib -R/usr/gnu/lib"
%endif

export ABI=32
./configure --prefix=%{_prefix}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}         \
            --infodir=%{_infodir}       \
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-cxx
make -j $CPUS 

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
cd gmp-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_libdir}/%{_arch64}/*.a
rm -f $RPM_BUILD_ROOT/%{_libdir}/%{_arch64}/*.la

#
# For GMP 64Bit headers are different from 32Bit headers
#
mkdir -p $RPM_BUILD_ROOT/%{_includedir}/%{_arch64}
mv $RPM_BUILD_ROOT/%{_includedir}/*.h $RPM_BUILD_ROOT/%{_includedir}/%{_arch64}
cd ..
%endif

cd gmp-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'gmp.info gmp.info-1 gmp.info-2' ;
  echo '"';
  echo 'retval=0';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} %{_infodir}/$info || retval=1';
  echo 'done';
  echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%preun
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'gmp.info gmp.info-1 gmp.info-2' ;
  echo '"';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} --delete %{_infodir}/$info';
  echo 'done';
  echo 'exit 0' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/info
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*.h
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_includedir}/%{_arch64}
%{_includedir}/%{_arch64}/*.h
%endif

%changelog
* Web May 06 2009 - moinakg@belenix.org
- Enable building C++ library, build with Gcc4.4.
- Fix installation of 64Bit headers.
* Fri Apr 17 2009 - moinakg@gmail.com
- Bump version and remove upstreamed patch.
* Sun Feb 24 2008 - moinakg@gmail.com
- Change to avoid wierd error from make.
* Fri Nov 02 2007 - nonsea@users.sourceforge.net
- Remove Requires/BuildRequires to SFEreadline
* Fri Aug 17 2007 - trisk@acm.jhu.edu
- Fix amd64 build
* Sat Jun 30 2007 - nonsea@users.sourceforge.net
- Use http url in Source.
* Tue mar  7 2007 - dougs@truemail.co.th
- enabled 64-bit build and added speedup patch for AMD64
* Fri Jun 23 2006 - laca@sun.com
- rename to SFEgmp
- bump to 4.2.1
- create devel subpkg
- update attributes
* Thu Nov 17 2005 - laca@sun.com
- create
