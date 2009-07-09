#
# spec file for package libproxy
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: wangke
# bugdb: http://code.google.com/p/libproxy/issues/detail?id=
#

%define pythonver 2.6

%if %opt_arch64
%define _demodir %{_prefix}/demo/jds/bin/%{_arch64}
%else
%define _demodir %{_prefix}/demo/jds/bin
%endif

Name:         libproxy
License:      LGPL v2.1
Group:        System/Libraries/GNOME
Version:      0.2.3
Release:      1
URL:          http://code.google.com/p/libproxy/
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Libproxy is a library that provides automatic proxy configuration management
Source:       http://libproxy.googlecode.com/files/libproxy-%{version}.tar.gz
#owner:wangke date:2009-02-02 type:branding
Patch1:       libproxy-01-orig-build.diff
#owner:wangke date:2009-02-11 type:branding
Patch2:       libproxy-02-wpad-fallback.diff
#owner:fujiwara date:2009-02-13 type:bug bugid:29
Patch3:       libproxy-03-proxy-readline.diff
#owner:wangke date:2009-03-10 type:branding
Patch5:       libproxy-05-config-posix.diff
BuildRoot:    %{_tmppath}/%{name}-%{version}-build

%package devel
Summary:      %{summary} - development files	
Requires:     %{name} = %{version}

%prep
%setup -q -n %{name}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch5 -p1

%build
aclocal
autoconf
automake -a -c -f
CFLAGS="%optflags"
LDFLAGS="%{_ldflags}"
./configure --prefix=%{_prefix}			 \
	    --libdir=%{_libdir}			 \
	    --bindir=%{_bindir}			 \
            --includedir=%{_includedir}/libproxy \
            --sysconfdir=%{_sysconfdir}		 \
	    --mandir=%{_mandir}			 \
	    --libexecdir=%{_libexecdir}		 \
            --without-kde	
make

%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

install -d $RPM_BUILD_ROOT%{_demodir}
mv $RPM_BUILD_ROOT%{_bindir}/* $RPM_BUILD_ROOT%{_demodir}
rm -r $RPM_BUILD_ROOT%{_bindir}

find $RPM_BUILD_ROOT%{_libdir} -type d -name "python*" -prune -exec mv {} $RPM_BUILD_ROOT%{_libdir}/python%{pythonver} ';'
if [ -x $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages ]; then
	mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages \
	   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
fi

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Mar 11 2009 - ke.wang@sun.com
- Mended bugdb
- Remove patch4 because the problem is fixed in Python26
* Tue Mar 10 2009 - ke.wang@sun.com
- Add patch5 to replace _GUN_SOURCE with _POSIX_C_SOURCE
* Mon Feb 23 2009 - ke.wang@sun.com
- make wpad-fallback be built by default, but not be check against
  user can use PX_CONFIG_ORDER to enable it
* Mon Feb 16 2009 - ke.wang@sun.com
- Add patch libproxy-04-py-find-lib.diff for python binding
* Fri Feb 13 2009 - takao.fujiwara@sun.com
- Add patch proxy-readline.diff to work proxy demo correctly.
* Mon Feb 2, 2009 - ke.wang@sun.com
- Initial spec.
