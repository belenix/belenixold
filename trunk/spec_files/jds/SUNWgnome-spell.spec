#
# spec file for package SUNWgnome-spell
#
# includes module(s): enchant
#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jefftsai
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use enchant_64 = enchant.spec
%endif

%include base.inc
%use enchant = enchant.spec

Name:          SUNWgnome-spell
Summary:       GNOME spell checker component
Version:       %{default_pkg_version}
SUNW_BaseDir:  %{_basedir}
SUNW_Copyright:%{name}.copyright
BuildRoot:     %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SUNWgnome-component
Requires:      SUNWglib2
Requires:      SUNWgnome-config
Requires:      SUNWgnome-libs
Requires:      SUNWiso-codes
%if %cc_is_gcc
Requires:      SFEgccruntime
%else
Requires:      SUNWlibC
%endif
Requires:      SFEaspell
BuildRequires: SUNWglib2-devel
BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-component-devel
BuildRequires: SUNWiso-codes-devel
BuildRequires: SFEaspell-devel

Source1:    %{name}-manpages-0.1.tar.gz

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
Requires:                %{name} = %{version}
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir -p %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%enchant_64.prep -d %name-%version/%_arch64
%endif

%enchant.prep -d %name-%version

mkdir %name-%version/%base_arch
%enchant.prep -d %name-%version/%base_arch

# Expand manpages tarball
cd %{_builddir}/%name-%version
gzcat %SOURCE1 | tar xf -

%build
%if %cc_is_gcc
%else
export CXX="${CXX} -norunpath"
%endif

# See http://bugzilla.abisource.com/show_bug.cgi?id=10668 for why LD is set 
# to $CXX.
export LD=$CXX
export LDFLAGS="%_ldflags"

%ifarch amd64 sparcv9
%enchant_64.build -d %name-%version/%_arch64
%endif

%enchant.build -d %name-%version/%base_arch
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export PKG_CONFIG_PATH=../enchant-%{enchant.version}:%{_pkg_config_path}

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%enchant_64.install -d %name-%version/%_arch64
rm $RPM_BUILD_ROOT%{_libdir}/%_arch64/*.la
rm $RPM_BUILD_ROOT%{_libdir}/%_arch64/enchant/*.la
%endif

%enchant.install -d %name-%version/%base_arch
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/enchant/*.la
rm $RPM_BUILD_ROOT%{_mandir}/man1/*

cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT


%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files

%doc -d enchant-%{enchant.version} AUTHORS README
%doc(bzip2) -d enchant-%{enchant.version} ChangeLog
%doc(bzip2) -d enchant-%{enchant.version} COPYING.LIB
%doc(bzip2) -d enchant-%{enchant.version} NEWS
%dir %attr (0755, root, other) %{_datadir}/doc

%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/enchant*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/enchant*
%endif
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libenchant*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/libenchant*
%endif

%dir %{_libdir}/enchant
%{_libdir}/enchant/*.so
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}/enchant
%{_libdir}/%{_arch64}/enchant/*.so
%endif

%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/enchant
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Wed Sep 17 2008 - jeff.cai@sun.com
- Add copyright.
* Tue Jul 29 2008 - jeff.cai@sun.com
- Add man page.
* Mon Jul 07 2008 - jeff.cai@sun.com
- Remove gnome-spell because Evolution doesn't depends on it.
- Add 64bit build support.
* Thu Jun 05 2008 - damien.carbery@sun.com
- Add Build/Requires SUNWiso-codes/-devel for gnome-spell.
* Wed Apr 02 2008 - jeff.cai@sun.com
- Add copyright file.
* Thu Apr 26 2007 - laca@sun.com
- set CXX to $CXX -norunpath because libtool swallows this option sometimes
  and leaves compiler paths in the binaries
* Wed Apr 4 2007 - irene.huang@sun.com
- remove enchant++.h from the package.
* Fri Mar 23 2007 - damien.carbery@sun.com
- Change %{_datadir}/control-center-2.0 perms to root:other on snv to match
  SUNWj5rt and SUNWj6rt who set the perms in their postinstall scripts.
* Thu Mar 15 2007 - damien.carbery@sun.com
- Add Requires SUNWlibC after check-deps.pl run.
* Thu Mar 08 2007 - jeff.cai@sun.com
- Remove dependency on aspell.
* Wed Feb 14 2007 - jeff.cai@sun.com
- Make gnome-spell use enchant.
* Sun Jan 28 2007 - laca@sun.com
- update %files so that dir attributes work on both s10 and nevada
* Mon Dec 11 2006 - damien.carbery@sun.com
- Set LD to $CXX so that linking to C++ libs works in enchant.
* Fri Dec 08 2006 - damien.carbery@sun.com
- Add enchant.spec module and update %files.
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Thu May 11 2006 - halton.huo@sun.com
- Merge -share pkg(s) into the base pkg(s).
* Fri Apr 21 2006 - halton.huo@sun.com.
- Add %{_libdir}/aspell to PATH,
  this is becuase aspell change, refer to LSARC/2006/231
* Mon Feb 20 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Sat Oct 30 2004 - laca@sun.com
- change version to 2.6.0 to match other GNOME pkgs
* Sat Oct 02 2004 - laca@sun.com
- added %pkgbuild_postprocess
* Thu Sep 23 2004 - damien.carbery@sun.com
- Add BuildRequires SUNWgnome-libs-devel so libgnomeui is available for 
  gnome-spell.
* Tue Jun 22 2004 - shirley.woo@sun.com
- changed install location to /usr/lib and /usr/bin
* Thu Mar 11 2004 - <laca@sun.com>
- initial version created
