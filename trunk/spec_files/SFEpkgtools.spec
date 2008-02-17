#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

Name:                SFEpkgtools
Summary:             SVR4 Packaging tools
Version:             1.0
Source0:             http://dlc.sun.com/osol/install/downloads/current/install-src-m10.tar.bz2

URL:                 http://dlc.sun.com/osol/devpro/downloads/current/
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: %{name}-root

%package root
Summary:       %{summary} - / filesystem
SUNW_BaseDir:  /
%include default-depend.inc

%prep
pkginfo -q SUNWwbint
if [ $? -ne 0 ]
then
	echo "ERROR:"
	echo "The SUNWwbint package is needed for building SFEpkgtools. Download it"
	echo "from http://dlc.sun.com/osol/install/downloads/current/"
	echo ""
	exit 1
fi

pkginfo -q SUNWzoneint
if [ $? -ne 0 ]
then
	echo "ERROR:"
	echo "The SUNWzoneint package is needed for building SFEpkgtools. Download it"
	echo "from http://dlc.sun.com/osol/install/downloads/current/"
	echo ""
	exit 1
fi

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

GATE=%{name}-%{version}-build
CDIR=`pwd`
WS=`dirname ${CDIR} | nawk '{ gsub("\/", "\\\/"); print $0; }'`
cat usr/src/tools/env/developer.sh | sed "
s/GATE=.*/GATE=${GATE};    export GATE/
s/CODEMGR_WS=.*/CODEMGR_WS=${WS}\/\${GATE};    export CODEMGR_WS/" > ./developer.sh
cat << __EOF__ >> ./developer.sh
BUILD_TOOLS=/opt;                               export BUILD_TOOLS
ONBLD_TOOLS=/opt/onbld;                 export ONBLD_TOOLS
SPRO_ROOT=/opt/SUNWspro;                        export SPRO_ROOT
SUNWSPRO=/opt/SUNWspro;                 export SUNWSPRO
PATH=/usr/ccs/bin:/opt/SUNWspro/bin:/usr/bin:${PATH}
export PATH
__EOF__

cd usr/src
mv Makefile.master Makefile.master.orig
cat Makefile.master.orig | sed '
s/BUILD_TOOLS=.*/BUILD_TOOLS=    \/opt/
s/SPRO_VROOT=.*/SPRO_VROOT=    \$\(SPRO_ROOT\)/' > Makefile.master

source ../../developer.sh
./opensolaris_build.sh

%install

cd %{name}-%{version}-build
rm -rf ${RPM_BUILD_ROOT}
mkdir ${RPM_BUILD_ROOT}

cd proto/root_i386
rm -rf swmt var/svc cd0 .tmp_proto cdbuild Misc common devtools lib webstart
rm -rf sbin etc tools bin usr/openwin usr/sadm/lib/wbem usr/sadm/lib/smc usr/sadm/bin
rm -rf usr/include/admin usr/share usr/dt usr/snadm/classes usr/snadm/bin
rm -rf Tools usr/lib/install usr/lib/lu usr/lib/help usr/lib/*.a usr/lib/llib*
rm -rf usr/sadm/lib usr/sadm/install/devmap_scripts
tar cpf - * | (cd ${RPM_BUILD_ROOT}; tar xpf - )

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, sys)
%dir %attr (0755, root, bin) /usr/sadm
%dir %attr (0755, root, bin) /usr/sadm/install
%dir %attr (0755, root, bin) /usr/sadm/install/scripts
/usr/sadm/install/scripts/*
%dir %attr (0755, root, bin) /usr/sadm/install/bin
/usr/sadm/install/bin/*

%defattr (-, root, bin)
%dir %attr (0755, root, bin) /usr/include
/usr/include/*
%dir %attr (0755, root, bin) /usr/snadm
%dir %attr (0755, root, bin) /usr/snadm/lib
/usr/snadm/lib/*
%dir %attr (0755, root, bin) /usr/lib
/usr/lib/*
%dir %attr (0755, root, bin) /usr/sbin
/usr/sbin/*
%dir %attr (0755, root, bin) /usr/bin
/usr/bin/*

%files root
%dir %attr (0755, root, sys) /var
%dir %attr (0755, root, sys) /var/sadm
%dir %attr (0755, root, bin) /var/sadm/install
%dir %attr (0755, root, bin) /var/sadm/install/admin
%attr (0755, root, sys) /var/sadm/install/admin/default

%changelog
* Sun Feb 17 2008 - moinak.ghosh@sun.com
- Initial spec.
