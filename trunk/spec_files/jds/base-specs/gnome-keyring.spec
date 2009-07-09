#
# spec file for package gnome-keyring
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jefftsai
#
Name:         gnome-keyring
License:      GPL v2, LGPL v2
Group:        System/GUI/GNOME
Version:      2.26.1
Release:      4
Distribution: Java Desktop System
Vendor:	      Sun Microsystems, Inc.
URL:          http://www.gnome.org
Summary:      GNOME Key Ring
Source:       http://download.gnome.org/sources/%{name}/2.26/%{name}-%{version}.tar.bz2
%if %build_l10n
Source1:      l10n-configure.sh
%endif
# date:2009-03-03 owner:qc161282 type:branding
Patch1:       gnome-keyring-01-not-check-asn1parser.diff
# date:2009-03-03 owner:qc161282 type:bug bugzilla:572527
Patch2:       gnome-keyring-02-ssh-agent.diff
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
gnome-keyring is a program that keep password and other secrets for
users. It is run as a daemon in the session, similar to ssh-agent, and
other applications can locate it by an environment variable.
                                                                                                                                                             
The program can manage several keyrings, each with its own master
password, and there is also a session keyring which is never stored to
disk, but forgotten when the session ends.
                                                                                                                                                             
The library libgnome-keyring is used by applications to integrate with
the gnome keyring system.

%package devel
Summary:      GNOME Key Ring Library
Group:        Development/Libraries/GNOME
Requires:     %{name} = %{version}
Requires:     gtk2-devel >= %{gtk2_version}

%description devel
gnome-keyring is a program that keep password and other secrets for
users. It is run as a daemon in the session, similar to ssh-agent, and
other applications can locate it by an environment variable.
                                                                                                                                                             
The program can manage several keyrings, each with its own master
password, and there is also a session keyring which is never stored to
disk, but forgotten when the session ends.
                                                                                                                                                             
The library libgnome-keyring is used by applications to integrate with
the gnome keyring system.

%prep
%setup -q
%patch1 -p1
%patch2 -p1

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

aclocal $ACLOCAL_FLAGS -I .
autoconf
autoheader
automake -a -c -f

CFLAGS="$RPM_OPT_FLAGS -I/usr/include/glib-2.0 -I/usr/lib/glib-2.0/include"	\
./configure --prefix=%{_prefix}			\
	    --sysconfdir=%{_sysconfdir}		\
	    --mandir=%{_mandir}			\
	    --disable-pam			\
            --libexecdir=%{_libexecdir}

# FIXME: hack: stop the build from looping
touch po/stamp-it

make -j $CPUS

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'
rm $RPM_BUILD_ROOT%{_bindir}/gnome-keyring

#%check
make check

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%{_datadir}/locale/*/LC_MESSAGES/*
%{_bindir}/*
%{_libdir}/lib*.so.*
%{_libexecdir}/gnome-keyring-ask

%files devel
%{_libdir}/pkgconfig/*.pc
%{_includedir}/gnome-keyring-1/*
%{_libdir}/lib*.so

%changelog
* Tue Apr 14 2009 - halton.huo@sun.com
- Bump to 2.26.1
* Mon Mar 16 2009 - jeff.cai@sun.com
- Bump to 2.26.0
- Remove patch -01-disable-im, upstreamed.
- Add patch 01-not-check-asn1parser to disable checking
  asn1parser since it is not shipped by libtasn1 due to
  GPLv3 issue.
* Tue Mar 03 2009 - jeff.cai@sun.com
- Add patch -02-ssh-agent, if one slot is correct, not
  return error. Fix #572527
* Tue Mar 03 2009 - jeff.cai@sun.com
- Bump to 2.25.92
- Remove -02-secure-memory-union, upstreamed.
* Thu Feb 19 2009 - jeff.cai@sun.com
- Remove /usr/bin/gnome-keyring since it is only a tool
  and not complete yet.
* Mon Feb 16 2009 - jeff.cai@sun.com
- Bump to 2.25.91
- Add patch -02-secure-memory-union to fix uname union, 
  Fix bugzilla #571951
* Fri Feb 13 2009 - jeff.cai@sun.com
- Change the owner to jeff cai.
* Wed Feb 04 2009 - jeff.cai@sun.com
- Bump to 2.25.90
* Wed Jan 20 2009 - jeff.cai@sun.com
- Bump to 2.25.5
- Remove patch -02-return-void, upstreamed
* Wed Jan 09 2009 - jeff.cai@sun.com
- Bump to 2.25.4.2
- Add patch -02-return-void, fix #567121.
* Fri Dec 12 2008 - jeff.cai@sun.com
- Bump to 2.25.2
- Remove patch -02-hal-error.diff, upstreamed
- Remove patch -03-libtasn1.diff, upstreamed
* Mon Dec 08 2008 - jeff.cai@sun.com
- Add patch -03-libtasn to get building flag with pkg-config
  Fix #563702
* Fri Nov 28 2008 - jeff.cai@sun.com
- Add patch -02-hal-error.diff to not print null string in printf.
* Tue Nov 18 2008 - takao.fujiwara@sun.com
- Add gnome-keyring-01-disable-im.diff to disable input method in password.
* Tue Nov 07 2008 - jeff.cai@sun.com
- Bump to 2.25.1
* Tue Nov 04 2008 - halton.huo@sun.com
- Bump to 2.24.1
- Remove upstreamed patch logout.diff
* Fri Oct 31 2008 - jeff.cai@sun.com
- Change the license tag.
* Wed Oct 15 2008 - jeff.cai@sun.com
- Add bugzilla bug id for -01-logout patch.
* Mon Sep 22 2008 - jeff.cai@sun.com
- Bump to 2.24.0
* Tue Sep 09 2008 - jeff.cai@sun.com
- Bump to 2.23.92
- Remove patch 02-timegm.diff
* Fri Sep 05 2008 - jeff.cai@sun.com
- Bump to 2.23.91
- Add patch -02-timegm.diff
* Mon Aug 26 2008 - jeff.cai@sun.com
- Change the bug comment.
* Mon Aug 19 2008 - jeff.cai@sun.com
- Bump to 2.23.90

* Mon Aug 18 2008 - jeff.cai@sun.com
- Remove gnome-keyring-pkcs11.la

* Tue Aug 05 2008 - jeff.cai@sun.com
- Add patch -01-logout.diff
  Fix bugster 6732147.

* Tue Aug 05 2008 - jeff.cai@sun.com
- Bump to 2.23.6.

* Tue Jul 22 2008 - damien.carbery@sun.com
- Bump to 2.23.5.

* Wed Jun 18 2008 - jeff.cai@sun.com
- Bump to 2.22.2. Remove -01-strsep, -02-gulong2gsize

* Wed Apr 16 2008 - damien.carbery@sun.com
- Add 'make check' call after %install.

* Thu Feb 14 2008 - damien.carbery@sun.com
- Add patch 02-gulong2gsize to sync with changes in glib 2.15.5. Also modify
  CFLAGS to find a glib header.

* Wed Jan 30 2008 - damien.carbery@sun.com
- Revert to 2.20.3 because the AM_PATH_LIBTASN1 macro is unavailable.

* Tue Jan 29 2008 - patrick.ale@gmail.com
- Fix typo in download URL

* Tue Jan 29 2008 - damien.carbery@sun.com
- Bump to 2.21.90.

* Sun Jan 20 2008 - patrick.ale@gmail.com
- Version unbumped to 2.20 by damien but download directory
  was still 2.21. Fixed by changing to /pub/SOURCES/2.20

* Fri Jan 18 2008 - damien.carbery@sun.com
- Revert to 2.20.3 because the AM_PATH_LIBTASN1 macro is unavailable.

* Thu Jan 17 2008 - damien.carbery@sun.com
- Bump to 2.21.5.

* Mon Jan 07 2008 - damien.carbery@sun.com
- Bump to 2.20.3.

* Wed Dec 19 2007 - patrick.ale@gmail.com
- Version unbumped to 2.20 by damien but download directory 
  was still 2.21. Fixed by changing to /pub/SOURCES/2.20

* Tue Dec 18 2007 - damien.carbery@sun.com
- Bump to 2.21.4.

* Tue Nov 27 2007 - damien.carbery@sun.com
- Bump to 2.20.2.

* Fri Oct 19 2007 - damien.carbery@sun.com
- Bump to 2.20.1. Remove upstream patch, 02-new-keyring-bug.

* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 2.20.0. Remove upstream patch, 02-export-symbols. Renumber rest.

* Thu Sep 13 2007 - darren.kenny@sun.com
- Added patch for bugzilla bug: 476644, which presents issues when creating a
  new keyring where non existed before : gnome-keyring-03-new-keyring-bug.diff

* Wed Sep 05 2007 - halton.huo@sun.com
- Bump to 2.19.91.
- Add patch 02-export-symbols for bugzilla #473796
- Remove upstream patches, XX-err_to_g_error and XX-string_header

* Thu Aug 16 2007 - damien.carbery@sun.com
- Unbump to 2.19.6.1 because of build error I cannot figure out.

* Wed Aug 15 2007 - damien.carbery@sun.com
- Bump to 2.19.90. Remove upstream patches, 01-err_to_g_error and
  02-string_header.

* Mon Jul 30 2007 - damien.carbery@sun.com
- Add 3 patches, 01-err_to_g_error, 02-string_header and 03-strsep to fix
  Solaris specific build issues.

* Tue Jul 31 2007 - halton.huo@sun.com
- Bump to 2.19.6.1.

* Mon Jul 30 2007 - damien.carbery@sun.com
- Bump to 2.19.6. Remove upstream patch, 01-suncc-build-fail.

* Mon Jul 09 2007 - halton.huo@sun.com
- Bump to 2.19.5.
- Add patch suncc-build-fail.diff to let build pass.

* Tue Jun 19 2007 - damien.carbery@sun.com
- Bump to 2.19.4.1.

* Mon Jun 18 2007 - damien.carbery@sun.com
- Bump to 2.19.4.

* Tue May 15 2007 - damien.carbery@sun.com
- Bump to 2.19.2. Remove unneeded patch, 01-pkcs. gnome-keyring uses libgcrypt
  now.

* Sun Apr 08 2007 - damien.carbery@sun.com
- Bump to 0.8.1. Remove upstream patch, 02-crash.

* Tue Mar 27 2007 - halton.huo@sun.com
- Add patch crash.diff.

* Mon Mar 12 2007 - damien.carbery@sun.com
- Bump to 0.8.

* Tue Mar 06 2007 - damien.carbery@sun.com
- Bump to 0.7.92.

* Tue Feb 13 2007 - damien.carbery@sun.com
- Bump to 0.7.91.

* Fri Jan 05 2007 - damien.carbery@sun.com
- Bump to 0.7.3.

* Tue Dec 19 2006 - damien.carbery@sun.com
- Bump to 0.7.2.

* Wed Dec 06 2006 - takao.fujiwara@sun.com
- Add intltoolize to read LIGUAS file. Fixes 6498950

* Mon Sep 04 2006 - damien.carbery@sun.com
- Bump to 0.6.0.

* Fri Jul 20 2006 - padraig.obriain@sun.com
- Bump to 0.5.1.

* Tue May 02 2006 - damien.carbery@sun.com
- Remove unneeded intltoolize call.

* Mon Mar 13 2006 - damien.carbery@sun.com
- Bump to 0.4.9.

* Tue Feb 28 2006 - damien.carbery@sun.com
- Bump to 0.4.8.

* Mon Feb 13 2006 - damien.carbery@sun.com
- Bump to 0.4.7.
- Add hack to fix infinite loop problem in po/Makefile.

* Tue Nov 29 2005 - damien.carbery@sun.com
- Bump to 0.4.6.

* Thu Sep 15 2005 - brian.cameron@sun.com
- Bump to 0.4.5.

* Fri Sep 09 2005 - laca@sun.com
- call intltoolize so that the correct Makefile.in.in is copied to po

* Tue Sep 06 2005 - damien.carbery@sun.com
- Call glib-gettextize as po/Makefile.in.in not in tarball. Add patch to
  skip the 'ar' locale as its files has problems #315335.

* Mon Sep 05 2005 - damien.carbery@sun.com
- Bump to 0.4.4.

* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 0.4.3.

* Wed Jun 15 2005 - laca@sun.com
- Add more libs to LDADD so that it builds with the new pkgconfig

* Fri May 06 2005 - glynn.foster@sun.com
- Bump to 0.4.2

* Fri Aug 29 2004 - brian.cameron@sun.com
- Added patch 01 for pkcs support.

* Wed Aug 18 2004 - brian.cameron@sun.com
- removed --disable-gtk-doc since this isn't an option this module's
  configure takes.

* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-keyring-l10n-po-1.2.tar.bz2

* Wed Jul 07 2004 - niall.power@sun.com
- ported to rpm4
                                                                                
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds

* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-keyring-l10n-po-1.1.tar.bz2

* Tue Apr 13 2004 - laszlo.kovacs@sun.com
- upgraded tarball
* Wed Mar 31 2004 - brian.cameron@sun.com
- replace tar jxf with the more solaris friendly
  bzcat piped through tar

* Mon Mar 29 2004 - damien.donlon@sun.com
- Adding gnome-keyring-l10n-po-1.0.tar.bz2 l10n content

* Fri Mar 19 2004 - glynn.foster@sun.com
- Bump to 0.1.91 and remove the uninstalled pc patch
  since it's upstream.

* Fri Mar 12 2004 - niall.power@sun.com
- define libexecdir in configure args

* Mon Feb 02 2004 - niall.power@sun.com
- bump to 0.1.2
- Add patch to generate an -uninstalled.pc file
- Add ACLOCAL_FLAGS env to aclocal invocation

* Mon Dec 15 2003 - glynn.foster@sun.com
- Initial Sun release
