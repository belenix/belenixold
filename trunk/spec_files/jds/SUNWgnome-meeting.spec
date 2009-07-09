#
# spec file for package SUNWgnome-meeting
#
# includes module(s): ptlib, opal, ekiga
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: elaine
#
# DO NOT REMOVE NEXT LINE
# PACKAGE NOT INCLUDED IN GNOME UMBRELLA ARC
#
%include Solaris.inc

%include base.inc
%define ekiga_libdir %{_libdir}/ekiga
%use ptlib = ptlib.spec
%use opal = opal.spec

%define ptlib_dir %{_builddir}/SUNWgnome-meeting-%{default_pkg_version}/%base_arch/ptlib-%{ptlib.version}
%define ptlib_opt --with-ptlib-dir=%{ptlib_dir}
%define opal_opt --with-opal-dir=%{_builddir}/SUNWgnome-meeting-%{default_pkg_version}/%base_arch/opal-%{opal.version}

%use ekiga = ekiga.spec

Name:          SUNWgnome-meeting
Summary:       GNOME video conference application
Version:       %{default_pkg_version}
Source:        %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:  %{_basedir}
SUNW_Copyright:%{name}.copyright
BuildRoot:     %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:      SUNWlibC
Requires:      SUNWlxml
Requires:      SUNWlibms
Requires:      SUNWlibmsr
Requires:      SUNWgnome-base-libs
Requires:      SUNWgnome-libs
Requires:      SUNWgnome-component
Requires:      SUNWgnutls
Requires:      SUNWgnome-config
Requires:      SUNWgnome-meeting-root
Requires:      SUNWdesktop-cache
Requires:      SUNWevolution-data-server
Requires:      SUNWgnome-audio
Requires:      SUNWavahi-bridge-dsd
Requires:      SUNWdbus
Requires:      SUNWsigcpp
Requires:      SFEsdl
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWgnome-doc-utils
BuildRequires: SUNWdbus-devel
BuildRequires: SUNWlxml-python
BuildRequires: SUNWavahi-bridge-dsd-devel
BuildRequires: SFEsdl-devel

%package root
Summary:                %{summary} - / filesystem
SUNW_BaseDir:           /
%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                %{summary} - l10n files
SUNW_BaseDir:           %{_basedir}
%include default-depend.inc
Requires:               %{name}
%endif

%prep
rm -rf %name-%version
mkdir %name-%version

mkdir %name-%version/%base_arch
%ptlib.prep -d %name-%version/%base_arch
%opal.prep -d %name-%version/%base_arch
%ekiga.prep -d %name-%version/%base_arch
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build
%if %cc_is_gcc
%else

# to fix performace CR#6401342 on sparc
%ifarch sparc
export EXTRA_CXXFLAGS="-features=tmplife -xO5 -xF=lcldata,gbldata -Qoption postopt -dataredundancy=on,-tune:optimizer:data-alignment=4 -xbuiltin=%%all"
%else
export EXTRA_CXXFLAGS="-features=tmplife -xbuiltin=%%all"
%endif

%endif

%if %cc_is_gcc
%else
export CXX="${CXX} -norunpath"
%endif

#export PWLIBDIR=`pwd`/%name-%version/%base_arch/pwlib-%{pwlib.version}
export PKG_CONFIG_PATH=%{_builddir}/%name-%version/%base_arch/ptlib-%{ptlib.version}:%{_builddir}/%name-%version/%base_arch/opal-%{opal.version}:%{_pkg_config_path}
%ptlib.build -d %name-%version/%base_arch
%opal.build -d %name-%version/%base_arch
%ekiga.build -d %name-%version/%base_arch

%install
rm -rf $RPM_BUILD_ROOT

%ptlib.install -d %name-%version/%base_arch
%opal.install -d %name-%version/%base_arch
%ekiga.install -d %name-%version/%base_arch
rm -rf $RPM_BUILD_ROOT%{_libdir}/%{ekiga.name}/pkgconfig
rm -f  $RPM_BUILD_ROOT%{_libdir}/%{ekiga.name}/lib*a

%if %can_isaexec
mkdir $RPM_BUILD_ROOT%{_bindir}/%{base_isa}
mv $RPM_BUILD_ROOT%{_bindir}/ekiga $RPM_BUILD_ROOT%{_bindir}/%{base_isa}
cd $RPM_BUILD_ROOT%{_bindir}
ln -s ../lib/isaexec ekiga
%endif

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/%{ekiga.name}/[a-z]*
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/%{ekiga.name}/%{ekiga.name}-[a-z]*.omf
%endif

# install man page
rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri desktop-mime-cache icon-cache gconf-cache

%postun
%restart_fmri desktop-mime-cache

%files
%doc(bzip2) -d %{base_arch} ptlib-%{ptlib.version}/mpl-1.0.htm 
%doc(bzip2) -d %{base_arch} ptlib-%{ptlib.version}/History.txt 
%doc(bzip2) -d %{base_arch} ptlib-%{ptlib.version}/ReadMe.txt
%doc(bzip2) -d %{base_arch} ptlib-%{ptlib.version}/ChangeLog-ptlib-v2_0_2.txt
%doc(bzip2) -d %{base_arch} ptlib-%{ptlib.version}/ChangeLog-ptlib-v2_1_2.txt
%doc(bzip2) -d %{base_arch} ptlib-%{ptlib.version}/ChangeLog-ptlib-v2_1_3.txt
%doc(bzip2) -d %{base_arch} ptlib-%{ptlib.version}/ChangeLog-ptlib-v2_2_0.txt
%doc(bzip2) -d %{base_arch} ptlib-%{ptlib.version}/ChangeLog-ptlib-v2_2_1.txt
%doc(bzip2) -d %{base_arch} ptlib-%{ptlib.version}/ChangeLog-ptlib-v2_2_2.txt
%doc(bzip2) -d %{base_arch} ptlib-%{ptlib.version}/ChangeLog-ptlib-v2_3_0.txt
%doc(bzip2) -d %{base_arch} ptlib-%{ptlib.version}/ChangeLog-ptlib-v2_3_1.txt
%doc(bzip2) -d %{base_arch} ptlib-%{ptlib.version}/ChangeLog-ptlib-v2_4_0.txt
%doc(bzip2) -d %{base_arch} ptlib-%{ptlib.version}/ChangeLog-ptlib-v2_4_1.txt
%doc(bzip2) -d %{base_arch} opal-%{opal.version}/mpl-1.0.htm
%doc(bzip2) -d %{base_arch} opal-%{opal.version}/ChangeLog-opal-v3_0_2.txt
%doc(bzip2) -d %{base_arch} opal-%{opal.version}/ChangeLog-opal-v3_1_2.txt
%doc(bzip2) -d %{base_arch} opal-%{opal.version}/ChangeLog-opal-v3_2_0.txt
%doc(bzip2) -d %{base_arch} opal-%{opal.version}/ChangeLog-opal-v3_2_1.txt
%doc(bzip2) -d %{base_arch} opal-%{opal.version}/ChangeLog-opal-v3_2_2.txt
%doc(bzip2) -d %{base_arch} opal-%{opal.version}/ChangeLog-opal-v3_3_0.txt
%doc(bzip2) -d %{base_arch} opal-%{opal.version}/ChangeLog-opal-v3_3_1.txt
%doc(bzip2) -d %{base_arch} opal-%{opal.version}/ChangeLog-opal-v3_4_0.txt
%doc(bzip2) -d %{base_arch} opal-%{opal.version}/ChangeLog-opal-v3_4_1.txt
%doc(bzip2) -d %{base_arch} ekiga-%{ekiga.version}/COPYING 
%doc -d %{base_arch} ekiga-%{ekiga.version}/AUTHORS 
%doc(bzip2) -d %{base_arch} ekiga-%{ekiga.version}/NEWS
%doc(bzip2) -d %{base_arch} ekiga-%{ekiga.version}/ChangeLog
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%hard %{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/%{ekiga.name}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%{_datadir}/sounds
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/%{ekiga.name}/C
%{_datadir}/omf/%{ekiga.name}/%{ekiga.name}-C.omf
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/16x16
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/16x16/apps/
%{_datadir}/icons/hicolor/16x16/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/22x22/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/22x22/apps/
%{_datadir}/icons/hicolor/22x22/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/32x32/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/32x32/apps/
%{_datadir}/icons/hicolor/32x32/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48/apps/
%{_datadir}/icons/hicolor/48x48/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/64x64/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/64x64/apps/
%{_datadir}/icons/hicolor/64x64/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/72x72/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/72x72/apps/
%{_datadir}/icons/hicolor/72x72/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/128x128/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/128x128/apps/
%{_datadir}/icons/hicolor/128x128/apps/*
%{_datadir}/dbus-1/*/*

%files root
%defattr (-, root, sys)
%dir %attr(0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/ekiga.schemas

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/gnome
%attr (-, root, other) %{_datadir}/locale
%{_datadir}/gnome/help/%{ekiga.name}/[a-z]*
%{_datadir}/omf/%{ekiga.name}/*-[a-z]*.omf
%endif

%changelog
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Mon Feb 23 2009 - elaine.xiong@sunc.om
- Remove SSE2 support to fix bugster#6808201. Because there is no 
  significant performance impact brought by SSE2 support since 3.0.
  Furthermore it is inappropriate to put SSE2 binaries in pentium+mmx.
* Fri Nov 14 2008 - elaine.xiong@sun.com
- Update copyright entries.
* Fri Nov 14 2008 - elaine.xiong@sun.com
- bump to Ekiga 3.0. 
- change some build options to fit new version.
- rename pwlib component to ptlib.
* Fri Nov 14 2008 - elaine.xiong@sun.com
- remove -xlinkopt option that causes error in SS12. 
* Tue Sep 16 2008 - elaine.xiong@sun.com
- Add %doc to %files for new copyright.
* Thu Mar 27 2008 - elaine.xiong@sun.com
- Add file SUNWgnome-meeting.copyright.
* Thu Jan  3 2008 - laca@sun.com
- use gconf-install.script instead of an inline script
* Wed Nov 14 2007 - damien.carbery@sun.com
- Add Build/Requires SUNWavahi-bridge-dsd/-devel as required by ekiga.
* Thu Oct 11 2007 - damien.carbery@sun.com
- Remove install dependency on SUNWgnome-doc-utils and change the build
  dependency from SUNWgnome-doc-utils-devel to SUNWgnome-doc-utils.
* Fri Sep 28 2007 - laca@sun.com
- delete SUNWxw* deps -- this pkg already depends on SUNWgnome-base-libs
* Thu Sep 13 2007 - elaine.xiong@sun.com
- Add SGML format man page.
* Thu Aug 30 2007 - elaine.xiong@sun.com
- simply cancel my last checkin about DBUS.
* Thu Jun 28 2007 - elaine.xiong@sun.com
- pack the DBUS service files to pkg since DBUS enabled.
* Thu Apr 26 2007 - laca@sun.com
- set CXX to $CXX -norunpath because libtool swallows this option sometimes
  and leaves compiler paths in the binaries, fixes 6497744
* Sat Apr  7 2007 - elaine.xiong@sun.com
- correct if/else statement related to EXTRA_CXXFLAGS. 
* Thu Apr  5 2007 - laca@sun.com
- explode ekiga.spec into individual spec files for each component and
  add SSE2 optimized versions
* Tue Mar 13 2007 - elaine.xiong@sun.com
- cancel part of last checking to make sure each env var change is solid and
  worthful.  
* Sun Mar 11 2007 - elaine.xiong@sun.com
- add some optimization options to get more optimized binary
* Mon Nov 20 2006 - dave.lin@sun.com
- add patch comment
* Thu Otc 26 2006 - dave.lin@sun.com
- Move patch ekiga-06-opal-jitter.diff, ekiga-07-conststr.diff from
  spec-files/Solaris/patches to spec-files/patches, rename the patch
  to solve the patch number conflict there(the new name are 
  ekiga-11-opal-jitter.diff, ekiga-12-conststr.diff) 
* Thu Sep 07 2006 - damien.carbery@sun.com
- Remove upstream patch, ekiga-08-pwlib-audiodev.diff.
* Mon Aug 28 2006 - dave.lin@sun.com
- add patch ekiga-08-pwlib-audiodev.diff to fix the bug CR#6462870
* Fri Jul 14 2006 - laca@sun.com
- update %post/%postun/etc scripts to support diskless client setup,
  part of 6448317
* Mon Jul 10 2006 - dave.lin@sun.com
- change to use Ekiga 2.0.2 release
- add patch ekiga-08-pwlib-audiodev.diff to get Ekiga worked on SunRay 
* Thu Jun 29 2006 - laca@sun.com
- update postrun scripts
* Fri Jun 16 2006 - dave.lin@sun.com
- fix the libraries missed problem
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Mon Jun 01 2006 - dave.lin@sun.com
- add BuildRequires SUNWlxml-python
- comment out Build/Requires SUNWdbus,SUNWdbus-devel since dbus's removed from
  the build temporarily.
* Sat Jun  3 2006 - laca@sun.com
- use post/preun scripts to install schemas into the merged gconf files
* Fri Jun 02 2006 - damien.carbery@sun.com
- Add Build/Requires SUNWgnome-doc-utils/-devel otherwise build fails.
* Fri May 26 2006 - dave.lin@sun.com
- add "-features=tmplife" in CXXFLAGS to fix hang problem
* Mon May 15 2006 - dave.lin@sun.com
- add patch ekiga-05-pwlib-jitter.diff, ekiga-06-opal-jitter.diff
  to fix CR#6416969, add patch ekiga-07-conststr.diff to
  fix bug CR#6401342 on i386, and to fix this bug on sparc, add options in
  CFLAGS, CXXFLAGS
* Fri Apr 14 2006 - dave.lin@sun.com
- delete SUNW_Category tag to use the general one 
- change all reference of "gnomemeeting" to "ekiga" 
* Fri Mar 31 2006 - dave.lin@sun.com
- initial version created
