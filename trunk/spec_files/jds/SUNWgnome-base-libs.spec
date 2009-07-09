#
# spec file for package SUNWgnome-base-libs
#
# includes module(s): none
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: erwannc
#
%include Solaris.inc

Name:                    SUNWgnome-base-libs
Summary:                 GNOME base GUI libraries
Version:                 %{default_pkg_version}
SUNW_Copyright:          %{name}.copyright

Requires: SUNWglib2
Requires: SUNWcairo
Requires: SUNWpango
Requires: SUNWlibatk
Requires: SUNWgtk2
Requires: SUNWlibglade
Requires: SUNWlibart
Requires: SUNWlibgnomecanvas

%package root
Summary:                 %{summary} - / filesystem
Requires: SUNWpango-root
Requires: SUNWgtk2-root

%package devel		
Summary:                 %{summary} - development files
Requires: SUNWglib2-devel
Requires: SUNWcairo-devel
Requires: SUNWpango-devel
Requires: SUNWlibatk-devel
Requires: SUNWgtk2-devel
Requires: SUNWlibglade-devel
Requires: SUNWlibart-devel
Requires: SUNWlibgnomecanvas-devel

%files
# empty package

%files devel
# empty package

%files root
# empty package

%changelog
* Tue Mar 31 2009 - dave.lin@sun.com
- Split SUNWgnome-base-libs into
    SUNWglib2
    SUNWcairo
    SUNWpango
    SUNWlibatk
    SUNWgtk2
    SUNWlibglade
    SUNWlibart
    SUNWlibgnomecanvas
  And keep SUNWgnome-base-libs as empty packages for dependency compatibility.
* Tue Mar 24 2009 - jeff.cai@sun.com
- Add dependencies on SUNWlxml-devel, SUNWxwinc, SUNWxorg-header
  for the development package
- Change SUNWpixman to a hard dependency
* Fri Jan 09 2009 - christian.kelly@sun.com
- Add SUNWgtk-doc as a BuildRequires.
* Wed Dec 10 2008 - dave.lin@sun.com
- Change PKG_CONFIG_PATH=.../cairo-%{cairo.version}:...
* Mon Dec 08 2008 - dave.lin@sun.com
- Removed empty dirs /usr/lib/gio, /usr/lib/%{_arch64}/gio
* Tue Nov 18 2008 - darren.kenny@sun.com
- Remove references to building pixman since we should now be on the system
  (delivered by X).
- Add Requires statement for SUNWpixman.
* Wed Sep 17 2008 - ghee.teo@sun.com
- Added %doc to %files for new copyright format.
* Tue Jun 08 2008 - christian.kelly@sun.com
- Bumped gtk+ to 2.13.4
* Tue Jun 03 2008 - damien.carbery@sun.com
- Remove gail module as it is not incorporated into gtk+. Update %files for
  new location of 64 bit gail libs.
* Wed May 21 2008 - damien.carbery@sun.com
- Add 'Requires: SUNWcupsu' to devel package to fix #6705123.
* Fri Apr 18 2008 - darren.kenny@sun.com
- Statically link in pixman into cairo, so don't ship libpixman.
- This is a temporary workaround until the X server provide libpixman.
* Tue Apr 15 2008 - erwann.chenede@sun.com
- added pixman module
* Tue Jan 22 2008 - damien.carbery@sun.com
- Remove pixman module as cairo has been reverted to 1.4.14.
* Thu Jan 17 2008 - damien.carbery@sun.com
- Add pixman module, as required by cairo 1.5.6.
* Wed Dec 26 2007 - damien.carbery@sun.com
- Add gtester and gtester-report to %files, introduced by glib 2.15.0.
* Wed Oct 10 2007 - damien.carbery@sun.com
- Remove 'Requires: SUNWgnome-doc-utils' as it is only used during building;
  change SUNWgnome-doc-utils-devel to SUNWgnome-doc-utils to match change in
  SUNWgnome-doc-utils.spec.
* Tue Oct  2 2007 - laca@sun.com
- set CFLAGS and LDFLAGS for GNU libintl/libiconv
* Sat Sep 29 2007 - damien.carbery@sun.com
- Run gtk-query-immodules-2.0 in %post instead of using a class action script
  which does not remove invalid entries. Fixes 6550492.
* Fri Sep 28 2007 - laca@sun.com
- add optional GNU libiconv and FOX dependencies instead of the Nevada
  equivalents
* Fri Sep 07 2007 - damien.carbery@sun.com
- Add gtk-builder-convert.1 manpage to %files.
* Thu Jul 12 2007 - damien.carbery@sun.com
- Add gail module and associated %files. It is a prerequisite of libgnomecanvas
  now.
* Wed Jul 04 2007 - damien.carbery@sun.com
- Add gtk-builder-convert to %files.
* Mon May 29 2007 - damien.carbery@sun.com
- Remove 'rm $RPM_BUILD_ROOT/var' and add im-multipress.conf to %files root as
  issue has been resolved.
* Fri May 25 2007 - damien.carbery@sun.com
- Remove $RPM_BUILD_ROOT/var in %install because gtk+ is installing to
  $RPM_BUILD_ROOT$RPM_BUILD_ROOT !
* Fri May 11 2007 - damien.carbery@sun.com
- Add Build/Requires SUNWgnome-doc-utils/-devel as required by atk.
* Thu Mar 15 2007 - laca@sun.com
- convert to new style of building multiple ISAs as per docs/multi-ISA.txt
* Mon Feb  5 2007 - damien.carbery@sun.com
- Add Requires SUNWpapi after check-deps.pl run.
* Fri Dec 01 2006 - takao.fujiwara@sun.com
- Added SUNWuiu8 dependency. Fixes 6499071
* Mon Oct 16 2006 - brian.cameron@sun.com
- Fix comment.
* Fri Oct 13 2006 - damien.carbery@sun.com
- Delete .a and .la files.
* Fri Sep 01 2006 - Matt.Keenan@sun.com
- New Manpage tarball
* Sun Aug 13 2006 - laca@sun.com
- delete %pre script (hack) and SUNWj5rt dep since we changed the icon dirs
  back to root:other
* Sat Aug 12 2006 - laca@sun.com
- set PERL to /usr/perl5/bin/perl as per CR6454456
* Fri Jul 21 2006 - damien.carbery@sun.com
- Add cairo dir to CFLAGS; update %install and %files for printbackends files.
* Fri Jul 14 2006 - laca@sun.com
- update %post/%postun/etc scripts to support diskless client setup,
  part of 6448317
* Thu Jul 13 2006 - damien.carbery@sun.com
- Add %{_bindir}/%{_arch64}/gtk-demo because of new tarball.
* Thu Jul  6 2006 - damien.carbery@sun.com
- Add BuildRequires SUNWlxml-devel as required by libglade.
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Wed May 10 2006 - laca@sun.com
- merge -share pkg(s) into the base pkg(s)
* Wed May 10 2006 - brian.cameron@sun.com
- Move gtk-demo to /usr/demo/jds/bin to meet ARC requirements.
* Mon Feb 20 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Sat Dec  3 2005 - laca@sun.com
- postrunify the gdk-pixbuf.loaders stuff
* Thu Sep 08 2005 - brian.cameron@sun.com
- Verified builds fine on Solaris, bump to 2.12.
* Tue Sep 06 2005 - laca@sun.com
- add to %files or remove unpackaged files
- add %post
- change _sysconfdir files to volatile (config)
* Fri Aug 26 2005 - damien.carbery@sun.com
- Add cairo.
* Mon Aug  1 2005 - damien.carbery@sun.com
- Add SUNWPython/-devel dependencies so that libglade-convert builds.
* Tue Jul 26 2005 - brian.cameron@sun.com
- Moved librsvg to SUNWlibrsvg.
* Mon Jul 11 2005 - brian.cameron@sun.com
- Added bin/rsvg-view and datadir/pixmaps to complete librsvg 
  packaging
* Tue Jun 14 2005 - laca@sun.com
- Added symlink to gdk/x11 so that the build can find gdkx.h
* Wed May 11 2005 - brian.cameron@sun.com
- Added libglade-convert to packaging.
* Mon May 9 2005 - brian.cameron@sun.com
- Fix setting of ACLOCAL_FLAGS so it builds with the 2.10 code.
* Tue Dec 14 2004 - brian.cameron@sun.com
- Add Requires SUNWmlib since we require SUNWmlib at runtime, not just
  build time.
* Tue Nov 16 2004 - laca@sun.com
- moved section 5 man page to share from devel-share
* Thu Nov 4 2004 - archana.shah@wipro.com
- Changed spec file to remove /etc/profile.d directory before packaging
  Fixes bug# 5097097
* Thu Oct 27 2004 - hidetoshi.tajima@sun.com
- fix typos for _arch64/gtk.immodules, fixes 6176001
* Thu Oct 21 2004 - laca@sun.com
- set PERL and PERL_PATH, fixes 5100958
* Wed Oct 13 2004 - laca@sun.com
- use _pkg_config_path64 in $PKG_CONFIG_PATH64
* Sat Oct 02 2004 - laca@sun.com
- added %pkgbuild_postprocess
* Sat Oct  2 2004 - Joseph.Townsend@Sun.COM
- Create 64bit libraries for Solaris
* Sat Sep 11 2004 - damien.carbery@sun.com
- Set LD_LIBRARY_PATH so Xrandr and Xrender found when running built files.
* Sat Sep 11 2004 - laca@sun.com
- Set LDFLAGS so Xrandr and Xrender can be found.
* Thu Sep 09 2004 - matt.keenan@sun.com
- Added librsvg-2.3, rsvg.1 manpages
* Mon Aug 30 2004 - shirley.woo@sun.com
- Bug 5091588 : include files and sman3/4 files should be in a separate devel
  package
* Mon Aug 23 2004 - laca@sun.com
- s/SUNWpl5u/SUNWperl584usr/
* Wed Aug 18 2004 - damien.carbery@sun.com
- Changed more manpage modes to 0755 for Solaris integration.
* Mon Aug 16 2004 - damien.carbery@sun.com
- Changed multiple manpage modes to 0755 for Solaris integration.
* Sat Jun 26 2004  shirley.woo@sun.com
- Changed install location to /usr/...
* Wed Jun 1 2004 - hidetoshi.tajima@sun.com
- remove unsupported input method modules
* Wed May 26 2004 - laca@sun.com
- add l10n subpackage
* Tue May 25 2004 - laca@sun.com
- add buildconflicts tags against glib/gtk 1.2 packages
* Wed May 19 2004 - brian.cameron@sun.com
- Added missing man pages.
* Fri Apr 23 2004 - laca@sun.com
- added SUNWfontconfig, MediaLib dependencies
* Sun Apr 04 2004 - laca@sun.com
- add some missing files to %files
* Wed Mar 24 2004 - brian.cameron@sun.com
- Added SGML man page integration
* Web Mar 10 2004 - laca@sun.com
- escape % chars in the sed commands
* Sat Feb 28 2004 - laca@sun.com
- add -D__STDC_VERSION__=199409L recommended by the compiler cteam
* Web Feb 25 2004 - laca@sun.com
- move libgnomecanvas here from SUNWgnome-libs
- move libart_lgpl here from SUNWgnome-libs
- move librsvg here from SUNWgnome-libs
* Fri Feb 13 2004 - Laszlo.Peter@sun.com
- add "-xc99=none -xCC" to make glib build on s10_51.
- fix mandir permissions
* Thu Feb 12 2004 - Niall.Power@sun.com
- insert dir attribute in front of directories so as not
  to recursively suck up all it's contents
* Mon Jan 19 2004 - Laszlo.Peter@sun.com
- generate module list config files in %install
* Fri Jan 9 2004 - Laszlo.Peter@sun.com
- initial Sun release.
