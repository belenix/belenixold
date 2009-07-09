#
# spec file for package glib2 
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: erwannc
#
Name:         glib2 
License:      LGPL
Group:        System/Libraries
Version:      2.20.0
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Low level core compatibility library for GTK+ and GNOME
Source:       http://ftp.gnome.org/pub/GNOME/sources/glib/2.20/glib-%{version}.tar.bz2

# Patch default-path to not include "." because on Solaris we want to avoid
# setting PATH to include the current working directory.  This was an ARC
# requirement.  The GNOME community already decided to not change this behavior
# (bugzilla bug 317945), but this change is safe.  This code only gets executed
# when the user's PATH is unset, which should be never.  Safer to avoid adding
# "." to PATH.
#owner:yippi date:2005-08-14 type:feature 
Patch1:       glib-01-default-path.diff
# owner:laca type:bug date:2005-10-13
Patch2:       glib-02-gmodule-always-lazy.diff
#owner:stephen date:2006-11-01 type:feature bugster:6393731
Patch3:       glib-03-trusted-extensions.diff
#owner:padraig date:2008-01-10 type:bug bugster:5105006
Patch4:       glib-04-gio-trash-only-home.diff
#owner:dcarbery date:2008-01-30 type:bug bugzilla:385132
Patch5:       glib-05-ac-canonical-host.diff
#owner:dcarbery date:2008-05-21 type:bug bugzilla:528506
Patch7:       glib-07-ss12-visibility.diff
#owner:bewitche date:2008-09-17 type:bug bugzilla:551919
Patch8:       glib-08-typedetect.diff
#owner:bewitche date:2009-02-23 type:bug
Patch9:      glib-09-gsize.diff  
URL:          http://www.gtk.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
AutoReqProv:  on
Prereq:       /sbin/ldconfig

%define pkgconfig_version 0.15.0
%define gtk_doc_version 1.1
%define intltool_version 0.34.1

Requires:      aaa_base
BuildRequires: pkgconfig >= %{pkgconfig_version}
BuildRequires: gtk-doc >= %{gtk_doc_version}
BuildRequires: intltool >= %{intltool_version}

%description
Glib is the base compatibility library for GTK+ and GNOME. It provides data
structure handling for C, portability wrappers, and interfaces for such
runtime functionality as an event loop, threads, dynamic laoding, and an
object system

%package devel
Summary:        GIMP Toolkit and GIMP Drawing Kit support library
Group:          Development/Libraries
Requires:       %{name} = %{version}

%description devel
Glib is the base compatibility library for GTK+ and GNOME. It provides data
structure handling for C, portability wrappers, and interfaces for such
runtime functionality as an event loop, threads, dynamic laoding, and an
object system

%prep
%setup -q -n glib-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1

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

aclocal $ACLOCAL_FLAGS
libtoolize --force --copy
gtkdocize
autoheader
automake -a -c -f
autoconf
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix} \
            --mandir=%{_mandir} \
            --datadir=%{_datadir} \
            --libdir=%{_libdir} \
            --bindir=%{_bindir} \
	    --sysconfdir=%{_sysconfdir}	\
	    --disable-fam	\
	    %{gtk_doc_option}

make -j $CPUS

%install

make DESTDIR=$RPM_BUILD_ROOT install
#Copy zh_HK from zh_TW
#Fixes bug 4930405
install -d $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES
install --mode=0644 $RPM_BUILD_ROOT%{_datadir}/locale/zh_TW/LC_MESSAGES/*.mo $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES/
rm $RPM_BUILD_ROOT%{_libdir}/*.la
 
%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/lib*.so.*
%{_datadir}/locale/*/LC_MESSAGES/*.mo

%files devel
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/lib*.so
%{_includedir}/glib-2.0/*
%{_libdir}/glib-2.0/include/*.h
%{_libdir}/pkgconfig/*.pc
%{_datadir}/aclocal/*.m4
%{_datadir}/glib-2.0/*
%{_datadir}/gtk-doc/html/*
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
* Sat Apr 04 2009 - dave.lin@sun.com
- Removed the unnecessary option %option_with_gnu_iconv.
* Fri Mar 13 2009 - dave.lin@sun.com
- Bump to 2.20.0
* Mon Mar 02 2009 - dave.lin@sun.com
- Bump to 2.19.10
* Mon Feb 23 2009 - chris.wang@sun.com
- Add patch 09 to fix 64 application fail on check gsize issue
* Wed Feb 18 2009 - dave.lin@sun.com
- Bump to 2.19.8
* Tue Feb 17 2009 - dave.lin@sun.com
- Bump to 2.19.7
* Fri Feb 13 2009 - dave.lin@sun.com
- Bump to 2.19.6
* Wed Jan 07 2000 - christian.kelly@sun.com
- Bump to 2.19.4.
- Remove patch9.
* Mon Dec 15 2008 - chris.wang@sun.com
- Add patch glib-09-sunpro_c.diff, define G_GNUC_INTERNAL to 
  __attribute__(visibility("hidden")) in SS12
* Wed Dec 03 2008 - dave.lin@sun.com
- Bump to 2.19.2
* Wed Dec 03 2008 - dave.lin@sun.com
- Bump to 2.19.1
* Wed Sep 17 2008 - chris.wang@sun.com
- add patch 08-typedetect to fix defecto bug 3355 core dump from pidgin
* Tue Sep 08 2008 - patrick.ale@gmail.com
- Correct download URL
* Wed Sep 03 2008 - christian.kelly@sun.com
- Bump to 2.18.0.
* Tue Aug 19 2008 - dave.lin@sun.com
- Bump to 2.17.7
- Removed the upstreamed patch glib-06-dont-show-zfs.diff
* Fri Aug 15 2008 - padraig.obriain@sun.com
- Update patch 06-dont-show-zfs to what has been accepted upstream.
* Wed Aug 06 2008 - damien.carbery@sun.com
- Bump to 2.17.6.
* Tue Jul 22 2008 - christian.kelly@sun.com
- Bump to 2.17.4
* Wed Jul 10 2008 - padraig.obriain@sun.com
- Add patch 06-dont-show-zfs.
* Thu Jul 03 2008 - damien.carbery@sun.com
- Bump to 2.17.3.
* Fri Jun 13 2008 - damien.carbery@sun.com
- Bump to 2.17.2.
* Thu May 29 2008 - damien.carbery@sun.com
- Bump to 2.17.0. Remove upstream patches, 06-gio-fen, 08-gio-set-name,
  09-gio-fs-type. Renumber remainder.
* Tue May 27 2008 - simon.zheng@sun.com
- Rework 09-gio-fs-type.diff the same as upstream.
* Wed Apr 08 2008 - damien.carbery@sun.com
- Add patch ss12-visibility to fix bugzilla 528506. Sun Studio 12 compiler
  doesn't support aliases for variables. Disable this change until we switch to
  building with ss12.
* Fri May 16 2008 - simon.zheng@sun.com
- Add glib-09-gio-fs-type.diff to identify filesystem type on Solaris. 
* Thu Apr 10 2008 - padraig.obriain@sun.com
- Rework glib-04-gio-trash-only-home.diff so that it applies
* Wed Apr 08 2008 - damien.carbery@sun.com
- Bump to 2.16.3.
* Wed Apr 09 2008 - padraig.obriain@sun.com
- Added glib-08-gio-set-name.diff.
* Thu Apr 03 2008 - padraig.obriain@sun.com
- Added glib-07-gio-ignore-fs.diff.
* Wed Apr 03 2008 - damien.carbery@sun.com
- Bump to 2.16.2.
* Tue Mar 18 2008 - lin.ma@sun.com
- Added glib-06-gio-fen.diff which is upstreamed and will be available
  Glib 2.18.0, so it will be removed at that time.
* Tue Mar 11 2008 - damien.carbery@sun.com
- Bump to 2.16.1.
* Tue Feb 26 2008 - damien.carbery@sun.com
- Bump to 2.15.6.
* Wed Feb 13 2008 - damien.carbery@sun.com
- Bump to 2.15.5. Remove upstream patch 05-func. Comment out patch4 as it needs
  engineer rework. Rename patch6.
* Tue Jan 29 2008 - damien.carbery@sun.com
- Bump to 2.15.4.
* Tue Jan 22 2008 - damien.carbery@sun.com
- Bump to 2.15.3.
* Mon Jan 07 2008 - damien.carbery@sun.com
- Bump to 2.15.2. Remove upstream patch, 04-sed-i. Rename remainder.
* Thu Jan 10 2008 - padraig.obriain@sun.com
- Add patch glib-05-gio-trash-only-home.diff, rework of gnome-vfs and
  nautilus patches.
* Mon Jan 07 2008 - damien.carbery@sun.com
- Bump to 2.15.1. Remove upstream patch, 04-void-return, rename remainder.
* Fri Jan 04 2008 - ghee.teo@sun.com
- Added --disable-fam as per damien.
* Wed Dec 26 2007 - damien.carbery@sun.com
- Add patch 05-sed-i to rework sed command for non-GNU sed that doesn't support
  -i option.
* Tue Dec 25 2007 - damien.carbery@sun.com
- Add patch 04-void-return. void functions returning values are breaking build.
* Fri Dec 21 2007 - damien.carbery@sun.com
- Bump to 2.15.0.
* Fri Dec 21 2007 - takao.fujiwara@sun.com
- Remove glib-01-convert-utf8.diff Fixes 6294268
* Tue Nov 27 2007 - damien.carbery@sun.com
- Bump to 2.14.4.
* Wed Nov 07 2007 - damien.carbery@sun.com
- Bump to 2.14.3.
* Fri Oct 19 2007 - damien.carbery@sun.com
- Bump to 2.14.2.
* Tue Oct  2 2007 - laca@sun.com
- when building with GNU iconv, hack glib-2.0.pc.in so that /usr/gnu/lib
  is automatically added to the library search path and RUNPATH
* Sat Sep 29 2007 - laca@sun.com
- remove --with-libiconv=native option as it appears to break the build
  on nevada
* Fri Sep 28 2007 - laca@sun.com
- add support for building with GNU libiconv
* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 2.14.1.
* Sun Aug 05 2007 - damien.carbery@sun.com
- Bump to 2.14.0. Remove upstream patch, 05-gthread-cast.
* Fri Jul 13 2007 - damien.carbery@sun.com
- Bump to 2.13.7. Add patch 05-gthread-cast from svn trunk.
* Mon Jul 02 2007 - damien.carbery@sun.com
- Bump to 2.13.6.
* Tue Jun 19 2007 - damien.carbery@sun.com
- Bump to 2.13.5.
* Thu Jun 07 2007 - damien.carbery@sun.com
- Bump to 2.13.4.
* Wed Jun 06 2007 - damien.carbery@sun.com
- Bump to 2.13.3.
* Wed May 23 2007 - damien.carbery@sun.com
- Bump to 2.13.2. Remove upstream patch, 04-hidden. Renumber rest.
* Fri May 11 2007 - damien.carbery@sun.com
- Bump to 2.13.1.
* Wed May 02 2007 - damien.carbery@sun.com
- Bump to 2.12.12.
* Thu Mar 15 2007 - laca@sun.com
- convert to new style of building multiple ISAs as per docs/multi-ISA.txt
* Wed Mar 15 2007 - dougs@truemail.co.th
- Removed adding ccdir to PATH
* Fri Mar 09 2007 - damien.carbery@sun.com
- Bump to 2.12.11.
* Thu Mar 08 2007 - damien.carbery@sun.com
- Bump to 2.12.10. Remove upstream patch, 04-msgfmt-c. Renumber remainder.
* Sun Feb  4 2007 - laca@sun.com
- remove patch ALL_LINGUAS.diff - no longer needed; reorder remaining
* Wed Jan 17 2007 - damien.carbery@sun.com
- Bump to 2.12.9.
* Mon Jan 15 2007 - damien.carbery@sun.com
- Bump to 2.12.8.
* Fri Jan 05 2007 - damien.carbery@sun.com
- Bump to 2.12.7.
* Thu Dec 21 2006 - damien.carbery@sun.com
- Bump to 2.12.6.
* Tue Dec 19 2006 - damien.carbery@sun.com
- Bump to 2.12.5. Remove upstream patches, 01-gettext-macro,
  05-solaris-thread-flags, 09-use-fdwalk. Renumber remainder.
* Fri Nov  3 2006 - laca@sun.com
- use %gtk_doc_option in configure so that it can be disabled using
  --without-gtk-doc
* Wed Nov 01 2006 - stephen.browne@sun.com
- added patch glib-11-trusted-extensions.diff: covers bugster 639371
* Mon Oct 02 2006 - damien.carbery@sun.com
- Bump to 2.12.4.
* Mon Sep 25 2006 - padraig.obriain@sun.com
- Add patch use-fdwalk for bugzilla 357585
* Wed Aug 30 2006 - damien.carbery@sun.com
- Bump to 2.12.3.
* Wed Aug 16 2006 - damien.carbery@sun.com
- Bump to 2.12.2.
* Mon Jul 24 2006 - damien.carbery@sun.com
- Bump to 2.12.1.
* Thu Jul 20 2006 - damien.carbery@sun.com
- Bump to 2.12.0.
* Thu Jul 13 2006 - laca@sun.com
- add patch ALL_LINGUAS.diff that removes the \n's from ALL_LINGUAS in
  AM_GLIB_GNU_GETTEXT
* Thu May 25 2006 - brian.cameron@sun.com
- Add patch glib-08-hidden.diff to make sure that the G_HAVE_GNUC_VISIBILITY
  macro is defined to "__hidden" if using the Sun Forte compiler.  This 
  makes sure that symbols that should be hidden are not exported when using
  our compiler.  This resolves the GNOME 2.14 LSARC 2006/202 TCR regarding
  this issue.
* Wed Apr 26 2006 - damien.carbery@sun.com
- Bump to 2.10.2.
* Wed Mar  8 2006 - damien.carbery@sun.com
- Bump to 2.10.1.
* Sun Feb 26 2006 - damien.carbery@sun.com
- Bump to 2.10.0.
* Mon Feb 13 2006 - damien.carbery@sun.com
- Bump to 2.9.6.
* Sun Feb 12 2006 - damien.carbery@sun.com
- Call gettextize to fix infinite loop in configure.
* Fri Jan 27 2006 - damien.carbery@sun.com
- Bump to 2.9.5
* Tue Jan 17 2006 - damien.carbery@sun.com
- Bump to 2.9.3
* Sun Jan 15 2006 - damien.carbery@sun.com
- Bump to 2.9.2.
* Tue Dec 20 2005 - damien.carbery@sun.com
- Bump to 2.9.1. Remove upstream patch 05-logname. Add intltool BuildRequires.
* Tue Nov 29 2005 - damien.carbery@sun.com
- Bump to 2.8.4.
* Mon Nov 28 2005 - laca@sun.com
- prepare for building from CVS snapshots:
- use a macro for Version
- fix autotool order, add some more
- cp mkinstalldirs so that we don't need to add even more autotool foo
* Tue Oct 11 2005 - damien.carbery@sun.com
- Bump to 2.8.3
* Tue Sep 27 2005 - glynn.foster@sun.com
- Bump to 2.8.2
* Mon Aug 15 2005 - glynn.foster@sun.com
- Bump to 2.8.0
* Wed Jun 15 2005 - matt.keenan@sun.com
- Bump to 2.6.5
- Remove patch glib-04-uninstalled-pc.diff
* Fri May 06 2005 - brian.cameron@sun.com
- Add patch 04 to add needed uninstalled.pc files to allow other
  base-libs libraries to build.  This requires calling autoconf
  aclocal, etc.
- Fix naming of patches since the patches were renamed but this
  spec file not updated.
* Fri May 06 2005 - glynn.foster@sun.com
- Bump to 2.6.4
* Wed Nov 15 2004 - glynn.foster@sun.com
- Bump to 2.4.8, since otherwise glib-gettextize doesn't create 
  mkinstalldirs properly, and consequently it means I can't create
  tarballs from CVS sources. We also get a rake of nice bug fixes
  as a result.
* Fri Nov 12 2004 - brian.cameron@sun.com
- Modify the default path that glib sets (if the user does not have PATH
  set), so it does not include "." since ARC determined this is a
  security concern.  When building on Sun, set it to just "/usr/bin"
  since "/bin" is a symlink to "/usr/bin".  On Linux set it to
  "/bin:/usr/bin".
* Fri Oct 29 2004 - laca@sun.com
- use $CC64 for the 64-bit build if defined
* Wed Oct 05 2004 - Yong.Sun@Sun.COM
- Added glib-04-convert-utf8.diff to fix CR 5055972
* Sat Oct  2 2004 - Joseph.Townsend@Sun.COM
- Create 64bit libraries for Solaris
* Thu Sep 16 2004 - ciaran.mcdermott@sun.com
- Added glib-03-g11n-allinguas.diff to include hu lingua
* Wed Aug 18 2004 - brian.cameron@sun.com
- added --enable-gtk-doc
* Thu Aug 05 2004 - archana.shah@wipro.com
- Add patch to fix glib get SIGCHLD everytime
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to glib2-l10n-po-1.2.tar.bz2
* Thu Jul 08 2004 - stephen.browne@sun.com
- ported to rpm4/suse91
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Fri May 14 2004 - glynn.foster@sun.com
- Bump to 2.4.1
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to glib2-l10n-po-1.1.tar.bz2
* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to glib2-l10n-po-1.0.tar.bz2
* Wed Mar 24 2004 - <glynn.foster@sun.com>
- Bump to 2.4.0
* Wed Mar 10 2004 - <niall.power@sun.com>
- remove glib-02 patch (it wasn't being applied anyway).
- bump to 2.3.6
* Thu Feb 19 2004 - <damien.carbery@sun.com>
- Add patch for glib/gmessages.h to change '...' to '__VA_ARGS__' to build
  on Solaris. May revisit to use '#ifdef __sun'
* Tue Feb 10 2004 - <matt.keenan@sun.com>
- Bump to 2.3.2, l10n to 0.7
* Mon Dec 15 2003 - <glynn.foster@sun.com>
- update to 2.3.1
* Sat Oct 04 2003 - <laca@sun.com>
- update to 2.2.3
* Thu Aug 14 2003 - <laca@sun.com>
- move lib*.so to -devel, remove *.a, *.la
* Fri Aug 01 2003 - <markmc@sun.com> 2.2.2-1
* Wed Jul 25 2003 - <niall.power@sun.com>
- add aaa_base dependency. Fixes postinstall script breakage
  during OS install.
* Wed Jul 09 2003 - <michael.twomey@sun.com>
- add in sun po files
* Thu May 12 2003 - <ghee.teo@sun.com>
- Initial spec file for glib2
