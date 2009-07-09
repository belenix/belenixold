#
# spec file for package gnome-games
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: migi
#
Name:         gnome-games
License:      GPL
Group:        Amusements/Games
Version:      2.26.0
Release:      1
Distribution: Java Desktop System
Vendor:	      Sun Microsystems, Inc.
Summary:      GNOME games
Source:       http://ftp.gnome.org/pub/GNOME/sources/%{name}/2.26/%{name}-%{version}.tar.bz2
# owner:davelam date:2008-05-14 type:bug bugzilla:532093
Patch1:       gnome-games-01-add-libz.diff
URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/%{name}
Autoreqprov:  on
Prereq:       GConf

%define python_version 2.4
%define libgnomeui_version 2.2.0
%define scrollkeeper_version 0.3.11

BuildRequires: libgnomeui-devel >= %{libgnomeui_version}
BuildRequires: scrollkeeper >= %{scrollkeeper_version}
BuildRequires: intltool
Requires:      libgnomeui >= %{libgnomeui_version}

%description
The gnome-games package includes some small games that come with the
GNOME desktop environment but can be used under any desktop.
The games are mostly puzzle or solitaire games.

%prep
%setup -q
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

export install_user=$LOGNAME
export install_group=`groups | awk '{print $1}'`

# Force the update of aclocal.m4 to incorporate the modified sdl.m4. Otherwise
# configure fails because /usr/bin/xgettext is checked instead of the CBE
# version which is GNU xgettext.
aclocal --force $ACLOCAL_FLAGS -I m4
libtoolize --force --copy
automake -a -c -f
autoconf --force

# Ommitted games:
# - aisleriot depends on guile headers.  We can add this game after we add
#   guile to our builds.
# - gnometris is removed.
#
./configure --prefix=%{_prefix} 	\
	    --sysconfdir=%{_sysconfdir} \
	    --bindir=%{_bindir} \
	    --libdir=%{_libdir} \
       --includedir=%{_includedir} \
	    --libexecdir=%{_libexecdir} \
	    --with-scores-user=$install_user   \
	    --with-scores-group=$install_group \
	    --with-sound=gstreamer   \
	    --disable-setgid \
	    --disable-scrollkeeper \
	    --with-libggz-includes=%{libggz_build_dir}/src \
	    --with-libggz-libraries=%{libggz_build_dir}/src/.libs \
	    --with-ggzmod-includes=%{ggzclient_build_dir}/ggzmod \
	    --with-ggzmod-libraries=%{ggzclient_build_dir}/ggzmod/.libs \
	    --with-ggz-server=force \
	    --enable-omitgames=aisleriot,gnometris

make -j $CPUS \
	pythondir=%{_libdir}/python%{python_version}/vendor-packages

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
%makeinstall localstatedir=%{_localstatedir}/lib \
	pythondir=%{_libdir}/python%{python_version}/vendor-packages
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

## things we just don't want in the package
rm -rf $RPM_BUILD_ROOT/var/lib/scrollkeeper
find $RPM_BUILD_ROOT -type f -name "*.pyo" -exec rm {} ';'

## install desktop files

%find_lang %{name}

#Copy zh_HK from zh_TW
#Fixes bug 4930405
install -d $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES
install --mode=0644 $RPM_BUILD_ROOT%{_datadir}/locale/zh_TW/LC_MESSAGES/*.mo $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES/

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
SCHEMAS="blackjack.schemas gataxx.schemas glines.schemas gnect.schemas gnibbles.schemas gnobots2.schemas gnomine.schemas gnotravex.schemas gtali.schemas iagno.schemas mahjongg.schemas same-gnome.schemas"
for S in $SCHEMAS; do
  gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$S > /dev/null
done

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog

# these are not setgid games
%{_bindir}/games-server.py
%{_bindir}/gnect
%{_bindir}/blackjack

%{_localstatedir}/lib

# these are setgid games
%attr(2551, root, games) %{_bindir}/gnomine
%attr(2551, root, games) %{_bindir}/same-gnome
%attr(2551, root, games) %{_bindir}/mahjongg
%attr(2551, root, games) %{_bindir}/gtali
%attr(2551, root, games) %{_bindir}/gnobots2
%attr(2551, root, games) %{_bindir}/gataxx
%attr(2551, root, games) %{_bindir}/gnotravex
%attr(2551, root, games) %{_bindir}/gnotski
%attr(2551, root, games) %{_bindir}/gnibbles
%attr(2551, root, games) %{_bindir}/glines
%attr(2551, root, games) %{_bindir}/iagno

%{_datadir}/applications
%{_datadir}/blackjack
%{_datadir}/gnect
%{_datadir}/gnibbles
%{_datadir}/gnobots2
%{_datadir}/gnome
%{_datadir}/gnome-games
%{_datadir}/locale/zh_HK/LC_MESSAGES
%{_datadir}/omf
%{_datadir}/pixmaps
%{_datadir}/sounds
%{_sysconfdir}/gconf/schemas/*
%config %{_sysconfdir}/sound/events/*

%changelog
* Tue Mar 17 2009 - dave.lin@sun.com
- Bump to 2.26.0.
* Fri Mar 13 2009 - dave.lin@sun.com
- Bump to 2.25.92
* Tue Mar 03 2009 - brian.cameron@sun.com
- Remove gnometris game.
* Tue Feb 17 2009 - dave.lin@sun.com
- Bump to 2.25.91
* Mon Feb 16 2009 - dave.lin@sun.com
- Bump to 2.25.90
* Tue Feb 03 2009 - Michal.Pryc@Sun.Com
- Removed gnome-games-02-libice.diff: Fixed upstream. 
* Fri Jan 30 2009 - Michal.Pryc@Sun.Com
- Bump to 2.25.5
- Removed gnome-games-03-string.diff. Patch applied upstream.
- gnome-games-02-libice.diff: Reworked.
* Thu Jan 08 2009 - Michal.Pryc@Sun.Com
- Added patch gnome-games-03-string.diff. bugzilla: 566797 
* Fri Dec 26 2008 - dave.lin@sun.com
- Added patch 02-libice.diff.
- Removed upstreamed patch 02-blackjack.diff.
* Wed Dec 03 2008 - dave.lin@sun.com
- Bump to 2.25.2
* Thu Oct 02 2008 - brian.cameron@sun.com
- Add blackjack and gnometris back to gnome-games.
* Mon Sep 29 2008 - christian.kelly@sun.com
- Bump to 2.24.0.
* Wed Sep 10 2008 - christian.kelly@sun.com
- Bump to 2.23.92.
* Tue Aug 19 2008 - dave.lin@sun.com
- Bump to 2.23.90
* Tue Aug 05 2008 - damien.carbery@sun.com
- Bump to 2.23.6. Add libtoolize call to override included libtool version.
* Mon Jul 21 2008 - damien.carbery@sun.com
- Bump to 2.23.5.
* Tue Jun 17 2008 - damien.carbery@sun.com
- Bump to 2.23.4.
* Fri Jun 6 2008 - Michal.Pryc@Sun.Com
- added --with-ggz-server=force
* Tue Jun 03 2008 - damien.carbery@sun.com
- Bump to 2.23.3.
* Wed May 28 2008 - damien.carbery@sun.com
- Bump to 2.23.1.
* Tue May 27 2008 - damien.carbery@sun.com
- Bump to 2.22.2.
* Wed May 14 2008 - dave.lin@sun.com
- Add patch gnome-games-01-add-libz.diff to fix build error
* Wed Apr 09 2008 - damien.carbery@sun.com
- Bump to 2.22.1.1. Remove upstream patch 01-skip-ggz-check.
* Tue Mar 25 2008 - damien.carbery@sun.com
- Add --with-sound=gstreamer to configure to ensure that sound support is built
  in. 
* Tue Mar 11 2008 - damien.carbery@sun.com
- Bump to 2.22.0.
* Thu Feb 28 2008 - brian.cameron@sun.com
- Use %{ggzclient_build_dir} instead of %{ggzmod_build_dir} since this
  is more accurate naming.  The module is ggz_client_libs.
* Tue Feb 26 2008 - damien.carbery@sun.com
- Bump to 2.21.92.
* Wed Feb 13 2008 - damien.carbery@sun.com
- Bump to 2.21.91.
* Tue Jan 29 2008 - damien.carbery@sun.com
- Bump to 2.21.90.
* Fri Jan 25 2008 - damien.carbery@sun.com
- Force the update of aclocal.m4 to incorporate the modified sdl.m4. Otherwise
  configure fails because /usr/bin/xgettext is checked instead of the CBE
  version which is GNU xgettext.
* Tue Jan 15 2008 - damien.carbery@sun.com
- Bump to 2.21.5.
* Wed Jan 09 2008 - damien.carbery@sun.com
- Remove 02-msgfmt patch, instead set ACLOCAL_FLAGS in SUNWgnome-games.spec to
  pick up modified intltool.m4.
* Mon Jan 07 2008 - patrick.ale@gmail.com
- Add patch gnome-games-02-msgfmt.diff
* Mon Jan 07 2008 - damien.carbery@sun.com
- Specify ggzmod location in configure.
* Wed Jan 02 2008 - damien.carbery@sun.com
- Use variable from SUNWgnome-games.spec to specify libggz location. Add patch
  01-skip-ggz-check to set compiler flags to get libggz search test work.
* Tue Dec 18 2007 - damien.carbery@sun.com
- Bump to 2.21.4.
* Tue Dec 04 2007 - damien.carbery@sun.com
- Bump to 2.21.3.
* Tue Nov 13 2007 - damien.carbery@sun.com
- Bump to 2.21.2.
* Tue Oct 30 2007 - damien.carbery@sun.com
- Bump to 2.21.1.
* Fri Oct 19 2007 - damien.carbery@sun.com
- Bump to 2.20.1.
* Tue Oct  9 2007 - damien.carbery@sun.com
- Add --disable-setgid to configure so that the games are not setgid-bin, which
  violates ARC rules.
* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 2.20.0.1. Remove upstream patch, 01-func-decl.
* Mon Sep 03 2007 - damien.carbery@sun.com
- Bump to 2.19.92. Add patch, 01-func-decl, to fix #473327.
* Wed Aug 29 2007 - damien.carbery@sun.com
- Bump to 2.19.91.1.
* Tue Aug 28 2007 - damien.carbery@sun.com
- Bump to 2.19.91. Remove upstream patch, gnome-menus-05-iconv-solaris.
* Thu Aug 16 2007 - damien.carbery@sun.com
- Add patch gnome-menus-05-iconv-solaris to fix #467309. Modify
  intltool-merge.in to allow use of non-GNU iconv.
* Wed Aug 15 2007 - damien.carbery@sun.com
- Bump to 2.19.90.1.
* Wed Aug 15 2007 - damien.carbery@sun.com
- Bump to 2.19.90b. Remove upstream patch, 01-build-gnometris.
* Mon Jul 30 2007 - damien.carbery@sun.com
- Bump to 2.19.6. Remove upstream patches, 01-strrchr and 03-ggz-signed-char.
  Renumber remainder.
* Tue Jun 19 2007 - damien.carbery@sun.com
- Bump to 2.19.4. Remove upstream patches, 01-named-struct and 03-signed-char.
* Mon Jun 11 2007 - damien.carbery@sun.com
- Add patch 04-build-gnometris to fix build error in gnometris game. Filed
  bugzilla #446290. Also add some autofoo calls to incorporate updates ggz.m4
  file (modified in patch3).
* Fri Jun 08 2007 - damien.carbery@sun.com
- Add patch, 03-signed-char, for #445556.
* Wed Jun 06 2007 - damien.carbery@sun.com
- Bump to 2.19.3. Add patches to fix some build errors.
* Fri May 18 2007 - matt.keenan@sun.com
- Add glchess.desktop back in bugzilla 426538 now fixed in 2.19.1.1
* Wed May 16 2007 - damien.carbery@sun.com
- Bump to 2.19.2.
* Wed May 09 2007 - damien.carbery@sun.com
- Bump to 2.19.1.
* Fri May 04 2007 - damien.carbery@sun.com
- Bump to 2.18.1.1.
* Thu Apr 12 2007 - damien.carbery@sun.com
- Bump to 2.18.1.
* Thu Apr 05 2007 - matt.keenan@sun.com
- Remove glchess.desktop, until glchess is made functional on Solaris
- Bugzilla : 426538, bugster : 6537569
* Wed Mar 21 2007 - damien.carbery@sun.com
- Bump to 2.18.0.1.
* Tue Mar 13 2007 - damien.carbery@sun.com
- Bump to 2.18.0.
* Mon Mar 05 2007 - damien.carbery@sun.com
- Bump to 2.17.92. Removed upstream patch, 01-grep-no-q.
* Thu Feb 15 2007 - damien.carbery@sun.com
- Add patch, 01-grep-no-q.diff, to remove '-q' from grep calls. Fixes 408331.
  Specify build user/group so that chown calls don't fail; disable building
  of aisleriot game (removing code from SUNWgnome-games.spec).
* Tue Feb 13 2007 - damien.carbery@sun.com
- Bump to 2.17.91.
* Wed Jan 24 2007 - damien.carbery@sun.com
- Bump to 2.17.90.1.
* Mon Jan 22 2007 - damien.carbery@sun.com
- Bump to 2.17.90.
* Mon Jan 08 2007 - damien.carbery@sun.com
- Bump to 2.17.5. Remove upstream patch 01-ggz-function.
* Wed Dec 20 2006 - damien.carbery@sun.com
- Bump to 2.17.4.1. Add patch 01-ggz-function to fix #363444.
* Tue Dec 19 2006 - damien.carbery@sun.com
- Bump to 2.17.4.
* Thu Dec 07 2006 - damien.carbery@sun.com
- Bump to 2.17.3. Remove upstream patches, 01-array-init and 02-ggz-function.
  Remove obsolete 'rm' calls in %install (those files/dirs no longer installed).
  Install python libs to vendor-packages dir and remove *.pyo files.
* Fri Nov 24 2006 - damien.carbery@sun.com
- Add patches 01-array-init to fix 363438 and 02-ggz-function to fix 362444.
* Wed Nov 22 2006 - damien.carbery@sun.com
- Bump to 2.17.1.
* Thu Nov 09 2006 - damien.carbery@sun.com
- Bump to 2.16.1.1.
* Tue Oct 03 2006 - damien.carbery@sun.com
- Bump to 2.16.1.
* Tue Sep 05 2006 - damien.carbery@sun.com
- Bump to 2.16.0.
* Tue Aug 22 2006 - damien.carbery@sun.com
- Bump to 2.15.92.
* Tue Aug 08 2006 - damien.carbery@sun.com
- Bump to 2.15.6.
* Mon Jul 24 2006 - damien.carbery@sun.com
- Bump to 2.15.5.
* Web Jul 21 2006 - dermot.mccluskey@sun.com
- Bump to 2.15.4.
* Mon Jun 26 2006 - laca@sun.com
- remove patch menu-entry.diff since gnome-games is moving back to /usr
* Fri Jun 23 2006 - brian.cameron@sun.com
- Bump to 2.14.2.
* Fri Apr 10 2006 - damien.carbery@sun.com
- Bump to 2.14.
* Mon Mar 13 2006 - damien.carbery@sun.com
- Bump to 2.14.
* Thu Feb 23 2006 - damien.carbery@sun.com
- Bump to 2.13.8.
* Mon Feb 13 2006 - damien.carbery@sun.com
- Bump to 2.13.7.
* Sat Jan 21 2006 - damien.carbery@sun.com
- Remove upstream patch, 02-illegal-cast.
* Tue Jan 17 2006 - damien.carbery@sun.com
- Bump to 2.13.5
* Sun Jan 15 2006 - damien.carbery@sun.com
- Bump to 2.13.4.
* Sat Jan 07 2006 - damien.carbery@sun.com
- Add patch, 02-illegal_cast, to fix compilation errors; bugzilla 326024.
* Tue Dec 20 2005 - dermot.mccluskey@sun.com
- Bump to 2.13.3
* Fri Dec 02 2005 - srirama.sharma@wipro.com
- Added gnome-games-01-sfw-path.diff to use the absolute path of the 
  executable in the .desktop file as usr/sfw/bin should not be 
  included in $PATH.
  Fixes bug #6345489.
* Tue Nov 29 2005 - laca.com
- remove javahelp stuff
* Tue Nov 29 2005 - damien.carbery@sun.com
- Bump to 2.12.2.
* Wed Oct 12 2005 - damien.carbery@sun.com
- Remove patch as offending struct is no longer empty.
* Tue Oct 11 2005 - damien.carbery@sun.com
- Bump to 2.12.1
* Sat Sep 17 2005 - glynn.foster@sun.com
- Bump to 2.12.0
* Mon Sep 05 2005 - damien.carbery@sun.com
- Bump to 2.11.5.
* Fri Sep 02 2005 - damien.carbery@sun.com
- Add patch to fix zero sized struct Solaris build error.
* Wed Aug 24 2005 - damien.carbery@sun.com
- Add patch to remove blank line 1 from same-gnome.xml (javahelp had prob).
* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 2.11.4.
* Fri May 20 2005 - glynn.foster@sun.com
- Bump to 2.10.1
* Wed May 11 2005 - ciaran.mcdermott@sun.com
- added gnome-games-05-g11n-desktop-fix.diff 
- to fix CR 6266891
* Wed Apr 27 2005 - kieran.colfer@sun.com
- added gnome-games-04-po-install-fixes.diff for CR 6243601
* Fri Nov 12 2004 - laca@sun.com
- added --libdir and --bindir to configure opts so they can be redirected on
  Solaris
* Mon Sep 20 2004 - dermot.mccluskey@sun.com
- removed sol from files
* Thu Sep 04 2004 - laslzo.kovacs@sun.com
- packaged sol
* Thu Aug 26 2004 - damien.carbery@sun.com
- Put scores files in %{_localstatedir}/lib.
* Wed Aug 25 2004 - damien.carbery@sun.com
- Add unpackaged files to %files.
* Mon Aug 23 2004 - niall.power@sun.com
- remove auto*-jds tool dependencies
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-games-l10n-po-1.2.tar.bz2
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Tue Jun 1 2004 - glynn.foster@sun.com
- Fix up schema install
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-games-l10n-po-1.1.tar.bz2
* Fri May 07 2004 - matt.keenan@sun.com
- Bump to 2.6.1
* Wed Apr 21 2004 - laca@sun.com
- disable javahelp conversion for stuff not built on Solaris
* Sun Apr 18 2004 - laca@sun.com
- enable javahelp conversion on Solaris
* Fri Apr 02 2004 - brian.cameron@sun.com
- Added patch 03 to fix Solaris Makefile issue, and added libexecdir to
  configure line.
* Thu Apr 01 2004 - matt.keenan@sun.com
- javahelp conversion
* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-games-l10n-po-1.0.tar.bz2
* Wed Mar 24 2004 - glynn.foster@sun.com
- Use JDS autotools
* Tue Mar 23 2004 - glynn.foster@sun.com
- Bump to 2.6.0. Remove 2 potfile patches and 
  replace with a single one.
* Thu Mar 11 2004 - yuriy.kuznetsov@sun.com
- added gnome-games-03-g11n-potfiles.diff
* Fri Feb 06 2004 - <matt.keenan@sun.com>
- Bump up 2.5.5, remove intltool-merge patch
- re-engineered patch-01, as automake etc is commented out.
- This could be changed again if automake 1.7 was being used not 1.6 !!
* Thu Jan 29 2004 - <dermot.mccluskey@sun.com>
- add patch 03 for intltool-merge and dep. on intltool
* Fri Dec 29 2003 - <niall.power@sun.com>
- comment out libtool, aclocal etc. which 
  is causing build failure
* Fri Dec 29 2003 - <glynn.foster@sun.com>
- Bump to 2.5.3
* Wed Dec 17 2003 - <glynn.foster@sun.com>
- Bump to 2.5.2
* Fri Oct 31 2003 - <glynn.foster@sun.com>
- Remove the Sun Supported keyword from the desktop 
  files. We're removing the Extras menu.
* Wed Oct 22 2003 - <glynn.foster@sun.com>
- Add blackjack into the build
* Tue Oct 21 2003 - <michael.twomey@sun.com>
- Updated to GNOME 2.4.0 version
- Removed freecell entries
- Moved gnome-games-03-menu-entry.diff patch to 
  gnome-games-01-menu-entry.diff
- Dropped gnome-games-04-glines-preferences.diff patch.
* Thu Aug 14 2003 - <laca@sun.com>
- remove *.so, *.a, *.la
* Wed Aug 06 2003 - <glynn.foster@sun.com>
- fix glines preference dialog
* Thu Jul 17 2003 - <glynn.foster@sun.com>
- remove more xbill stuff
* Wed Jul 09 2003 - <michael.twomey@sun.com>
- add in sun po files
* Tue Jul 08 2003 - glynn.foster@sun.com
- Add menu icon for freecell, and add aclocal, automake checks
* Tue May 13 2003 - ghee.teo@Sun.COM
- Created new spec file for gnome-games

