#
# spec file for package SUNWperl-xml-parser
#
# includes module(s): XML-Parser (Perl XML::Parser module)
#                     XML:Simple
#
# Copyright (c) 2004 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: laca
#
%include Solaris.inc
Name:                    SUNWperl-xml-parser
Summary:                 XML::Parser and XML::Simple PERL modules
Version:                 5.8.4
%define xml_parser_version 2.34
%define xml_simple_version 2.18
Source:                  http://www.cpan.org/authors/id/M/MS/MSERGEANT/XML-Parser-%{xml_parser_version}.tar.gz
Source1:                 http://search.cpan.org/CPAN/authors/id/G/GR/GRANTM/XML-Simple-%{xml_simple_version}.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
BuildRequires:           SUNWsfwhea

%define perl_version 5.8.4
%ifarch sparc
%define perl_dir sun4-solaris-64int
%else
%define perl_dir i86pc-solaris-64int 
%endif
%include default-depend.inc
Requires: SUNWlexpt
%define expat_libdir /usr/sfw/lib
%define expat_includedir /usr/sfw/include

Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc

%prep
%setup -q            -c -n %name-%version
%setup -q -D -T -b 1 -c -n %name-%version

%build
cd XML-Parser-%{xml_parser_version}
perl Makefile.PL \
    EXPATLIBPATH=%{expat_libdir} \
    EXPATINCPATH=%{expat_includedir} \
    PREFIX=$RPM_BUILD_ROOT%{_prefix} \
    INSTALLSITELIB=$RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version} \
    INSTALLSITEARCH=$RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir} \
    INSTALLSITEMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLSITEMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \
    INSTALLMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3
make CC=$CC CCCDLFLAGS="%picflags" OPTIMIZE="%optflags" LD=$CC
cd ..

cd XML-Simple-%{xml_simple_version}
perl Makefile.PL \
    EXPATLIBPATH=%{expat_libdir} \
    EXPATINCPATH=%{expat_includedir} \
    PREFIX=$RPM_BUILD_ROOT%{_prefix} \
    INSTALLSITELIB=$RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version} \
    INSTALLSITEARCH=$RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir} \
    INSTALLSITEMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLSITEMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \
    INSTALLMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3
make CC=$CC CCCDLFLAGS="%picflags" OPTIMIZE="%optflags" LD=$CC

%install
rm -rf $RPM_BUILD_ROOT
cd XML-Parser-%{xml_parser_version}
make install
cd ..

cd XML-Simple-%{xml_simple_version}
make install
cd ..

rm -rf $RPM_BUILD_ROOT%{_prefix}/lib

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_prefix}/perl5
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_version}
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_version}/XML
%{_prefix}/perl5/vendor_perl/%{perl_version}/XML/*
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}
%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}/XML
%if %is_s10
%dir %attr(0755, root, other) %{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}/auto
%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}/auto/*
%else
%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}/auto
%endif
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%changelog
* Fri Dec 21 2007 - patrick.ale@gmail.com
- Bump XML-Simple to 2.18. Source to 2.16 N/A
* Mon Mar 20 2007 - damien.carbery@sun.com
- Bump XML-Simple to 2.16. (Reported by reborg on desktop-discuss).
* Sun Jan 28 2007 - laca@sun.com
- update %files so that the attributes work on both s10 and nevada
* Wed May 10 2006 - laca@sun.com
- merge -share pkg(s) into the base pkg(s)
* Wed Feb 15 2006 - damien.carbery@sun.com
- Correct perms to match s10fcs ones.
* Fri Sep 02 2005 - laca@sun.com
- remove unpackaged files
* Wed Jul 06 2005 - laca@sun.com
- added SUNWsfwhea dependency needed for expat headers
* Sat Oct 02 2004 - laca@sun.com
- added %pkgbuild_postprocess
* Mon Aug 30 2004 - shirley.woo@sun.com
- Bug 5091588 : man3 files should be in a separate devel package
* Mon Aug 16 2004 - laca@sun.com
- Use libexpat from Solaris (SUNWlexpt)
* Thu Jul 08 2004 - damien.carbery@sun.com
- Change to support perl 5.8.4. Use %ifarch to install to different dirs.
* Tue Jun 22 2004 - shirley.woo@sun.com
- changed install location to /usr/lib and /usr/bin
* Sat Feb 28 2004 - laca@sun.com
- fix man page installation
* Mon Jan 26 2004 - Laszlo.Peter@sun.com
- initial version added to CVS
