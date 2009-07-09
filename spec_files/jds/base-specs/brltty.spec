#
# spec file for package brltty
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: dcarbery
#
Name:           brltty
License:        GPL
Group:          System/Library
Version:        3.9
Release:        1
Distribution:   Java Desktop System
Vendor:	        Sun Microsystems, Inc.
Summary:        Braille Support
Source:         http://www.mielke.cc/brltty/releases/brltty-%{version}.tar.gz
# date:2005-08-24 owner:dcarbery type:bug state:upstream
Patch1:         brltty-01-suncc.diff
# date:2008-08-29 owner:laca type:bug state:upstream
# Willie said he would push it upstream
Patch2:         brltty-02-dlsym.diff
URL:            http://mielke.cc/brltty/
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Docdir:         %{_defaultdocdir}/doc
Autoreqprov:    on

%description
BRLTTY is a background process (daemon) providing access to the Linux/Unix
console (when in text mode) for a blind person using a refreshable braille
display. It also provides an API for braille support.

%prep
%setup -q -n brltty-%{version}
%patch1 -p1 
%patch2 -p1

%build
CFLAGS="%optflags"
LDFLAGS="%{_ldflags} %optflags"
bash ./configure     --prefix=%{_prefix}             \
                --sysconfdir=%{_sysconfdir}     \
                --disable-tcl-bindings          \
		--libdir=%{_libdir}		\
		--bindir=%{_bindir}		\
		--mandir=%{_mandir}
make

%install
#rm -rf $RPM_BUILD_ROOT
make install INSTALL_ROOT=$RPM_BUILD_ROOT sysconfdir=$RPM_BUILD_ROOT/etc
rm $RPM_BUILD_ROOT%{_libdir}/*.a
# Move python site-packages dir to vendor-packages.
if [ -x $RPM_BUILD_ROOT%{_libdir}/python?.? ] ; then
cd $RPM_BUILD_ROOT%{_libdir}/python?.?
mv site-packages vendor-packages 
fi

%clean
rm -rf $RPM_BUILD_ROOT

%post

%postun

%files
%defattr(644, root, root)
%{_sysconfdir}/brlapi.key
%{_includedir}/brltty/*
%{_sysconfdir}/brltty/*
%{_bindir}/*
%{_libdir}/libbrl*
%{_libdir}/brltty/libbrltty*.so
%{_mandir}/*

%changelog
* Fri Aug 29 2008 - laca@sun.com
- add patch dlsym.diff
* Mon Jul 07 2008 - li.yuan@sun.com
- Fix 6697334. Add 64 bit libraries support.
* Tue Nov 13 2007 - brian.cameron@sun.com
- Bump to 3.9.
* Wed Jul 25 2007 - damien.carbery@sun.com
- Bump to 3.8. Remove upstream patch, 02-lib-symlinks. Add code to handle new
  python libs.
* Wed Nov 01 2006 - damien.carbery@sun.com
- Add patch, 02-lib-sylinks to fix 6454451. Adds code to create symlink for 
  to a module library. Executable required the symlink.
* Tue Apr 4 2006 - glynn.foster@sun.com
- Remove libbrlapi.a from the package.
* Tue Jan 17 2006 - damien.carbery@sun.com
- Bump to 3.7.2.
* Tue Dec 20 2005 - damien.carbery@sun.com
- Bump to 3.7.1.
* Wed Oct 26 2005 - damien.carbery@sun.com
- Bump to 3.7.
* Thu Sep 27 2005 - damien.carbery@sun.com
- Bump to 3.6.2.
* Tue Aug 16 2005 - rich.burridge@sun.com
- Initial Sun release
