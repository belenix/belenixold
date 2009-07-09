#
# spec file for package SUNWtgnome-tsoljdslabel
#
# includes module(s): tsoljdslabel
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: stephen

# NOTE: If the version is bumped the new tarball must be uploaded to the
#       Sun Download Center. Contact GNOME RE for assistance.
%define tsoljdslabel_version 0.6.4

%include Solaris.inc

Name:                    SUNWtgnome-tsoljdslabel
Summary:                 GNOME Trusted Extensions Session Label Selector
Version:                 %{default_pkg_version}
Source:			 http://dlc.sun.com/osol/jds/downloads/extras/tjds/tsoljdslabel-%{tsoljdslabel_version}.tar.bz2
%if %build_l10n
Source1:                 l10n-configure.sh
%endif
Patch1:			 SUNWtgnome-tsoljdslabel-01-dbus-launch.diff
# owner:fujiwara date:2009-02-13 type:branding state:upstream
Patch2:			 SUNWtgnome-tsoljdslabel-02-xinitrc-migration.diff
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires: SUNWtgnome-tsol-libs-devel
BuildRequires: SUNWgnome-component-devel
BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-vfs-devel
Requires: SUNWtgnome-tsol-libs
Requires: SUNWgnome-component
Requires: SUNWgnome-config
Requires: SUNWgnome-libs
Requires: SUNWgnome-vfs
#Requires: SUNWgnome-display-mgr

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n tsoljdslabel-%{tsoljdslabel_version}
%patch1 -p1
#%patch2 -p1 # continue to use dtstart to launch trusted sessions for now

%build
export ACLOCAL_FLAGS="-I /usr/share/aclocal"

libtoolize -f
intltoolize --copy --force --automake

%if %build_l10n
bash -x %SOURCE1 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS
autoconf
autoheader
automake -acf

./configure --with-gnome-prefix=%{_prefix} \
            --prefix=%{_prefix} \
	    --sysconfdir=%{_sysconfdir} \
	    --mandir=%{_mandir}

%install
make install DESTDIR=$RPM_BUILD_ROOT
LANG_LIST='
ar ar_EG.UTF-8
cs_CZ.ISO8859-2
da_DK.ISO8859-15
de.UTF-8 de
el_GR.ISO8859-7
en_GB.ISO8859-15 en_IE.ISO8859-15 en_US.ISO8859-15 en_US.UTF-8
es.UTF-8 es
et_EE.ISO8859-15
fi_FI.ISO8859-15
fr.UTF-8 fr
he he_IL.UTF-8
hi_IN.UTF-8
hr_HR.ISO8859-2
hu hu_HU.ISO8859-2
it.UTF-8 it
ja ja_JP.PCK ja_JP.UTF-8 ja_JP.eucJP
ko.UTF-8 ko
nl_BE.ISO8859-15 nl_NL.ISO8859-15
pl_PL.ISO8859-2 pl_PL.UTF-8
pt_BR.UTF-8 pt_BR pt_PT.ISO8859-15
ru_RU.ISO8859-5 ru_RU.UTF-8
sv.UTF-8 sv 
th_TH.ISO8859-11 th_TH.TIS620 th_TH.UTF-8 th_TH
tr_TR.ISO8859-9
zh.GBK zh.UTF-8 zh zh_HK.BIG5HK zh_TW.BIG5 zh_TW.UTF-8 zh_TW
'

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, other)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/tsoljdslabel
%{_bindir}/tsoljdslabel-ui
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_datadir}/xsessions
%dir %attr(0755, root, bin) %{_datadir}/xsessions/multilabel
%{_datadir}/xsessions/multilabel/tgnome.desktop
%dir %attr (0755, root, bin) %{_prefix}/dt
%dir %attr (0755, root, bin) %{_prefix}/dt/config
%{_prefix}/dt/config/Xsession.tjds
%{_prefix}/dt/config/Xsession2.tjds
%{_prefix}/dt/config/Xinitrc.tjds

%if %build_l10n
%files l10n
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/locale
%endif

%changelog
* Fri Feb 13 2009 - takao.fujiwara@sun.com
- Add patch xinitrc-migration.diff. Now gnome-session is invoked directly and
  enviroment values are loaded in /etc/X11/xinit/xinitrc.d instead of /usr/dt.
- Remove --with-dtstart option.
* Fri Sep 19 2008 - ghee.teo@sun.com
- Updated 01-dbus-launch.diff to make it more robust fix bugster:6750408.
* Fri Aug 29 2008 - dave.lin@sun.com
- Remove l10n files if --with-l10n isn't specified.
- Don't define %{_datadir}/locale if --with-l10n isn't specified.
* Fri Aug 22 2008 - stephen.browne@sun.com
- Uprev version, remove upstream patches, add --with-dtstart for opensolairs

* Mon Jul 21 2008 - jeff.cai@sun.com
- Not start ssh-agent since gnome-keyring provides this feature.

* Thu Jul 10 2008 - damien.carbery@sun.com
- Add 01-gtk-disable-deprecated to get module to build with new gtk+ tarball.

* Fri May 16 2008 - stephen.browne@sun.com
- Uprev version, remove upstream patch, remove conditional build, remove tcde

* Thu May 08 2008 - takao.fujiwara@sun.com
- Add SUNWtgnome-tsoljdslabel-01-po.diff for cs.po
  Contributed l10n from Hana Zalska <Hana.Zalska@sun.com>

* Tue Mar 25 2008 - takao.fujiwara@sun.com
- remove upstreamed scripts.

* Fri Mar 14 2008 - stephen.browne@sun.com
- add new GDM files update version and point a tarball on dlc.sun.com

* Thu Sep 19 2007 - stephen.browne@sun.com
- dont install dtlogin and gdm configuration

* Mon Nov 06 2006 - stephen.browne@sun.com
- removed tsoljdslabel-helper binary

* Fri Sep 15 2006 - takao.fujiwara@sun.com
- Add *-10n package.

* Sun Jul 30 2006 - damien.carbery@sun.com
- Always use nightly tarballs as source.

* Wed Jul 19 2006 - damien.carbery@sun.com
- Update Build/BuildRequires after check-deps.pl run.

* Thu Jul 13 2006 - damien.carbery@sun.com
- Add %{_datadir}/locale to %files, a byproduct of intltool up-rev.

* Tue Jul 11 2006 - damien.carbery@sun.com
- Add autogen.sh commands to %prep to permit building from 'cvs co' tarballs.

* Fri Jun 30 2006 - stephen.browne@sun.com
- Changed version to default for vermillion port

* Mon Jun 26 2006 - takao.fujiwara@sun.com
- Added locale dirs for /usr/dt/config/*/Xresources.d/Xtsolresources.jds
  Fixes 6439171

* Wed May 24 2006 - stephen.browne@sun.com
- remove man page from files and shorten summary

* Wed Mar 22 2006 - damien.carbery@sun.com
- Fix dir permissions after last commit.

* Sat Mar 18 2006 - damien.carbery@sun.com
- Fix dir permissions after last commit.

* Thu Mar 16 2006 - ghee.teo@sun.com
- Changed installation location for startup up config scripts from /etc to /usr
  as requested by ARC as a TCR.

* Wed Mar  8 2006 - damien.carbery@sun.com
- Add %dir %attr for %{_datadir} as %defattr is wrong for this dir.

* Tue Nov 22 2005 - <stephen.browne@sun.com>
- added root package and moved dtlogin integration to /etc/dt

* Tue Oct 04 2005 - <stephen.browne@sun.com>
- added dtlogin session configuration

* Thu Aug 25 2005 - <stephen.browne@sun.com>
- created 
