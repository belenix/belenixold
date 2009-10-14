#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

#%ifarch amd64 sparcv9
#%include arch64.inc
#%endif

%include base.inc
%define python_vers  2.6

Name:                SFEfree-cad
Summary:             FreeCAD is aimed as a general purpose 3D CAD modeler
Version:             0.8.2237
License:             GPL or LGPL
URL:                 http://sourceforge.net/apps/mediawiki/free-cad/index.php?title=Main_Page
Source:              %{sf_download}/free-cad/FreeCAD%%20Linux/FreeCAD%%200.8%%20R2237/freecad_%{version}.orig.tar.gz
Patch1:              free-cad-01-solaris.diff

SUNW_BaseDir:        %{_basedir}
#SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWPython26
Requires: SFEsoqt
Requires: SFEcoin3d
Requires: SFEqt4
Requires: SFEopencascade
Requires: SFEsimage
Requires: SFEode
Requires: SFEgts
Requires: SFEboost-gpp
Requires: SFEopencv
Requires: SUNWxorg-mesa
Requires: SFExerces-c
BuildRequires: SUNWPython26-devel
BuildRequires: SFEdoxygen
BuildRequires: SUNWxorg-headers
BuildRequires: SFEsimage-devel
BuildRequires: SFEsoqt-devel
BuildRequires: SFEcoin3d-devel
BuildRequires: SFEqt4-devel
BuildRequires: SFEopencascade-devel
BuildRequires: SFEode-devel
BuildRequires: SFEgts-devel
BuildRequires: SFEboost-gpp-devel
BuildRequires: SFEopencv-devel
BuildRequires: SFExerces-c-devel

%description
FreeCAD will be a general purpose 3D CAD modeler. The development is
completely Open Source (GPL & LGPL License). FreeCAD is aimed directly
at mechanical engineering and product design but also fits in a wider
range of uses around engineering, such as architecture or other
engineering specialties.

FreeCAD features tools similar to Catia, SolidWorks or Solid Edge, and
therefore also falls into the category of MCAD, PLM, CAx and CAE. It
will be a feature based parametric modeler with a modular software
architecture which makes it easy to provide additional functionality
without modifying the core system

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name
Requires: SUNWPython26-devel
Requires: SFEdoxygen
Requires: SFEsoqt-devel
Requires: SFEcoin3d-devel
Requires: SUNWxorg-headers
Requires: SFEqt4-devel
Requires: SFEopencascade-devel
Requires: SFEsimage-devel
Requires: SFEode-devel
Requires: SFEgts-devel
Requires: SFEboost-gpp-devel
Requires: SFEopencv-devel
Requires: SFExerces-c-devel

%prep
%setup -q -c -n %name-%version
cd FreeCAD-%version
%patch1 -p1
cd ..

#%ifarch amd64 sparcv9
#cp -rp FreeCAD-%version FreeCAD-%{version}-64
#%endif


%build
#%ifarch amd64 sparcv9
#cd FreeCAD-%{version}-64

#export CFLAGS="%optflags64"
#export CXXFLAGS="%cxx_optflags64"
#export LDFLAGS="%_ldflags64"

#./configure --prefix=%{_prefix} \
#            --bindir=%{_bindir}/%{_arch64} \
#            --libdir=%{_libdir}/%{_arch64} \
#            --sysconfdir=%{_sysconfdir} \
#            --includedir=%{_includedir} \
#            --libexecdir=%{_libexecdir} \
#            --with-simage \
#            --with-mesa \
#            --enable-threadsafe \
#            --enable-html 

#gmake -j$CPUS

#cd ..
#%endif

cd FreeCAD-%version
xul_lib=`grep "^libdir" %{_libdir}/pkgconfig/mozilla-nss.pc | cut -f2 -d"="`
export CFLAGS="-march=pentium3 -fno-omit-frame-pointer -fPIC -DPIC"
export CXXFLAGS="-march=pentium3 -fno-omit-frame-pointer -fPIC -DPIC"
export LDFLAGS="-L%{_libdir} -R%{_libdir} -lsocket -lnsl %{gnu_lib_path} -lstdc++ -lm -L%{_libdir}/boost/gcc4 -R%{_libdir}/boost/gcc4 -L${xul_lib} -R${xul_lib}"
export PATH="%{_prefix}/qt4/bin:${PATH}"

#
# Workarounds for broken configure
#
export CXX="${CXX} -I%{_includedir}/boost/gcc4"
export LD_LIBRARY_PATH="%{_libdir}:%{gnu_lib}:%{sfw_lib}"

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --libdir=%{_libdir} \
            --sysconfdir=%{_sysconfdir} \
            --includedir=%{_includedir} \
            --libexecdir=%{_libexecdir} \
            --mandir=%{_mandir} \
            --with-qt4-dir=%{_prefix} \
            --with-qt4-include=%{_includedir}/qt4 \
            --with-qt4-lib=%{_libdir} \
            --with-qt4-bin=%{_prefix}/qt4/bin \
            --with-boost-include=%{_includedir}/boost/gcc4 \
            --with-boost-lib=%{_libdir}/boost/gcc4

unset LD_LIBRARY_PATH

#
# Parallel build appears to be broken for MeshPart
#
gmake
cd ..


%install
rm -rf $RPM_BUILD_ROOT

#%ifarch amd64 sparcv9
#cd FreeCAD-%{version}-64
#
#gmake DESTDIR=$RPM_BUILD_ROOT install
#cd ..
#%endif

cd FreeCAD-%version
export LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir}:/lib:%{_libdir}:%{gnu_lib}
gmake DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/*
%dir %attr (0755, root, bin) %{_prefix}/Mod
%{_prefix}/Mod/*

#%ifarch amd64 sparcv9
#%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
#%{_libdir}/%{_arch64}/lib*.so*
#%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

#%ifarch amd64 sparcv9
#%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
#%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
#%{_libdir}/%{_arch64}/pkgconfig/*
#%endif

%changelog
* Sat Oct 10 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Initial version.
