#
# spec file for package libvisual.spec
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jerrytan 
# bugdb: http://sourceforge.net/tracker/index.php?func=detail&group_id=106542&atid=644748&aid=

Name:                   libvisual
License:		LGPL v2.1
Summary:                Libvisual provides a convenient API for writing visualization plugins
Version:                0.4.0
URL:                    http://localhost.nl/~synap/libvisual-wiki/index.php/Main_Page
Source:                 http://downloads.sourceforge.net/libvisual/libvisual-%{version}.tar.bz2
# date:2008-11-25 owner:jerrytan type:bug bugid:2342323
Patch1:                 libvisual-01-solaris.diff
# date:2008-11-25 owner:jerrytan type:branding 
Patch2:			libvisual-02-compiler.diff
# date:2008-12-07 owner:jerrytan type:feature bugster:6788530
Patch3:			libvisual-03-map.diff

%package devel
Summary:        %{summary} - development files
Requires: %name
Requires: SUNWgnome-common-devel

%prep
%setup -q -n libvisual-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%ifos linux
if [ -x /usr/bin/getconf ]; then
  CPUS=`getconf _NPROCESSORS_ONLN`
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

./configure --prefix=%{_prefix}		\
	    --mandir=%{_mandir}		\
            --datadir=%{_datadir}	\
            --sysconfdir=%{_sysconfdir} \
            --enable-shared=yes		\
	    --enable-static=no


make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT/%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, other)  %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Tue Nov 25 2008 - jim.li@sun.com
- add license tag
- rename SFElibvisual to libvisual
- use sun compiler 12 instead of gcc
* Sun Jun 29 2008 - river@wikimedia.org
- force /usr/sfw/bin/gcc, use gcc cflags instead of studio
* Thu Jan 24 2008 - moinak.ghosh@sun.com
- Initial spec.
