#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#

%include Solaris.inc

Name:                SFEprtpart
License:             CDDL
Summary:             An utility to dump the partition table of a disk/disk image.
Version:             0.1
Source:              prtpart-%{version}.tar.gz
URL:                 http://www.belenix.org/
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n prtpart

%build
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%changelog
* Sat Mar 01 2008 - moinakg@gmail.com
- Initial spec.
