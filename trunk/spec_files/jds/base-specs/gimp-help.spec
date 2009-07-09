#
# spec file for package gimp-help
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: dkenny
#
Name:         gimp-help
License:      GPL/LGPL
Group:        System/Documentation/GNOME
Version:      2.4.1
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      On-line Help for the GIMP (GNU Image Manipulation Program)
Source:       ftp://ftp.gimp.org/pub/gimp/help/%{name}-%{version}.tar.bz2
URL:          http://www.gimp.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/doc
Autoreqprov:  on
Requires:     gimp

%description
On-Line help documents for the Gimp.

%prep
%setup -q

%build
./configure --prefix=%{_prefix}	\
    --sysconfdir=%{_sysconfdir} \
    --bindir=%{_bindir}		\
    --libdir=%{_libdir}		\
    --includedir=%{_includedir} \
    --libexecdir=%{_libexecdir} \
    --localstatedir=/var/lib	\
    --mandir=%{_mandir}		\
    --enable-mp			\
    %{gtk_doc_option}           \
    --enable-default-binary	\
    --without-gimp		\
    %{print_options}

make

%install
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, root)
%{_datadir}/gimp/*/help/

%changelog
* Wed Apr 23 2008 - damien.carbery@sun.com
- Bump to 2.4.1.

* Fri Jan 11 2008 - laca@sun.com
- Create -- split out of gimp.spec
