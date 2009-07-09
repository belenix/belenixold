#
# spec file for package gnome-mime-data
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: padraig
#
Name:			gnome-mime-data
License:		LGPL
Group:			System/GUI/GNOME
BuildArchitectures:	noarch
Version:		2.18.0
Release:		2
Distribution:		Java Desktop System
Vendor:			Sun Microsystems, Inc.
Summary:		MIME Type and Application Database for the GNOME Desktop
Source:			http://ftp.gnome.org/pub/GNOME/sources/%{name}/2.18/%{name}-%{version}.tar.bz2
Source1:                gnome-realplay.keys
%if %build_l10n
Source2:                 l10n-configure.sh
%endif
# owner:padraig date:2004-10-05 type:branding
Patch1:                 gnome-mime-data-01-set-mozilla-default.diff
# owner:padraig date:2004-10-05 type:branding
Patch2:                 gnome-mime-data-02-text-plain-handler.diff
# owner:padraig date:2004-10-05 type:branding
Patch3:                 gnome-mime-data-03-always-use-app.diff
# owner:padraig date:2004-10-05 type:branding
Patch4:                 gnome-mime-data-04-swf-handler.diff
# owner:padraig date:2004-10-05 type:branding
Patch5:                 gnome-mime-data-05-jar-handler.diff
# owner:padraig date:2004-09-07 type:branding
Patch6:                 gnome-mime-data-06-pdfviewer.diff
# owner:padraig date:2004-11-10 type:branding
Patch7:                 gnome-mime-data-07-shellscript.diff
# owner:padraig date:2005-02-01 type:branding
Patch8:                 gnome-mime-data-08-associate-glade-files.diff
# owner:padraig date:2005-05-10 type:bug bugster:6267137 bugzilla:303532
Patch9:                 gnome-mime-data-09-return-path-pattern.diff
URL:			http://www.gnome.org
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
Docdir:			%{_defaultdocdir}/%{name}
Autoreqprov:		on

%define gnome_common_version 2.4.0

BuildRequires: gnome-common >= %{gnome_common_version}
BuildRequires: intltool
BuildRequires: glib2

PreReq: RealPlayer
Prereq: coreutils

%description
MIME Type and Application Database for the GNOME Desktop that allows the
GNOME Virtual Filesystem to associate data files with their icon and
description, and to launch them with suitable applications.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
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

libtoolize --force
intltoolize --force --copy --automake

%if %build_l10n
bash -x %SOURCE2 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS
automake -a -c -f
autoconf
./configure --prefix=%{_prefix}			\
	    --sysconfdir=%{_sysconfdir}		\
            --mandir=%{_mandir}
make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install
make DESTDIR=$RPM_BUILD_ROOT install
#Copy zh_HK from zh_TW
#Fixes bug 4930405
install -d $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES
install --mode=0644 $RPM_BUILD_ROOT%{_datadir}/locale/zh_TW/LC_MESSAGES/*.mo \
	$RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES/
install --mode=0644 %SOURCE1 $RPM_BUILD_ROOT%{_datadir}/mime-info


%post
install -p -m644 "%{_datadir}/mime-info/gnome-realplay.keys" \
	"%{_datadir}/mime-info/realplay.keys"


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_sysconfdir}/gnome-vfs-mime-magic
%{_datadir}/mime-info/*
%{_datadir}/application-registry/*
%{_mandir}/man4/*
# This package is so small, it's not worth doing a -devel package
# just for the pkgconfig file.
%{_libdir}/pkgconfig/gnome-mime-data-2.0.pc

%changelog
* Wed Aug 29 2007 - damien.carbery@sun.com
- Add intltoolize call to update intltool scripts.

* Wed Apr 04 2007 - damien.carbery@sun.com
- Bump to 2.18.0.

* Fri Jan 26 2007 - alvaro@sun.com
- gnome-mime-data-01-realplay-g11n-keys.diff removed. 
  It was empty. Patches renamed.

* Thu Nov 09 2006 - damien.carbery@sun.com
- Bump to 2.4.3.

* Wed Jul 27 2005 - narayana.pattipati@wipro.com
- Removed patch gnome-mime-data-08-add-nfs-mime.diff because its not 
  required anymore after nfs:// method removal from gnome-vfs. Renamed 
  the following patches accordingly.

* Tue May 10 2005 - vinay.mandyakoppal@wipro.com
- Added patch gnome-mime-data-14-return-path-pattern.diff given by 
  Antonio Xu <Antonio.Xu@Sun.COM> to add pattern "Return-path"
  for message.rfc822. fixes bug #6267137.

* Fri May 06 2005 - glynn.foster@sun.com 
- Bump to 2.4.2

* Wed Apr 06 2005 - dermot.mccluskey@sun.com 
- 6241631: added gnome-realplay.keys, which overwrites
  /usr/share/mime-info/realplay.keys in %post.  This sets
  RP as the player for most possible media types.

* Thu Mar 31 2005 - glynn.foster@wipro.com 
- Removed jmplay as default player for many media types in 
  preference of realplayer. It still defaults back to some
  though. Remove the realplayer patch since it's now bogus.

* Fri Mar 11 2005 - dinoop.thomas@wipro.com 
- Added patch gnome-mime-data-14-associate-java-files.diff to
  associate java files with netbeans.
  Fixes bug #6229767.

* Thu Feb 03 2005 - dinoop.thomas@wipro.com
- Added patch gnome-mime-data-13-associate-glade-files.diff to
  associate glade files with glade tool.
  Fixes bug #6222813.

* Fri Nov 26 2004 - laca@sun.com
- removed patch 13

* Thu Nov 18 2004 - laca@sun.com
- added patch gnome-mime-data-13-acroread-mozilla-wrappers.diff

* Wed Nov 10 2004 - archana.shah@wipro.com
- Added patch gnome-mime-data-12-shellscript.diff to add flags for
  shell scripts' mime types.

* Tue Oct 05 2004 - takao.fujiwara@sun.com
- Updated gnome-mime-data-02-make-jmplay-default-player.diff to add x-gsm mime
  Fixed 6173640

* Wed Sep 15 2004 - archana.shah@wipro.com
- Added patch gnome-mime-data-11-pdfviewer.diff.
  Fixes bug# 5100997

* Wed Jul 14 2004 - narayana.pattipati@wipro.com
- Added patch gnome-mime-data-10-add-nfs-mime.diff to add entries for
  x-directory/nfs-mount and x-directory/nfs-share mime types to enable
  browsing nfs:// locations. Fixes bugtraq bug#5034725.

* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-mime-data-l10n-po-1.2.tar.bz2

* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds

* Wed Jun 23 2004 - narayana.pattipati@wipro.com
- Added patch gnome-mime-data-09-realplayer-command-change.diff to 
  fix the problem of mime association for realplayer by correcting 
  the command name. Fixes bugtraq bug#5061307

* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-mime-data-l10n-po-1.1.tar.bz2

* Tue Apr 27 2004 - vijaykumar.patwari@wipro.com
- Set mozilla as the default browser for text/html mime type.

* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-mime-data-l10n-po-1.0.tar.bz2

* Mon Mar 22 2004 - <takao.fujiwara@sun.com>
- Replaced gnome-mime-data-08-i18n-keys.diff with
  gnome-mime-data-08-g11n-keys.diff

* Mon Feb 23 2004  <ghee.teo@sun.com>
- Repatched gnome-mime-data-02-make-jmplay-default-player.diff for
  cinnabar.

* Mon Feb 23 2004 - <stephen.browne@sun.com>
- New tarball 2.4.1, ported patches, still two patches to do

* Thu Jan 29 2004 - <dermot.mccluskey@sun.com>
- Add dependency on intltool
                                                                                                                                                             
* Mon Dec 15 2003 - <glynn.foster@sun.com
- Add back the man pages, and some patches.

* Mon Oct 20 2003 - <ghee.teo@sun.com
- Added patch gnome-mime-data-04-text-plain-handler.diff which was in
  Mercury so that gedit is lauched instead of text viewer for nautilus
  on a text/*.

* Wed Oct 15 2003 - <markmc@sun.com> 2.4.0-2
- Re-add the view-as-webpage diff.

* Tue Oct 07 2003 - ghee.teo@sun.com
- Updated to use GNOME 2.4 for Quicksilver. Deleted one patch and
  renumbered the other one.

* Thu Aug 21 2003 - ghee.teo@sun.com
- Updated gnome-vfs.applications to include all the real formats
  that realplay itself understand since the current definitions is
  rather limiting. simply updated the Patch3.

* Wed Aug 20 2003 - ghee.teo@sun.com
- updated gnome-vfs.applications, gnome-vfs.keys.in and gnome-vfs.mime
  to include some of the more obscure mime types that jmplay can 
  handle including x-gsm, rmf, ogg, mvr, x-jmx.

* Mon Aug 18 2003 - brian.nitz@sun.com
- created a patch to add jmplay as default media player.

* Mon Aug 11 2003 - <stephen.browne@sun.com>
- new tarball, reset release

* Mon Jul 28 2003 - <markmc@sun.com>
- Make pdfs get opened in the gpdf component by default

* Wed Jul 09 2003 - <michael.twomey@sun.com>
- add in sun po files

* Mon Jul 07 2003 - <niall.power@sun.com>
- added patch to shortlist nautilus_audio_view for viewing directory contents.

* Thu May 13 2003 - ghee.teo@Sun.COM
- Created new spec file for gnome-mime-data
