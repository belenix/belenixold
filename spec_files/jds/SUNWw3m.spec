#
# spec file for packages SUNWw3m
#
# includes module(s): w3m
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: yuntong.jin 
#
%include Solaris.inc

%use w3m = w3m.spec

Name:                    SUNWw3m
Summary:                 A text-based web browser
Version:                 %{default_pkg_version}
Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:            SUNWlibms
Requires:            SUNWlibgc
Requires:            SUNWperl584core
Requires:            SUNWfirefox
Requires:            SUNWopenssl-libraries
BuildRequires:       SUNWlibm 
BuildRequires:       SUNWlibgc-devel
BuildRequires:       SUNWopenssl-include

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
%w3m.prep -d %name-%version
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build
export CFLAGS="%optflags `pkg-config --cflags bdw-gc`"
export LDFLAGS="%_ldflags -L/usr/sfw/lib -R/usr/sfw/lib `pkg-config --libs bdw-gc` "
export RPM_OPT_FLAGS="$CFLAGS"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"

%w3m.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT

%w3m.install -d %name-%version

#remove man page and help file for ja
rm -rf $RPM_BUILD_ROOT%{_mandir}/ja
rm -rf $RPM_BUILD_ROOT%{_datadir}/w3m/w3mhelp-funcdesc.ja.pl

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

# install man page
rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/w3m
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/w3m/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%doc -d w3m-%{w3m.version} ChangeLog NEWS README
%dir %attr (0755, root, other) %{_datadir}/doc

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Mon Mar 30 2009 - yuntong.jin@sun.com
- change the owner to yuntong.jin
* Fri Sep 19 2008 - rick.ju@sun.com
- Add %doc for copyright files
* Thu Aug 06 2008 - rick.ju@sun.com
- fix a libm dependency issue #6733315  
* Thu Jun 05 2008 - rick.ju@sun.com
- renamed to SUNWw3m.spec 
* Wed Jun 04 2008 - takao.fujiwara@sun.com
- Add l10n packages with w3m fix.
* Mon May 26 2008 - rick.ju@sun.com
- Add openssl dependency
* Tue Apr 15 2008 - damien.carbery@sun.com
- Remove l10n package as the libgsf files were the only l10n files.
* Mon Apr 14 2008 - halton.huo@sun.com
- Move libgsf part into SUNWlibgsf. Remove -root and devel pkgs too.
* Thu Mar 27 2008 - halton.huo@sun.com
- Add copyright file
* Wed Feb 27 2008 - halton.huo@sun.com
- Remove man pages for ja
- Add Requires:{name} for -devel pkg
* Tue Feb 26 2008 - halton.huo@sun.com
- Remove Requires: SUNWpostrun, Add Requires: SUNWdesktop-search-libs-root
- Move %{_mandir}/ja into -l1n pkg
- Use gconf-install.script for %post root
* Wed Feb 20 2008 - halton.huo@sun.com
- Remove unused SOURCE0
* Tue Jan 29 2008 - damien.carbery@sun.com
- Add Build/Requires SUNWgnome-python-libs/-devel.
* Thu Jan 24 2008 - halton.huo@sun.com
- Move libgc out.
* Wed Jan 02 2008 - halton.huo@sun.com
- Initial spec-file created
