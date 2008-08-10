#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Spec file for automated packaging of zyd driver
#

%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

Name:                SFEzyd
Summary:             Driver for ZyDAS ZD1211 chipsets based wireless 802.11g devices.
Version:             0.1
Source:              http://www.opensolaris.org/os/community/laptop/downloads/zyd-0.1-src.tar.gz

URL:                 http://www.opensolaris.org/os/community/laptop/wireless/zyd/
SUNW_BaseDir:        /
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include core-depend.inc

%prep
%setup -q -c -n %name-%version

%ifarch amd64
cp -rp zyd-%version zyd-%{version}-64
%endif

%build

if [ "x$ON_WS" = "x" ]
then
	echo "Please set ON_WS environment variable to point to the ON workspace"
	echo ""
	exit 1
fi

%ifarch amd64
cd zyd-%{version}-64/src
cat Makefile | sed 's/GATE= \/usr\/src\/onnv-gate/GATE= \${ON_WS}/' | sed 's/ISA=i386/ISA=amd64/' > Makefile.new
mv Makefile.new Makefile

gmake all
cd ../..
%endif

cd zyd-%{version}/src
cat Makefile | sed 's/GATE= \/usr\/src\/onnv-gate/GATE= \${ON_WS}/' > Makefile.new
mv Makefile.new Makefile

gmake all
cd ../..


%install
rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/doc
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/doc/zyd
mkdir -p ${RPM_BUILD_ROOT}/kernel/drv

cd zyd-%{version}/src
cp zyd ${RPM_BUILD_ROOT}/kernel/drv
chmod 0755 ${RPM_BUILD_ROOT}/kernel/drv/zyd

cd ../doc
cp * ${RPM_BUILD_ROOT}%{_datadir}/doc/zyd
cp ../LICENSE ${RPM_BUILD_ROOT}%{_datadir}/doc/zyd
cd ../..

%ifarch amd64
mkdir -p ${RPM_BUILD_ROOT}/kernel/drv/%{_arch64}

cd zyd-%{version}-64/src
cp zyd ${RPM_BUILD_ROOT}/kernel/drv/%{_arch64}
chmod 0755 ${RPM_BUILD_ROOT}/kernel/drv/%{_arch64}/zyd
cd ../..
%endif


%clean
rm -rf $RPM_BUILD_ROOT

%post
BASEDIR=${BASEDIR:=/}
add_drv -b $BASEDIR -n -i '"usbace,1211"' zyd

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%defattr (-, root, sys)
%dir %attr (0755, root, sys) /kernel
%dir %attr (0755, root, sys) /kernel/drv
/kernel/drv/zyd
%dir %attr (0755, root, sys) /kernel/drv/%{_arch64}
/kernel/drv/%{_arch64}/zyd

%changelog
* Sun Aug 10 2008 - moinakg@belenix.org
- Initial spec.
