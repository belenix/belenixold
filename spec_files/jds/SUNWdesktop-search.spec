#
# spec file for packages SUNWdesktop-search
#
# includes module(s): tracker
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jerrytan
#

%include Solaris.inc

%define ff_ext_magic \{fda00e13-8c62-4f63-9d19-d168115b11ca\}
%define tb_ext_magic \{b656ef18-fd76-45e6-95cc-8043f26361e7\}
%use tracker = tracker.spec

Name:           SUNWdesktop-search
Summary:        Desktop search tool
Version:        %{default_pkg_version}
SUNW_BaseDir:   %{_basedir}
SUNW_Copyright: %{name}.copyright
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source1:        tracker-firefox-history-xesam.xpi
Source2:        tracker-thunderbird.xpi

%include default-depend.inc
Requires:       SUNWlibgnomecanvas
Requires:       SUNWdesktop-search-root
Requires:       SUNWgnome-media
Requires:       SUNWgnome-pdf-viewer
Requires:       SUNWgnome-utility-applets
Requires:       SUNWdbus
Requires:       SUNWgamin
Requires:       SUNWhal
Requires:       SUNWlibexif
Requires:       SUNWlibgmime
Requires:       SFElibgsf
Requires:       SUNWlxsl
Requires:       SUNWpng
Requires:       SUNWogg-vorbis
Requires:       SUNWsqlite3
Requires:       SUNWunzip
Requires:       SUNWw3m
Requires:       SUNWzlib

%if %option_with_gnu_iconv
Requires: SUNWgnu-libiconv
Requires: SUNWgnu-gettext
%else
Requires: SUNWuiu8
%endif

BuildRequires:  SUNWdbus-devel
BuildRequires:  SUNWgamin-devel
BuildRequires:  SUNWgnome-media-devel
BuildRequires:  SUNWgnome-pdf-viewer-devel
BuildRequires:  SUNWgnome-utility-applets-devel
BuildRequires:  SUNWhal
BuildRequires:  SUNWlibexif-devel
BuildRequires:  SUNWlibgmime-devel
BuildRequires:  SUNWlxsl-devel
BuildRequires:  SFElibgsf-devel
BuildRequires:  SUNWogg-vorbis-devel
BuildRequires:  SUNWpng-devel
BuildRequires:  SUNWsqlite3
BuildRequires:  SUNWevolution-devel
BuildRequires:  SUNWlibgnomecanvas-devel

%package devel
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%package firefox
Summary:        %{summary} - firefox extension files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SUNWfirefox

%package thunderbird
Summary:        %{summary} - thunderbird extension files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SUNWthunderbird

%prep
rm -rf %name-%version
mkdir -p %name-%version
%tracker.prep -d %name-%version

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CFLAGS="%optflags -D__EXTENSIONS__"
%if %option_with_gnu_iconv
export CFLAGS="$CFLAGS -I/usr/gnu/include"
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib -lintl"
%endif
export RPM_OPT_FLAGS="$CFLAGS"
%tracker.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%tracker.install -d %name-%version
cd %{_builddir}/%name-%version

# Install firefox extension
#mkdir -p $RPM_BUILD_ROOT%{_libdir}/firefox/extensions
#cd $RPM_BUILD_ROOT%{_libdir}/firefox/extensions
#mkdir %{ff_ext_magic}
#cd %{ff_ext_magic}
#unzip %SOURCE1

# Install thunderbird extension
mkdir -p $RPM_BUILD_ROOT%{_libdir}/thunderbird/extensions
cd $RPM_BUILD_ROOT%{_libdir}/thunderbird/extensions
mkdir %{tb_ext_magic}
cd %{tb_ext_magic}
unzip %SOURCE2

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc -d tracker-%{tracker.version} README AUTHORS
%doc(bzip2) -d tracker-%{tracker.version} COPYING ChangeLog NEWS po/ChangeLog
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
#%dir %attr (0755, root, bin) %{_libexecdir}
#%{_libexecdir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%{_libdir}/tracker*
%dir %attr (0755, root, bin) %{_libdir}/evolution
%dir %attr (0755, root, bin) %{_libdir}/evolution/2.26
%dir %attr (0755, root, bin) %{_libdir}/evolution/2.26/plugins/
%{_libdir}/evolution/2.26/plugins/*
%dir %attr (0755, root, bin) %{_libdir}/deskbar-applet
%dir %attr (0755, root, bin) %{_libdir}/deskbar-applet/modules-2.20-compatible
%{_libdir}/deskbar-applet/modules-2.20-compatible/tracker-module.py
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/tracker
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*.desktop
%dir %attr (0755, root, bin) %{_datadir}/dbus-1
%dir %attr (0755, root, bin) %{_datadir}/dbus-1/services
%{_datadir}/dbus-1/services/org.freedesktop.Tracker.*
%dir %attr (0755, root, bin) %{_datadir}/gtk-doc
%dir %attr (0755, root, bin) %{_datadir}/gtk-doc/html
%dir %attr (0755, root, bin) %{_datadir}/gtk-doc/html/libtracker-common
%{_datadir}/gtk-doc/html/libtracker-common/*
%dir %attr (0755, root, bin) %{_datadir}/gtk-doc/html/libtracker-module
%{_datadir}/gtk-doc/html/libtracker-module/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*
%defattr (-, root, other)
%{_datadir}/icons

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%dir %attr (0755, root, sys) %{_sysconfdir}/xdg
%dir %attr (0755, root, sys) %{_sysconfdir}/xdg/autostart
%{_sysconfdir}/xdg/autostart/*.desktop

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

#%files firefox
#%defattr (-, root, bin)
#%dir %attr (0755, root, bin) %{_libdir}
#%{_libdir}/firefox

%files thunderbird
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/thunderbird


%changelog
* Mon Mar 23 2009 - jeff.cai@sun.com
- Add the dependencies on SUNWunzip, SUNWw3m, SUNWgnome-pdf-viewer and
  SUNWlxsl since xsltproc, unzip, w3m and pdf2text are used in the scripts
  under /usr/lib/tracker/filters/*/*filter
* Fri Sep 12 2008 - jerry.tan@sun.com
- add doc for copyright
* Mon Sep 01 2008 - halton.huo@sun.com
- Remove extension part under %{_libdir}/firefox3
* Mon Apr 14 2008 - nonsea@users.sourceforge.net
- Add Requires:SUNWlibgsf cause the pkg name change.
* Thu Mar 27 2008 - halton.huo@sun.com
- Add copyright file
* Tue Feb 26 2008 - halton.huo@sun.com
- Split -extension to -firefox and -thunderbird
- Use macro for extension dir
* Thu Feb 21 2008 - damien.carbery@sun.com
- Rename SUNWsqlite dependency to SUNWsqlite3 to match pkg from SFW.
* Fri Jan 25 2008 - nonsea@users.sourceforge.net
- Add Build/Requires SUNWgnome-utility-applets-devel so that deskbar-applet is
  available. This is required for the python module in tracker.
* Wed Jan 23 2008 - nonsea@users.sourceforge.net
- Add extension link to firefox3, remove it when FF3 rename to firefox.
* Wed Jan 02 2008 - nonsea@users.sourceforge.net
- Rename from SFEtracker to SUNWdesktop-search.
* Sun Nov 18 2007 - daymobrew@users.sourceforge.net
- Add support for building on Indiana systems
* Fri Nov 02 2007 - nonsea@users.sourceforge.net
- Split into base/tracker.spec
- Remove GNOMOE 2.19/2.20 install compatible part.
- Add package -extension to install firefox/thunderbird extensions.
* Fri Sep 28 2007 - nonsea@users.sourceforge.net
- Add patch thunderbird.diff to enable thunderbird index.
* Wed Sep 26 2007 - nonsea@users.sourceforge.net
- Bump to 0.6.3.
- Move wv and libgsf to Requires.
- Add patch w3m-crash to fix w3m crash on solaris.
* Fri Sep 21 2007 - trisk@acm.jhu.edu
- Fix install in GNOME 2.19/2.20
* Wed Sep 05 2007 - nonsea@users.sourceforge.net
- Bump to 0.6.2.
- Move w3m to Requires.
* Thu Aug 09 2007 - nonsea@users.sourceforge.net
- Bump to 0.6.1.
* Mon Aug 06 2007 - nonsea@users.sourceforge.net
- Add --enable-external-sqlite
* Fri Jul 24 2007 - nonsea@users.sourceforge.net
- Bump to 0.6.0.
- Remove dependency on file.
* Fri May 04 2007 - nonsea@users.sourceforge.net
- Add Requires to SFEsqlite
- Add conditional Requires to SFEwv
- Revert patch tracker-01-stdout.diff.
- Add attr (0755, root, other) to %{_datadir}/pixmaps
  and %{_datadir}/applications
* Fri May 04 2007 - nonsea@users.sourceforge.net
- Add conditional Require SFElibgsf SFEw3m
- Remove upstreamed patch tracker-01-stdout.diff
- Add URL and License.
* Fri May 04 2007 - nonsea@users.sourceforge.net
- Initial spec
