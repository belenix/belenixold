#
# spec file for package gnome-user-docs
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: davelam
#
Name:		        gnome-user-docs
License:		FDL
Group:			Documentation
BuildArchitectures:	noarch
Version:		2.26.0
Release:		48
Distribution:		Java Desktop System
Vendor:			Sun Microsystems, Inc.
Summary:		User Documentation for the GNOME desktop
Source:		        http://ftp.gnome.org/pub/GNOME/sources/gnome-user-docs/2.26/gnome-user-docs-%{version}.tar.bz2
URL:			http://developer.gnome.org/projects/gdp/
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
Docdir:			%{_defaultdocdir}/doc

%define			scrollkeeper_version 0.3.12

Prereq:			scrollkeeper >= %{scrollkeeper_version}
Requires:		scrollkeeper >= %{scrollkeeper_version}

%description
This package contains general GNOME user documentation which is not 
directly associated with any particular GNOME application or package.

%prep
%setup -q -n gnome-user-docs-%{version}
for f in gnome2-user-guide/bg/*.xml gnome2-user-guide/zh_CN/*.xml; do
  dos2unix -ascii $f $f
done


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
aclocal $ACLOCAL_FLAGS
automake -a -c -f
autoconf

./configure --prefix=%{_prefix}			\
            --datadir=%{_datadir}		\
	    --disable-scrollkeeper
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
chmod -R a+rX $RPM_BUILD_ROOT%{_datadir}/gnome/help

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = "2" ] ; then # upgrade
  if which scrollkeeper-update>/dev/null 2>&1; then scrollkeeper-update -q; fi
fi

%files
%defattr(-,root,root)
%doc COPYING COPYING-DOCS AUTHORS README ChangeLog NEWS INSTALL
%{_datadir}/gnome/help/*
%{_datadir}/omf/*

%changelog
* Tue Mar 17 2009 - dave.lin@sun.com
- Bump to 2.26.0
* Fri Mar 13 2009 - dave.lin@sun.com
- Bump to 2.25.1
* Wed Mar 11 2009 - dave.lin@sun.com
- Took the ownership of this spec file.
* Mon Sep 29 2008 - christian.kelly@sun.com
- Bump to 2.24.0.
* Tue May 27 2008 - damien.carbery@sun.com
- Bump to 2.22.1.
* Mon Mar 10 2008 - damien.carbery@sun.com
- Bump to 2.22.0.
* Fri Oct 19 2007 - damien.carbery@sun.com
- Bump to 2.20.1.
* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 2.20.0.
* Tue Jul 03 2007 - damien.carbery@sun.com
- Bump to 2.18.2.
* Tue Apr 10 2007 - damien.carbery@sun.com
- Bump to 2.18.1.
* Tue Mar 13 2007 - damien.carbery@sun.com
- Bump to 2.18.0.
* Tue Oct 03 2006 - damien.carbery@sun.com
- Bump to 2.16.1.
* Tue Sep 05 2006 - damien.carbery@sun.com
- Bump to 2.16.0.
* Mon Sep 04 2006 - damien.carbery@sun.com
- Single threaded 'make' call because multi-threaded one often fails.
* Wed Aug 16 2006 - damien.carbery@sun.com
- dos2unix some xml files that were breaking the build.
* Wed Aug 09 2006 - damien.carbery@sun.com
- Bump to 2.15.1.
* Tue Apr 11 2006 - damien.carbery@sun.com
- Bump to 2.14.2.
* Fri Apr 10 2006 - damien.carbery@sun.com
- Bump to 2.14.1.
* Mon Mar 13 2006 - damien.carbery@sun.com
- Bump to 2.14.0.
* Wed Feb 22 2006 - damien.carbery@sun.com
- Correct %setup dir name for new tarball.
* Tue Feb 21 2006 - damien.carbery@sun.com
- Bump to 2.13.1.1.
* Thu Dec 08 2005 - damien.carbery@sun.com
- Remove l10n stuff and associated patches. Not maintained for OpenSolaris.
* Tue Nov 29 2005 - laca@sun.com
- remove javahelp stuff
* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 2.8.1.
* Fri Jul 15 2005 - damien.carbery@sun.com
- Use Linux docs tarballs on Solaris because some omf files missing.
* Mon Jun 20 2005 - matt.keenan@sun.com
- Update l10n tarball to 1.3
* Thu May 05 2005 - damien.carbery@sun.com
- Updated docs tarball (gnome-user-docs-AG-0.10linux) from irene.ryan@sun.com.
* Wed May 04 2005 - damien.carbery@sun.com
- Updated docs tarball (gnome-user-docs-AG-0.9linux) from irene.ryan@sun.com.
- Updated docs tarball (gnome-user-docs-SAG-0.17linux) from 
  eugene.oconnor@sun.com.
* Thu Apr 21 2005 - damien.carbery@sun.com
- Updated docs (gnome-user-docs-ORMS-0.12linux) from maeve.anslow@sun.com.
* Fri Apr 08 2005 - damien.carbery@sun.com
- Updated docs (gnome-user-docs-ORMS-0.11linux) from irene.ryan@sun.com.
* Fri Apr 08 2005 - ghee.teo@sun.com
- Reinsert Prereq for scrollkeeper which was in B28 that governs the
  whereabout this rpm resides on the disk. Currently, gnome-user-docs
  sitting on CD1 seems to cause scriptlet failure during install no
  matter whatever is the content of the postinstall scriptlet.
* Thu Apr 07 2005 - damien.carbery@sun.com
- Updated docs (gnome-user-docs-ORMS-0.10linux) from maeve.anslow@sun.com.
* Wed Apr 06 2005 - damien.carbery@sun.com
- Updated docs tarball (gnome-user-docs-UG-0.28linux) from brian.casey@sun.com.
- Updated docs (gnome-user-docs-ORMS-0.9linux) from maeve.anslow@sun.com.
* Mon Apr 04 2005 - damien.carbery@sun.com
- Updated docs tarball (gnome-user-docs-UG-0.27linux) from brian.casey@sun.com.
* Thu Mar 31 2005 - ghee.teo@sun.com
- Putback the Requires dependency and also postinstall script for Update
  only to fix 6245485.
* Thu Mar 31 2005 - damien.carbery@sun.com
- Updated docs tarball (gnome-user-docs-SAG-0.16linux) from 
  eugene.oconnor@sun.com.
* Mon Mar 21 2005 - damien.carbery@sun.com
- Updated docs tarball (gnome-user-docs-UG-0.26linux) from brian.casey@sun.com.
* Fri Mar 11 2005 - damien.carbery@sun.com
- Updated docs tarball (gnome-user-docs-AG-0.8linux) from irene.ryan@sun.com.
- Updated docs (gnome-user-docs-ORMS-0.8linux) from irene.ryan@sun.com.
* Wed Mar 09 2005 - kazuhiko.maekawa@sun.com
- Updated patches/gnome-user-docs-01-l10n-online-help.diff to add online_update
* Fri Feb 25 2005 - damien.carbery@sun.com
- Updated docs tarball (gnome-user-docs-UG-0.25linux) from irene.ryan@sun.com.
* Mon Feb 21 2005 - damien.carbery@sun.com
- Updated docs (gnome-user-docs-ORMS-0.7linux) from maeve.anslow@sun.com.
* Wed Feb 16 2005 - damien.carbery@sun.com
- Updated docs (gnome-user-docs-ORMS-0.6linux) from irene.ryan@sun.com.
* Fri Feb 11 2005 - damien.carbery@sun.com
- Updated docs (gnome-user-docs-ORMS-0.5linux) from irene.ryan@sun.com.
* Wed Feb 09 2005 - damien.carbery@sun.com
- Updated docs tarball (gnome-user-docs-AG-0.7linux) from irene.ryan@sun.com.
- Updated docs (gnome-user-docs-ORMS-0.4linux) from maeve.anslow@sun.com.
* Tue Feb 08 2005 - damien.carbery@sun.com
- Updated docs tarball (gnome-user-docs-UG-0.24linux) from brian.casey@sun.com.
* Tue Jan 25 2005 - damien.carbery@sun.com
- Updated docs tarball (gnome-user-docs-UG-0.23linux) from brian.casey@sun.com.
* Fri Jan 14 2005 - damien.carbery@sun.com
- Updated docs tarball (gnome-user-docs-SAG-0.15linux) from 
  eugene.oconnor@sun.com.
* Thu Dec 16 2004 - kazuhiko.maekawa@sun.com
- Update l10n help tarball to use linux version
* Fri Dec 10 2004 - damien.carbery@sun.com
- Updated docs tarball (gnome-user-docs-SAG-0.14linux) from 
  eugene.oconnor@sun.com.
- Updated docs tarball (gnome-user-docs-AG-0.6linux) from irene.ryan@sun.com.
* Fri Dec  3 2004 - damien.carbery@sun.com
- Updated docs tarball (gnome-user-docs-UG-0.22linux) from brian.casey@sun.com.
- Updated gnome-user-docs-09-linux-user-guide.diff to add new file, 
  appendixa.xml.
- Updated docs (gnome-user-docs-ORMS-0.2linux) from maeve.anslow@sun.com.
* Thu Nov 25 2004 - damien.carbery@sun.com
- Fix 6197994: Add Linux-specific patches to remove references to files not in
  the Linux docs tarballs and add files that are (but not in Solaris tarball).
* Fri Nov 12 2004 - damien.carbery@sun.com
- Updated docs tarball (gnome-user-docs-UG-0.21solaris) from 
  brian.casey@sun.com.
- Updated docs tarball (gnome-user-docs-ORMS) from maeve.anslow@sun.com.
  Added '%ifos solaris' to handle this Solaris version of the tarball.
* Thu Nov 11 2004 - damien.carbery@sun.com
- Update docs tarball (gnome-user-docs-AG-0.5) from irene.ryan@sun.com. Update
  patch gnome-user-docs-07-access_guide.diff to add new file.
* Tue Nov  2 2004 - damien.carbery@sun.com
- Updated docs tarball (gnome-user-docs-UG-0.20linux) from brian.casey@sun.com.
* Tue Oct 26 2004 - damien.carbery@sun.com
- Updated docs tarball (gnome-user-docs-SAG) from Eugene.oconnor@sun.com.
  Added '%ifos solaris' to handle this Solaris version of the tarball.
* Thu Oct 21 2004 - matt.keenan@sun.com
- #6179792, fix permissions problem with some loading help files.
* Fri Oct 15 2004 - kazuhiko.maekawa@sun.com
- Change patch1 order not to overwride by tar
- Updated l10n help tarball.  gnome-user-docs-l10n-online-help-ci.tar.bz2
* Wed Oct  6 2004 - damien.carbery@sun.com
- Updated docs tarball (gnome-user-docs-ORMS-0.5) from maeve.anslow@sun.com.
* Thu Sep 30 2004 - damien.carbery@sun.com
- Updated docs tarball (gnome-user-docs-UG-0.19ssolaris) from 
  brian.casey@sun.com.
- Update docs tarball (gnome-user-docs-AG-0.4) from irene.ryan@sun.com. Update
  patch gnome-user-docs-07-access_guide.diff to add two new files.
* Fri Sep 24 2004 - damien.carbery@sun.com
- Change UG-0.18sparc tarball to UG-0.18solaris and use for x86 and sparc at
  request of Brian.
* Thu Sep 23 2004 - damien.carbery@sun.com
- Updated docs tarball (gnome-user-docs-UG-0.18sparc) from brian.casey@sun.com.
  This is sparc only so '%ifarch sparc' is used.
* Wed Sep 22 2004 - damien.carbery@sun.com
- Updated docs tarball (gnome-user-docs-UG-0.17) from brian.casey@sun.com.
* Tue Sep 21 2004 - damien.carbery@sun.com
- Updated docs tarball (gnome-user-docs-ORMS-0.4) from maeve.anslow@sun.com.
* Sun Sep 19 2004 - laca@sun.com
- fix file permissions
* Thu Sep 02 2004 - damien.carbery@sun.com
- Integrated updated docs tarball from patrick.costello@sun.com.
- Added javahelp-convert for new docs. Also updated orms patch.
* Wed Sep 01 2004 - matt.keenan@sun.com
- Added javahelp-convert for mozilla_info/office_info/sample_apps_info
* Tue Aug 31 2004 - damien.carbery@sun.com
- Update docs tarball (gnome-user-docs-UG-0.16) from brian.casey@sun.com.
* Wed Aug 25 2004 - Kazuhiko.Maekawa@sun.com
- Updated l10n help contents
* Fri Aug 20 2004 - damien.carbery@sun.com
- Integrated updated docs tarball from breda.mccolgan@sun.com.
* Thu Aug 19 2004 - damien.carbery@sun.com
- Add docs tarball (gnome-user-docs-ORMS-0.1) from breda.mccolgan@sun.com.
- Update docs tarball (gnome-user-docs-AG-0.3) from irene.ryan@sun.com
* Thu Aug 19 2004 - damien.carbery@sun.com
- Updated /usr/share/gnome/help/user-guide/*/*.xml to 0755 for integration.
* Mon Aug 16 2004 - damien.carbery@sun.com
- Updated /usr/share/gnome/help/user-guide/*/*.xml to 0644 for Solaris
  integration.
* Thu Aug 12 2004 - damien.carbery@sun.com
- Update docs tarball (gnome-user-docs-UG-0.15) from brian.casey@sun.com
* Wed Aug 11 2004 - damien.carbery@sun.com
- Add new docs tarball (gnome-user-docs-SAG-0.12.tar.bz2) from
  eugene.oconnor@sun.com.
* Sun Jul 11 2004 - damien.carbery@sun.com
- Remove javahelp-convert-install code for quick start guide.
* Sat Jul 10 2004 - damien.carbery@sun.com
- Remove javahelp-convert-install code for introduction-to-gnome.
* Fri Jul 09 2004 - damien.carbery@sun.com
- Disable patch 3 that adds sun-desktop (aka quick start user guide) Makefiles.
  This fixes bug 5072270.
* Wed Jul 07 2004 - damien.carbery@sun.com
- Add accessibility tarball and patch.
* Wed Jul 07 2004 - damien.carbery@sun.com
- Add new docs tarball (gnome-user-docs-SAG-0.11.tar.bz2) from
  eugene.oconnor@sun.com. Add patch gnome-user-docs-06-sag_update.diff to
  incorporate these docs.
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Mon Jul 05 2004 - damien.carbery@sun.com
- Update new docs tarball (gnome-user-docs-UG-0.14) from brian.casey@sun.com
* Mon Jun 14 2004 - damien.carbery@sun.com
- Add patch to comment out omf_dest_dir assignment in
  gnome2-user-guide/C/Makefile.am. Old docs tarball had its own Makefile.am
  which hid this issue.
* Thu Jun 10 2004 - damien.carbery@sun.com
- Incorporate new docs tarball from brian.casey@sun.com
* Fri May 28 2004 - damien.carbery@sun.com
- Incorporate new docs tarball from brian.casey@sun.com
* Tue May 04 2004 - matt.keenan@sun.com
- Remove jdstoc (Master Help set for Javahelp), now delivered
- in it's own module "jdstoc"
* Sun Apr 18 2004 - laca@sun.com
- enable javahelp conversion on Solaris
* Thu Apr 15 2004 Matt Keenan <matt.keenan@sun.com>
- Added jdstoc (Master Help Set for Javahelp)
* Wed Apr 14 2004 Matt Keenan <matt.keenan@sun.com>
- Patch to ensure preface.xml is installed for user-guide
* Mon Apr 05 2004 Dermot McCluskey <dermot.mccluskey@sun.com>
- new tarball: gnome-user-docs-UG-SAG-0.09.tar.bz2 (Makefile.am error)
* Thu Apr 01 2004 Matt Keenan <matt.keenan@sun.com>
- Javahelp conversion
* Thu Apr 01 2004 Dermot McCluskey <dermot.mccluskey@sun.com>
- update UG-SAG tarball to gnome-user-docs-UG-SAG-0.08.tar.bz2
* Thu Feb 19 2004 Matt Keenan <matt.keenan@sun.com>
- Update to 2.5.0, report patches
* Sat Oct 18 2003 Laszlo Peter <laca@sun.com>
- Update to 2.4.1
* Fri Sep 26 2003 Laszlo Peter <laca@sun.com>
- Updated the user's guide
* Tue Aug 26 2003 Michael Twomey <michael.twomey@sun.com>
- Updated to 0.2 l10n docs tarball to fix seriesid issues.
- Changing to use just scrollkeeper-update to fix i18n issues.
* Mon Aug 18 2003 Matt Keenan <matt.keenan@sun.com>
- Added new sun-section
* Wed Jul 16 2003 Michael Twomey <michael.twomey@sun.com>
- Updated to newer l10n docs tarball.
* Fri Jul 11 2003 Laca Peter <laca@sun.com>
- Initial version
