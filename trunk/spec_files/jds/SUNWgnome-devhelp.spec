#
# spec file for package SUNWdevhelp.spec
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s): devhelp
#
# Owner: halton
#

%include Solaris.inc
%use devhelp = devhelp.spec

Name:                    SUNWgnome-devhelp
Summary:                 API documentation browser for GNOME 2
Version:                 %{default_pkg_version}
Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:                SUNWgnome-base-libs
Requires:                SUNWgnome-panel
Requires:                SUNWfirefox
Requires:                %{name}-root
Requires:                SUNWdesktop-cache
Requires:                SUNWlibwnck
Requires:                SFEwebkit
BuildRequires:           SUNWgnome-base-libs-devel
BuildRequires:           SUNWgnome-panel-devel
BuildRequires:           SUNWfirefox-devel
BuildRequires:           SUNWlibwnck-devel

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package devel
Summary:                 %{summary} - developer files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SUNWgnome-base-libs-devel

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
%devhelp.prep -d %name-%version
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build
export CFLAGS="%optflags -I/usr/include/mps"
export LDFLAGS="%_ldflags"
export ACLOCAL_FLAGS="-I /usr/share/aclocal"
%if %cc_is_gcc
%else
export CXX="${CXX} -norunpath"
%endif
export CXXFLAGS="%cxx_optflags -I/usr/include/mps"
%devhelp.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%devhelp.install -d %name-%version
rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri gconf-cache

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*
%{_libdir}/gedit-2/plugins/devhelp*
%dir %attr (0755, root, sys) %{_datadir}
%doc -d devhelp-%{devhelp.version} README AUTHORS
%doc(bzip2) -d devhelp-%{devhelp.version} COPYING NEWS ChangeLog po/ChangeLog
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, bin) %{_datadir}/devhelp
%{_datadir}/devhelp/*
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/scalable/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/scalable/apps/
%{_datadir}/icons/hicolor/scalable/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/16x16
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/16x16/apps/
%{_datadir}/icons/hicolor/16x16/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/22x22/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/22x22/apps/
%{_datadir}/icons/hicolor/22x22/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/24x24/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/24x24/apps/
%{_datadir}/icons/hicolor/24x24/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/32x32/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/32x32/apps/
%{_datadir}/icons/hicolor/32x32/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48/apps/
%{_datadir}/icons/hicolor/48x48/apps/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%{_mandir}/*/*

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/devhelp.schemas

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Mon May 26 2008 - evan.yan@sun.com
- Modification has been made in base/devhelp.spec, so that we can support both
  of FF2 and FF3 now. Using --with-ff3 to build with FF3
* Fri May 16 2008 - damien.carbery@sun.com
- Undo Evan's change - revert to depend on SUNWfirefox/-devel because FF3 is
  not stable enough to be the default browser in Nevada.
* Thu May 08 2008 - evan.yan@sun.com
- Replace Build/Requires SUNWfirefox/-devel to SUNWfirefox3/-devel
- Remove hardcode of firefox inlude path.
* Thu Mar 27 2008 - simon.zheng@sun.com
- Add file SUNWgnome-devhelp.copyright.
* Thu Jan  3 2008 - laca@sun.com
- use gconf-install.script instead of an inline script
* Wed Oct 31 2007 - simon.zheng@sun.com
- Change the inline postinstall script to an include.
* Tue Apr 24 2007 - laca@sun.com
- make gconf postrun scripts consistent with other packages
- use $BASEDIR instead of $PKG_INSTALL_ROOT to fix diskless install
  (CR 6537817)
* Tue Apr 24 2007 - laca@sun.com
- s/0755/-/ in defattr so that files are not made all executable
* Thu Mar 19 2007 - simon.zheng@sun.com
- Add manpage.
* Thu Mar 15 2007 - damien.carbery@sun.com
- Add Build/Requires SUNWgnome-panel/-devel for libwnck.
* Wed March 14 2007 - simon.zheng@sun.com
- Initial version created, which stems from extra-spec-file
  created by li.ma@sun.com on sourceforge.net svn repository.
