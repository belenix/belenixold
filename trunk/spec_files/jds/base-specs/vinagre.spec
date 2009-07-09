#
# spec file for package vinagre
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#

Name:           vinagre
License:        GPL v2
Group:          Development/Libraries
Version:        2.26.1
Release:        1
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
URL:            http://www.gnome.org/projects/vinagre
Summary:        A VNC client for the GNOME Desktop
Source:         http://download.gnome.org/sources/%{name}/2.26/%{name}-%{version}.tar.bz2
# date:2008-11-28 owner:fujiwara type:feature bugster:6777514 bugzilla:562524
Patch1:         vinagre-01-cp-utf8.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-root

BuildRequires: gtk2-devel

%description
vinagre is  a VCN client for the GNOME Desktop

%prep
%setup -q
%patch1 -p1

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

libtoolize --force
aclocal $ACLOCAL_FLAGS -I .
autoheader
automake -a -c -f
autoconf

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --mandir=%{_mandir} \
            --libdir=%{_libdir} \
            --libexecdir=%{_libexecdir} \
            --datadir=%{_datadir} \
            --includedir=%{_includedir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-avahi=yes
	

make -j $CPUS

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-, root, root)
%doc AUTHORS ChangeLog NEWS README COPYING.LIB
%{_bindir}/*
%{_libdir}/lib*.so.*
%{_libdir}/bonobo/servers/GNOME_RemoteDesktop.server

%changelog
* Tue Apr 14 2009 - halton.huo@sun.com
- Bump to 2.26.1
* Tue Mar 17 2009 - dave.lin@sun.com
- Bump to 2.26.0
* Tue Mar 03 2009 - halton.huo@sun.com
- Bump to 2.25.92
* Tue Feb 17 2009 - halton.huo@sun.com
- Bump to 2.25.91
* Thu Feb 05 2009 - christian.kelly@sun.com
- Bump to 2.25.90.
* Tue Jan 22 2009 - halton.huo@sun.com
- Bump to 2.25.5
* Tue Jan 06 2009 - halton.huo@sun.com
- Bump to 2.25.4
* Tue Dec 23 2008 - halton.huo@sun.com
- Bump to 2.25.3
- Remove upstreamed patch setlocale.diff and reorder
* Thu Dec 11 2008 - halton.huo@sun.com
- Bump to 2.24.2
* Fri Nov 28 2008 - takao.fujiwara@sun.com
- Add patch setlocale.diff to to support locales.
- Add patch cp-utf8.diff to copy multibyte chars.
* Thu Nov 13 2008 - halton.huo@sun.com
- Moved from SFE
* Tue Sep 09 2008 - halton.huo@sun.com
- Bump to 2.23.92
* Tue Sep 02 2008 - halton.huo@sun.com
- Bump to 2.23.91
- Remove upstreamed patch libsocket.diff
* Wed Aug 20 2008 - nonsea@users.sourceforge.net
- Bump to 2.23.90
- Add patch libsocket.diff to fix bugzilla #548585
* Tue Mar 10 2008 - nonsea@users.sourceforge.net
- Bump to 0.5.0
* Tue Mar 04 2008 - nonsea@users.sourceforge.net
- Bump to 0.4.92
- Remove upstreamed patch gthread.diff
* Wed Feb 20 2008 - nonsea@users.sourceforge.net
- Bump to 0.4.91
- Remove upstreamed patch wall.diff
- Add new patch gthread.diff to fix bugzilla #517603.
* Thu Dec 13 2007 - nonsea@users.sourceforge.net
- Bump to 0.4
- Add patch wall.diff to fix build problem on Solaris.
* Fri Nov 30 2007 - nonsea@users.sourceforge.net
- Initial version
