#
# spec file for package SFEkoffice
#
# includes module(s): koffice
#
# No 64Bit build yet since Phonon and dependency GStreamer are still 32Bit
#
%include Solaris.inc
%include base.inc

%define have_kivio 0
%define have_kexi 0
%define have_kformula 1
%define have_kugar 0

%define src_dir          koffice
%define python_version   2.6
Name:                    SFEkoffice
Summary:                 Base package for KOffice an integrated office suite for KDE (2.1Beta2).
Version:                 2.0.91
License:                 GPLv2
URL:                     http://www.koffice.org/
Source:                  ftp://gd.tuwien.ac.at/kde/unstable/koffice-%{version}/src/koffice-%{version}.tar.bz2
Patch1:                  koffice-01-math.diff
Patch2:                  koffice-02-CS.diff

SUNW_BaseDir:            /
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SFEkdelibs4
Requires:      SFEkdepimlibs4
Requires:      SFEkdebase4-workspace
Requires:      SFEkdebase4-runtime
Requires:      SFEexiv2
Requires:      SUNWbzip
Requires:      SFEfreeglut
Requires:      SFEglew
Requires:      SFEgraphicsmagick
Requires:      SFEgsl
Requires:      SFElcms
Requires:      SUNWxorg-mesa
Requires:      SFEkdegraphics4
Requires:      SFEwpd
Requires:      SFEwpg
Requires:      SUNWlxsl
Requires:      SUNWmysql51r
Requires:      SUNWmysql51u
Requires:      SFElibpqxx
Requires:      SFEpoppler
Requires:      SFEpstoedit
Requires:      SFEqca
Requires:      SFEreadline
Requires:      SFEwv2
BuildRequires: SFEkdelibs4-devel
BuildRequires: SFEkdepimlibs4-devel
BuildRequires: SFEkdebase4-workspace-devel
BuildRequires: SFEautomoc
BuildRequires: SFEcmake
BuildRequires: SFEkdebase4-runtime
BuildRequires: SFEeigen
BuildRequires: SFEexiv2-devel
BuildRequires: SFEfreeglut-devel
BuildRequires: SFEglew
BuildRequires: SFEgmm
BuildRequires: SUNWgnome-desktop-prefs
BuildRequires: SFEgraphicsmagick-devel
BuildRequires: SFEgsl-devel
BuildRequires: SFElcms-devel
BuildRequires: FSWxorg-headers
BuildRequires: SFEkdegraphics4-devel
BuildRequires: SFEwpd-devel
BuildRequires: SFEwpg-devel
BuildRequires: SUNWlxsl-devel
BuildRequires: SUNWmysql51u
BuildRequires: SFElibpqxx-devel
BuildRequires: SFEpoppler-devel
BuildRequires: SFEpstoedit-devel
BuildRequires: SFEqca-devel
BuildRequires: SFEreadline-devel
BuildRequires: SFEwv2-devel
Conflicts:     SFEkoffice3
BuildConflicts: SFEkoffice3-devel

%description
KOffice is an integrated office suite for KDE.

%package -n SFEkoffice-devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            /
%include default-depend.inc
Requires:      %name
Requires:      SFEkdelibs4-devel
Requires:      SFEkdepimlibs4-devel
Requires:      SFEkdebase4-workspace-devel
Requires:      SFEautomoc
Requires:      SFEcmake
Requires:      SFEkdebase4-runtime
Requires:      SFEeigen
Requires:      SFEexiv2-devel
Requires:      SFEfreeglut-devel
Requires:      SFEglew
Requires:      SFEgmm
Requires:      SUNWgnome-desktop-prefs
Requires:      SFEgraphicsmagick-devel
Requires:      SFEgsl-devel
Requires:      SFElcms-devel
Requires:      FSWxorg-headers
Requires:      SFEwpd-devel
Requires:      SUNWlxsl-devel
Requires:      SUNWmysql51u
Requires:      SFElibpqxx-devel
Requires:      SFEpoppler-devel
Requires:      SFEpstoedit-devel
Requires:      SFEqca-devel
Requires:      SFEreadline-devel
Requires:      SFEwv2-devel
Conflicts: SFEkoffice3-devel

%package -n SFEkoffice-kword
Summary:        A frame-based word processor in KOffice suite
SUNW_BaseDir:   /
%include default-depend.inc
Requires: %name
Conflicts:     SFEkoffice3-kword

%package -n SFEkoffice-kspread
Summary:        A powerful spreadsheet application in KOffice suite
SUNW_BaseDir:   /
%include default-depend.inc
Requires: %name
Conflicts:     SFEkoffice3-kspread

%package -n SFEkoffice-kpresenter
Summary:        A full-featured presentation program in KOffice suite
SUNW_BaseDir:   /
%include default-depend.inc
Requires: %name
Conflicts:     SFEkoffice3-kpresenter

%if %{?have_kexi}
%package -n SFEkoffice-kexi
Summary:        An integrated environment for databases and database applications in KOffice suite
SUNW_BaseDir:   /
%include default-depend.inc
Requires: %name
Conflicts:     SFEkoffice3-kexi
%endif

%if %{?have_kivio}
%package -n SFEkoffice-kivio
Summary:        A Visio(R)-style flowcharting application in KOffice suite
SUNW_BaseDir:   /
%include default-depend.inc
Requires: %name
Conflicts:     SFEkoffice3-kivio
%endif

%package -n SFEkoffice-karbon
Summary:        A vector drawing application in KOffice suite
SUNW_BaseDir:   /
%include default-depend.inc
Requires: %name
Conflicts:     SFEkoffice3-karbon14

%package -n SFEkoffice-krita
Summary:        A layered pixel image manipulation application in KOffice suite
SUNW_BaseDir:   /
%include default-depend.inc
Requires: %name
Conflicts:     SFEkoffice3-krita

%package -n SFEkoffice-kplato
Summary:        An integrated project management and planning tool in KOffice suite
SUNW_BaseDir:   /
%include default-depend.inc
Requires: %name
Conflicts:     SFEkoffice3-kplato

%package -n SFEkoffice-kchart
Summary:        An integrated graph and chart drawing tool in KOffice suite
SUNW_BaseDir:   /
%include default-depend.inc
Requires: %name
Conflicts:     SFEkoffice3-kchart

%if %{?have_kformula}
%package -n SFEkoffice-kformula
Summary:        A powerful formula editor in KOffice suite
SUNW_BaseDir:   /
%include default-depend.inc
Requires: %name
Conflicts:     SFEkoffice3-kformula
%endif

%if %{?have_kugar}
%package -n SFEkoffice-kugar
Summary:        A tool for generating business quality reports in KOffice suite
SUNW_BaseDir:   /
%include default-depend.inc
Requires: %name
Conflicts:     SFEkoffice3-kugar
%endif

%package -n SFEkoffice-suite
Summary:        The Full Koffice Office Suite
SUNW_BaseDir:   /
%include default-depend.inc
Requires: %name
Requires: SFEkoffice-kchart
Requires: SFEkoffice-kplato
Requires: SFEkoffice-krita
Requires: SFEkoffice-karbon
Requires: SFEkoffice-kpresenter
Requires: SFEkoffice-kspread
Requires: SFEkoffice-kword
%if %{?have_kexi}
Requires: SFEkoffice-kexi
%endif
%if %{?have_kivio}
Requires: SFEkoffice-kivio
%endif
%if %{?have_kformula}
Requires: SFEkoffice-kformula
%endif
%if %{?have_kugar}
Requires: SFEkoffice-kugar
%endif

%prep
%setup -q -c -n %name-%version
cd %{src_dir}-%{version}
%patch1 -p1
%patch2 -p1
cd ..

%build
%define _buildpath %{_builddir}/%{src_dir}-%version
#
# Need to force some shell info to point to bash because the scripts
# are for bash.
#
export SHELL="/bin/bash"
export CONFIG_SHELL="/bin/bash"
export MAKESHELL="/bin/bash"
export GCC="yes"
export CC=%{_prefix}/gnu/bin/gcc
export CXX=%{_prefix}/gnu/bin/g++
export QTDIR=%{_prefix}
export QT_INCLUDES=%{_includedir}/qt4
export CMAKE_INCLUDE_PATH="%{gnu_inc}:%{xorg_inc}"
export JAVA_HOME=%{_prefix}/java
OPATH=${PATH}

mkdir -p kdebld
cd kdebld

#
# SFE paths are needed for libusb
#
export CFLAGS="-march=pentium3 -fno-omit-frame-pointer -fPIC -DPIC -I%{gnu_inc} -I%{sfw_inc} -I%{_prefix}/poppler/include -I%{_prefix}/poppler/include/poppler -DSOLARIS -DUSE_SOLARIS -D__C99FEATURES__"
export CXXFLAGS="-march=pentium3 -fno-omit-frame-pointer -fPIC -DPIC -I%{gnu_inc} -I%{sfw_inc} -I%{_prefix}/poppler/include -I%{_prefix}/poppler/include/poppler -DSOLARIS -DUSE_SOLARIS -D__C99FEATURES__"
export LDFLAGS="%_ldflags -L%{_prefix}/poppler/lib -R%{_prefix}/poppler/lib -lsocket -lnsl -L/lib -R/lib %{gnu_lib_path} -lstdc++ %{xorg_lib_path} %{sfw_lib_path}"
export PATH="%{qt4_bin_path}:%{_prefix}/sfw/bin:${OPATH}"
export PKG_CONFIG_PATH=%{_prefix}/poppler/lib/pkgconfig:%{_prefix}/lib/pkgconfig:%{_prefix}/gnu/lib/pkgconfig
export CMAKE_LIBRARY_PATH="%{xorg_lib}:%{gnu_lib}:%{_prefix}/lib:/lib:%{sfw_lib}"

cmake   ../%{src_dir}-%{version} -DCMAKE_INSTALL_PREFIX=%{_prefix}      \
        -DCMAKE_BUILD_TYPE=Release                                      \
        -DCMAKE_C_COMPILER:FILEPATH=${CC}                               \
        -DCMAKE_C_FLAGS:STRING="${CFLAGS}"                              \
        -DCMAKE_CXX_COMPILER:FILEPATH=${CXX}                            \
        -DCMAKE_CXX_FLAGS_RELEASE:STRING="${CXXFLAGS}"                  \
        -DCMAKE_INCLUDE_PATH="%{gnu_inc}"				\
        -DCMAKE_SKIP_RPATH:BOOL=YES                                     \
        -DINCLUDE_INSTALL_DIR=%{_includedir}                            \
        -DSYSCONF_INSTALL_DIR=%{_sysconfdir}                            \
        -DDBUS_INTERFACES_INSTALL_DIR=%{_datadir}/dbus-1/interfaces     \
        -DDBUS_SERVICES_INSTALL_DIR=%{_datadir}/dbus-1/services         \
        -DBOOST_INCLUDEDIR=%{_includedir}/boost/gcc4                    \
        -DBOOST_LIBRARYDIR=%{_libdir}/boost/gcc4                        \
        -DMYSQL_INCLUDE_DIR:PATH=%{_prefix}/mysql/5.1/include/mysql     \
        -DMYSQL_LIBRARIES:FILEPATH=%{_prefix}/mysql/5.1/lib/mysql/libmysqlclient.so \
        -DPOPPLER_INCLUDE_DIR=%{_prefix}/poppler/include                \
        -DPOPPLER_LIBRARY=%{_prefix}/poppler/lib/libpoppler-qt4.so      \
        -DBUILD_SHARED_LIBS=On                                          \
        -DKDE4_ENABLE_HTMLHANDBOOK=On                                   \
        -DCMAKE_VERBOSE_MAKEFILE=1 > config.log 2>&1

make VERBOSE=1
cd ..
export PATH="${OPATH}"


%install
rm -rf $RPM_BUILD_ROOT
OPATH=${PATH}
cd kdebld
export PATH="%{qt4_bin_path}:${OPATH}"
make install DESTDIR=$RPM_BUILD_ROOT

BLDPATH=`pwd`
export BLDPATH

(cd $RPM_BUILD_ROOT
 find usr/include usr/share/apps/cmake > $BLDPATH/devel.files
%if %{?have_kexi}
%else
 find * -type d | egrep "kexi$" | xargs rm -f
%endif
%if %{?have_kivio}
%else
 find * -type d | grep 'kivio$' | xargs rm -rf
 find * -type f | grep 'kivio' | xargs rm -f
%endif
%if %{?have_kformula}
%else
 find * -type d | grep 'kformula$' | xargs rm -rf
%endif
)

# conflicts with oxygen-icon-theme  
rm -f $RPM_BUILD_ROOT%{_datadir}/icons/oxygen/16x16/actions/format-justify-{center,fill,left,right}.png
rm -f $RPM_BUILD_ROOT%{_datadir}/icons/oxygen/16x16/actions/format-text-{bold,italic,underline}.png
rm -f $RPM_BUILD_ROOT%{_datadir}/icons/oxygen/16x16/actions/object-{group,ungroup}.png
rm -f $RPM_BUILD_ROOT%{_datadir}/icons/oxygen/16x16/actions/object-order-{back,front,lower,raise}.png


export PATH="${OPATH}"
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/kthesaurus
%{_bindir}/koconverter
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libkdeinit4_kthesaurus*
%{_libdir}/libflake.so*
%{_libdir}/libchartshapelib.so*
%{_libdir}/libkdchart.so*
%{_libdir}/libkoaction.so*
%{_libdir}/libkobase.so*
%{_libdir}/libkochart.so*
%{_libdir}/libkocolorwidgets.so*
%{_libdir}/libkoffice_graya_u16.so*
%{_libdir}/libkofficegrayau8colorspace.so*
%{_libdir}/libkokross.so*
%{_libdir}/libkomain.so*
%{_libdir}/libkoodf.so*
%{_libdir}/libkopageapp.so*
%{_libdir}/libkoplugin.so*
%{_libdir}/libkoresources.so*
%{_libdir}/libkostore.so*
%{_libdir}/libkotext.so*
%{_libdir}/libkowidgets.so*
%{_libdir}/libkowmf.so*
%{_libdir}/libkspreadcommon.so*
%{_libdir}/libkwmf.so*
%{_libdir}/libpigmentcms.so*
%{_libdir}/libkwordexportfilters.so*

%if %{?have_kformula}
%{_libdir}/libkformulalib.so*
%endif

%dir %attr (0755, root, bin) %{_libdir}/kde4
%{_libdir}/kde4/autocorrect.so
%{_libdir}/kde4/changecase.so
%{_libdir}/kde4/clipartthumbnail.*
%{_libdir}/kde4/defaulttools.so
%{_libdir}/kde4/kodocinfopropspage.*
%{_libdir}/kde4/kofficescan.*
%{_libdir}/kde4/kofficethumbnail.*
%{_libdir}/kde4/kopabackgroundtool.*
%{_libdir}/kde4/koffice_graya_u16_plugin.so
%{_libdir}/kde4/kofficegrayau8plugin.so
%{_libdir}/kde4/kofficedockers.so
#%{_libdir}/kde4/kofficesimpletextedit.so
%{_libdir}/kde4/libkounavailpart.*
%{_libdir}/kde4/paragraphtool.so
%{_libdir}/kde4/spellcheck.so
%{_libdir}/kde4/textvariables.so
%{_libdir}/kde4/thesaurustool.so
%{_libdir}/kde4/artistictextshape.so
%{_libdir}/kde4/chartshape.so
%{_libdir}/kde4/divineproportionshape.so
%{_libdir}/kde4/kpr_shapeanimation_example.so
%{_libdir}/kde4/musicshape.so
%{_libdir}/kde4/pictureshape.so
%{_libdir}/kde4/spreadsheetshape.so
%{_libdir}/kde4/textshape.so
%{_libdir}/kde4/pathshapes.so
%{_libdir}/kde4/libabiwordexport.*
%{_libdir}/kde4/libabiwordimport.*
%{_libdir}/kde4/libamiproexport.*
%{_libdir}/kde4/libamiproimport.*
%{_libdir}/kde4/libapplixspreadimport.*
%{_libdir}/kde4/libapplixwordimport.*
%{_libdir}/kde4/libasciiexport.*
%{_libdir}/kde4/libasciiimport.*
%{_libdir}/kde4/libdbaseimport.*
%{_libdir}/kde4/libdocbookexport.*
%{_libdir}/kde4/libexcelimport.*
%{_libdir}/kde4/libgenerickofilter.*
%{_libdir}/kde4/libhtmlexport.*
%{_libdir}/kde4/libhtmlimport.*
%{_libdir}/kde4/libkspreadlatexexport.*
%{_libdir}/kde4/libkwordkword1dot3import.*
#%{_libdir}/kde4/libmswordodf_import.*
%{_libdir}/kde4/libmswriteexport.*
%{_libdir}/kde4/libmswriteimport.*
%{_libdir}/kde4/liboowriterexport.*
%{_libdir}/kde4/liboowriterimport.*
%{_libdir}/kde4/libpalmdocexport.*
%{_libdir}/kde4/libpalmdocimport.*
%{_libdir}/kde4/libpowerpointimport.*
%{_libdir}/kde4/librtfexport.*
%{_libdir}/kde4/librtfimport.*
%{_libdir}/kde4/libwmlexport.*
%{_libdir}/kde4/libwmlimport.*
%{_libdir}/kde4/libwpexport.*
%{_libdir}/kde4/libwpgimport.*
%{_libdir}/kde4/libwpimport.*
%{_libdir}/kde4/libxsltimport.*
%{_libdir}/kde4/libxsltexport.*
%{_libdir}/kde4/libhancomwordimport.*


%if %{?have_kformula}
%{_libdir}/kde4/formulashape.*
%endif

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/kde4
%dir %attr (0755, root, bin) %{_datadir}/kde4/services
%{_datadir}/kde4/services/autocorrect.desktop
%{_datadir}/kde4/services/changecase.desktop
%{_datadir}/kde4/services/clipartthumbnail.desktop
%{_datadir}/kde4/services/defaulttools.desktop
%{_datadir}/kde4/services/kodocinfopropspage.desktop
%{_datadir}/kde4/services/kofficethumbnail.desktop
%{_datadir}/kde4/services/koffice_graya_u16_plugin.desktop
%{_datadir}/kde4/services/kofficegrayaplugin.desktop
%{_datadir}/kde4/services/kofficedockers.desktop
%{_datadir}/kde4/services/kopabackgroundtool.desktop
%{_datadir}/kde4/services/kounavail.desktop
#%{_datadir}/kde4/services/kofficesimpletextedit.desktop
%{_datadir}/kde4/services/paragraphtool.desktop
%{_datadir}/kde4/services/spellcheck.desktop
%{_datadir}/kde4/services/textvariables.desktop
%{_datadir}/kde4/services/thesaurustool.desktop
%{_datadir}/kde4/services/pathshapes.desktop
%{_datadir}/kde4/services/pictureshape.desktop
%{_datadir}/kde4/services/artistictextshape.desktop
%{_datadir}/kde4/services/textshape.desktop
%{_datadir}/kde4/services/musicshape.desktop
%{_datadir}/kde4/services/spreadsheetshape.desktop
%{_datadir}/kde4/services/chartshape.desktop
%{_datadir}/kde4/services/divineproportionshape.desktop
%{_datadir}/kde4/services/generic_filter.desktop
%{_datadir}/kde4/services/xslt*.desktop
%if %{?have_kformula}
%{_datadir}/kde4/services/*formulashape*
%endif

%dir %attr (0755, root, bin) %{_datadir}/kde4/servicetypes
%{_datadir}/kde4/servicetypes/filtereffect.desktop
%{_datadir}/kde4/servicetypes/kochart.desktop
%{_datadir}/kde4/servicetypes/kofficedocker.desktop
%{_datadir}/kde4/servicetypes/kofficepart.desktop
%{_datadir}/kde4/servicetypes/koplugin.desktop
%{_datadir}/kde4/servicetypes/inlinetextobject.desktop
%{_datadir}/kde4/servicetypes/texteditingplugin.desktop
%{_datadir}/kde4/servicetypes/textvariableplugin.desktop
%{_datadir}/kde4/servicetypes/pigment*.desktop
%{_datadir}/kde4/servicetypes/flake*.desktop
%{_datadir}/kde4/servicetypes/kofilter*.desktop

%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, bin) %{_datadir}/doc/HTML
%dir %attr (0755, root, bin) %{_datadir}/doc/HTML/en
%{_datadir}/doc/HTML/en/koffice
%{_datadir}/doc/HTML/en/thesaurus

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_datadir}/apps/koffice
%{_datadir}/apps/koffice/*
%dir %attr (0755, root, other) %{_datadir}/applications
%dir %attr (0755, root, other) %{_datadir}/applications/kde4
%{_datadir}/applications/kde4/KThesaurus.desktop
%{_datadir}/applications/kde4/koffice.desktop

%dir %attr (0755, root, other) %{_datadir}/apps
%if %{?have_kformula}
%dir %attr (0755, root, other) %{_datadir}/apps/formulashape
%{_datadir}/apps/formulashape/*
%endif
%dir %attr (0755, root, other) %{_datadir}/apps/musicshape
%{_datadir}/apps/musicshape/*
%dir %attr (0755, root, other) %{_datadir}/apps/cmake
%{_datadir}/apps/cmake/*
%dir %attr (0755, root, other) %{_datadir}/apps/xsltfilter
%{_datadir}/apps/xsltfilter/*
%dir %attr (0755, root, other) %{_datadir}/color
%dir %attr (0755, root, other) %{_datadir}/color/icc
%dir %attr (0755, root, other) %{_datadir}/color/icc/pigment
%{_datadir}/color/icc/pigment/*
%dir %attr (0755, root, other) %{_datadir}/icons
%{_datadir}/icons/*

%files -n SFEkoffice-devel
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_datadir}/apps
%dir %attr (0755, root, other) %{_datadir}/apps/cmake
%dir %attr (0755, root, other) %{_datadir}/apps/cmake/modules
%{_datadir}/apps/cmake/modules/*

%files -n SFEkoffice-kword
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/kword
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libkdeinit4_kword.so
%{_libdir}/libkwordprivate.so*

%dir %attr (0755, root, bin) %{_libdir}/kde4
%{_libdir}/kde4/krossmodulekword.so
%{_libdir}/kde4/libkwordpart.*

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, bin) %{_datadir}/doc/HTML
%dir %attr (0755, root, bin) %{_datadir}/doc/HTML/en
#%{_datadir}/doc/HTML/en/kword
%dir %attr (0755, root, bin) %{_datadir}/kde4
%dir %attr (0755, root, bin) %{_datadir}/kde4/services
%{_datadir}/kde4/services/*kword*.desktop
%dir %attr (0755, root, bin) %{_datadir}/kde4/services/ServiceMenus
%{_datadir}/kde4/services/ServiceMenus/kword_konqi.desktop

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_datadir}/config
%{_datadir}/config/kwordrc
%dir %attr (0755, root, other) %{_datadir}/apps
%dir %attr (0755, root, other) %{_datadir}/apps/kword
%{_datadir}/apps/kword/*
%dir %attr (0755, root, sys) %{_datadir}/templates
%{_datadir}/templates/TextDocument.desktop
%dir %attr (0755, root, sys) %{_datadir}/templates/.source
%{_datadir}/templates/.source/TextDocument.kwt
%dir %attr (0755, root, other) %{_datadir}/applications
%dir %attr (0755, root, other) %{_datadir}/applications/kde4
%{_datadir}/applications/kde4/*kword.desktop

%files -n SFEkoffice-kspread
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/kspread
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libkdeinit4_kspread.so

%dir %attr (0755, root, bin) %{_libdir}/kde4
%{_libdir}/kde4/krossmodulekspread.so
%{_libdir}/kde4/kspread*.so
%{_libdir}/kde4/libkspreadpart.*
%{_libdir}/kde4/libcsvexport.*
%{_libdir}/kde4/libcsvimport.*
%{_libdir}/kde4/libgnumericexport.*
%{_libdir}/kde4/libgnumericimport.*
%{_libdir}/kde4/libkspreadhtmlexport.*
%{_libdir}/kde4/libkspreadsolver.so
%{_libdir}/kde4/libopencalcexport.*
%{_libdir}/kde4/libopencalcimport.*
%{_libdir}/kde4/libqproimport.*

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, bin) %{_datadir}/doc/HTML
%dir %attr (0755, root, bin) %{_datadir}/doc/HTML/en
%{_datadir}/doc/HTML/en/kspread
%dir %attr (0755, root, bin) %{_datadir}/kde4
%dir %attr (0755, root, bin) %{_datadir}/kde4/services
%{_datadir}/kde4/services/krossmodulekspread.desktop
%{_datadir}/kde4/services/kspread*.desktop
%dir %attr (0755, root, bin) %{_datadir}/kde4/services/ServiceMenus
%{_datadir}/kde4/services/ServiceMenus/kspread_konqi.desktop
%dir %attr (0755, root, bin) %{_datadir}/kde4/servicetypes
%{_datadir}/kde4/servicetypes/kspread_plugin.desktop

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_datadir}/config.kcfg
%{_datadir}/config.kcfg/kspread.kcfg
%dir %attr (0755, root, other) %{_datadir}/apps
%dir %attr (0755, root, other) %{_datadir}/apps/kspread
%{_datadir}/apps/kspread/*
%dir %attr (0755, root, sys) %{_datadir}/templates
%{_datadir}/templates/SpreadSheet.desktop
%dir %attr (0755, root, sys) %{_datadir}/templates/.source
%{_datadir}/templates/.source/SpreadSheet.kst
%dir %attr (0755, root, other) %{_datadir}/applications
%dir %attr (0755, root, other) %{_datadir}/applications/kde4
%{_datadir}/applications/kde4/*kspread.desktop

%files -n SFEkoffice-kpresenter
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/kpresenter
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libkdeinit4_kpresenter.so
%{_libdir}/libkpresenterprivate.so*

%dir %attr (0755, root, bin) %{_libdir}/kde4
%{_libdir}/kde4/*kpresenter*.*
%{_libdir}/kde4/kpr_*.*
%{_libdir}/kde4/libFilterkpr2odf.so

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, bin) %{_datadir}/doc/HTML
%dir %attr (0755, root, bin) %{_datadir}/doc/HTML/en
%{_datadir}/doc/HTML/en/kpresenter
%dir %attr (0755, root, bin) %{_datadir}/kde4
%dir %attr (0755, root, bin) %{_datadir}/kde4/services
%{_datadir}/kde4/services/kpr*.desktop
%{_datadir}/kde4/services/Filterkpr2odf.desktop
%dir %attr (0755, root, bin) %{_datadir}/kde4/services/ServiceMenus
%{_datadir}/kde4/services/ServiceMenus/kpresenter_konqi.desktop
%dir %attr (0755, root, bin) %{_datadir}/kde4/servicetypes
%{_datadir}/kde4/servicetypes/kpr*.desktop
%{_datadir}/kde4/servicetypes/presentationeventaction.desktop
%{_datadir}/kde4/servicetypes/scripteventaction.desktop

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_datadir}/config
%{_datadir}/config/kpresenterrc
%dir %attr (0755, root, other) %{_datadir}/apps
%dir %attr (0755, root, other) %{_datadir}/apps/kpresenter
%{_datadir}/apps/kpresenter/*
%dir %attr (0755, root, sys) %{_datadir}/templates
%{_datadir}/templates/Presentation.desktop
%dir %attr (0755, root, sys) %{_datadir}/templates/.source
%{_datadir}/templates/.source/Presentation.kpt
%dir %attr (0755, root, other) %{_datadir}/applications
%dir %attr (0755, root, other) %{_datadir}/applications/kde4
%{_datadir}/applications/kde4/*kpresenter.desktop

%files -n SFEkoffice-karbon
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/karbon
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libkdeinit4_karbon.so
%{_libdir}/libkarboncommon.so*
%{_libdir}/libkarbonui.so*

%dir %attr (0755, root, bin) %{_libdir}/kde4
%{_libdir}/kde4/*karbon*.*
%{_libdir}/kde4/libwmfexport.*
%{_libdir}/kde4/libwmfimport.*

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, bin) %{_datadir}/doc/HTML
%dir %attr (0755, root, bin) %{_datadir}/doc/HTML/en
%{_datadir}/doc/HTML/en/karbon
%dir %attr (0755, root, bin) %{_datadir}/kde4
%dir %attr (0755, root, bin) %{_datadir}/kde4/services
%{_datadir}/kde4/services/karbon*
%dir %attr (0755, root, bin) %{_datadir}/kde4/servicetypes
%{_datadir}/kde4/servicetypes/karbon_module.desktop
%dir %attr (0755, root, bin) %{_datadir}/kde4/services/ServiceMenus
%{_datadir}/kde4/services/ServiceMenus/karbon_konqi.desktop

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_datadir}/config
%{_datadir}/config/karbonrc
%dir %attr (0755, root, other) %{_datadir}/apps
%dir %attr (0755, root, other) %{_datadir}/apps/karbon
%{_datadir}/apps/karbon/*
%dir %attr (0755, root, sys) %{_datadir}/templates
%{_datadir}/templates/Illustration.desktop
%dir %attr (0755, root, sys) %{_datadir}/templates/.source
%{_datadir}/templates/.source/Illustration.karbon
%dir %attr (0755, root, other) %{_datadir}/applications
%dir %attr (0755, root, other) %{_datadir}/applications/kde4
%{_datadir}/applications/kde4/*karbon.desktop

%files -n SFEkoffice-krita
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/krita
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libkdeinit4_krita.so
%{_libdir}/libkrita*.so*
#%{_libdir}/libkrossmodulekrita*

%dir %attr (0755, root, bin) %{_libdir}/kde4
%{_libdir}/kde4/*krita*

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, bin) %{_datadir}/doc/HTML
%dir %attr (0755, root, bin) %{_datadir}/doc/HTML/en
%{_datadir}/doc/HTML/en/krita
%dir %attr (0755, root, bin) %{_datadir}/kde4
%dir %attr (0755, root, bin) %{_datadir}/kde4/services
%{_datadir}/kde4/services/krita*
%dir %attr (0755, root, bin) %{_datadir}/kde4/servicetypes
%{_datadir}/kde4/servicetypes/krita*
%dir %attr (0755, root, bin) %{_datadir}/kde4/services/ServiceMenus
%{_datadir}/kde4/services/ServiceMenus/krita_konqi.desktop
%dir %attr (0755, root, root) %{_datadir}/mime
%dir %attr (0755, root, root) %{_datadir}/mime/packages
%attr (0755, root, root) %{_datadir}/mime/packages/krita_ora.xml

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_datadir}/config
%{_datadir}/config/kritarc
%dir %attr (0755, root, other) %{_datadir}/apps
%dir %attr (0755, root, other) %{_datadir}/apps/krita
%{_datadir}/apps/krita/*
%dir %attr (0755, root, other) %{_datadir}/apps/kritaplugins
%{_datadir}/apps/kritaplugins/*
%dir %attr (0755, root, other) %{_datadir}/applications
%dir %attr (0755, root, other) %{_datadir}/applications/kde4
%{_datadir}/applications/kde4/*krita*
%dir %attr (0755, root, other) %{_datadir}/color
%dir %attr (0755, root, other) %{_datadir}/color/icc
%dir %attr (0755, root, other) %{_datadir}/color/icc/krita
%{_datadir}/color/icc/krita/*

%files -n SFEkoffice-kplato
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/kplato
%{_bindir}/kplatowork
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libkdeinit4_kplato.so
%{_libdir}/libkdeinit4_kplatowork.so
%{_libdir}/libkplato*.so*

%dir %attr (0755, root, bin) %{_libdir}/kde4
%{_libdir}/kde4/libkplatopart.*
%{_libdir}/kde4/libkplatoworkpart.so
%{_libdir}/kde4/libicalendarexport.*
%{_libdir}/kde4/krossmodulekplato.so

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, bin) %{_datadir}/doc/HTML
%dir %attr (0755, root, bin) %{_datadir}/doc/HTML/en
%{_datadir}/doc/HTML/en/kplato
%dir %attr (0755, root, bin) %{_datadir}/kde4
%dir %attr (0755, root, bin) %{_datadir}/kde4/services
%{_datadir}/kde4/services/kplato*.desktop
%{_datadir}/kde4/services/krossmodulekplato.desktop
%dir %attr (0755, root, bin) %{_datadir}/kde4/servicetypes
%{_datadir}/kde4/servicetypes/kplato*.desktop

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_datadir}/config
%{_datadir}/config/kplatorc
%{_datadir}/config/kplatoworkrc
%dir %attr (0755, root, other) %{_datadir}/config.kcfg
%{_datadir}/config.kcfg/kplatosettings.kcfg
%dir %attr (0755, root, other) %{_datadir}/apps
%dir %attr (0755, root, other) %{_datadir}/apps/kplato
%{_datadir}/apps/kplato/*
%dir %attr (0755, root, other) %{_datadir}/apps/kplatowork
%{_datadir}/apps/kplatowork/*
%dir %attr (0755, root, other) %{_datadir}/applications
%dir %attr (0755, root, other) %{_datadir}/applications/kde4
%{_datadir}/applications/kde4/kplato.desktop
%{_datadir}/applications/kde4/kplatowork.desktop

%files -n SFEkoffice-kchart
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_bindir}
#%{_bindir}/kchart
%dir %attr (0755, root, bin) %{_libdir}
#%{_libdir}/libkdeinit4_kchart.so
%{_libdir}/libkchartcommon.so*

%dir %attr (0755, root, bin) %{_libdir}/kde4
%{_libdir}/kde4/*kchart*

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, bin) %{_datadir}/doc/HTML
%dir %attr (0755, root, bin) %{_datadir}/doc/HTML/en
%{_datadir}/doc/HTML/en/kchart
%dir %attr (0755, root, bin) %{_datadir}/kde4
%dir %attr (0755, root, bin) %{_datadir}/kde4/services
%{_datadir}/kde4/services/kchart*
%dir %attr (0755, root, bin) %{_datadir}/kde4/services/ServiceMenus
%{_datadir}/kde4/services/ServiceMenus/kchart_konqi.desktop

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_datadir}/config.kcfg
#%{_datadir}/config.kcfg/kchart.kcfg
%dir %attr (0755, root, other) %{_datadir}/apps
%dir %attr (0755, root, other) %{_datadir}/apps/kchart
%{_datadir}/apps/kchart/*
%dir %attr (0755, root, other) %{_datadir}/applications
%dir %attr (0755, root, other) %{_datadir}/applications/kde4
#%{_datadir}/applications/kde4/kchart*

%if %{?have_kformula}
%files -n SFEkoffice-kformula
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/kformula
%dir %attr (0755, root, bin) %{_libdir}
#%{_libdir}/libkdeinit4_kformula.so
%{_libdir}/libkdeinit_kformula.so
%{_libdir}/libkformulaprivate.so*

%dir %attr (0755, root, bin) %{_libdir}/kde4
%{_libdir}/kde4/*kformula*

%dir %attr (0755, root, sys) %{_datadir}
#%dir %attr (0755, root, other) %{_datadir}/doc
#%dir %attr (0755, root, bin) %{_datadir}/doc/HTML
#%dir %attr (0755, root, bin) %{_datadir}/doc/HTML/en
#%{_datadir}/doc/HTML/en/kformula
%dir %attr (0755, root, bin) %{_datadir}/kde4
%dir %attr (0755, root, bin) %{_datadir}/kde4/services
%{_datadir}/kde4/services/kformula*.desktop
%dir %attr (0755, root, bin) %{_datadir}/kde4/services/ServiceMenus
%{_datadir}/kde4/services/ServiceMenus/kformula_konqi.desktop

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_datadir}/apps
#%dir %attr (0755, root, other) %{_datadir}/apps/kformula
#%{_datadir}/apps/kformula/*
%dir %attr (0755, root, other) %{_datadir}/applications
%dir %attr (0755, root, other) %{_datadir}/applications/kde4
%{_datadir}/applications/kde4/*kformula.desktop
%endif

%files -n SFEkoffice-suite
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}

%changelog
* Sun Nov 08 2009 - Moinak Ghosh
- Bump to 2.1 RC1.
* Mon Sep 28 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Initial version.
