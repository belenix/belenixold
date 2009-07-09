#
# spec file for package SUNWgnome-ps-viewer
#
# includes module(s): <none>  (backcompat pkg with a symlink to evince)
#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: laca
#
%include Solaris.inc

Name:                    SUNWgnome-ps-viewer
Summary:                 GNOME PostScript document viewer (Obsolete)
Version:                 2.6.0
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWgnome-pdf-viewer

%install
mkdir -p $RPM_BUILD_ROOT%{_bindir}
cd $RPM_BUILD_ROOT%{_bindir}
ln -s evince ggv
# mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
# cd $RPM_BUILD_ROOT%{_mandir}/man1
# ln -s evince.1 ggv.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%changelog
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Tue Feb 28 2006 - laca@sun.com
- add backcompat spec file (make ggv a symlink to evince)
