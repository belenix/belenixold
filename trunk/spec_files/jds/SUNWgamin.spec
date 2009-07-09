#
# spec file for package SUNWgamin, SUNWgamin-devel
#
# includes module(s): gamin
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: lin
#

%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use gamin64 = gamin.spec
%endif

%include base.inc
%use gamin = gamin.spec

Name:			SUNWgamin
Summary:		%{gamin.summary}
Version:		%{gamin.version}
SUNW_Copyright:		%{name}.copyright
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
Source:			%{name}-manpages-0.1.tar.gz
%include default-depend.inc
Requires:      SUNWgnome-base-libs
BuildRequires: SUNWgnome-base-libs-devel

%package devel
Summary:		%{summary} - developer files
Group:			Development/Libraries
SUNW_BaseDir:		%{_basedir}
Requires:		%{name}

%prep
rm -rf %name-%version
mkdir %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64

%gamin64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%base_arch
%gamin.prep -d %name-%version/%base_arch
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build
%ifarch amd64 sparcv9
%gamin64.build -d %name-%version/%_arch64
%endif

%gamin.build -d %name-%version/%base_arch

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%gamin64.install -d %name-%version/%_arch64
%endif

%gamin.install -d %name-%version/%base_arch
rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

# move python stuff to vendor-packages
(
  cd $RPM_BUILD_ROOT%{_libdir}/python*
  mv site-packages vendor-packages
  rm vendor-packages/*.la
)

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc -d %{base_arch}/gamin-%{gamin.version} README AUTHORS
%doc(bzip2) -d %{base_arch}/gamin-%{gamin.version} ChangeLog NEWS COPYING
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libexecdir}/gam_server
%{_libdir}/python2.4/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%{_libdir}/%{_arch64}/python2.4/*
%{_libexecdir}/%{_arch64}/gam_server
%endif

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%files devel
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*.pc
%endif

%changelog
* Wed Sep 18 2008 - lin.ma@sun.com
- Update copyright
* Tue May 27 2008 - damien.carbery@sun.com
- Add %dir %attr for %{_datadir}.
* Mon May 26 2008 - lin.ma@sun.com
- CR#6683160, added manpages.
* Sat Oct 13 2007 - lin.ma@sun.com
- Initial FEN backend
* Sun Apr 15 2007 - dougs@truemail.co.th
- Initial version
