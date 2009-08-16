#
# spec file for package SFEgcc
#
# includes module(s): GNU gcc
#
%include Solaris.inc
%include usr-gnu.inc
%include base.inc

Name:                SFEgccruntime
Summary:             GNU gcc runtime libraries required by applications
Version:             4.4.0
#%define snap_ver     20090331
%define full_ver     %{version}
Source:              ftp://ftp.gnu.org/pub/gnu/gcc/gcc-%{version}/gcc-%{version}.tar.bz2
#Source:              ftp://ftp.nluug.nl/mirror/languages/gcc/snapshots/%{full_ver}/gcc-%{full_ver}.tar.bz2
Patch1:              gcc4-01-nameser_compat.diff

SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      SFEgccruntime.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEgmp-devel
BuildRequires: SFEbinutils
Requires: SFEbinutils
BuildRequires: SFEmpfr-devel
BuildRequires: SFEppl-devel
BuildRequires: SFEcloog-devel
Requires: SFEmpfr
Requires: SFEgmp
Requires: SFEppl
Requires: SFEcloog
Requires: SUNWpostrun

%package -n SFEgcc
Summary:                 GNU gcc
Version:                 4.4

SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          SFEgcc.copyright
%include default-depend.inc
Requires: %name
BuildRequires: SFEgmp-devel
BuildRequires: SFEbinutils
Requires: SFEbinutils
BuildRequires: SFEmpfr-devel
Requires: SFEmpfr
Requires: SFEgmp
Requires: SUNWpostrun


%if %build_l10n
%package -n SFEgcc-l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -c -n %{name}-%version
mkdir gcc
cd gcc-%{full_ver}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

cd gcc

%if %build_l10n
nlsopt=-enable-nls
%else
nlsopt=-disable-nls
%endif

%define ld_options      -zignore -zcombreloc -Bdirect -i

%define gnu_lib_path -L/usr/gnu/lib -R/usr/gnu/lib
export PATH="/opt/SUNWspro/bin:/usr/sfw/bin:/usr/gnu/bin:/usr/bin:/usr/X11/bin:/usr/sbin:/sbin:/usr/sfw/bin"
export CONFIG_SHELL=/usr/bin/bash
export CFLAGS=""
export CPP="cc -E -Xs"
export STAGE1_CFLAGS="$(CFLAGS) -DHANDLE_PRAGMA_PACK_PUSH_POP=1"
export CFLAGS_FOR_TARGET="-g -O3"
export LDFLAGS="%_ldflags %gnu_lib_path"
export LD_OPTIONS="%ld_options %gnu_lib_path"

%if %build_gcc_with_gnu_ld
export LD="/usr/gnu/bin/ld"
%endif

../gcc-%{full_ver}/configure			\
	--prefix=%{_prefix}			\
        --libdir=%{_libdir}			\
        --libexecdir=%{_libexecdir}		\
        --mandir=%{_mandir}			\
	--infodir=%{_infodir}			\
	--with-as=/usr/gnu/bin/gas		\
	--with-gnu-as				\
%if %build_gcc_with_gnu_ld
	--with-ld=/usr/gnu/bin/gld		\
	--with-gnu-ld				\
%else
	--with-ld=/usr/ccs/bin/ld		\
	--without-gnu-ld			\
%endif
	--enable-languages=c,c++,fortran,objc	\
	--enable-shared				\
	--disable-static			\
	--enable-decimal-float			\
        --enable-multilib 			\
        --with-system-zlib 			\
        --with-ppl=%{_prefix}			\
        --enable-gather-detailed-mem-stats	\
        --enable-largefile			\
        --enable-symvers			\
        --without-system-libunwind		\
        --disable-libmudflap			\
        --with-long-double-128			\
        --enable-decimal-float			\
	$nlsopt

make -j$CPUS bootstrap

%install
rm -rf $RPM_BUILD_ROOT

export CONFIG_SHELL=/usr/bin/bash
export CFLAGS="%optflags"
export STAGE1_CFLAGS="$(CFLAGS) -DHANDLE_PRAGMA_PACK_PUSH_POP=1"
export CFLAGS_FOR_TARGET="-g -O3"
export LDFLAGS="%_ldflags %gnu_lib_path"
export LD_OPTIONS="%ld_options %gnu_lib_path"

cd gcc
make install DESTDIR=$RPM_BUILD_ROOT

cd $RPM_BUILD_ROOT
%patch1 -p0

cd $RPM_BUILD_ROOT%{_prefix}
ln -s share/man man

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post -n SFEgcc
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'gcc.info cpp.info gccint.info cppinternals.info gccinstall.info gfortran.info' ;
  echo '"';
  echo 'retval=0';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} %{_infodir}/$info || retval=1';
  echo 'done';
  echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%preun -n SFEgcc
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'gcc.info cpp.info gccint.info cppinternals.info gccinstall.info gfortran.info' ;
  echo '"';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} --delete %{_infodir}/$info';
  echo 'done';
  echo 'exit 0' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/lib*.spec
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%{_libdir}/%{_arch64}/lib*.spec
%endif


%files -n SFEgcc
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}
%{_prefix}/man
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.a
%{_libdir}/lib*.la
%{_libdir}/gcc
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*.1
%dir %attr (0755, root, bin) %{_mandir}/man7
%{_mandir}/man7/*.7
%dir %attr(0755, root, sys) %{_std_datadir}
%dir %attr(0755, root, bin) %{_infodir}
%{_infodir}/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.a
%{_libdir}/%{_arch64}/lib*.la
%endif
%defattr (-, root, bin)
%{_includedir}

%if %build_l10n
%files -n SFEgcc-l10n
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sat Aug 15 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Patch a header bug.
* Web May 06 2009 - moinakg@belenix.org
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
