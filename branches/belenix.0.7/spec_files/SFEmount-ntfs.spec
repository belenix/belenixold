#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#

%include Solaris.inc

Name:                SFEmount-ntfs
License:             GPL
Summary:             An userland NFS server to mount ntfs filesystems.
Version:             0.1
Source:              mount-ntfs-%{version}.tar.gz
URL:                 http://www.belenix.org/
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:            SFEntfsprogs
BuildRequires:       SFEntfsprogs-devel
Requires:            SFEmount-ext2fs
Requires:            SFEprtpart

%prep
%setup -q -n mount_ntfs

%build

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
make

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, sys) %{_libdir}/fs
%dir %attr (0755, root, sys) %{_libdir}/fs/ntfs
%{_libdir}/fs/ntfs/*

%changelog
* Sat Mar 01 2008 - moinakg@gmail.com
- Initial spec.
