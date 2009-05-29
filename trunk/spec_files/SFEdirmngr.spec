#
# spec file for package SFEdirmngr
#
# includes module(s): dirmngr
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

%define	src_name dirmngr
%define	src_url	ftp://ftp.gnupg.org/gcrypt/dirmngr

Name:                SFEdirmngr
Summary:             DirMngr is a server for managing certificates and certificate revocation lists (CRLs) for X.509 certificates.
Version:             1.0.2
License:             GPLv2
Source:              %{src_url}/%{src_name}-%{version}.tar.bz2
URL:                 http://www.gnupg.org/

SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlibgpg-error
Requires: SFElibassuan
Requires: SFElibksba
Requires: SFEpth
Requires: SUNWlibgcrypt
BuildRequires: SFElibksba-devel
BuildRequires: SFEpth-devel
BuildRequires: SUNWlibgcrypt-devel

%description
DirMngr is a server for managing and downloading certificate
revocation lists (CRLs) for X.509 certificates and for downloading
the certificates themselves. Dirmngr also handles OCSP requests as
an alternative to CRLs. Dirmngr is either invoked internaly by
gpgsm (from gnupg 1.9) or when running as a system daemon through
the dirmngr-client tool.

%package doc
Summary:                 Documentation files for dirmngr package
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%prep
%setup -q -c -n %name-%version

%ifarch amd64 sparcv9
cp -rp %{src_name}-%version %{src_name}-%{version}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CPPFLAGS="-I%{gnu_inc} -I%{gnu_inc}/openldap"
OPATH="${PATH}"

%ifarch amd64 sparcv9
cd %{src_name}-%{version}-64

export CFLAGS="%optflags64"
export LDFLAGS="%_ldflags64 %{gnu_lib_path64}"
export PATH="%{_prefix}/bin/%{_arch64}:%{_prefix}/gnu/bin/%{_arch64}:${PATH}"

bash ./configure --prefix=%{_prefix}			\
            --bindir=%{_bindir}/%{_arch64}	\
            --libdir=%{_libdir}/%{_arch64}	\
            --libexecdir=%{_libdir}/%{_arch64}	\
            --sysconfdir=%{_sysconfdir}		\
            --includedir=%{_includedir} 	\
            --mandir=%{_mandir}			\
	    --infodir=%{_infodir}		\
	    --disable-rpath			\
	    --disable-static			\
	    --enable-shared

make -j$CPUS
cd ..
%endif

cd %{src_name}-%{version}
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags %{gnu_lib_path}"
export PATH="${OPATH}"

bash ./configure --prefix=%{_prefix}                 \
            --bindir=%{_bindir}                 \
            --libdir=%{_libdir}                 \
            --libexecdir=%{_libdir}                 \
            --sysconfdir=%{_sysconfdir}         \
            --includedir=%{_includedir}         \
            --mandir=%{_mandir}                 \
            --infodir=%{_infodir}               \
            --disable-rpath                     \
            --disable-static                    \
            --enable-shared

make -j$CPUS
cd .. 

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
cd %{src_name}-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/lib*.*a
cd ..
%endif

cd %{src_name}-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a
cd ..

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'dirmngr.info' ;
  echo '"';
  echo 'retval=0';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} %{_infodir}/$info || retval=1';
  echo 'done';
  echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%preun
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'dirmngr.info' ;
  echo '"';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} --delete %{_infodir}/$info';
  echo 'done';
  echo 'exit 0' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/dirmngr*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/dirmngr_ldap

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/dirmngr*
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/dirmngr_ldap
%endif

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_localedir}
%{_localedir}/*

%files doc
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*
%dir %attr (0755, root, bin) %{_infodir}
%{_infodir}/dirmngr.info

%changelog
* Fri May 29 2009 - Moinak Ghosh <moinakg@belenix(dot)org>
- Initial version.
