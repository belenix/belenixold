#
# spec file for package seahorse
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jefftsai
#
Name:         seahorse
License:      GPL v2, LGPL v2, FDL v1.1
Group:        System/GUI/GNOME
Version:      2.26.1
Release:      1
Distribution: Java Desktop System
Vendor:	      Sun Microsystems, Inc.
Summary:      Seahorse
Source:       http://download.gnome.org/sources/%{name}/2.26/%{name}-%{version}.tar.bz2
%if %build_l10n
Source1:                 l10n-configure.sh
%endif

# date:2008-10-22 owner:jefftsai type:branding
Patch2:		seahorse-02-disable-remote.diff
# date:2008-11-04 bugzilla:556670 owner:jefftsai type:bug
Patch3:		seahorse-03-import-ssh.diff
# date:2008-12-29 owner:jefftsai type:branding
Patch6:		seahorse-06-return-void.diff

URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Autoreqprov:  on
Prereq:       /sbin/ldconfig

%define gtk2_version 2.4.0
%define pkgconfig_version 0.15.0
%define gtk_doc_version 1.1

Requires: gtk2 >= %{gtk2_version}
BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: gtk-doc >= %{gtk_doc_version}
BuildRequires: pkgconfig >= %{pkgconfig_version}

%description
Seahorse is a GNOME application for managing encryption keys. It also
integrates with nautilus, gedit and other places for encryption, decrption
and other operations.

%prep
%setup -q
%patch2 -p1
%patch3 -p1
%patch6 -p1

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
intltoolize -f -c --automake

%if %build_l10n
bash -x %SOURCE1 --enable-copyright
%endif

gnome-doc-prepare --force
aclocal -I /usr/share/aclocal -I m4
autoconf
autoheader
automake 

CFLAGS="$RPM_OPT_FLAGS -I/usr/include/glib-2.0 -I/usr/lib/glib-2.0/include"	\
./configure --prefix=%{_prefix}			\
	    --sysconfdir=%{_sysconfdir}		\
	    --mandir=%{_mandir}			\
            --libexecdir=%{_libexecdir}         \
            --disable-ldap                      \
            --disable-hkp
make  -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT%{_libdir}/*.la

%check
make check

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue Apr 14 2009 - halton.huo@sun.com
- Bump to 2.26.1
* Mon Mar 16 2009 - jeff.cai@sun.com 
- Bump to 2.26.0
- Remove patch -04-disable-im, upstreamed.
* Tue Mar 03 2009 - jeff.cai@sun.com 
- Bump to 2.25.92
* Mon Feb 16 2009 - jeff.cai@sun.com
- Bump to 2.25.91
* Wed Feb 04 2009 - jeff.cai@sun.com
- Bump to 2.25.90
- Remove patch -05-libtasn1, not needed since the dependency
  is removed
* Mon Feb 02 2009 - jeff.cai@sun.com
- Add patch -05-libtasn1.diff, Fix #570171.
- Remove patch -01-input-passwd.diff, this bug is not 
  reproducible on 2.25.4
* Fri Jan 09 2009 - jeff.cai@sun.com
- Bump to 2.25.4
- Remove -05-ssh-upload.diff, upstreamed
- Remove -07-gp11object-slot.diff, not needed.
* Mon Dec 29 2008 - jeff.cai@sun.com
- Bump to 2.25.3
- Remove -03-a11y-hang, upstreamed.
- Remove -04-show-error, upstreamed.
- Remove -05-dialog-markup, upstreamed.
- Remove -08-progress-pos, upstreamed.
- Remove -09-key-name, upstreamed.
- Reorder the rest patches.
- Add patch -06-return-void, upstreamed.
- Add patch -07-gpobject-slot, fix bug #566031. 
  This is only a temporary solution for the build issue.
* Thu Nov 27 2008 - jeff.cai@sun.com
- Add -10-ssh-upload.diff to defer the destroy of swidget
  Fix #562413
* Tue Nov 20 2008 - jeff.cai@sun.com
- Add -09-key-name.diff to refresh key names if it changes.
  Fix #561641
* Tue Nov 19 2008 - jeff.cai@sun.com
- Add seahorse-08-progress-pos.diff to make the progress dialog
  not cover the password dialog.
* Tue Nov 18 2008 - takao.fujiwara@sun.com
- Add seahorse-07-disable-im.diff to disable input method in password.
* Wed Nov 04 2008 - jeff.cai@sun.com
- Add patch -06-import-ssh, need a better patch.
* Fri Oct 31 2008 - jeff.cai@sun.com
- Change the license tag.
* Thu Oct 30 2008 - jeff.cai@sun.com
- Add comment " not upgrade it before it goes to nevada"
* Thu Oct 30 2008 - jeff.cai@sun.com
- Add patch -04-show-error to fix #558491
- Add patch -05-dialog-markup to fix #558494
* Thu Oct 23 2008 - jeff.cai@sun.com
- Add patch -03-a11y-hang to fix #557537
* Wed Oct 22 2008 - jeff.cai@sun.com
- Bump to 2.24.1.
- Remove upstream patch -01-build-thread
- Add patch -01-input-password
- Add patch -02-disable-remote since solaris doesn't
  have PGP support
* Mon Sep 22 2008 - jeff.cai@sun.com
- Bump to 2.24.0.
- Add patch -01-build-thread
* Thu Sep 08 2008 - jeff.cai@sun.com
- Bump to 2.23.92.
* Thu Sep 02 2008 - christian.kelly@sun.com
- Bump to 2.23.91.
* Tue Aug 19 2008 - dave.lin@sun.com
- Bump to 2.23.90
* Tue Aug 05 2008 - damien.carbery@sun.com
- Bump to 2.23.6. Remove all patches as they are upstream.

* Wed Jul 23 2008 - jeff.cai@sun.com
- Add bug no.

* Mon Jul 21 2008 - jeff.cai@sun.com
- Initial Sun release
