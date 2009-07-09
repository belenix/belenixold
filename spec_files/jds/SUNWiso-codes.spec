#
# # spec file for package SUNWiso-codes.spec
#
# includes module(s): iso-codes
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: laca
#
%include Solaris.inc

%use iso_codes = iso-codes.spec

Name:                    SUNWiso-codes
Summary:                 ISO code lists and translations
Version:                 %{iso_codes.version}
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWPython

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SUNWiso-codes

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
%iso_codes.prep -d %name-%version

%build
%iso_codes.build -d %name-%version

%install
%iso_codes.install -d %name-%version

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/iso-codes
%{_datadir}/xml/iso-codes

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/pkgconfig
%{_datadir}/pkgconfig/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Mon Feb  5 2007 - laca@sun.com
- add Python dependency
* Sun Jan 21 2007 - laca@sun.com
- update %files for version 1.0
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
- Fri Jun  9 2006 - laca@sun.com
- separate the l10n stuff, fixes CR 6436771
* Thu Sep 15 2005 - laca@sun.com
- created
