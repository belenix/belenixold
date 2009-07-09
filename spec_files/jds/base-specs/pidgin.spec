#
# spec file for package pidgin
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: elaine
# old_bugdb: http://sourceforge.net/tracker/index.php?func=detail&group_id=235&atid=300235&aid=
# bugdb: http://developer.pidgin.im/ticket/
#
%include l10n.inc
Name:		pidgin
Version:	2.5.5
Release:        1
License:	GPL
Group:		Applications/Internet
Distribution:	Java Desktop System
Vendor:		Sun Microsystems, Inc.
Summary:	Multiprotocol Instant Messaging Client
Source:		http://easynews.dl.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tar.bz2
%if %build_l10n
Source1:        pidgin-po-sun-%{po_sun_version}.tar.bz2
Source2:        l10n-configure.sh
%endif
# date:2006-11-16 owner:rickju type:branding bugster:6439103
Patch1:         pidgin-01-gnome-keyring.diff
# date:2006-12-20 owner:rickju type:feature bugid:1643233
Patch2:         pidgin-02-uninstalled-pc.diff
# date:2008-06-02 owner:rickju type:branding
Patch3:         pidgin-03-runpath.diff
# date:2007-03-07 owner:rickju type:bug bugster:6524856 state:upstream
Patch4:        pidgin-04-jabber-msg.diff
# date:2007-04-03 owner:rickju type:bug bugster:6524819 state:upstream
Patch5:        pidgin-05-option-menu.diff
# date:2007-08-27 owner:rickju type:bug bugster:6595691 state:upstream
Patch6:        pidgin-06-parse-account.diff
# date:2008-08-21 owner:jedy type:branding
Patch7:        pidgin-07-menu-entry.diff
URL:		http://www.pidgin.im
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
Docdir:		%{_defaultdocdir}/pidgin
Autoreqprov:	on
Prereq:       sed

BuildRequires:	gtk2-devel
BuildRequires:	glib2-devel

%description
Pidgin allows you to chat over the Internet using a variety of
messaging protocols, including AIM, ICQ, IRC, Yahoo!, 
MSN Messenger and Jabber.
These protocols are implemented using a modular, easy to use
design.

%package devel
Summary:      Multiprotocol Instant Messaging Client
Group:        System/GUI/GNOME
Autoreqprov:  on
Requires:     %name = %version

%description devel
Pidgin allows you to chat over the Internet using a variety of
messaging protocols, including AIM, ICQ, IRC, Yahoo!, 
MSN Messenger and Jabber.
These protocols are implemented using a modular, easy to use
design.

%prep
%setup -q
%if %build_l10n
bzcat %SOURCE1 | tar xf -
cd po-sun; make; cd ..
%endif
for po in po/*.po; do
  dos2unix -ascii $po $po
done

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

%build
%{!?perl_vendorarch: %define perl_vendorarch %(eval "`%{__perl} -V:installvendorarch`"; echo $installvendorarch)}

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

glib-gettextize -f
libtoolize --force
intltoolize --force --copy --automake

%if %build_l10n
bash -x %SOURCE2 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS -I .
autoheader
automake -a -c -f
autoconf

CFLAGS="$RPM_OPT_FLAGS -DG_IMPLEMENT_INLINES -DG_HAVE_ISO_VARARGS" \
LD_LIBRARY_PATH="%{_libdir}:$LD_LIBRARY_PATH"
./configure 				\
	--prefix=%{_prefix} 		\
	--mandir=%{_mandir}		\
	--sysconfdir=%{_sysconfdir}	\
	--disable-binreloc		\
	--enable-gnutls=no              \
	--with-nss-includes=/usr/include/mps   \
	--with-nss-libs=/usr/lib/mps           \
	--with-nspr-includes=/usr/include/mps  \
	--with-nspr-libs=/usr/lib/mps          \
	--enable-gnome-keyring                 \
	--enable-gevolution                    \
	--enable-cap                           \
	--disable-meanwhile                    \
	--disable-nm                           \
	--disable-consoleui                    \
  --with-perl-lib=vendor

make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install \
    SITEPREFIX=/dummy VENDORPREFIX=/dummy PERLPREFIX=/dummy
rm -Rf $RPM_BUILD_ROOT/dummy
rm -rf $RPM_BUILD_ROOT%{_bindir}/purple-client-example
rm $RPM_BUILD_ROOT%{_libdir}/pidgin/*.la
rm $RPM_BUILD_ROOT%{_libdir}/purple-2/*.la
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm -rf $RPM_BUILD_ROOT%{_datadir}/pixmaps/purple/buddy_icons/qq
rm -rf $RPM_BUILD_ROOT%{_datadir}/purple/ca-certs
rm -rf $RPM_BUILD_ROOT%{_datadir}/purple
rm -rf $RPM_BUILD_ROOT%{_libdir}/purple-2/libqq.so
rm -rf $RPM_BUILD_ROOT%{_libdir}/purple-2/libsimple.so
rm -rf $RPM_BUILD_ROOT%{_libdir}/purple-2/libzephyr.so
rm -rf $RPM_BUILD_ROOT%{_libdir}/purple-2/libmyspace.so
rm -rf $RPM_BUILD_ROOT%{_libdir}/purple-2/dbus-example.so


%files
%defattr(-, root, root)
%doc doc/the_penguin.txt doc/CREDITS NEWS COPYING AUTHORS
%doc doc/FAQ README ChangeLog HACKING
%attr(755, root, root) %{_libdir}/pidgin/*.so
%{_bindir}/*
%{_libdir}/lib*.so.*
%{_datadir}/locale/*/*/*
%{_datadir}/pixmaps/*
%{_datadir}/sounds/pidgin/*
%{_datadir}/icons/*
%{_datadir}/applications/*
%{_datadir}/dbus-1
%attr(755, root, root) %{perl_vendorarch}/Pidgin.pm
%attr(755, root, root) %{perl_vendorarch}/Purple.pm
%attr(755, root, root) %{perl_vendorarch}/auto/Pidgin
%attr(755, root, root) %{perl_vendorarch}/auto/Purple

%files devel
%defattr(-, root, root)
%{_libdir}/pkgconfig/*
%{_includedir}/pidgin/*
%{_datadir}/aclocal

%clean
rm -r $RPM_BUILD_ROOT

%changelog
* Thu Mar 12 2009 - elaine.xiong@sun.com
- bump to 2.5.5.

* Wed Mar 11 2009 - elaine.xiong@sun.com
- Change ownership to elaine.

* Tue Mar 03 2009 - elaine.xiong@sun.com
- bump to 2.5.4

* Tue Jan 05 2009 - rick.ju@sun.com
- bump to 2.5.3

* Tue Oct 27 2008 - rick.ju@sun.com
- bump to 2.5.2

* Tue Oct 20 2008 - rick.ju@sun.com
- Add gtk-spell check

* Tue Sep 02 2008 - rick.ju@sun.com
- Bump to 2.5.1

* Thu Aug 21 2008 - jedy.wang@sun.com
- Add 07-menu-entry.diff.

* Thu Aug 21 2008  - rick.ju@sun.com
- Bump to 2.5.0.

* Mon Jul 07 2008 - damien.carbery@sun.com
- Bump to 2.4.3.

* Mon Jun 23 2008 - damien.carbery@sun.com
- Disable consoleui support - we don't have ncurses on the build machines. If a
  system does have ncurses then additional files will be delivered and appear
  to break the build.  Adding --disable-consoleui to configure prevents this.

* Thu Jun 02 2008  - rick.ju@sun.com
- Add a runpath fix for nss library

* Thu May 29 2008  - rick.ju@sun.com
- fix the cap.so and gevolution.so missing issue

* Thu May 22 2008  - rick.ju@sun.com
  bump to 2.4.2

* Fri Mar 07 2008  - rick.ju@sun.com
  Enable dbus, Avahi and Gadu-gadu.

* Thu Mar 06 2008  - rick.ju@sun.com
  bump to pidgin 2.4.0

* Fri Jan 04 2008  - rick.ju@sun.com
  bump to pidgin 2.3.1

* Tue Dec 06 2007  - rick.ju@sun.com
  bump to pidgin 2.3.0

* Tue Nov 06 2007  - rick.ju@sun.com
  bump to pidgin 2.2.2

* Fri Nov 02 2007  - rick.ju@sun.com
  remove libbonjour.so

* Thu Aug 30 2007 - damien.carbery@sun.com
- Add intltoolize call to update intltool scripts.

* Mon Aug 27 2007 - rick.ju@sun.com
- Add pidgin-06-parse-account.diff to fix bug bugster:6595691
  gaim crash on startup when parsing the account.

* Wed Aug 22 2007 - damien.carbery@sun.com
- Bump to 2.1.1.

* Thu Aug 02 2007 - rick.ju@sun.com
- bump to 2.1.0

* Tue Jul 10 2007 - rick.ju@sun.com
- remove the line removing libxmpp.so

* Thu Jun 07 2007 - damien.carbery@sun.com
- Add patch, 10-remove-evo-header, to remove reference to obsolete evolution
  header file.

* Tue May 30 2007 - rick.ju@sun.com
- bump to pidgin 2.0.1

* Tue May 03 2007 - rick.ju@sun.com
- Reopen configure arguments for nss/nspr include/lib
- Added patch 14-enable-nss.diff

* Tue Apr 28 2007 - rick.ju@sun.com
- Added configure arguments for nss/nspr include/lib

* Tue Apr 03 2007 - rick.ju@sun.com
- Added 13-option-menu.diff for bug#6524819

* Wed Feb 21 2007 - takao.fujiwara@sun.com
- Added l10n tarball. Fixes CR 6463000.

* Thu Feb  8 2007 - damien.carbery@sun.com
- Renumber 'Patch??:' lines to be sequential after Patch3 removal.

* Thu Jan 25 2007 - alvaro.lopez@sun.com
- gaim-03-long-preferences.diff removed. It's no longer needed.

* Thu Jan 25 2007 - rick.ju@sun.com
- Bump to beta6. Add patches 11-return-void and 12-static-prpls. Rename patch
  11-dbus-abort to 10-dbus-abort.

* Sun Jan 21 2007 - rick.ju@sun.com
- Add patch 11-dbus-abort to fix #6508240.

* Thu Jan 18 2007 - damien.carbery@sun.com
- Remove the code from %install that deletes $RPM_BUILD_ROOT as it trashes the
  'make install' of gaim-otr when part of SUNWgnome-im-client build.

* Wed Jan 17 2007 - damien.carbery@sun.com
- Remove unneded patch, 02-perl-common-argc, renumber remainder.

* Thu Nov 30 2006 - damien.carbery@sun.com
- Bump to 2.0.0beta5.

* Thu Nov 30 2006 - rick.ju@sun.com
- Add configure argument enable-gnome-keying to fix #6439103.

* Thu Nov 13 2006 - rick.ju@sun.com
- Add patches 08-gnome-keyring and 09-gtk-file-chooser; add
  --enable-gnome-keyring to configure and

* Mon Nov 13 2006 - patrick.wade@sun.com
- Add patch, 07-protocol-mnemonics, to add protocol mnemonics, CR#6477194

* Mon Nov 06 2006 - rick.ju@sun.com
- Remove upstream patch 05-msn-crash. Rename rest.

* Fri Nov 03 2006 - damien.carbery@sun.com
- Specify sysconfdir in configure call as gaim.schemas is installed there.
 
* Thu Nov 02 2006 - damien.carbery@sun.com
- Add patch, 07-gtk-func-def, to fix inconsistency between a function 
  declaration and definition. Submitted upstream via sourceforge.net bug db.

* Thu Nov 02 2006 - damien.carbery@sun.com
- Bump to 2.0.0beta4. Remove upstream patch, 05-nopyextension, and obsolete
  patch, 06-psychic, (referenced code no longer in module). Rename remainder.

* Mon Oct 16 2006 - damien.carbery@sun.com
- Remove the '-f' from the 'rm *.la *.a' lines so that any changes to the
  module source will be seen as a build error and action can be taken.

* Mon Aug 28 2005 - rick.ju@sun.com
- Bump to 2.0.0beta3.1

* Mon Aug 28 2006 - patrick.wade@sun.com
- Add patch gaim-12-proxy_mnemonics.diff to add new mnemonics, CR#6442067

* Wed May 10 2006 - brian.cameron@sun.com
- Add patch gaim-11-nopyextensions.diff to remove .py extensions from
  executables and move gaim-notifications-example to
  /usr/share/doc/gaim/examples since it is a system-independant demo
  program.

* Wed Feb 15 2006 - damien.carbery@sun.com
- Bump to 2.0.0beta2. Remove obsolete patch, 11-forte.

* Wed Jan 18 2006 - damien.carbery@sun.com
- Bump to 2.0.0beta1, remove obsolete patches (08-sound_errors and 
  11-g11n-enable-im). Add patches 08-libgaimperl and 11-forte.

* Tue Nov 29 2005 - laca.com
- remove javahelp stuff

* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 1.5.0.

* Thu Jun 10 2005 - glynn.foster@sun.com
- Bump to 1.3.0

* Thu Mar 24 2005 - alvaro.lopez@sun.com
- Rev to 1.3.0.  Patches #9, 12, 17, 18 and 19 removed.

* Thu Mar 24 2005 - vijaykumar.patwari@wipro.com
- Added gaim-19-yahoo-privacy-fix.diff patch, fixes yahoo
  privacy issue.

* Tue Jan 25 2005 - damien.carbery@sun.com
- Update docs with Linux specific tarball from maeve.anslow@sun.com.

* Tue Jan 18 2005 - glynn.foster@sun.com
- New backported patch to fix msn messenger. Fixes #6217610.

* Wed Jan 12 2005 - takao.fujiwara@sun.com
- Added gaim-15-g11n-enable-im.diff to enable Ja input method.  Fix 4990149.
- Added gaim-16-g11n-filename.diff to get/put localized filenames. Fixes 6216501

* Tue Jan 11 2005 - alvaro.lopez@sun.com
- Added patch #15. Fixes #6204972

* Thu Dec 16 2004 - kazuhiko.maekawa@sun.com
- Update l10n help tarball to use linux version 

* Wed Dec  8 2004 - damien.carbery@sun.com
- Update docs tarball from maeve.anslow@sun.com.

* Fri Nov 12 2004 - kazuhiko.maekawa@sun.com
- Added workaround fix for 6193354

* Fri Oct 29 2004 - vijaykumar.patwari@wipro.com
- Fixes msn security issues.

* Thu Oct 21 2004 - alvaro.lopez@sun.com
- Added patch #11. Fixes #5101982

* Mon Sep 06 2004 - matt.keenan@sun.com
- Add javahelp-convert for new docs

* Fri Sep 03 2004 - damien.carbery@sun.com
- Add docs tarball from patrick.costello@sun.com.
- Add patch to incorporate docs tarball.

* Mon Aug 30 2004 - glynn.foster@sun.com
- Bump to 0.82.1

* Tue Aug 24 2004 - laszlo.kovacs@sun.com
- mandir/man3 added to base package

* Tue Aug 24 2004 - glynn.foster@sun.com
- Bump to 0.81 and create a devel package.

* Fri Aug 20 2004 - damien.carbery@sun.com
- Comment out removal of man3 files - these don't exist on Solaris.

* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to gaim-l10n-po-1.2.tar.bz2

* Wed Jul 07 2004 - niall.power@sun.com
- ported to rpm4
                                                                                
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds

* Wed Jun 09 2004 - kaushal.kumar@wipro.com
- Modified patch gaim-02-remove-unwanted-protocols.diff to remove the 
  unnecessary protocols from the build.

* Fri Jun 04 2004 - arvind.samptur@wipro.com
- Add patch gaim-10-iconv-open.diff. Fixes the irc protocol on
  Solaris

* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to gaim-l10n-po-1.1.tar.bz2

* Sun May 02 2004 - laca@sun.com
- add patch #9 (void-return) for a void function returning a value

* Tue Apr 27 2004 - vijaykumar.patwari@wipro.com
- Bumped new tarball 0.76 version and updated spec file 
  accordingly.

* Mon Apr 05 2004 - niall.power@sun.com
- ifos'ify glib-gettexttize, to stop nameless .mo files being 
  generated on cinnabar/linux.

* Sun Apr 04 2004 - laca@sun.com
- add glib-gettextize to make the build work with Solaris msgfmt

* Wed Mar 31 2004 - brian.cameron@sun.com
- replace tar jxf with the more solaris friendly
  bzcat piped through tar

* Mon Mar 29 2004 - damien.donlon@sun.com
- Adding gaim-l10n-po-1.0.tar.bz2 l10n content

* Mon Mar 08 2004 - Vijaykumar.patwari@wipro.com
- Fixes all vulnerabilities reproted in the bug report.

* Thu Mar 04 2004 - takao.fujiwara@sun.com
- Removed gaim-01-menu-entry.diff
- Added gaim-01-g11n-menu-entry.diff to fix 4957377
- Added gaim-08-g11n-potfiles.diff

* Wed Mar 03 2004 - <laca@sun.com>
- fix Solaris build by forcing the use of the glib gettext test macro

* Fri Feb 20 2004 - <matt.keenan@sun.com>
- Distro to Cinnabar, fixed patch gaim-06-po-mkinstalldirs.diff

* Thu Feb 19 2004 - <damien.carbery@sun.com>
- Update to 0.75.

* Fri Oct 31 2003 - <glynn.foster@sun.com>
- Remove the Sun Supported keyword from the menu
  patch.

* Mon Oct 20 2003 - <stephen.browne@sun.com>
- update to 0.70 and removed potfiles patch

* Thu Aug 14 2003 - <laca@sun.com>
- remove *.a, *.la

* Tue Aug 05 2003 michael.twomey@sun.com
- Added POTFILES.in patch again (updated)

* Fri Aug 01 2003 Stephen.Browne@sun.com
- removed unwanted protocols

* Fri Aug 01 2003 Stephen.Browne@sun.com
- why was there no changelog for this before? well 
  new tarball, bumped release, reset release, added lbgaim-remote.so.*
