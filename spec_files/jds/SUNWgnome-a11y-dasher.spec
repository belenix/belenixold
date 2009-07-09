#
# spec file for package SUNWgnome-a11y-dasher
#
# includes module(s): dasher
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: yippi
#
%include Solaris.inc

%use dasher = dasher.spec

Name:                    SUNWgnome-a11y-dasher
Summary:                 Predictive text entry system
Version:                 %{dasher.version}
Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_prefix}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-a11y-libs-devel
BuildRequires: SUNWsfwhea
BuildRequires: SUNWgnome-a11y-speech-devel
BuildRequires: SUNWgnome-component-devel
BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWgnome-vfs-devel
BuildRequires: SUNWlibpopt-devel
Requires: SUNWlexpt
Requires: SUNWgnome-a11y-libs
Requires: SUNWgnome-a11y-speech
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-libs
Requires: SUNWgnome-component
Requires: SUNWgnome-config
Requires: SUNWgnome-vfs
Requires: SUNWlibpopt
Requires: SUNWlibC
Requires: SUNWlibms
Requires: SUNWdesktop-cache
Requires: %{name}-root

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
%dasher.prep -d %name-%version
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build
export PKG_CONFIG_PATH=%{_pkg_config_path}
export CFLAGS="%optflags -I/usr/sfw/include"
export CPPFLAGS="-I/usr/sfw/include"
export CXXFLAGS="%cxx_optflags -staticlib=stlport4"
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="%_ldflags -L/usr/sfw/lib -R/usr/sfw/lib"
%dasher.build -d %name-%version

%install
%dasher.install -d %name-%version
rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
# REMOVE l10n FILES
rm -r $RPM_BUILD_ROOT%{_datadir}/locale
%endif
rm -rf $RPM_BUILD_ROOT/var

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):supported" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri desktop-mime-cache gconf-cache

%postun
%restart_fmri desktop-mime-cache

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%{_datadir}/dasher
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help
%attr (-, root, other) %{_datadir}/icons
%doc -d dasher-%{dasher.version} AUTHORS README
%doc(bzip2) -d dasher-%{dasher.version} COPYING NEWS
%doc(bzip2) -d dasher-%{dasher.version} ChangeLog po/ChangeLog
%doc(bzip2) -d dasher-%{dasher.version} Data/Help/Gnome/ChangeLog
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, bin) %{_datadir}/man
%dir %attr (0755, root, bin) %{_datadir}/man/man1
%{_datadir}/man/man1/*
%{_datadir}/omf

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/dasher.schemas

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Fri Sep 11 2008 - brian.cameron@sun.com
- Add new copyright files.
* Wed Apr 02 2008 - brian.cameron@sun.com
- Add SUNW_Copyright
* Thu Jan  3 2008 - laca@sun.com
- use gconf-install.script instead of an inline script
* Fri Sep 28 2007 - laca@sun.com
- delete Nevada X deps
- delete some unneeded env vars
* Sat Aug 18 2007 - damien.carbery@sun.com
- Add -f to rm call to delete /var in %install.
* Wed May 16 2007 - damien.carbery@sun.com
- Set CPPFLAGS in %build so that expat.h under /usr/sfw/include can be found.
* Tue Apr 24 2007 - laca@sun.com
- s/0755/-/ in defattr so that files are not made all executable
* Thu Jan 04 2007 - damien.carbery@sun.com
- Remove '-f' from rm calls so that changes that require spec file changes are
  seen quickly.
* Wed Dec 06 2006 - damien.carbery@sun.com
- Add root package for dasher.schemas, and %post/%preun scripts to accompany
  the new package.
* Mon Aug 28 2006 - brian.cameron@sun.com
- install the NROFF manpage until we convert it to SGML.
* Sat Aug 12 2006 - laca@sun.com
- change datadir/icons permissions back to root:other since it's a stable
  interface and wasn't supposed to be changed
* Thu Jul 27 2006 - damien.carbery@sun.com
- Delete scrollkeeper files before packaging.
* Fri Jul 14 2006 - laca@sun.com
- update %post/%postun/etc scripts to support diskless client setup,
  part of 6448317
* Thu Jun 29 2006 - laca@sun.com
- update postrun scripts
* Fri Jun 23 2006 - brian.cameron@sun.com
- Remove '-library=stlport' from CXXFLAGS so it the library is not dynamically
  linked.
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Thu May 04 2006 - laca@sun.com
- merge -share pkg(s) into the base pkg(s)
* Thu Feb 23 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Tue Feb 14 2006 - damien.carbery@sun.com
- Set CXXFLAGS to find stlport4.
* Sat Dec  3 2005 - laca@sun.com
- add %post script that runs update-desktop-database
* Fri Sep 30 2005 - brian.cameron@sun.com
- Correct packaging.
* Tue Sep 20 2005 - laca@sun.com
- add /usr/sfw/ to LDFLAGS and CFLAGS
- add expat dependencies
* Tue Sep 20 2005 - glynn.foster@sun.com
- Initial SUNWgnome-a11y-dasher package
