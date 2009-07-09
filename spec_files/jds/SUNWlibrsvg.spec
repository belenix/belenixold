#
# spec file for package SUNWlibrsvg
#
# includes module(s): librsvg
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: padraig
#

%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use rsvg64 = librsvg.spec
%endif

%include base.inc
%use rsvg = librsvg.spec

Name:                    SUNWlibrsvg
Summary:                 SVG-format scalable graphics support library
Version:                 %{rsvg.version}
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
Source:                  %{name}-manpages-0.1.tar.gz
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires: SUNWlibcroco-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-vfs-devel
BuildRequires: SUNWgnome-print-devel
BuildRequires: SUNWlibpopt-devel
BuildRequires: SUNWfirefox-devel
Requires: SUNWgnome-base-libs
Requires: SUNWlibcroco
Requires: SUNWgnome-vfs
Requires: SUNWfontconfig
Requires: SUNWfreetype2
Requires: SUNWgnome-print
Requires: SUNWlibms
Requires: SUNWlibpopt
Requires: SUNWlxml
Requires: SUNWdesktop-cache
Requires: SUNWPython
# SFEgeckosdk provides /usr/bin/mozilla-config but not the required headers.
# SUNWfirefox-devel provides /usr/bin/firefox-config and the header files.
BuildConflicts: SFEgeckosdk

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:   SUNWgnome-base-libs-devel

%prep
rm -rf %name-%version
mkdir %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%rsvg64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%base_arch
%rsvg.prep -d %name-%version/%base_arch
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build
export EXTRA_CFLAGS="-I%{_includedir}/mps"

%ifarch amd64 sparcv9
export PKG_CONFIG_PATH=%{_libdir}/%{_arch64}/pkgconfig
%rsvg64.build -d %name-%version/%_arch64
%endif

export PKG_CONFIG_PATH=
%rsvg.build -d %name-%version/%base_arch

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%rsvg64.install -d %name-%version/%_arch64

rm -r $RPM_BUILD_ROOT%{_bindir}/%_arch64

%endif
%rsvg.install -d %name-%version/%base_arch

#Firefox has built-in support for svg
rm -rf $RPM_BUILD_ROOT%{_libdir}/mozilla
rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

# Delete gtk-doc files before packagine.
rm -rf $RPM_BUILD_ROOT%{_datadir}/gtk-doc

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri pixbuf-loaders-installer

%postun
%restart_fmri pixbuf-loaders-installer

%files
%doc(bzip2) -d %{base_arch}/librsvg-%{version} COPYING COPYING.LIB ChangeLog NEWS
%doc -d %{base_arch}/librsvg-%{version} MAINTAINERS README
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%dir %attr (0755, root, bin) %{_libdir}
%{_bindir}/*
%{_libdir}/lib*.so*
%{_libdir}/gtk-2.0
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/gtk-2.0
%{_libdir}/%{_arch64}/mozilla
%{_libdir}/%{_arch64}/lib*.so*
%endif
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*


%changelog
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Tue Mar 24 2009 - jeff.cai@sun.com
- Since /usr/lib/amd64/pkgconfig/librsvg-2.0.pc (SUNWlibrsvg-devel) requires
  /usr/lib/amd64/pkgconfig/glib-2.0.pc which is found in
  SUNWgnome-base-libs-devel, add the dependency.
- Since /usr/lib/amd64/pkgconfig/librsvg-2.0.pc (SUNWlibrsvg-devel) requires
  /usr/lib/amd64/pkgconfig/gdk-pixbuf-2.0.pc which is found in
  SUNWgnome-base-libs-devel, add the dependency.
- Since /usr/lib/amd64/pkgconfig/librsvg-2.0.pc (SUNWlibrsvg-devel) requires
  /usr/lib/amd64/pkgconfig/cairo.pc which is found in
  SUNWgnome-base-libs-devel, add the dependency.
* Mon Mar 23 2009 - jeff.cai@sun.com
- Since /usr/bin/rsvg (SUNWlibrsvg) requires /usr/bin/i86/isapython2.4 which
  is found in SUNWPython, add the dependency.
* Wed Sep 10 2008 - padraig.obriain@sun.com
- Add %doc to %files for copyright
* Fri Aug 22 2008 - dave.lin@sun.com
- exclude %{_libdir}/%{_arch64}/pkgconfig from base pkg and add it in devel pkg
* Thu Aug 21 2008 - laca@sun.com
- add 64-bit build, fixes 6723060
* Wed May 07 2008 - damien.carbery@sun.com
- Remove PERL5LIB setting as it is not necessary.
* Thu Mar 27 2008 - alvaro.lopez@sun.com
- Added Copyright file.
* Fri Sep 28 2007 - laca@sun.com
- delete Nevada X dep
* Tue Jan 09 2007 - damien.carbery@sun.com
- Add BuildConflicts SFEgeckosdk because the build fails when SFEgeckosdk is
  installed. SFEgeckosdk provides /usr/bin/mozilla-config but not the required
  headers. Added BuildRequires SUNWfirefox-devel because it provides
  /usr/bin/firefox-config and the header files.
* Mon Sep 04 2006 - Matt.Keenan@sun.com
- New Manpage tarball
* Fri Jul 14 2006 - laca@sun.com
- update %post/%postun/etc scripts to support diskless client setup,
  part of 6448317
* Sun Jun 11 2006 - laca@Sun.com
- change group from other to bin/sys
* Thu May 04 2006 - laca@sun.com
- merge -share pkg(s) into the base pkg(s)
* Thu Mar 23 2003 - shirley.woo@sun.com
- Updated package Summary description
* Mon Feb 20 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Thu Feb  9 2006 - damien.carbery@sun.com
- Delete gtk-doc files before packaging.
* Mon Jan 09 2006 - damien.carbery@sun.com
- Remove gtk-doc dir from devel-share as files no longer installed.
* Sat Dec  3 2005 - laca@sun.com
- postrunify the gdk-pixbuf.loaders stuff
* Thu Sep 13 2005 - brian.cameron@sun.com
- Now use librsvg version number.
* Thu Sep 08 2005 - brian.cameron@sun.com
- Verified builds fine on Solaris and bump to 2.11.
* Tue Sep 06 2005 - laca@sun.com
- move mozilla plugin to /usr/sfw and add to %files
- fix %post/%postun scripts
* Wed Jul 27 2005 - brian.cameron@sun.com
- Created.
