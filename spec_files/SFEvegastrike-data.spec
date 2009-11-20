#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

Name:                SFEvegastrike-data
Summary:             3D OpenGL spaceflight simulator
Version:             0.5.0
License:             GPLv2+
Group:               Amusements/Games
Source:              %{sf_download}/vegastrike/vegastrike-linux-%{version}.tar.bz2

URL:                 http://vegastrike.sourceforge.net/
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%description
Data files for Vega Strike, a GPL 3D OpenGL Action RPG space sim that allows
a player to trade and bounty hunt. 

%prep
%setup -q -c -n %name-%version
cd vegastrike-%{version}
rm -r cockpits/bomber-cockpit.cpt/#cockpit.xmesh# meshes/supernova.bmp.xmesh~ \
      modules/.cvsignore modules/builtin `find . -name "*.xmesh"`
find . -type d | xargs chmod a+x

# SVR4 packaging can't handle filenames with spaces - arrgh.
mv "history/a brief history in time and space.pdf" "history/a_brief_history_in_time_and_space.pdf"
mv "Install Vega Strike.sh" "Install_Vega_Strike.sh"

find . -type f | xargs chmod -x
chmod +x units/findunits.py modules/webpageize.py
sed -i 's/\r//g' documentation/mission_howto.txt
# remove the stale included manpages and the .xls abonimation
rm documentation/*.1 documentation/*.xls

%build
# Nothing to build for data

%install
rm -rf $RPM_BUILD_ROOT
cd vegastrike-%{version}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/vegastrike
for i in .vegastrike-0.5.0 ai animations bases cockpits communications \
    history meshes mission modules movies programs sectors sounds \
    sprites textures units universe \
    *.xml *.csv *.config *.cur *.xpm New_Game Version.txt; do
	cp -a $i $RPM_BUILD_ROOT%{_datadir}/vegastrike
done

mkdir -p $RPM_BUILD_ROOT%{_docdir}/vegastrike
cp -r documentation $RPM_BUILD_ROOT%{_docdir}/vegastrike

mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/128x128/apps
ginstall -p -m 644 vegastrike.xpm $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/128x128/apps

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_datadir}/vegastrike
%{_datadir}/vegastrike/*
%{_datadir}/vegastrike/.vegastrike-%{version}/*
%attr(0755, root, bin) %{_datadir}/vegastrike/.vegastrike-%{version}/.system
%dir %attr(0755, root, other) %{_docdir}
%{_docdir}/*
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/128x128
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/128x128/apps
%attr (0455, root, other) %{_datadir}/icons/hicolor/128x128/apps/*

%changelog
* Fri Nov 20 2009 - Moinak Ghosh
- Initial version
