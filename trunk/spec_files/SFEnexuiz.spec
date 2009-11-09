#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

Name:                SFEnexuiz
Summary:             Nexuiz is a free open-source, cross-platform first person shooter.
Version:             2.5.2
%define tarball_version 252
License:             GPL
Source:              %{sf_download}/nexuiz/nexuiz-%{tarball_version}.zip
Source2:             nexuiz.desktop
Source3:             nexuiz

URL:                 http://www.alientrap.org/nexuiz/
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEsdl
BuildRequires: SFEsdl-devel
Requires: SUNWxorg-mesa
BuildRequires: SUNWxorg-headers
BuildRequires: SUNWunzip
BuildRequires: SUNWimagick

%description
Nexuiz is a fast paced 3d deathmatch game project created online 
by a team of developers called Alientrap.

%prep
%setup -q -c -n %name-%version
(cd Nexuiz/sources/
 unzip enginesource*.zip
 cd darkplaces
 cp makefile makefile.orig
 echo "SHELL=/usr/bin/bash" > makefile
 cat makefile.orig >> makefile
 perl -pi -e 's/\bmodel_t\b/lh_dp_model_t/g' *.c *.h
 cp makefile.inc makefile.inc.orig
 cat makefile.inc.orig | sed 's/#CPUOPTIMIZATIONS?=-march=pentium3/CPUOPTIMIZATIONS?=-march=pentium3/' > makefile.inc
)

%build
cd Nexuiz/sources/darkplaces
gmake -f makefile cl-nexuiz
convert nexuiz.xpm nexuiz.png

%define datez 20091001
%install
rm -rf $RPM_BUILD_ROOT
cd Nexuiz
mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/usr/share/nexuiz/data
mkdir -p $RPM_BUILD_ROOT/usr/share/pixmaps
mkdir -p $RPM_BUILD_ROOT/usr/share/applications

ginstall --mode=755 %{SOURCE3} $RPM_BUILD_ROOT/usr/bin
ginstall --mode=755 sources/darkplaces/nexuiz-glx $RPM_BUILD_ROOT/usr/share/nexuiz
cp sources/darkplaces/nexuiz.png $RPM_BUILD_ROOT/usr/share/pixmaps
cp %{SOURCE2} $RPM_BUILD_ROOT/usr/share/applications

cd data
zipsplit -n 104857600 data%{datez}.pk3 
mv data20_1.zip data%{datez}.1.pk3
mv data20_2.zip data%{datez}.2.pk3
mv data20_3.zip data%{datez}.3.pk3
mv data20_4.zip data%{datez}.4.pk3
mv data20_5.zip data%{datez}.5.pk3
mv data20_6.zip data%{datez}.6.pk3

cd ..

cp data/data%{datez}.1.pk3 $RPM_BUILD_ROOT/usr/share/nexuiz/data
cp data/data%{datez}.2.pk3 $RPM_BUILD_ROOT/usr/share/nexuiz/data
cp data/data%{datez}.3.pk3 $RPM_BUILD_ROOT/usr/share/nexuiz/data
cp data/data%{datez}.4.pk3 $RPM_BUILD_ROOT/usr/share/nexuiz/data
cp data/data%{datez}.5.pk3 $RPM_BUILD_ROOT/usr/share/nexuiz/data
cp data/data%{datez}.6.pk3 $RPM_BUILD_ROOT/usr/share/nexuiz/data

cp data/common-spog.pk3 $RPM_BUILD_ROOT/usr/share/nexuiz/data
cp havoc/data%{datez}havoc.pk3 $RPM_BUILD_ROOT/usr/share/nexuiz/data

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x %{_bindir}/update-mime-database || exit 0';
  echo '%{_bindir}/update-mime-database %{_datadir}/mime'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x /usr/bin/scrollkeeper-update || exit 0';
  echo '/usr/bin/scrollkeeper-update'
) | $BASEDIR/lib/postrun -b -u -c JDS

%postun
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x %{_bindir}/update-mime-database || exit 0';
  echo '%{_bindir}/update-mime-database %{_datadir}/mime'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x /usr/bin/scrollkeeper-update || exit 0';
  echo '/usr/bin/scrollkeeper-update'
) | $BASEDIR/lib/postrun -b -u -c JDS

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, sys) %{_datadir}
%{_datadir}/nexuiz
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (-, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*

%changelog
* Fri Nov 06 2009 - Moinak Ghosh
- Imported from SFE repo.
* Web Sep 09 2009 - drdoug007@gmail.com
- Updated required packages
* Tue Sep 08 2009 - drdoug007@gmail.com
- Initial version
