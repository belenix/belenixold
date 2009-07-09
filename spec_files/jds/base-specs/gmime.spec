#
# spec file for package gmime
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jerrytan
#

Name:			gmime
License:		LGPL v2.1
Group:			System/Libraries
# DO NOT BUMP TO 2.3.x until tracker supports it - check with Jerry.Tan@sun.com
Version:		2.2.22
Release:	 	4
Distribution:		Java Desktop System
Vendor:			Sun Microsystems, Inc.
Summary:		Libraries and binaries to parse and index mail messages
Source:			http://download.gnome.org/sources/gmime/2.2/%{name}-%{version}.tar.bz2
URL:			http://spruce.sourceforge.net/gmime/
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
Docdir:			%{_defaultdocdir}/doc
Autoreqprov:		on
Prereq:                 /sbin/ldconfig

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  glib2-devel >= 1:2.12.1
BuildRequires:  gtk-doc >= 1.0
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  zlib-devel

%description
This library allows you to manipulate MIME messages.

%package devel
Summary:		Header files for developing applications with libgmime 
Group:			Development/Libraries
Requires:		%{name} = %{version}
Requires:		glib2-devel >= 1:2.11.4
Requires:               gtk-doc-common
Requires:               zlib-devel

%description devel
Header files develop libgmime applications.


%prep
%setup -q

%build
%ifos linux
if [ -x /usr/bin/getconf ]; then
  CPUS=`getconf _NPROCESSORS_ONLN`
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f
autoconf

CFLAGS="$RPM_OPT_FLAGS"			\
./configure --prefix=%{_prefix}         \
            --mandir=%{_mandir}         \
            --libdir=%{_libdir}         \
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
	    %gtk_doc_option

make -j $CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog README TODO
%attr(755,root,root) %{_libdir}/libgmime-2.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgmime-2.0.so.2

%files devel
%defattr(-,root,root)
%doc PORTING
%attr(755,root,root) %{_bindir}/gmime-config
%attr(755,root,root) %{_libdir}/libgmime-2.0.so
%attr(755,root,root) %{_libdir}/gmimeConf.sh
%{_libdir}/pkgconfig/gmime-2.0.pc
%{_includedir}/gmime-2.0
%{_datadir}/gtk-doc/html/gmime



%changelog
* Mon Jul 21 2008 - damien.carbery@sun.com
- Bump to 2.2.22.
* Fri Jun 06 2008 - damien.carbery@sun.com
- Revert to 2.2.21 as tracker does not yet support 2.3.x.
* Tue Jun 03 2008 - jerry.tan@sun.com
- Bump to 2.3.1.
* Fri May 30 2008 - jerry.tan@sun.com
- Bump to 2.3.0.
* Mon May 26 2008 - damien.carbery@sun.com
- Bump to 2.2.21. Remove upstream patch, 01-bitregion-crash.
* Sun May 04 2008 - halton.huo@sun.com
- Bump to 2.2.19
* Thu Apr 30 2008 - rick.ju@sun.com
- fix 6689345
* Thu Mar 27 2008 - damien.carbery@sun.com
- Bump to 2.2.18.
* Tue Feb 12 2008 - damien.carbery@sun.com
- Bump to 2.2.17.
* Sun Feb 03 2008 - halton.huo@sun.com
- Bump to 2.2.16.
* Tue 29 Jan 2008 - patrick.ale@gmail
- Revert change since this is not correct.
* Sun 27 Jan 2008 - patrick.ale@gmail.com
- Revert change and remove /usr/share from
  build area
* Sat 26 Jan 2008 - patrick.ale@gmail.com
- Add /usr/share to the prototype
* Thu Jan 24 2008 - halton.huo@sun.com
- Remove mono stuff.
* Thu Jan 03 2008 - halton.huo@sun.com
- Bump to 2.2.15
* Wed Jan 02 2008 - halton.huo@sun.com
- spilit from SUNWgmime.spec
