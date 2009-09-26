#
# spec file for package SFEplotutils
#
# includes module(s): plotutils
#

%include Solaris.inc
%include usr-gnu.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc


Name:         SFEplotutils
Summary:      GNU vector and raster graphics utilities and libraries
Group:        Applications/Productivity
Version:      2.5
License:      GPLv2+
BuildRoot:    %{_tmppath}/plotutils-%{version}-build
Source:       http://ftp.gnu.org/gnu/plotutils/plotutils-%{version}.tar.gz
URL:          http://www.gnu.org/software/plotutils/
SUNW_BaseDir: %{_basedir}
%include default-depend.inc
Requires:      FSWxorg-clientlibs
Requires:      SUNWpng
Requires:      SUNWpostrun
BuildRequires: SUNWxorg-headers
BuildRequires: SUNWpng-devel
BuildRequires: SUNWflexlex

%description
The GNU plotutils package contains software for both programmers and
technical users. Its centerpiece is libplot, a powerful C/C++ function
library for exporting 2-D vector graphics in many file formats, both
vector and raster. It can also do vector graphics animations. Besides
libplot, the package contains command-line programs for plotting
scientific data. Many of them use libplot to export graphics.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SUNWxorg-headers
Requires: SUNWpng-devel
Requires: SUNWflexlex
Requires: FSWxorg-clientlibs

%prep
%setup -q -c -n %name-%version
%ifarch amd64 sparcv9
cp -pr plotutils-%{version} plotutils-%{version}-64
%endif


%build
%ifarch amd64 sparcv9
cd plotutils-%{version}-64
export CFLAGS="%optflags64"
export CXXFLAGS="%cxx_optflags64"
export LDFLAGS="%_ldflags64"
        ./configure                     \
                --prefix=%{_prefix}     \
                --mandir=%{_mandir}     \
                --infodir=%{_infodir}   \
                --libdir=%{_libdir}/%{_arch64}     \
                --disable-static        \
                --enable-libplotter     \
                --enable-libxmi         \
                --enable-ps-fonts-in-pcl
make
cd ..
%endif

cd plotutils-%{version}
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags"
        ./configure                     \
                --prefix=%{_prefix}     \
                --mandir=%{_mandir}     \
                --infodir=%{_infodir}   \
                --libdir=%{_libdir}     \
                --disable-static        \
                --enable-libplotter     \
                --enable-libxmi         \
                --enable-ps-fonts-in-pcl
make
cd ..

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd plotutils-%{version}-64
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/lib*.la
cd ..
%endif

cd plotutils-%{version}
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la
rm ${RPM_BUILD_ROOT}%{_infodir}/dir
cd ..

%post
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'libxmi.info plotutils.info' ;
  echo '"';
  echo 'retval=0';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} %{_infodir}/$info || retval=1';
  echo 'done';
  echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%preun
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'libxmi.info plotutils.info' ;
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
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/tek2plot
%{_datadir}/tek2plot/*
%dir %attr (0755, root, bin) %{_datadir}/pic2plot
%{_datadir}/pic2plot/*
%dir %attr (0755, root, bin) %{_datadir}/libplot
%{_datadir}/libplot/*
%dir %attr (0755, root, bin) %{_datadir}/ode
%{_datadir}/ode/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, sys) /usr/share
%dir %attr (0755, root, bin) /usr/share/info
/usr/share/info/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}

%changelog
* Sat Sep 26 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Initial version.
