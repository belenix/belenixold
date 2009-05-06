#
# spec file for package SFEfunc
#
# includes module(s): Func
#
%include Solaris.inc

# pfexec groupadd func
# pfexec useradd -s /usr/bin/false -d / -g func -R root -P "Primary Administrator" func

Name:                    SFEfunc
Summary:                 Fedora Unified Network Controller
Version:                 0.24
Source:                  http://people.fedoraproject.org/~alikins/files/func/func-%{version}.tar.gz
Source1:                 func.xml
Source2:                 func.sh
Source3:                 mydbm.py
Patch1:                  func-01-dbm.diff
URL:                     https://fedorahosted.org/func/

SUNW_BaseDir:            /
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                SUNWPython25
Requires:                SUNWpython25-pyopenssl
Requires:                SFEcertmaster
BuildRequires:           SUNWPython25-devel


%prep
%setup -q -c -n %{name}-%version
cd func-%{version}
%patch1 -p1
cp %{SOURCE3} func/

%build
cd func-%{version}

python2.5 setup.py build_ext
python2.5 setup.py build

%install
rm -rf $RPM_BUILD_ROOT
cd func-%{version}

python2.5 setup.py install --prefix=%{_prefix} --root=${RPM_BUILD_ROOT}
rm -rf ${RPM_BUILD_ROOT}%{_sysconfdir}/init.d
gunzip ${RPM_BUILD_ROOT}%{_mandir}/man1/*.gz
rm -f ${RPM_BUILD_ROOT}%{_mandir}/man1/*.gz

mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/svc/manifest/application
cp %{SOURCE1} ${RPM_BUILD_ROOT}%{_localstatedir}/svc/manifest/application
chmod 0644 ${RPM_BUILD_ROOT}%{_localstatedir}/svc/manifest/application/*

mkdir -p ${RPM_BUILD_ROOT}/lib/svc/method
cp %{SOURCE2} ${RPM_BUILD_ROOT}/lib/svc/method/svc-func
chmod 0755 ${RPM_BUILD_ROOT}/lib/svc/method/svc-func

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
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, sys) %{_sysconfdir}
%dir %attr (0755, root, bin) %{_sysconfdir}/func
%dir %attr (0755, root, bin) %{_sysconfdir}/func/minion-acl.d
%config %class(preserve) %attr (0644, root, bin) %{_sysconfdir}/func/minion.conf
%config %class(preserve) %attr (0644, root, bin) %{_sysconfdir}/func/async_methods.conf
%dir %attr (0755, root, bin) %{_sysconfdir}/logrotate.d
%{_sysconfdir}/logrotate.d/*
%dir %attr (0755, root, bin) %{_sysconfdir}/func/modules
%{_sysconfdir}/func/modules/*
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, other) %{_localstatedir}/lib
%dir %attr (0755, root, bin) %{_localstatedir}/lib/func
%dir %attr (0755, root, sys) %{_localstatedir}/log
%dir %attr (0755, root, bin) %{_localstatedir}/log/func
%dir %attr (0755, root, bin) /lib
%dir %attr (0755, root, bin) /lib/svc
%dir %attr (0755, root, bin) /lib/svc/method
%attr (0755, root, bin) /lib/svc/method/svc-func
%dir %attr (0755, root, sys) %{_localstatedir}/svc
%dir %attr (0755, root, sys) %{_localstatedir}/svc/manifest
%dir %attr (0755, root, sys) %{_localstatedir}/svc/manifest/application
%class(manifest) %attr (0755, root, sys) %{_localstatedir}/svc/manifest/application/func.xml

%changelog
* Web May 06 2009 - moinakg@belenix.org
- Initial spec file.
