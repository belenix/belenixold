#
# spec file for package SUNWspeex
#
# includes module(s): speex 
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: yippi
#
%include Solaris.inc
%use speex = speex.spec

Name:                    SUNWspeex
Summary:                 Open Source speech codec
Version:                 %{speex.version}
Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Autoreqprov:             on
                                                                                
%include default-depend.inc
BuildRequires: SUNWgnome-common-devel
BuildRequires: SUNWogg-vorbis-devel
Requires: SUNWogg-vorbis
Requires: SUNWlibms

%package devel
Summary:      %{summary} - development files
SUNW_BaseDir: %{_basedir}
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir %name-%version
%speex.prep -d %name-%version
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build
export LDFLAGS="%_ldflags"
export CFLAGS="%optflags"
%speex.build -d %name-%version
                                                                                
%install
%speex.install -d %name-%version
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

chmod 755 $RPM_BUILD_ROOT%{_mandir}/man3/*.3
                                                                                
%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libspeex*.so*
%dir %attr (0755, root, sys) %{_datadir}
%doc -d speex-%{speex.tarball_version} AUTHORS README
%doc(bzip2) -d speex-%{speex.tarball_version} COPYING NEWS
%doc(bzip2) -d speex-%{speex.tarball_version} ChangeLog
%dir %attr (0755, root, other) %{_datadir}/doc
 
%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, other) %{_datadir}/doc/speex
%{_datadir}/doc/speex/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%files
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%changelog
* Fri Sep 12 2008 - brian.cameron@sun.com
- Add new copyright files.
* Mon Mar 31 2008 - brian.cameron@sun.com
- Add SUNW_Copyright.
* Thu May 04 2006 - laca@sun.com
- merge -share pkg(s) into the base pkg(s)
* Fri Feb 17 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Tue Sep 13 2005 - brian.cameron@sun.com
- Now use speex version number.
* Wed Jul 27 2005 - balamurali.viswanathan@wipro.com
- Add dependency of SUNWogg-vorbis
* Tue Jul 26 2005 - balamurali.viswanathan@wipro.com
- Initial spec-file created
