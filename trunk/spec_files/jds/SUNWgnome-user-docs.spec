#
# spec file for package SUNWgnome-user-docs
#
# includes module(s): gnome-user-docs
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: davelam
#
%include Solaris.inc

%use gud = gnome-user-docs.spec

Name:                    SUNWgnome-user-docs
Summary:                 GNOME user documentation
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWlxml-python
Requires: SUNWgnome-help-viewer

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
%gud.prep -d %name-%version

%build
export PKG_CONFIG_PATH=%{_pkg_config_path}
export MSGFMT="/usr/bin/msgfmt"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export LDFLAGS="%_ldflags"
export CFLAGS="%optflags"
%gud.build -d %name-%version

%install
%gud.install -d %name-%version

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/[a-z]*
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z][a-z].omf
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z][a-z]_[A-Z]*.omf
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

# Remove scrollkeeper files before packaging.
rm -rf $RPM_BUILD_ROOT/var

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%doc -d gnome-user-docs-%{gud.version} README AUTHORS
%doc(bzip2) -d gnome-user-docs-%{gud.version} COPYING COPYING-DOCS
%doc(bzip2) -d gnome-user-docs-%{gud.version} NEWS ChangeLog
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/*/C
%{_datadir}/omf/*/*-C.omf

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/*/[a-z]*
%{_datadir}/omf/*/*-[a-z][a-z].omf
%{_datadir}/omf/*/*-[a-z][a-z]_[A-Z]*.omf
%endif


%changelog
* Fri Apr  3 2009 - laca@sun.com
- stop using postrun
* Wed Mar 11 2009 - dave.lin@sun.com
- Took the ownership of this spec file.
* Fri Sep 19 2008 - halton.huo@sun.com
- Add %doc part to %files
* Thu Apr 03 2008 - damien.carbery@sun.com
- Add SUNW_Copyright.
* Tue Jul 10 2007 - damien.carbery@sun.com
- Add BuildRequires SUNWlxml-python.
* Wed Aug 16 2006 - damien.carbery@sun.com
- Add %files entry to pick up pt_BR and zh_CN omf files.
* Fri Jul 14 2006 - laca@sun.com
- update %post/%postun/etc scripts to support diskless client setup,
  part of 6448317
* Thu Jun 29 2006 - laca@sun.com
- update postrun scripts
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Wed Mar 22 2006 - damien.carbery@sun.com
- Uncomment removal of l10n files when not doing l10n build.
* Tue Mar 14 2006 - damien.carbery@sun.com
- Uncomment l10n files to pick up 'it' files.
* Tue Feb 21 2006 - damien.carbery@sun.com
- Delete scrollkeeper files before packaging.
* Tue Nov 29 2005 - laca@sun.com
- remove javahelp stuff
* Fri Sep 30 2005  damien.carbery@sun.com
- Remove obsolete javahelp references.
* Thu Sep 30 2004  shirley.woo@sun.com
- Fixed dependencies lies for base package
* Wed Aug 25 2004  Kazuhiko.Maekawa@sun.com
- Updated files to extracted only l10n content
* Tue Aug 24 2004  laca@sun.com
- separated l10n content into l10n subpkg
* Thu Aug 19 2004  damien.carbery@sun.com
- Remove xml perms change - done in base spec file.
* Wed Aug 18 2004  damien.carbery@sun.com
- Change xml perms for Solaris integration.
* Sat Jun 26 2004  shirley.woo@sun.com
- Changed install location to /usr/...
