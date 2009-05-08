#
# spec file for package func
#
# includes module(s): Func
#
%include Solaris.inc

Name:                    func
Summary:                 Fedora Unified Network Controller
Version:                 0.24
Source:                  http://people.fedoraproject.org/~alikins/files/func/func-%{version}.tar.gz
Source1:                 func.xml
Source2:                 func.sh
Source3:                 mydbm.py
Source4:                 http://www.belenix.org/binfiles/func-opensolaris-modules-0.1.tar.gz
Source5:                 func-initchk.sh
Source6:                 func.README.opensolaris
Source7:                 func-secdbmodule.c
Patch1:                  func-01-dbm.diff
Patch2:                  func-02-setup.py.diff
Patch3:                  func-03-command.py.diff
URL:                     https://fedorahosted.org/func/

SUNW_BaseDir:            /
License:                 GPL2
SUNW_Copyright:          LICENSE.GPL
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                SUNWPython25
Requires:                SUNWpython25-pyopenssl
Requires:                certmaster
BuildRequires:           SUNWPython25-devel


%prep
%setup -q -c -n %{name}-%version
cd func-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
cp %{SOURCE3} func/
(cd func/minion/modules
 gunzip -c %{SOURCE4} | tar xf -)
cp %{SOURCE7} func/secdbmodule.c

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
chmod -R a+r ${RPM_BUILD_ROOT}%{_sysconfdir}/func

mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/func
cp %{SOURCE5} ${RPM_BUILD_ROOT}%{_libdir}/func/func-initchk
chmod a+x ${RPM_BUILD_ROOT}%{_libdir}/func/func-initchk

mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/doc/func
cp README ${RPM_BUILD_ROOT}%{_datadir}/doc/func
cp %{SOURCE6} ${RPM_BUILD_ROOT}%{_datadir}/doc/func/README.opensolaris

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
%dir %attr (0755, root, bin) %{_libdir}/func
%{_libdir}/func/func-initchk
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
%dir %attr (0777, root, bin) %{_localstatedir}/lib/func
%dir %attr (0755, root, sys) %{_localstatedir}/log
%dir %attr (0777, root, bin) %{_localstatedir}/log/func
%dir %attr (0755, root, bin) /lib
%dir %attr (0755, root, bin) /lib/svc
%dir %attr (0755, root, bin) /lib/svc/method
%attr (0755, root, bin) /lib/svc/method/svc-func
%dir %attr (0755, root, sys) %{_localstatedir}/svc
%dir %attr (0755, root, sys) %{_localstatedir}/svc/manifest
%dir %attr (0755, root, sys) %{_localstatedir}/svc/manifest/application
%class(manifest) %attr (0755, root, sys) %{_localstatedir}/svc/manifest/application/func.xml

%defattr (-, root, other)
%dir %attr(0755, root, other) %{_datadir}/doc
%dir %attr(0755, root, other) %{_datadir}/doc/func
%doc %{_datadir}/doc/func/*

%changelog
* Fri May 08 2009 - moinakg@belenix.org
- Updated startup scripts and add Solaris functionality.
- Renamed package and multitude of fixes.
* Web May 06 2009 - moinakg@belenix.org
- Initial spec file.
