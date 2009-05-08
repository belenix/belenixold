#
# spec file for package SFEcertmaster
#
# includes module(s): Certmaster
#
%include Solaris.inc

# pfexec groupadd func
# pfexec useradd -s /usr/bin/false -d / -g func -R root -P "Primary Administrator" func

Name:                    certmaster
Summary:                 A set of tools and a library for easily distributing SSL certificates to applications
Version:                 0.24
Source:                  http://people.fedoraproject.org/~alikins/files/certmaster/certmaster-%{version}.tar.gz
Source1:                 certmaster.xml
Source2:                 certmaster.sh
Source3:                 certmaster-initchk.sh
URL:                     https://fedorahosted.org/certmaster/

SUNW_BaseDir:            /
SUNW_Copyright:          LICENSE.GPL
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                SUNWPython25
Requires:                SUNWpython25-pyopenssl
BuildRequires:           SUNWPython25-devel


%prep
%setup -q -c -n %{name}-%version

%build
cd certmaster-%{version}

python2.5 setup.py build_ext
python2.5 setup.py build

%install
rm -rf $RPM_BUILD_ROOT
cd certmaster-%{version}

python2.5 setup.py install --prefix=%{_prefix} --root=${RPM_BUILD_ROOT}
rm -rf ${RPM_BUILD_ROOT}%{_sysconfdir}/init.d
gunzip ${RPM_BUILD_ROOT}%{_mandir}/man1/*.gz
rm -f ${RPM_BUILD_ROOT}%{_mandir}/man1/*.gz

mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/svc/manifest/application
cp %{SOURCE1} ${RPM_BUILD_ROOT}%{_localstatedir}/svc/manifest/application
chmod 0644 ${RPM_BUILD_ROOT}%{_localstatedir}/svc/manifest/application/*

mkdir -p ${RPM_BUILD_ROOT}/lib/svc/method
cp %{SOURCE2} ${RPM_BUILD_ROOT}/lib/svc/method/svc-certmaster
chmod 0755 ${RPM_BUILD_ROOT}/lib/svc/method/svc-certmaster

mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/certmaster
cp %{SOURCE3} ${RPM_BUILD_ROOT}%{_libdir}/certmaster/certmaster-initchk
chmod a+x ${RPM_BUILD_ROOT}%{_libdir}/certmaster/certmaster-initchk

#
# These directries will be created at runtime with the appropriate
# certmaster daemon user ownership.
#
rm -rf ${RPM_BUILD_ROOT}%{_localstatedir}/lib/certmaster/*
rm -rf ${RPM_BUILD_ROOT}%{_sysconfdir}/pki/*
rm -rf ${RPM_BUILD_ROOT}%{_localstatedir}/log/certmaster/*

%clean
rm -rf $RPM_BUILD_ROOT

%iclass preserve -f i.preserve

%files
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/python2.5
%dir %attr (0755, root, bin) %{_libdir}/python2.5/site-packages
%{_libdir}/python2.5/site-packages/*
%dir %attr (0755, root, bin) %{_libdir}/certmaster
%{_libdir}/certmaster/certmaster-initchk
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, sys) %{_sysconfdir}
%dir %attr (0755, root, bin) %{_sysconfdir}/certmaster
%dir %attr (0755, root, bin) %{_sysconfdir}/certmaster/minion-acl.d
%config %class(preserve) %attr (0644, root, bin) %{_sysconfdir}/certmaster/minion.conf
%config %class(preserve) %attr (0644, root, bin) %{_sysconfdir}/certmaster/certmaster.conf
%dir %attr (0755, root, bin) %{_sysconfdir}/logrotate.d
%{_sysconfdir}/logrotate.d/*
%dir %attr (0777, root, bin) %{_sysconfdir}/pki
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, other) %{_localstatedir}/lib
%dir %attr (0777, root, bin) %{_localstatedir}/lib/certmaster
%dir %attr (0755, root, sys) %{_localstatedir}/log
%dir %attr (0777, root, bin) %{_localstatedir}/log/certmaster
%dir %attr (0755, root, bin) /lib
%dir %attr (0755, root, bin) /lib/svc
%dir %attr (0755, root, bin) /lib/svc/method
%attr (0755, root, bin) /lib/svc/method/svc-certmaster
%dir %attr (0755, root, sys) %{_localstatedir}/svc
%dir %attr (0755, root, sys) %{_localstatedir}/svc/manifest
%dir %attr (0755, root, sys) %{_localstatedir}/svc/manifest/application
%class(manifest) %attr (0755, root, sys) %{_localstatedir}/svc/manifest/application/certmaster.xml

%changelog
* Fri May 08 2009 - moinakg@belenix.org
- Updated startup scripts and add Solaris functionality.
- Renamed package and multitude of fixes.
* Web May 06 2009 - moinakg@belenix.org
- Initial spec file
