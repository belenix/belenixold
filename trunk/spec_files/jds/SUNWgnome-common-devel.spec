#
# spec file for package SUNWgnome-common-devel
#
# includes module(s): pkgconfig, intltool, gtk-doc, gnome-common
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: laca
#
%include Solaris.inc
%use pkgconfig = pkg-config.spec
%use gcommon = gnome-common.spec
%use gettext = gettext.spec
%use intltool = intltool.spec

Name:                    SUNWgnome-common-devel
Summary:                 GNOME common development tools
Version:                 %{default_pkg_version}
Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWperl584usr
Requires: SUNWperl584core
Requires: SUNWPython
Requires: SUNWlibpopt
Requires: SUNWperl-xml-parser
Requires: SUNWopenjade
Requires: SUNWgnome-xml-root
Requires: SUNWlxsl
BuildRequires: SUNWPython-devel
BuildRequires: SUNWPython25-devel
BuildRequires: SUNWlibpopt-devel

%prep
rm -rf %name-%version
mkdir %name-%version

%pkgconfig.prep -d %name-%version
%gcommon.prep -d %name-%version
%gettext.prep -d %name-%version
%intltool.prep -d %name-%version
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build
%pkgconfig.build -d %name-%version

# gnome-common required pkg-config.
export PATH=%{_builddir}/%name-%version/%{pkgconfig.name}-%{pkgconfig.version}:$PATH
export PERL=/usr/perl5/bin/perl
export LDFLAGS="%_ldflags"

cd %{_builddir}

%gcommon.build -d %name-%version
%if %cc_is_gcc
%else
export CXX="${CXX} -norunpath"
%endif
export CXXFLAGS="%{cxx_optflags}"
%gettext.build -d %name-%version
export INTLTOOL_XGETTEXT="%{_libdir}/intltool/gettext-tools/xgettext"
export INTLTOOL_MSGMERGE="%{_libdir}/intltool/gettext-tools/msgmerge"
%intltool.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT

%pkgconfig.install -d %name-%version
%gcommon.install -d %name-%version
%gettext.install -d %name-%version
%intltool.install -d %name-%version
rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

# Normally we build this package before we build scrollkeeper, but
# remove any scrollkeeper files if user happens to rebuild this
# package after scrollkeeper is already on the system.
#
rm -rf $RPM_BUILD_ROOT%{_prefix}/var

# Remove /usr/share/info/dir, it's a generated file and shared by multiple
# packages
rm -f $RPM_BUILD_ROOT%{_datadir}/info/dir

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}/*
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%{_datadir}/gnome-common
%{_datadir}/info
%{_datadir}/intltool
%{_mandir}/*/*

%changelog
* Wed Jan 07 2008 - christian.kelly@sun.com
- Moved gtk-doc out into it's own spec because of circular dependency.
* Fri Dec  5 2008 - laca@sun.com
- update files
* Tue Jul 15 2008 - damien.carbery@sun.com
- Remove pkg-config code, replacing it with %use.
* Wed Jun 18 2008 - damien.carbery@sun.com
- Add Build/Requires SUNWPython/-devel because /usr/bin/gtkdoc-depscan is a
  python script.
* Mon Jan 31 2008 - brian.cameron@sun.com
- Bump pkg-config to 0.23.
* Mon Dec 10 2007 - brian.cameron@sun.com
- Bump pkg-config to 0.22.
* Fri Feb 16 2007 - damien.carbery@sun.com
- Update %files because gtk-doc xml files moved from %{_datadir}/gnome/help to
  %{_datadir}/doc with the bumping of gtk-doc to 1.8.
* Thu Jan 11 2007 - damien.carbery@sun.com
- Bump pkg-config to 0.21. Remove upstream patch, pkgconfig-01-wall.diff.
  Rename rest.
* Fri Sep 15 2006 - Brian.Cameron@sun.com
- Install gtk-doc documentation and call pkg-config configure script with
  --mandir set properly.
* Fri Sep 01 2006 - Matt.Keenan@sun.com
- New Manpage tarball
* Sat Aug 12 2006 - laca@sun.com
- set PERL to /usr/perl5/bin/perl as per CR6454456
* Fri Jun 23 2006 - christopher.hanna@sun.com
- removed man page intltool-unicodify
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Wed May 10 2006 - laca@sun.com
- merge -share pkg(s) into the base pkg(s)
* Tue May 02 2006 - damien.carbery@sun.com
- Remove gnome and omf dirs from share package as they are no longer installed.
- Remove 'rm -rf $RPM_BUILD_ROOT' as pkg-config already installed.
* Tue Apr 11 2006 - damien.carbery@sun.com
- Set ACLOCAL_FLAGS for gtk-doc to find a pkgconfig macro. Move pkgconfig dir.
* Sun Feb 19 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Thu Jan 19 2006 - damien.carbery@sun.com
- Bump pkg-config to 0.20.0, remove upstream patch (01-pkg.m4), add new patch
  (01-wall, bug #4888).
* Tue Sep 13 2005 - brian.cameron@sun.com
- Bump version to 2.12.
* Thu Sep 08 2005 - brian.cameron@sun.com
- Verified builds fine on Solaris, bump to 2.11.
* Fri Sep 02 2005 - laca@sun.com
- remove unpackaged files; fix to build with new pkgbuild
* Wed Jul 07 2005 - laca@sun.com
- backport pkg.m4 fix from 0.17.2
* Wed Jul 06 2005 - laca@sun.com
- downgrade pkgconfig to 0.16.0
* Thu Oct 21 2004 - laca@sun.com
- set PERL, fixes 5100958
* Sat Oct 02 2004 - laca@sun.com
- added %pkgbuild_postprocess
* Mon Aug 23 2004 - laca@sun.com
- s/SUNWpl5u/SUNWperl584usr/
* Sat Jun 26 2004  shirley.woo@sun.com
- Changed install location to /usr/...
* Thu May 27 2004 - laca@sun.com
- added %_libdir/pkgconfig
* Wed May 19 2004 - brian.cameron@sun.com
- Added missing man pages.
* Wed Mar 24 2004 - brian.cameron@sun.com
- Added SGML man page integration
* Mon Mar 02 2004 - Laszlo.Peter@sun.com
- add dependency on SUNWlxsl (libxslt)
* Mon Jan 26 2004 - Laszlo.Peter@sun.com
- initial version added to CVS
