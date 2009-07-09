#
# spec file for package gtk2
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: erwannc
#
%include l10n.inc
Name:         gtk2
License:      LGPL
Group:        System/Libraries
Version:      2.16.1
Release:      3
Distribution: Java Desktop System
Vendor:	      Sun Microsystems, Inc.
Summary:      GTK+ - GIMP Toolkit Library for creation of graphical user interfaces
Source:       http://ftp.gnome.org/pub/GNOME/sources/gtk+/2.16/gtk+-%{version}.tar.bz2
Source1:      gtk.unset-hack.sh
Source2:      gtk.unset-hack.csh
Source3:      %{name}-po-sun-%{po_sun_version}.tar.bz2
Source4:      l10n-configure.sh
#owner:erwannc date:2000-00-00 type:feature
Patch1:       gtk+-01-window-icons-for-message-dialog.diff
#owner:niall date:2003-07-11 type:feature
Patch2:       gtk+-02-fileseldlg-navbuttons.diff
#owner:erwannc date:2004-05-17 bugster:5035382 type:bug
Patch3:       gtk+-03-use-xim-for-all-locales.diff
#owner:erwannc date:2004-08-12 type:feature
Patch4:       gtk+-04-sun-copy-paste-keybindings.diff
#owner:erwannc date:2004-08-12 bugzilla:74223 type:feature
Patch5:       gtk+-05-sun-pgdn-pgup-keybindings.diff
#owner:laca    date:2004-09-18 type:feature
Patch6:       gtk+-06-solaris-2.0.0-compat.diff
#owner:erwannc date:2006-05-01 type:feature
Patch7:       gtk+-07-trusted-extensions.diff
# date:2006-09-17 bugster:6494571 bugzilla:382676 owner:gheet type:bug
Patch8:       gtk+-08-printing-papi-backend.diff
# date:2007-07-12 bugster:6563388 bugzilla:456137 owner:bewitche type:bug
Patch9:       gtk+-09-null-print.diff    
# date:2007-11-07 bugster:6625702 launchpad:144326 owner:erwannc type:bug
Patch10:      gtk+-10-gdk-window-null-checks.diff
# date:2008-08-14 bugzilla:546817 bugster:6725919 owner:bewitche type:bug
Patch11:      gtk+-11-hidewindow.diff
# date:2008-01-11 bugster:6630867 bugzilla:505857 owner:bewitche type:bug
Patch12:      gtk+-12-filechooser-enterkey.diff
# date:2008-03-25 bugster:6676839 owner:gheet type:bug
Patch13:      gtk+-13-printing-cups-support.diff
# date:2009-03-17 defect:7438 owner:erwannc type:bug
Patch14:      gtk+-14-fix-deprecated.diff
# date:2009-04-16 owner:yippi type:bug doo:7783 bugster:6825001 bugzilla:580079
Patch15:      gtk+-15-xfree-xinerama.diff
# date:2009-04-22 owner:yippi type:bug bugzilla:579884
Patch16:      gtk+-16-fix-module.diff
# date:2009-04-22 owner:gheet type:bug bugster:6795517
Patch17:      gtk+-17-default-print-ps.diff
# date:2009-04-24 owner:yippi type:bug bugster:6831308
Patch18:      gtk+-18-medialib.diff

BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/doc
Autoreqprov:  on
Prereq:       /sbin/ldconfig

%define cairo_version 0.9.2
%define atk_version 1.7.0
%define pango_version 1.9.0
%define glib2_version 2.7.1
%define libpng_version 1.2.5
%define libjpeg_version 6.2.0

BuildRequires: cairo-devel >= %{cairo_version}
BuildRequires: atk-devel >= %{atk_verGsion}
BuildRequires: pango-devel >= %{pango_version}
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: libpng-devel >= %{libpng_version}
BuildRequires: libjpeg >= %{libjpeg_version}
Requires:      cairo >= %{cairo_version}
Requires:      glib2 >= %{glib2_version}
Requires:      atk >= %{atk_version}
Requires:      pango >= %{pango_version}
Requires:      libpng >= %{libpng_version}
Requires:      libjpeg >= %{libjpeg_version}

%description
This fast and versatile library is used all over the world for all
GNOME applications, the GIMP and several others. Originally it was
written for the GIMP and hence has the name Gimp ToolKit. Many people
like it because it is small, efficient and very configurable.

%package devel
Summary:      Library for creation of graphical user interfaces
Group:        Development/Libraries/X11
Autoreqprov:  on
Requires:     %{name} = %{version}
Requires:     cairo-devel >= %{cairo_version}
Requires:     atk-devel >= %{atk_version}
Requires:     pango-devel >= %{pango_version}

%description devel
This fast and versatile library is used all over the world for all
GNOME applications, the GIMP and several others. Originally it was
written for the GIMP and hence has the name Gimp ToolKit. Many people
like it because it is small, efficient and very configurable.

%prep
%setup -q -n gtk+-%{version} 

# Fixes build error. Solaris msgfmt does not have '-c'.
for f in po/Makefile.in.in po-properties/Makefile.in.in ; do
  sed -e 's/$(GMSGFMT) -c/$(GMSGFMT)/g' $f > $f$$
  mv $f$$ $f
  d=`dirname $f`
  touch $d/*.po
done

%if %build_l10n
# workaround for bugster 6581452, bugzilla 457863
sh -x %SOURCE4 --disable-gnu-extensions

bzcat %SOURCE3 | tar xf -
cd po-sun; make; cd ..
%endif
%patch1 -p1
%patch2 -p1
%patch3 -p1

%ifos solaris
%patch4 -p1
%endif

%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1

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
aclocal $ACLOCAL_FLAGS -I .
gtkdocize
autoheader
automake -a -c -f
autoconf
export CFLAGS="%optflags -I/usr/X11/include"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix} \
            --libdir=%{_libdir} \
            --bindir=%{_bindir} \
            --datadir=%{_datadir} \
            --with-native-locale=yes \
	    --with-xinput=xfree \
            --mandir=%{_mandir} \
            --infodir=%{_infodir} \
	    --enable-shm \
            --enable-xim \
            --enable-fbmanager \
            --with-gdktarget=x11 \
	    --sysconfdir=%{_sysconfdir}	\
	    --enable-explicit-deps=yes	\
	    --without-libjasper		\
	    %{gtk_doc_option}

# Build needed uninstalled.pc file
make gdk-x11-2.0-uninstalled.pc

make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install
./mkinstalldirs $RPM_BUILD_ROOT%{_sysconfdir}/gtk-2.0
mkdir -p $RPM_BUILD_ROOT/etc/profile.d
cp %SOURCE1 $RPM_BUILD_ROOT/etc/profile.d/
cp %SOURCE2 $RPM_BUILD_ROOT/etc/profile.d
#Copy zh_HK from zh_TW
#Fixes bug 4930405
install -d $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES
install --mode=0644 $RPM_BUILD_ROOT%{_datadir}/locale/zh_TW/LC_MESSAGES/*.mo $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES/
rm $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/*/immodules/*.la
rm $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/*/loaders/*.la
rm $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/*/engines/*.la
rm $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/*/printbackends/*.la
rm $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/modules/*.la
rm $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%{_bindir}/gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules
%{_bindir}/gdk-pixbuf-query-loaders > %{_sysconfdir}/gtk-2.0/gdk-pixbuf.loaders

%postun
#If this is the last version of the package remove the config files
if [ $1 = 0 ]
then
	rm %{_sysconfdir}/gtk-2.0/gtk.immodules
	rm %{_sysconfdir}/gtk-2.0/gdk-pixbuf.loaders
fi
/sbin/ldconfig

%files 
%{_bindir}/*query*
%{_bindir}/gtk-update-icon-cache
%{_libdir}/lib*.so.*
%{_libdir}/gtk-2.0/*/immodules/*.so
%{_libdir}/gtk-2.0/*/loaders/*.so
%{_libdir}/gtk-2.0/*/engines/*.so
%{_datadir}/themes/*/*
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_sysconfdir}/profile.d/gtk.unset-hack.sh
%{_sysconfdir}/profile.d/gtk.unset-hack.csh
%dir %{_sysconfdir}/gtk-2.0
%{_mandir}/man1/*.gz

%files devel
%{_bindir}/*-demo
%{_bindir}/*-csource
%{_includedir}/gtk-2.0
%{_libdir}/lib*.so
%{_libdir}/gtk-2.0/include
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gtk-2.0
%{_datadir}/aclocal/*.m4
%{_datadir}/gtk-doc/html/*
%{_mandir}/man3/*.gz

%changelog -n gtk2
* Thu Apr 23 2009 - brian.cameron@sun.com
- Add patch gtk+-18-medialib.diff so that mediaLib only uses RTLD_PROBE
  to find umem_alloc.  This avoids tickling the lazy loading of all
  dependencies.
* Thu Apr 23 2009 - ghee.teo@sun.com
- Added patch gtk+-17-default-print-ps.diff.
* Wed Apr 22 2009 - brian.cameron@sun.com
- Add patch gtk+-16-fix-module.diff to fix bugzilla bug #579884.
* Thu Apr 16 2009 - brian.cameron@sun.com
- Add patch gtk+-15-xfree-xinerama.diff to fix problems with Xinerama not
  working.  See doo bug #7783 and bugster bug #6825001.
* Wed Apr 15 2009 - dave.lin@sun.com
- Bump to 2.16.1
* Tue Mar 17 2009 - dave.lin@sun.com
- Bump to 2.16.0
* Fri Mar 13 2009 - dave.lin@sun.com
- Bump to 2.15.5
* Wed Feb 18 2009 - dave.lin@sun.com
- Bump to 2.15.4
* Fri Feb 13 2009 - dave.lin@sun.com
- Bump to 2.15.3
* Thu Jan 08 2009 - christian.kelly@sun.com
- Remove old reference to patch14.
* Wed Jan 07 2009 - christian.kelly@sun.com
- Bump to 2.15.0.
- Remove gtk+-11-hidewindow.diff.
* Tue Dec 09 2008 - chris.wang@sun.com
- removed upstreamed patch 15 print-dbl-free
* Mon Dec 08 2008 - dave.lin@sun.com
- Bump to 2.14.5
* Sat Sep 27 2008 patrick.ale@gmail.com
- Correct download URL
* Thu Sep 25 2008 chris.wang@sun.com
- Add patch gtk+-15-print-dbl-free.diff to fix bugzilla 553241, the patch has 
  been accpted by upstream
* Wed 24 2008 ghee.teo@sun.com
- Remove gtk+-15-gdk-x-error.diff, #bugzilla:521371 is obsolete.
* Thu Sep 18 2008 - chris.wang@sun.com
- Add patch 02-gdk-x-error to fix bug 6717703
* Sat Sep 06 2008 - christian.kelly@sun.com
- Bump to 2.14.1.
* Tue Aug 19 2008 - dave.lin@sun.com
- Bump to 2.13.7
- Removed the upstreamed patches
    gtk+-16-sun-xinerama.diff
    gtk+-17-sun-xinerama-2.diff
    gtk+-18-void-func.diff
* Thu Aug 14 2008 - chris.wang@sun.com
- Add patch 19-hidewindow to fix bug 6725919, trunk code showed the window
  after reparent, this is not match with the API description. the slip unveiled
  a bug xtbin based FF plugin work no properly on Xsun. A new bug will log
  against this.
* Wed Aug 13 2008 - damien.carbery@sun.com
- Add patch 18-void-func to fix bugzilla 547555.
* Tue Aug 12 2008 - erwann.chenede@sun.com
- Bump to 2.13.6. Add patch 17-sun-xinerama-2 to make init_solaris_xinerama
  compile. Bugzilla 547456.
* Tue Jul 22 2008 - christian.kelly@sun.com
- Bump to 2.13.5.
* Tue Jun 24 2008 - damien.carbery@sun.com
- Add patch 17-gail-uninstalled to fix 536430.  Previous version of patch
  pointed to wrong gail .la file and required -lgailutil to be added to
  LDFLAGS of multiple modules. These modules can now have that change removed.
* Mon Jun 16 2008 - damien.carbery@sun.com
- Bump to 2.13.3. Remove upstream patch, 17-gail-uninstalled.
* Wed Jun 04 2008 - damien.carbery@sun.com
- Bump to 2.13.2.
* Sat May 31 2008 - damien.carbery@sun.com
- Add patch, 17-gail-uninstalled, to correct the paths in the
  gail-uninstalled.pc.in file. Fixes bugzilla #536430.
* Sat May 31 2008 - damien.carbery@sun.com
- Add --without-libjasper to configure as libjasper is not on Solaris.
* Tue Mar 25 2008 - ghee.teo@sun.com
- Added gtk+-15-printing-cups-support.diff
* Thu Mar 13 2008 - damien.carbery@sun.com
- Add -I/usr/X11/include to CFLAGS after update of SUNWwinc.
* Wed Mar 12 2008 - damien.carbery@sun.com
- Bump to 2.12.9.
* Tue Feb 26 2008 - damien.carbery@sun.com
- Revert to 2.12.8 as it 2.12.x will be in GNOME 2.22.
* Mon Feb 25 2008 - damien.carbery@sun.com
- Bump to 2.13.0.
* Wed Feb 13 2008 - damien.carbery@sun.com
- Bump to 2.12.8.
* Wed Feb 08 2008 - brian.cameron@sun.com
- Remove patch gtk+-08-blank-popup-menu-fix.diff.  The actual problem was
  fixed in separate bug 129463.  This patch causes combo buttons that are
  defined to be appears-as-lists to crash, since they do not have menus.
* Wed Jan 30 2008 - damien.carbery@sun.com
- Bump to 2.12.7.
* Tue Jan 29 2008 - damien.carbery@sun.com
- Bump to 2.12.6.
* Fri Jan 11 2008 - chris.wang@sun.com
- Add gtk+-14-filechooser-enterkey.diff to fix bug 6630867 Nautilus : icon 
  customization dialog box doesn't support Enter key by adding some dialog
  action with gtk_dialog_set_default_response to filechooser.
* Wed Jan 09 2008 - damien.carbery@sun.com
- Bump to 2.12.5.
* Tue Jan 08 2008 - damien.carbery@sun.com
- Bump to 2.12.4.
* Wed Dec 05 2007 - damien.carbery@sun.com
- Bump to 2.12.3.
* Mon Dec 03 2007 - takao.fujiwara@sun.com
- Added gtk+-13-g11n-xim-spotlocation.diff to replace the vte patch.
* Tue Nov 27 2007 - damien.carbery@sun.com
- Bump to 2.12.2.
* Mon Oct 22 2007 - damien.carbery@sun.com
- Bump to 2.12.1. Remove upstream patch, 12-g11n-filechooser-date.
* Tue Oct 16 2007 - takao.fujiwara@sun.com
- Add gtk+-12-g11n-filechooser-date.diff to fix correct encodings and cast.
* Wed Sep 19 2007 - brian.cameron@sun.com
- Fix URL so it can download.
* Wed Jul 25 2007 - damien.carbery@sun.com
- Add --enable-explicit-deps=yes to configure to ensure all libs mentioned in
  gdk-pixbuf-2.0.pc file (otherwise subsequent modules break).
* Tue Jul 24 2007 - damien.carbery@sun.com
- Bump to 2.11.6.
* Wed Jul 18 2007 - takao.fujiwara@sun.com
- Add l10n-configure.sh to remove "%Id". Fixes 6581452
* Thr Jul 12 2007 - chris.wang@sun.com
- Add patch gtk+-13-print-null.diff fix the bug gaim/pidgin dies on startup 
  with SIGABRT
* Tue Jul 03 2007 - damien.carbery@sun.com
- Bump to 2.11.5.
* Wed Jun 20 2007 - damien.carbery@sun.com
- Bump to 2.11.4.
* Mon Jun 18 2007 - damien.carbery@sun.com
- Bump to 2.11.3.
* Wed Jun 07 2007 - brian.cameron@sun.com
- Bump to 2.11.2.  Remove unneeded tooltip patch fixed upstream.
* Wed Jun 06 2007 - brian.cameron@sun.com
- Add patch gtk+-14=fixtooltip.diff to fix problem with tooltips crashing
  when the window they are associated with are destroyed before the 
  tooltip timeout function is called.
* Tue Jun 05 2007 - damien.carbery@sun.com
- Bump to 2.11.1. Remove upstream patch, 14-fix-destdir.
* Tue May 29 2007 - damien.carbery@sun.com
- Add upstream patch, 14-fix-destdir, to fix build error where two files are
  installed to $RPM_BUILD_ROOT/$RPM_BUILD_ROOT.
* Fri May 25 2007 - damien.carbery@sun.com
- Bump to 2.11.0.
* Thu May 03 2007 - damien.carbery@sun.com
- Bump to 2.10.12.
* Tue May 01 2007 - brian.cameron@sun.com
- Remove patch to add gdk-x11-uninstalled-pc.diff and instead call
  "make gdk-x11-2.0-uninstalled.pc" before calling "make".  According
  to bugzilla bug #304128, this is the right way to build this file.
* Thu Apr 12 2007 - takao.fujiwara@sun.com
- Add 'touch *.po' so that .mo files are compatible with Solaris gettext.
  Fixes 6544910
* Thu Mar 15 2007 - laca@sun.com
- convert to new style of building multiple ISAs as per docs/multi-ISA.txt
* Wed Mar 15 2007 - dougs@truemail.co.th
- Removed adding ccdir to PATH
* Wed Mar 14 2007 - damien.carbery@sun.com
- Bump to 2.10.11.
* Tue Mar 13 2007 - damien.carbery@sun.com
- Bump to 2.10.10.
* Fri Feb 16 2007 - takao.fujiwara@sun.com
- Removed '-c' option of msgfmt in po*/Makefile.in.in
* Tue Feb 13 2007 - takao.fujiwara@sun.com
- Add l10n tarball.
* Mon Jan 22 2007 - damien.carbery@sun.com
- Bump to 2.10.9.
* Wed Jan 17 2007 - damien.carbery@sun.com
- Bump to 2.10.8. Removed upstream patches, 15-load-gdm-modules.
* Mon Jan 08 2007 - damien.carbery@sun.com
- Bump to 2.10.7. Remove upstream patches, 15-hidden and 17-recent-files-crash.
  Renumber remainder.
* Wed Dec 13 2006 - padraig.obriain@sun.com
- remove patch 08-nofocus-empty.diff as it is not needed.
* Wed Dec 06 2006 - ghee.teo@sun.com
- Include bugzilla id for 19-printing-papi-backend.diff which is now cleaned up.
* Thu Nov 23 2006 - padraig.obriain@sun.com
- added patch 20-gedit-menu-shortcuts.diff
* Thu Nov 16 2006 - ghee.teo@sun.com
- added patch 19-printing-papi-backend.diff
* Fri Nov  3 2006 - laca@sun.com
- use %gtk_doc_option in configure so that it can be disabled using
  --without-gtk-doc
- add --datadir=%{_datadir} to the configure options, fixes 6443777
* Thu Oct 26 2006 padraig.obriain@sun.com
- Add patch, 18-recent-files-crash, for bugster 6485464, bugzilla 365031.
* Mon Oct 18 2006 - brian.cameron@sun.com
- Call autoconf after autoheader/automake.
* Fri Oct 13 2006 - damien.carbery@sun.com
- Delete .a and .la files.
* Wed Oct 04 2006 - damien.carbery@sun.com
- Bump to 2.10.6.
* Tue Oct 03 2006 - damien.carbery@sun.com
- Add patch, 17-stock_icons_typo, to fix typo in Makefile. Already fixed
  upstream.
* Mon Oct 02 2006 - damien.carbery@sun.com
- Bump to 2.10.5. Remove upstream patch, 17-hang-on-mutex.
* Wed Sep 27 2006 - padraig.obriain@sun.com
- Add patch hang-on-mutex as part fix for bug 6475663
* Tue Sep 05 2006 - damien.carbery@sun.com
* Tue Sep 26 2006 - damien.carbery@sun.com
- Bump to 2.10.4.
* Tue Sep 05 2006 - damien.carbery@sun.com
- Bump to 2.10.3.
* Fri Aug 18 2006 - damien.carbery@sun.com
- Bump to 2.10.2.
* Mon Jul 24 2006 - damien.carbery@sun.com
- Bump to 2.10.1.
* Thu Jul 20 2006 - damien.carbery@sun.com
- Bump to 2.10.0.
* Mon Jul 10 2006 - brian.cameron@sun.com
- Bump to 2.8.20.
* Tue Jul 04 2006 - ghee.teo@sun.com
- added gtk+-15-truested-extensions.diff
* Tue Jun 27 2006 - yuriy.kuznetsov@sun.com
- remove line with "cp po/Makefile.in.in po-properties"
  to fix CR#6439573
* Wed Apr 26 2006 - damien.carbery@sun.com
- Bump to 2.8.17.
* Thu Mar 16 2006 - damien.carbery@sun.com
- Bump to 2.8.16.
* Mon Mar 13 2006 - damien.carbery@sun.com
- Bump to 2.8.15.
* Thu Mar  9 2006 - damien.carbery@sun.com
- Bump to 2.8.14.
* Sun Feb 26 2006 - damien.carbery@sun.com
- Bump to 2.8.13.
* Mon Feb 13 2006 - damien.carbery@sun.com
- Bump to 2.8.12.
* Sun Jan 29 2006 - damien.carbery@sun.com
- Bump to 2.8.11
* Tue Dec 20 2005 - damien.carbery@sun.com
- Bump to 2.8.9.
* Tue Nov 29 2005 - damien.carbery@sun.com
- Bump to 2.8.8.
- Remove upstream patches 15-gtkcalendar and 16-glib-mkenums.
* Mon Nov 28 2005 - laca@sun.com
- prepare for building from CVS snapshots:
- use a macro for Version
- fix autotool order, add some more
- cp mkinstalldirs so that we don't need to add even more autotool foo
* Tue Oct 11 2005 - damien.carbery@sun.com
- Bump to 2.8.6
- Add patch, gtk+-15-gtkcalendar, to declare a missing var. #318578.
- Add patch, gtk+-16-glib-mkenums, to use macro instead of hardcoding. #318582.
* Tue Sep 13 2005 - brian.cameron@sun.com
- Bump to 2.8.3 fixing a core dumping problem for the panel and
  nautilus on Solaris x86.
* Mon Aug 15 2005 - glynn.foster@sun.com
- Bump to 2.8.0
* Fri May 06 2005 - brian.cameron@sun.com
- Added a patch and then backed it out.
* Fri May 06 2005 - glynn.foster@sun.com
- Bump to 2.6.7
* Wed May 04 2005 - srirama.sharma@wipro.com
- Added gtk+-17-treeview-keynav.diff to modify the keynav
  in treeview. Fixes bug #6216594.
* Mon Mar 21 2005 - vinay.mandyakoppal@wipro.com
- Edited patch gtk+-02-fileseldlg-navbuttons.diff to make
  save attachment Desktop button work. Fixes #6240188.
* Tue Feb 22 2005 - vijaykumar.patwari@wipro.com
- Added patch gtk+-16-blank-popup-menu-fix.diff to
  fix blank popup menu area.
* Wed Dec 15 2004 - glynn.foster@sun.com
- Bump to 2.4.14
* Thu Nov 25 2004 - yong.sun@sun.com
- Patch 19 for bugster #6199166: Cinnabar [linux] Styles are not localized
  in Gtk/Gnome font selector dialog
* Sat Nov 06 2004 - srirama.sharma@wipro.com
- Patch for the Bug #6185180 is rolled to the original 
  gtk+-06-file-chooser.diff.
* Thu Nov 04 2004 - srirama.sharma@wipro.com
- Rolled in the patch for Bug #6178360 to the original 
  gtk+-06-file-chooser.diff
* Fri Oct 29 2004 - padraig.obriain@sun.com
- Add patch gtk+-17-iter-inside-word.diff for bugzilla 153628.
* Fri Oct 29 2004 - laca@sun.com
- use $CC64 for the 64-bit build if defined
* Sat Oct  2 2004 - Joseph.Townsend@Sun.COM
- Create 64bit libraries for Solaris
* Thu Sep 30 2004 - vijaykumar.patwari@wipro.com
- Fix image code security issue.
* Sat Sep 18 2004 - laca@sun.com
- Add patch 15 for ABI compatibility with gdk in the Solaris GNOME 2.0 release
* Wed Sep 15 2004 - muktha.narayan@wipro.com
- Added patch gtk+-14-solaris-xinerama-support.diff to
  enable xinerama flags on Solaris.
* Sat Sep 11 2004 - laca@sun.com
- Move Solaris specific LDFLAGS to the Solaris spec file
* Fri Sep 10 2004 - damien.carbery@sun.com
- Set LDFLAGS so Xrandr and Xrender can be found.
* Thu Aug 26 2004 - glynn.foster@sun.com
- Bump to 2.4.9
* Tue Aug 24 2004 - glynn.foster@sun.com
- Bump to 2.4.7
* Wed Aug 18 2004 - brian.cameron@sun.com
- added --enable-gtk-doc.
* Tue Aug 17 2004 - balamurali.viswanathan@wipro.com
- Added Sun branding patch gtk+-15-sun-pgdn-pgup-keybinding.diff
  Sun keyboard bindings for Keypad keys PageUp, PageDown, Home and End.
  The patch has been rejected by the GTK maintainers as a WONTFIX as they feel
  its a bug in the Sun Xserver. Corresponding sun-patch is 085-74223-w.diff
* Thu Aug 12 2004 - narayana.pattipati@wipro.com
- Added Sun branding patch gtk+-14-sun-copy-paste-keybindings.diff 
  to provide copy, paste, cut key bindings in Sun Keyboards. The patch is
  ported from GNOME 2.0 (sun-patches/gtk+/190-00000-s.diff). It was rejected
  by community. So, it will be a SUN specific patch.
* Thu Jul 22 2004 - padraig.obriain@sun.com
- Added patches gtk+-10-combo-a11y.diff for bugzilla #132847
  gtk+-11-nofocus-empty.diff for bugzilla #126295
  gtk+-12-file-chooser-a11y-names.diff for bugzilla #144405
  gtk+-13-single-row-treeview.diff for bugzilla #131226
* Wed Jul 14 2004 - Yong.Sun@Sun.COM
- Added a new -09 patch to fix bugtraq #5048804
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to gtk2-l10n-po-1.2.tar.bz2
* Thu Jul 08 2004 - niall.power@sun.com
- run libtoolize to fix some weirdness
* Wed Jul 07 2004 - niall.power@sun.com
- Ported to rpm4
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Mon May 17 2004 - hidetoshi.tajima@sun.com
- Added a new -07 patch to fix bugtraq #5035382.
- Moved the previous revision 07 patch to fix bug 141190 to revision 08
  as the last patch, since the same fix is already in community's cvs server,
  hence the patch should be removed eventually when the fix comes from a
  new version of gtk+ tarball, including gtkimcontextxim.c revision 1.47 or
  newer.
* Fri May 14 2004 - danek.duvall@sun.com
- Applied patch to fix bug 141190, bringing gtkimcontextxim.c
  up to revision 1.47.  Revision 1.46, included in 2.4.1, broke
  compilation on Solaris.
* Fri May 14 2004 - glynn.foster@sun.com
- Bump to 2.4.1. Remove render icon patch, since upstream.
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to gtk2-l10n-po-1.1.tar.bz2
* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to gtk2-l10n-po-1.0.tar.bz2
* Thu Mar 25 2004 - glynn.foster@sun.com
- Use JDS autotools.
* Wed Mar 24 2004 - glynn.foster@sun.com
- Bump to 2.4.0 and remove upstream file chooser patch.
* Mon Mar 22 2004 - <brian.cameron@sun.com>
- added patch 7 to add mediaLib support.  Also added autoconf/
  automake since this patch changes configure.in/Makefile.am
  files.
* Thu Mar 18 2004 - hidetoshi.tajima@sun.com
- don't install unsupported gtk-2.0/*/immodules/im-*.so
* Tue Mar 16 2004 - <brian.cameron@sun.com>
- Add patch 6 to fix -1 enumeration issue on Solaris.  This
  fixed many programs from crashing (panel, gdm, nautilus).
* Mon Mar 15 2004 - <laca@sun.com>
- Add patch to fix build on Solaris. In cvs.gnome.org already.
* Thu Mar 11 2004 - <glynn.foster@sun.com>
- Remove patches 4 and 5 - they're upstream.
* Wed Mar 10 2004 - <niall.power@sun.com>
- Bump to 2.3.6, update dependenciy versions.
* Tue Feb 10 2004 - <matt.keenan@sun.com>
- Bump to 2.3.2, and l10n to 0.7, and port patch 05
* Fri Jan 09 2004 - <laca@sun.com>
- add a missing .pc file
- clean up for Solaris builds
* Wed Jan 07 2004 - <glynn.foster@sun.com>
- Remove the tab cycling patch for notebooks, since it's already
  upstream.
* Mon Dec 15 2003 - <glynn.foster@sun.com>
- Bump to 2.3.1
* Mon Aug 25 2003 - <ghee.teo@sun.com>
- Fix input method hanged in zh_CN.gb18030 locale.
  Taken patch from community for bugzilla 115077 and 105909.
  Fixed 4894673, 4908025.
* Thu Aug 14 2003 - <laca@sun.com>
- move lib*.so to -devel, remove *.a, *.la
* Fri Jul 25 2003 - niall.power@sun.com
- /etc/gtk-2.0 needs to exist before postinstall script is run.
  run ./mkinstalldirs to ensure this.
* Fri Jul 18 2003 - <michael.twomey@sun.com>
- Fixing %postun action so that config files are only removed on final
  uninstall of gtk2.
* Fri Jul 11 2003 - <niall.power@sun.com>
- add file selection dialog shortcuts patch
* Wed Jul 09 2003 - <michael.twomey@sun.com>
- add in sun po files
* Mon Jul 07 2003 - <markmc@sun.com>
- add new patch to make message dialogs have window icons.
  See bug #116896.
* Mon Jun 30 2003 - <glynn.foster@sun.com>
- Add new patch to make sure that rendering on pixbufs is okay. This 
  fixes an issue with gnome-theme-manager
* Mon Jun 30 2003 - <glynn.foster@sun.com>
- Bump version number for new tarballs, and reset release number.
* Wed Jun 25 2003 - <markmc@sun.com>
- add gtk-unset-hack.sh and gtk-unset-hack.csh to workaround
  SuSE's gtk-1.2 rpms installing crackrock scripts into
  /etc/profile.d
* Thu May 29 2003 - <Laszlo.Kovacs@sun.com>
- added patch gtk+-01-tab-change-with-ctrl-alt-pageup-pagedn.diff
* Tue May 13 2003 - Stephen.Browne@sun.com
- initial release
