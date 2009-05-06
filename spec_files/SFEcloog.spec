#
# spec file for package SFEcloog
#
# includes module(s): cloog
#
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

Name:                    SFEcloog
Summary:                 CLooG is a free software and library to generate code for scanning Z-polyhedra
Version:                 0.15.3
Source:                  ftp://gcc.gnu.org/pub/gcc/infrastructure/cloog-ppl-%{version}.tar.gz

SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          LICENSE.GPL
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWzlib
Requires: SUNWlibms
Requires: SFEppl
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
cp -rp cloog-ppl cloog-ppl-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

%ifarch amd64 sparcv9
cd cloog-ppl-64
export CFLAGS="%optflags64"
export CXXFLAGS="%cxx_optflags64"
export CPPFLAGS="-I/usr/include/%{_arch64}"
export LDFLAGS="%_ldflags -L/usr/gnu/lib/%{_arch64} -R/usr/gnu/lib/%{_arch64}"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --bindir=%{_bindir}/%{_arch64}              \
            --libdir=%{_libdir}/%{_arch64}              \
            --libexecdir=%{_libexecdir}/%{_arch64}      \
            --sysconfdir=%{_sysconfdir}      \
            --infodir=%{_infodir}           \
            --with-pic                       \
            --with-ppl                       \
            --enable-shared                  \
            --disable-static

make -j$CPUS
cd ..
%endif

cd cloog-ppl
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib"
export CPPFLAGS="-I/usr/include"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --bindir=%{_bindir}              \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --infodir=%{_infodir}           \
            --with-pic                       \
            --with-ppl                       \
            --enable-shared                  \
            --disable-static

make -j$CPUS
cd ..


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd cloog-ppl-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.la
cd ..
%endif

cd cloog-ppl
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
cd ..

rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir


%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'cloog.info' ;
  echo '"';
  echo 'retval=0';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} %{_infodir}/$info || retval=1';
  echo 'done';
  echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%preun
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'cloog.info' ;
  echo '"';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} --delete %{_infodir}/$info';
  echo 'done';
  echo 'exit 0' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/cloog
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_infodir}
%{_infodir}/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/cloog
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Web May 06 2009 - moinakg@belenix.org
- Initial spec file.
