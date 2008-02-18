#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

Name:                SUNWmlib
Summary:             mediaLib - Shared Libraries
Version:             5.11
Source:             http://dlc.sun.com/osol/devpro/downloads/current/devpro-mlib-src-20071106.tar.bz2

URL:                 http://dlc.sun.com/osol/devpro/downloads/current/
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package -n SUNWmlibh
Summary:       mediaLib - Header files
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc

%prep
rm -rf %{name}-%{version}-build
mkdir %{name}-%{version}-build

cd %{name}-%{version}-build
bunzip2 -c %{SOURCE} | tar xpf -

%build
cd %{name}-%{version}-build

if [ "x`basename $CC`" = xgcc ]
then
	%error This spec file requires SUN Studio, set the CC and CXX env variables
fi

export PATH=/usr/ccs/bin:/usr/bin:/usr/sbin:${PATH}
export MLIB_CCHOME=/opt/SS12/SUNWspro
cd usr/src/mlib/build/solaris
./build_mlib.sh

%install

cd %{name}-%{version}-build
rm -rf ${RPM_BUILD_ROOT}
mkdir ${RPM_BUILD_ROOT}

cd usr/src/mlib/dist/x86
tar cpf - * | (cd ${RPM_BUILD_ROOT}; tar xpf - )

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%files -n SUNWmlibh
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Sun Feb 10 2008 - moinak.ghosh@sun.com
- Initial spec.
