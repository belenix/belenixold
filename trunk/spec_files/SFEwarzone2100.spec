#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include base.inc

Name:                SFEwarzone2100
Summary:             Innovative 3D real-time strategy
Version:             2.2.1
License:             GPLv2+ and CC-BY-SA
Group:               Amusements/Games
Source:              http://download.gna.org/warzone/releases/2.2/warzone2100-%{version}.tar.bz2
Source1:             http://guide.wz2100.net/files/sequences.wz
Patch1:              warzone2100-01-solaris.diff
Patch2:              warzone2100-02-netlog_fix.diff

URL:                 http://wz2100.net/
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWxorg-mesa
BuildRequires: SUNWxorg-headers
Requires: SFEphysfs
BuildRequires: SFEphysfs-devel
Requires: SUNWogg-vorbis
BuildRequires: SUNWogg-vorbis-devel
BuildRequires: SUNWflexlex
BuildRequires: SUNWbison
Requires: SFEfreealut
BuildRequires: SFEfreealut-devel
Requires: SUNWzlib
Requires: SUNWpng
BuildRequires: SUNWpng-devel
Requires: SFEsdl-net
BuildRequires: SFEsdl-net-devel
Requires: SFEopenal
BuildRequires: SFEopenal-devel
Requires: SFEfreealut
BuildRequires: SFEfreealut-devel
Requires: SUNWgnome-desktop-prefs
BuildRequires: SUNWgnome-common-devel
Requires: SUNWlibtheora
BuildRequires: SUNWlibtheora-devel
Requires: SFEquesoglc
BuildRequires: SFEquesoglc-devel
Requires: SUNWlibpopt
BuildRequires: SUNWlibpopt-devel

%description
Warzone 2100 was an innovative 3D real-time strategy game back in 1999, and
most will agree it didn't enjoy the commercial success it should have had. The
game's source code was liberated on December 6th, 2004, under a GPL license
(see COPYING in this directory for details). Soon after that, the Warzone 2100
ReDev project was formed to take care of its future.

%package sequences
Summary:                 Video file for Warzone2100
Group:                   Amusements/Games
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %{name}

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -c -n %name-%version
cd warzone2100-%{version}
%patch1 -p1
%patch2 -p1
cd ..

%build
cd warzone2100-%{version}
export CFLAGS="%{optflags} -fno-strict-aliasing"
export CXXCFLAGS="%{cxx_optflags} -fno-strict-aliasing"
export LDFLAGS="%{_ldflags} %{xorg_lib_path} -lX11"
export CPPFLAGS="-D__EXTENSIONS__"

./configure --prefix=%{_prefix} --datadir=%{_datadir} \
            --disable-rpath \
            --disable-debug --with-distributor="BeleniX"

gmake

%install
rm -rf $RPM_BUILD_ROOT
cp warzone2100-%{version}/COPYING* .
cp warzone2100-%{version}/AUTHORS .
cp warzone2100-%{version}/ChangeLog .

cd warzone2100-%{version}
gmake install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_datadir}/warzone2100
ginstall -p -m644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/warzone2100
mkdir -p $RPM_BUILD_ROOT%{_docdir}

%if %build_l10n
%else
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_datadir}/warzone2100
%{_datadir}/warzone2100/base.wz
%{_datadir}/warzone2100/mp.wz
%dir %attr(0755, root, bin) %{_datadir}/warzone2100/mods
%{_datadir}/warzone2100/mods/*
%dir %attr(0755, root, bin) %{_datadir}/warzone2100/music
%{_datadir}/warzone2100/music/*
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/icons
%{_datadir}/icons/*

%files sequences
%defattr (-, root, bin)
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_datadir}/warzone2100
%{_datadir}/warzone2100/sequences.wz

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Mon Nov 30 2009 - Moinak Ghosh
- Initial version
