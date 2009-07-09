#
# spec file for package gtk-vnc
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#


Name:           gtk-vnc
License:        LGPL v2.1, MIT, MPL 1.1
Group:          Development/Libraries
Version:        0.3.8
Release:        1
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
URL:            http://gtk-vnc.sf.net/
Summary:        A GTK widget for VNC clients
Source:         http://download.gnome.org/sources/%{name}/0.3/%{name}-%{version}.tar.bz2
# date:2008-11-28 owner:fujiwara type:feature bugster:6777514 bugzilla:2354859
Patch1:         gtk-vnc-01-textdomain.diff
# date:2008-11-28 owner:fujiwara type:feature bugster:6777514 bugzilla:2354851
Patch2:         gtk-vnc-02-cp-utf8.diff
# date:2008-12-16 owner:halton type:bug bugzilla:564718
Patch3:         gtk-vnc-03-ff3.1.diff
BuildRoot:     %{_tmppath}/%{name}-%{version}-root

BuildRequires: gtk2-devel pygtk2-devel python-devel

%{?!pythonver:%define pythonver 2.4}

%description
gtk-vnc is a VNC viewer widget for GTK. It is built using coroutines
allowing it to be completely asynchronous while remaining single threaded.

%package devel
Summary: Libraries, includes, etc. to compile with the gtk-vnc library
Group: Development/Libraries
Requires: %{name} = %{version}
Requires: pkgconfig
Requires: pygtk2-devel gtk2-devel

%description devel
gtk-vnc is a VNC viewer widget for GTK. It is built using coroutines
allowing it to be completely asynchronous while remaining single threaded.

Libraries, includes, etc. to compile with the gtk-vnc library

%package python
Summary: Python bindings for the gtk-vnc library
Group: Development/Libraries
Requires: %{name} = %{version}

%description python
gtk-vnc is a VNC viewer widget for GTK. It is built using coroutines
allowing it to be completely asynchronous while remaining single threaded.

A module allowing use of the GTK-VNC widget from python

%prep
%setup -q
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

export PYTHON=/usr/bin/python%{pythonver}

libtoolize --force --force
intltoolize --automake -c -f
aclocal -I gnulib/m4
autoheader
automake --add-missing --copy
autoconf

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --mandir=%{_mandir} \
            --libdir=%{_libdir} \
            --datadir=%{_datadir} \
            --includedir=%{_includedir} \
            --sysconfdir=%{_sysconfdir} \
%if %debug_build
            --enable-debug=yes \
%endif
%if %with_brower_plugin
            --enable-plugin
%endif
	

make -j $CPUS

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

# move to vendor-packages
%if %with_64
cd $RPM_BUILD_ROOT%{_libdir}/..
mkdir -p python%{pythonver}/vendor-packages/64
mv python%{pythonver}/site-packages/* python%{pythonver}/vendor-packages/64
%else
cd $RPM_BUILD_ROOT%{_libdir}
mkdir -p python%{pythonver}/vendor-packages
mv python%{pythonver}/site-packages/* python%{pythonver}/vendor-packages/
%endif
rmdir python%{pythonver}/site-packages

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-, root, root)
%doc AUTHORS ChangeLog NEWS README COPYING.LIB
%{_libdir}/lib*.so.*

%files devel
%defattr(-, root, root)
%doc AUTHORS ChangeLog NEWS README COPYING.LIB
%doc examples/gvncviewer.c
%{_libdir}/lib*.so
%dir %{_includedir}/%{name}-1.0/
%{_includedir}/%{name}-1.0/*.h
%{_libdir}/pkgconfig/%{name}-1.0.pc

%files python
%defattr(-, root, root)
%doc AUTHORS ChangeLog NEWS README COPYING.LIB
%doc examples/gvncviewer.py
%{_libdir}/python*/site-packages/gtkvnc.so

%changelog
* Tue Dec 16 2008 - halton.huo@sun.com
- Add ff3.1.diff to fix the build issue when FF bumped to 3.1
* Thu Dec 11 2008 - halton.huo@sun.com
- Bump to 0.3.8
* Fri Nov 28 2008 - takao.fujiwara@sun.com
- Add patch textdomain.diff to support message i18n.
- Add patch cp-utf8.diff to copy multibyte chars.
* Wed Nov 26 2008 - halton.huo@sun.com
- use %{pythonver} macro to select which version of Python to build with
* Thu Nov 13 2008 - halton.huo@sun.com
- Moved from SFE
* Tue Sep 09 2008 - halton.huo@sun.com
- Bump to 0.3.7
* Tue May 06 2008 - nonsea@users.sourceforge.net
- Bump to 0.3.6
- Remove upsteamed patch solaris-ld-ast.diff
* Tue Apr 22 2008 - nonsea@users.sourceforge.net
- Bump to 0.3.5
* Fri Mar 07 2008 - nonsea@users.sourceforge.net
- Bump to 0.3.4
* Wed Feb 20 2008 - nonsea@users.sourceforge.net
- Bump to 0.3.3
- Remove upstreamed patch suncc-range-case.diff
* Thu Jan 10 2008 - nonsea@users.sourceforge.net
- Bump to 0.3.2
- Add patch suncc-range-case.diff to fix build issue.
* Fri Dec 14 2007 - nonsea@users.sourceforge.net
- Bump to 0.3.1
* Thu Dec 13 2007 - nonsea@users.sourceforge.net
- Bump to 0.3.0
- Remove upsreamed patches: makefile.diff, macro.diff,
  yield.diff and coroutine.diff
- Add new patch solaris-ld-ast.diff
* Tue Oct 30 2007 - nonsea@users.sourceforge.net
- Add debug option.
* Thu Oct 25 2007 - nonsea@users.sourceforge.net
- Initial version
