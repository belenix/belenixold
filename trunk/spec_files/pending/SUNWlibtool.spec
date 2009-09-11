#
# spec file for package SUNWlibtool, SUNWltdl
#
# includes module(s): libtool
#
%include Solaris.inc

%define	src_ver 2.2.4
%define	src_name libtool
%define	src_url	ftp://ftp.gnu.org/gnu/libtool/

Name:		SUNWlibtool
Summary:	GNU libtool - library support utility
Version:	%{src_ver}
License:	GPL
Source:		%{src_url}/%{src_name}-%{version}.tar.gz

SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
BuildRequires: SFEcmake
Requires: SUNWltdl
Requires: SUNWbash
Requires: SUNWxcu4
Requires: SUNWbtool
Requires: SFEsed
Requires: SUNWpostrun

%package -n SUNWltdl
Summary:                 libltdl - GNU libtool dlopen wrapper
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: SUNWlibmsr

%prep
%setup -q -n %{src_name}-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --libdir=%{_libdir} \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir} \
            --includedir=%{_includedir}

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT CMAKE_INSTALL_PREFIX=/usr
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a
rm -f $RPM_BUILD_ROOT%{_datadir}/info/dir

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'libtool.info libtool.info-1' ;
  echo '"';
  echo 'retval=0';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} %{_infodir}/$info || retval=1';
  echo 'done';
  echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%preun
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'libtool.info libtool.info-1' ;
  echo '"';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} --delete %{_infodir}/$info';
  echo 'done';
  echo 'exit 0' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%{_includedir}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/libtool
%{_datadir}/libtool/*
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%dir %attr(0755, root, bin) %{_datadir}/info
%{_datadir}/info/*

%files -n SUNWltdl
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%changelog
* Mon Jul 30 2007 - dougs@truemail.co.th
- Initial spec
