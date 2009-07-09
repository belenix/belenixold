#
# spec file for package SUNWgnome-wm
#
# includes module(s): metacity
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: erwannc
#
%include Solaris.inc

%use metacity = metacity.spec

Name:                    SUNWgnome-wm
Summary:                 GNOME window manager
Version:                 %{default_pkg_version}
Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires: SUNWxorg-headers
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWgnome-dialog
Requires: SUNWgnome-wm-root
Requires: SUNWgnome-libs
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-config
Requires: SUNWpostrun
Requires: SUNWbzip
Requires: SUNWzlib
Requires: SUNWlxml
Requires: SUNWlibms
Requires: SUNWdesktop-cache

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package  devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %{name}
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
%metacity.prep -d %name-%version
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build
export CFLAGS="%optflags -I/usr/sfw/include -I/usr/X11/include -I/usr/sfw/include/freetype2 -DANSICPP"
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="%_ldflags -L/usr/X11/lib -R/usr/X11/lib -L/usr/sfw/lib -R/usr/sfw/lib -lXrender"
export PKG_CONFIG_PATH=%{_pkg_config_path}

%metacity.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%metacity.install -d %name-%version

rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

# Move demo to demo directory.
#
install -d $RPM_BUILD_ROOT%{_prefix}/demo/jds/bin
mv $RPM_BUILD_ROOT%{_bindir}/metacity-window-demo $RPM_BUILD_ROOT%{_prefix}/demo/jds/bin/metacity-window-demo

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri desktop-mime-cache gconf-cache
%ifarch sparc
( echo 'test -x /usr/bin/gconftool-2 || {';
  echo '  echo "ERROR: gconftool-2 not found"';
  echo '  exit 0';
  echo '}';
  echo 'umask 0022';
  echo "GCONF_CONFIG_SOURCE=xml:merged:/etc/gconf/gconf.xml.defaults";
  echo 'export GCONF_CONFIG_SOURCE';
  echo "SDIR=%{_sysconfdir}/gconf/schemas";
  echo '/usr/bin/gconftool-2 --direct --config-source=$GCONF_CONFIG_SOURCE -t bool -s /apps/metacity/general/reduced_resources true'
) | $BASEDIR/lib/postrun -c JDS
%endif

%postun
%restart_fmri desktop-mime-cache

%files
%doc -d metacity-%{metacity.version} README AUTHORS MAINTAINERS
%doc(bzip2) -d metacity-%{metacity.version} NEWS COPYING ChangeLog
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libexecdir}/metacity-dialog
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%dir %attr (0755, root, other) %{_datadir}/gnome
%dir %attr(0755, root, bin) %{_datadir}/gnome/wm-properties
%{_datadir}/applications/*
%{_datadir}/gnome/wm-properties/*
%{_datadir}/gnome/help/*
%{_datadir}/metacity/icons
%{_datadir}/themes
%{_datadir}/gnome-control-center/keybindings
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%{_prefix}/demo/jds/bin/metacity-window-demo

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/metacity.schemas

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Wed Feb 18 2009 - dave.lin@sun.com
- Add BuildRequires: SUNWgnome-dialog as it requires zenity.
* Fri Dec 12 2008 - dave.lin@sun.com
- Fix gnome/help attribute issue.
* Thu Sep 02 2008 - christian.kelly@sun.com
- Unbump to 2.23.377, reworked patch 8.
* Thu Jan  3 2008 - laca@sun.com
- use gconf-install.script instead of an inline script
* Fri Sep 28 2007 - laca@sun.com
- delete SUNWxwrtl and SUNWxorg-clientlibs deps
- delete some unnecessary env variables
* Tue Aug 07 2007 - damien.carbery@sun.com
- Updated for %files for new tarball - change %{_datadir}/control-center to
  %{_datadir}/gnome-control-center.
* Mon May 14 2007 - erwann.chenede@sun.com
- Added new dir in %files
* Mon Sep 04 2006 - Matt.Keenan@sun.com
- New Manpage tarball
* Fri Jul 14 2006 - laca@sun.com
- update %post/%postun/etc scripts to support diskless client setup,
  part of 6448317
* Thu Jun 29 2006 - laca@sun.com
- update postrun scripts
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Thu May 25 2006 - laca@sun.com
- use post/preun scripts to install schemas into the merged gconf files
* Fri May 12 2006 - damien.carbery@sun.com
- Small update to dependency list after check-deps.pl run.
* Thu May 11 2006 - brian.cameron@sun.com
- Move metacity-window-demo to /usr/share/jds/bin and no longer include
  the useless manpage.
* Wed May 10 2006 - laca@sun.com
- merge -share pkg(s) into the base pkg(s)
* Fri Feb 17 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Sat Dec  3 2005 - laca@sun.com
- add %post script that runs update-desktop-database
* Thu Jun 02 2005 - brian.cameron@sun.com
- Install l10n package last since it fails when building
  outside of the official build.
* Thu May 19 2005 - brian.cameron@sun.com
- Update to 2.10 and fix packaging.
* Wed Nov 10 2004 - arvind.samptur@wipro.com
- Set reduced_resource key to true on sparc m/c's
* Fri Oct 08 2004 - kaushal.kumar@wipro.com
- Added patch metacity-02-enable-Sun-keys-Open-Front.diff.
  Fixes bug 5103120. 
* Sat Oct 02 2004 - laca@sun.com
- added %pkgbuild_postprocess
* Sat Sep 11 2004 - laca@sun.com
- Set LDFLAGS so Xrandr and Xrender can be found.
* Thu Sep 09 2004 - matt.keenan@sun.com
- Added metacity-message.1, metacity-window-demo.1 manpages
* Thu Aug 26 2004 - balamurali.viswanathan@wipro.com
- Added patch to use sdtprocess instead of gnome-system-monitor.
* Wed Aug 18 2004 - damien.carbery@sun.com
- Change manpage perms for Solaris integration.
* Sat Jun 26 2004  shirley.woo@sun.com
- Changed install location to /usr/...
* Wed Jun  2 2004 - takao.fujiwara@sun.com
- Added %{_datadir}/locale to install l10n messages
* Wed Mar 24 2004 - brian.cameron@sun.com
- Added SGML man page integration
* Mon Mar 01 2004 - <laca@sun.com>
- remove dependencies on SUNWgnome-libs-share and root
* Thu Feb 26 2004 - <laca@sun.com>
- set PERL5LIB for XML::Parser
* Mon Feb 22 2004 - <niall.power@sun.com>
- install gconf schemas at end of install stage.
- make clean stage clean stuff up.
