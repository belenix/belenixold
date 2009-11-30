#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include base.inc

Name:                SFEtorcs
Summary:             The Open Racing Car Simulator
Version:             1.3.1
License:             GPLv2+
Group:               Amusements/Games
Source:              http://downloads.sf.net/torcs/TORCS-%{version}-src.tgz
Source1:             http://downloads.sf.net/torcs/TORCS-%{version}-src-robots-base.tgz
Source2:             torcs.desktop
Patch1:              torcs-01-endian.diff
Patch2:              torcs-02-math.diff
Patch3:              torcs-03-solaris.diff

URL:                 http://torcs.org/
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWxorg-mesa
BuildRequires: SUNWxorg-headers
Requires: SFEfreeglut
BuildRequires: SFEfreeglut-devel
Requires: SFEplib
Requires: SUNWjpg
BuildRequires: SUNWjpg-devel
Requires: SUNWzlib
Requires: SUNWpng
BuildRequires: SUNWpng-devel
Requires: SFEopenal
BuildRequires: SFEopenal-devel
Requires: SFEfreealut
BuildRequires: SFEfreealut-devel
Requires: SUNWgnome-desktop-prefs
BuildRequires: SUNWgnome-common-devel
Requires: SFEtorcs-data
Requires: SFEtorcs-data-tracks-road
Requires: SFEtorcs-data-cars-extra

%description
TORCS is a 3D racing cars simulator using OpenGL. The goal is to have
programmed robots drivers racing against each others. You can also drive
yourself with either a wheel, keyboard or mouse.

%prep
%setup -q -c -n %name-%version
gunzip -c %{SOURCE1} | tar xf - 
cd torcs-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
chmod -x src/libs/learning/policy.*

%build
cd torcs-%{version}
export LDFLAGS="-L%{_libdir} -R%{_libdir} %{gnu_lib_path} -lgnuintl -lgnuiconv"
export CFLAGS="%{optflags}"
export CXXFLAGS="%{cxx_optflags}"
export CPPFLAGS="-I`pwd`/src/interfaces -I`pwd`/src/modules/simu/simuv2/SOLID-2.0/src -I`pwd`/src/modules/simu/simuv2/SOLID-2.0/include -D__C99FEATURES__"

./configure --prefix=%{_prefix} --datadir=%{_datadir}/torcs --enable-shared
for m in `find . -name Makefile`
do
	%{gnu_bin}/sed -i 's/-maxdepth 0/-prune/g' ${m}
done
gmake

%install
rm -rf $RPM_BUILD_ROOT
cp torcs-%{version}/COPYING .
cp torcs-%{version}/README .

cd torcs-%{version}
gmake install DESTDIR=$RPM_BUILD_ROOT

# Icon for the desktop file
ginstall -D -p -m 0644 Ticon.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/torcs.png

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install \
	--vendor "belenix" \
	--dir $RPM_BUILD_ROOT%{_datadir}/applications \
	%{SOURCE2}

find $RPM_BUILD_ROOT -type d | xargs chmod 0755
mkdir -p $RPM_BUILD_ROOT%{_docdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/games
%{_datadir}/games/*

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr (0755, root, other) %{_docdir}
%doc COPYING README

%changelog
* Mon Nov 30 2009 - Moinak Ghosh
- Initial version
