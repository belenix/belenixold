#
# spec file for package SUNWcups-manager
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: gheet
#

%include Solaris.inc 
%define pythonver 2.6

%use scp = system-config-printer.spec

Name:                    SUNWcups-manager
License:  		 GPL v2
Summary:                 Print Manager for CUPS
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                SUNWPython
Requires:                SFEcups
BuildRequires:           SUNWgnome-desktop-prefs
BuildRequires:           SFEcups-devel

%include default-depend.inc

%package root
Summary:		 %{summary} - / filesystem
SUNW_BaseDir:		 /
%include default-depend.inc
Requires: SUNWPython

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
rm -rf %name-%version
mkdir -p %name-%version
%scp.prep -d %name-%version

%build
export PYTHON=python%{pythonver}
%scp.build -d %name-%version

%install
export PYTHON=python%{pythonver}
%scp.install -d %name-%version

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/%{scp.name}/icons/*
%{_datadir}/%{scp.name}/*.glade
%doc -d %scp.name-%{scp.version} AUTHORS README NEWS
%doc(bzip2) -d %scp.name-%{scp.version} COPYING ChangeLog
%dir %attr (0755, root, other) %{_datadir}/doc

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%attr(0755, root, bin) %dir %{_sysconfdir}/dbus-1
%attr(0755, root, bin) %dir %{_sysconfdir}/dbus-1/system.d
%{_sysconfdir}/dbus-1/system.d/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Tue Dec 09 2008 - takao.fujiwara@sun.com
- Add l10n package.
* Thu Dec 04 2008 - dave.lin@sun.com
- Add BuildRequires on SUNWgnome-desktop-prefs(desktop-file-install)
* Tues Nov 18 2008 - ghee.teo@sun.com
- Initial version.
