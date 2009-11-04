#
# spec file for package SFEFligthGear-data
# Moinak Ghosh
#
#
%include Solaris.inc

%define src_name	FlightGear-data
%define src_url		ftp://ftp.ibiblio.org/pub/mirrors/flightgear/ftp/Shared
# mirror that works sometime:
# http://flightgear.mxchange.org/pub/fgfs/Source/FlightGear-1.0.0.tar.gz
# http://mirror.fslutd.org/flightgear/Source/FlightGear-1.0.0.tar.gz
#ftp://ftp.kingmont.com/flightsims/flightgear/Source/FlightGear-1.0.0.tar.gz
# TODO: make package with:
# http://www.flightgear.org/Docs/getstart/getstart.html
# http://mirrors.ibiblio.org/pub/mirrors/flightgear/ftp/Docs/getstart.pdf
# faire un package pour installer modele son et scene.
# ftp://ftp.flightgear.org/pub/fgfs/Shared/fgfs-base-1.0.0.tar.bz2

Name:                   SFEFlightGear-data
Summary:                FlightGear base package of textures, models, data, aircraft, sample scenery, and config files.
Version:                1.9.0
Source:                 %{src_url}/%{src_name}-%{version}.tar.bz2

SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -c -n  %{name}

%build
cd data

%install
rm -rf $RPM_BUILD_ROOT
cd data
mkdir -p $RPM_BUILD_ROOT%{_datadir}/FlightGear
cp -r * $RPM_BUILD_ROOT%{_datadir}/FlightGear

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/FlightGear
%{_datadir}/FlightGear/*

%changelog
* Mon Nov 02 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Pulled in with modifications from SFE repo.
* Mon Nov 20 2008 - dauphin@enst.fr
- Initial version
