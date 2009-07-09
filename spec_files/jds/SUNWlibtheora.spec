#
# spec file for package SUNWlibtheora
#
# includes module(s): libtheora 
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jerrytan
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use theora64 = libtheora.spec
%endif

%include base.inc
%use theora = libtheora.spec

Name:                    SUNWlibtheora
Summary:                 Theora video compression codec
Version:                 %{theora.version}
Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Autoreqprov: on
                                                                                
%include default-depend.inc
BuildRequires: SUNWgnome-common-devel
BuildRequires: SUNWogg-vorbis-devel
Requires: SUNWogg-vorbis

%package devel
Summary:      %{summary} - development files
SUNW_BaseDir: %{_basedir}
%include default-depend.inc

%prep
rm -rf %name-%version
%ifarch amd64 sparcv9
mkdir -p %name-%version/%_arch64
%theora64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%theora.prep -d %name-%version/%{base_arch}
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build
export ACLOCAL_FLAGS="-I /usr/share/aclocal"

%ifarch amd64 sparcv9
%theora64.build -d %name-%version/%_arch64
%endif

%theora.build -d %name-%version/%{base_arch}

%install
%ifarch amd64 sparcv9
%theora64.install -d %name-%version/%_arch64
%endif

%theora.install -d %name-%version/%{base_arch}
rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

chmod 755 $RPM_BUILD_ROOT%{_mandir}/man3/*.3

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif
%dir %attr (0755, root, sys) %{_datadir}
%doc -d %{base_arch}/libtheora-%{theora.tarball_version} AUTHORS README
%doc(bzip2) -d %{base_arch}/libtheora-%{theora.tarball_version} COPYING CHANGES
%dir %attr (0755, root, other) %{_datadir}/doc
 
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
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, other) %{_datadir}/doc/libtheora-1.0
%{_datadir}/doc/libtheora-1.0/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%changelog
* Fri Sep 12 2008 - brian.cameron@sun.com
- Add new copyright files.
* Wed Apr 02 2008 - brian.cameron@sun.com
- Add SUNW_Copyright.
* Sun Jun 11 2006 - laca@Sun.com
- change group from other to bin/sys
* Tue Sep 13 2005 - brian.cameron@sun.com
- Now use theora version number.
* Tue Jul 26 2005 - balamurali.viswanathan@wipro.com
- Add ogg and vorbis dependency
* Tue Jul 26 2005 - balamurali.viswanathan@wipro.com
- Initial spec-file created
