#
# spec file for package SUNWgnome-gui-test
#
# includes module(s): dogtail
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: davelam
#
%include Solaris.inc
%use dogtail = dogtail.spec

Name:                    SUNWgnome-gui-test
Summary:                 GUI test tool and automation framework
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWPython
Requires: SUNWPython-extra
Requires: SUNWgnome-a11y-libs
Requires: SUNWgnome-python-libs
BuildRequires: SUNWPython-devel
BuildRequires: SUNWPython-extra
BuildRequires: SUNWgnome-a11y-libs-devel
Requires: SUNWdesktop-cache

%prep
rm -rf %name-%version
mkdir %name-%version
%dogtail.prep -d %name-%version

%build

%install
[ "$RPM_BUILD_ROOT" != "" ] && [ -d $RPM_BUILD_ROOT ] && rm -rf $RPM_BUILD_ROOT
%dogtail.install -d %name-%version

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}
#Remove AT-API browser and dogtail from the menus
echo "NoDisplay=true" >> $RPM_BUILD_ROOT%{_datadir}/applications/sniff.desktop
echo "NoDisplay=true" >> $RPM_BUILD_ROOT%{_datadir}/applications/dogtail-recorder.desktop
%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri desktop-mime-cache

%postun
%restart_fmri desktop-mime-cache

%files
%defattr (-, root, bin)
%doc -d dogtail-%{dogtail.version} README
%doc(bzip2) -d dogtail-%{dogtail.version} COPYING NEWS
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*.desktop
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/dogtail
%{_datadir}/dogtail
%attr (-, root, other) %{_datadir}/icons

%changelog
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Mon Mar 23 2009 - jeff.cai@sun.com
- Since /usr/bin/dogtail-recorder (SUNWgnome-gui-test) requires
  /usr/lib/python2.4/vendor-packages/gtk-2.0/gtk/keysyms.pyc which is
  found in SUNWgnome-python-libs, add the dependency.
* Wed Mar 11 2009 - dave.lin@sun.com
- Took the ownership of this spec file.
* Fri Sep 19 2008 - halton.huo@sun.com
- Add %doc part to %files
* Thu Apr 03 2008 - damien.carbery@sun.com
- Add SUNW_Copyright.
* Wed Apr 04 2007 - glynn.foster@sun.com
- Set .desktop items to NoDisplay=true
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
* Tue Feb 21 2006 - damien.carbery@sun.com
- Update packaging for new tarball.
* Sat Dec  3 2005 - laca@sun.com
- add %post script that runs update-desktop-database
* Mon Oct 21 2005 - laca@sun.com
- fix permissions
* Thu Oct 20 2005 - damien.carbery@sun.com
- Initial version.
