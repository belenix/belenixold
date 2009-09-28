#
# spec file for package SFElibspnav
#
# includes module(s): libspnav
#

%include Solaris.inc
%include base.inc


Name:         SFElibspnav
Summary:      A free, compatible alternative for 3Dconnexion's 3D input device drivers and SDK: Library
Group:        Applications/Productivity
Version:      0.2.1
License:      GPLv3+
BuildRoot:    %{_tmppath}/libspnav-%{version}-build
Source:       %{sf_download}/spacenav/libspnav-%{version}.tar.gz
URL:          http://spacenav.sourceforge.net/
SUNW_BaseDir: %{_basedir}
SUNW_Copyright: %{name}.copyright
%include default-depend.inc

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

%prep
%setup -q -c -n %name-%version

%build
cd libspnav-%{version}
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags %{gnu_lib_path}"
        ./configure                     \
                --prefix=%{_prefix}     \
                --infodir=%{_datadir}/info \
                --mandir=%{_mandir}     \
                --libdir=%{_libdir}
make
cd ..

%install
rm -rf $RPM_BUILD_ROOT
cd libspnav-%{version}
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_includedir}
/usr/ucb/install -m 0755 libspnav.so.0.1 $RPM_BUILD_ROOT%{_libdir}
(cd $RPM_BUILD_ROOT%{_libdir}
 ln -s libspnav.so.0.1 libspnav.so)
cp -p spnav.h spnav_magellan.h spnav_config.h $RPM_BUILD_ROOT%{_includedir}
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Mon Sep 28 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Initial version.
