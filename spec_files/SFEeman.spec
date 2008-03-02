#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#

%include Solaris.inc

Name:                SFEeman
License:             CDDL
Summary:             A small shell script wrapper to generate more readable man pages.
Version:             0.1
Source:              eman-%{version}.tar.gz
URL:                 http://blogs.sun.com/timc/date/20051108
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWTk

%prep
%setup -q -n eman

%build
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*

%changelog
* Sat Mar 01 2008 - moinakg@gmail.com
- Initial spec.
