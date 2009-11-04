#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

Name:                SFEosg
Summary:             An open source high performance 3D graphics toolkit.
Version:             2.8.2
License:             OpenSceneGraph Public License
Source:              http://www.openscenegraph.org/downloads/stable_releases/OpenSceneGraph-%{version}/source/OpenSceneGraph-%{version}.zip
URL:                 http://www.openscenegraph.org/projects/osg
Patch1:              osg-01-xul.diff

SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SFEfltk
BuildRequires: SFEfltk-devel
Requires: SUNWpng
BuildRequires: SUNWpng-devel
Requires: SUNWxorg-clientlibs
BuildRequires: SUNWxorg-headers
Requires: SFEjasper
BuildRequires: SFEjasper-devel
Requires: SUNWTiff
BuildRequires: SUNWTiff-devel
Requires: SUNWzlib
Requires: SUNWfreetype2
Requires: SFEcoin3d
BuildRequires: SFEcoin3d-devel
Requires: SFEgiflib
Requires: SFEopenexr
BuildRequires: SFEopenexr-devel
Requires: SFEopenvrml
BuildRequires: SFEopenvrml-devel
Requires: SFExine-lib
BuildRequires: SFExine-lib-devel
Requires: SUNWlibrsvg
BuildRequires: SUNWlibrsvg-devel
Requires: SUNWcairo
BuildRequires: SUNWcairo-devel
Requires: SFEgtkglext
BuildRequires: SFEgtkglext-devel

%description
The OpenSceneGraph is an open source high performance 3D graphics
toolkit, used by application developers in fields such as visual
simulation, games, virtual reality, scientific visualization and
modelling. Written entirely in Standard C++ and OpenGL it runs on
all Windows platforms, OSX, GNU/Linux, IRIX, Solaris, HP-Ux, AIX
and FreeBSD operating systems. The OpenSceneGraph is now well
established as the world leading scene graph technology, used
widely in the vis-sim, space, scientific, oil-gas, games and
virtual reality industries.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: SFEfltk-devel
Requires: SUNWpng-devel
Requires: SUNWxorg-headers
Requires: SFEjasper-devel
Requires: SUNWTiff-devel
Requires: SFEcoin3d-devel
Requires: SFEopenexr-devel
Requires: SFEopenvrml-devel
Requires: SFExine-lib-devel
Requires: SUNWlibrsvg-devel
Requires: SUNWcairo-devel
Requires: SFEgtkglext-devel

%prep
%setup -q -c -n %name-%version
cd OpenSceneGraph-%version
%patch1 -p1
cd ..

#%ifarch amd64 sparcv9
#cp -rp OpenSceneGraph-%version OpenSceneGraph-%{version}-64
#%endif


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

#
# Need 64Bit xine for 64Bit build.
#
#%ifarch amd64 sparcv9
#cd OpenSceneGraph-%{version}-64
#
#export CFLAGS="%optflags64 -I%{_prefix}/poppler/include"
#export CXXFLAGS="%cxx_optflags64 -I%{_prefix}/poppler/include"
#export LDFLAGS="%_ldflags64 -L%{_prefix}/poppler/lib/%{_arch64} -R%{_prefix}/poppler/lib/%{_arch64}"
#export PKG_CONFIG_PATH=%{_prefix}/poppler/lib/%{_arch64}/pkgconfig:%{_prefix}/lib/%{_arch64}/pkgconfig:%{_prefix}/gnu/lib/%{_arch64}/pkgconfig
#
#cmake   -DCMAKE_INSTALL_PREFIX=%{_prefix}                               \
#        -DCMAKE_BUILD_TYPE=Release                                      \
#        -DCMAKE_C_COMPILER:FILEPATH=${CC}                               \
#        -DCMAKE_C_FLAGS:STRING="${CFLAGS}"                              \
#        -DCMAKE_CXX_COMPILER:FILEPATH=${CXX}                            \
#        -DCMAKE_CXX_FLAGS_RELEASE:STRING="${CXXFLAGS}"                  \
#        -DLIB_INSTALL_DIR=%{_libdir}/%{_arch64}                         \
#        -DPOPPLER_INCLUDE_DIR=%{_prefix}/poppler/include/poppler/qt4    \
#        -DPOPPLER_LIBRARY=%{_prefix}/poppler/lib/libpoppler-qt4.so      \
#        -DBUILD_SHARED_LIBS=On                                          \
#        -DCMAKE_VERBOSE_MAKEFILE=1 . > config.log 2>&1
#
#gmake -j$CPUS
#cd ..
#%endif

#
# Disable SSE till we figure out the recurrence of:
# http://gcc.gnu.org/bugzilla/show_bug.cgi?id=17990
#
cd OpenSceneGraph-%{version}
export CFLAGS="%optflags -I%{_prefix}/poppler/include -mmmx -mno-sse"
export CXXFLAGS="%cxx_optflags -I%{_prefix}/poppler/include -mmmx -mno-sse"
export LDFLAGS="%_ldflags -L%{_prefix}/poppler/lib -R%{_prefix}/poppler/lib"
export PKG_CONFIG_PATH=%{_prefix}/poppler/lib/pkgconfig:%{_prefix}/lib/pkgconfig:%{_prefix}/gnu/lib/pkgconfig

cmake   -DCMAKE_INSTALL_PREFIX=%{_prefix}                               \
        -DCMAKE_BUILD_TYPE=Release                                      \
        -DCMAKE_C_COMPILER:FILEPATH=${CC}                               \
        -DCMAKE_C_FLAGS:STRING="${CFLAGS}"                              \
        -DCMAKE_CXX_COMPILER:FILEPATH=${CXX}                            \
        -DCMAKE_CXX_FLAGS_RELEASE:STRING="${CXXFLAGS}"                  \
        -D_OPENTHREADS_ATOMIC_USE_GCC_BUILTINS=0                        \
        -DPOPPLER_INCLUDE_DIR=%{_prefix}/poppler/include/poppler/qt4    \
        -DPOPPLER_LIBRARY=%{_prefix}/poppler/lib/libpoppler-qt4.so      \
        -DLIB_INSTALL_DIR=%{_libdir}                                    \
        -DBUILD_SHARED_LIBS=On                                          \
        -DCMAKE_VERBOSE_MAKEFILE=1 . > config.log 2>&1

gmake -j$CPUS
cd ..


%install
rm -rf $RPM_BUILD_ROOT

#%ifarch amd64 sparcv9
#cd OpenSceneGraph-%{version}-64
#
#gmake DESTDIR=$RPM_BUILD_ROOT install
#cd ..
#%endif

cd OpenSceneGraph-%{version}
gmake DESTDIR=$RPM_BUILD_ROOT install
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%dir %attr (0755, root, bin) %{_libdir}/osgPlugins-%{version}
%{_libdir}/osgPlugins-%{version}/*.so*

#%ifarch amd64 sparcv9
#%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
#%{_libdir}/%{_arch64}/*.a
#%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, bin) %{_includedir}/osgSim
%{_includedir}/osgSim/*
%dir %attr (0755, root, bin) %{_includedir}/osgAnimation
%{_includedir}/osgAnimation/*
%dir %attr (0755, root, bin) %{_includedir}/osgVolume
%{_includedir}/osgVolume/*
%dir %attr (0755, root, bin) %{_includedir}/osgText
%{_includedir}/osgText/*
%dir %attr (0755, root, bin) %{_includedir}/osgShadow
%{_includedir}/osgShadow/*
%dir %attr (0755, root, bin) %{_includedir}/osgUtil
%{_includedir}/osgUtil/*
%dir %attr (0755, root, bin) %{_includedir}/osgDB
%{_includedir}/osgDB/*
%dir %attr (0755, root, bin) %{_includedir}/osgParticle
%{_includedir}/osgParticle/*
%dir %attr (0755, root, bin) %{_includedir}/osgFX
%{_includedir}/osgFX/*
%dir %attr (0755, root, bin) %{_includedir}/osg
%{_includedir}/osg/*
%dir %attr (0755, root, bin) %{_includedir}/osgGA
%{_includedir}/osgGA/*
%dir %attr (0755, root, bin) %{_includedir}/osgViewer
%{_includedir}/osgViewer/*
%dir %attr (0755, root, bin) %{_includedir}/osgTerrain
%{_includedir}/osgTerrain/*
%dir %attr (0755, root, bin) %{_includedir}/osgWidget
%{_includedir}/osgWidget/*
%dir %attr (0755, root, bin) %{_includedir}/osgManipulator
%{_includedir}/osgManipulator/*
%dir %attr (0755, root, bin) %{_includedir}/OpenThreads
%{_includedir}/OpenThreads/*

%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Mon Nov 02 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Initial version.
