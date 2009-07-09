#
# spec file for package SUNWgnome-dtlogin-integration
#
# includes module(s): dtlogin-integration
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: laca
#
%define dtlogin_config_basedir /usr
# NOTE: If the version is bumped the new tarball must be uploaded to the
#       Sun Download Center. Contact GNOME RE for assistance.
%define tarball_version 0.37

%include Solaris.inc
Name:                    SUNWgnome-dtlogin-integration
SourcePackage:           SUNWgnome-dtlogin-integ-src
Summary:                 dtlogin configuration files for the JDS desktop
Version:                 %{default_pkg_version}
Source:                  http://dlc.sun.com/osol/jds/downloads/extras/dtlogin-integration-%{tarball_version}.tar.bz2
Source1:                 l10n-configure.sh
Source2:                 dtstart
Source11:                0011.env
Source12:                0020.pre-localization
Source13:                0060.sockets
Source14:                0070.dbus
Source15:                0110.fonts
Source16:                0120.xrdb
Source17:                0210.im
Patch1:                  %{name}-01-g11n-migration.diff
SUNW_BaseDir:            %{dtlogin_config_basedir}
SUNW_Copyright:          SUNWgnome-dtlogin-integration.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWgnome-panel
Requires: SUNWgnome-session
Requires: SUNWgnome-wm

%package -n SUNWdesktop-startup
Summary:                 Desktop startup scripts in xinitrc.d
SUNW_BaseDir:            /
%include default-depend.inc
Requires: SUNWgnome-panel
Requires: SUNWgnome-session
Requires: SUNWgnome-wm
Requires: SUNWgnome-component

%prep
%setup -q -n dtlogin-integration-%{tarball_version}

bash -x %SOURCE1 --enable-sun-linguas

%patch1 -p1

%build
export LDFLAGS="%_ldflags"
export CFLAGS="%optflags"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
libtoolize -f
intltoolize --force --copy --automake

%if %build_l10n
bash -x %SOURCE1 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS
autoconf
automake -acf

./configure --with-gnome-prefix=%{_prefix} \
            --prefix=%{dtlogin_config_basedir}

%install
rm -rf $RPM_BUILD_ROOT
%if %option_with_gnu_iconv
make install DESTDIR=$RPM_BUILD_ROOT ICONV=/usr/gnu/bin/iconv ENCODING=UTF-8
%else
make install DESTDIR=$RPM_BUILD_ROOT
%endif

%if %option_without_dt
rm -r $RPM_BUILD_ROOT%{dtlogin_config_basedir}/dt/appconfig
rm -r $RPM_BUILD_ROOT%{dtlogin_config_basedir}/dt/config/C
rm -r $RPM_BUILD_ROOT%{dtlogin_config_basedir}/dt/config/[a-z][a-z]*
rm -r $RPM_BUILD_ROOT%{dtlogin_config_basedir}/dt/config/Xsession*
rm -r $RPM_BUILD_ROOT%{dtlogin_config_basedir}/dt/config/Xinitrc*
rmdir $RPM_BUILD_ROOT%{dtlogin_config_basedir}/dt/config
rmdir $RPM_BUILD_ROOT%{dtlogin_config_basedir}/dt
%endif

install --mode=0755 -d $RPM_BUILD_ROOT/usr/bin
install --mode=0755 %SOURCE2 $RPM_BUILD_ROOT/usr/bin/dtstart

# Create dbus session initialisation script for dtlogin
%if %option_with_dt
install --mode=0755 -d $RPM_BUILD_ROOT/%{dtlogin_config_basedir}/dt/config/Xsession.d
install --mode=0755 %SOURCE14 $RPM_BUILD_ROOT/%{dtlogin_config_basedir}/dt/config/Xsession.d
%endif

# rough script number?
# 1 - 50: pre configurations
# 51 - 100: pre processes
# 101 - 150: post configurations
# 151 - 200: post processes

install --mode=0755 -d $RPM_BUILD_ROOT/etc/X11/xinit/xinitrc.d/
%if %option_with_dt
install --mode=0755 -d $RPM_BUILD_ROOT/%{dtlogin_config_basedir}/dt/config/Xsession.d
%endif

for FILE in %SOURCE11 %SOURCE12 %SOURCE13 %SOURCE15 %SOURCE16
do
  install --mode=0755 $FILE $RPM_BUILD_ROOT/etc/X11/xinit/xinitrc.d
%if %option_with_dt
  install --mode=0755 $FILE $RPM_BUILD_ROOT/%{dtlogin_config_basedir}/dt/config/Xsession.d
%endif
done

# 0210.im for xinitrc.d and 0020.dtims for Xsession.d
install --mode=0755 %SOURCE17 $RPM_BUILD_ROOT/etc/X11/xinit/xinitrc.d


rm -rf $RPM_BUILD_ROOT/tmp

%clean
rm -rf $RPM_BUILD_ROOT

%if %option_with_dt
%files
%defattr (-, root, bin)
%{dtlogin_config_basedir}/dt
%endif

%files -n SUNWdesktop-startup
%defattr (-, root, bin)
%dir %attr(0755, root, sys) /etc
%dir %attr(0755, root, sys) /etc/X11
%dir %attr(0755, root, sys) /etc/X11/xinit
%dir %attr(0755, root, sys) /etc/X11/xinit/xinitrc.d
/etc/X11/xinit/xinitrc.d/*
%dir %attr (0755, root, sys) /usr
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/dtstart


%changelog
* Mon Mar 23 2009 - jeff.cai@sun.com
- Since /usr/dt/config/Xinitrc.jds (SUNWgnome-dtstart) requires
  /usr/bin/linc-cleanup-sockets which is found in SUNWgnome-component,
  add the dependency.
* Thu Feb 05 2009 - takao.fujiwara@sun.com
- Renamed 0010.env to 0011.env for CDE.
* Wed Feb 04 2009 - takao.fujiwara@sun.com
- Add SUNWdesktop-startup for xinitrc.d scripts.
- Add patch g11n-migration.diff
* Thu Oct 02 2008 - ghee.teo@sun.com
- Bump up tarball to 0.37. Removed dtlogin-integration-02-dbus-launch.diff 
  and dtlogin-integration-01-vte-cjk.diff  which are now upstreamed.
* Fri Sep 19 2008 - ghee.teo@sun.com
- Added dtlogin-integration-02-dbus-launch.diff to fix 6750408.
* Thu Sep 11 2008 - takao.fujiwara@sun.com
- Add dtlogin-integration-01-vte-cjk.diff to fix 6745785.
* Fri Aug 29 2008 - ghee.teo@sun.com
- Released 0.36 tarball and remove these patches
- SUNWgnome-dtlogin-integration-01-no-mo.diff
- SUNWgnome-dtlogin-integration-02-ssh-agent.diff
- SUNWgnome-dtlogin-integration-03-dbus-launch.diff
* Thu Aug 28 2008 - ghee.teo@sun.com
- Added script to launch dbus session bus now that gnome-session does not do that.
* Mon Jul 21 2008 - jeff.cai@sun.com
- Not start ssh-agent because gnome-keyring-daemon has added this feature.
* Tue Apr  1 2008 - damien.carbery@sun.com
- Remove 'BuildRequires' lines for i18n pkgs that are no longer delivered to
  Nevada (beginning snv_86).
* Tue Feb 26 2008 - brian.cameron@sun.com
- Bump to 0.35.  This reverts the code change made on 2007-12-07 to
  launch gnome-session with "/bin/sh -c" rather than exec.  I
  discovered that using "/bin/sh -c" was having the unwanted
  side-effect of causing gnome-session and child processes to not
  have an associated TTY number.  For example, gnome-session should
  have a value like "pts/1", but when using "/bin/sh -c" it has "?".
  So reverting this change fixes this problem.  The original need
  to switch to "/bin/sh -c" has gone away now that we launch D-Bus
  from gnome-session instead of from the startup scripts.

* Wed Jan 09 2008 - brian.cameron@sun.com
- Bump to 0.34.
* Fri Dec 07 2007 - brian.cameron@sun.com
- Bump to 0.33.
* Thu Oct 25 2007 - takao.fujiwara@sun.com
- Add SUNWgnome-dtlogin-integration-01-no-mo.diff.
  We don't need .mo files for this package.
* Fri Sep 28 2007 - laca@sun.com
- combine SUNWgnome-dtlogin-integration and SUNWgnome-dtstart in one
  spec.  If this spec file is built without /usr/dt support then
  it builds SUNWgnome-dtstart with include /usr/bin/dtstart and the
  JDS startup scripts in /usr/dt/config.  /ust/bin/dtstart is a
  simple replacement for /usr/dt/bin/Xsession
* Fri Sep 07 2007 - brian.cameron@sun.com
- Bump to 0.32, remove upstream patch.
* Thu Aug 30 2007 - damien.carbery@sun.com
- Add intltoolize call to update intltool scripts.
* Mon Jul 23 2007 - takao.fujiwara@sun.com
- Added SUNWgnome-dtlogin-integration-01-g11n-xinitrc.diff. 
  Fixes 6555226, 6583891
* Tue Jun  5 2007 - laca@sun.com
- bump to 0.31, delete patch
* Mon Apr 02 2007 - takao.fujiwara@sun.com
- Added SUNWgnome-dtlogin-integration-01-unset-locale.diff. Fixes 6532300
* Tue Nov 14 2006 - damien.carbery@sun.com
- Bump to 0.29, to change menu string to 2.16. Fixes 6493544.
* Thu Aug 24 2006 - laca@sun.com
- remove autoheader call since there is AC_CONFIG_HEADER in configure.in
* Fri Aug 04 2006 - damien.carbery@sun.com
- Bump to 0.27, to change menu string to 2.15.
* Fri Jun 23 2006 - laca@sun.com
- bump to 0.26, fixes 6340366 "A modified version of
  /usr/dt/config/Xinitrc.jds in /etc/dt/config is not used" and
  moves the code starting ssh-agent here from gdm so that it runs
  for dtlogin users too.
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Thu Apr  6 2006 - brian.cameron@sun.com
- Now use tarball_version
* Wed Feb  1 2006 - damien.carbery@sun.com
- Bump to 0.25 to change menu string to "Gnome 2.14 for OpenSolaris"
* Tue Sep 13 2005 - laca@sun.com
- remove unpackaged files
* Fri Jul  8 2005 - damien.carbery@sun.com
- Add definition for ACLOCAL_FLAGS in order to build.
* Fri Apr  1 2005 - brian.cameron@sun.com
- Update to 0.23.  Remove /usr/openwin/bin from PATH and move it to GDM2
  so it doesn't get set twice when logging in via CDE login.
* Wed Mar 16 2005 - brian.cameron@sun.com
- commented out the rm datadir/locale/*/LC_MESSAGES/dtlogin-integration.mo
  line since it got accidently uncommented in my last putback.
* Tue Mar 01 2005 - brian.cameron@sun.com
- Update to 0.22: Remove /usr/dt/bin from default user PATH.
* Wed Dec 15 2004 - laca@sun.com
- Update to 0.21: get rid of the login popup
* Mon Dec 13 2004 - damien.carbery@sun.com
- Update to 0.20. Implement ARC decision: Remove /usr/demo/jds/bin from PATH 
  and change wording for message about adding /usr/sfw/bin to the PATH 
  (Xinitrc.in).
* Fri Nov 26 2004 - damien.donlon@sun.com
- Added translations for new popup dialog. Asian to be modfied still.
* Fri Nov 26 2004 - laca@sun.com
- update to 0.17: fixes 6182467 (adds sfw login dialog)
- add %_datadir to files
* Fri Oct 29 2004 - laca@sun.com
- uprev to 0.16: adds comment about /usr/sfw/bin to Xinitrc, uses new
  Solaris 10 branding
* Wed Oct 20 2004 - laca@sun.com
- uprev to 0.15 (removes /usr/sfw/bin from the PATH)
* Fri Oct 15 2004 - damien.donlon@sun.com
- Uprevved tarball to 0.14 (0.12 & 0.13 already present)
* Thu Sep 09 2004 - hidetoshi.tajima@sun.com
- Uprevved tarball to 0.11
* Tue Sep 07 2004 - laca@sun.com
- Added SourcePackage tag because SUNWgnome-dtlogin-integration-src is too
  long...
* Tue Sep 07 2004 - takao.fujiwara@sun.com
- Added BuildRequires for effective iconv convertions.
* Tue Sep 07 2004 - laca@sun.com
- Uprevved tarball to 0.10
* Mon Sep 06 2004 - takao.fujiwara@sun.com
- Upstreamed dtlogin-integration-01-g11n-i18n-ui.diff
* Fri Sep 03 2004 - takao.fujiwara@sun.com
- Added dtlogin-integration-01-g11n-i18n-ui.diff
- Updated BuildRequires
* Mon Aug 30 2004 - damien.donlon@sun.com
- Uprevved tarball to 0.9 to fix bugid 5093158
* Thu Jul 08 2004 - damien.carbery@sun.com
- Update to version 0.7 to add /usr/sfw/bin to PATH and /usr/lib/jds-private to
  LD_LIBRARY_PATH.
* Tue Jun 22 2004 - damien.donlon@sun.com
- update to version 0.6 to fix th_TH attrib issue (again!)
* Mon Jun 21 2004 - laca@sun.com
- update to version 0.5
* Tue Jun 15 2004 - hidetoshi.tajima@sun.com
- update to version 0.4
- removed dtlogin-integration-01-th_TH_file_conflict.diff and
  include the same fix to the module.
* Thu Jun 10 2004 - damien.donlon@sun.com
- Patch dtlogin-integration-01-th_TH_file_conflict.diff to fix th_TH conflict
* Tue May 18 2004 - laca@sun.com
- update to version 0.3
* Tue May 18 2004 - laca@sun.com
- update to version 0.2
* Tue May 04 2004 - laca@sun.com
- initial version of the spec file
