#
# spec file for package SUNWpilot-link
#
# includes module(s): pilot-link
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#
%include Solaris.inc
%use plink = pilot-link.spec
%define libusb_prefix /usr/sfw

Name:          SUNWpilot-link
Summary:       %{plink.summary}
Version:       %{plink.version}
Source:	       %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:  %{_basedir}
SUNW_Copyright:  %{name}.copyright
BuildRoot:     %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWlibms
Requires: SUNWlibpopt
Requires: SUNWlibusb
Obsoletes:SUNWpltlk
BuildRequires: SUNWlibpopt-devel
BuildConflicts: SUNWgnome-pilot-link
BuildConflicts: SUNWgnome-pilot-link-root
BuildConflicts: SUNWgnome-pilot-link-share
BuildConflicts: SUNWgnome-pilot-link-devel
BuildConflicts: SUNWgnome-pilot-link-devel-share

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires:      %{name}

%prep
rm -rf %name-%version
mkdir -p %name-%version
%plink.prep -d %name-%version
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build
export LDFLAGS="%{?arch_ldadd} -L/usr/lib -R/usr/lib -L%{libusb_prefix}/lib -R%{libusb_prefix}/lib"
export CFLAGS="-I/usr/gnu/include %optflags -I%{libusb_prefix}/include -D_POSIX_PTHREAD_SEMANTICS"
export RPM_OPT_FLAGS="$CFLAGS"
%plink.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%plink.install -d %name-%version

# remove unused files
rm -r $RPM_BUILD_ROOT%{_datadir}/pilot-link
rm -r $RPM_BUILD_ROOT%{_mandir}/man7
cd $RPM_BUILD_ROOT%{_mandir}/man1
for i in `ls |grep -v pilot-xfer`; do rm -r $i; done
cd $RPM_BUILD_ROOT%{_bindir}
for i in `ls |grep -v pilot-xfer`; do rm -r $i; done
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*
%doc(bzip2) -d pilot-link-%{plink.version} COPYING COPYING.LIB 
%doc(bzip2) -d pilot-link-%{plink.version} NEWS ChangeLog README
%dir %attr (0755, root, other) %{_datadir}/doc

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/libpisock/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %dir %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*

%changelog
* Wed Sept 17 2008 - jijun.yu@sun.com
- Modify copyright based on new process.
* Fri Aug 1 2008 - jijun.yu@sun.com
- Add manpages.
* Mon Mar 31 2008 - jijun.yu@sun.com
- Add copyright
* Wed Nov 28 2007 - damien.carbery@sun.com
- Remove man7 files and most man1 files as they are not useful.
* Tue Nov 27 2007 - damien.carbery@sun.com
- Add manpage dirs to %files to fix build.
* Fri Nov 23 2007 - jijun.yu@sun.com
- Remove some unuseful files from the package. Remove %{_datadir}/pilot-link
  dir and all %{_bindir} files except pilot-xfer as the files are not needed.
* Tue Nov 13 2007 - jijun.yu@sun.com
- Remove some unnecessary files from the package.
* Fri Oct  5 2007 - laca@sun.com
- add /usr/gnu stuff to CFLAGS and LDFLAGS so that GNU libintl and
  libiconv are used (with --with-gnu-iconv)
* Sun Apr 30 2007 - jijun.yu@sun.com
- Remove a manpage from manpages/man1 to fix #6550823
* Mon Feb  5 2007 - damien.carbery@sun.com
- Add Requires SUNWbash after check-deps.pl run.
* Thu Nov 30 2006 - halton.huo@sun.com
- initial version created
