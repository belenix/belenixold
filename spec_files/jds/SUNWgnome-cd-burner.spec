#
# spec file for package brasero
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: lin
#

%include l10n.inc
%include Solaris.inc

Name:           SUNWgnome-cd-burner
License:        GPL
Version:        2.26.1
Summary:        Gnome CD/DVD burner
Source:         http://ftp.gnome.org/pub/GNOME/sources/brasero/2.26/brasero-%{version}.tar.bz2
Source1:        l10n-configure.sh 
Source2:        brasero-po-sun-%{po_sun_version}.tar.bz2
URL:            http://www.gnome.org/projects/brasero
SUNW_Basedir:   %{_basedir}
SUNW_Copyright: %{name}.copyright
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
# date:2008-09-05 owner:lin type:branding
Patch1:         brasero-01-manpages.diff
Patch2:         brasero-02-src-data.diff
# date:2008-09-05 owner:lin type:branding
Patch3:         brasero-03-load-by-gksu.diff

%include default-depend.inc
BuildRequires: SUNWgtk2-devel
BuildRequires: SUNWgnome-media-devel
BuildRequires: SUNWtotem-pl-parser-devel
BuildRequires: SUNWlxml-devel
BuildRequires: SUNWdbus-devel
BuildRequires: SUNWhal
Requires: SUNWgtk2
Requires: %{name}-root
Requires: SUNWdesktop-cache
Requires: SUNWdbus
Requires: SUNWgnome-media
Requires: SUNWtotem-pl-parser
Requires: SUNWlxml
Requires: SUNWhal
Requires: SUNWgksu

%description
Brasero is a application to burn CD/DVD for the Gnome Desktop. It is designed to be as simple as possible and has some unique features to enable users to create their discs easily and quickly.

%package devel
Summary:                 %summary - developer files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %name

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%if %build_l10n
%package l10n
Summary: %{summary} - l10n files
%include default-depend.inc
Requires: %{name}
%endif

%prep
%setup -q -n brasero-%{version}
find . -name '*.c' -o -name '*.h' -exec dos2unix {} {} \;

bzcat %SOURCE2 | tar xf -
cd po-sun; make; cd ..

%patch1 -p0
%patch2 -p1
%patch3 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

intltoolize --copy --force --automake
sh %SOURCE1 --enable-copyright
libtoolize --copy --force
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f 
autoconf

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
    --libdir=%{_libdir}		\
    --libexecdir=%{_libexecdir}	\
    --sysconfdir=%{_sysconfdir}	\
    --disable-gnome2		\
    --disable-inotify		\
    --enable-shared		\
    --disable-static		\
    --disable-scrollkeeper	\
    --disable-gtk-doc		\
    --disable-cdrkit

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

# RBAC related
mkdir $RPM_BUILD_ROOT/etc/security

# prof_attr(4)
cat >> $RPM_BUILD_ROOT/etc/security/prof_attr <<EOF
Desktop Removable Media User:::Access removable media for desktop user:
Console User::::profiles=Desktop Removable Media User
EOF

# exec_attr(4)
cat >> $RPM_BUILD_ROOT/etc/security/exec_attr <<EOF
Desktop Removable Media User:solaris:cmd:::/usr/bin/brasero:privs=sys_devices
EOF

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri icon-cache desktop-mime-cache gconf-cache

%postun
%restart_fmri desktop-mime-cache

%files
%doc README AUTHORS
%doc(bzip2) ChangeLog NEWS COPYING
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%attr (0755, root, bin)%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, bin) %{_libdir}/brasero
%dir %attr (0755, root, bin) %{_libdir}/brasero/plugins
%{_libdir}/brasero/plugins/lib*.so
%{_libdir}/nautilus/extensions-2.0/*.so
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr(0755, root, bin) %{_datadir}/brasero
%{_datadir}/brasero/*
%dir %attr(0755, root, bin) %{_datadir}/omf
%{_datadir}/omf/*
%dir %attr(0755, root, root) %{_datadir}/mime
%dir %attr(0755, root, root) %{_datadir}/mime/packages
%{_datadir}/mime/packages/*
%dir %attr(0755, root, other) %{_datadir}/icons
%attr(-, root, other) %{_datadir}/icons/*
%dir %attr(0755, root, other) %{_datadir}/gnome
%dir %attr(0755, root, bin) %{_datadir}/gnome/help
%{_datadir}/gnome/help/*
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc

%files root
%defattr (0755, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/brasero.schemas
%config %class (rbac) %attr (0644, root, sys) /etc/security/prof_attr
%config %class (rbac) %attr (0644, root, sys) /etc/security/exec_attr

%if %build_l10n
%files l10n
%defattr(-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/locale
%attr(-, root, other) %{_datadir}/locale/*
%endif

%changelog
* Tue Apr 22 2009 - lin.ma@sun.com
- Updated gksu related patch, and fixed a nit of spec.
* Tue Apr 21 2009 - lin.ma@sun.com
- Added gksu related patch.
- Added dependency for gksu.
- Changed profile name.
* Tue Apr 14 2009 - brian.cameron@sun.com
- Bump to 2.26.1.
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Tue Mar 17 2009 - dave.lin@sun.com
- Bump to 2.26.0.
* Wed Mar 11 2009 - lin.ma@sun.com
- Create and new profile 'Desktop CD User' and 'Console User'.
- Removed file_dac_read, because console user owns the device.
* Tue Mar 03 2009 - lin.ma@sun.com
- Removed run-time dependency SUNWgksu, renamed to SUNWgnome-cd-burner.
- Restored removed patch 02-src-data.diff, because it's partly upstreamed.
* Mon Mar 02 2009 - dave.lin@sun.com
- Bump to 2.25.92.
- Removed upstreamed patch 02-src-data.diff.
* Tue Feb 24 2009 - lin.ma@sun.com
- Bump to 2.25.91.2 Add brasero-02-src-data.diff, add RBAC stuff.
* Tue Feb 17 2009 - brian.cameron@sun.com
- Bump to 2.25.91.  Remove upstream patch brasero-04-po.diff.
* Tue Feb 10 2009 - halton.huo@sun.com
- Add dependency on SUNWgnome-media-player, CR #6755918
* Fri Jan 16 2009 - takao.fujiwara@sun.com
- Add l10n tarball.
* Fri Jan 09 2009 - takao.fujiwara@sun.com
- Add patch po.diff from community trunk.
* Wed Sep 18 2008 - lin.ma@sun.com
- Bump to 0.8.2. Update copyright.
* Mon Sep 15 2008 - takao.fujiwara@sun.com
- Add brasero-03-g11n-im-jacket.diff to enable IM for jacket editor.
* Mon Aug 18 2008 - lin.ma@sun.com
- Initial version.

