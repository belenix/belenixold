#
# spec file for package SUNWgnome-devel-docs
#
# includes module(s): GNOME Devel Docs
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: davelam
#
#
%include Solaris.inc

%use gdd = gnome-devel-docs.spec

Name:               SUNWgnome-devel-docs
Summary:            GNOME developer documentation
Version:            %{default_pkg_version}
SUNW_BaseDir:       %{_basedir}
SUNW_Copyright:     %{name}.copyright
BuildRoot:          %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWlxml-python
BuildRequires: SUNWlxsl
BuildRequires: SUNWgnome-libs
Requires: SUNWgnome-help-viewer
Requires: SUNWgnome-libs

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
rm -rf %name-%version
mkdir %name-%version
%gdd.prep -d %name-%version

%build
export PKG_CONFIG_PATH=%{_pkg_config_path}
export MSGFMT="/usr/bin/msgfmt"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export LDFLAGS="%_ldflags"
export CFLAGS="%optflags"
%gdd.build -d %name-%version

%install
%gdd.install -d %name-%version

%if %build_l10n
%else
# REMOVE l10n FILES
rm -r $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/[a-z]*
rm -r $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z][a-z].omf
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

# Remove scrollkeeper files before packaging.
rm -rf $RPM_BUILD_ROOT/var

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/*/C
%{_datadir}/omf/*/*-C.omf

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/*/[a-z]*
%{_datadir}/omf/*/*-[a-z][a-z].omf
%{_datadir}/omf/*/*-[a-z][a-z]_[A-Z]*.omf
%endif

%changelog
* Fri Apr  3 2009 - laca@sun.com
- stop using postrun
* Tue Mar 17 2009 - dave.lin@sun.conm
- Uncomment %{_datadir}/omf/*/*-[a-z][a-z]_[A-Z]*.omf in %file l10n.
* Mon Sep 10 2007 - Damien Carbery <damien.carbery@sun.com>
- Update dependencies.
* Sat Sep 01 2007 - Dave Lin <dave.lin@sun.com>
- initial version

