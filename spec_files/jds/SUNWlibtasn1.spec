#
# spec file for package SUNWlibtasn1
#
# includes module(s): libtasn1
#
# Owner: jefftsai
%include Solaris.inc

%include base.inc
%use libtasn1 = libtasn1.spec

Name:                SUNWlibtasn1
Summary:             Tiny ASN.1 library
Version:             %{libtasn1.version}
SUNW_BaseDir:        %{_prefix}
SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWlibC

Source1:	%{name}-manpages-0.1.tar.gz

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir -p %name-%version

%libtasn1.prep -d %name-%version

# Expand manpages tarball
cd %{_builddir}/%name-%version
gzcat %SOURCE1 | tar xf -

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"

%libtasn1.build -d %name-%version/

%install
rm -rf $RPM_BUILD_ROOT
%libtasn1.install -d %name-%version/

rm -rf $RPM_BUILD_ROOT/%{_bindir}/asn1*
rm -rf $RPM_BUILD_ROOT%{_datadir}/info
rm -rf $RPM_BUILD_ROOT/usr/local
rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT

%files

%doc -d libtasn1-%{libtasn1.version} AUTHORS README
%doc(bzip2) -d libtasn1-%{libtasn1.version} ChangeLog
%doc(bzip2) -d libtasn1-%{libtasn1.version} COPYING.LIB 
%doc(bzip2) -d libtasn1-%{libtasn1.version} NEWS
%dir %attr (0755, root, other) %{_datadir}/doc

%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%files devel
%defattr (-, root, bin)
%{_bindir}
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Wed Feb 25 2009 - jeff.cai@sun.com
- Add defattr in the 'file' section
* Thu Feb 19 2009 - jeff.cai@sun.com
- Ship man page of libtasn1-config since it 
  comes back again.
- Move libtasn1-config to the devel package
* Thu Oct 13 2008 - jeff.cai@sun.com
- Remove /usr/share/aclocal since it doesn't
  ship libtasn1.pc.
- Remove /usr/share/man/man1 since it doesn't
  ship libtasn1-config.1
* Wed Sep 16 2008 - jeff.cai@sun.com
- Add copyright.
* Thu Jul 31 2008 - jeff.cai@sun.com
- Add man page for libtasn1-config
* Tue Jun 17 2008 - jeff.cai@sun.com
- Remove 64bits stuff. Change it according to laca.
* Tue Jun 17 2008 - jeff.cai@sun.com
- Ship libtasn1-config.
* Mon Jun 16 2008 - jeff.cai@sun.com
- Add man page.
* Mon Jun 16 2008 - jeff.cai@sun.com
- Move spec files from SFE.
* Wed May 28 2008 - jeff.cai@sun.com
- Split to two spec files
* Fri Jul 27 2007 - dougs@truemail.co.th
- Initial spec
