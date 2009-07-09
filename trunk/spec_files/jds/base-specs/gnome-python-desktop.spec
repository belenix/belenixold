#
# spec file for package gnome-python-desktop
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: laca
#
Name:			gnome-python-desktop
License:		GPL
Group:			System/Library
Version:		2.26.0
Release:		1
Distribution:		Java Desktop System
Vendor:			Sun Microsystems, Inc.
Summary:		Python bindings for various GNOME desktop libraries
Source:			http://ftp.gnome.org/pub/GNOME/sources/%{name}/2.26/%{name}-%{version}.tar.bz2
URL:			http://www.gnome.org
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
Docdir:			%{_defaultdocdir}/doc
Autoreqprov:		on

%define python_version		   2.4
%define pygtk2_version             2.4.0
%define gnome_python_version       2.10.0
%define gnome_panel_version        2.13.4
%define libgnomeprint_version      2.2.0
%define libgnomeprintui_version    2.2.0
%define gtksourceview_version      1.1.90
%define libwnck_version            2.9.92
%define libgtop_version            2.13.0
%define nautilus_cd_burner_version 2.11.1
%define gconf_version              2.10.0
%define metacity_version           2.13.3

Requires: pygtk2 >= %{pygtk2_version}
Requires: gnome-python >= %{gnome_python_version}
Requires: gnome-panel >= %{gnome_panel_version}
Requires: libgnomeprint >= %{libgnomeprint_version}
Requires: libgnomeprintui >= %{libgnomeprintui_version}
Requires: gtksourceview >= %{gtksourceview_version}
Requires: libwnck >= %{libwnck_version}
Requires: libgtop >= %{libgtop_version}
Requires: nautilus-cd-burner >= %{nautilus_cd_burner_version}
Requires: GConf >= %{gconf_version}
Requires: metacity >= %{metacity_version}

BuildRequires: pygtk2-devel >= %{pygtk2_version}
BuildRequires: gnome-python-devel >= %{gnome_python_version}
BuildRequires: gnome-panel-devel >= %{gnome_panel_version}
BuildRequires: libgnomeprint-devel >= %{libgnomeprint_version}
BuildRequires: libgnomeprintui-devel >= %{libgnomeprintui_version}
BuildRequires: gtksourceview-devel >= %{gtksourceview_version}
BuildRequires: libwnck-devel >= %{libwnck_version}
BuildRequires: libgtop-devel >= %{libgtop_version}
BuildRequires: nautilus-cd-burner >= %{nautilus_cd_burner_version}
BuildRequires: GConf-devel >= %{gconf_version}
BuildRequires: metacity >= %{metacity_version}

%description
GNOME-Python provides the Python language bindings for the GNOME desktop libraries.

%package devel
Summary: Files needed to build applications using the Python bindings for GNOME desktop libraries
Group: Development/Languages
Requires: %{name} = %{version}

%description devel
This package contains files required to build Python applications that need 
to interoperate with the various GNOME desktop libraries

%prep
%setup -q -n gnome-python-desktop-%{version}

%build
CFLAGS="$RPM_OPT_FLAGS"				\
./configure 	--prefix=%{_prefix}		\
	    	--sysconfdir=%{_sysconfdir}     \
                %{gtk_doc_option}
make \
    pyexecdir=%{_libdir}/python%{python_version}/vendor-packages \
    pythondir=%{_libdir}/python%{python_version}/vendor-packages

%install
make install DESTDIR=$RPM_BUILD_ROOT \
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
%{_libdir}/python?.?/vendor-packages/gtk-2.0

%doc AUTHORS NEWS README ChangeLog
%doc examples

%files devel
%defattr(644, root, root)
%{_libdir}/pkgconfig/*
%{_datadir}/pygtk
%{_datadir}/gtk-doc

%changelog -n gnome-python-desktop
* Tue Mar 17 2009 - dave.lin@sun.com
- Bump to 2.26.0
* Mon Feb 16 2009 - dave.lin@sun.com
- Bump to 2.25.91
* Thu Feb 05 2009 - christian.kelly@sun.com
- Bump to 2.25.90.
* Tue Jan 20 2009 - brian.cameron@sun.com
- Bump to 2.25.1.
* Mon Sep 29 2008 - christian.kelly@sun.com
- Bump to 2.24.0.
* Tue Sep 02 2008 - christian.kelly@sun.com
- Bump to 2.23.1.
* Mon Jun 16 2008 - damien.carbery@sun.com
- Bump to 2.23.0.
* Mon Mar 10 2008 - damien.carbery@sun.com
- Bump to 2.22.0.
* Mon Feb 25 2008 - damien.carbery@sun.com
- Bump to 2.21.3.
* Thu Jan 17 2008 - damien.carbery@sun.com
- Bump to 2.21.2.
* Tue Dec 18 2007 - damien.carbery@sun.com
- Bump to 2.21.1.
* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 2.20.0.
* Tue Jul 31 2007 - damien.carbery@sun.com
- Bump to 2.19.2.
* Mon Jul 09 2007 - damien.carbery@sun.com
- Bump to 2.19.1.
* Mon Mar 12 2007 - damien.carbery@sun.com
- Bump to 2.18.0.
* Mon Mar 05 2007 - damien.carbery@sun.com
- Bump to 2.17.93. Remove upstream patch, 01-bad-include.
* Wed Jan 31 2007 - damien.carbery@sun.com
- Add patch, 01-bad-include, to fix #401760. Patch from upstream fix.
* Mon Jan 08 2007 - damien.carbery@sun.com
- Bump to 2.17.3. Remove upstream patch, 01-no_inline.
* Wed Nov 22 2006 - damien.carbery@sun.com
- Bump to 2.17.1. Add patch, 01-no_inline, to fix #368364.
* Fri Nov  3 2006 - laca@sun.com
- use %gtk_doc_option in configure so that it can be disabled using
  --without-gtk-doc
* Tue Sep 05 2006 - damien.carbery@sun.com
- Bump to 2.16.0.
* Wed Jul 26 2006 - damien.carbery@sun.com
- Bump to 2.15.90.
* Mon Mar 13 2006 - damien.carbery@sun.com
- Bump to 2.14.0.
* Wed Mar 01 2006 - glynn.foster@sun.com
- Initial version
