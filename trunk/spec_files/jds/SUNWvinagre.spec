#
# spec file for package SUNWvinagre
#
# includes module(s): vinagre
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#

%include Solaris.inc

%use vinagre = vinagre.spec

Name:               SUNWvinagre
Summary:            Vinagre - A VNC client for the GNOME Desktop
Version:            %{vinagre.version}
SUNW_Copyright:     %{name}.copyright
SUNW_BaseDir:       %{_basedir}
BuildRoot:          %{_tmppath}/%{name}-%{version}-build
Source1:            %{name}-manpages-0.1.tar.gz

%include default-depend.inc
Requires:           SUNWgnome-base-libs
Requires:           SUNWgnome-libs
Requires:           SUNWgnutls
Requires:           SUNWavahi-bridge-dsd
Requires:           SUNWgnome-component
Requires:           SUNWgnome-config
Requires:           SUNWgnome-panel
Requires:           SUNWgnome-vfs
Requires:           SUNWgtk-vnc
Requires:           SUNWlibpopt
Requires:           SUNWfontconfig
Requires:           SUNWfreetype2
Requires:           SUNWlibmsr
Requires:           SUNWlxmlr
Requires:           SUNWmlib
Requires:           SUNWxorg-clientlibs
Requires:           SUNWxwice
Requires:           SUNWxwplt
Requires:           SUNWdesktop-cache
Requires:           %{name}-root
BuildRequires:      SUNWgnome-base-libs-devel
BuildRequires:      SUNWgnome-libs-devel
BuildRequires:      SUNWgnutls-devel
BuildRequires:      SUNWavahi-bridge-dsd-devel
BuildRequires:      SUNWgnome-component-devel
BuildRequires:      SUNWgnome-config-devel
BuildRequires:      SUNWgnome-panel-devel
BuildRequires:      SUNWgnome-vfs-devel
BuildRequires:      SUNWgtk-vnc-devel
BuildRequires:      SUNWlibpopt-devel
BuildRequires:      SUNWlxml-devel
BuildRequires:      SUNWmlibh

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%package root
Summary:       %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir -p %name-%version
%vinagre.prep -d %name-%version
cd %{_builddir}/%name-%version
gzcat %SOURCE1 | tar xf -

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
%vinagre.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%vinagre.install -d %name-%version

# remove duplicated files in %{_datadir}/doc/vinagre,
# we have them in %{_datadir}/doc/SUNWvinagre
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/vinagre

# install man page
rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -r $RPM_BUILD_ROOT%{_datadir}/gnome/help/vinagre/[a-z][a-z]
rm -r $RPM_BUILD_ROOT%{_datadir}/gnome/help/vinagre/[a-z][a-z]_[A-Z][A-Z]
rm $RPM_BUILD_ROOT%{_datadir}/omf/vinagre/vinagre-[a-z][a-z].omf
rm $RPM_BUILD_ROOT%{_datadir}/omf/vinagre/vinagre-[a-z][a-z]_[A-Z][A-Z].omf
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri desktop-mime-cache icon-cache gconf-cache

%postun
%restart_fmri desktop-mime-cache

%files
%doc -d vinagre-%{vinagre.version} README AUTHORS
%doc(bzip2) -d vinagre-%{vinagre.version} COPYING ChangeLog po/ChangeLog help/ChangeLog NEWS
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/vinagre
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/vinagre-applet
%dir %attr (0755, root, bin) %{_libdir}/bonobo
%dir %attr (0755, root, bin) %{_libdir}/bonobo/servers
%{_libdir}/bonobo/servers/GNOME_VinagreApplet.server
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/vinagre
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/*/apps
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/*/mimetypes
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/*/status
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/vinagre/C
%{_datadir}/omf/vinagre/vinagre-C.omf
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/icons/hicolor/*/mimetypes/*
%{_datadir}/icons/hicolor/*/status/*
%dir %attr (-, root, root) %{_datadir}/mime
%dir %attr (-, root, root) %{_datadir}/mime/packages
%{_datadir}/mime/packages/vinagre-mime.xml
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%{_datadir}/omf/vinagre/vinagre-[a-z][a-z].omf
%{_datadir}/omf/vinagre/vinagre-[a-z][a-z]_[A-Z][A-Z].omf
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/vinagre/[a-z][a-z]
%{_datadir}/gnome/help/vinagre/[a-z][a-z]_[A-Z][A-Z]
%endif

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/vinagre.schemas


%changelog
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Tue Jan 06 2009 - halton.huo@sun.com
- Change %files to reflect version bumping
* Tue Dec 23 2008 - halton.huo@sun.com
- Update %files after bump to 2.25.3
* Mon Dec 22 2008 - halton.huo@sun.com
- update deps after run check-deps.pl
* Thu Nov 20 2008 - halton.huo@sun.com
- Add %{_datadir}/locale to %files l10n
* Thu Nov 13 2008 - halton.huo@sun.com
- Moved from SFE
* Wed Aug 20 2008 - nonsea@users.sourceforge.net
- Update %files becuase verion upgrading
* Wed Feb 20 2008 - nonsea@users.sourceforge.net
- Add -root package, add %post and %preun -root package.
- Update files according updated version.
* Fri Nov 30 2007 - nonsea@users.sourceforge.net
- Initial spec
