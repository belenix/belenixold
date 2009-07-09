#
# spec file for package SUNWjdsver
#
# includes module(s): SunDesktopVersion
#
# Copyright (c) 2004 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: dermot
#
%include Solaris.inc

%use jdsver = SunDesktopVersion.spec

Name:                    SUNWjdsver
Summary:                 Version info for the Java Desktop System
# Note: increment the micro version in case of a respin.
#       New builds should start with a 0
Version:                 %{jdsver.prodRelMajor}.%{jdsver.prodBuild}.1
SUNW_Category: 		 JDS,system,%{jds_version}
SUNW_BaseDir:            /
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWjdsrm

%prep
rm -rf %name-%version
mkdir %name-%version
%jdsver.prep -d %name-%version

%build
%jdsver.build

%install
%jdsver.install

rm -f $RPM_BUILD_ROOT%{_sysconfdir}/sun-release

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/product-info

%changelog
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Wed Jun 15 2005 - laca@sun.com
- call the %build section of the linux spec file
* Tue Nov 05 2004 - shirley.woo@sun.com
- Bug 4810847 & 6185753: Added Requires SUNWjdsrm to removing previous 
  non-standard version pkg
* Tue Aug 17 2004 - laca@sun.com
- updated CATEGORY and fixed version string to avoid using alpha
* Mon Aug 16 2004 - dermot.mccluskey@sun.com
- changed root from /etc to /
