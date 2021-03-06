#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%define tarball_version 1.6.9p15

Name:                %{pkg_prefix}sudo
Summary:             Provides limited super user privs to specific users
Version:             1.6.9
Source:              http://www.courtesan.com/sudo/dist/sudo-%{tarball_version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: %{name}-root

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -n sudo-%{tarball_version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
            --libexecdir=%{_libexecdir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1m
%{_mandir}/man1m/*
%dir %attr (0755, root, bin) %{_mandir}/man4
%{_mandir}/man4/*

%files root
%defattr (-, root, root)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/sudoers

%changelog
* Sun Apr 27 2008 - Shivakumar GN <shivakumar.gn@gmail.com>
- Bumped from 1.6.9p12 to 1.6.9p15
- 1.6.9p12 had vanished from the hosted location. Time to have our own source hosting!
- removal of {_libdir}/*.la under %install failed since *.la didn't exist. Fixed it with rm -f option.
* Mon Apr 07 2008 - moinakg@gmail.com
- Fix perms for /etc/sudoers.
* Wed Feb 06 2008 - Ananth Shrinivas <ananth@sun.com>
- updated to sudo 1.6.9p12
* Sat Dec 15 2007 - Ananth Shrinivas <ananth@sun.com>
- updated to sudo 1.6.9p9
* Mon Sep 03 2007 - Ananth Shrinivas <ananth@sun.com>
- updated to new sudo version
* Thu Nov 09 2006 - Eric Boutilier
- Initial spec
