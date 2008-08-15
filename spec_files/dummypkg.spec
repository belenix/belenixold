#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define		nm %(echo $PNAME)

Name:                %nm
Summary:             This is an empty package to satisfy dependencies
Version:             1.0

SUNW_BaseDir:        /
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

%prep
rm -rf %{name}-%{version}-build
mkdir %{name}-%{version}-build
if [ "x$PNAME" = "x" ]
then
	echo "The environment variable PNAME must contain the package name"
	echo ""
	exit 1
fi

%build
cd %{name}-%{version}-build

%install
cd %{name}-%{version}-build
rm -rf ${RPM_BUILD_ROOT}
mkdir ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}

%changelog
* Fri Aug 15 2008 - moinakg@belenix.org
- Initial spec.
