#
# Copyright (c) Sun Microsystems, Inc.
#
# Owner: davelam
# bugdb: bugzilla.mozilla.org
#
#####################################
##   Package Information Section   ##
#####################################

Name:        firefox
Summary:     Mozilla Firefox Web browser
Version:     3.1
%define tarball_version 3.1b3
Release:     1
Copyright:   MPL/LGPL
Group:       Applications/Internet
Distribution:Java Desktop System
Vendor:      Sun Microsystems, Inc.
Source:      http://ftp.mozilla.org/pub/mozilla.org/%{name}/releases/%{tarball_version}/source/%{name}-%{tarball_version}-source.tar.bz2
Source1:     firefox-icon.png
Source2:     firefox.desktop
Source3:     firefox-preload.list.in
Source4:     %{name}.cfg
Source5:     %{name}-xpcom.pc.in
Source6:     %{name}-plugin.pc.in
Source7:     %{name}-js.pc.in
%define without_moz_nss_nspr %{?_without_moz_nss_nspr:1}%{?!_without_moz_nss_nspr:0}
%define with_apoc_adapter %{?_with_apoc_adapter:1}%{?!_with_apoc_adapter:0}

# owner:evan date:2007-11-28 type:branding
# change preference to support multi-language
Patch1: firefox3-01-locale.diff

# owner:davelam date:2006-02-24 type:branding
# enable firefox preload mechanism
Patch2: firefox3-02-preload.diff

# owner:hawklu date:2007-04-27 type:branding
# bugster:6542910
Patch3: firefox3-03-disable-online-update.diff

# owner:ginnchen date:2009-03-04 type:bug bugzilla:448512
Patch4: firefox3-04-xinerama.diff

# owner:fujiwara date:2008-04-10 type:bug
# bugster:6686579 bugzilla:285267
Patch5: firefox3-05-g11n-nav-lang.diff

# owner:ginnchen date:2008-08-19 type:bug
# bugster:6724471 bugzilla:451007
Patch6: firefox3-06-donot-delay-stopping-realplayer.diff

# owner:ginnchen date:2008-09-19 type:bug bugzilla:442231
Patch7: firefox3-07-spellchecker-default.diff

# owner:alfred date:2008-10-10 type:bug bugster:6750518
Patch8: firefox3-08-ksh.diff

# owner:ginnchen date:2008-10-15 type:branding
# bugzilla:457196
Patch9: firefox3-09-jemalloc-shared-library.diff

# owner:ginnchen date:2008-11-27 type:bug bugzilla:464443
Patch10: firefox3-10-fix-mimetype-for-helper-app.diff

# owner:ginnchen date:2009-03-04 type:bug bugzilla:472635 status:upstream
Patch11: firefox3-11-im-context-not-match.diff

# owner:hawklu date:2008-12-04 type:bug bugzilla:463987 status:upstream
Patch12: firefox3-12-js.diff

# owner:hawklu date:2008-12-12 type:bug bugzilla:468041 status:upstream
Patch13: firefox3-13-js-dtrace.diff

# owner:ginnchen date:2009-03-04 type:branding bugzilla:478390 bugster:6805829
Patch14: firefox3-14-compiler-workaround.diff

# owner:hawklu date:2008-12-10 type:bug bugzilla:449754 status:upstream
Patch15: firefox3-15-libogg-liboggz.diff

# owner:ginnchen date:2009-03-04 type:bug bugzilla:471642 status:upstream
Patch16: firefox3-16-rename-nsSelectionBatcher.diff

# owner:ginnchen date:2009-03-04 type:bug bugzilla:479022 status:upstream
Patch17: firefox3-17-bigendian.diff

# owner:ginnchen date:2008-12-16 type:bug bugzilla:474758 status:upstream
Patch18: firefox3-18-font-config.diff

# owner:hawklu date:2008-12-16 type:branding
Patch19: firefox3-19-xpcom-glue-no-hidden.diff

# owner:hawklu date:2008-04-20 type:branding bugster:664645
Patch20: firefox3-20-gen-devel-files.diff

# owner:ginnchen date:2009-03-04 type:bug bugzilla:472269 status:upstream
Patch21: firefox3-21-runmozilla.diff

# owner:alfred date:2009-03-31 type:bug bugzilla:484320,485217,485286 status:upstream
# security fixes released in Firefox 3.0.8
Patch22: firefox3-22-308-security-fixes.diff

# owner:ginnchen date:2009-03-20 type:bug bugzilla:468727 status:upstream
Patch26 : firefox3-26-bug468727.diff

# owner:ginnchen date:2009-03-30 type:bug bugzilla:484932 status:upstream
Patch27 : firefox3-27-bug484932.diff

# owner:ginnchen date:2009-03-30 type:branding
# disable sessionstore for form by default
Patch28 : firefox3-28-ss-privacy-level.diff

%if %option_with_indiana_branding
# owner:alfred date:2009-03-02 type:branding
Patch29 : firefox3-29-getting-started.diff
%endif

Patch30 : firefox3-pango-bug478871-patch.diff

Patch31 : firefox3-perf-tweaks.diff

URL:         http://www.mozilla.com/firefox

BuildRoot:   %{_tmppath}/%{name}-%{tarball_version}-build
Prefix:      /usr
Provides:    webclient
Autoreqprov: on

#####################################
##     Package Defines Section     ##
#####################################

%define _unpackaged_files_terminate_build 0
%define _ffdir %{_libdir}/%{name}
%if %without_moz_nss_nspr
%define nss_nspr_dir %{_libdir}/mps
%else
%define nss_nspr_dir %{_libdir}/%{name}
%endif

#####################################
##  Package Requirements Section   ##
#####################################

BuildRequires: libjpeg
BuildRequires: zip
BuildRequires: perl
BuildRequires: autoconf
BuildRequires: libIDL-devel
BuildRequires: glib2-devel
BuildRequires: gtk2-devel
Prereq: fileutils perl
Prereq: /usr/bin/killall

#####################################
##   Package Description Section   ##
#####################################

%description
Mozilla Firefox is an open-source web browser, designed for standards
compliance, performance and portability.

#####################################
##   Package Preparation Section   ##
#####################################

%prep

%setup -q -c -n %{name}

cd ..
/bin/mv %{name} %{name}.tmp.$$
/bin/mv %{name}.tmp.$$/mozilla* %{name}
rm -rf %{name}.tmp.$$
cd %{name}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch26 -p1
%patch27 -p1
%patch28 -p1
%if %option_with_indiana_branding
%patch29 -p1
%endif
%patch30 -p1
%patch31 -p1

#####################################
##      Package Build Section      ##
#####################################

%build
%ifos linux
if [ -x /usr/bin/getconf ]; then
  CPUS=`getconf _NPROCESSORS_ONLN`
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

cat << "EOF" > .mozconfig
mk_add_options MOZ_OBJDIR=@TOPSRCDIR@/../obj
. $topsrcdir/browser/config/mozconfig
mk_add_options BUILD_OFFICIAL=1
mk_add_options MOZILLA_OFFICIAL=1
ac_add_options --prefix=%{_prefix}
ac_add_options --libdir=%{_libdir}
ac_add_options --mandir=%{_mandir} 
%if %option_with_debug
ac_add_options --enable-debug
ac_add_options --enable-libxul
ac_add_options --disable-optimize
%endif
ac_add_options --enable-official-branding
ac_add_options --disable-updater
ac_add_options --disable-tests
ac_add_options --enable-dtrace
ac_add_options --with-system-jpeg
ac_add_options --enable-system-cairo
ac_add_options --disable-crashreporter
EOF

%if %with_apoc_adapter
echo "ac_add_options --enable-extensions=default,apoc" >> .mozconfig
%endif

BUILD_OFFICIAL=1 
MOZILLA_OFFICIAL=1
MOZ_PKG_FORMAT=BZ2
PKG_SKIP_STRIP=1
export BUILD_OFFICIAL MOZILLA_OFFICIAL MOZ_PKG_FORMAT PKG_SKIP_STRIP CFLAGS CXXFLAGS

#Build in a separated directory
SRCDIR=$PWD
export MOZCONFIG=$PWD/.mozconfig
mkdir -p ../obj
cd ../obj

${SRCDIR}/configure
make

# install firefox.cfg (make debugging easier in obj/dist/bin)
cp %{SOURCE4} dist/bin/firefox.cfg

cd browser/installer
make

%install
/bin/rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/%{name}
mkdir -p $RPM_BUILD_ROOT%{_includedir}/%{name}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/idl/%{name}
mkdir -p $RPM_BUILD_ROOT/tmp

LIBDIR=$RPM_BUILD_ROOT%{_libdir}/%{name}
INCLUDEDIR=$RPM_BUILD_ROOT%{_includedir}/%{name}
IDLDIR=$RPM_BUILD_ROOT%{_datadir}/idl/%{name}

BUILDDIR=$PWD/../obj
cd $RPM_BUILD_ROOT/tmp
bzip2 -dc $BUILDDIR/dist/firefox-*.sdk.tar.bz2 | tar -xf -

cd firefox*
mv bin/*  ${LIBDIR}
mv sdk/bin/xpidl  ${LIBDIR}
mv sdk/bin/xpt_link  ${LIBDIR}
mv sdk/bin/xpt_dump  ${LIBDIR}
echo `date` > ${LIBDIR}/.autoreg

mv include/* ${INCLUDEDIR}
mv idl/* ${IDLDIR}

# Fix *.h *.idl attribute issue
find ${INCLUDEDIR} ${IDLDIR} \
  -type f -name "*.h" -o -type f -name "*.idl" | xargs chmod 644

%if %without_moz_nss_nspr
# Don't deliver nss, nspr header files if we use system nss nspr
rm -rf $RPM_BUILD_ROOT/%{_includedir}/%{name}/include/nss
rm -rf $RPM_BUILD_ROOT/%{_includedir}/%{name}/include/nspr
%endif

/bin/mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
/bin/mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps
/bin/mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
install -c -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/pixmaps/firefox-icon.png
install -c -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/applications/firefox.desktop

/bin/ln -s ../lib/firefox/firefox $RPM_BUILD_ROOT%{_bindir}/firefox

# install preloaded library list that would be picked up by gdmprefetch 
/usr/bin/sed -e 's,NSS_NSPR_DIR,%{nss_nspr_dir},g' \
             -e 's,FIREFOX_LIB_DIR,%{_ffdir},g' %{SOURCE3} > \
  $RPM_BUILD_ROOT%{_ffdir}/firefox-preload.list
/bin/chmod 644 $RPM_BUILD_ROOT%{_ffdir}/firefox-preload.list

# install firefox.cfg
install -c -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_ffdir}/firefox.cfg

# install firefox-xpcom.pc
mkdir -p  $RPM_BUILD_ROOT%{_libdir}/pkgconfig

/usr/bin/sed -e "s,BASEDIR,%{_basedir},g" \
             -e "s,LIBDIR,%{_libdir},g" \
             -e "s,DATADIR,%{_datadir},g"\
             -e "s,IDLDIR,%{_datadir}/idl/%{name},g"\
             -e "s,INCLUDEDIR,%{_includedir},g" \
             -e "s,NAME,%{name},g" \
             %{SOURCE5} > $RPM_BUILD_ROOT/tmp/%{name}-xpcom.pc
install -c -m 644 $RPM_BUILD_ROOT/tmp/%{name}-xpcom.pc \
             $RPM_BUILD_ROOT%{_libdir}/pkgconfig/%{name}-xpcom.pc

/usr/bin/sed -e "s,BASEDIR,%{_basedir},g" \
             -e "s,LIBDIR,%{_libdir},g" \
             -e "s,DATADIR,%{_datadir},g"\
             -e "s,INCLUDEDIR,%{_includedir},g" \
             -e "s,NAME,%{name},g" \
             %{SOURCE6} > $RPM_BUILD_ROOT/tmp/%{name}-plugin.pc
install -c -m 644 $RPM_BUILD_ROOT/tmp/%{name}-plugin.pc \
$RPM_BUILD_ROOT%{_libdir}/pkgconfig/%{name}-plugin.pc

/usr/bin/sed -e "s,BASEDIR,%{_basedir},g" \
             -e "s,LIBDIR,%{_libdir},g" \
             -e "s,DATADIR,%{_datadir},g"\
             -e "s,INCLUDEDIR,%{_includedir},g" \
             -e "s,NAME,%{name},g" \
             %{SOURCE7} > $RPM_BUILD_ROOT/tmp/%{name}-js.pc
install -c -m 644 $RPM_BUILD_ROOT/tmp/%{name}-js.pc \
$RPM_BUILD_ROOT%{_libdir}/pkgconfig/%{name}-js.pc

cd $RPM_BUILD_ROOT
/usr/bin/rm -rf $RPM_BUILD_ROOT/tmp

# remove local dictionary and share the one that delivered 
# by myspell-dictionary
rm -rf $RPM_BUILD_ROOT%{_ffdir}/dictionaries

# move the default bookmarks file to a separated package: SUNWfirefox-bookmark
# remove this one
rm -f $RPM_BUILD_ROOT%{_libdir}/firefox/defaults/profile/bookmarks.html

%clean
/bin/rm -rf $RPM_BUILD_ROOT

#########################################
##  Package Post[Un] Install Section   ##
#########################################

%post
# run ldconfig before regxpcom
/sbin/ldconfig >/dev/null 2>/dev/null

%postun
/sbin/ldconfig >/dev/null 2>/dev/null

#####################################
##      Package Files Section      ##
#####################################

%files
%defattr(-,root,root)
%dir %{_ffdir}
%{_ffdir}/*
%{_bindir}/firefox
%{_mandir}/man1/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}-icon.png

%changelog
* Tue Apr 09 2009 - alfred.peng@sun.com
- Add patch firefox3-22-308-security-fixes.diff to include the security
  fixes released in Firefox 3.0.8.
* Tue Mar 31 2009 - ginn.chen@sun.com
- Add patch firefox3-27-bug484932.diff. Fix d.o.o. 7638.
- Add patch firefox3-28-ss-privacy-level.diff. Workaround for d.o.o. 7634.
* Wed Mar 25 2009 - ginn.chen@sun.com
- Add patch firefox3-26-bug468727.diff.
* Tue Mar 10 2009 - ginn.chen@sun.com
- Bump to Firefox 3.1 beta 3.
* Mon Mar 09 2009 - alfred.peng@sun.com
- Add patch for OpenSolaris getting started page.
* Mon Feb 02 2009 - alfred.peng@sun.com
- fit and finish: add default-to-downloads.diff for bugster CR#6735323.
* Fri Dec 19 2008 - dave.lin@sun.com
- Correct version number to digit only(3.1b2 -> 3.1).
* Wed Dec 17 2008 - ginn.chen@sun.com
- clean up and update some patches
* Wed Dec 17 2008 - alfred.peng@sun.com
- correct the name typo of patch36.
* Tue Dec 16 2008 - brian.lu@sun.com
- patches/firefox3-36-font-config.diff
  patches/firefox3-37-xpcom-no-hidden.diff
* Mon Dec 15 2008 - dave.lin@sun.com
- Removed upstreamed patch -24-moz-fix-link-path.diff.
* Mon Dec 15 2008 - brian.lu@sun.com
- patches/firefox3-18-gen-devel-files.diff
  patches/firefox3-21-donot-delay-stopping-realplayer.diff: 
  update patch 
- patches/firefox3-31-js-dtrace.diff: add patch 
- patches/firefox3-32-alloca.diff: add patch 

* Fri Dec 12 2008 - brian.lu@sun.com
- Bump to firefox 3.1b2

  Remove following patches (upstreamed):
  firefox3-19-no-xrender-perf.diff
  firefox3-20-remap-pixman-functions.diff
  firefox3-26-know-your-rights.diff

  Add following patches:
  firefox3-30-js.diff
  firefox3-33-libogg.diff
  firefox3-34-liboggz.diff
  firefox3-35-theora-disable-inline-asm.diff

  Update following patches:
  firefox3-09-remove-core-file-check.diff
  firefox3-29-strip-gtk-module-settings.diff

* Wed Dec 03 2008 - alfred.peng@sun.com
- Move the default bookmarks file to a separated package, CR6777386.
  Remove patches: firefox3-11-getting-started-bookmark.diff and
  firefox3-22-bug-report-bookmark.diff
* Thu Nov 27 2008 - ginn.chen@sun.com
- Add firefox3-28-fix-mimetype-for-helper-app.diff
- Add firefox3-29-strip-gtk-module-settings.diff
* Mon Nov 17 2008 - brian.lu@sun.com
- bump to 3.0.4
* Wed Oct 15 2008 - ginn.chen@sun.com
- Add firefox3-27-jemalloc-interpose-flag.diff.
* Fri Oct 10 2008 - alfred.peng@sun.com
- Add %option_with_indiana_branding for firefox3-25-ksh.diff.
* Fri Oct 10 2008 - alfred.peng@sun.com
- Add firefox3-25-ksh.diff for indiana only to fix bugster CR6750518.
  Add firefox3-26-know-your-rights.diff for the EULA pop-up bugster CR6757178.
  Update firefox3-11-getting-started-bookmark.diff for the default
  bookmarks and toolbar entries on OpenSolaris 2008.11.
* Fri Oct 10 2008 - ginn.chen@sun.com
- enable system cairo: fix for #3586
* Sat Sep 27 2008 - ginn.chen@sun.com
- Bump to 3.0.3.
- Add enable-libxul for debug version.
* Fri Sep 19 2008 - ginn.chen@sun.com
- Add firefox3-23-spellchecker-default.diff
- Add firefox3-24-moz-fix-link-path.diff
* Wed Sep 17 2008 - ginn.chen@sun.com
- Remove firefox3-01-change-install-dir.diff
- Remove firefox3-03-plugins.diff
- Remove firefox3-04-common-tar-option.diff
- Remove firefox3-06-find-opt.diff
- Remove firefox3-11-developer-guide-bookmark.diff
- Put timestamp into .autoreg as a workaround for IPS for now.
* Tue Sep 09 2008 - ginn.chen@sun.com
- Do not remove nss/nspr header files for now.
* Wed Sep 03 2008 - ginn.chen@sun.com
- Fix firefox-preload.list.in and some small tweaks for specfile.
* Tue Sep 02 2008 - brian.lu@sun.com
- Add %if option_with_sun_branding around patch22
* Wed Aug 27 2008 - ginn.chen@sun.com
- Update patch firefox3-20-remap-pixman-functions.diff
* Fri Aug 22 2008 - dave.lin@sun.com
- add patch firefox3-22-bug-report-bookmark.diff 
* Wed Aug 20 2008 - dave.lin@sun.com
- Rename firefox3-preload.list.in to firefox-preload.list.in.
* Tue Aug 19 2008 - ginn.chen@sun.com
- Add firefox3-21-donot-delay-stopping-realplayer.diff
- Update firefox3-20-remap-pixman-functions.diff
- Remove firefox3-16-crash-in-8-bit-mode.diff
- Remove firefox3-07-no-ldlibpath.diff
* Mon Aug 18 2008 - dave.lin@sun.com
- Rename firefox3.spec to firefox.spec since FF2 has been replaced by FF3 in Nevada and OS for several builds
* Mon Aug 18 2008 - dave.lin@sun.com
- Enable debug mode when --with-debug specified
* Mon Jul 21 2008 - dave.lin@sun.com
- Fixed another "-type f" issue of find command, which is similar as below
* Mon Jul 21 2008 - damien.carbery@sun.com
- Add another "-type f" to /usr/bin/find command because Solaris find needs it
  on both sides of -o to only find files.
* Mon Jul 21 2008 - ginn.chen@sun.com
- Add bugdb info.
* Sat Jul 19 2008 - dave.lin@sun.com
- Fixed *.h *.idl 755 attribute issue.
* Thu Jul 17 2008 - brian.lu@sun.com
- bump to 3.0.1 
* Thu Jul 17 2008 - dave.lin@sun.com
- Change the patch firefox3-03-plugins as branding patch
* Fri Jul 11 2008 - brian.lu@sun.com
- Add bugId for the patch firefox3-09-remove-core-file-check.diff
- Remove patch firefox3-16-crash-in-8-bit-mode.diff: upstreamed 
- Add bugId for firefox3-18-gen-devel-files.diff
* Thu Jun 26 2008 - brian.lu@sun.com
- Add patch 
* Fri Jun 20 2008 - dave.lin@sun.com
- Bump to Firefox 3.0 official release
* Thu Jun 12 2008 - ginn.chen@sun.com
- Bump to Firefox 3.0 RC3
- Add with-system-jpeg (bugzilla 437041)
- Add firefox3-19-no-xrender-perf.diff to improve Firefox rendering performance
  when X Render is not available.
- Remove patch10, patch14

* Thu May 29 2008 - damien.carbery@sun.com
- Disable developer guide patch to fix 6700877 as the developer guide is not
  needed for OpenSolaris or SXCE.
* Thu May 22 2008 - dave.lin@sun.com
- change to build as default browser
* Mon Apr 21 2008 - brian.lu@sun.com
- new firefox3 devel package
  remove unnecessary comment
* Mon Apr 14 2008 - brian.lu@sun.com
- bump to beta 5
  remove patch14 which has been fixed in cario trunk (to be fixed in 
  firefox3 final release) but not in firefox3 beta 5
* Thu Apr 10 2008 - takao.fujiwara@sun.com
- Add firefox3-17-g11n-nav-lang.diff to assign locales in
  general.useragent.locale so that JavaScript navigator.language works.
* Thu Feb 28 2008 - brian.lu@sun.com
- Remove the patch firefox3-10-cario-perf.diff 
  which causes a regression CR6668422
* Mon Feb 25 2008 - brian.lu@sun.com
- Fix the bug CR6656460 firefox crash in 8 bit mode
* Wed Feb 20 2008 - dave.lin@sun.com
- Bump to beta3, and removed upstreamed patche firefox3-15-printing-failed.diff
* Wed Jan 24 2008 - brian.lu@sun.com
- patch fixing the bug CR6646478 status:upstream
* Wed Jan 09 2008 - dave.lin@sun.com
- renamed FF 3 spec to *firefox3 to let FF 3 coexist with FF 2
* Wed Jan 09 2008 - brian.lu@sun.com
- the patch is from bugzilla.freedesktop.org (bug 4945) Fixing CR6646456
* Sat Dec 29 2007 - dave.lin@sun.com
- changed to use "make" instead of "make export" and "make libs"
* Thu Dec 27 2007 - dave.lin@sun.com
- move to 3.0 beta2
- set not building apoc adapter as default
* Mon Dec 03 2007 - dave.lin@sun.com
- bump to 2.0.0.11 for several regressions in 2.0.0.10
* Fir Nov 28 2007 - evan.yan@sun.com
- replace firefox-06-locale.diff with mozilla-09-locale.diff, to correct our way
  of supporting multi-language
* Thu Nov 27 2007 - dave.lin@sun.com
- bump to 2.0.0.10 for several security bug fixes
* Fri Nov 11 2007 - brian.lu@sun.com
- Add firefox-15-remove-core-file-check.diff patch to remove core file checking
  code in run-mozilla.sh. Fixes CR6589754.
* Fri Nov 02 2007 - dave.lin@sun.com
- bump to 2.0.0.9 to fix several regressions in previous release
* Mon Oct 22 2007 - dave.lin@sun.com
- bump to 2.0.0.8
* Sat Oct 20 2007 - laca@sun.com
- add indiana branding patch
* Fri Sep 28 2007 - laca@sun.com
- do not add developer guide bookmark when sun branding is not requested
* Wed Sep 19 2007 - dave.lin@sun.com
- bump to 2.0.0.7
* Fri Aug 03 2007 - dave.lin@sun.com
- bump to 2.0.0.6
* Mon Jul 23 2007 - dave.lin@sun.com
- bump to 2.0.0.5 and remove patch firefox-15-infinite-recursion.diff which
  has been upstreamed in that release
* Thu Jun 21 2007 - damien.carbery@sun.com
- Add patch, mozilla-08-cairo-update.diff, to update the private copy of
  cairo.h used in the build.
* Thu May 31 2007 - dave.lin@sun.com
- bump to 2.0.0.4
* Fri May 18 2007 - brian.lu@sun.com
- Firefox dumps core due to infinite recursion 
* Mon Apr 30 2007 - dave.lin@sun.com
- remove local dictionary and use the one delivered by myspell-dictionary(CR6218511)
* Thu Apr 27 2007 - brian.lu@sun.com
- add patch to grey out "Check for Updates" in Firefox menu since it's not supported
* Thu Apr 12 2007 - dave.lin@sun.com
- disable update feature in Firefox menu since it's not supported
  on Solaris so far(CR#6542910)
* Wed Apri 10 2007 - brian.lu@sun.com
- change the comments of Patch15 from type:upstream to type:bug state:upstream 
* Wed Apri 04 2007 - brian.lu@sun.com
- # bugster: CR6331694 partly fixed, the patch has been upstreamed
* Wed Mar 21 2007 - dave.lin@sun.com
- bump to 2.0.0.3
* Tue Mar 20 2007 - dave.lin@sun.com
- fix bug CR#6521792
    part1: add file ".autoreg" and add postinstall/postremove scripts in
           SUNWfirefox-apoc-adapter
    part2: add patch firefox-12-regenerate-compreg-file.diff
* Sat Mar 03 2007 - dave.lin@sun.com
- removed patch firefox-12-bookmark-drag-and-drop.diff which has been
  upstreamed in 2.0.0.2
* Mon Feb 26 2007 - dave.lin@sun.com
- bump version to 2.0.0.2
* Mon Feb 12 2007 - damien.carbery@sun.com
- Add patch, 02-xpcom-mps.diff, to add '-I/usr/include/mps' to firefox-xpcom.pc
  to allow totem to find prtypes.h (as nscore.h includes this).
* Mon Feb 05 2007 - brian.lu@sun.com
- fix bug CR6519241:bookmark drag and drop crash firefox
- bugzilla id 367203. The patch has been put into upstream
* Fri Jan 26 2007 - dave.lin@sun.com
- enable xinerama support to fix bug CR6507236
* Thu Jan 18 2007 - damien.carbery@sun.com
- Fix 'patch7 -p0' - change to -p1 and change patch file too.
* Wed Jan 17 2007 - damien.carbery@sun.com
- Remove unneeded patch, firefox-02-font_Xft.diff.
* Fri Jan 05 2007 - dave.lin@sun.com
- remove firefox-rebuild-databases and %preun since it's unnecessary for
  Firefox 2.0
* Thu Dec 28 2006 - dave.lin@sun.com
- change the patch type to branding for some patches in patch comments
- bump version to 2.0.0.1
* Thu Dec 07 2006 - brian.lu@sun.com
- Add "solaris developer guide" to bookmark and default home page etc 
* Wed Nov 29 2006 - damien.carbery@sun.com
- Correct path to sparcv8plus dir. Enclose code within '%ifarch sparc'.
* Tue Nov 28 2006 - dave.lin@sun.com
- add %if %with_apoc_adapter to conditinoally disable building apoc
  adapter, default: build apoc adapter, use 
  --without-apoc-adapter to disable it
- remove empty firefox/cpu/sparcv8plus and firefox/cpu
* Mon Nov 27 2006 - dave.lin@sun.com
- enable apoc adapter(CR#6478680)
- move manpage related part in "%ifos linux" since SUNWfirefox.spec
  would cover that on Solaris
* Fri Nov 17 2006 - dave.lin@sun.com
- add patch comments
* Wed Oct 25 2006 - dave.lin@sun.com
- bump verion to 2.0(official release)
* Fri Oct 20 2006 - dave.lin@sun.com
- bump version to 2.0rc3
* Mon Oct 09 2006 - dave.lin@sun.com
- bump version to 2.0rc2
* Thu Sep 07 2006 - dave.lin@sun.com
- add patch firefox-09-no-pkg-files.diff to remove patch checker scripts 
  since it's unnecessary to deliver them with the bundled version
- change the version 2.0bx to 2.0 to comply WOS integration rules
- re-organize the patch list 
* Mon Sep 04 2006 - dave.lin@sun.com
- bump version to 2.0 beta 2
* Mon Aug 28 2006 - dave.lin@sun.com
- create symbol link libnssckbi.so -> /usr/lib/mps/libnssckbi.so
  to fix bug CR#6459752
* Tue Aug 08 2006 - dave.lin@sun.com
- bump version to 2.0b1
- remove the patch mozilla-03-s11s-smkfl.diff, mozilla-04-s11x-smkfl.diff,
  firefox-03-yelp-hang.diff which have been fixed in 2.0b1
- change to xpinstall/packager to run make to make the binary tarball
* Tue Aug 08 2006 - dave.lin@sun.com
- fixed the preload list problem
* Thu Jul 27 2006 - damien.carbery@sun.com
- Remove 'aclocal' dir from %files as it is now empty.
* Wed Jul 26 2006 - matt.keenan@sun.com
- Remove firefox-10-gecko.m4.diff : yelp uses local copy now, and re-shuffled
  the rest of the firefox-* patches to be in sequence.
* Fri Jul 07 2006 - dave.lin@sun.com
- add patch mozilla-07-no-ldlibpath.diff to remove the LD_LIBRARY_PATH in
  the startup script
* Tue Jun 13 2006 - dave.lin@sun.com
- add patch firefox-15-no-nss-nspr.diff to let firefox use nss, nspr in 
  /usr/lib/mps required by ARC
- remove all nss, nspr header files in development package
* Mon Jun 12 2006 - dave.lin@sun.com
- add patch firefox-14-plugins.diff to add Mozilla plugins direcotry
  (/usr/sfw/lib/mozilla/plugins) in Firefox plugin searching path(CR#6428445)
* Fri Jun 02 2006 - dave.lin@sun.com
- bump src version to 1.5.0.4
* Mon May 08 2006 - dave.lin@sun.com
- bump src version to 1.5.0.3
* Fri Apr 28 2006 - dave.lin@sun.com
- remove patch mozilla-06-skip-strip.diff, use another simple way to skip
  strip instead, setting PKG_SKIP_STRIP=1
* Fri Apr 21 2006 - dave.lin@sun.com
- switch back to 1.5.0.2 since we're not get ARC approved yet
* Fri Apr 14 2006 - dave.lin@sun.com
- removed firefox-chrome-lang.txt per l10n team's request, firefox uses new
  strategy to register chrome entries, so this file is useless
* Thu Apr 13 2006 - davelin@sun.com
- Changed the installation location from "/usr/sfw/lib" to "/usr/lib"
  on Solaris
* Tue Apr 04 2006 - dave.lin@sun.com
- Bump version to 2.0 alpha1
- Remove Patch3,4,11 which have been upstreamed into this version
- Add patch mozilla-06-skip-strip.diff to make no stripped libraries 
* Fri Mar 31 2006 - dave.lin@sun.com
- Add patch firefox-13-locale.diff to make firefox automatically
  pick up locale setting from user environment and start up in
  that locale
* Fri Feb 24 2006 - dave.lin@sun.com
- Add patch firefox-11-new-tab.diff to fix CR6368789
- Add patch firefox-12-preload.diff and extra source file 
  firefox-preload.list.in to enable firefox preload mechanism
- Remove useless file firefox-rebuild-databases since it's only
  for Linux
- Remove useless sources and patch
* Thu Dec 15 2005 - dave.lin@sun.com
- Add patch firefox-09-yelp-hang.diff to fix yelp hang problem.
* Fri Dec 02 2005 - damien.carbery@sun.com
- Add Makefile.in patch to link fontconfig and Xft libraries.
- make from top directory to build nsIconChannel.o.
* Fri Dec 02 2005 - dave.lin@sun.com
- Bump tarball version to 1.5.
- Modify the configuration options
* Fri Nov 11 2005 - dave.lin@sun.com
- Bump tarball version to 1.5rc3.
* Fri Nov 11 2005 - halton.huo@sun.com
- Bump tarball version to 1.5rc2.
* Tue Nov 08 2005 - dave.lin@sun.com
- Bump tarball version to 1.5rc1
- Remove the patch mozilla-07-bz307041.diff since it's upstreamed in 1.5rc1
  already
- Enable '--enalbe-timeline' in nightly builds
* Thu Nov  1 2005 - laca@sun.com
- change version to numeric and introduce %tarball_version
* Fri Oct 21 2005 - dave.lin@sun.com
- Update version from 1.5b1 to 1.5b2 and add patch 307041 from bugzilla
- Change configure option per Leo Sha from developer team
- Add nss header file in development package
* Mon Sep 26 2005 - <halton.huo@sun.com>
- Bump to 1.5b1.
- Move dir mozilla to firefox after tarball unpacking.
* Mon Sep 12 2005 - <laca@sun.com>
- get rid of %builddir as it would be different on Solaris
* Thu Sep 08 2005 - damien.carbery@sun.com
- Change BuildPrereq to BuildRequires, a format that build-gnome2 understands.
* Mon Sep 05 2005 - Dave Lin <dave.lin@sun.com>
- Add patches to remove the specific gtar options 
- Set MOZ_PKG_FORMAT=BZ2 to keep consistent of tarball
  format between linux and solaris
* Fri Sep 01 2005 - damien.carbery@sun.com
- Change gtar to tar; add two necessary mkdir's.
* Mon Aug 22 2005 Dave Lin <dave.lin@sun.com>
- initial version of the spec file created
