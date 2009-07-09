#
# spec file for package SUNWgnome-commander
#
# includes module(s): gnome-commander
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: padraig
#
%include Solaris.inc

Name:                    SUNWgnome-commander
License:                 GPL
Summary:                 gnome commander file manager
Version:                 1.2.7
Source:                  http://ftp.gnome.org/pub/GNOME/sources/gnome-commander/1.2/gnome-commander-%{version}.tar.bz2
# date:2008-06-25 owner:padraig type:feature
Patch1:          gnome-commander-01-desktop-menu.diff
# date:2008-08-22 owner:fujiwara type:bug bugster:6739065 bugzilla:548948 state:upstream
Patch2:                  gnome-commander-02-g11n-collation-str.diff
# date:2008-08-22 owner:fujiwara type:feature bugster:6740270 bugzilla:548961 state:upstream
Patch3:                  gnome-commander-03-g11n-search-wz-im.diff
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:    %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFElibgsf-devel
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-vfs-devel
BuildRequires: SUNWPython
BuildRequires: SUNWgnome-python-libs-devel
Requires: SUNWgnome-vfs
Requires: SFElibgsf
Requires: SUNWgnome-libs
Requires: SUNWgnome-python-libs
Requires: SUNWdesktop-cache

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n gnome-commander-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export PYTHON="/usr/bin/python2.4"
export CFLAGS="%optflags -I/usr/gnu/include"
export LDFLAGS="-L/usr/gnu/lib -lgnuintl -lgnuiconv -R/usr/gnu/lib"

intltoolize --force --copy --automake
aclocal $ACLOCAL_FLAGS -I m4
automake -a -c -f
autoconf
./configure \
    --prefix=%{_prefix} \
    --disable-scrollkeeper
make prefix=%{_prefix} -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/gnome-commander/*.a
rm $RPM_BUILD_ROOT%{_libdir}/gnome-commander/*.la
rm $RPM_BUILD_ROOT%{_libdir}/gnome-commander/plugins/*.a
rm $RPM_BUILD_ROOT%{_libdir}/gnome-commander/plugins/*.la

%if %build_l10n
%else
# REMOVE l10n FILES
rm -r $RPM_BUILD_ROOT%{_datadir}/locale
#rm -r $RPM_BUILD_ROOT%{_datadir}/gnome/help/gnome-commander/[a-z]*
#rm -r $RPM_BUILD_ROOT%{_datadir}/omf/gnome-commander/*-[a-z]*.omf
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri desktop-mime-cache

%postun
%restart_fmri desktop-mime-cache

%files
%doc(bzip2) COPYING ChangeLog
%doc README NEWS
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/*/C
%{_datadir}/omf/gnome-commander/gnome-commander-C.omf
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/gnome-commander.1
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Wed Sep 10 2008 - padraig.obriain@sun.com
- Add %doc to %files for copyright
* Fri Aug 22 2008 - takao.fujiwara@sun.com
- Add gnome-commander-02-g11n-collation-str.diff to avoid crash on none UTF-8.
- Add gnome-commander-03-g11n-search-wz-im.diff to enable input method.
* Wed Aug 06 2008 - padraig.obriain@sun.com
- Update following review; bump to 1.2.7.
* Wed Jul 02 2008 - padraig.obriain@sun.com
- Copy from SFEgnome-commander
* Mon Feb 11 2008 - laca@sun.com
- add --disable-scrollkeeper configure option
* Thu Nov 15 2007 - daymobrew@users.sourceforge.net
- Add support for Indiana builds.
* Wed Oct 17 2007 - laca@sun.com
- add /usr/gnu to search paths for the indiana build
* Mon Oct 08 2007 - damien.carbery@sun.com
- Add deletion of /var files back for building on pre-GNOME 2.20 systems where
  scrollkeeper is used. The /var files are not installed when rarian is used.
* Mon Oct 08 2007 - damien.carbery@sun.com
- Add intltoolize call and remove some non-l10n rm calls.
* Tue Jun 12 2007 - damien.carbery@sun.com
- Add patches, 08-warnx and 09-other, to fix a few more build issues.
- Update %files and %install now that build is working.
* Mon Jun 11 2007 - damien.carbery@sun.com
- Initial version
