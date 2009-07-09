#
# spec file for package SUNWperl-authen-pam
#
# includes module(s): 
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: padraig
#
%include Solaris.inc
Name:                    SUNWperl-authen-pam
Summary:                 Authen-PAM PERL module
Version:                 5.8.4
%define tarball_version 0.16
Source:                  http://www.cpan.org/modules/by-module/Authen/Authen-PAM-%{tarball_version}.tar.gz
#owner:padraig date:2006-04-10 type:bug state:upstream
Patch1:                  authen-pam-01-solaris.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
SUNW_Copyright:          %{name}.copyright

%define perl_version 5.8.4
%ifarch sparc
%define perl_dir sun4-solaris-64int
%else
%define perl_dir i86pc-solaris-64int 
%endif
%include default-depend.inc

%prep
%setup -q            -c -n %name-%version
cd Authen-PAM-%{tarball_version}
%patch1 -p1

%build
cd Authen-PAM-%{tarball_version}
autoconf
perl Makefile.PL \
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
cd Authen-PAM-%{tarball_version}
make install

rm -rf $RPM_BUILD_ROOT%{_prefix}/lib

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc -d Authen-PAM-%{tarball_version} README
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_prefix}/perl5
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_version}
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}/Authen
%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}/Authen/*
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
%dir %attr(0755, root, other) %{_datadir}/doc

%changelog
* Wed Sep 17 2008 - christian.kelly@sun.com
- Fix up pkg'ing section.
* Mon Sep 15 2008 - christian.kelly@sun.com
- Remove /usr/share/doc from %files. 
* Wed Sep 10 2006 - padraig.obriain@sun.com
- Add %doc to %files for copyright
* Thu Jul 17 2008 - damien.carbery@sun.com
- s/authen_pam_version/tarball_version/ to be consistent with other spec files.
* Tue Jan 30 2007 - damien.carbery@sun.com
- Fix typo s/Autoconf/autoconf/.
* Sun Jan 28 2007 - laca@sun.com
- update %file so that dir attributes work on both s10 and nevada
* Mon Apr 10 2006 - padraig.obriain@sun.com
- Initial spec file
