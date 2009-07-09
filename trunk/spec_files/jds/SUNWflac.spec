#
# spec file for package SUNWflac
#
# includes module(s): flac
#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: yippi
#
%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use flac_64 = flac.spec
%endif

%include base.inc
%use flac = flac.spec

Name:                    SUNWflac
Summary:                 Free Lossless Audio Codec
Version:                 %{flac.version}
Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildConflicts: SFEnasm
BuildRequires:  SUNWgnome-common-devel
BuildRequires:  SUNWogg-vorbis-devel
%if %cc_is_gcc
BuildRequires:  SFEgccruntime
%else
BuildRequires:  SUNWlibC
%endif
Requires:       SUNWogg-vorbis
Requires:       SUNWlibms
%if %cc_is_gcc
Requires:       SFEgccruntime
%else
Requires:       SUNWlibC
%endif

%package devel
Summary:      %{summary} - development files
SUNW_BaseDir: %{_basedir}
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%flac_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%base_arch
%flac.prep -d %name-%version/%base_arch

cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build
%if %cc_is_gcc
%else
export CXX="${CXX} -norunpath"
%endif

%ifarch amd64 sparcv9
#export CFLAGS_EXTRA="-L/usr/sfw/lib/%{_arch64} -R/usr/sfw/lib/%{_arch64}"
%flac_64.build -d %name-%version/%_arch64
%endif

%flac.build -d %name-%version/%base_arch

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%flac_64.install -d %name-%version/%_arch64
%endif

%flac.install -d %name-%version/%base_arch
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

%if %can_isaexec
mkdir $RPM_BUILD_ROOT%{_bindir}/%{base_isa}
mv $RPM_BUILD_ROOT%{_bindir}/flac $RPM_BUILD_ROOT%{_bindir}/%{base_isa}
mv $RPM_BUILD_ROOT%{_bindir}/metaflac $RPM_BUILD_ROOT%{_bindir}/%{base_isa}
cd $RPM_BUILD_ROOT%{_bindir}
ln -s ../lib/isaexec flac
ln -s ../lib/isaexec metaflac
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%if %can_isaexec
%{_bindir}/%{base_isa}
%endif
%hard %{_bindir}/flac
%hard %{_bindir}/metaflac
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libFLAC.so*
%dir %attr (0755, root, sys) %{_datadir}
%doc -d %{base_arch}/flac-%{flac.version} AUTHORS README
%doc(bzip2) -d %{base_arch}/flac-%{flac.version} COPYING.Xiph COPYING.GPL
%doc(bzip2) -d %{base_arch}/flac-%{flac.version} COPYING.LGPL COPYING.FDL
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/*
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif
 
%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, other) %{_datadir}/doc/flac-1.2.1
%{_datadir}/doc/flac-1.2.1/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*.pc
%endif
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%changelog
* Thu Feb 19 2009 - brian.cameron@sun.com
- Remove compiling with -xarch=sse2.  Installing sse2 code to pentium+mmx
  is problematic since pentium+mmx isn't guaranteed to support SSE2.
  So removing this optimization for now.
* Fri Sep 12 2008 - brian.cameron@sun.com
- Add new copyright files.
* Mon Mar 31 2008 - brian.cameron@sun.com
- Add SUNW_Copyright.
* Mon Mar 17 2008 - irene.huang@sun.com
- remove line for c++ files.
* Fri Mar 14 2008 - irene.huang@sun.com
- remove c++ files from the package.
* Wed Oct 10 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Wed Sep 19 2007 - damien.carbery@sun.com
- Add C++ libs to %files.
* Fri Jun 29 2007 - irene.huang@sun.com
- remove FLAC++.so.* from file list. 
* Thu Apr 26 2007 - laca@sun.com
- set CXX to $CXX -norunpath because libtool swallows this option sometimes
  and leaves compiler paths in the binaries, fixes 6497744
* Thu Apr  5 2007 - laca@sun.com
- use hard links for isaexec now that pkgbuild 1.2.0+ supports them.
* Thu Mar 15 2007 - dougs@truemail.co.th and laca@sun.com
- enable building 64-bit and SSE2 variants
* Fri Feb 16 2007 - damien.carbery@sun.com
- Add %{_libdir}/pkgconfig to %files devel.
* Wed Feb 14 2007 - laca@sun.com
- add BuildConflicts against SFEnasm as it breaks the build
* Mon Dec 04 2006 - damien.carbery@sun.com
- Remove ogg flac libraries as they are no longer built.
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Thu May 04 2006 - laca@sun.com
- merge -share pkg(s) into the base pkg(s)
* Fri Feb 17 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Tue Sep 13 2005 - brian.cameron@sun.com
- Now use flac version number.
* Fri Aug 12 2005 - balamurali.viswanathan@wipro.com
- Initial spec-file created
