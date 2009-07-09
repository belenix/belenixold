#
# spec file for package SunDesktopVersion
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: davelam
#
%define product Sun Java Desktop System
%define productAbbrv Java_DS
%define prodRelMajor 4
%define prodRelMinor 0
%define prodBuild 113
%define buildType devel
%define assembled %(date +"%d %b %Y")

Name:         		SunDesktopVersion
License:      		GPL
Group:        		Development/Tools
BuildArchitectures:     noarch
Version:      		%prodRelMajor.%prodRelMinor.%prodBuild
Release:      		%prodBuild
Distribution: 		Java Desktop System
Vendor:       		Sun Microsystems, Inc.
Summary:      		Release info for Sun Java Desktop
URL:          		http://www.sun.com
BuildRoot:    		%{_tmppath}/%{name}-%{version}-build
Autoreqprov:            no 

%description
Release info for Sun Java Desktop

%prep
mkdir -p %name-%version

%build
echo "product=%product" > product-info
echo "productAbbrv=%productAbbrv" >> product-info
if [ "x%prodRelMinor" != x0 ]; then
	echo "release=%prodRelMajor.%prodRelMinor" >> product-info
else
	echo "release=%prodRelMajor" >> product-info
fi
echo "build=%prodBuild" >> product-info
echo "buildType=%buildType" >> product-info
echo "assembled=%assembled" >> product-info

if [ "x%prodRelMinor" != x0 ]; then
	echo "Sun Java Desktop System, Release %prodRelMajor.%prodRelMinor - build %prodBuild" > sun-release
else
	echo "Sun Java Desktop System, Release %prodRelMajor - build %prodBuild" > sun-release
fi
echo "Assembled %assembled" >> sun-release

%install
install -d ${RPM_BUILD_ROOT}/etc
install --mode=0644 sun-release ${RPM_BUILD_ROOT}/etc/sun-release
install --mode=0644 product-info ${RPM_BUILD_ROOT}/etc/product-info

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/etc/sun-release
/etc/product-info

%changelog
* Wed Mar 11 2009 - dave.lin@sun.com
- Took the ownership of this spec file.
* Fri Jun 03 2005 - laca@sun.com
- changed to generate file contents on-the-fly instead of using a static tarball
