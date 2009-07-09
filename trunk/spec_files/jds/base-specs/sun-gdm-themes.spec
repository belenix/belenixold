#
# spec file for package sun-gdm-themes
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: erwannc
#
Name:			sun-gdm-themes
License:		LGPL
Group:			System/GUI/GNOME
BuildArchitectures:	noarch
# NOTE: If the version is bumped the new tarball must be uploaded to the
#       Sun Download Center. Contact GNOME RE for assistance.
Version:		0.26
Release:		1
Distribution:		Java Desktop System
Vendor:			Sun Microsystems, Inc.
Summary:		Sun branded GNOME login manager theme
Source:			http://dlc.sun.com/osol/jds/downloads/extras/%{name}-%{version}.tar.gz
%if %build_l10n
Source1:		l10n-configure.sh
%endif
URL:			http://sun.com
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
Docdir:			%{_defaultdocdir}/%{name}
Autoreqprov:		on

%define intltool_version 0.25

BuildRequires:  intltool >= %{intltool_version}

%description
This package contains Sun branded GNOME login manager [GDM] themes 

%prep
%setup -q -n %name-%version
%if %build_l10n
sh -x %SOURCE1 --enable-sun-linguas
%endif

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

intltoolize --copy --force --automake

%if %build_l10n
bash -x %SOURCE1 --enable-copyright
%endif

libtoolize --force
aclocal $ACLOCAL_FLAGS
automake -a -c -f
autoconf

CFLAGS="$RPM_OPT_FLAGS" \
./configure \
	--prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir} \
	--localstatedir=/var/lib
make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%post

%files
%defattr (-, root, root)
%{_datadir}/gdm/themes/*

%changelog
* Fri Aug 24 2007 - takao.fujiwara@sun.com
- Add sun-gdm-themes-01-g11n-passwd-len.diff to locaize "Welcome to". CR 6551411
- Add sun-gdm-themes-02-g11n-po.diff for the translations.
- Add l10n-configure.sh

* Wed Sep 15 2004 - ciaran.mcdermott@sun.com
- added sun-gdm-themes-01-g11n-alllinguas.diff, to support all locales.

* Fri Jul 23 2004 - vinay.madyakoppal@wipro.com
- Up the version to 15 and reset the release

* Thu Jul 22 2004 - vinay.mandyakoppal@wipro.com
- Remove the patches as they are now integrated in to
  the cvs.

* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to sun-gdm-themes-l10n-po-1.2.tar.bz2

* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds

* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to sun-gdm-themes-l10n-po-1.1.tar.bz2

* Tue Apr 20 2004 - Chookij.Vanatham@Sun.COM
- moved 2 patches (sun-gdm-themes-01-trans_desktop.diff,
  sun-gdm-themes-02-g11n-truncated-username.diff) to sun-gdm-themes CVS
  and bumped the spec version to pick up sun-gdm-themes-0.14.tar.gz.

* Sat Apr 03 2004 - Chookij.Vanatham@Sun.COM
- added sun-gdm-themes-02-g11n-truncated-username.diff to fix 4955151

* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to sun-gdm-themes-l10n-po-1.0.tar.bz2

* Mon Feb 16 2004 - <niall.power@sun.com>
- replace tar jxf with the more solaris friendly
  bzcat piped through tar

* Mon Jan 19 2004 - damien.donlon@sun.com
- Updated l10n content to sun-gdm-themes-l10n-po-0.7.tar.bz2

* Mon Dec 22 2003 - takao.fujiwara@sun.com
- Adding sun-gdm-themes-01-trans_desktop.diff
* Fri Oct 31 2003 - damien.donlon@sun.com
- Adding sun-gdm-themes-l10n-po-0.6.tar.bz2 l10n content

* Sun Oct 26 2003 - <carl.gadener@sun.com>
- Bolder and Blue JDS banner
- Improved button alignment to handle all resolutions
- Offset panel 5% right/down according to Chester
- Changed order of buttons left-to-right with right most important
* Wed Oct 23 2003 - <carl.gadener@sun.com>
- Bolder Java Desktop System banner
- Sun Font on JDS
- Color Java Logo
* Tue Oct 21 2003 - glynn.foster@sun.com
- Updated tarball
* Sun Oct 19 2003 - damien.donlon@sun.com
- Adding sun-gdm-themes-l10n-po-0.4.tar.bz2 l10n content
* Tue Sep 02 2003 - <carl.gadener@sun.com>
- Added the new Sun default theme 
- renamed the others to meaningful names
* Fri Aug 08 2003 - <erwann@sun.com>
- bumped release for the new icons
* Tue Jul 22 2003 - <markmc@sun.com>
- update to 0.8.9.1
* Fri Jun 26 2003 - glynn.foster@Sun.COM
- It's a no architecture package
* Fri Jun 26 2003 - glynn.foster@Sun.COM
- Initial Sun release

