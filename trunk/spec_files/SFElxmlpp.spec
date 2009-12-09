#
# spec file for package SFElxmlpp
#
#
%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%endif
%include base.inc

Name:			SFElxmlpp
License:		LGPLv2+
Group:			System Environment/Libraries
Version:		2.26.0
Summary:		C++ wrapper for the libxml2 XML parser library
Source:			http://ftp.gnome.org/pub/GNOME/sources/libxml++/2.26/libxml++-%{version}.tar.bz2

URL:			http://libxmlplusplus.sourceforge.net/
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:		%{_prefix}
Requires: SUNWlxml
BuildRequires: SUNWlxml-devel
Requires: SUNWglibmm
BuildRequires: SUNWglibmm-devel
BuildRequires: SFEdoxygen
BuildRequires: SFEgraphviz
%if %cc_is_gcc
Requires: SFEgccruntime
%endif

%description
libxml++ is a C++ wrapper for the libxml2 XML parser library. It's original
author is Ari Johnson and it is currently maintained by Christophe de Vienne
and Murray Cumming.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
Requires: SUNWlxml-devel
Requires: SUNWglibmm-devel
Requires: SFEdoxygen
Requires: SFEgraphviz

%prep
%setup -q -c -n %name-%version
#%ifarch amd64 sparcv9
#cp -pr libxml++-%{version} libxml++-%{version}-64
#%endif

%build

# 64Bit build disabled since SUNWglibmm is not 64Bit yet.
#%ifarch amd64 sparcv9
#cd libxml++-%{version}-64
#export CFLAGS="-m64 -march=opteron -fno-omit-frame-pointer -O2"
#export CXXFLAGS="-m64 -march=opteron -fno-omit-frame-pointer -O2"
#export LDFLAGS="-m64 %{gnu_lib_path64} -lintl -liconv -L/lib/%{_arch64} -R/lib/%{_arch64} -L$RPM_BUILD_ROOT%{_libdir}"
#./configure \
#    --prefix=%{_prefix} \
#    --sysconfdir=%{_sysconfdir} \
#    --libdir=%{_libdir}/%{_arch64} \
#    --disable-static \
#    --mandir=%{_mandir} \
#    --infodir=%{_infodir}
#
#gmake
#cd ..
#%endif

cd libxml++-%{version}
export CFLAGS="-march=pentium3 -fno-omit-frame-pointer -O2"
export CXXFLAGS="-march=pentium3 -fno-omit-frame-pointer -O2"
export LDFLAGS="%{gnu_lib_path} -lintl -liconv -L/lib -R/lib -L$RPM_BUILD_ROOT%{_libdir}"
./configure \
    --prefix=%{_prefix} \
    --sysconfdir=%{_sysconfdir} \
    --libdir=%{_libdir} \
    --disable-static \
    --mandir=%{_mandir} \
    --infodir=%{_infodir}
 
gmake

%install
rm -rf $RPM_BUILD_ROOT
#%ifarch amd64 sparcv9
#cd libxml++-%{version}-64
#make install DESTDIR=$RPM_BUILD_ROOT
#rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/lib*a
#cd ..
#%endif

cd libxml++-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_infodir}
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

#%ifarch amd64 sparcv9
#%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
#%{_libdir}/%{_arch64}/lib*.so*
#%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
#%{_libdir}/%{_arch64}/pkgconfig/*
#%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/libxml++-2.6
%{_libdir}/libxml++-2.6/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*

%changelog
* Tue Jan 22 2008 - moinak.ghosh@sun.com
- Initial spec.
