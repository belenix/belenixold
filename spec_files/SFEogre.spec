#
# spec file for package SFEogre.spec
#
# includes module(s): ogre
#
%include Solaris.inc

%define src_name	ogre
%define src_url		%{sf_download}/ogre
%define glew_version    1.5.1

Name:                   SFEogre
Summary:                Object-Oriented Graphics Rendering Engine
Version:                1-6-4
License:                LGPLv2+ and CC-BY-SA and Freely redistributable without restriction and MIT
Group:                  System Environment/Libraries
URL:                    http://www.ogre3d.org/

Source:                 %{src_url}/%{src_name}-v%{version}.tar.bz2
Source1:                %{sf_download}/glew/glew-%{glew_version}-src.tgz
Patch1:			ogre-01-rpath.diff
Patch2:			ogre-02-glew.diff
Patch3:			ogre-03-solaris.diff

SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEopenexr-devel
Requires: SFEopenexr
BuildRequires: SFEcegui-devel
Requires: SFEcegui
BuildRequires: SFEfreeimage-devel
Requires: SFEfreeimage
BuildRequires: SFEzziplib-devel
Requires: SFEzziplib
BuildRequires: SFEcal3d-devel
Requires: SFEcal3d
Requires: SUNWfreetype2
Requires: SUNWxorg-mesa
BuildRequires: SFEglew
BuildRequires: SUNWesu

%description
OGRE (Object-Oriented Graphics Rendering Engine) is a scene-oriented,
flexible 3D engine written in C++ designed to make it easier and more
intuitive for developers to produce applications utilising
hardware-accelerated 3D graphics. The class library abstracts all the
details of using the underlying system libraries like Direct3D and
OpenGL and provides an interface based on world objects and other
intuitive classes.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
%setup -q -c -n %name-%version
gunzip -c %{SOURCE1} | tar xf -

cd ogre
%patch1 -p1
%patch3 -p1

# - Non-free licensed headers under RenderSystems/GL/include/GL removed
rm RenderSystems/GL/include/GL/{gl,glext,glxext,glxtokens,wglext}.h

# - GLEW sources update to 1.5.1
cp -f ../glew/include/GL/{glew,glxew,wglew}.h RenderSystems/GL/include/GL/
dos2unix ../glew/src/glew.c > RenderSystems/GL/src/glew.cpp
%patch2 -p1

# - Non-free chiropteraDM.pk3 under Samples/Media/packs removed
rm Samples/Media/packs/chiropteraDM.{pk3,txt}

# - Non-free fonts under Samples/Media/fonts removed
rm Samples/Media/fonts/{bluebold,bluecond,bluehigh,solo5}.ttf

# Fix path to Media files for the Samples
sed -i 's|../../Media|%{_datadir}/OGRE/Samples/Media|g' \
    Samples/Common/bin/resources.cfg

# Remove spurious execute buts from some Media files
chmod -x `find Samples/Media/DeferredShadingMedia -type f` \
    Samples/Media/overlays/Example-DynTex.overlay \
    Samples/Media/gui/TaharezLook.looknfeel \
    Samples/Media/gui/Falagard.xsd \
    Samples/Media/materials/scripts/Example-DynTex.material 

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

cd ogre
ln -s `which automake-1.9` automake
ln -s `which aclocal-1.9` aclocal
export PATH=$PWD:$PATH

X11LIBS="-L/usr/X11/lib -R/usr/X11/lib"
export CPPFLAGS="-I/usr/X11/include"
export CXXFLAGS="-O3 -fno-omit-frame-pointer"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -lc $X11LIBS %{gnu_lib_path} -lstdc++"
export LD_OPTIONS="-i"
bash ./bootstrap
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --disable-rpath		\
            --disable-cg                \
            --disable-devil             \
            --enable-openexr            \
            --enable-shared		\
	    --disable-static

# Don't use rpath!
%{gnu_bin}/sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
%{gnu_bin}/sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

# Stop ogre from linking the GL render plugin against the system libOgre
# instead of the just build one.
%{gnu_bin}/sed -i 's|-L%{_libdir}||g' `find . -name Makefile`

gmake -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
cd ogre
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT/%{_libdir}/lib*.*a

# These 2 not really public header files are needed for ogre4j
ginstall -p -m 644 \
    OgreMain/include/OgreOptimisedUtil.h \
    OgreMain/include/OgrePlatformInformation.h \
    $RPM_BUILD_ROOT%{_includedir}/OGRE

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/OGRE

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755,root,bin) %{_libdir}
%dir %attr (0755,root,other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc

%changelog
* Mon Nov 30 2009 - Moinak Ghosh
- Initial version
