#
# spec file for package gtkmm
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: bewitche
#

Name:         gtkmm
License:      LGPL
Group:        System/Libraries
Version:      2.16.0
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      gtkmm - C++ Interfaces for GTK+ and GNOME
Source:       http://download.gnome.org/sources/gtkmm/2.16/gtkmm-%{version}.tar.bz2

#date:2008-02-14 owner:bewitche type:feature  
Patch1:       gtkmm-01-ignore-defs.diff

URL:          http://www.gtkmm.org/
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n gtkmm-%version
%patch1 -p1


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
%if %cc_is_gcc
%else
export CXX="${CXX} -norunpath"
%endif
export CXXFLAGS="%cxx_optflags -D_XPG4_2 -D_RWSTD_NO_WSTR -D__EXTENSIONS__"

# background.jpg is required by gtkmm-demo, but not in the right directory
# we simply copy the file into the proper directory
cp ./demos/background.jpg ./demos/gtk-demo

# Recreate aclocal.m4 because of automake version mismatch (CBE: 1.10,
# gtkmm: 1.10.1)
aclocal -Iscripts
automake --add-missing
autoconf
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}
make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*


%changelog
* Tue Mar 17 2009 - dave.lin@sun.com
- Bump to 2.16.0
* Fri Mar 13 2009 - dave.lin@sun.com
- Bump to 2.15.5
* Mon Feb 16 2009 - dave.lin@sun.com
- Bump to 2.15.3
* Thu Jan 08 2009 - christian.kelly@sun.com
- Bump to 2.15.0.
* Mon Nov 17 2008 - chris.wang@sun.com
- Add _RWSTD_NO_WSTR to CXXFLAG
* Fri Sep 12 2008 - chris,wang@sun.com
- Bump to 2.13.8
- remove patch 02-widget, as the community has revert the code
* Thu Aug 21 2008 - dave.lin@sun.com
- Bump to 2.13.7
* Fri Aug 08 2008 - damien.carbery@sun.com
- Remove reference to upstream patch glibmm-02-m4-macro.diff. Rename remainder.
* Tue Aug 05 2008 - damien.carbery@sun.com
- Bump to 2.13.6.
* Thu Jul 30 2008 - chris.wang@sun.com
- Bump to 2.13.5, we added pangomm spec
* Fri Jul 18 2008 - christian.kelly@sun.com
- Add patch gtkmm-03-widget, fix build issue, widget.cc use of & operator.
* Thu Jul 17 2008 - christian.kelly@sun.com
- Bump to 2.13.4.
- Remove patch 02-gtk-deprecated, fix upstream.
* Thu Jul 10 2008 - damien.carbery@sun.com
- Add patch 02-gtk-deprecated.
* Wed Apr 03 2008 - damien.carbery@sun.com
- Bump to 2.12.7.
* Wed Mar 05 2008 - damien.carbery@sun.com
- Don't need to rename 'demo' to 'gtkmm-demo' as the installed file is now
  called 'gtkmm-demo'.
* Mon Feb 25 2008 - damien.carbery@sun.com
- Bump to 2.12.5. Remove upstream patches, 02-demo and 03-demo-installation.
* Fri Feb 22 2008 - damien.carbery@sun.com
- Add glibmm-02-m4-macro to fix #423990. Use glibmm patch as issue is identical.
* Thu Feb 14 2008 - chris.wang@sun.com
- Add patches gtkmm-02-demo, gtkmm-03-demo-installation to deliver gtkmm-demo
  on /usr/demo/jds/bin and resource files on /usr/share/gtkmm-2.4/demo
* Thu Feb 14 2008 - chris.wang@sun.com
- Add patch gtkmm-01-ignore-defs to remove the build of defs files since they
  are delivered with tarball and libglibmm_generate_extra_defs.so is not 
  delivered. We have raise this issue to module owner, and will remove the 
  patch if the module owner agree to remove .def file from tarball
* Tue Jan 29 2008 - chris.wang@sun.com
- create
