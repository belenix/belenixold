#
# spec file for package SUNWthunderbird
#
# includes module(s): thunderbird
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: davelam
#
# DO NOT REMOVE NEXT LINE
# PACKAGE NOT INCLUDED IN GNOME UMBRELLA ARC
#
%include Solaris.inc
# use --without-lightning to disable building lightning
# default: build lightning
%define with_lightning %{?!_without_lightning:1}%{?_without_lightning:0}
%use thunderbird = thunderbird.spec

#####################################
##   Package Information Section   ##
#####################################

Name:          SUNWthunderbird
Summary:       Mozilla Thunderbird Email/Newsgroup Client
Version:       %{thunderbird.version}
Source:        %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:  %{_basedir}
SUNW_Category: THUNDERBIRD,application,%{jds_version}
SUNW_Copyright:%{name}.copyright
BuildRoot:     %{_tmppath}/%{name}-%{version}-build

#####################################
##  Package Requirements Section   ##
#####################################

%include default-depend.inc
Requires: SUNWjdsrm
Requires: SUNWj5rt
Requires: SUNWgnome-base-libs
Requires: SUNWdtbas
Requires: SUNWfontconfig
Requires: SUNWfreetype2
Requires: SUNWgnome-config
Requires: SUNWgnome-libs
Requires: SUNWgnome-vfs
Requires: SUNWlibC
Requires: SUNWlibms
Requires: SUNWdesktop-cache
Requires: SUNWpr
Requires: SUNWtls
Requires: SUNWbash
BuildRequires: SUNWzip
BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-vfs-devel
BuildRequires: SUNWgnome-component-devel
BuildRequires: SUNWgnome-base-libs-devel

#####################################
##   Package Description Section   ##
#####################################

%if %with_lightning
%package calendar
Summary:       %{summary} - Calendar
Version:       %{thunderbird.version}
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires:      SUNWthunderbird
%endif

#####################################
##   Package Preparation Section   ##
#####################################

%prep
rm -rf %name-%version
mkdir -p %name-%version
%thunderbird.prep -d %name-%version
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

#####################################
##      Package Build Section      ##
#####################################

%build
export PKG_CONFIG_PATH=${_libdir}/pkgconfig:%{_pkg_config_path}
export MSGFMT="/usr/bin/msgfmt"
export LDFLAGS="-z ignore"
export CFLAGS="-xlibmopt -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 -I/usr/X11/include"
export CXXFLAGS="-xlibmil -xlibmopt -lCrun -lCstd -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64"

%thunderbird.build -d %name-%version

%install
%thunderbird.install -d %name-%version

%if %with_lightning
# Lightning extension ID
ext_id=e2fda1a4-762b-4020-b5ad-a41df1933103

# create file list for SUNWthunderbird, SUNWthunderbird-calendar(ie. Lightning)
cd $RPM_BUILD_ROOT%{_libdir}
find thunderbird ! -type d | \
  sed -e 's#{#\\{#g' -e 's#}#\\}#g' -e 's#^.*$#%{_libdir}/&#' \
  >  /tmp/%{name}-full.list

grep -v "{${ext_id}" /tmp/%{name}-full.list > \
  %{_builddir}/%name-%version/%{name}.list
grep "{${ext_id}" /tmp/%{name}-full.list > \
  %{_builddir}/%name-%version/%{name}-calendar.list

rm -f /tmp/%{name}-full.list
%endif

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
%restart_fmri desktop-mime-cache

%postun
%restart_fmri desktop-mime-cache

#####################################
##      Package Files Section      ##
#####################################

%if %with_lightning
%files -f SUNWthunderbird.list
%else
%files
%endif

%doc -d thunderbird/mozilla README.txt LICENSE
%dir %attr (0755, root, other) %{_datadir}/doc

%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/thunderbird
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/thunderbird.desktop
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/thunderbird-icon.png
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%if %with_lightning
%files calendar -f SUNWthunderbird-calendar.list
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%endif

%changelog
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Mon Mar 23 2009 - jeff.cai@sun.com
- Since /usr/lib/thunderbird/thunderbird (SUNWthunderbird) requires
  /usr/bin/bash which is found in SUNWbash, add the dependency.
* Thu Sep 19 2008 - brian.lu@sun.com
- add %doc section to generate new copyright files
* Thu Apr 24 2008 - brian.lu@sun.com
- remove wcap-enable.xpi because WCAP is already part of lightning 0.8
* Fri Oct 12 2007 - laca@sun.com
- add /usr/X11/include to CFLAGS/CXXFLAGS if built with FOX
* Tue Apr 24 2007 - laca@sun.com
- s/0755/-/ in defattr so that files are not made all executable
* Sat Mar 03 2007 - dave.lin@sun.com
- enable WCAP in lightning
* Fri Jan 26 2007 - dave.lin@sun.com
- enable lightning extension(0.3) in Thunderbird
- remove BuildRequires: SUNWfirefox-devel since it's not necessary
- remove -R%{_libdir}/firefox since is not necessary
* Thu Dec 28 2006 - dave.lin@sun.com
- remove "Requires:  SUNWfirefox" since it's not necessary
* Tue Sep 05 2006 - Matt.Keenan@sun.com
- New Manpage tarball
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
- changed to let thunderbird use nss,nspr in /usr/lib/mps required by ARC
- remove -R%{_libdir}
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Fri Jun 09 2006 - damien.carbery@sun.com
- Uncomment man page lines in %files.
* Thu Jun 08 2006 - dave.lin@sun.com
- add man page prepared by Leon Sha
* Fri May 12 2006 - damien.carbery@sun.com
- Small update to dependency list after check-deps.pl run.
* Thu Apr 27 2006 - dave.lin@sun.com
- remove the devel pkg since the it's almost the same as firefox's devel pkg
- set -R%{_libdir}/firefox to let thunderbird use the nss,nspr libs delivered
  by firefox
* Fri Apr 14 2006 - dave.lin@sun.com
- changed pkg category to "THUNDERBIRD" to make it more clear
* Thu Apr 13 2006 - dave.lin@sun.com
- changed the installation location from "/usr/sfw/lib" to "/usr/lib"
* Mon Feb 20 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Thu Jan 18 2006 - dave.lin@sun.com
- add "-lXft -lfontconfig -lfreetype" to support configure opt "enable-static"
* Sat Dec  3 2005 - laca@sun.com
- add %post script that runs update-desktop-database
* Mon Oct 31 2005 - laca@sun.com
- merge -share pkgs into base
* Mon Sep 26 2005 - halton.huo@sun.com
- Change version same with linux verion.
* Thu Sep 22 2005 - laca@sun.com
- add %{_libdir} to %files so that we actually package thunderbird...
* Fri Sep 02 2005 - damien.carbery@sun.com
- Fix %files.
* Fri Aug 26 2005 - dave.lin@sun.com
- initial version of the spec file created
