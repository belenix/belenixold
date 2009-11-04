#
# spec file for package SFEFligthGear.spec
# Gilles Dauphin
#
#
%include Solaris.inc

%define src_name	FlightGear
%define src_url		ftp://ftp.kingmont.com/flightsims/flightgear/Source
# mirror that works sometime:
# http://flightgear.mxchange.org/pub/fgfs/Source/FlightGear-1.0.0.tar.gz
# http://mirror.fslutd.org/flightgear/Source/FlightGear-1.0.0.tar.gz
#ftp://ftp.kingmont.com/flightsims/flightgear/Source/FlightGear-1.0.0.tar.gz
# TODO: make package with:
# http://www.flightgear.org/Docs/getstart/getstart.html
# http://mirrors.ibiblio.org/pub/mirrors/flightgear/ftp/Docs/getstart.pdf
# faire un package pour installer modele son et scene.
# ftp://ftp.flightgear.org/pub/fgfs/Shared/fgfs-base-1.0.0.tar.bz2

Name:                   SFEFlightGear
Summary:                Flight Simulator for 'true' airplane
License:                GPL
Version:                1.9.1
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
Patch2:                 FlightGear-02-reg.diff
Patch3:                 FlightGear-03-ioctl.diff

SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:		SFEopenal-devel
Requires:		SFEopenal
BuildRequires:		SFEfreealut-devel
Requires:		SFEfreealut
# Take care: needed freeglut-2.6.0-rc1
BuildRequires:		SFEfreeglut-devel
Requires:		SFEfreeglut
BuildRequires:		SFESimGear-devel
Requires:		SFESimGear
Requires:		SFEplib
BuildRequires:          SFEboost-gpp-devel
Requires:               SFEboost-gpp
BuildRequires:		SUNWsvn-devel
Requires:		SUNWsvn
Requires:		SUNWzlib
Requires:		SFEFlightGear-data

%prep
%setup -q -c -n  %{name}
%patch2 -p0
%patch3 -p0

%build
cd %{src_name}-%{version}
export CFLAGS="-I%{_includedir}/boost/gcc4 -I%{gnu_inc} -I%{gnu_inc}/apr-1"
export CXXFLAGS="-I%{_includedir}/boost/gcc4 -I%{gnu_inc} -I%{gnu_inc}/apr-1"
export LDFLAGS="-L/lib -R/lib -L%{_libdir}/boost/gcc4 -R%{_libdir}/boost/gcc4 %{gnu_lib_path}"
/bin/bash ./configure CONFIG_SHELL=/bin/bash --prefix=%{_prefix}
gmake

%install
rm -rf $RPM_BUILD_ROOT
cd %{src_name}-%{version}
gmake install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755,root,bin) %{_mandir}
%{_mandir}/*

%changelog
* Mon Nov 02 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Pulled in with modifications from SFE repo.
* Mon Nov 20 2008 - dauphin@enst.fr
- Initial version
