#
# spec file for package ttf-baekmuk
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: dermot
#
Name:         ttf-baekmuk
License:      baekmuk
Group:        User Interface/X
Version:      2.1
Release:      54
Distribution: Java Desktop System
Vendor:	      Sun Microsystems, Inc.
Summary:      Korean Baekmuk Truetype Fonts
Source:       ftp://ftp.mizi.com/pub/baekmuk/baekmuk-ttf-%{version}.tar.gz
URL:          ftp://ftp.mizi.com/pub/baekmuk/
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/doc
Autoreqprov:  on
BuildArchitectures:    noarch

PreReq:		aaa_base

%ifos solaris
%define font_dir /usr/openwin/lib/X11/fonts/TrueType
%else
%define font_dir %{_prefix}/X11R6/lib/X11/fonts/truetype
%endif

%description
Baekmuk Korean TrueType Fonts

%prep
%setup -q -c -n %{name}-%{version}


%install
install -d ${RPM_BUILD_ROOT}%{font_dir}
install *.ttf ${RPM_BUILD_ROOT}%{font_dir}

%clean
rm -rf $RPM_BUILD_ROOT

%post 
test -x /sbin/SuSEconfig && /sbin/SuSEconfig --module fonts

%postun
test -x /sbin/SuSEconfig && /sbin/SuSEconfig --module fonts

%files
%defattr(-,root,root)
%{font_dir}/*.ttf

%changelog
* Wed Feb 16 2005 - dermot.mccluskey@sun.com
- prereq aaa_base
* Sat Oct 30 2004 - laca@sun.com
- test if SuSEconfig is installed before running it, fixes 4911608
* Sat May 01 2004 - laca@sun.com
- install fonts into /usr/openwin on Solaris
* Tue Feb 24 2004 - michael.twomey@sun.com
- Updated to Cinnabar.
* Thu Jul 17 2003 - michael.twomey@sun.com
- Changed to invoke SuSEconfig directly.
* Thu Jul 10 2003 - michael.twomey@sun.com
- Initial release
