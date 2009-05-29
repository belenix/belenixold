#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:				apcupsd
URL:				http://www.apcupsd.org
Summary:			A daemon for controlling APC UPSes
Version:			3.14.5
Source:				%{sf_download}/%{name}/%{name}-%{version}.tar.gz
License:			GPLv2
Distribution:		        BeleniX
Vendor:				OpenSolaris Community
Source1:			apcupsd.manifest.xml
Patch1:				apcupsd-01-constness.patch
Patch2:				apcupsd-02-noinitd.patch
Patch3:				apcupsd-03-makedepend.patch
SUNW_BaseDir:		/
SUNW_Copyright:		%{name}.copyright
BuildRoot:			%{_tmppath}/%{name}-%{version}-build

BuildRequires: SUNWsfwhea

%prep
%setup -q -n %{name}-%{version}
%patch1 -p1
%patch2 -p1
%if %cc_is_gcc
%else
%patch3 -p1
%endif

%build
# Test without parallelizing the compilation.
#CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
#if test "x$CPUS" = "x" -o $CPUS = 0; then
#     CPUS=1
#fi

CPUS=1

export CFLAGS="%optflags -I$(pwd)/include"
export CXXFLAGS="%optflags -I$(pwd)/include"
export CPPFLAGS="-I$(pwd)/include"
export LDFLAGS="%_ldflags -lc"

if [ -f /usr/sfw/lib/libusb.so.1 ]
then
	export LDFLAGS="${LDFLAGS} %{sfw_lib_path}"
fi

mkdir include_disabled
./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
            --sbindir=%{_sbindir} \
            --sysconfdir=%{_sysconfdir}/apcupsd \
            --enable-usb \
            --enable-static=no
mv include/getopt.h include_disabled

gmake -j$CPUS VERBOSE=2

%install
rm -rf $RPM_BUILD_ROOT
gmake install DESTDIR=$RPM_BUILD_ROOT
# Install service manifest
mkdir -p $RPM_BUILD_ROOT/var/svc/manifest/device/
cp %{SOURCE1} $RPM_BUILD_ROOT/var/svc/manifest/device/%{name}.xml
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755, root, sys) %{_sysconfdir}
%dir %attr (0755, root, sys) %{_sysconfdir}/apcupsd
%{_sysconfdir}/apcupsd/*
%dir %attr (0755, root, sys)  /var
%dir %attr (0755, root, sys)  /var/svc
%dir %attr (0755, root, sys)  /var/svc/manifest
%dir %attr (0755, root, sys)  /var/svc/manifest/device
%class(manifest) %attr (0755, root, bin) /var/svc/manifest/device/apcupsd.xml
%dir %attr (0755, root, bin)  /lib
%dir %attr (0755, root, bin)  /lib/svc
%dir %attr (0755, root, bin)  /lib/svc/method
/lib/svc/method/*

%changelog
* Fri May 29 2009 - Moinak Ghosh <moinakg@belenix(dot)org>
- Pulled in from SourceJuicer and major fixes to spec file.
* Mon Apr 20 2009 - Emanuele Pucciarelli <ep@acm.org>
- Improved formatting for spec file
* Sun Apr 19 2009 - Emanuele Pucciarelli <ep@acm.org>
- Initial spec
