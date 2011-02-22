%define build_gcc_with_gnu_ld 0
%define build_libstdcxx_docs 0
%define osrev %(/usr/bin/uname -r)
%define gcc_target_platform %(/usr/bin/uname -p)-%{_target_vendor}-solaris%{osrev}

Name:       gcc
Summary:    GNU Gcc compiler suite (C, C++, Fortran)
Version:    4.5.2
Release:    2%{?dist}
Group:      Development/Languages
%define full_ver     %{version}
Source:     ftp://ftp.gnu.org/pub/gnu/gcc/gcc-%{version}/gcc-%{version}.tar.bz2
Group:      System Environment/Libraries
License:    GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions

Patch1:    gcc4-01-nameser_compat.diff
Patch2:    gcc4-02-handle_pragma_pack_push_pop.diff
Patch3:    gcc45-c++-builtin-redecl.patch
Patch4:    gcc45-libgomp-omp_h-multilib.patch
Patch5:    gcc45-pr33763.patch
Patch6:    gcc45-pr38757.patch
Patch7:    gcc45-libstdc++-docs.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-build
BuildRequires: gmp-devel
BuildRequires: libmpc-devel
Requires: gmp
Requires: libmpc
Requires: libgcc
#BuildRequires: gnu-binutils
#Requires: gnu-binutils
BuildRequires: mpfr-devel
BuildRequires: ppl-devel
BuildRequires: cloog-devel
Requires: mpfr
Requires: ppl
Requires: cloog
%if %{build_libstdcxx_docs}
#BuildRequires: doxygen
#BuildRequires: graphviz
%endif

%description
The gcc package contains the GNU Compiler Collection version %{version}
You'll need this package in order to compile C code.

%package -n libgcc
Summary:    Basic GNU gcc support library required by applications
Version:    %{version}
Group:      Development/Libraries
License:    GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions
#Requires: libc

%description
This package contains GCC shared support library which is needed
e.g. for exception handling support.

%if %build_l10n
%package -n gcc-l10n
Version:    %{version}
Group:      System Environment/Libraries
License:    GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions
Summary:    %{summary} - l10n files
Requires:   %{name}
%endif

%package -n libstdc++
Summary:    GNU Standard C++ Library
Version:    %{version}
Group:      System Environment/Libraries
License:    GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions
#Requires:  libc

%description -n libstdc++
The libstdc++ package contains a rewritten standard compliant GCC Standard
C++ Library.

%package -n libstdc++-docs
Summary:    GNU Standard C++ Library Documentation
Version:    %{version}
Group:      Development/Documentation
License:    GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions
Requires:   libstdc++

%description -n libstdc++-docs
HTML documentation files for libstdc++.

%package -n libobjc
Summary:    Objective-C runtime
Version:    %{version}
Group:      System Environment/Libraries
License:    GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions
#Requires:  libc

%description -n libobjc
This package contains Objective-C shared library which is needed to run
Objective-C dynamically linked programs.

%package -n libgfortran
Summary:    Fortran runtime
Version:    %{version}
Group:      System Environment/Libraries
License:    GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions
#Requires:  libc

%description -n libgfortran
This package contains Fortran shared library which is needed to run
Fortran dynamically linked programs.

%package -n libgomp
Summary:    GCC OpenMP v3.0 shared support library
Version:    %{version}
Group:      System Environment/Libraries
License:    GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions
#Requires:  libc

%description -n libgomp
This package contains GCC shared support library which is needed
for OpenMP v3.0 support.


%prep
if [ "x${CC}" = "x" ]
then
	echo "Compiler not defined. Please set the CC and CXX environment variables."
	exit 1
fi

%setup -q -c -n %{name}-%version
mkdir build
cd gcc-%{full_ver}
%patch2 -p1
%patch3 -p0
%patch4 -p0
%patch5 -p0
%patch6 -p0
%patch7 -p0

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export PATH=/usr/gnu/bin:`dirname ${CC}`:/usr/bin:/usr/X11/bin:/usr/sbin:/sbin:/usr/sfw/bin
cd build

%if %build_l10n
nlsopt=-enable-nls
%else
nlsopt=-disable-nls
%endif
%define ld_options      -zignore -zcombreloc -Bdirect 

export CONFIG_SHELL=/usr/bin/bash
export CFLAGS=""
%if %gcc_compiler
export CPP=cpp
%else
export CPP="cc -E -Xs"
%endif
export STAGE1_CFLAGS="-DHANDLE_PRAGMA_PACK_PUSH_POP=1"
export CFLAGS_FOR_TARGET="-g -O3 -I/usr/include/gmp -I/usr/include/mpfr"
export LDFLAGS="-Wl,-zignore -Wl,-zcombreloc -Wl,-Bdirect"
export LD_OPTIONS="%ld_options"
export CPPFLAGS="-I/usr/include/gmp -I/usr/include/mpfr"

%if %build_gcc_with_gnu_ld
export LD="/usr/gnu/bin/ld"
%endif

../gcc-%{full_ver}/configure			\
	--prefix=%{_prefix}			\
        --mandir=%{_mandir}			\
	--infodir=%{_infodir}			\
	--with-as=/usr/bin/gas		        \
	--with-gnu-as				\
%if %build_gcc_with_gnu_ld
	--with-ld=/usr/gnu/bin/gld		\
	--with-gnu-ld				\
%else
	--with-ld=/usr/ccs/bin/ld		\
	--without-gnu-ld			\
%endif
	--enable-languages=c,c++,fortran,objc,obj-c++	\
	--enable-shared				\
	--disable-static			\
	--enable-decimal-float			\
        --enable-multilib 			\
        --with-system-zlib 			\
        --enable-gather-detailed-mem-stats	\
        --enable-largefile			\
        --enable-symvers			\
        --without-system-libunwind		\
        --disable-libmudflap			\
        --with-long-double-128			\
        --enable-__cxa_atexit                   \
        --enable-checking=release               \
%ifarch x86_64
        --with-arch_32=i686                     \
%endif
        --enable-decimal-float			\
        --enable-lto                            \
	$nlsopt

        #--with-ppl=%{_prefix}			
gmake -j $CPUS bootstrap

%if %{build_libstdcxx_docs}
cd %{gcc_target_platform}/libstdc++-v3
make doc-html-doxygen
make doc-man-doxygen
cd ../..
%endif

%install
rm -rf $RPM_BUILD_ROOT

export CONFIG_SHELL=/usr/bin/bash
export CFLAGS="%optflags"
export STAGE1_CFLAGS="$(CFLAGS) -DHANDLE_PRAGMA_PACK_PUSH_POP=1"
export CFLAGS_FOR_TARGET="-g -O3"
export LDFLAGS="%_ldflags"
export LD_OPTIONS="%ld_options"

cd build
gmake install DESTDIR=$RPM_BUILD_ROOT
BDIR=`pwd`

cd $RPM_BUILD_ROOT
%patch1 -p0

cd $RPM_BUILD_ROOT%{_prefix}
ln -s share/man man

rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_libdir32}/libssp.so*
rm -f $RPM_BUILD_ROOT%{_libdir64}/libssp.so*
rm -f $RPM_BUILD_ROOT%{_libdir32}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir64}/*.la

mv $RPM_BUILD_ROOT%{_libdir32}/*.a  $RPM_BUILD_ROOT%{_libdir32}/gcc/i386-pc-solaris2.11/%{version}
mv $RPM_BUILD_ROOT%{_libdir64}/*.a  $RPM_BUILD_ROOT%{_libdir32}/gcc/i386-pc-solaris2.11/%{version}/%{_arch64}

(cd $RPM_BUILD_ROOT%{_libdir32}/gcc/i386-pc-solaris2.11/%{version}
 rm -f libssp_nonshared.a
 ar cr libssp_nonshared.a ${BDIR}/i386-pc-solaris2.11/libssp/.libs/*.o
 ln -s libssp_nonshared.a libssp.a
 cd %{_arch64}
 ln -s libssp_nonshared.a libssp.a)

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post -n gcc
PATH=/usr/bin:/usr/sfw/bin; export PATH
for info in gcc.info cpp.info gccint.info cppinternals.info gccinstall.info gfortran.info
do
  install-info --info-dir=%{_infodir} %{_infodir}/$info
done

%preun -n gcc
PATH=/usr/bin:/usr/sfw/bin; export PATH
retval=0
for info in gcc.info cpp.info gccint.info cppinternals.info gccinstall.info gfortran.info
do
  install-info --info-dir=%{_infodir} --delete %{_infodir}/$info
done

%files 
%defattr (-, root, bin)
%{_prefix}/man
%{_bindir32}/*
%{_libdir32}/gcc
%{_libexecdir32}/gcc
%{_mandir}/man1/*.1
%{_mandir}/man7/*.7
%{_infodir}/*
%defattr (-, root, bin)
%{_includedir}/*

%files -n libgcc
%defattr (-, root, bin)
%{_libdir32}/libgcc_s*
%{_libdir64}/libgcc_s*

%files -n libstdc++
%defattr (-, root, bin)
%{_libdir32}/libstdc++*
%{_libdir64}/libstdc++*
%dir %attr (0755, root, bin) %{_datadir}/gcc-%{version}
%{_datadir}/gcc-%{version}/*

%files -n libobjc
%defattr (-, root, bin)
%{_libdir32}/libobjc*
%{_libdir64}/libobjc*

%files -n libgfortran
%defattr (-, root, bin)
%{_libdir32}/libgfortran*
%{_libdir64}/libgfortran*

%files -n libgomp
%defattr (-, root, bin)
%{_libdir32}/libgomp*
%{_libdir64}/libgomp*

%if %{build_libstdcxx_docs}
%files -n libstdc++-docs
%defattr(-,root,bin)
%{_mandir}/man3/*
%doc libstdc++-v3/html
%endif

%if %build_l10n
%files -n gcc-l10n
%defattr (-, root, bin)
%{_datadir}/locale/*
%endif

%changelog
* Sat Sep 12 2009 - moinakg(at)belenix<dot>org
- Fix package version.
* Sat Aug 29 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Bump version to 4.4.1.
- Add patch required for successful Wine build.
* Sat Aug 15 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Patch a header bug.
* Wed May 06 2009 - moinakg@belenix.org
- Enable building with ClooG and PPL libs to get the Graphite framework.
* Thu Apr 30 2009 - moinakg@belenix.org
- Bump to 4.4.0 release version.
* Tue Apr 28 2009 - moinakg@belenix.org
- Delete commented patch lines.
* Tue Apr 21 2009 - moinakg@belenix.org
- Bump to 4.4 pre-release snapshot. Comment out unneeded patches.
- Add configure options as tested for OSUNIX.
* Tue Aug 12 2008 - moinakg@belenix.org
- Change to use Solaris linker by default. GNU linker does not support versioned
- symbols in shared libraries.
* Tue Jun 26 2008 - russiaen39@gmail.com
- fixed libunwind bug. See http://gcc.gnu.org/bugzilla/show_bug.cgi?id=27880
* Mon Jun 23 2008 - russiane39@gmail.com
- added pragma pack support, bump up gcc to 4.2.4
* Mon Mar 10 2008 - laca@sun.com
- add missing defattr
* Sun Mar  2 2008 - Mark Wright <markwright@internode.on.net>
- Add gcc-01-libtool-rpath.diff patch for a problem where
- the old, modified libtool 1.4 in gcc 4.2.3 drops
- -rpath /usr/gnu/lib when building libstdc++.so.6.0.9.
* Fri Feb 29 2008 - Mark Wright <markwright@internode.on.net>
- Bump to 4.2.3.  Remove patch for 32787 as it is upstreamed into gcc 4.2.3.
* Sat Jan 26 2008 - Moinak Ghosh <moinak.ghosh@sun.com>
- Refactor package to have SFEgcc and SFEgccruntime.
* Sun Oct 14 2007 - Mark Wright <markwright@internode.on.net>
- Bump to 4.2.2.
* Wed Aug 15 2007 - Mark Wright <markwright@internode.on.net>
- Change from /usr/ccs/bin/ld to /usr/gnu/bin/ld, this change
  requires SFEbinutils built with binutils-01-bug-2495.diff,
  binutils-02-ld-m-elf_i386.diff and binutils-03-lib-amd64-ld-so-1.diff.
  Add objc to --enable-languages, add --enable-decimal-float.
* Wed Jul 24 2007 - Mark Wright <markwright@internode.on.net>
- Bump to 4.2.1, add patch for gcc bug 32787.
* Wed May 16 2007 - Doug Scott <dougs@truemail.co.th>
- Bump to 4.2.0
* Tue Mar 20 2007 - Doug Scott <dougs@truemail.co.th>
- Added LD_OPTIONS so libs in /usr/gnu/lib will be found
* Sun Mar  7 2007 - Doug Scott <dougs@truemail.co.th>
- change to use GNU as from SFEbinutils
* Sun Mar  7 2007 - Doug Scott <dougs@truemail.co.th>
- Initial spec
