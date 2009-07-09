#
# spec file for package orca
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: dcarbery
#
%include l10n.inc
Name:           orca
License:        LGPL
Group:          System/Library
Version:        2.26.0
Release:        1
Distribution:   Java Desktop System
Vendor:	        Sun Microsystems, Inc.
Summary:        Orca Screen Reader/Magnifier
Source:         http://ftp.gnome.org/pub/GNOME/sources/orca/2.26/orca-%{version}.tar.bz2
%if %build_l10n
Source1:        l10n-configure.sh
Source2:        %{name}-po-sun-%{po_sun_version}.tar.bz2
%endif
# owner:jedy date:2008-08-21 type:branding
Patch1:         orca-01-menu-entry.diff
URL:            http://www.gnome.org
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Docdir:         %{_defaultdocdir}/doc
Autoreqprov:    on

%define python_version 2.4
%define pyorbit_version 2.0.1
%define pygtk2_version 2.6.2
%define gnome_python_version 2.6.2
%define brltty_version 3.6.1

Requires: pygtk2 >= %{pygtk2_version}
Requires: pyorbit >= %{pyorbit_version}
Requires: gnome-python >= %{gnome_python_version}
Requires: brltty >= %{brltty_version}

BuildRequires: pygtk2-devel >= %{pygtk2_version}
BuildRequires: pyorbit-devel >= %{pyorbit_version}
BuildRequires: gnome-python-devel >= %{gnome_python_version}

%description
Orca a scriptable screen reader/magnifier that is under development.
As such it is highly unstable and undergoes frequent changes.
To read more about Orca, please refer to the "Programmer's Guide" in
the docs/programmers-guide directory.

%prep
%setup -q -n orca-%{version}
%if %build_l10n
bzcat %SOURCE2 | tar xf -
cd po-sun; make; cd ..
%endif

%patch1 -p1

%build
libtoolize --force
intltoolize -c -f --automake

%if %build_l10n
bash -x %SOURCE1 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS -I .
autoconf
autoheader
automake -a -c -f
CFLAGS="$RPM_OPT_FLAGS"                         \
./configure     --prefix=%{_prefix}             \
                --libdir=%{_libdir}             \
                --bindir=%{_bindir}             \
                --datadir=%{_datadir}           \
                --sysconfdir=%{_sysconfdir}

# FIXME: hack: stop the build from looping
touch po/stamp-it

make \
    pyexecdir=%{_libdir}/python%{python_version}/vendor-packages \
    pythondir=%{_libdir}/python%{python_version}/vendor-packages

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install \
    pyexecdir=%{_libdir}/python%{python_version}/vendor-packages \
    pythondir=%{_libdir}/python%{python_version}/vendor-packages
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.pyo" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%post

%postun

%files
%defattr(-, root, root)
%{_libdir}/python?.?/vendor-packages/orca
%{_bindir}/orca
%{_bindir}/orca-setup
%{_datadir}/locale

%doc AUTHORS NEWS README ChangeLog

%changelog
* Tue Mar 17 2009 - dave.lin@sun.com
- Bump to 2.26.0
* Fri Mar 06 2009 - li.yuan@sun.com
- Bump to 2.25.92.
* Tue Feb 17 2009 - dave.lin@sun.com
- Bump to 2.25.91
* Thu Feb 05 2009 - christian.kelly@sun.com
- Bump to 2.25.90.
* Wed Dec 03 2008 - dave.lin@sun.com
- Bump to 2.25.2
* Wed Oct 01 2008 - takao.fujiwara@sun.com
- Add l10n tarball.
* Mon Sep 29 2008 - brian.cameron@sun.com
- Bump to 2.24.0.
* Tue Sep 09 2008 - christian.kelly@sun.com
- Bump to 2.23.92.
* Tue Sep 02 2008 - christian.kelly@sun.com
- Bump to 2.23.91.
* Thu Aug 21 2008 - jedy.wang@sun.com
- add 01-menu-entry.diff
* Tue Aug 19 2008 - dave.lin@sun.com
- Bump to 2.23.90
* Tue Aug 05 2008 - damien.carbery@sun.com
- Bump to 2.23.6.
* Tue Jul 22 2008 - damien.carbery@sun.com
- Bump to 2.23.5.
* Tue Jun 17 2008 - damien.carbery@sun.com
- Bump to 2.23.4.
* Tue Jun 03 2008 - damien.carbery@sun.com
- Bump to 2.23.3.
* Wed May 28 2008 - damien.carbery@sun.com
- Bump to 2.23.2.
* Tue May 27 2008 - li.yuan@sun.com
- Bump to 2.22.2 and remove patch #1.
* Fri May 16 2008 - li.yuan@sun.com
- Updated patch info.
* Thu May 08 2008 - li.yuan@sun.com
- Fixed 6699122. Do not read password in login window.
* Wed Apr 09 2008 - damien.carbery@sun.com
- Bump to 2.22.1.
* Mon Mar 10 2008 - damien.carbery@sun.com
- Bump to 2.22.0.
* Tue Feb 26 2008 - damien.carbery@sun.com
- Bump to 2.21.92.
* Tue Feb 12 2008 - damien.carbery@sun.com
- Bump to 2.21.91.
* Tue Jan 29 2008 - damien.carbery@sun.com
- Bump to 2.21.90.
* Thu Jan 17 2008 - damien.carbery@sun.com
- Bump to 2.21.5.
* Tue Dec 18 2007 - damien.carbery@sun.com
- Bump to 2.21.4.
* Tue Dec 04 2007 - damien.carbery@sun.com
- Bump to 2.21.3.
* Tue Nov 13 2007 - damien.carbery@sun.com
- Bump to 2.21.2.
* Tue Oct 30 2007 - damien.carbery@sun.com
- Bump to 2.21.1.
* Tue Oct 30 2007 - damien.carbery@sun.com
- Bump to 2.20.1.
* Mon Oct 08 2007 - damien.carbery@sun.com
- Bump to 2.20.0.1.
* Wed Sep 19 2007 - damien.carbery@sun.com
- Bump to 2.20.0.
* Mon Sep 03 2007 - damien.carbery@sun.com
- Bump to 2.19.92.
* Mon Aug 27 2007 - damien.carbery@sun.com
- Bump to 2.19.91.
* Wed Aug 15 2007 - damien.carbery@sun.com
- Bump to 2.19.90.
* Mon Jul 30 2007 - damien.carbery@sun.com
- Bump to 2.19.6.
* Mon Jul 09 2007 - damien.carbery@sun.com
- Bump to 2.19.5.
* Mon Jun 18 2007 - damien.carbery@sun.com
- Bump to 2.19.4.
* Wed Jun 06 2007 - damien.carbery@sun.com
- Bump to 2.19.3.
* Mon May 14 2007 - damien.carbery@sun.com
- Bump to 2.19.2.
* Thu May 10 2007 - damien.carbery@sun.com
- Bump to 2.19.1.
* Thu Apr 12 2007 - damien.carbery@sun.com
- Bump to 2.18.1.
* Tue Mar 13 2007 - damien.carbery@sun.com
- Bump to 2.18.0.
* Mon Mar 05 2007 - damien.carbery@sun.com
- Bump to 2.17.92.
* Tue Jan 13 2007 - damien.carbery@sun.com
- Bump to 2.17.91.
* Mon Jan 22 2007 - damien.carbery@sun.com
- Bump to 2.17.90.
* Mon Jan 08 2007 - damien.carbery@sun.com
- Bump to 2.17.5.
* Mon Dec 18 2006 - damien.carbery@sun.com
- Bump to 2.17.4. Remove upstream patch orca-01-g11n-i18n-ui.diff.
* Tue Dec 12 2006 - takao.fujiwara@sun.com
- Added intltoolize to read LINGUAS file.
- Add orca-01-g11n-i18n-ui.diff to localize UI. Fixes 6499543.
* Tue Dec 04 2006 - damien.carbery@sun.com
- Bump to 2.17.3.
* Thu Nov 23 2006 - damien.carbery@sun.com
- Bump to 2.17.2.
* Mon Sep 04 2006 - damien.carbery@sun.com
- Bump to 1.0.0.
* Tue Aug 21 2006 - damien.carbery@sun.com
- Bump to 0.9.0.
* Tue Aug 08 2006 - damien.carbery@sun.com
- Bump to 0.2.8.
* Mon Jul 24 2006 - damien.carbery@sun.com
- Bump to 0.2.7.
* Wed Jul 12 2006 - william.walker@sun.com
- Update to 0.2.6
* Wed Jun 14 2006 - william.walker@sun.com
- Update to 0.2.5
* Tue May 02 2006 - damien.carbery@sun.com
- Remove unneeded intltoolize call.
* Sat Mar 18 2006 - damien.carbery@sun.com
- Bump to 0.2.2.
* Thu Feb 23 2006 - damien.carbery@sun.com
- Use bzip source tarball. It's smaller.
* Thu Feb 23 2006 - william.walker@sun.com
- Update to orca-0.2.1
* Tue Feb 14 2006 - damien.carbery@sun.com
- Add hack to fix infinite loop problem in po/Makefile.
* Wed Nov 30 2005 - william.walker@sun.com
- Update to orca-0.2.0
* Thu Oct 27 2005 - laca@sun.com
- move from site-packages to vendor-packages
* Thu Sep 15 2005 - laca@sun.com
- autotoolize
- add patch bindir.diff
* Mon Aug 15 2005 - rich.burridge@sun.com
- Initial Sun release
