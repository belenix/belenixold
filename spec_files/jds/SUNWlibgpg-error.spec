#
# spec file for package SUNWlibgpg-error
#
# includes module(s): libgpg-error
#
# Copyright (c) 2004 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jefftsai
#
%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use libgpgerror64 = libgpg-error.spec
%endif

%include base.inc
%use libgpgerror = libgpg-error.spec

Name:          SUNWlibgpg-error
Summary:       Common error codes for GnuPG, libgcrypt
Version:       %{libgpgerror.version}
SUNW_BaseDir:  %{_basedir}
SUNW_Copyright:%{name}.copyright
BuildRoot:     %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-base-libs-devel
Source1:    %{name}-manpages-0.1.tar.gz

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires:      %{name}

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
%ifarch amd64 sparcv9
mkdir -p %name-%version/%_arch64
%libgpgerror64.prep -d %name-%version/%_arch64
%endif

mkdir -p %name-%version/%base_arch
%libgpgerror.prep -d %name-%version/%base_arch

%build
%ifarch amd64 sparcv9
%libgpgerror64.build -d %name-%version/%_arch64
%endif

%libgpgerror.build -d %name-%version/%base_arch

# Expand manpages tarball
cd %{_builddir}/%name-%version
gzcat %SOURCE1 | tar xf -

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%libgpgerror64.install -d %name-%version/%_arch64
#remove this file because SUNWgnome-base-libs deliver same file
rm -f $RPM_BUILD_ROOT%{_libdir}/%_arch64/charset.alias
%endif

%libgpgerror.install -d %name-%version/%base_arch

#remove this file because SUNWgnome-base-libs deliver same file
rm -f $RPM_BUILD_ROOT%{_libdir}/charset.alias

cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files

%doc -d %{base_arch}/libgpg-error-%{libgpgerror.version} AUTHORS README
%doc(bzip2) -d %{base_arch}/libgpg-error-%{libgpgerror.version} ChangeLog
%doc(bzip2) -d %{base_arch}/libgpg-error-%{libgpgerror.version} COPYING COPYING.LIB
%doc(bzip2) -d %{base_arch}/libgpg-error-%{libgpgerror.version} NEWS
%dir %attr (0755, root, other) %{_datadir}/doc

%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%ifarch amd64 sparcv9
%{_libdir}/%{_arch64}/lib*.so*
%endif
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%{_datadir}/common-lisp

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Tue Sep 16 2007 - jeff.cai@sun.com
- Add copyright.
* Tue Oct  9 2007 - damien.carbery@sun.com
- Add Build/Requires SUNWgnome-base-libs/-devel for glib-gettextize.
* Tue Oct  2 2007 - laca@sun.com
- add l10n subpkg
* Tue Mar 27 2007 - laca@sun.com
- enable 64-bit build
* Mon Jul 19 2007 - damien.carbery@sun.com
- Remove l10n package and update %files after libgpg-error bumped to 1.5.
* Sat Jul 22 2006 - halton.huo@sun.com
- Add l10n package.
* Thu May 11 2006 - halton.huo@sun.com
- Change %defattr to (-, root, other).
* Thu May 04 2006 - laca@sun.com
- merge -share pkg(s) into the base pkg(s)
* Thu Apr 06 2006 - glynn.foster@sun.com
- Move -config file to -devel.
* Tue Apr 04 2006 - halton.huo@sun.com
- Alter remove .a/.la files part into linux spec. 
* Thu Mar 30 2006 - halton.huo@sun.com
- Remove all *.a/*.la files.
* Fri Sep 09 2005 - <laca@sun.com>
- remove unpackaged files
* Wed Aug 31 2005 - halton.huo@sun.com
- initial version created
