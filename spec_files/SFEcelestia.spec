#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include base.inc

Name:                SFEcelestia
Summary:             Render a planetary image into an X window
Version:             1.6.0
License:             GPLv2
URL:                 http://www.shatters.net/celestia/
Source:              %{sf_download}/celestia/celestia-%{version}.tar.gz
Patch1:              celestia-01-solaristime.diff
Patch2:              celestia-02-no_sun.diff

SUNW_BaseDir:        %{_basedir}
#SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWglib2
Requires: SUNWxwsvr
Requires: FSWxorg-clientlibs
Requires: SUNWxorg-clientlibs
Requires: SUNWpng
Requires: SUNWjpg
Requires: SUNWgnome-desktop-prefs
Requires: SUNWxorg-mesa
Requires: SFEfreeglut
Requires: SUNWgnu-gettext
Requires: SFEgtkglext
Requires: SFElua
BuildRequires: SUNWglib2-devel
BuildRequires: FSWxorg-headers
BuildRequires: SUNWxorg-headers
BuildRequires: SUNWpng-devel
BuildRequires: SUNWjpg-devel
BuildRequires: SUNWgnome-desktop-prefs-devel
BuildRequires: SFEfreeglut-devel
BuildRequires: SUNWgnu-gettext-devel
BuildRequires: SFEgtkglext-devel

%description
Celestia is a real-time space simulation which lets you experience the
universe in three dimensions. Celestia does not confine you to the
surface of the Earth, it allows you to travel throughout the solar
system, to any of over 100,000 stars, or even beyond the galaxy.

Travel in Celestia is seamless; the exponential zoom feature lets
you explore space across a huge range of scales, from galaxy clusters
down to spacecraft only a few meters across. A 'point-and-goto'
interface makes it simple to navigate through the universe to the
object you want to visit.

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -c -n %name-%version
cd celestia-%version
cat %{PATCH1} | gpatch --fuzz=0 --unified -p 1 -b
cat %{PATCH2} | gpatch --fuzz=0 --unified -p 1 -b
cd ..

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

cd celestia-%{version}
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -lm"
export LUA_CFLAGS="-I%{_includedir}"
export LUA_LIBS="-llua"
export LUALIB_CFLAGS="-I%{_includedir}"
export LUALIB_LIBS="-llua"

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --libdir=%{_libdir} \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir} \
            --includedir=%{_includedir} \
            --libexecdir=%{_libexecdir} \
	    --with-gtk

gmake -j$CPUS

cd ..


%install
rm -rf $RPM_BUILD_ROOT
cd celestia-%{version}
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 gmake DESTDIR=$RPM_BUILD_ROOT install

ginstall -p -m 644 -D src/celestia/kde/data/hi48-app-celestia.png \
  $RPM_BUILD_ROOT%{_datadir}/pixmaps/celestia.png
mkdir -p $RPM_BUILD_ROOT%{_datadir}/celestia/models/
ginstall -p -m 644 -D models/*.3ds $RPM_BUILD_ROOT%{_datadir}/celestia/models/
cp README $RPM_BUILD_ROOT%{_datadir}/celestia
cp devguide.txt controls.txt $RPM_BUILD_ROOT%{_datadir}/celestia
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_datadir}/celestia
%{_datadir}/celestia/*
%dir %attr(0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr(0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sat Oct 03 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Initial version.
