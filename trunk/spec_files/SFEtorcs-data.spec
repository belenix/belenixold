#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include base.inc

Name:                SFEtorcs-data
Summary:             The Open Racing Car Simulator data files
Version:             1.3.1
License:             GPLv2+ and Free Art
Group:               Amusements/Games
Source0:             http://downloads.sf.net/torcs/TORCS-%{version}-data.tgz
Source1:             http://downloads.sf.net/torcs/TORCS-%{version}-data-tracks-dirt.tgz
Source2:             http://downloads.sf.net/torcs/TORCS-%{version}-data-tracks-oval.tgz
Source3:             http://downloads.sf.net/torcs/TORCS-%{version}-data-tracks-road.tgz
Source4:             http://downloads.sf.net/torcs/TORCS-%{version}-data-cars-extra.tgz
Source5:             Free-Art-License 

URL:                 http://torcs.org/
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%description
TORCS is a 3D racing cars simulator using OpenGL. The goal is to have
programmed robots drivers racing against each others. You can also drive
yourself with either a wheel, keyboard or mouse.

This package contains the data files needed to run the game.

SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%package tracks-dirt
Summary:             The Open Racing Car Simulator additional dirt tracks
Group:               Amusements/Games
SUNW_BaseDir:        %{_prefix}
%include default-depend.inc
Requires: %{name}

%description tracks-dirt
TORCS is a 3D racing cars simulator using OpenGL.  The goal is to have
programmed robots drivers racing against each others.  You can also drive
yourself with either a wheel, keyboard or mouse.

This package contains additional tracks for the game.

%package tracks-oval
Summary:             The Open Racing Car Simulator additional oval tracks
Group:               Amusements/Games
SUNW_BaseDir:        %{_prefix}
%include default-depend.inc
Requires: %{name}

%description tracks-oval
TORCS is a 3D racing cars simulator using OpenGL.  The goal is to have
programmed robots drivers racing against each others.  You can also drive
yourself with either a wheel, keyboard or mouse.

This package contains additional tracks for the game.

%package tracks-road
Summary:             The Open Racing Car Simulator additional road tracks
Group:               Amusements/Games
SUNW_BaseDir:        %{_prefix}
%include default-depend.inc
Requires: %{name}

%description tracks-road
TORCS is a 3D racing cars simulator using OpenGL.  The goal is to have
programmed robots drivers racing against each others.  You can also drive
yourself with either a wheel, keyboard or mouse.

This package contains additional tracks for the game.

%package cars-extra
Summary:             The Open Racing Car Simulator additional cars
Group:               Amusements/Games
SUNW_BaseDir:        %{_prefix}
%include default-depend.inc
Requires: %{name}

%description cars-extra
TORCS is a 3D racing cars simulator using OpenGL.  The goal is to have
programmed robots drivers racing against each others.  You can also drive
yourself with either a wheel, keyboard or mouse.

This package contains additional cars for the game.

%prep
[ -d %{name}-%{version} ] && rm -rf %{name}-%{version}
mkdir %{name}-%{version}
cd %{name}-%{version}
# Uncompress all packages in a separate tree
for source in %{SOURCE0} %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4}; do
    package="`basename ${source} .tgz | sed 's/TORCS-%{version}-//g'`"
    mkdir -p ${package}%{_datadir}/games/torcs/
    ( cd ${package}%{_datadir}/games/torcs/
        tar xzf ${source} )
    echo ${package} >> package.list
done

%build
cd %{name}-%{version}
# List each package's files
for package in `cat package.list`; do
    ( cd ${package}
      find .%{_datadir}/games/torcs -type d \
          | sed s/^./\%dir\ / > ../${package}.files
      find .%{_datadir}/games/torcs -type f \
          | sed s/^.// >> ../${package}.files )
done

%install
cd %{name}-%{version}
rm -rf $RPM_BUILD_ROOT
# Install all trees into the main build root
mkdir -p $RPM_BUILD_ROOT

for package in `cat package.list`; do
    cp -a ${package}/* $RPM_BUILD_ROOT
done
# Prepare Free-Art-License for doc inclusion
ginstall -m 0644 %{SOURCE5} .
mkdir -p $RPM_BUILD_ROOT%{_docdir}

%clean
cd %{name}-%{version}
rm -rf $RPM_BUILD_ROOT

%files -f data.files
%defattr (-, root, bin)
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, other) %{_docdir}
%doc Free-Art-License

%files tracks-dirt -f data-tracks-dirt.files
%defattr (-, root, bin)
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, other) %{_docdir}
%doc Free-Art-License

%files tracks-oval -f data-tracks-oval.files
%defattr (-, root, bin)
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, other) %{_docdir}
%doc Free-Art-License

%files tracks-road -f data-tracks-road.files
%defattr (-, root, bin)
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, other) %{_docdir}
%doc Free-Art-License

%files cars-extra -f data-cars-extra.files
%defattr (-, root, bin)
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, other) %{_docdir}
%doc Free-Art-License

%changelog
* Mon Nov 30 2009 - Moinak Ghosh
- Initial version
