#
# spec file for package gnome-backgrounds
#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: erwannc
#
Name:			gnome-backgrounds
License:		GPL
Group:			System/GUI/GNOME
Version:		2.24.1
Release:		1
Distribution:		Java Desktop System
Vendor:			Sun Microsystems, Inc.
Summary:		Selection of backgrounds for the GNOME desktop
Source:			http://ftp.gnome.org/pub/GNOME/sources/%{name}/2.24/%{name}-%{version}.tar.bz2
%if %build_l10n
Source1:                 l10n-configure.sh
%endif
URL:			http://www.gnome.org
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
BuildArchitectures:     noarch
Docdir:			%{_defaultdocdir}/%{name}
Autoreqprov:		on

Requires:	glib2
BuildRequires:  intltool
BuildRequires:  glib2

%description
Selection of backgrounds for the GNOME desktop.

%prep
%setup -q
# Fix 326430.
for po in po/*.po; do
  dos2unix -ascii $po $po
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
intltoolize --copy --force --automake

%if %build_l10n
bash -x %SOURCE1 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS 
automake -a -c -f
autoconf
CFLAGS="$RPM_OPT_FLAGS" \
  ./configure \
	--prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir} \
	--mandir=%{_mandir}
make -j $CPUS

%install
make -i install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, root)
%{_datadir}/gnome-background-properties
%{_datadir}/pixmaps/backgrounds/
%{_datadir}/locale/*/LC_MESSAGES/*.mo

%changelog
* Wed Mar 18 2009 - dave.lin@sun.com
- Bump to 2.24.1
* Sat Sep 27 2008 - brian.cameron@sun.com
- Bump to 2.24.0.
* Wed Sep 10 2008 - christian.kelly@sun.com
- Bump to 2.23.92.
* Tue Sep 02 2008 - christian.kelly@sun.com
- Bump to 2.23.91.
* Tue Aug 19 2008 - dave.lin@sun.com
- Bump to 2.23.90
* Wed Jul 23 2008 - damien.carbery@sun.com
- Bump to 2.23.0.
* Mon Mar 10 2008 - damien.carbery@sun.com
- Bump to 2.22.0.
* Mon Jan 21 2008 - glynn.foster@sun.com
- Move OpenSolaris backgrounds to new module on opensolaris.org
* Wed Oct  3 2007 - laca@sun.com
- add indiana background(s) patch and Source
* Fri Sep 28 2007 - laca@sun.com
- do not install sun branded desktop wallpapers when sun branding is
  not requested
* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 2.20.0.
* Mon Jul 02 2007 - damien.carbery@sun.com
- Bump to 2.18.3.
* Mon Nov 27 2006 - damien.carbery@sun.com
- Bump to 2.16.2.
* Mon Oct 02 2006 - damien.carbery@sun.com
- Bump to 2.16.1.
* Tue Aug 22 2006 - damien.carbery@sun.com
- Bump to 2.15.92.
* Fri Jul 21 2006 - damien.carbery@sun.com
- Bump to 2.14.2.1.
* Thu Apr 13 2006 - damien.carbery@sun.com
- Bump to 2.14.1.
* Thu Apr 13 2006 - dermot.mccluskey@sun.com
- replace sed with dos2unix to work around ^M problem in SVN
* Mon Mar 13 2006 - damien.carbery@sun.com
- Bump to 2.14.0.
* Wed Mar  1 2006 - laca@sun.com
- use sed instead of dos2unix for converting the po files, because dos2unix
  corrupts some UTF-8 strings
* Wed Mar  1 2006 - damien.carbery@sun.com
- Bump to 2.13.92.
* Tue Feb 14 2006 - damien.carbery@sun.com
- Bump to 2.13.91.
* Tue Jan 31 2006 - damien.carbery@sun.com
- Bump to 2.13.90.
- Add intltoolize call.
* Tue Jan 10 2006 - damien.carbery@sun.com
- dos2unix vi.po to fix 326430.
* Wed Dec 21 2005 - damien.carbery@sun.com
- Bump to 2.12.2.
* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 2.10.2.
* Fri Mar 20 2005 - glynn.foster@sun.com
- Install the sun backgrounds here
* Fri Mar 13 2005 - glynn.foster@sun.com
- Initial import of gnome-backgrounds
