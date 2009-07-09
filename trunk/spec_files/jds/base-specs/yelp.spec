#
# spec file for package yelp 
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: mattman
#
%include l10n.inc
Name:         yelp
License:      GPL
Group:        System/GUI/GNOME
Version:      2.26.0
Release:      1
Distribution: Java Desktop System
Vendor:	      Sun Microsystems, Inc.
Summary:      The GNOME Help Browser 
Source:       http://ftp.gnome.org/pub/GNOME/sources/%{name}/2.26/%{name}-%{version}.tar.bz2
%if %build_l10n
Source1:      l10n-configure.sh
Source2:      %{name}-po-sun-%{po_sun_version}.tar.bz2
%endif
# date:2007-09-18 owner:dcarbery type:bug
Patch1:       yelp-01-va-args.diff
# date:2007-10-18 owner:mattman type:bug bugster:6610215 bugzilla:493751
Patch2:       yelp-02-search-crash.diff
# date:2008-04-20 owner:hawklu type:bug bugster:6646451 bugzilla:499744
Patch3:       yelp-03-using-firefox3-gecko.diff
# date:2008-08-21 owner:jedy type:branding
Patch4:       yelp-04-menu-entry.diff

URL:          www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Autoreqprov:  on

%define gconf_version 2.6.0
%define libxml2_version 2.6.5
%define gtk2_version 2.5.3
%define libgtkhtml_version 2.6.0
%define gnome_vfs_version 2.6.0
%define libgnomeui_version 2.6.0
%define libbonobo_version 2.6.0
%define libglade_version 2.5.1
%define libxslt_version 1.1.14
%define gail_version 1.8.4
%define pango_version 1.8.1
%define gnome_doc_utils_version 0.1.1
%define mozilla_version 1.7
%define mozilla_nspr_version 4.5.0

Requires: gtk2 >= %{gtk2_version}
Requires: gnome-vfs >= %{gnome_vfs_version}
Requires: libgtkhtml >= %{libgtkhtml_version}
Requires: libgnomeui >= %{libgnomeui_version}
Requires: libbonobo >= %{libbonobo_version}
Requires: libxslt >= %{libxslt_version}
Requires: libglade >= %{libglade_version}
Requires: libxml2 >= %{libxml2_version}
Requires: mozilla >= %{mozilla_version}
Requires: mozilla-nspr >= %{mozilla_nspr_version}

BuildRequires: pango-devel >= %{pango_version}
BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: gnome-vfs-devel >= %{gnome_vfs_version}
BuildRequires: libgtkhtml-devel >= %{libgtkhtml_version}
BuildRequires: libgnomeui-devel >= %{libgnomeui_version}
BuildRequires: libbonobo-devel >= %{libbonobo_version}
BuildRequires: libglade-devel >= %{libglade_version}
BuildRequires: libxslt-devel >= %{libxslt_version}
BuildRequires: gail-devel >= %{gail_version}
BuildRequires: libxml2-devel >= %{libxml2_version}
BuildRequires: GConf >= %{gconf_version}
BuildRequires: gnome-doc-utils >= %{gnome_doc_utils_version}
BuildRequires: mozilla >= %{mozilla_version}
BuildRequires: mozilla-nspr-devel >= %{mozilla_nspr_version}

%description
"Yelp" is the help browser for the GNOME 2.2 Desktop. It features man, info and docbook document sources.

%prep
%setup -q
%if %build_l10n
bzcat %SOURCE2 | tar xf -
cd po-sun; make; cd ..
%endif

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

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
glib-gettextize -f
intltoolize --force --copy

%if %build_l10n
bash -x %SOURCE1 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f
autoconf

%ifos solaris
NO_RTTI=--enable-cpp-rtti
%endif

./configure \
    --prefix=%{_prefix} \
    --datadir=%{_datadir}       \
    --sysconfdir=%{_sysconfdir} \
    --libexecdir=%{_libexecdir} \
    --with-gecko=firefox \
    --localstatedir=/var/lib $NO_RTTI
make -j $CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT
#Copy zh_HK from zh_TW
#Fixes bug 4930405
install -d $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES
install --mode=0644 $RPM_BUILD_ROOT%{_datadir}/locale/zh_TW/LC_MESSAGES/*.mo $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES/

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
SCHEMAS="yelp.schemas"
for S in $SCHEMAS; do
	gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$S >/dev/null
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, root)
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_bindir}/*
%{_datadir}/icons
%{_datadir}/yelp
%{_datadir}/applications/yelp.desktop
%{_libdir}/*
%{_mandir}/man1/*
%{_sysconfdir}/gconf/schemas/yelp.schemas

%changelog
* Mon Mar 23 2009 - dave.lin@sun.com
- Remove option --with-ff3 which is unnecessary.
* Tue Mar 17 2009 - dave.lin@sun.com
- Bump to 2.26.0
* Mon Mar 02 2009 - dave.lin@sun.com
- Bump to 2.25.1
* Wed Oct 01 2008 - takao.fujiwara@sun.com
- Add l10n tarball.
* Wed Sep 24 2008 - christian.kelly@sun.com
- Bump to 2.24.0.
* Tue Sep 09 2008 - christian.kelly@sun.com
- Bump to 2.23.91.
* Fri Aug 22 2008 - dave.lin@sun.com
- Bump to 2.23.2
* Thu Aug 21 2008 - jedy.wang@sun.com
- Add 04-menu-entry.diff.

* Fri Jul 11 2008 - brian.lu@sun.com
- Add bugId for the patch 04-using-firefox3-gecko

* Tue Jun 03 2008 - damien.carbery@sun.com
- Bump to 2.23.1. Remove upstream patch 03-g11n-cast-iteration. Renumber
  remainder.

* Fri May 16 2008 - damien.carbery@sun.com
- Disable Brian's patch, 04-using-firefox3-gecko, to build against firefox 2
  because FF3 is not stable enough to be the default broswer in Nevada.

* Mon Apr 21 2008 - brian.lu@sun.com
- Add patch yelp-04-using-firefox3-gecko.diff:
  build yelp with firefox3 devel package

* Wed Apr 09 2008 - damien.carbery@sun.com
- Bump to 2.22.1.

* Thu Mar 20 2008 - takao.fujiwara@sun.com
- Add yelp-03-g11n-cast-iteration.diff to avoid fr crash. CR 6656484.

* Mon Mar 10 2008 - damien.carbery@sun.com
- Bump to 2.22.0.

* Tue Jan 29 2008 - damien.carbery@sun.com
- Bump to 2.21.90. Remove upstream patch 03-search-crash-v2. 

* Thu Jan 24 2008 - glynn.foster@sun.com
- Fix up gconf schema install.

* Tue Jan 08 2008 - damien.carbery@sun.com
- Bump to 2.21.2.

* Tue Dec 04 2007 - matt.keenan@sun.com
- Add patch 03-search-crash-v2 fix bugster:6630773 bugzilla:501559

* Tue Dec 04 2007 - damien.carbery@sun.com
- Bump to 2.21.1.

* Thu Oct 18 2007 - matt.keenan@sun.com
- Add patch 02-search-crash fix bugster:6610215 bugzilla:480876

* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 2.20.0.
- Add patch 01-va-args to fix compilation issue.

* Wed Aug 15 2007 - damien.carbery@sun.com
- Bump to 2.19.90. Remove upstream patches, 01-macro-reference-crash and
  02-std-solaris.

* Wed Aug 01 2007 - damien.carbery@sun.com
- Add patch, 02-std-solaris, to fix 462440.

* Tue Jul 31 2007 - damien.carbery@sun.com
- Bump to 2.19.1. Remove obsolete patches, 01-null-frag-id and
  02-empty-contents-list.

* Wed Jun 13 2007 - matt.keenan@sun.com
- Fix crash for #6560664 patch in bugzilla #447107

* Thu Apr 12 2007 - damien.carbery@sun.com
- Bump to 2.18.1.

* Tue Apr 10 2007 - matt.keenan@sun.com
- New patch for 6534411, empty contents_list for locales throws critcal 
- gnome-vfs warnings.

* Tue Mar 13 2007 - damien.carbery@sun.com
- Bump to 2.18.0.

* Mon Nov 27 2006 - damien.carbery@sun.com
- Bump to 2.16.2.

* Tue Oct 03 2006 - damien.carbery@sun.com
- Bump to 2.16.1.

* Mon Sep 04 2006 - damien.carbery@sun.com
- Bug  Bugster:6471853 / Bugzilla:318996 - Null frag_id crash, add local patch

* Mon Sep 04 2006 - damien.carbery@sun.com
- Bump to 2.16.0.

* Tue Aug 08 2006 - damien.carbery@sun.com
- Bump to 2.15.91.

* Mon Jul 24 2006 - damien.carbery@sun.com
- Bump to 2.15.5.

* Fri Apr 10 2006 - damien.carbery@sun.com
- Bump to 2.14.1.

* Mon Mar 13 2006 - damien.carbery@sun.com
- Bump to 2.14.0.

* Mon Feb 27 2006 - damien.carbery@sun.com
- Bump to 2.13.6.

* Mon Feb 13 2006 - damien.carbery@sun.com
- Bump to 2.13.5.

* Tue Jan 31 2006 - damien.carbery@sun.com
- Bump to 2.13.4.
- Remove upstream patch, 01-build-xlibs.

* Mon Jan 19 2005 - glynn.foster@sun.com
- Add yelp-01-build-xlibs.diff so we can link
  against -lX11

* Mon Jan 19 2005 - glynn.foster@sun.com
- Bump to 2.13.3

* Tue Dec 20 2005 - dermot.mccluskey@sun.com
- Bump to 2.13.2

* Tue Nov 29 2005 - damien.carbery@sun.com
- Bump to 2.12.2.

* Sat Sep 17 2005 - glynn.foster@sun.com
- Bump to 2.12.0

* Mon Sep 05 2005 - damien.carbery@sun.com
- Bump to 2.11.92.

* Tue Aug 16 2005 - damien.carbery@sun.com
- Bump to 2.11.1.

* Tue Jun 21 2005 - matt.keenan@sun.com
- Add requires for mozilla

* Wed Jun 08 2005 - matt.keenan@sun.com
- port to 2.10
- Remove patch yelp-01-empty-struct-build-fix.diff
- Remove patch yelp-03-session-save.diff
- Rename patch yelp-04-yelp-sections.diff to yelp-01-yelp-sections.diff
- Remove patch yelp-06-yelp-pager.diff

* Fri Feb 25 2005 - matt.keenan@sun.com
- #6233172, Add Actions section, change Development Section

* Thu Feb 17 2005 - matt.keenan@sun.com
- #6228279, yelp crash viewing jdsoverview.xml

* Fri Dec 24 2004 - kazuhiko.maekawa@sun.com
- Bug fix for 6186542, added zh_HK entry in l10n.xml

* Mon Nov 15 2004 - matt.keenan@sun.com
- #6182913, patch yelp-04-help-sections.diff

* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to yelp-l10n-po-1.2.tar.bz2

* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds

* Thu May 20 2004 - arvind.samptur@wipro.com
- added yelp-03-session-save.diff. Yelp is session aware now!

* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to yelp-l10n-po-1.1.tar.bz2

* Thu May 06 2004 - matt.keenan@sun.com
- Bump to 2.6.1

* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to yelp-l10n-po-1.0.tar.bz2

* Wed Mar 24 2004 - glynn.foster@sun.com
- Bump to 2.6.0. Remove the sed build fixes, rename the
  empty struct diff, and update the potfiles patch.

* Mon Mar 22 2004 - laca@sun.com
- fix non-portable sed commands (bugzilla #134534)

* Thu Mar 18 2004 - matt.keenan@sun.com
- Bump to 2.5.91

* Thu Mar 11 2004 - yuriy.kuznetsov@sun.com
- added yelp-03-g11n-potfiles.diff 

* Tue Feb 24 2004 - matt.keenan@sun.com
- Bump to 2.5.5

* Tue Feb 17 2004 - niall.power@sun.com
- two patches two fix a solaris build issues
- add ACLOCAL_FLAGS to aclocal

* Fri Feb 06 2004 - matt.keenan@sun.com
- Bump to 2.5.4, remove two patches, update l10n tarball

* Tue Dec 16 2003 - glynn.foster@sun.com
- Bump to 2.5.1

* Fri Oct 31 2003 - glynn.foster@sun.com
- Removed the Sun Supported menu entry since we're
  removing the Extras menu.

* Mon Oct 13 2003 - matt.keenan@sun.com
- New 2.4 Tarball

* Tue Oct 07 2003 - matt.keenan@sun.com
- Second Change For Help Section for Java Desktop System

* Fri Sep 26 2003 - matt.keenan@sun.com
- Modified Help Section for Java Desktop System

* Fri Aug 22 2003 - Laszlo.Kovacs@sun.com
- categorycode patch

* Mon Aug 18 2003 - matt.keenan@sun.com
- Help sections patch

* Fri Aug 01 2003 - glynn.foster@sun.com
- Add menu categorization.

* Wed Jul 23 2003 - glynn.foster@sun.com
- Add back window icon.

* Thu Jul 10 2003 - michael.twomey@sun.com
- Added .po tarball

* Wed Jun 25 2003 - laca@Sun.COM
- Add libexec/* to %files

* Wed Jun 25 2003 - Glynn.Foster@Sun.COM
- Update the version of Yelp

* Wed May 14 2003 - Laszlo.Kovacs@Sun.COM
- Initial Sun release
