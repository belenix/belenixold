#
# # spec file for package SUNWgnome-desklets
#
# includes module(s): gdesklets
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: bewitche
#
%include Solaris.inc

%use gdesklets = gdesklets.spec

Name:                    SUNWgnome-desklets
Summary:                 GNOME desktop widgets engine
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWgtk2
Requires: SUNWPython
Requires: SUNWgnome-libs
Requires: SUNWlibrsvg
Requires: SUNWgnome-python-desktop
Requires: SUNWgnome-python-libs
Requires: SUNWgnome-desktop-prefs
Requires: SUNWdesktop-cache
BuildRequires: SUNWgtk2-devel
BuildRequires: SUNWPython-devel
BuildRequires: SUNWgnome-desktop-prefs-devel
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-python-desktop-devel
BuildRequires: SUNWgnome-python-libs-devel
BuildRequires: SUNWlibrsvg-devel

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
rm -rf %name-%version
mkdir %name-%version
%gdesklets.prep -d %name-%version

%build
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="%_ldflags"
%gdesklets.build -d %name-%version

%install
%gdesklets.install -d %name-%version 

# Change %{_bindir}/gdesklets symlink to a relative one.
cd $RPM_BUILD_ROOT%{_bindir}
rm gdesklets
ln -s  ../lib/gdesklets/gdesklets

# fixes %_datadir/gdesklets/Displays/Calendar/gfx/months/README
chmod -R a+rX $RPM_BUILD_ROOT

rm -r $RPM_BUILD_ROOT%{_datadir}/mime
rm $RPM_BUILD_ROOT%{_datadir}/applications/*.cache

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri desktop-mime-cache icon-cache

%postun
%restart_fmri desktop-mime-cache

%files
%doc -d gDesklets-%{gdesklets.version} AUTHORS
%doc(bzip2) -d gDesklets-%{gdesklets.version} COPYING README NEWS ChangeLog
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/gdesklets
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*.desktop
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/icons/gnome
%dir %attr (0755, root, other) %{_datadir}/icons/gnome/48x48
%dir %attr (0755, root, other) %{_datadir}/icons/gnome/48x48/mimetypes
%{_datadir}/icons/gnome/48x48/mimetypes/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Wed Sep 18 2008 - chris.wang@sun.com
- Update copyright
* Wed Jun 04 2008 - damien.carbery@sun.com
- Make %{_bindir}/gdesklets a relative symlink as absolute symlinks are not
  permitted by Solaris WOS.
* Mon Oct 15 2007 - laca@sun.com
- make all files in the package readable
* Thu Oct 11 2007 - halton.huo@sun.com
- Use desktop-database-install.script for %post
  and desktop-database-uninstall.script for %postun
* Thu Oct 11 2007 - halton.huo@sun.com
- Change the inline postinstall script to an include
* Thu Mar 22 2007 - halton.huo@sun.com
- Change %{_datadir}/icons/gnome/48x48/mimetypes attr to root:other.
* Thu Feb  8 2007 - damien.carbery@sun.com
- Update dependency list for files used in %post and during build.
* Mon Feb  5 2007 - damien.carbery@sun.com
- Set %dir %attr for icons dirs.
- Remove 'rm -rf $RPM_BUILD_ROOT' from %install as it is not needed.
* Thu Jan 29 2007 - <chris.wang@sun.com>
- initial creation

