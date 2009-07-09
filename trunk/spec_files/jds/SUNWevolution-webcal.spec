#
# spec file for package SUNWevolution-webcal
#
# includes module(s): exchange-webcal
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jedy
#
%include Solaris.inc
%use webcal = evolution-webcal.spec

Name:          SUNWevolution-webcal
Summary:       Webcal support for Evolution
Version:       %{default_pkg_version}
SUNW_Category: EVO25,%{default_category}
SUNW_Copyright: %{name}.copyright
SUNW_BaseDir:  %{_basedir}
BuildRoot:     %{_tmppath}/%{name}-%{version}-build
Source1:    %{name}-manpages-0.1.tar.gz
%include default-depend.inc
Requires: SUNWgtk2
Requires: SUNWevolution
Requires: SUNWlibpopt
Requires: SUNWevolution-data-server
Requires: SUNWevolution-libs
Requires: SUNWgnome-component
Requires: SUNWgnome-config
Requires: SUNWgnome-libs
Requires: %{name}-root
Requires: SUNWdesktop-cache
BuildRequires: SUNWgtk2-devel
BuildRequires: SUNWevolution-data-server-devel
BuildRequires: SUNWevolution-libs-devel
BuildRequires: SUNWgnome-component-devel
BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWlibpopt-devel

%package root
Summary:       %{summary} - / filesystem
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
mkdir -p %name-%version
%webcal.prep -d %name-%version

# Expand manpages tarball
cd %{_builddir}/%name-%version
gzcat %SOURCE1 | tar xf -

%build
export LDFLAGS="%_ldflags -L%{_libdir} -R%{_libdir}"
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
export PKG_CONFIG_PATH="%_pkg_config_path"
%webcal.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%webcal.install -d %name-%version

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rmdir $RPM_BUILD_ROOT%{_datadir} 
%endif

rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):supported" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri gconf-cache

%files
%doc -d evolution-webcal-%{webcal.version} AUTHORS
%doc(bzip2) -d evolution-webcal-%{webcal.version} ChangeLog
%doc(bzip2) -d evolution-webcal-%{webcal.version} COPYING
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libexecdir}
%{_libexecdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/evolution-webcal.schemas

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Fri Oct 10 2008 - jedy.wang@sun.com
- Ship manpage.
* Fri Sep 19 2008 - christian.kelly@sun.com
- Set permissions on /usr/share and /usr/share/doc.
* Tue Sep 16 2008 - jedy.wang@sun.com
- Add copyright files.
* Fri Aug  1 2008 - jedy.wang@sun.com
- Add the manpage.
* Thu Jan  3 2008 - laca@sun.com
- use gconf-install.script instead of an inline script
* Sat Aug 12 2006 - laca@sun.com
- delete some unnecessary env variables
* Fri Jul 14 2006 - laca@sun.com
- update %post/%postun/etc scripts to support diskless client setup,
  part of 6448317
* Thu Jun 29 2006 - laca@sun.com
- update postrun scripts
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Wed May 31 2006 - laca@sun.com
- use post/preun scripts to install schemas into the merged gconf files
* Thu May 11 2006 - halton.huo@sun.com
- Change %defattr to (-, root, other).
* Thu Apr 13 2006 - halton.huo@sun.com
- Add install schema script, fix bug #6408031.
* Thu Feb 23 2006 - damien.carbery@sun.com
- Use default pkg version to match other pkgs; add EVO25 to default category.
* Mon Feb 20 2006 - damien.carbery@sun.com
- Complete update of Build/Requires after running check-deps.pl script.
* Thu Feb 16 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Tue Sep 20 2005 - glynn.foster@sun.com
- Initial spec for SUNWevolution-webcal

