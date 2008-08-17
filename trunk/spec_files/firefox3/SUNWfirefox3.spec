#
# spec file for package SUNWfirefox3
#
# includes module(s): firefox3
#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner:davelam
#
# DO NOT REMOVE NEXT LINE
# PACKAGE NOT ARC REVIEWED BY SUN JDS TEAM
#
%include Solaris.inc
# use --without-apoc-adapter to disable building apoc adapter 
# default: not build apoc adapter
%define with_apoc_adapter %{?_with_apoc_adapter:1}%{?!_with_apoc_adapter:0}
# use --without-moz-nss-nspr to not devlier Mozilla bundled nss, nspr libs
# default: with Mozilla bundled nss, nspr libs
%define without_moz_nss_nspr %{?_without_moz_nss_nspr:1}%{?!_without_moz_nss_nspr:0}
%use firefox = firefox3.spec

#####################################
##   Package Information Section   ##
#####################################

# Build as Firefox3 only if "--with-ff3" is specified 
# ===================================================
Name:          SUNWfirefox
Summary:       Mozilla Firefox Web browser
Version:       %{firefox.version}
Source:        %{name}-manpages-0.1.tar.gz
Source1:       staroffice-mime.types.in
Source2:       staroffice-mailcap.in
SUNW_BaseDir:  %{_basedir}
SUNW_Category: FIREFOX,application,%{jds_version}
SUNW_Copyright:%{name}.copyright
BuildRoot:     %{_tmppath}/%{name}-%{version}-build

#####################################
##  Package Requirements Section   ##
#####################################

%include default-depend.inc
Requires: SUNWjdsrm
Requires: SUNWj5rt
Requires: SUNWgnome-base-libs
Requires: SUNWfontconfig
Requires: SUNWfreetype2
Requires: SUNWgnome-config
Requires: SUNWgnome-libs
Requires: SUNWgnome-vfs
Requires: SUNWlibC
Requires: SUNWlibms
Requires: SUNWtls
Requires: SUNWlibmsr
BuildRequires: SUNWzip
BuildRequires: SUNWgtar
BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-vfs-devel
BuildRequires: SUNWgnome-component-devel
BuildRequires: SUNWgnome-base-libs-devel
Requires: SUNWpostrun
#%if %option_with_indiana_branding
#Requires: SUNWgetting-started-guide
#%endif
%if %without_moz_nss_nspr
Requires: SUNWpr
%endif
Requires: SUNWsqlite3

#####################################
##   Package Description Section   ##
#####################################

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires:      %{name}

%if %with_apoc_adapter
%package apoc-adapter
Summary:       %{summary} - Apoc Adapter
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires:      %{name}
%endif

#####################################
##   Package Preparation Section   ##
#####################################

%prep
rm -rf %name-%version
mkdir -p %name-%version
%firefox.prep -d %name-%version
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

#####################################
##      Package Build Section      ##
#####################################

%build
export PKG_CONFIG_PATH=${_libdir}/pkgconfig:%{_pkg_config_path}
LDFLAGS="-z ignore" 
%if %without_moz_nss_nspr
LDFLAGS="$LDFLAGS -R%{_libdir}/mps"
%endif
export LDFLAGS
export CFLAGS="-xlibmopt -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 -I/usr/X11/include"
export CXXFLAGS="-xlibmil -xlibmopt -lCrun -lCstd -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64"
%if %option_with_fox
export CFLAGS="$CFLAGS -I/usr/X11/include"
%endif

%firefox.build -d %name-%version

%install
%firefox.install -d %name-%version

# creat file list for SUNWfirefox to separate .autoreg(marked as 'v')
# and maybe libmozapoc.so if apoc enabled
cd $RPM_BUILD_ROOT%{_libdir}
find %{firefox.name} ! -type d | egrep -v "(libmozapoc.so|\.autoreg|xpidl|xpt_dump|xpt_link)" | \
  sed -e 's#{#\\{#g' -e 's#}#\\}#g' -e 's#^.*$#%{_libdir}/&#' \
    >  %{_builddir}/%name-%version/%{name}.list

rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

#########################################
##  Package Post[Un] Install Section   ##
#########################################

%post
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait


%postun
test -x $BASEDIR/lib/postrun || exit 0
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS


%if %with_apoc_adapter
%post apoc-adapter
PKGCOND=/usr/bin/pkgcond
test -x $PKGCOND || exit 0
if $PKGCOND is_path_writable $BASEDIR/lib/%{firefox.name} > /dev/null 2>&1 ; then
  touch $BASEDIR/lib/%{firefox.name}/.autoreg
fi

exit 0
%postun apoc-adapter
PKGCOND=/usr/bin/pkgcond
test -x $PKGCOND || exit 0
if $PKGCOND is_path_writable $BASEDIR/lib/%{firefox.name} > /dev/null 2>&1 ; then
  touch $BASEDIR/lib/%{firefox.name}/.autoreg
fi

exit 0
%endif

%files -f SUNWfirefox.list

%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/firefox
%dir %attr (0755, root, bin) %{_libdir}
%ghost %{_libdir}/%{firefox.name}/.autoreg

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/firefox.desktop
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/firefox-icon.png
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%files devel
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/%{firefox.name}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/idl/%{firefox.name}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%{_libdir}/firefox/xpidl
%{_libdir}/firefox/xpt_dump
%{_libdir}/firefox/xpt_link

%if %with_apoc_adapter
%files apoc-adapter
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/%{firefox.name}/components/libmozapoc.so
%endif

%changelog
* Sun Aug 17 2008 - moinakg@belenix.org
- Remove circular dependency on self.
* Thu May 22 2008 - dave.lin@sun.com
- change to build pkg only if "--with-ff3" is specified, otherwisze build nothing
- change to build as "SUNWfirefox" and as default browser
* Fri May 16 2008 - damien.carbery@sun.com
- Disable creation of symlink for firefox 3. This means that ff2 is left as
  default browser.
* Thu Mar 13 2008 - damien.carbery@sun.com
- Add -I/usr/X11/include to CFLAGS after update of SUNWwinc.
* Mon Feb 25 2008 - alfred.peng@sun.com
- Add "-D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64" in CXXFLAGS to fix CR#6516110
* Thu Feb 21 2008 - damien.carbery@sun.com
- Rename SUNWsqlite dependency to SUNWsqlite3 to match pkg from SFW.
* Wed Jan 09 2008 - dave.lin@sun.com
- renamed FF 3 spec to *firefox3 to let FF 3 coexist with FF 2
* Fri Dec 28 2007 - dave.lin@sun.com
- deliver .autoreg no matter apoc enabled or not
* Thu Dec 27 2007 - dave.lin@sun.com
- move to 3.0 beta2
- set not building apoc adapter as default
- remove SUNWfirefox-root pkg
- disable apoc adapter since it's not available for 3.0
* Thu Dec 27 2007 - dave.lin@sun.com
- set no apoc-adapter as default
* Sat Oct 20 2007 - laca@sun.com
- add indiana getting started guide dependency
* Fri Oct 12 2007 - laca@sun.com
- add /usr/X11/include to CFLAGS if built with FOX
* Fri Sep 28 2007 - laca@sun.com
- delete Nevada X deps
- disable developer guide dep if sun branding is not requested
* Tue Aug 21 2007 - dave.lin@sun.com
- made postremove/postinstall script more robust(CR#6594606)
* Tue Apr 24 2007 - laca@sun.com
- s/0755/-/ in defattr so that files are not made all executable
* Tue Apr 10 2007 - dave.lin@sun.com
- remove dependency on SUNWstaroffice-menuintegration from SUNWfirefox-root
  since it caused CR#6530982 fixed failed(see details in bugster)
* Mon Mar 26 2007 - dave.lin@sun.com
- add new package SUNWfirefox-root to fix bug CR#6530982, the package 
  would just add staroffice entries in /etc/mime.types /etc/mailcap 
  in postinstall
* Tue Mar 20 2007 - dave.lin@sun.com
- fix bug CR#6521792
    part1: add file ".autoreg" and add postinstall/postremove scripts in
           SUNWfirefox-apoc-adapter
    part2: add patch firefox-12-regenerate-compreg-file.diff
* Thu Dec 28 2006 - dave.lin@sun.com
- remove %preun to fix bug CR#6502253
* Fri Dec  8 2006 - laca@sun.com
- add SUNWsolaris-devel-docs dependency
* Tue Nov 28 2006 - dave.lin@sun.com
- add %if %with_apoc_adapter to conditinoally disable apoc adapter,
  default: enable apoc adapter, use --without-apoc-adapter to disable it
* Mon Nov 27 - dave.lin@sun.com
- enable apoc adapter(SUNWfirefox-apoc-adapter), CR#6478680
* Tue Sep 05 2006 - Matt.Keenan@sun.com
- New Manpage tarball
* Thu Jul 27 2006 - damien.carbery@sun.com
- Remove 'aclocal' dir from %files as it is now empty.
* Fri Jul 14 2006 - laca@sun.com
- update %post/%postun/etc scripts to support diskless client setup,
  part of 6448317
* Thu Jul 13 2006 - dave.lin@sun.com
- add "-lCrun -lCstd" in CXXFLAGS to improve the startup performance
* Thu Jun 29 2006 - laca@sun.com
- update postrun scripts
* Tue Jun 20 2006 - damien.carbery@sun.com
- Add SUNWpr and SUNWtls dependencies after check-deps.pl run.
* Mon Jun 12 2006 - dave.lin@sun.com
- changed to let firefox use nss,nspr in /usr/lib/mps required by ARC
- remove -R%{_libdir}
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Fri Jun 09 2006 - damien.carbery@sun.com
- Uncomment man page lines in %files.
* Thu Jun 08 2006 - dave.lin@sun.com
- add man page prepared by Leon Sha
* Thu Apr 13 2006 - dave.lin@sun.com
- changed installation location from "/usr/sfw/lib" to "/usr/lib"
* Fri Feb 24 2006 - dave.lin@sun.com
- Changed package category to FIREFOX
- Improved preremove script, using ${BASEDIR} instead of absolute path
* Mon Feb 20 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Thu Jan 19 2006 - damien.carbery@sun.com
- Add BuildRequires SUNWgnome-base-libs-devel.
* Sat Dec  3 2005 - laca@sun.com
- add %post script that runs update-desktop-database
* Fri Dec 02 2005 - damien.carbery@sun.com
- Add .autoreg file introduced in 1.5.
* Mon Oct 31 2005 - laca@sun.com
- Merge share pkgs into base
* Mon Oct 24 2005 - damien.carbery@sun.com
- Add BuildRequires SUNWgtar because source tarball needs GNU tar.
* Mon Sep 26 2005 - halton.huo@sun.com
- Change version same with linux verion.
* Fri Sep 02 2005 - damien.carbery@sun.com
- Correct ownership of %{_libdir}/pkgconfig directory.
* Fri Aug 26 2005 - dave.lin@sun.com
- initial version of the spec file created
