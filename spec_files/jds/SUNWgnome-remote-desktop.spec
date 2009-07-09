#
# spec file for package SUNWgnome-remote-desktop
#
# includes module(s): vino, realvnc-java-client
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#
%include Solaris.inc

%define makeinstall make install DESTDIR=$RPM_BUILD_ROOT
%use vino = vino.spec
%if %option_with_java
%use rjc = realvnc-java-client.spec
%endif

Name:                    SUNWgnome-remote-desktop
Summary:                 GNOME remote desktop
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Source1:		 %{name}-manpages-0.1.tar.gz

%include default-depend.inc
Requires: SUNWgnome-libs
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-component
Requires: SUNWgnome-config
Requires: SUNWgnutls
Requires: SUNWjpg
Requires: SUNWlibgcrypt
Requires: SUNWzlib
Requires: SUNWdesktop-cache
Requires: SUNWgnome-panel
Requires: SUNWavahi-bridge-dsd
Requires: SUNWlibunique
Requires: %{name}-root
BuildRequires: SUNWgnome-component-devel
BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWgnutls-devel
BuildRequires: SUNWjpg-devel
BuildRequires: SUNWlibgcrypt-devel
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-panel-devel
BuildRequires: SUNWavahi-bridge-dsd-devel
BuildRequires: SUNWlibunique-devel

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir %name-%version
%vino.prep -d %name-%version
%if %option_with_java
%rjc.prep -d %name-%version
%endif
cd %{_builddir}/%name-%version
gzcat %SOURCE1 | tar xf -

%build
export PKG_CONFIG_PATH=%{_pkg_config_path}
export CFLAGS="%optflags -I%{_includedir} -I/usr/sfw/include"
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="%_ldflags -L/usr/sfw/lib -R/usr/sfw/lib"

%vino.build -d %name-%version
%if %option_with_java
%rjc.build -d %name-%version
%endif

%install
rm -rf $RPM_BUILD_ROOT
%vino.install -d %name-%version
%if %option_with_java
# install vnc client
cd %{name}-%{version}
cd vnc-*javasrc/java
install --mode=0755 vncviewer.jar $RPM_BUILD_ROOT%{_datadir}/vino/vino-client.jar
install --mode=0755 vino-client.html $RPM_BUILD_ROOT%{_datadir}/vino/vino-client.html
%endif

# install man page
rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):unsupported" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri desktop-mime-cache icon-cache gconf-cache

%postun
%restart_fmri desktop-mime-cache

%files
%doc vino-%{vino.version}/AUTHORS
%doc vino-%{vino.version}/README
%doc(bzip2) vino-%{vino.version}/COPYING
%doc(bzip2) vino-%{vino.version}/NEWS
%doc(bzip2) vino-%{vino.version}/ChangeLog
%doc(bzip2) vino-%{vino.version}/po/ChangeLog
%doc(bzip2) vnc-%{rjc.tarball_version}-javasrc/java/LICENCE.TXT
%doc(bzip2) vnc-%{rjc.tarball_version}-javasrc/java/README
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/vino-server
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/vino
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/vino-server.schemas
%{_sysconfdir}/xdg/autostart/vino-server.desktop

%changelog
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Sat Jan 24 2009 - halton.huo@sun.com
- Update %files, move autostart/vino-server.desktop to -root pkg.
* Sat Jan 24 2009 - halton.huo@sun.com
- Add Requires to libunique package
* Wed Nov 05 2008 - halton.huo@sun.com
- Add po/ChangeLog to %files
* Wed Sep 10 2008 - halton.huo@sun.com
- Add %doc to %files for new copyright
* Thu Aug 07 2008 - halton.huo@sun.com
- Add %{_datadir}/gnome/autostart for new gnome-session change.
* Thu Mar 27 2008 - halton.huo@sun.com
- Add copyright file
* Thu Jan  3 2008 - laca@sun.com
- use gconf-install.script instead of an inline script
* Fri Nov 02 2007 - halton.huo@sun.com
- Remove vncviewer wrapper since C version of vncviewer will be added.
* Fri Nov 02 2007 - halton.huo@sun.com
- Add SUNWavahi-bridge-dsd to Requires
- Add SUNWavahi-bridge-dsd-devel to BuildRequires
* Wed Oct 31 2007 - damien.carbery@sun.com
- Remove %{_datadir}/icons from %files as it is not installed.
* Thu Oct 11 2007 - halton.huo@sun.com
- Use desktop-database-install.script for %post
  and desktop-database-uninstall.script for %postun
* Thu Oct 11 2007 - halton.huo@sun.com
- change the inline postinstall script to an include
* Fri Sep 28 2007 - laca@sun.com
- disable building the java client when --without-java is used
- delete unneeded env variables
* Tue Jul 31 2007 - halton.huo@sun.com
- Add Requires: SUNWgnome-panel and BuildRequires: SUNWgnome-panel-devel
  because vino-server now depend on libnotify, fix bugster #6585037.
* Tue Jul 10 2007 - halton.huo@sun.com
- Use $prefix/share/vino for data in favor of $prefix/share/gnome/vino,
  refer bugzilla #436460.
* Fri Jun 22 2007 - halton.huo@sun.com
- Use realvnc-java-client.spec generate vino-client.jar and vino-client.html
- Add script wrapper /usr/bin/vncviewer for vino-client.jar 
* Tue Apr 24 2007 - laca@sun.com
- s/0755/-/ in defattr so that files are not made all executable
* Wed Nov 08 2006 - halton.huo@sun.com
- Add manpage section to fix bug, bugster #6489749
* Fri Spe 22 2006 - dermot.mccluskey@sun.com
- temporarily comment out manpage sections as source tarball does not exist
* Mon Sept 11 2006 - steven.zhang@sun.com
- update to add vnc client support with server
- update to add manpage
* Sat Aug 12 2006 - laca@sun.com
- change datadir/icons permissions back to root:other since it's a stable
  interface and wasn't supposed to be changed
* Fri Jul 14 2006 - laca@sun.com
- update %post/%postun/etc scripts to support diskless client setup,
  part of 6448317
* Thu Jun 29 2006 - laca@sun.com
- update postrun scripts
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Fri Jun  2 2006 - laca@sun.com
- use post/preun scripts to install schemas into the merged gconf files
* Thu May 11 2006 - halton.huo@sun.com
- Merge -share pkg(s) into the base pkg(s).
* Mon Feb 20 2006 - damien.carbery@sun.com
- Complete update of Build/Requires after running check-deps.pl script.
* Fri Feb 17 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Sat Dec  3 2005 - laca@sun.com
- add %post script that runs update-desktop-database
* Fri Sep 30 2005 - damien.carbery@sun.com
- Add applications and icons dirs under %{_datadir}.
* Sat Oct 02 2004 - laca@sun.com
- added %pkgbuild_postprocess
* Mon Aug 23 2004 - laca@sun.com
- s/SUNWpl5u/SUNWperl584usr/
* Thu Jun 23 2004 - shirley.woo@sun.com
- more changes for change install location to /usr/lib and /usr/bin
* Tue Jun 22 2004 - shirley.woo@sun.com
- changed install location to /usr/lib and /usr/bin
* Wed Jun  2 2004 - takao.fujiwara@sun.com
- Added %{_datadir}/locale to install l10n messages
* Fri May 07 2004 - brian.cameron@sun.com
- Removed locale/C from "%files share" since it doesn't
  exist.
* Thu Apr 15 2004 - brian.cameron@sun.com
- Created
