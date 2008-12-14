#
# Copyright (c) 2008 BeleniX team
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc


Name:                netbeans-php
Summary:             Netbeans PHP Module
Version:             6.5
Source:              http://dlc.sun.com.edgesuite.net/netbeans/6.5/final/zip/moduleclusters/netbeans-6.5-200811100001-ml-php.zip

SUNW_BaseDir:        /
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
Requires:            SUNWj6dev
Requires:            netbeans-base

%prep
rm -rf %{name}-%{version}-build
mkdir %{name}-%{version}-build
cd %{name}-%{version}-build

%build

uid=`/usr/bin/id -u`
if [ $uid -eq 0 ]
then
	echo "ERROR: This spec file cannot be built as root user"
	exit 1
fi

cd %{name}-%{version}-build
unzip %{SOURCE} 

%install

cd %{name}-%{version}-build
pdir=`pwd`
rm -rf ${RPM_BUILD_ROOT}
mkdir ${RPM_BUILD_ROOT}
mkdir ${RPM_BUILD_ROOT}/opt
mkdir ${RPM_BUILD_ROOT}/opt/netbeans-%{version}
find . | cpio -pdumv ${RPM_BUILD_ROOT}/opt/netbeans-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, root)
%dir %attr (0755, root, sys) /opt
/opt/netbeans-%{version}

%changelog
* Tue Dec 09 2008 - moinakg@belenix.org
- Initial spec.
