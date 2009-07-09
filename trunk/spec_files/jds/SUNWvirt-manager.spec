#
# spec file for package SUNWvirt-manager
#
# includes module(s): virt-manager
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: mattman
#
%include Solaris.inc

%use virtmanager = virt-manager.spec

Name:                    SUNWvirt-manager
Summary:                 Virtual Machine Manager
Version:                 %{virtmanager.version}
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:           %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Source:            	 %{name}-manpages-0.1.tar.gz

%ifnarch sparc
# these packages are only avavilable on i386/x64
# ===========================================

%include default-depend.inc
Requires: SUNWgnome-python-libs
Requires: SUNWlibvirt
Requires: SUNWvirtinst
Requires: SUNWurlgrabber
Requires: SUNWdesktop-cache
Requires: %{name}-root
BuildRequires: SUNWgnome-python-libs-devel

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc


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
%virtmanager.prep -d %name-%version
#unzip the manpage tarball
cd %{_builddir}/%name-%version
gzcat %SOURCE | tar xf -


%build
cd %{name}-%{version}
%virtmanager.build


%install
rm -rf $RPM_BUILD_ROOT
%virtmanager.install -d %name-%version

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

# install man page
rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


%post
%restart_fmri gconf-cache

%files
%doc -d virt-manager-%{virtmanager.version} README AUTHORS
%doc(bzip2) -d virt-manager-%{virtmanager.version} COPYING COPYING-DOCS NEWS ChangeLog
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/virt-manager
%{_libdir}/virt-manager/*
%{_libexecdir}/virt-manager-launch
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/virt-manager
%{_datadir}/virt-manager/*
%dir %attr (0755, root, bin) %{_datadir}/dbus-1
%dir %attr (0755, root, bin) %{_datadir}/dbus-1/services
%{_datadir}/dbus-1/services/virt-manager.service
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/virt-manager.desktop
%dir %attr (0755, root, other) %{_datadir}/gnome
%dir %attr (0755, root, bin) %{_datadir}/gnome/help
%dir %attr (0755, root, bin) %{_datadir}/gnome/help/virt-manager
%{_datadir}/gnome/help/virt-manager/*
%dir %attr (0755, root, bin) %{_datadir}/omf
%dir %attr (0755, root, bin) %{_datadir}/omf/virt-manager
%{_datadir}/omf/virt-manager/virt-manager-C.omf
%dir %attr(0755, root, bin) %{_mandir}
%{_mandir}/*/*


%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/virt-manager.schemas


%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

# endif for "ifnarch sparc"
%endif


%changelog
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Wed Sep 17 2008 - Henry Zhang <hua.zhang@sun.com>
- Add  %doc to %files for copyright
* Mon Apr 14 2008 - damien.carbery@sun.com
- Move '%ifnarch sparc' test above BuildRequires lines as pkgs in those lines
  are not on sparc and so build fails incorrectly.
* Thu Apr 9 2008 - hua.zhang@sun.com
- reopen the Xen dependencies since they were integrated into NV
* Fri Mar 28 2008 - hua.zhang@sun.com
- Add copyright package
* Wed Mar  19 2008 - hua.zhang@sun.com
- Add ifnarch so it only build at i386/x64 platform
* Fri Feb  15 2008 - laca@sun.com
- Add manpage
* Thu Jan  3 2008 - laca@sun.com
- use gconf-install.script instead of an inline script
* Fri Jun 22 2007 - dermot.mccluskey@sun.com
- comment out Xen-team deps until they are integrated.
* Thu Jun 21 2007 - dermot.mccluskey@sun.com
- Remove virtinst from pkg and add deps. on libvirt,
  urlgrabber and virtinst
* Tue May 22 2007 - dermot.mccluskey@sun.com
- Update %files for bumped versions
* Tue Apr 24 2007 - laca@sun.com
- s/0755/-/ in defattr so that files are not made all executable
- define l10n subpkg
* Thu Mar 08 2007 - damien.carbery@sun.com
- Clean out $RPM_BUILD_ROOT at start of the %install section.
* Mon Mar 05 2007 - dermot.mccluskey@sun.com
- Add virtinst module
* Fri Jan 12 2007 - dermot.mccluskey@sun.com
- Tidy up.
* Wed Jan 10 2007 - dermot.mccluskey@sun.com
- fixes from code review:
  handle GConf schemas properly (in new -root pkg);
  use %{_libexecdir};
  move patch 01 to linux spec file
* Tue Dec 12 2006 - damien.carbery@sun.com
- Add Build/Requires SUNWgnome-python-libs/-devel for pygtk.
* Fri Dec  8 2006 - dermot.mccluskey@sun.com
- Initial version
