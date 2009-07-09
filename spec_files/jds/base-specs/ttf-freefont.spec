#
# spec file for package ttf-freefont
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: dermot
#
Name:         ttf-freefont
License:      GPL
Group:        User Interface/X
Version:      20050407
Release:      54
Distribution: Java Desktop System
Vendor:	      Sun Microsystems, Inc.
Summary:      Free UCS TrueType Fonts
Source:       http://savannah.nongnu.org/download/freefont/freefont-ttf.tar.gz
URL:          http://savannah.nongnu.org/projects/freefont/
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/doc
Autoreqprov:  on
BuildArchitectures:    noarch

PreReq:       aaa_base

%ifos solaris
%define font_dir /usr/openwin/lib/X11/fonts/TrueType
%else
%define font_dir %{_prefix}/X11R6/lib/X11/fonts/truetype
%endif

%description
A set of free scalable fonts covering the ISO 10646/Unicode UCS.

%prep
%setup -q -c -n ttf-freefont


%install
install -d ${RPM_BUILD_ROOT}%{font_dir}
install sfd/*.ttf ${RPM_BUILD_ROOT}%{font_dir}

%clean
rm -rf $RPM_BUILD_ROOT

%post 
test -x /sbin/SuSEconfig && /sbin/SuSEconfig --module fonts

%postun
test -x /sbin/SuSEconfig && /sbin/SuSEconfig --module fonts

%files
%defattr(-,root,root)
%doc README AUTHORS CREDITS INSTALL ChangeLog
%{font_dir}/*.ttf

%changelog
* Fri Dec 02 2005 - damien.carbery@sun.com
- Remove %{version} from Source URL as there isn't one on website.

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
- Using version numbered copy of freefont-ttf.tar.gz as original is not version numbered.
