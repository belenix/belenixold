#
# spec file for package SFEspacenavd
#
# includes module(s): spacenavd
#

%include Solaris.inc
%include base.inc


Name:         SFEspacenavd
Summary:      A free, compatible alternative for 3Dconnexion's 3D input device drivers and SDK: Daemon
Group:        Applications/Productivity
Version:      0.4
License:      GPLv3+
BuildRoot:    %{_tmppath}/spacenav-%{version}-build
Source:       %{sf_download}/spacenav/spacenavd-%{version}.tar.gz
URL:          http://spacenav.sourceforge.net/
SUNW_BaseDir: %{_basedir}
%include default-depend.inc
Requires:      SFElibspnav
BuildRequires: SFElibspnav-devel

%description
The spacenav project provides a free, compatible alternative
to the proprietary 3Dconnexion device driver and SDK, for their
3D input devices (called "space navigator", "space pilot",
"space traveller", etc). 

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SFElibspnav-devel

%prep
%setup -q -c -n %name-%version
cd spacenavd-%{version}
cd ..

%build
cd spacenavd-%{version}
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags %{gnu_lib_path}"
        ./configure                     \
                --prefix=%{_prefix}     \
                --infodir=%{_datadir}/info \
                --mandir=%{_mandir}     \
                --libdir=%{_libdir}     \
                --disable-static
make
cd ..

%install
rm -rf $RPM_BUILD_ROOT
cd spacenavd-%{version}
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la
cd ..


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, bin) %{_libdir}/spacenav
%{_libdir}/spacenav/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/spacenav
%{_datadir}/spacenav/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*

%changelog
* Wed Mar 08 2006 - brian.cameron@sun.com
- Created.
