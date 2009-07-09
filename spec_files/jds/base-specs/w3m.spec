#
# spec file for package w3m
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jerrytan
#

Name:			w3m
License:		BSD
Group:			Applications/Internet
Version:		0.5.2
Release:	 	4
Distribution:		Java Desktop System
Vendor:			Sun Microsystems, Inc.
Summary:		A text-based web browser
Source:			http://dl.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
%if %build_l10n
Source1:		l10n-configure.sh
%endif
# date:2008-06-04 owner:fujiwara type:bug bugster:6710470
Patch1:			w3m-01-build.diff
# date:2009-02-16 owner:jerrytan type:branding
Patch2:			w3m-02-checkgc.diff
URL:			http://w3m.sourceforge.net/
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
Docdir:			%{_defaultdocdir}/doc
Autoreqprov:		on
Prereq:                 /sbin/ldconfig

BuildPreReq: openssl-devel >= 0.9.8a, ncurses-devel
BuildPreReq: gdk-pixbuf-devel >= 0.16.0
BuildPreReq: libpng-devel >= 1.2.2, gc-devel

%define openssl_version 0.9.8a
BuildRequires: openssl-devel >= %{openssl_version}

%description
W3m is a pager adapted to World Wide Web. W3m is a text-based WWW
browser as well as a pager.

%prep
%setup -q
%patch1 -p1
%patch2 -p1

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

intltoolize -c -f --automake

%if %build_l10n
bash -x %SOURCE1 --enable-copyright
%endif

# the orignal aclocal.m4 defines AC_W3M_SSL_DIGEST_AUTH
mv aclocal.m4 ssl.m4
aclocal -I .
autoconf
CFLAGS="$RPM_OPT_FLAGS"			\
./configure --prefix=%{_prefix}         \
            --mandir=%{_mandir}         \
            --libdir=%{_libdir}         \
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --with-browser=/usr/bin/firefox \

touch po/stamp-it
#FIXME: If the simultaneously running job > 2, it builds failed
#make -j $CPUS
make -j 2

%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%files
%defattr(-, root, root)
%doc Bonus ChangeLog NEWS README TODO doc doc-jp
%{_sysconfdir}/w3m
%{_bindir}/w3m
%dir %{_libexecdir}/w3m
%{_libexecdir}/w3m/inflate
%dir %{_libexecdir}/w3m/cgi-bin
%{_libexecdir}/w3m/cgi-bin/w3mbookmark
%{_libexecdir}/w3m/cgi-bin/w3mhelperpanel
%{_mandir}/man1/w3m.1*
%{_mandir}/ja/man1/w3m.1*
%{_datadir}/locale/*/*/*
%{_datadir}/w3m/w3mhelp-funcdesc.en.pl
%{_datadir}/w3m/w3mhelp-funcdesc.ja.pl
%{_datadir}/w3m/w3mhelp-funcname.pl
%{_datadir}/w3m/w3mhelp.html

%changelog
* Fri Sep 05 2008 - dave.lin@sun.com
- commented out the line "make -j $CPU" and specified the simultaneously running job as 2, 
  it built failed when the job is 16
* Wed Jun 04 2008 - takao.fujiwara@sun.com
- Add w3m-01-build.diff to enable nls.
* Mon May 26 2008 - rick.ju@sun.com
- Add openssl dependency
* Mon Apr 14 2008 - halton.huo@sun.com
- Remove %gtk_doc_option when configure because there is no this option.
* Thu Feb 21 2008 - laca@sun.com
- delete all autotoolization, particularly intltoolize,
  since intltool is not used at all in this module
* Wed Feb 20 2008 - halton.huo@sun.com
- Remove commented lines.
* Wed Jan 02 2008 - halton.huo@sun.com
- spilit from SFEw3m.spec
