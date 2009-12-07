#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include base.inc

Name:                SFEstarfighter
Summary:             Project: Starfighter, a space arcade game
Version:             1.1
License:             GPLv2+
Group:               Amusements/Games
Source:              http://www.parallelrealities.co.uk/download/starfighter/starfighter-1.1-1.tar.gz
Source1:             starfighter.png
Patch0:              starfighter-01-makefile.diff

URL:                 http://www.parallelrealities.co.uk/projects/starfighter.php
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWxorg-mesa
BuildRequires: SUNWxorg-headers
Requires: SFEsdl
BuildRequires: SFEsdl-devel
Requires: SFEsdl-mixer
BuildRequires: SFEsdl-mixer-devel
Requires: SFEsdl-image
BuildRequires: SFEsdl-image-devel
Requires: SUNWgnome-desktop-prefs
BuildRequires: SUNWgnome-common-devel

%description
After decades of war one company, who had gained powerful supplying both sides
with weaponary, steps forwards and crushes both warring factions in one swift
movement. Using far superior weaponary and AI craft, the company was completely
unstoppable and now no one can stand in their way. Thousands began to perish
under the iron fist of the company. The people cried out for a saviour, for
someone to light this dark hour... and someone did.

This game features 26 missions over 4 star systems and boss battles.

%prep
%setup -q -c -n %name-%version
cd starfighter-%{version}
%patch0 -p1
%{gnu_bin}/sed -i 's#install -m#ginstall -m#' makefile
%{gnu_bin}/sed -i 's#LIBS =#LIBS = %{gnu_lib_path}#' makefile

%build
cd starfighter-%{version}
export LDFLAGS="%{_ldflags}"
export CFLAGS="%{optflags}"

gmake PREFIX="%{_prefix}" OPTFLAGS="%{optflags}"

%install
rm -rf $RPM_BUILD_ROOT
cd starfighter-%{version}
gmake install PREFIX="%{_prefix}" DESTDIR=$RPM_BUILD_ROOT

ginstall -D -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/pixmaps/starfighter.png

# Install menu entry
cat > starfighter.desktop << EOF
[Desktop Entry]
Name=Project: Starfighter
Comment=Space Arcade Game
Icon=starfighter
Exec=starfighter
Terminal=false
Type=Application
Categories=Game;ArcadeGame;
Encoding=UTF-8
EOF

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install \
	--vendor "belenix" \
	--dir $RPM_BUILD_ROOT%{_datadir}/applications \
	starfighter.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_datadir}/starfighter
%{_datadir}/starfighter/*

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*

%changelog
* Mon Dec 07 2009 - Moinak Ghosh
- Initial version
