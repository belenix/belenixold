#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#

%include Solaris.inc

Name:                SFEmount-ext2fs
License:             GPL
Summary:             An userland NFS server to mount ext2 filesystems.
Version:             0.1
Source:              mount-ext2fs-%{version}.tar.gz
URL:                 http://www.belenix.org/
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:            SFEe2fsprogs
BuildRequires:       SFEe2fsprogs-devel
Requires:            SFEprtpart

%prep
%setup -q -n mount_ext2fs

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
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, sys) %{_libdir}/fs
%dir %attr (0755, root, sys) %{_libdir}/fs/ext2fs
%{_libdir}/fs/ext2fs/*

%changelog
* Sat Mar 01 2008 - moinakg@gmail.com
- Initial spec.
