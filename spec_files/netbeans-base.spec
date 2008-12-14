#
# Copyright (c) 2008 BeleniX team
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc


Name:                netbeans-base
Summary:             Netbeans IDE with base Javase support
Version:             6.5
%define src_file     netbeans-%{version}-ml-javase-solaris-x86.sh
Source:              %src_file
%define src_url      http://services.netbeans.org/bouncer/index.php?product=netbeans-%{version}-javase&os=solaris-x86

SUNW_BaseDir:        /
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
Requires:            SUNWj6dev

%prep
if [ ! -f "%SOURCE" ]
then
	wget '%src_url' -O %SOURCE
fi

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
cp %{SOURCE} .
chmod +x ./%{src_file}

%install

cd %{name}-%{version}-build
pdir=`pwd`
rm -rf ${RPM_BUILD_ROOT}
mkdir ${RPM_BUILD_ROOT}
mkdir ${RPM_BUILD_ROOT}/opt
mkdir ${RPM_BUILD_ROOT}/opt/netbeans-%{version}
olddir=""
if [ -d ${HOME}/netbeans-%{version} ]
then
	olddir=${HOME}/netbeans-%{version}-orig
	mv ${HOME}/netbeans-%{version} $olddir
fi
ln -sf ${RPM_BUILD_ROOT}/opt/netbeans-%{version} ${HOME}/netbeans-%{version}

${pdir}/%{src_file} --silent
rm ${RPM_BUILD_ROOT}/opt/netbeans-%{version}/nb%{version}/var/license_accepted
rm ${HOME}/netbeans-%{version}
if [ -n "$olddir" ]
then
	nv $olddir ${HOME}/netbeans-%{version}
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, root)
%dir %attr (0755, root, sys) /opt
/opt/netbeans-%{version}

%changelog
* Tue Dec 09 2008 - moinakg@belenix.org
- Initial spec.
