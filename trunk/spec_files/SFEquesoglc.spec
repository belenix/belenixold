#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%endif
%include base.inc

Name:                SFEquesoglc
Summary:             The OpenGL Character Renderer
Version:             0.7.1
Group:               System Environment/Libraries
License:             LGPLv2+
URL:                 http://quesoglc.sourceforge.net/
Source:              %{sf_download}/quesoglc/quesoglc-%{version}.tar.gz

SUNW_BaseDir:        /
#SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWfontconfig
Requires: SUNWfreetype2
BuildRequires: SUNWgnome-common-devel
Requires: SFEfreeglut
BuildRequires: SFEfreeglut-devel
Requires: SFElibfribidi
BuildRequires: SFElibfribidi-devel
Requires: SFEglew
Requires: SUNWxorg-clientlibs
BuildRequires: SUNWxorg-headers
BuildRequires: SFEdoxygen

%description
The OpenGL Character Renderer (GLC) is a state machine that provides OpenGL
programs with character rendering services via an application programming
interface (API).

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            /
%include default-depend.inc
Requires: %name
Requires: SUNWgnome-common-devel
Requires: SFEfreeglut-devel
Requires: SFElibfribidi-devel
Requires: SFEglew
Requires: SUNWxorg-headers
Requires: SFEdoxygen

%description devel
This package provides the libraries, include files, and other resources needed
for developing GLC applications.

%prep
%setup -q -c -n %name-%version
cd quesoglc-%{version}
rm -f include/GL/{glxew,wglew,glew}.h
ln -s %{xorg_inc}/GL/{glxew,wglew,glew}.h include/GL/
#%patch6 -p1
cd ..

%ifarch amd64 sparcv9
cp -pr quesoglc-%{version} quesoglc-%{version}-64
%endif

%build
# 64Bit build disabled till we get 64Bit libfribidi
#%ifarch amd64 sparcv9
#cd quesoglc-%{version}-64
#export CFLAGS="-m64 -fPIC -DPIC -I/usr/X11/include"
#export CXXFLAGS="-m64 -fPIC -DPIC -I/usr/X11/include"
#export LDFLAGS="%{_ldflags64} %{gnu_lib_path64}"
#
#./configure --prefix=%{_prefix}  \
#            --bindir=%{_bindir}/%{_arch64} \
#            --libdir=%{_libdir}/%{_arch64} \
#            --mandir=%{_mandir} \
#            --disable-static
#gmake
#cd ..
#%endif

cd quesoglc-%{version}
export CFLAGS="-fPIC -DPIC -I/usr/X11/include"
export LDFLAGS="%{_ldflags} %{gnu_lib_path}"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
            --disable-static
gmake
cd docs; doxygen
cd ../..

%install
rm -rf $RPM_BUILD_ROOT
#%ifarch amd64 sparcv9
#cd quesoglc-%{version}-64
#gmake install     DESTDIR=$RPM_BUILD_ROOT
#rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/libGLC.la
#cd ..
#%endif

cd quesoglc-%{version}
gmake install     DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/libGLC.la
mkdir -p $RPM_BUILD_ROOT%{xorg_inc}/GL
mv $RPM_BUILD_ROOT%{_includedir}/GL/* $RPM_BUILD_ROOT%{xorg_inc}/GL
rmdir $RPM_BUILD_ROOT%{_includedir}/GL
rmdir $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, bin) %{xorg_inc}
%{xorg_inc}/*

%changelog
* Mon Dec 07 2009 - Moinak Ghosh
- Initial spec
