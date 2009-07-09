#
# spec file for package SUNWgtkperf
#
# includes module(s): gtkperf
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: dermot
#
%include Solaris.inc

%use gtkperf = gtkperf.spec

Name:                    SUNWgtkperf
Summary:                 Gtk+ performance testing application
Version:                 %{gtkperf.version}
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-base-libs
Requires: SUNWlibms
Requires: SUNWmlib
BuildRequires: SUNWgnome-base-libs-devel

%prep
rm -rf %name-%version
mkdir %name-%version
%gtkperf.prep -d %name-%version

%build
%gtkperf.build -d %name-%version

%install
%gtkperf.install -d %name-%version
# Delete the unneeded README/COPYING etc files.
rm -rf $RPM_BUILD_ROOT%{_prefix}/doc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*


%changelog
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Mon Feb 20 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Mon Oct 21 2005 - damien.carbery@sun.com
- Initial spec file created.
