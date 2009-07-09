#
# Copyright (c) Sun Microsystems, Inc.
#
# Owner: davelam
# bugdb: bugzilla.mozilla.org
#

#####################################
##   Package Information Section   ##
#####################################

Name:        thunderbird
Summary:     Mozilla Thunderbird Standalone E-mail and Newsgroup Client
Version:     3.0
%define tarball_version 3.0b2 
Release:     1
Copyright:   MPL/LGPL
Group:       Applications/Internet
Distribution:Java Desktop System
Vendor:      Sun Microsystems, Inc.
Source:     http://ftp.mozilla.org/pub/mozilla.org/%{name}/releases/%{tarball_version}/source/%{name}-%{tarball_version}-source.tar.bz2
Source1:     thunderbird-icon.png
Source2:     thunderbird.desktop
%define with_lightning %{?!_without_lightning:1}%{?_without_lightning:0}
%define without_moz_nss_nspr %{?_without_moz_nss_nspr:1}%{?!_without_moz_nss_nspr:0}
Source4:     thunderbird.cfg
Source5:     thunderbird-3.0b2-configure
Source6:     thunderbird-3.0b2-mozilla-configure
Source7:     thunderbird-3.0b2-mozilla-js-src-configure

# owner:evan date:2007-11-28 type:branding
# change preference to support multi-language
Patch1: thunderbird3-01-locale.diff

# owner:hawklu date:2007-04-27 type:branding
# bugster:6542910
Patch2: thunderbird3-02-disable-online-update.diff

# owner:hawklu date:2008-12-04 type:bug bugzilla:463987
Patch3: thunderbird3-03-js.diff

# owner:hawklu date:2008-12-10 type:bug bugzilla:449754 status:upstream
Patch4: thunderbird3-04-libogg-liboggz.diff

# owner:alfred date:2008-10-10 type:bug bugster:6750518
Patch5: thunderbird3-05-ksh.diff

# owner:hawklu date:2008-12-16 type:bug bugster:6770058 
Patch6: thunderbird3-06-font-config.diff

# owner:brian.lu date:2009-02-19 type:bug bugzilla:478871 
Patch7: thunderbird3-07-pango-1-23.diff

# owner:ginn.chen date:2009-02-27 type:bug bugzilla:472635 status:upstream
Patch8: thunderbird3-08-im-context-not-match.diff

# owner:ginn.chen date:2009-02-27 type:bug bugzilla:471642 status:upstream
Patch9: thunderbird3-09-rename-nsSelectionBatcher.diff

# owner:ginn.chen date:2009-02-27 type:bug bugzilla:479022 status:upstream
Patch10: thunderbird3-10-bigendian.diff

# owner:ginnchen date:2008-10-15 type:branding
# bugzilla:457196
Patch11: thunderbird3-11-jemalloc-shared-library.diff

# owner:hawklu date:2008-12-12 type:bug bugzilla:468041 status:upstream
Patch13: thunderbird3-13-js-dtrace.diff

# owner:ginnchen date:2009-03-04 type:bug bugzilla:448512
Patch14: thunderbird3-14-xinerama.diff

# owner:fujiwara date:2008-04-10 type:bug
# bugster:6686579 bugzilla:285267
Patch15: thunderbird3-15-g11n-nav-lang.diff

# owner:ginnchen date:2008-08-19 type:bug
# bugster:6724471 bugzilla:451007
Patch16: thunderbird3-16-delay-stopping-realplayer.diff

# owner:ginnchen date:2009-03-04 type:bug bugzilla:472269 status:upstream
Patch17: thunderbird3-17-runmozilla.diff

# owner:ginnchen date:2008-11-27 type:bug bugzilla:464443
Patch18: thunderbird3-18-fix-mimetype-for-helper-app.diff

# owner:hawklu date:2009-03-31 type:bug bugzilla:484160 defect:7723 status:upstream
Patch19: thunderbird3-19-small-migration-wizard-window.diff

URL:         http://www.sun.com/software/javadesktopsystem/

BuildRoot:   %{_tmppath}/%{name}-%{tarball_version}-build
Prefix:      /usr
Provides:    webclient
Autoreqprov: on

#####################################
##     Package Defines Section     ##
#####################################

%define _unpackaged_files_terminate_build 0
%define _tbdir %{_libdir}/%{name}

#####################################
##  Package Requirements Section   ##
#####################################

BuildRequires: libpng-devel
BuildRequires: libjpeg
BuildRequires: zlib-devel
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
Mozilla Thunderbird is a standalone e-mail and newsgroup client 
that can be used as a companion to Mozilla Firefox or by itself. 

#####################################
##   Package Preparation Section   ##
#####################################

%prep

%setup -q -c -n %{name}
cd ..
/bin/mv %{name} %{name}.tmp.$$
# this is workaround for current 3.0 beta 2 tar ball
# fix it when we bump to beta 3
/bin/mv %{name}.tmp.$$/thunderbird %{name} || /bin/mv %{name}.tmp.$$ %{name}
rm -rf %{name}.tmp.$$

cd %{name}/mozilla
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
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1

# go back to the thunderbird directory
cd ..  
%patch19 -p1

cp  %{SOURCE5} configure
cp  %{SOURCE6} mozilla/configure
cp  %{SOURCE7} mozilla/js/src/configure
chmod +x configure mozilla/configure mozilla/js/src/configure

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
# we don't have autoconf-2.13 in jds-cbe
mk_add_options AUTOCONF=echo
mk_add_options BUILD_OFFICIAL=1
mk_add_options MOZILLA_OFFICIAL=1
mk_add_options MOZ_OBJDIR=@TOPSRCDIR@/../objdir-tb
ac_add_options --prefix=%{_prefix}
ac_add_options --libdir=%{_libdir}
ac_add_options --mandir=%{_mandir}
ac_add_options --enable-static
ac_add_options --enable-official-branding
ac_add_options --enable-application=mail
ac_add_options --enable-dtrace
ac_add_options --with-system-jpeg
ac_add_options --enable-system-cairo
ac_add_options --enable-optimize
ac_add_options --disable-updater
ac_add_options --disable-tests
ac_add_options --disable-debug
ac_add_options --disable-shared
ac_add_options --disable-crashreporter
EOF

%if %with_lightning
echo "ac_add_options --enable-calendar" >> .mozconfig
%endif

BUILD_OFFICIAL=1 
MOZILLA_OFFICIAL=1
MOZ_PKG_FORMAT=BZ2
PKG_SKIP_STRIP=1
export BUILD_OFFICIAL MOZILLA_OFFICIAL MOZ_PKG_FORMAT PKG_SKIP_STRIP CFLAGS CXXFLAGS

export MOZCONFIG=$PWD/.mozconfig
make -f client.mk build

# install thunderbird.cfg (make debugging easier in obj-tb/dist/bin)
cp  %{SOURCE4} ../objdir-tb/mozilla/dist/bin/thunderbird.cfg

cd ../objdir-tb
make package

%install
/bin/rm -rf $RPM_BUILD_ROOT

BUILDDIR=$PWD/../objdir-tb
/bin/mkdir -p $RPM_BUILD_ROOT%{_libdir}
cd $RPM_BUILD_ROOT%{_libdir}
/usr/bin/bzip2 -dc $BUILDDIR/mozilla/dist/thunderbird-*.tar.bz2 | gtar -xf -

/bin/mkdir -p $RPM_BUILD_ROOT%{_bindir}
/bin/ln -s ../lib/thunderbird/thunderbird $RPM_BUILD_ROOT%{_bindir}/thunderbird

/bin/mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
/bin/mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps
install -c -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/pixmaps/thunderbird-icon.png
install -c -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/applications/thunderbird.desktop

# install the man page
#/bin/mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
#install -c -m 644  %{SOURCE4} $RPM_BUILD_ROOT%{_mandir}/man1/thunderbird.1

#/bin/cat %{SOURCE3} | /usr/bin/sed -e 's,FFDIR,%{_tbdir},g' > \
#  $RPM_BUILD_ROOT%{_tbdir}/thunderbird-rebuild-databases
#/bin/chmod 755 $RPM_BUILD_ROOT%{_tbdir}/thunderbird-rebuild-databases

# install thunderbird.cfg
install -c -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_tbdir}/thunderbird.cfg

# remove local dictionary and share the one that delivered 
# by myspell-dictionary
rm -f $RPM_BUILD_ROOT%{_tbdir}/dictionaries/en-US.dic
rm -f $RPM_BUILD_ROOT%{_tbdir}/dictionaries/en-US.aff
rmdir $RPM_BUILD_ROOT%{_tbdir}/dictionaries

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

%preun

#####################################
##      Package Files Section      ##
#####################################

%files
%defattr(-,root,root)
%dir %{_tbdir}
%{_tbdir}/*
%{_bindir}/thunderbird
#%{_mandir}/man1/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}-icon.png

%changelog
* Tue Mar 31 2009 - brian.lu@sun.com
- Fix bug 7723
* Mon Mar 30 2009 - ginn.chen@sun.com
- Remove thunderbird3-12-ldap-crash.diff, this bug is gone.
* Fri Mar 06 2009 - ginn.chen@sun.com
- Copy firefox3-25-pango-1-23.diff to thunderbird3-07-pango-1-23.diff
* Fri Mar 06 2009 - brian.lu@sun.com
- Replace the patch thunderbird3-07-pango-1-23.diff with 
  the  patch firefox3-25-pango-1-23.diff 
* Thu Mar 05 2009 - ginn.chen@sun.com
- add option to use system cairo and jpeg
* Wed Mar 04 2009 - ginn.chen@sun.com
- copy firefox3-*.diff to thunderbird3-*.diff
- use configure in ext-sources
* Mon Mar 02 2009 - alfred.peng@sun.com
- Patch updates for Thunderbird 3.0b2.
* Fri Feb 27 2009 - brian.lu@sun.com
- bump to Thunderbird 3.0b2
* Thu Feb 19 2009 - brian.lu@sun.com
- Fix the issue caused by pango upgrade
* Fri Jan 23 2009 - brian.lu@sun.com
- Fix the bug 6187
* Fri Jan 16 2009 - brian.lu@sun.com
-  Change the bugzilla ID of thunderbird-13-ldap-crash.diff to 374731
* Wed Dec 31 2008 - brian.lu@sun.com
- Replace the patch thunderbird-24-rename-selectionBacher.diff
  with thunderbird-25-allow-muldefs.diff
* Mon Dec 22 2008 - brian.lu@sun.com
- Upgrade to 3.0b1
* Tue Dec 02 2008 - brian.lu@sun.com
- Fix the bug CR677345
* Mon Oct 13 2008 - ginn.chen@sun.com
- Change /bin/tar to tar.
* Oct 10 2008 - alfred.peng@sun.com
- Add thunderbird-21-ksh.diff for indiana only to fix bugster CR6750518.
* Man 06 2008 - brian.lu@sun.com
- Bump lightning to 0.9 
* Sat Sep 27 2008 - ginn.chen@sun.com
- Bump to 2.0.0.17
* Fri Sep 26 2008 - brian.lu@sun.com
- Fix the bug CR6752288
* Tue Jul 29 2008 - brian.lu@sun.com
- bump to 2.0.0.16
* Mon Jul 21 2008 - ginn.chen@sun.com
- Add bugdb info.
* Mon Jun 02 2008 - ginn.chen@sun.com
- Add indiana branding patch: thunderbird-18-remove-hardcoded-fontname.diff
* Mon May 05 2008 - dave.lin@sun.com
- bump to 2.0.0.14
* Thu April 24 2008 - brian.lu@sun.com
- bump lightning to 0.8
* Wed Mar 26 2008 - brian.lu@sun.com
- Fix bug CR6640830
* Thu Feb 28 2008 - dave.lin@sun.com
- bump to TB 2.0.0.12
* Fir Nov 28 2007 - evan.yan@sun.com
- replace thunderbird-08-locale.diff with mozilla-09-locale.diff, to correct our
  way of supporting multi-language
* Mon Nov 19 2007 - dave.lin@sun.com
- bump to TB 2.0.0.9
- remove patch thunderbird-16-crash-with-some-themes.diff since it has been upstreamed
* Tue Nov 13 2007 - brian.lu@sun.com
- Add patch, thunderbird-16-crash-with-some-themes.diff 
  to fix 'thunderbird crashing under some themes' bug CR6586103 
* Fri Nov 02 2007 - dave.lin@sun.com
- bump lightning to 0.7
* Fri Aug 03 2007 - dave.lin@sun.com
- bump to 2.0.0.6
* Mon Jun 23 2007 - dave.lin@sun.com
- bump to 2.0.0.5
* Thu Jun 21 2007 - damien.carbery@sun.com
- Add patch, mozilla-08-cairo-update.diff, to update the private copy of
  cairo.h used in the build.
* Tue June 05 2007 - brian.lu@sun.com
- Fix the bug CR6284006: GConf Error: Bad key or directory name: "desktop/gnome/url-handlers/GMT+00/command": `+' messages 
* Mon Apr 30 2007 - dave.lin@sun.com
- remove local dictionary and use the one delivered by myspell-dictionary(CR6218511)
* Thu Apr 27 2007 - brian.lu@sun.com
- add patch to grey out "Check for Updates" in Thunderbird menu since it's not supported
* Sat Apr 21 2007 - dave.lin@sun.com
- Bump to 2.0.0.0
* Thu Apr 12 2007 - dave.lin@sun.com
- bump to 2.0.0.0rc1, removed the patches thunderbird-11-drag-and-drop.diff,
  thunderbird-12-defaultAccount.diff which are upstreamed in this release
* Thu Apr 12 2007 - dave.lin@sun.com
- disable update feature in Thunderbird menu since it's not supported
  on Solaris so far(CR#6542910)
* Wed Mar 23 2007 - brian.lu@sun.com 
- Fix the bug CR6535724:Thunderbird crashes with LDAP in snv 60 
* Mon Mar 12 2007 - brian.lu@sun.com 
- Fix the bug CR6530327
* Sat Mar 10 2007 - dougs@truemail.co.th
- Fixed URL for lightning
* Sat Mar 03 2007 - dave.lin@sun.com
- bump lightning version to 0.3.1
* Thu Feb 01 2007 - brian.lu@sun.com
- fix drag and drop crashing bug CR6519257 
- bugzilla id 367203. The patch has been put into upstream
* Sun Jan 28 2007 - laca@sun.com
- add full download url for lightning
* Fri Jan 26 2007 - dave.lin@sun.com
- enable lightning extension(0.3) in Thunderbird
* Wed Jan 24 2007 - dave.lin@sun.com
- bump version to 2.0b2
* Thu Dec 28 2006 - dave.lin@sun.com
- change the patch type to branding for some patches in patch comments
- bump version to 2.0b1 and remove mozilla-03-s11s-smkfl.diff, 
  mozilla-04-s11x-smkfl.diff since they're upstreamed in that branch
* Fri Nov 17 2006 - dave.lin@sun.com
- add patch comments
* Mon Nov 13 2006 - dave.lin@sun.com
- change the version to 1.5.0.8 since 2.0a1 could not be able to integrated 
  into SNV, and add patches mozilla-03-s11s-smkfl.diff, mozilla-04-s11x-smkfl.diff 
  back because they're not upstreamed in the branch that for Thunderbird 1.5.x
* Thu Sep 07 2006 - dave.lin@sun.com
- add patch thunderbird-10-no-pkg-files.diff to remove patch checker scripts
  since it's unnecessary to deliver them with the bundled version
- change the version 2.0a1 to 2.0 to comply WOS integration rules
- re-organize the patch list
* Mon Aug 28 2006 - dave.lin@sun.com
- create symbol link libnssckbi.so -> /usr/lib/mps/libnssckbi.so
  to fix bug CR#6459752
* Tue Aug 08 2006 - dave.lin@sun.com
- bump version to 2.0a1
- remove the patch mozilla-03-s11s-smkfl.diff, mozilla-04-s11x-smkfl.diff
  which have been fixed in 2.0a1
- change to xpinstall/packager to run the make to generate the binary tarball
* Mon Jul 31 2006 - dave.lin@sun.com
- bump to 1.5.0.5
* Fri Jul 07 2006 - dave.lin@sun.com
- add patch mozilla-07-no-ldlibpath.diff to remove the LD_LIBRARY_PATH in
- change to "disable-static, enable-shared" per Brian Lu
* Wed Jun 21 2006 - dave.lin@sun.com
- remove patch thunderbird-07-ldap-prefs.diff to fix bug CR#6344861
* Fri Jun 02 2006 - dave.lin@sun.com
- bump src version to 1.5.0.4
* Sat Apr 29 2006 - halton.huo@sun.com
- Add patch thunderbird-09-no-nss-nspr.diff to not deliver the nss,nspr
* Fri Apr 27 2006 - damien.carbery@sun.com
- Remove patch 9 as it is not in svn and breaks build.
* Fri Apr 27 2006 - dave.lin@sun.com
- change to not deliver the devel pkg
- add patch thunderbird-09-no-nss-nspr.diff to not deliver the nss,nspr
  libraries, and use firefox's instead 
- remove patch mozilla-06-skip-strip.diff, use another simple way to skip
  strip instead, setting PKG_SKIP_STRIP=1 
* Fri Apr 21 2006 - dave.lin@sun.com
- bump to 1.5.0.2, remove patch 06 thunderbird-06-save-all-attach.diff,
  which is already upstreamed
* Fri Apr 14 2006 - dave.lin@sun.com
- add patch mozilla-06-skip-strip.diff to make no stripped libraries 
- add patch firefox-13-locale.diff to make firefox automatically
  pick up locale setting from user environment and start up in
  that locale
* Thu Apr 13 2006 - dave.lin@sun.com
- Changed the installation location from "/usr/sfw/lib" to "/usr/lib"
  on Solaris

* Fri Mar 10 2006 -halton.huo@sun.com
- Add patch thunderbird-06-save-all-attach.diff to fix 6373061.
- Add patch thunderbird-07-ldap-prefs.diff to fix CR6344861.

* Tue Jan 17 2006 - dave.lin@sun.com
- Bump tarball version to 1.5
- add two configure options --enable-static, --disable-shared
- to get rid of intermedia shared libraries  
- disable parallel build option 

* Tue Nov 08 2005 - dave.lin@sun.com
- Bump tarball version to 1.5rc1
- Remove the patch mozilla-07-bz307041.diff since it's upstreamed in 1.5rc1 already

* Thu Nov  1 2005 - laca@sun.com
- change version to numeric and introduce %tarball_version

* Fri Oct 21 2005 - <halton.huo@sun.com>
- Bump to 1.5b2.
- Add patch 307041 from bugzilla.

* Mon Sep 26 2005 - <halton.huo@sun.com>
- Bump to 1.5b1.
- Move dir mozilla to thunderbird after tarball unpacking.

* Thu Sep 08 2005 - damien.carbery@sun.com
- Change BuildPrereq to BuildRequires, a format that build-gnome2 understands.

* Mon Sep 05 2005 - Dave Lin <dave.lin@sun.com>
- Add patches to remove the specific gtar options
- Set MOZ_PKG_FORMAT=BZ2 to keep consistent of tarball
  format between linux and solaris

* Fri Sep 02 2005 - damien.carbery@sun.com
- Change gtar to tar and rework tar command.

* Mon Aug 22 2005 - Dave Lin <dave.lin@sun.com>
- initial version of the spec file created

