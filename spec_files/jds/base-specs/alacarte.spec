#
# spec file for package gnome-menu-editor
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jedy
#
%include l10n.inc
%define python_version 2.4

Name:         alacarte
Version:      0.11.10
Release:      1
Summary:      Simple menu editor for GNOME
Group:        System/GUI/GNOME
License:      GPL
URL:          http://www.realistanew.com/projects/alacarte/
Distribution: java-desktop-system
Vendor:       Sun Microsystems, Inc.
Source:       http://ftp.gnome.org/pub/GNOME/sources/alacarte/0.11/alacarte-%{version}.tar.bz2
%if %build_l10n
Source1:      l10n-configure.sh
Source2:      %{name}-po-sun-%{po_sun_version}.tar.bz2
%endif
#owner:jedy date:2008-07-14 type:branding
Patch1:       alacarte-01-menu-entry.diff

BuildRoot:    %{_tmppath}/%{name}-%{version}-build

BuildRequires:  pygtk2.0-devel
BuildRequires: 	desktop-file-utils
BuildRequires:  gnome-menus-devel >= 2.15.4.1
BuildRequires:  perl-XML-Parser
Requires: 	pygtk2.0, gnome-python-gconf, gnome-python
Requires: 	python-gnome-menus
Obsoletes:      smeg
Provides:       smeg %{version}-%{release}

%description
Alacarte is a menu editor for GNOME that lets you get things done,
simply and quickly.

Just click and type to edit, add, and delete any menu entry.

%prep
%setup -q
%if %build_l10n
bzcat %SOURCE2 | tar xf -
cd po-sun; make; cd ..
%endif

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

intltoolize -c -f --automake

%if %build_l10n
bash -x %SOURCE1 --enable-copyright
%endif

libtoolize --copy --force
aclocal $ACLOCAL_FLAGS
automake -a -c -f 
autoconf

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}
make -j $CPUS \
    pyexecdir=%{_libdir}/python%{python_version}/vendor-packages \
    pythondir=%{_libdir}/python%{python_version}/vendor-packages

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install \
    pyexecdir=%{_libdir}/python%{python_version}/vendor-packages \
    pythondir=%{_libdir}/python%{python_version}/vendor-packages
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.pyo" -exec rm -f {} ';'

%post
%update_menus
%update_icon_cache hicolor

%postun
%clean_menus
%clean_icon_cache hicolor

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr (-, root, root)
%doc README AUTHORS COPYING
%{_libdir}/python?.?/vendor-packages/*
%{_bindir}/*
%{_datadir}/applications/*
%{_datadir}/%name/*
%{_datadir}/icons/*
%{_libdir}/menu/%{name}

%changelog
* Wed Mar 18 2009 - dave.lin@sun.com
- Bump to 0.11.10
* Tue Feb 17 2009 - dave.lin@sun.com
- Bump to 0.11.9
* Mon Feb 16 2009 - dave.lin@sun.com
- Bump to 0.11.8
* Wed Oct 01 2008 - takao.fujiwara@sun.com
- Add l10n tarball.
* Tue Sep 23 2008 - christian.kelly@sun.com
- Bump to 0.11.6.
* Fri Aug 22 2008 - jedy.wang@sun.com
- rename desktop.diff to menu-entry.diff.
* Mon Jul 14 2008 - jedy.wang@sun.com
- Add 01-desktop.diff.
* Tue Mar 11 2008 - damien.carbery@sun.com
- Bump to 0.11.5.
* Mon Feb 18 2008 - damien.carbery@sun.com
- Bump to 0.11.4.
* Fri Nov 09 2007 - jedy.wang@sun.com
* Remove 01-force-reload.diff.
* Thu Oct 12 2007 - jedy.wang@sun.com
- Take the ownership from harrylu.
* Wed Oct 10 2007 - damien.carbery@sun.com
- Don't delete *.pyc files - they are needed.
* Fri Aug 17 2007 - jedy.wang@sun.com
- Fix 'patch1 -p0' - change to -p1 and change patch file too.
* Tue Feb 13 2007 - damien.carbery@sun.com
- Bump to 0.11.3.
* Thu Jan 11 2007 - damien.carbery@sun.com
- Bump to 0.11.1.1.
* Tue Jan 09 2007 - damien.carbery@sun.com
- Bump to 0.11.0.
* Tue Dec 19 2006 - damien.carbery@sun.com
- Bump to 0.10.2. Remove upstream patches, 02-launch-menu-item and
  03-g11n-i18n-ui.
* Tue Dec 12 2006 - takao.fujiwara@sun.com
- Added intltoollize to read LINGUAS file
- Added alacarte-03-g11n-i18n-ui.diff
* Fri Nov 17 2006 - damien.carbery@sun.com
- Change patch2 to use p1.
* Wed Nov 15 2006 - calum.benson@sun.com
  Change menu item to match latest UI spec.
* Tue Oct 03 2006 - damien.carbery@sun.com
- Bump to 0.10.0.
* Mon Sep 04 2006 - damien.carbery@sun.com
- Bump to 0.10.0.
* Thu Aug 24 2006 - laca@sun.com
- remove autoheader call since there is AC_CONFIG_HEADER in configure.in
* Tue Aug 22 2006 - halton.huo@sun.com
- Divide SFEgnome-menu-editor.spec into alacarte.spec
  and SUNWgnome-menu-editor.spec
* Wed Aug 16 2006 - harry.lu@sun.com
- bump up to 0.9.90 and add patch alacarte-01-force-reload.diff to make
  it work on solaris.
* Wed Jul  5 2006 - laca@sun.com
- rename to gnome-menu-editor
- delete share subpkg
* Fri Apr 21 2006 - glynn.foster@sun.com
- Initial spec file
