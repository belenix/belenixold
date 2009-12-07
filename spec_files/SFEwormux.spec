#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include base.inc

Name:                SFEwormux
Summary:             2D convivial mass murder game
Version:             0.8.5
License:             GPLv2+
Group:               Amusements/Games
Source:              http://download.gna.org/wormux/wormux-%{version}.tar.bz2
Source1:             wormux.desktop
Patch1:              wormux-01-cflags.diff
Patch2:              wormux-02-solaris.diff

URL:                 http://www.wormux.org/
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEsdl-image
BuildRequires: SFEsdl-image-devel
Requires: SFEsdl-gfx
BuildRequires: SFEsdl-gfx-devel
Requires: SUNWpng
BuildRequires: SUNWpng-devel
Requires: SFEsdl-ttf
BuildRequires: SFEsdl-ttf-devel
Requires: SFEsdl-mixer
BuildRequires: SFEsdl-mixer-devel
Requires: SFEsdl-net
BuildRequires: SFEsdl-net-devel
Requires: SUNWcurl
BuildRequires: SUNWcurl-devel
Requires: SUNWgnome-desktop-prefs
BuildRequires: SUNWgnome-common-devel
Requires: SFEwormux-data
Requires: SFElxmlpp
BuildRequires: SFElxmlpp-devel

%description
Battle your favorite free software mascots in the Wormux arena. With big
sticks of dynamite, grenades, baseball bats, and bazookas you can exterminate
your opponent in a 2D cartoon style scenery. The goal of the game is to
destroy all of your opponents' mascots.

%package data
Summary:                 Data files for wormux
Group:                   Amusements/Games
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -c -n %name-%version
cd wormux-%{version}
%patch1 -p1
%patch2 -p1

for m in `find . -name Makefile.in`
do
	cp ${m} ${m}.orig
	cat ${m}.orig | sed 's#-Wl,--as-needed##' > ${m}
done
cd ..

%build
cd wormux-%{version}
export CFLAGS="%{optflags} -fno-strict-aliasing"
export CXXCFLAGS="%{cxx_optflags} -fno-strict-aliasing"
export LDFLAGS="%{_ldflags} %{xorg_lib_path} -lX11"
export CPPFLAGS="-D__EXTENSIONS__"
export cxx_present="yes"

./configure --prefix=%{_prefix} --datadir=%{_datadir} \
            --disable-rpath \
            --disable-debug --with-distributor="BeleniX"

gmake

%install
rm -rf $RPM_BUILD_ROOT
cd wormux-%{version}
gmake install DESTDIR=$RPM_BUILD_ROOT
cp %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/applications/wormux.desktop
ginstall -d $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/32x32/apps/
ginstall -p -m 644 data/wormux_32x32.png \
    $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/32x32/apps/wormux.png

mkdir -p $RPM_BUILD_ROOT%{_docdir}/wormux
cp COPYING* $RPM_BUILD_ROOT%{_docdir}/wormux
cp AUTHORS $RPM_BUILD_ROOT%{_docdir}/wormux
cp ChangeLog $RPM_BUILD_ROOT%{_docdir}/wormux
cp -rp doc/howto* $RPM_BUILD_ROOT%{_docdir}/wormux

%if %build_l10n
%else
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%post
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
	%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
	%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/icons
%{_datadir}/icons/*

%files data
%defattr (-, root, bin)
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_datadir}/wormux
%{_datadir}/wormux/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Mon Dec 07 2009 - Moinak Ghosh
- Initial version
