#
# spec file for package gksu
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: dkenny
#
%include l10n.inc
Name:         gksu
License:      GPL v2
Group:        Applications/System
Version:      1.3.0
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Graphical frontend to su
Source:       http://people.debian.org/~kov/gksu/old_stuff/gksu/gksu-%{version}.tar.gz
Source1:      %{name}-po-sun-%{po_sun_version}.tar.bz2
Source2:      l10n-configure.sh
# date:2006-08-03 owner:jim type:feature
Patch1:	      gksu-01-Makefile.diff
# date:2006-08-03 owner:jim type:feature
Patch2:	      gksu-02-gksu.diff
# date:2006-11-15 owner:calumb bugster:6489289 type:bug
Patch3:       gksu-03-hide-launch-menu-items.diff
# date:2009-04-06 owner:fujiwara bugster:6493486 type:bug state:upstream
Patch4:       gksu-04-g11n-trunk-string.diff
URL:          http://www.nongnu.org/gksu/
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/%{name}
Autoreqprov:  on
Prereq:       GConf


BuildRequires: gtk+-devel >= 2.4.0, libgksu-devel, libgksuui-devel
BuildRequires: gettext, intltool, perl(XML::Parser)
BuildRequires: bison, gtk-doc, libgksuui-devel, gtk2-devel, gnome-keyring-devel
BuildRequires: GConf2-devel

%description
Gtk+ frontend to /bin/su. It supports login shells and preserving environment
when acting as a su frontend. It is useful to menu items or other graphical
programs that need to ask a user's password to run another program as another
user.

%prep
%setup
sh -x %SOURCE2 --enable-sun-linguas
/bin/rm -f po/stamp-po
bzcat %SOURCE1 | tar xf -
cd po-sun; make; cd ..
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

# libtoolize --force
# aclocal $ACLOCAL_FLAGS
# automake -a -c -f
autoconf

CFLAGS="$RPM_OPT_FLAGS" \
  ./configure \
	--prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir} \
        --libexecdir=%{_libexecdir} \
        --mandir=%{_mandir} \
	--disable-scrollkeeper
make -j $CPUS


%install
make -i install DESTDIR=$RPM_BUILD_ROOT

%clean
# rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr (-, root, root)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README TODO
%doc %{_mandir}/man1/*.1*
%{_sysconfdir}/gconf/schemas/gksu.schemas
%{_bindir}/gksu*
%{_datadir}/gksu/
%{_datadir}/pixmaps/gksu*.png
%{_datadir}/applications/gksu*.desktop

%changelog
* Mon Apr 06 2009 - takao.fujiwara@sun.com
- Add patch gksu-04-g11n-trunk-string.diff. Back port the string from
  trunk for translations since the current gksu is old.
- Update gksu-02-gksu.diff. Back port the string from trunk.
- Add l10n tarball to back port the translations.
* Thu Sep 18 2008 - li.yuan@sun.com
- Add patch gksu-04-exit.diff. Quit gksu after launch the child process.
* Sun Jan 28 2007 - laca@sun.com
- update download url
* Wed Nov 15 2006 Calum Benson <calum.benson@sun.com>
- Remove menu items from launch menu, in line with latest JDS UI spec.
* Sat Apr 08 2006 Dries Verachtert <dries@ulyssis.org> - 1.3.4-1.2
- Rebuild for Fedora Core 5.
* Fri Jan 13 2006 Dag Wieers <dag@wieers.com> - 1.3.4-2
- Fixed group.
* Sat Sep 17 2005 Dries Verachtert <dries@ulyssis.org> - 1.3.4-1
- Initial package.
