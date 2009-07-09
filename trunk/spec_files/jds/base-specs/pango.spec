#
# spec file for package pango
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: erwannc
#
Name:         pango
License:      LGPL
Group:        System/Libraries
Version:      1.24.0
# "grep pango_module_version configure.in" for the api version number.
%define module_api_version 1.6.0
Release:      1
Distribution: Java Desktop System
Vendor:	      Sun Microsystems, Inc.
Summary:      Library for layout and rendering of internationalized text
Source:       http://ftp.gnome.org/pub/GNOME/sources/pango/1.24/pango-%{version}.tar.bz2
#owner:dcarbery date:2007-06-20 type:bug bugzilla:449482 bugster:6571762
Patch1:       pango-01-no-xrender.diff
#owner:bewitche date:2007-07-31 type:bug bugzilla:466755 bugster:6556808 
Patch2:	      pango-02-hangul-face.diff

## Solaris CJK fonts include Latin scripts.
## - Add PANGO_SCRIPT_LATIN, PANGO_SCRIPT_GREEK, PANGO_SCRIPT_CYRILLIC,
## PANGO_SCRIPT_HAN, PANGO_SCRIPT_KATAKANA, PANGO_SCRIPT_HIRAGANA for ja and zh.
## - Add PANGO_SCRIPT_LATIN, PANGO_SCRIPT_HANGUL for ko.
#owner:fujiwara date:2009-04-02 type:feature bugster:6617438
Patch3:	      pango-03-solaris-cjk-font-table.diff

URL:          http://www.gtk.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/doc
Autoreqprov:  on
Prereq:       /sbin/ldconfig

%define freetype2_version 2.1.3
%define cairo_version 0.9.2
%define glib2_version 2.5.7
%define pkgconfig_version 0.15.0
%define XFree86_version 4.3.0
%define fontconfig_version 2.2.92

Requires:      freetype2 >= %{freetype2_version}
Requires:      cairo >= %{cairo_version}
Requires:      glib2 >= %{glib2_version}
Requires:      XFree86-libs >= %{XFree86_version}
Requires:      fontconfig >= %{fontconfig_version}
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: cairo-devel >= %{cairo_version}
BuildRequires: pkgconfig >= %{pkgconfig_version}
BuildRequires: freetype2-devel >= %{freetype2_version}
BuildRequires: XFree86-devel >= %{XFree86_version}

%description
Pango is a library for layout and rendering of text, with an emphasis on internationalization. 
It forms the core of text and font handling in GTK+ 2.0.

%package devel
Summary:      Development Library for layout and rendering of internationalized text
Group:        Development/Libraries
Requires:     %{name} = %{version}-%{release}
Requires:     glib2-devel >= %{glib2_version}
Requires:     cairo-devel >= %{cairo_version}
Requires:     freetype2-devel >= %{freetype2_version}
Requires:     XFree86-devel >= %{XFree86_version}

%description devel
Pango is a library for layout and rendering of text, with an emphasis on internationalization. 
It forms the core of text and font handling in GTK+ 2.0.

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

aclocal $ACLOCAL_FLAGS
libtoolize --force --copy
gtkdocize
autoheader
autoconf
automake -a -c -f
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix} \
            --mandir=%{_mandir} \
            --with-native-locale=yes \
            --with-xinput=xfree \
            --without-qt \
            --sysconfdir=%{_sysconfdir} \
            --libdir=%{_libdir} \
            --bindir=%{_bindir} \
	    %{gtk_doc_option}
make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/pango/%{module_api_version}/modules/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%{_bindir}/pango-querymodules > %{_sysconfdir}/pango/pango.modules

%postun
/sbin/ldconfig

%files
%defattr(-, root, root)
%{_bindir}/*
%{_libdir}/pango/*/*/*.so
%{_libdir}/libpango*-*.so.*
%{_bindir}/pango-querymodules
%{_sysconfdir}/pango/*
%{_mandir}/man1/*

%files devel
%defattr(-, root, root)
%{_libdir}/libpango*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_datadir}/gtk-doc/html/pango
%{_mandir}/man3/*

%changelog
* Sat Apr 04 2009 - dave.lin@sun.com
- export CFLAGS="%optflags" & LDFLAGS="%_ldflags" before configure.
* Thu Apr 02 2009 - takao.fujiwara@sun.com
- Add patch solaris-cjk-font-table.diff because Solaris CJK fonts include 
  latin scripts. 6617438.
* Mon Mar 30 2009 - takao.fujiwara@sun.com
- Remove patch pua.diff because pango doesn't support no space fonts.
  Bugzilla 456202.
* Tue Mar 17 2009 - dave.lin@sun.com
- Bump to 1.24.0
* Fri Feb 20 2009 - jedy.wang@sun.com
- Fix the broken download link.
* Fri Feb 13 2009 - matt.keenan@sun.com
- Bump to 1.23.0
* Tue Dec 09 2008 - chris.wang@sun.com
- Removed patch4 unamed-union.diff, as SS12 has supported unamed union
* Mon Dec 08 2008 - dave.lin@sun.com
- Bump to 1.22.3
* Wed Sep 10 2008 - christian.kelly@sun.com
- Bump to 1.21.6.
* Tue Aug 12 2008 - damien.carbery@sun.com
- Bump to 1.21.4.
* Tue Jun 17 2008 - damien.carbery@sun.com
- Bump to 1.21.3.
* Tue Jun 03 2008 - damien.carbery@sun.com
- Bump to 1.21.2.
* Thu May 29 2008 - damien.carbery@sun.com
- Bump to 1.21.1.
* Mon May 26 2008 - damien.carbery@sun.com
- Bump to 1.20.3.
* Thu Apr 10 2008 - damien.carbery@sun.com
- Bump to 1.20.2.
* Wed Apr 09 2008 - damien.carbery@sun.com
- Bump to 1.20.1.
* Mon Mar 10 2008 - damien.carbery@sun.com
- Bump to 1.20.0.
* Tue Feb 26 2008 - damien.carbery@sun.com
- Bump to 1.19.4.
* Tue Jan 22 2008 - damien.carbery@sun.com
- Bump to 1.19.3.
* Tue Dec 18 2007 - damien.carbery@sun.com
- Bump to 1.19.2.
* Tue Dec 04 2007 - damien.carbery@sun.com
- Bump to 1.19.1.
* Tue Oct 30 2007 - damien.carbery@sun.com
- Bump to 1.19.0.
* Fri Oct 19 2007 - damien.carbery@sun.com
- Bump to 1.18.3.
* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 1.18.2.
* Tue Aug 28 2007 - damien.carbery@sun.com
- Bump to 1.18.1.
* Tue Aug 21 2007 - damien.carbery@sun.com
- Bump to 1.18.0.
* Tue Jul 31 2007 - damien.carbery@sun.com
- Bump to 1.17.5.
* Tue Jul 31 2007 - chris.wang@sun.com
- Add patch pango-03-hangul-face.diff to fix gnome-about crash bug,
  bugster 6556808. The cause of bug is hangul shape engine haven't
  detect the existence of the font face before invoke it.
* Fri Jul 13 2007 - takao.fujiwara@sun.com
- Removed pango-01-fullwidth-space.diff for another fix.
- Updated pango-01-pua.diff for bugzilla 456202.
* Tue Jul 03 2007 - damien.carbery@sun.com
- Bump to 1.17.4.
* Tue Jun 19 2007 - damien.carbery@sun.com
- Bump to 1.17.3.
* Tue May 27 2007 - damien.carbery@sun.com
- Bump to 1.17.1.
* Wed May 16 2007 - damien.carbery@sun.com
- Bump to 1.17.0.
* Mon Apr 30 2007 - damien.carbery@sun.com
- Bump to 1.16.4.
* Tue Apr 24 2007 - damien.carbery@sun.com
- Bump to 1.16.3.
* Thu Apr 12 2007 - damien.carbery@sun.com
- Bump to 1.16.2.
* Thu Mar 15 2007 - laca@sun.com
- convert to new style of building multiple ISAs as per docs/multi-ISA.txt
* Wed Mar 15 2007 - dougs@truemail.co.th
- Removed adding ccdir to PATH
* Tue Mar 13 2007 - damien.carbery@sun.com
- Bump to 1.16.1.
* Tue Mar 06 2007 - damien.carbery@sun.com
- Add patch, 03-no-xrender, to skip xrender check. This can be removed when X
  server team delivers the xrender.pc file.
* Mon Mar 05 2007 - damien.carbery@sun.com
- Bump to 1.16.0.
* Tue Feb 13 2007 - damien.carbery@sun.com
- Bump to 1.15.6.
* Tue Jan 23 2007 - damien.carbery@sun.com
- Bump to 1.15.5.
* Thu Jan 18 2007 - damien.carbery@sun.com
- Bump to 1.15.4.
* Tue Jan 09 2007 - damien.carbery@sun.com
- Bump to 1.15.3.
* Thu Dec 21 2006 - damien.carbery@sun.com
- Bump to 1.15.2.
* Thu Dec 07 2006 - damien.carbery@sun.com
- Bump to 1.15.1. Update api module version to 1.6.0.
* Mon Nov 27 2006 - damien.carbery@sun.com
- Bump to 1.14.8.
* Fri Nov  3 2006 - laca@sun.com
- use %gtk_doc_option in configure so that it can be disabled using
  --without-gtk-doc
* Mon Oct 16 2006 - damien.carbery@sun.com
- Bump to 1.14.7.
* Fri Oct 13 2006 - damien.carbery@sun.com
- Bump to 1.14.6.
* Tue Oct 03 2006 - damien.carbery@sun.com
- Bump to 1.14.5.
* Tue Sep 26 2006 - damien.carbery@sun.com
- Bump to 1.14.4.
* Tue Sep 05 2006 - damien.carbery@sun.com
- Bump to 1.14.3.
* Wed Aug 23 2006 - damien.carbery@sun.com
- Bump to 1.14.2.
* Tue Aug 22 2006 - damien.carbery@sun.com
- Bump to 1.14.1.
* Wed Aug 09 2006 - damien.carbery@sun.com
- Bump to 1.14.0.
* Tue Aug 01 2006 - damien.carbery@sun.com
- Bump to 1.13.5.
* Wed Jul 26 2006 - damien.carbery@sun.com
- Bump to 1.13.4.
* Thu Jul 20 2006 - damien.carbery@sun.com
- Bump to 1.13.3.
* Fri Apr 28 2006 - damien.carbery@sun.com
- Bump to 1.12.2.
* Wed Apr 26 2006 - damien.carbery@sun.com
- Bump to 1.12.1.
* Mon Mar 13 2006 - damien.carbery@sun.com
- Bump to 1.12.0.
* Mon Feb 27 2006 - damien.carbery@sun.com
- Bump to 1.11.99.
- Remove upstream patch, 04-void-func.
* Wed Feb 22 2006 - damien.carbery@sun.com
- Added patch (04-void-func) to fix #332167 (void func returning value).
* Tue Feb 21 2006 - damien.carbery@sun.com
- Bump to 1.11.6.
* Mon Feb 13 2006 - damien.carbery@sun.com
- Bump to 1.11.5.
- Change path to modules from 1.4.0 to 1.5.0.
* Tue Jan 31 2006 - damien.carbery@sun.com
- Bump to 1.11.3.
* Tue Jan 17 2006 - glynn.foster@sun.com
- Bump to 1.11.2
* Tue Dec 20 2005 - damien.carbery@sun.com
- Bump to 1.11.1.
* Mon Nov 28 2005 - laca@sun.com
- prepare for building from CVS snapshots:
- use a macro for Version
- fix autotool order, add some more
- cp mkinstalldirs so that we don't need to add even more autotool foo
* Tue Oct 11 2005 - damien.carbery@sun.com
- Bump to 1.10.1
* Fri Aug 26 2005 - damien.carbery@sun.com
- Add patches to build on Solaris - fix uninstalled.pc and configure.in and
  aclocal/autoconf.
* Tue Aug 16 2005 - glynn.foster@sun.com
- Bump to 1.10.0
* Mon Aug 15 2005 - glynn.foster@sun.com
- Bump to 1.9.1
* Fri May 06 2005 - glynn.foster@sun.com
- Bump to 1.8.1
* Thu Dec 09 2004 - federic.zhang@sun.com
- add pango-05-family-list.diff back to build 25 with several modifications:
  - check whether enable_native_family is set or not, in order
    to not display korean family name in both de and fr locales
  - create fake face in pango_fc_family_list_faces for missing styles
* Tue Nov 30 2004 - federic.zhang@sun.com
- take the patch pango-05-family-list.diff out temporarily 
  will integrate it into build 25
* Mon Nov 22 2004 - federic.zhang@sun.com
- add patch pango-05-family-list.diff to fix 6198418
      localized font name is needed
* Fri Nov 12 2004 - federic.zhang@sun.com
- add patch pango-04-pua.diff to fix 6192581:
      pango should support PUA area.
* Fri Oct 29 2004 - laca@sun.com
- use $CC64 for the 64-bit build if defined
* Sun Oct 10 2004 - federic.zhang@sun.com
- add patch pango-03-disable-script.diff to fix 5098206
      Latin font should not be used for ASCII when monospace family.
- update patch pango-02-fullwidth-space.diff to fix 5068848
      [Cinnabar] Space width problem in gedit, evolution.
* Sat Oct  2 2004 - Joseph.Townsend@Sun.COM
- Create 64bit libraries for Solaris
* Wed Aug 18 2004 - brian.cameron@sun.com
- added --enable-gtk-doc.
* Fri Aug 06 2004 - <federic.zhang@sun.com>
- Removed pango-01-unihan.diff, 1.4.1 fixes the Unihan issue.
* Thu Aug 05 2004 - glynn.foster@sun.com
- Bump to 1.4.1
* Wed Jul 07 2004 - niall.power@sun.com
- ported to rpm4
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Thu Jul 01 2004 - <federic.zhang@sun.com>
- Added patch pango-03-fullwidth-space.diff to fix bug 5067780,
  [Cinnabar] Japanese space chars are corrupt at Sans/Monospace
* Wed Mar 28 2004 - <federic.zhang@sun.com>
- add patch pango-01-unihan.diff to fix 5038959
     Unihan issue should be resolved with current language tag
- add patch pango-02-broken-text.diff to fix 5038972
     pango wouldn't render the legacy encoding string
* Wed Mar 24 2004 - <glynn.foster@sun.com>
- Bump to 1.4.0
* Thu Mar 11 2004 - <glynn.foster@sun.com>
- Bumped to 1.3.6. Remove pua-character patch until it has been properly
  created. We're not keeping broken patches around.
* Tue Mar 02 2004 - <michael.twomey@sun.com>
- Bumped to 1.3.5
- Removed pango-01-fix_pc.diff, not needed anymore.
- Renamed pango-02-pua-character.diff to pango-01-pua-character.diff.
* Tue Feb 24 2004 - <matt.keenan@sun.com>
- Bump to 1.3.2
- Re-Marge patch pango-01-fix_pc.diff
- Port patch pango-02-pua-character.diff from QS, should have been done already
* Fri Jan 09 2004 - <laca@sun.com>
- add patch to fix a broken .pc file
- clean up for Solaris builds
* Mon Dec 15 2003 - <glynn.foster@sun.com>
- Updating to 1.3.1 tarball
* Mon Oct 06 2003 - <michael.twomey@sun.com> 1.2.5-1
- Updating to 1.2.5 from GNOME 2.4.0.
* Thu Aug 14 2003 - <laca@sun.com>
- remove *.a, *.la
* Fri Jul 25 2003 - Niall.Power@sun.com
- add XFree86-libs dependency so postinstall script 
  doesn't fail during OS install.
* Wed Jul 09 2003 - michael.twomey@sun.com
- updated to pango 1.2.3
* Tue May 13 2003 - Stephen.Browne@sun.com
- initial Sun release.
