#
# spec file for package SUNWmusicbrainz
#
# includes module(s): libmusicbrainz
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: yippi
#
%include Solaris.inc
%use musicbrainz = libmusicbrainz.spec

Name:                    SUNWmusicbrainz
Summary:                 Library for accessing MusicBrainz servers
Version:                 %{musicbrainz.version}
Patch0:                  musicbrainz-2.1.4-gcc43-includes.patch
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWlexpt
Requires: SUNWlibmsr
Requires: SUNWneon
Requires: SFElibdiscid
BuildRequires: SUNWlexpt
%if %cc_is_gcc
Requires: SFEgccruntime
%else
Requires: SUNWlibC
%endif
BuildRequires: SFEcmake

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir %name-%version
%musicbrainz.prep -d %name-%version
cd %{_builddir}/%name-%version/libmusicbrainz-%{musicbrainz.version}
%patch0 -p1
cd ..

%build
export CXXFLAGS="%cxx_optflags -I/usr/gnu/include"
export LDFLAGS="%_ldflags -R/usr/gnu/lib -L/usr/gnu/lib -lstdc++"
%if %cc_is_gcc
%else
CXXFLAGS="$CXXFLAGS lCrun -lCstd -XCClinker -norunpath"
%endif
export CFLAGS="%optflags -I/usr/gnu/include"
%musicbrainz.build -d %name-%version

%install
%musicbrainz.install -d %name-%version

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libmusicbrainz*.so*
%doc -d libmusicbrainz-%{musicbrainz.version} AUTHORS README
%doc -d libmusicbrainz-%{musicbrainz.version} perl/Bundle/README
%doc -d libmusicbrainz-%{musicbrainz.version} perl/Client/README
%doc -d libmusicbrainz-%{musicbrainz.version} perl/TRM/README
%doc -d libmusicbrainz-%{musicbrainz.version} perl/Queries/README
%doc -d libmusicbrainz-%{musicbrainz.version} python/README
%doc(bzip2) -d libmusicbrainz-%{musicbrainz.version} COPYING python/COPYING
%doc(bzip2) -d libmusicbrainz-%{musicbrainz.version} ChangeLog 
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/musicbrainz

%changelog
* Mon Sep 15 2008 - brian.cameron@sun.com
- Add new copyright files.
* Mon Mar 31 2008 - brian.cameron@sun.com
- Add SUNW_Copyright
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Mon Feb 20 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Wed Jan 04 2006 - damien.carbery@sun.com
- Set LDFLAGS/CFLAGS to find expat files under /usr/sfw.
* Tue Sep 27 2005 - brian.cameron@sun.com
- Fix libmusicbrainz so it links against the Forte STL library
  since it was building with unresolved symbols before.
* Mon Jul 25 2005 - balamurali.viswanathan@wipro.com
- Create a separate devel package
* Fri Jul 08 2005 - balamurali.viswanathan@wipro.com
- Modify patch not to include -lstdc++
* Thu Jul 07 2005 - balamurali.viswanathan@wipro.com
- Initial spec-file created
