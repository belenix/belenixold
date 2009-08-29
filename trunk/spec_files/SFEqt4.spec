
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

%define mysql_dir /usr/mysql/5.1
%define postgres_dir /usr/postgres/8.3

Name:                   SFEqt4
Summary:		Qt4 is an X11 toolkit.
Version:                4.4.3
URL:                    http://www.qtsoftware.com/products/
Source:                 ftp://ftp.trolltech.com/qt/source/qt-x11-opensource-src-%{version}.tar.gz
Source1:                assistant.desktop
Source2:                designer.desktop
Source3:                linguist.desktop
Source4:                qtdemo.desktop
Source5:                qtconfig.desktop

Patch1:                 qt4-01-use_bash.diff
Patch2:                 qt4-02-qglobal.h.diff
Patch3:                 qt4-03-qmutex_unix.cpp.diff
Patch4:                 qt4-04-gnu-libiconv.pro.diff
Patch5:                 qt4-05-fulltextsearch.pro.diff
Patch6:                 qt4-06-freetype.pro.diff
Patch7:                 qt4-07-psql.pro.diff
Patch8:                 qt4-08-fontconfig.pro.diff
Patch9:                 qt4-09-largefile.prf.diff
Patch10:                qt4-10-largefiletest.cpp.diff
Patch11:                qt4-11-main.cpp.diff
Patch12:                qt4-12-phonon.pro.diff
Patch13:                qt4-13-qt.prf.diff
Patch14:                qt4-14-mediaplayer.h.diff
Patch17:                qt4-17-qsql-unicode.diff
Patch18:                qt4-18-thread.pri.diff
Patch19:                qt4-19-regexp.h.diff
Patch20:                qt4-20-arch.pri.diff
Patch21:                qt4-21-xfixes.pro.diff
Patch22:                qt4-22-xcursor.pro.diff

%define src_dir         qt-x11-opensource-src-%{version}
License:		LICENSE.GPL
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires:		SFEgiflib
BuildRequires:		SFElibmng-devel
BuildRequires:		SUNWsqlite3-devel
BuildRequires:		SUNWfontconfig
BuildRequires:		SUNWfreetype2
BuildRequires:		SUNWgnu-libiconv-devel
BuildRequires:          SFEunixodbc
BuildRequires:          SUNWhal
BuildRequires:          SUNWdbus-devel
BuildRequires:          SUNWxorg-headers
BuildRequires:          SFEcups-devel
BuildRequires:          SUNWmysql51u
BuildRequires:		SUNWgnome-media-devel
BuildRequires:		SFEnas-devel
BuildRequires:		SUNWTiff-devel
BuildRequires:          SUNWpng-devel
BuildRequires:          SUNWgnome-media-devel
Requires:               SFEgiflib
Requires:		SFElibmng
Requires:		SUNWxwplt
Requires:		SUNWsqlite3
Requires:		SUNWfontconfig
Requires:		SUNWfreetype2
Requires:		SUNWgnu-libiconv
Requires:               SFEunixodbc
Requires:               SUNWhal
Requires:               SUNWdbus
Requires:               SFEcups
Requires:		SUNWgnome-media
Requires:		SFEnas
Requires:               SUNWmysql51u
Requires:               SUNWTiff
Requires:               SFEgccruntime
Requires:               SUNWpng
Requires:               SUNWgnome-media

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires:               SFEgiflib
Requires:               SFElibmng-devel
Requires:               SUNWsqlite3-devel
Requires:               SUNWfontconfig
Requires:               SUNWfreetype2
Requires:               SUNWgnu-libiconv-devel
Requires:               SFEunixodbc
Requires:               SUNWhal
Requires:               SUNWdbus-devel
Requires:               SUNWxorg-headers
Requires:               SFEcups-devel
Requires:               SUNWmysql51u
Requires:               SUNWgnome-media-devel
Requires:               SFEnas-devel
Requires:               SUNWTiff-devel
Requires:               SUNWpng-devel
Requires:               SUNWgnome-media-devel

%package debug
Summary:                 %{summary} - debug libraries
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %{name}-devel

%package doc
Summary:                 %{summary} - documentation files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -c -n %name-%version
cd %{src_dir}
%patch1 -p10
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
cd ..

%ifarch amd64 sparcv9
cp -rp %{src_dir} %{src_dir}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CC=/usr/gnu/bin/gcc
export CXX=/usr/gnu/bin/g++
OPATH=$PATH
PDIR=`pwd`

#
# Fixup a couple of config scripts for our purpose. We patch
# mysql_config to not report SUN Studio compiler flags/libs
# since we are using Gcc. We delete -lpgport and -ledit from
# pg_config since those two static libs are not needed.
#
mkdir bin
mkdir bin/%{_arch64}
cat %{mysql_dir}/bin/mysql_config | sed "s#ldflags='-L/opt/SUNWspro/lib -lCrun -lrt'#ldflags=''#" > bin/mysql_config
cat %{mysql_dir}/bin/%{_arch64}/mysql_config | sed "s#ldflags='-L/opt/SUNWspro/lib -lCrun -lrt'#ldflags=''#" > bin/%{_arch64}/mysql_config

cat %{postgres_dir}/bin/pg_config | sed '{
    s#-lpgport##g
    s#-ledit##g
}' > bin/pg_config
cat %{postgres_dir}/bin/%{_arch64}/pg_config | sed '{
    s#-lpgport##g
    s#-ledit##g
}' > bin/%{_arch64}/pg_config

chmod 0755 bin/*
chmod 0755 bin/%{_arch64}/*

%ifarch amd64 sparcv9
cd %{src_dir}-64

INCL_PATHS="-I/usr/X11/include -I/usr/gnu/include -I%{postgres_dir}/include -I%{postgres_dir}/include/server -I%{mysql_dir}/include -I/usr/sfw/include -D_REENTRANT -DSOLARIS -D_POSIX_PTHREAD_SEMANTICS -D__EXTENSIONS__ -D_LARGEFILE_SOURCE"
export CFLAGS="-O3 -ftree-loop-linear -floop-interchange -floop-strip-mine -floop-block -ftree-loop-distribution -fno-gcse -fivopts -ftree-loop-im -m64 -fPIC -DPIC -Xlinker -i -march=opteron -fno-omit-frame-pointer -fno-strict-aliasing ${INCL_PATHS}"

LPATHS="-L/usr/X11/lib/%{_arch64} -R/usr/X11/lib/%{_arch64} -L/usr/gnu/lib/%{_arch64} -R/usr/gnu/lib/%{_arch64} -L%{postgres_dir}/lib/%{_arch64} -R%{postgres_dir}/lib/%{_arch64} -L%{mysql_dir}/lib/%{_arch64} -R%{mysql_dir}/lib/%{_arch64} -L/usr/sfw/lib/%{_arch64} -R/usr/sfw/lib/%{_arch64} -L%{_builddir}/%{src_dir}-64/lib"
export LDFLAGS="%_ldflags64 ${LPATHS}"

export CXXFLAGS=${CFLAGS}
export QMAKE_LFLAGS="-L/usr/gnu/lib/%{_arch64} -R/usr/gnu/lib/%{_arch64}"
export PATH="${PDIR}/bin/%{_arch64}:%{_prefix}/bin/%{_arch64}:${OPATH}"

echo yes | ./configure -prefix %{_prefix} \
           -platform solaris-g++-64 \
           -bindir %{_prefix}/qt4/bin/%{_arch64} \
           -docdir %{_docdir}/qt4 \
           -headerdir %{_includedir}/qt4 \
           -libdir %{_libdir}/%{_arch64} \
           -plugindir %{_libdir}/%{_arch64}/qt4/plugins \
           -datadir %{_datadir}/qt4 \
           -translationdir %{_datadir}/qt4/translations \
           -examplesdir %{_datadir}/qt4/examples \
           -demosdir %{_datadir}/qt4/demos \
           -sysconfdir %{_sysconfdir} \
           -release -shared \
           -no-fast \
           -largefile \
           -exceptions \
           -accessibility \
           -stl \
           -plugin-sql-mysql \
           -plugin-sql-odbc \
           -plugin-sql-sqlite \
           -plugin-sql-psql -system-sqlite -webkit \
           -assistant-webkit \
           -system-libpng \
           -system-libjpeg \
           -system-libmng \
           -system-zlib \
           -system-libtiff \
           -xcursor \
           -xrandr \
           -xrender \
           -sm -xshape \
           -xinerama \
           -xfixes \
           -fontconfig \
           -no-tablet \
           -xkb -opengl \
           -glib \
           -system-nas-sound \
           -xmlpatterns \
           -svg \
           -no-phonon \
           -qt-gif \
           -dbus-linked \
           -iconv \
           -cups \
           -openssl-linked \
           -no-optimized-qmake \
           -freetype \
           -no-pch \
           -nis \
           -no-tablet \
           -verbose \
           -make libs \
           -make tools \
           -make examples \
           -make demos \
           -make docs \
           ${INCL_PATHS} \
           ${LPATHS}

make -j$CPUS
cd ..
%endif

cd %{src_dir}

INCL_PATHS="-I/usr/X11/include -I/usr/gnu/include -I%{postgres_dir}/include -I%{postgres_dir}/include/server -I%{mysql_dir}/include -I/usr/sfw/include -D_REENTRANT -DSOLARIS -D_POSIX_PTHREAD_SEMANTICS -D__EXTENSIONS__ -D_LARGEFILE_SOURCE"
export CFLAGS="-O3 -ftree-loop-linear -floop-interchange -floop-strip-mine -floop-block -ftree-loop-distribution -fno-gcse -fivopts -ftree-loop-im -fPIC -DPIC -Xlinker -i -march=pentium4 -fno-omit-frame-pointer -fno-strict-aliasing ${INCL_PATHS}"

LPATHS="-L/usr/X11/lib -R/usr/X11/lib -L/usr/gnu/lib -R/usr/gnu/lib -L%{postgres_dir}/lib -R%{postgres_dir}/lib -L%{mysql_dir}/lib -R%{mysql_dir}/lib -L/usr/sfw/lib -R/usr/sfw/lib -L%{_builddir}/%{src_dir}/lib"
export LDFLAGS="%_ldflags ${LPATHS}"

export CXXFLAGS=${CFLAGS}
export QMAKE_LFLAGS="-L/usr/gnu/lib -R/usr/gnu/lib"
export PATH="${PDIR}/bin:${OPATH}"

echo yes | ./configure -prefix %{_prefix} \
           -platform solaris-g++ \
           -bindir %{_prefix}/qt4/bin \
           -docdir %{_docdir}/qt4 \
           -headerdir %{_includedir}/qt4 \
           -libdir %{_libdir} \
           -plugindir %{_libdir}/qt4/plugins \
           -datadir %{_datadir}/qt4 \
           -translationdir %{_datadir}/qt4/translations \
           -examplesdir %{_datadir}/qt4/examples \
           -demosdir %{_datadir}/qt4/demos \
           -sysconfdir %{_sysconfdir} \
           -release -shared \
           -no-fast \
           -largefile \
           -exceptions \
           -accessibility \
           -stl \
           -plugin-sql-mysql \
           -plugin-sql-odbc \
           -plugin-sql-sqlite \
           -plugin-sql-psql -system-sqlite -webkit \
           -assistant-webkit \
           -system-libpng \
           -system-libjpeg \
           -system-libmng \
           -system-zlib \
           -system-libtiff \
           -xcursor \
           -xrandr \
           -xrender \
           -sm -xshape \
           -xinerama \
           -xfixes \
           -fontconfig \
           -no-tablet \
           -xkb -opengl \
           -glib \
           -system-nas-sound \
           -xmlpatterns \
           -svg \
           -phonon \
           -phonon-backend \
           -qt-gif \
           -dbus-linked \
           -iconv \
           -cups \
           -openssl-linked \
           -no-optimized-qmake \
           -freetype \
           -no-pch \
           -nis \
           -no-tablet \
           -verbose \
           -make libs \
           -make tools \
           -make examples \
           -make demos \
           -make docs \
           ${INCL_PATHS} \
           ${LPATHS}

make -j$CPUS
cd ..

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64
cd %{src_dir}-64
make install INSTALL_ROOT=$RPM_BUILD_ROOT

# Developing Qt apps needs a few .a libs
#
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.la
rm -rf ${RPM_BUILD_ROOT}%{_datadir}

mkdir -p ${RPM_BUILD_ROOT}%{_includedir}/qt4/Qt/64
mv ${RPM_BUILD_ROOT}%{_includedir}/qt4/Qt/qconfig.h ${RPM_BUILD_ROOT}%{_includedir}/qt4/Qt/64
mkdir -p ${RPM_BUILD_ROOT}%{_includedir}/qt4/QtCore/64
mv ${RPM_BUILD_ROOT}%{_includedir}/qt4/QtCore/qconfig.h ${RPM_BUILD_ROOT}%{_includedir}/qt4/QtCore/64

#
# Fixup binaries that conflict with Qt3
#
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}/%{_arch64}
(cd ${RPM_BUILD_ROOT}%{_prefix}/qt4/bin/%{_arch64}
 for i in * ; do
   case "${i}" in
     assistant|designer|linguist|lrelease|lupdate|moc|qmake|qtconfig|qtdemo|uic)
       mv $i ../../../bin/%{_arch64}/${i}-qt4
       ln -s ../../../bin/%{_arch64}/${i}-qt4 .
       ln -s ../../../bin/%{_arch64}/${i}-qt4 $i
       ;;
     *)
       mv $i ../../../bin/%{_arch64}/
       ln -s ../../../bin/%{_arch64}/$i .
       ;;
   esac
 done)

cd ..
%endif

cd %{src_dir}
make install INSTALL_ROOT=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la

#
# Create a compatibility doc link
#
(cd ${RPM_BUILD_ROOT}%{_datadir}/qt4
  mkdir doc
  chmod 0755 doc
  cd doc
  ln -s ../../doc/qt3/html
)

#
# Fixup binaries that conflict with Qt3
#
(cd ${RPM_BUILD_ROOT}%{_prefix}/qt4/bin
 for i in * ; do
   case "${i}" in
     assistant|designer|linguist|lrelease|lupdate|moc|qmake|qtconfig|qtdemo|uic)
       mv $i ../../bin/${i}-qt4
       ln -s ../../bin/${i}-qt4 .
       ln -s ../../bin/${i}-qt4 $i
       ;;
     %{_arch64}) echo ""
       ;;
     *)
       mv $i ../../bin/
       ln -s ../../bin/$i .
       ;;
   esac
 done)

#
# Patch qglobal.h to pull in correct 32Bit or 64Bit qconfig depending on
# build flags.
#
(cd ${RPM_BUILD_ROOT}%{_includedir}/qt4/Qt
 %patch2 -p4
)
(cd ${RPM_BUILD_ROOT}%{_includedir}/qt4/QtCore
 %patch2 -p4
)

#
# Fix qmake.conf
#
LPATHS="-L/usr/X11/lib/%{_arch64} -R/usr/X11/lib/%{_arch64} -L/usr/gnu/lib/%{_arch64} -R/usr/gnu/lib/%{_arch64} -L%{postgres_dir}/lib/%{_arch64} -R%{postgres_dir}/lib/%{_arch64} -L%{mysql_dir}/lib/%{_arch64} -R%{mysql_dir}/lib/%{_arch64} -L/usr/sfw/lib/%{_arch64} -R/usr/sfw/lib/%{_arch64}"
QMAKE64="${RPM_BUILD_ROOT}%{_datadir}/qt4/mkspecs/solaris-g++-64/qmake.conf"
cp ${QMAKE64} ${QMAKE64}.orig
cat ${QMAKE64}.orig | sed "{
    s@^QMAKE_LIBDIR		=.*@QMAKE_LIBDIR          = @
    s@^QMAKE_LFLAGS		= -m64@QMAKE_LFLAGS		= -m64 ${LPATHS}@
    s@^QMAKE_LIBS		=@QMAKE_LIBS		= -lstdc++ -lintl -liconv@
    s@^QMAKE_LIBDIR_X11	=.*@QMAKE_LIBDIR_X11	= /usr/X11/lib/%{_arch64}@
    s@^QMAKE_INCDIR_X11	=.*@QMAKE_INCDIR_X11	= /usr/X11/include@
    s@^QMAKE_LIBDIR_OPENGL	=.*@QMAKE_LIBDIR_OPENGL	= /usr/X11/lib/GL/%{_arch64}@
    s@^QMAKE_INCDIR_OPENGL	=.*@QMAKE_INCDIR_OPENGL	= /usr/X11/include@
}" > ${QMAKE64}

LPATHS="-L/usr/X11/lib -R/usr/X11/lib -L/usr/gnu/lib -R/usr/gnu/lib -L%{postgres_dir}/lib -R%{postgres_dir}/lib -L%{mysql_dir}/lib -R%{mysql_dir}/lib -L/usr/sfw/lib -R/usr/sfw/lib"
QMAKE="${RPM_BUILD_ROOT}%{_datadir}/qt4/mkspecs/solaris-g++/qmake.conf"
cp ${QMAKE} ${QMAKE}.orig
cat ${QMAKE}.orig | sed "{
    s@^QMAKE_LIBDIR		=.*@QMAKE_LIBDIR          = @
    s@^QMAKE_LFLAGS		=@QMAKE_LFLAGS		= ${LPATHS}@
    s@^QMAKE_LIBS		=@QMAKE_LIBS		= -lstdc++ -lintl -liconv@
    s@^QMAKE_LIBDIR_X11	=.*@QMAKE_LIBDIR_X11	= /usr/X11/lib@
    s@^QMAKE_INCDIR_X11	=.*@QMAKE_INCDIR_X11	= /usr/X11/include@
    s@^QMAKE_LIBDIR_OPENGL	=.*@QMAKE_LIBDIR_OPENGL	= /usr/X11/lib/GL@
    s@^QMAKE_INCDIR_OPENGL	=.*@QMAKE_INCDIR_OPENGL	= /usr/X11/include@
}" > ${QMAKE}

rm -f ${QMAKE64}.orig
rm -f ${QMAKE}.orig

#
# Copy *.desktop entries
#
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/applications
cp %{SOURCE1} ${RPM_BUILD_ROOT}%{_datadir}/applications
cp %{SOURCE2} ${RPM_BUILD_ROOT}%{_datadir}/applications
cp %{SOURCE3} ${RPM_BUILD_ROOT}%{_datadir}/applications
cp %{SOURCE4} ${RPM_BUILD_ROOT}%{_datadir}/applications
cp %{SOURCE5} ${RPM_BUILD_ROOT}%{_datadir}/applications

cd ..


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/assistant-qt4
%{_bindir}/assistant_adp
%{_bindir}/qdbus
%{_bindir}/qdbusviewer

%dir %attr (0755, root, bin) %{_prefix}/qt4
%dir %attr (0755, root, bin) %{_prefix}/qt4/bin
%{_prefix}/qt4/bin/assistant
%{_prefix}/qt4/bin/assistant_adp
%{_prefix}/qt4/bin/assistant-qt4
%{_prefix}/qt4/bin/qdbus
%{_prefix}/qt4/bin/qdbusviewer

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%_arch64
%{_bindir}/%_arch64/assistant_adp
%{_bindir}/%_arch64/assistant-qt4
%{_bindir}/%_arch64/qdbus
%{_bindir}/%_arch64/qdbusviewer

%dir %attr (0755, root, bin) %{_prefix}/qt4/bin/%{_arch64}
%{_prefix}/qt4/bin/%{_arch64}/assistant
%{_prefix}/qt4/bin/%{_arch64}/assistant_adp
%{_prefix}/qt4/bin/%{_arch64}/assistant-qt4
%{_prefix}/qt4/bin/%_arch64/qdbus
%{_prefix}/qt4/bin/%_arch64/qdbusviewer
%endif

%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libQt3Support.prl
%{_libdir}/libQt3Support.so
%{_libdir}/libQt3Support.so.4
%{_libdir}/libQt3Support.so.4.4
%{_libdir}/libQt3Support.so.4.4.3
%{_libdir}/libQtAssistantClient.prl
%{_libdir}/libQtAssistantClient.so
%{_libdir}/libQtAssistantClient.so.4
%{_libdir}/libQtAssistantClient.so.4.4
%{_libdir}/libQtAssistantClient.so.4.4.3
%{_libdir}/libQtCLucene.prl
%{_libdir}/libQtCLucene.so
%{_libdir}/libQtCLucene.so.4
%{_libdir}/libQtCLucene.so.4.4
%{_libdir}/libQtCLucene.so.4.4.3
%{_libdir}/libQtCore.prl
%{_libdir}/libQtCore.so
%{_libdir}/libQtCore.so.4
%{_libdir}/libQtCore.so.4.4
%{_libdir}/libQtCore.so.4.4.3
%{_libdir}/libQtDBus.prl
%{_libdir}/libQtDBus.so
%{_libdir}/libQtDBus.so.4
%{_libdir}/libQtDBus.so.4.4
%{_libdir}/libQtDBus.so.4.4.3
%{_libdir}/libQtDesigner.prl
%{_libdir}/libQtDesigner.so
%{_libdir}/libQtDesigner.so.4
%{_libdir}/libQtDesigner.so.4.4
%{_libdir}/libQtDesigner.so.4.4.3
%{_libdir}/libQtDesignerComponents.prl
%{_libdir}/libQtDesignerComponents.so
%{_libdir}/libQtDesignerComponents.so.4
%{_libdir}/libQtDesignerComponents.so.4.4
%{_libdir}/libQtDesignerComponents.so.4.4.3
%{_libdir}/libQtGui.prl
%{_libdir}/libQtGui.so
%{_libdir}/libQtGui.so.4
%{_libdir}/libQtGui.so.4.4
%{_libdir}/libQtGui.so.4.4.3
%{_libdir}/libQtHelp.prl
%{_libdir}/libQtHelp.so
%{_libdir}/libQtHelp.so.4
%{_libdir}/libQtHelp.so.4.4
%{_libdir}/libQtHelp.so.4.4.3
%{_libdir}/libQtNetwork.prl
%{_libdir}/libQtNetwork.so
%{_libdir}/libQtNetwork.so.4
%{_libdir}/libQtNetwork.so.4.4
%{_libdir}/libQtNetwork.so.4.4.3
%{_libdir}/libQtOpenGL.prl
%{_libdir}/libQtOpenGL.so
%{_libdir}/libQtOpenGL.so.4
%{_libdir}/libQtOpenGL.so.4.4
%{_libdir}/libQtOpenGL.so.4.4.3
%{_libdir}/libQtPhonon.prl
%{_libdir}/libQtPhonon.so
%{_libdir}/libQtPhonon.so.4
%{_libdir}/libQtPhonon.so.4.1
%{_libdir}/libQtPhonon.so.4.1.3
%{_libdir}/libQtScript.prl
%{_libdir}/libQtScript.so
%{_libdir}/libQtScript.so.4
%{_libdir}/libQtScript.so.4.4
%{_libdir}/libQtScript.so.4.4.3
%{_libdir}/libQtSql.prl
%{_libdir}/libQtSql.so
%{_libdir}/libQtSql.so.4
%{_libdir}/libQtSql.so.4.4
%{_libdir}/libQtSql.so.4.4.3
%{_libdir}/libQtSvg.prl
%{_libdir}/libQtSvg.so
%{_libdir}/libQtSvg.so.4
%{_libdir}/libQtSvg.so.4.4
%{_libdir}/libQtSvg.so.4.4.3
%{_libdir}/libQtTest.prl
%{_libdir}/libQtTest.so
%{_libdir}/libQtTest.so.4
%{_libdir}/libQtTest.so.4.4
%{_libdir}/libQtTest.so.4.4.3
%{_libdir}/libQtUiTools.a
%{_libdir}/libQtUiTools.prl
%{_libdir}/libQtWebKit.prl
%{_libdir}/libQtWebKit.so
%{_libdir}/libQtWebKit.so.4
%{_libdir}/libQtWebKit.so.4.4
%{_libdir}/libQtWebKit.so.4.4.3
%{_libdir}/libQtXml.prl
%{_libdir}/libQtXml.so
%{_libdir}/libQtXml.so.4
%{_libdir}/libQtXml.so.4.4
%{_libdir}/libQtXml.so.4.4.3
%{_libdir}/libQtXmlPatterns.prl
%{_libdir}/libQtXmlPatterns.so
%{_libdir}/libQtXmlPatterns.so.4
%{_libdir}/libQtXmlPatterns.so.4.4
%{_libdir}/libQtXmlPatterns.so.4.4.3

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%_arch64
%{_libdir}/%_arch64/libQt3Support.prl
%{_libdir}/%_arch64/libQt3Support.so
%{_libdir}/%_arch64/libQt3Support.so.4
%{_libdir}/%_arch64/libQt3Support.so.4.4
%{_libdir}/%_arch64/libQt3Support.so.4.4.3
%{_libdir}/%_arch64/libQtAssistantClient.prl
%{_libdir}/%_arch64/libQtAssistantClient.so
%{_libdir}/%_arch64/libQtAssistantClient.so.4
%{_libdir}/%_arch64/libQtAssistantClient.so.4.4
%{_libdir}/%_arch64/libQtAssistantClient.so.4.4.3
%{_libdir}/%_arch64/libQtCLucene.prl
%{_libdir}/%_arch64/libQtCLucene.so
%{_libdir}/%_arch64/libQtCLucene.so.4
%{_libdir}/%_arch64/libQtCLucene.so.4.4
%{_libdir}/%_arch64/libQtCLucene.so.4.4.3
%{_libdir}/%_arch64/libQtCore.prl
%{_libdir}/%_arch64/libQtCore.so
%{_libdir}/%_arch64/libQtCore.so.4
%{_libdir}/%_arch64/libQtCore.so.4.4
%{_libdir}/%_arch64/libQtCore.so.4.4.3
%{_libdir}/%_arch64/libQtDBus.prl
%{_libdir}/%_arch64/libQtDBus.so
%{_libdir}/%_arch64/libQtDBus.so.4
%{_libdir}/%_arch64/libQtDBus.so.4.4
%{_libdir}/%_arch64/libQtDBus.so.4.4.3
%{_libdir}/%_arch64/libQtDesigner.prl
%{_libdir}/%_arch64/libQtDesigner.so
%{_libdir}/%_arch64/libQtDesigner.so.4
%{_libdir}/%_arch64/libQtDesigner.so.4.4
%{_libdir}/%_arch64/libQtDesigner.so.4.4.3
%{_libdir}/%_arch64/libQtDesignerComponents.prl
%{_libdir}/%_arch64/libQtDesignerComponents.so
%{_libdir}/%_arch64/libQtDesignerComponents.so.4
%{_libdir}/%_arch64/libQtDesignerComponents.so.4.4
%{_libdir}/%_arch64/libQtDesignerComponents.so.4.4.3
%{_libdir}/%_arch64/libQtGui.prl
%{_libdir}/%_arch64/libQtGui.so
%{_libdir}/%_arch64/libQtGui.so.4
%{_libdir}/%_arch64/libQtGui.so.4.4
%{_libdir}/%_arch64/libQtGui.so.4.4.3
%{_libdir}/%_arch64/libQtHelp.prl
%{_libdir}/%_arch64/libQtHelp.so
%{_libdir}/%_arch64/libQtHelp.so.4
%{_libdir}/%_arch64/libQtHelp.so.4.4
%{_libdir}/%_arch64/libQtHelp.so.4.4.3
%{_libdir}/%_arch64/libQtNetwork.prl
%{_libdir}/%_arch64/libQtNetwork.so
%{_libdir}/%_arch64/libQtNetwork.so.4
%{_libdir}/%_arch64/libQtNetwork.so.4.4
%{_libdir}/%_arch64/libQtNetwork.so.4.4.3
%{_libdir}/%_arch64/libQtOpenGL.prl
%{_libdir}/%_arch64/libQtOpenGL.so
%{_libdir}/%_arch64/libQtOpenGL.so.4
%{_libdir}/%_arch64/libQtOpenGL.so.4.4
%{_libdir}/%_arch64/libQtOpenGL.so.4.4.3
#%{_libdir}/%_arch64/libQtPhonon.prl
#%{_libdir}/%_arch64/libQtPhonon.so
#%{_libdir}/%_arch64/libQtPhonon.so.4
#%{_libdir}/%_arch64/libQtPhonon.so.4.1
#%{_libdir}/%_arch64/libQtPhonon.so.4.1.3
%{_libdir}/%_arch64/libQtScript.prl
%{_libdir}/%_arch64/libQtScript.so
%{_libdir}/%_arch64/libQtScript.so.4
%{_libdir}/%_arch64/libQtScript.so.4.4
%{_libdir}/%_arch64/libQtScript.so.4.4.3
%{_libdir}/%_arch64/libQtSql.prl
%{_libdir}/%_arch64/libQtSql.so
%{_libdir}/%_arch64/libQtSql.so.4
%{_libdir}/%_arch64/libQtSql.so.4.4
%{_libdir}/%_arch64/libQtSql.so.4.4.3
%{_libdir}/%_arch64/libQtSvg.prl
%{_libdir}/%_arch64/libQtSvg.so
%{_libdir}/%_arch64/libQtSvg.so.4
%{_libdir}/%_arch64/libQtSvg.so.4.4
%{_libdir}/%_arch64/libQtSvg.so.4.4.3
%{_libdir}/%_arch64/libQtTest.prl
%{_libdir}/%_arch64/libQtTest.so
%{_libdir}/%_arch64/libQtTest.so.4
%{_libdir}/%_arch64/libQtTest.so.4.4
%{_libdir}/%_arch64/libQtTest.so.4.4.3
%{_libdir}/%_arch64/libQtUiTools.a
%{_libdir}/%_arch64/libQtUiTools.prl
%{_libdir}/%_arch64/libQtWebKit.prl
%{_libdir}/%_arch64/libQtWebKit.so
%{_libdir}/%_arch64/libQtWebKit.so.4
%{_libdir}/%_arch64/libQtWebKit.so.4.4
%{_libdir}/%_arch64/libQtWebKit.so.4.4.3
%{_libdir}/%_arch64/libQtXml.prl
%{_libdir}/%_arch64/libQtXml.so
%{_libdir}/%_arch64/libQtXml.so.4
%{_libdir}/%_arch64/libQtXml.so.4.4
%{_libdir}/%_arch64/libQtXml.so.4.4.3
%{_libdir}/%_arch64/libQtXmlPatterns.prl
%{_libdir}/%_arch64/libQtXmlPatterns.so
%{_libdir}/%_arch64/libQtXmlPatterns.so.4
%{_libdir}/%_arch64/libQtXmlPatterns.so.4.4
%{_libdir}/%_arch64/libQtXmlPatterns.so.4.4.3
%endif

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/qt4
%dir %attr (0755, root, bin) %{_datadir}/qt4/translations
%{_datadir}/qt4/translations/assistant_adp_de.qm
%{_datadir}/qt4/translations/assistant_adp_ja.qm
%{_datadir}/qt4/translations/assistant_adp_pl.qm
%{_datadir}/qt4/translations/assistant_adp_zh_CN.qm
%{_datadir}/qt4/translations/assistant_adp_zh_TW.qm
%{_datadir}/qt4/translations/assistant_de.qm
%{_datadir}/qt4/translations/assistant_pl.qm
%{_datadir}/qt4/translations/assistant_zh_CN.qm
%{_datadir}/qt4/translations/assistant_zh_TW.qm
%{_datadir}/qt4/translations/designer_de.qm
%{_datadir}/qt4/translations/designer_ja.qm
%{_datadir}/qt4/translations/designer_pl.qm
%{_datadir}/qt4/translations/designer_zh_CN.qm
%{_datadir}/qt4/translations/designer_zh_TW.qm
%{_datadir}/qt4/translations/linguist_de.qm
%{_datadir}/qt4/translations/linguist_ja.qm
%{_datadir}/qt4/translations/linguist_pl.qm
%{_datadir}/qt4/translations/linguist_zh_CN.qm
%{_datadir}/qt4/translations/linguist_zh_TW.qm
%{_datadir}/qt4/translations/qt_ar.qm
%{_datadir}/qt4/translations/qt_de.qm
%{_datadir}/qt4/translations/qt_es.qm
%{_datadir}/qt4/translations/qt_fr.qm
%{_datadir}/qt4/translations/qt_help_de.qm
%{_datadir}/qt4/translations/qt_help_pl.qm
%{_datadir}/qt4/translations/qt_help_zh_CN.qm
%{_datadir}/qt4/translations/qt_help_zh_TW.qm
%{_datadir}/qt4/translations/qt_iw.qm
%{_datadir}/qt4/translations/qt_ja_jp.qm
%{_datadir}/qt4/translations/qt_pl.qm
%{_datadir}/qt4/translations/qt_pt.qm
%{_datadir}/qt4/translations/qt_ru.qm
%{_datadir}/qt4/translations/qt_sk.qm
%{_datadir}/qt4/translations/qt_sv.qm
%{_datadir}/qt4/translations/qt_uk.qm
%{_datadir}/qt4/translations/qt_zh_CN.qm
%{_datadir}/qt4/translations/qt_zh_TW.qm
%{_datadir}/qt4/translations/qtconfig_pl.qm
%{_datadir}/qt4/translations/qtconfig_zh_CN.qm
%{_datadir}/qt4/translations/qtconfig_zh_TW.qm
%{_datadir}/qt4/translations/qvfb_pl.qm
%{_datadir}/qt4/translations/qvfb_zh_CN.qm
%{_datadir}/qt4/translations/qvfb_zh_TW.qm

%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/assistant.desktop

%dir %attr (0755, root, bin) %{_datadir}/qt4/phrasebooks
%{_datadir}/qt4/phrasebooks/swedish.qph
%{_datadir}/qt4/phrasebooks/polish.qph
%{_datadir}/qt4/phrasebooks/danish.qph
%{_datadir}/qt4/phrasebooks/italian.qph
%{_datadir}/qt4/phrasebooks/japanese.qph
%{_datadir}/qt4/phrasebooks/french.qph
%{_datadir}/qt4/phrasebooks/russian.qph
%{_datadir}/qt4/phrasebooks/finnish.qph
%{_datadir}/qt4/phrasebooks/dutch.qph
%{_datadir}/qt4/phrasebooks/german.qph
%{_datadir}/qt4/phrasebooks/spanish.qph
%{_datadir}/qt4/phrasebooks/norwegian.qph

%dir %attr (0755, root, bin) %{_libdir}/qt4
%dir %attr (0755, root, bin) %{_libdir}/qt4/plugins
%{_libdir}/qt4/plugins/accessible/libqtaccessiblecompatwidgets.so
%{_libdir}/qt4/plugins/accessible/libqtaccessiblewidgets.so
%{_libdir}/qt4/plugins/codecs/libqcncodecs.so
%{_libdir}/qt4/plugins/codecs/libqjpcodecs.so
%{_libdir}/qt4/plugins/codecs/libqkrcodecs.so
%{_libdir}/qt4/plugins/codecs/libqtwcodecs.so
%{_libdir}/qt4/plugins/designer/libarthurplugin.so
%{_libdir}/qt4/plugins/designer/libcontainerextension.so
%{_libdir}/qt4/plugins/designer/libcustomwidgetplugin.so
%{_libdir}/qt4/plugins/designer/libqt3supportwidgets.so
%{_libdir}/qt4/plugins/designer/libqwebview.so
%{_libdir}/qt4/plugins/designer/libtaskmenuextension.so
%{_libdir}/qt4/plugins/designer/libworldtimeclockplugin.so
%{_libdir}/qt4/plugins/iconengines/libqsvgicon.so
%{_libdir}/qt4/plugins/imageformats/libqgif.so
%{_libdir}/qt4/plugins/imageformats/libqico.so
%{_libdir}/qt4/plugins/imageformats/libqjpeg.so
%{_libdir}/qt4/plugins/imageformats/libqmng.so
%{_libdir}/qt4/plugins/imageformats/libqsvg.so
%{_libdir}/qt4/plugins/imageformats/libqtiff.so
%{_libdir}/qt4/plugins/inputmethods/libqimsw-multi.so
%{_libdir}/qt4/plugins/phonon_backend/libphonon_gstreamer.so
%{_libdir}/qt4/plugins/script/libqtscriptdbus.so
%{_libdir}/qt4/plugins/sqldrivers/libqsqlite.so
%{_libdir}/qt4/plugins/sqldrivers/libqsqlmysql.so
%{_libdir}/qt4/plugins/sqldrivers/libqsqlodbc.so
%{_libdir}/qt4/plugins/sqldrivers/libqsqlpsql.so
#
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%_arch64/qt4
%dir %attr (0755, root, bin) %{_libdir}/%_arch64/qt4/plugins
%{_libdir}/%_arch64/qt4/plugins/accessible/libqtaccessiblecompatwidgets.so
%{_libdir}/%_arch64/qt4/plugins/accessible/libqtaccessiblewidgets.so
%{_libdir}/%_arch64/qt4/plugins/codecs/libqcncodecs.so
%{_libdir}/%_arch64/qt4/plugins/codecs/libqjpcodecs.so
%{_libdir}/%_arch64/qt4/plugins/codecs/libqkrcodecs.so
%{_libdir}/%_arch64/qt4/plugins/codecs/libqtwcodecs.so
%{_libdir}/%_arch64/qt4/plugins/designer/libarthurplugin.so
%{_libdir}/%_arch64/qt4/plugins/designer/libcontainerextension.so
%{_libdir}/%_arch64/qt4/plugins/designer/libcustomwidgetplugin.so
%{_libdir}/%_arch64/qt4/plugins/designer/libqt3supportwidgets.so
%{_libdir}/%_arch64/qt4/plugins/designer/libqwebview.so
%{_libdir}/%_arch64/qt4/plugins/designer/libtaskmenuextension.so
%{_libdir}/%_arch64/qt4/plugins/designer/libworldtimeclockplugin.so
%{_libdir}/%_arch64/qt4/plugins/iconengines/libqsvgicon.so
%{_libdir}/%_arch64/qt4/plugins/imageformats/libqgif.so
%{_libdir}/%_arch64/qt4/plugins/imageformats/libqico.so
%{_libdir}/%_arch64/qt4/plugins/imageformats/libqjpeg.so
%{_libdir}/%_arch64/qt4/plugins/imageformats/libqmng.so
%{_libdir}/%_arch64/qt4/plugins/imageformats/libqsvg.so
%{_libdir}/%_arch64/qt4/plugins/imageformats/libqtiff.so
%{_libdir}/%_arch64/qt4/plugins/inputmethods/libqimsw-multi.so
#%{_libdir}/%_arch64/qt4/plugins/phonon_backend/libphonon_gstreamer.so
%{_libdir}/%_arch64/qt4/plugins/script/libqtscriptdbus.so
%{_libdir}/%_arch64/qt4/plugins/sqldrivers/libqsqlite.so
%{_libdir}/%_arch64/qt4/plugins/sqldrivers/libqsqlmysql.so
%{_libdir}/%_arch64/qt4/plugins/sqldrivers/libqsqlodbc.so
%{_libdir}/%_arch64/qt4/plugins/sqldrivers/libqsqlpsql.so
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/designer-qt4
%{_bindir}/linguist-qt4
%{_bindir}/lrelease-qt4
%{_bindir}/lupdate-qt4
%{_bindir}/moc-qt4
%{_bindir}/pixeltool
%{_bindir}/qcollectiongenerator
%{_bindir}/qdbuscpp2xml
%{_bindir}/qdbusxml2cpp
%{_bindir}/qhelpconverter
%{_bindir}/qhelpgenerator
%{_bindir}/qmake-qt4
%{_bindir}/qt3to4
%{_bindir}/qtconfig-qt4
%{_bindir}/qtdemo-qt4
%{_bindir}/rcc
%{_bindir}/uic-qt4
%{_bindir}/uic3
%{_bindir}/xmlpatterns

%dir %attr (0755, root, bin) %{_prefix}/qt4
%dir %attr (0755, root, bin) %{_prefix}/qt4/bin
%{_prefix}/qt4/bin/designer
%{_prefix}/qt4/bin/qcollectiongenerator
%{_prefix}/qt4/bin/qdbuscpp2xml
%{_prefix}/qt4/bin/qdbusxml2cpp
%{_prefix}/qt4/bin/qhelpconverter
%{_prefix}/qt4/bin/qhelpgenerator
%{_prefix}/qt4/bin/linguist
%{_prefix}/qt4/bin/lrelease
%{_prefix}/qt4/bin/lupdate
%{_prefix}/qt4/bin/moc
%{_prefix}/qt4/bin/qmake
%{_prefix}/qt4/bin/qtconfig
%{_prefix}/qt4/bin/qtdemo
%{_prefix}/qt4/bin/uic
%{_prefix}/qt4/bin/designer-qt4
%{_prefix}/qt4/bin/linguist-qt4
%{_prefix}/qt4/bin/lrelease-qt4
%{_prefix}/qt4/bin/lupdate-qt4
%{_prefix}/qt4/bin/moc-qt4
%{_prefix}/qt4/bin/qmake-qt4
%{_prefix}/qt4/bin/qtconfig-qt4
%{_prefix}/qt4/bin/qtdemo-qt4
%{_prefix}/qt4/bin/uic-qt4
%{_prefix}/qt4/bin/rcc
%{_prefix}/qt4/bin/uic3
%{_prefix}/qt4/bin/qt3to4
%{_prefix}/qt4/bin/pixeltool
%{_prefix}/qt4/bin/xmlpatterns

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%_arch64
%{_bindir}/%_arch64/designer-qt4
%{_bindir}/%_arch64/linguist-qt4
%{_bindir}/%_arch64/lrelease-qt4
%{_bindir}/%_arch64/lupdate-qt4
%{_bindir}/%_arch64/moc-qt4
%{_bindir}/%_arch64/pixeltool
%{_bindir}/%_arch64/qcollectiongenerator
%{_bindir}/%_arch64/qdbuscpp2xml
%{_bindir}/%_arch64/qdbusxml2cpp
%{_bindir}/%_arch64/qhelpconverter
%{_bindir}/%_arch64/qhelpgenerator
%{_bindir}/%_arch64/qmake-qt4
%{_bindir}/%_arch64/qt3to4
%{_bindir}/%_arch64/qtconfig-qt4
%{_bindir}/%_arch64/qtdemo-qt4
%{_bindir}/%_arch64/rcc
%{_bindir}/%_arch64/uic-qt4
%{_bindir}/%_arch64/uic3
%{_bindir}/%_arch64/xmlpatterns

%dir %attr (0755, root, bin) %{_prefix}/qt4/bin/%{_arch64}
%{_prefix}/qt4/bin/%{_arch64}/designer
%{_prefix}/qt4/bin/%{_arch64}/linguist
%{_prefix}/qt4/bin/%{_arch64}/lrelease
%{_prefix}/qt4/bin/%{_arch64}/lupdate
%{_prefix}/qt4/bin/%{_arch64}/moc
%{_prefix}/qt4/bin/%{_arch64}/qmake
%{_prefix}/qt4/bin/%{_arch64}/qtconfig
%{_prefix}/qt4/bin/%{_arch64}/qtdemo
%{_prefix}/qt4/bin/%{_arch64}/uic
%{_prefix}/qt4/bin/%{_arch64}/designer-qt4
%{_prefix}/qt4/bin/%{_arch64}/linguist-qt4
%{_prefix}/qt4/bin/%{_arch64}/lrelease-qt4
%{_prefix}/qt4/bin/%{_arch64}/lupdate-qt4
%{_prefix}/qt4/bin/%{_arch64}/moc-qt4
%{_prefix}/qt4/bin/%{_arch64}/qmake-qt4
%{_prefix}/qt4/bin/%{_arch64}/qtconfig-qt4
%{_prefix}/qt4/bin/%{_arch64}/qtdemo-qt4
%{_prefix}/qt4/bin/%{_arch64}/uic-qt4
%{_prefix}/qt4/bin/%{_arch64}/uic3
%{_prefix}/qt4/bin/%{_arch64}/qdbuscpp2xml
%{_prefix}/qt4/bin/%{_arch64}/qhelpgenerator
%{_prefix}/qt4/bin/%{_arch64}/qt3to4
%{_prefix}/qt4/bin/%{_arch64}/qhelpconverter
%{_prefix}/qt4/bin/%{_arch64}/pixeltool
%{_prefix}/qt4/bin/%{_arch64}/xmlpatterns
%{_prefix}/qt4/bin/%{_arch64}/rcc
%{_prefix}/qt4/bin/%{_arch64}/qdbusxml2cpp
%{_prefix}/qt4/bin/%{_arch64}/qcollectiongenerator
%endif

%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, bin) %{_includedir}/qt4
%dir %attr (0755, root, bin) %{_includedir}/qt4/Qt
%{_includedir}/qt4/Qt/*
%{_includedir}/qt4/Qt3Support/*
%{_includedir}/qt4/QtAssistant/*
%{_includedir}/qt4/QtCore/*
%{_includedir}/qt4/QtDBus/*
%{_includedir}/qt4/QtDesigner/*
%{_includedir}/qt4/QtGui/*
%{_includedir}/qt4/QtNetwork/*
%{_includedir}/qt4/QtOpenGL/*
%{_includedir}/qt4/QtScript/*
%{_includedir}/qt4/QtSql/*
%{_includedir}/qt4/QtSvg/*
%{_includedir}/qt4/QtTest/*
%{_includedir}/qt4/QtUiTools/*
%{_includedir}/qt4/QtXml/*
%{_includedir}/qt4/QtXmlPatterns/*
%{_includedir}/qt4/QtHelp/*
%{_includedir}/qt4/QtWebKit/*

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/qt4
%dir %attr (0755, root, bin) %{_datadir}/qt4/demos
%{_datadir}/qt4/demos/*

%dir %attr (0755, root, bin) %{_datadir}/qt4/examples
%{_datadir}/qt4/examples/*

%dir %attr (0755, root, bin) %{_datadir}/qt4/mkspecs
%{_datadir}/qt4/mkspecs/*

%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/designer.desktop
%{_datadir}/applications/linguist.desktop
%{_datadir}/applications/qtdemo.desktop
%{_datadir}/applications/qtconfig.desktop

%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/Qt3Support.pc
%{_libdir}/pkgconfig/QtAssistantClient.pc
%{_libdir}/pkgconfig/QtCLucene.pc
%{_libdir}/pkgconfig/QtCore.pc
%{_libdir}/pkgconfig/QtDBus.pc
%{_libdir}/pkgconfig/QtDesigner.pc
%{_libdir}/pkgconfig/QtDesignerComponents.pc
%{_libdir}/pkgconfig/QtGui.pc
%{_libdir}/pkgconfig/QtHelp.pc
%{_libdir}/pkgconfig/QtNetwork.pc
%{_libdir}/pkgconfig/QtOpenGL.pc
%{_libdir}/pkgconfig/QtPhonon.pc
%{_libdir}/pkgconfig/QtScript.pc
%{_libdir}/pkgconfig/QtSql.pc
%{_libdir}/pkgconfig/QtSvg.pc
%{_libdir}/pkgconfig/QtTest.pc
%{_libdir}/pkgconfig/QtUiTools.pc
%{_libdir}/pkgconfig/QtWebKit.pc
%{_libdir}/pkgconfig/QtXml.pc
%{_libdir}/pkgconfig/QtXmlPatterns.pc

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%_arch64
%dir %attr (0755, root, other) %{_libdir}/%_arch64/pkgconfig
%{_libdir}/%_arch64/pkgconfig/Qt3Support.pc
%{_libdir}/%_arch64/pkgconfig/QtAssistantClient.pc
%{_libdir}/%_arch64/pkgconfig/QtCLucene.pc
%{_libdir}/%_arch64/pkgconfig/QtCore.pc
%{_libdir}/%_arch64/pkgconfig/QtDBus.pc
%{_libdir}/%_arch64/pkgconfig/QtDesigner.pc
%{_libdir}/%_arch64/pkgconfig/QtDesignerComponents.pc
%{_libdir}/%_arch64/pkgconfig/QtGui.pc
%{_libdir}/%_arch64/pkgconfig/QtHelp.pc
%{_libdir}/%_arch64/pkgconfig/QtNetwork.pc
%{_libdir}/%_arch64/pkgconfig/QtOpenGL.pc
#%{_libdir}/%_arch64/pkgconfig/QtPhonon.pc
%{_libdir}/%_arch64/pkgconfig/QtScript.pc
%{_libdir}/%_arch64/pkgconfig/QtSql.pc
%{_libdir}/%_arch64/pkgconfig/QtSvg.pc
%{_libdir}/%_arch64/pkgconfig/QtTest.pc
%{_libdir}/%_arch64/pkgconfig/QtUiTools.pc
%{_libdir}/%_arch64/pkgconfig/QtWebKit.pc
%{_libdir}/%_arch64/pkgconfig/QtXml.pc
%{_libdir}/%_arch64/pkgconfig/QtXmlPatterns.pc
%endif

%files doc
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, bin) %{_datadir}/doc/qt4
%{_datadir}/doc/qt4/*
%dir %attr (0755, root, bin) %{_datadir}/qt4
%{_datadir}/qt4/q3porting.xml
%{_datadir}/qt4/doc

%files debug
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}/qt4
%dir %attr (0755, root, bin) %{_prefix}/qt4/bin
%{_prefix}/qt4/bin/*.debug

%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.debug
%dir %attr (0755, root, bin) %{_libdir}/qt4
%dir %attr (0755, root, bin) %{_libdir}/qt4/plugins
%{_libdir}/qt4/plugins/designer/libqt3supportwidgets.so.debug
%{_libdir}/qt4/plugins/designer/libcontainerextension.so.debug
%{_libdir}/qt4/plugins/designer/libcustomwidgetplugin.so.debug
%{_libdir}/qt4/plugins/designer/libtaskmenuextension.so.debug
%{_libdir}/qt4/plugins/designer/libarthurplugin.so.debug
%{_libdir}/qt4/plugins/designer/libworldtimeclockplugin.so.debug
%{_libdir}/qt4/plugins/designer/libqwebview.so.debug
%{_libdir}/qt4/plugins/accessible/libqtaccessiblewidgets.so.debug
%{_libdir}/qt4/plugins/accessible/libqtaccessiblecompatwidgets.so.debug
%{_libdir}/qt4/plugins/codecs/libqcncodecs.so.debug
%{_libdir}/qt4/plugins/codecs/libqtwcodecs.so.debug
%{_libdir}/qt4/plugins/codecs/libqkrcodecs.so.debug
%{_libdir}/qt4/plugins/codecs/libqjpcodecs.so.debug
%{_libdir}/qt4/plugins/imageformats/libqsvg.so.debug
%{_libdir}/qt4/plugins/imageformats/libqtiff.so.debug
%{_libdir}/qt4/plugins/imageformats/libqmng.so.debug
%{_libdir}/qt4/plugins/imageformats/libqico.so.debug
%{_libdir}/qt4/plugins/imageformats/libqgif.so.debug
%{_libdir}/qt4/plugins/imageformats/libqjpeg.so.debug
%{_libdir}/qt4/plugins/iconengines/libqsvgicon.so.debug
%{_libdir}/qt4/plugins/inputmethods/libqimsw-multi.so.debug
%{_libdir}/qt4/plugins/script/libqtscriptdbus.so.debug
%{_libdir}/qt4/plugins/phonon_backend/libphonon_gstreamer.so.debug
%{_libdir}/qt4/plugins/sqldrivers/libqsqlite.so.debug
%{_libdir}/qt4/plugins/sqldrivers/libqsqlpsql.so.debug
%{_libdir}/qt4/plugins/sqldrivers/libqsqlodbc.so.debug
%{_libdir}/qt4/plugins/sqldrivers/libqsqlmysql.so.debug

%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*.debug

%changelog
* Sat Aug 29 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Update MySQL dependency to 5.1.x package.
- Remove duplicate options.
* Sun Jul 05 2009 - Moinak Ghosh <moinakg@belenix(dot)org>
- Pull in additional patches and enable phonon build for 32Bit target.
* Tue Jun 23 2009 - Moinak Ghosh <moinakg@belenix(dot)org>
- Pull in more needed patches from KDE-Solaris repo.
* Sun Apr 17 2009 - moinakg@belenix.org
- Fix packaging to avoid conflict with Qt3.
- Build with newer arch and avoid aliasing issues.
- Add in *.desktop files from FC10.
- Disable Qt4 internal Phonon in favor of KDE4's Phonon.
* Sat May 16 2009 - moinakg@belenix.org
- Add debug package.
- Update devel package dependencies.
- Fix mkspecs and add patch for dual-arch qconfig.h.
* Sun May 03 2009 - moinakg@belenix.org
- Imported from KDE Solaris CvsDude and heavily modified.
* Fri Oct 24 2008 - oboril.lukas@gmail.com
- add dependencies for Solaris 10
- remove 64bit includes, not need right now.
- note about flags

* Wed Oct  8 2008 - groot@kde.org
- Turned back into a SPEC file
- Updated for Qt 4.4.1 installing into a different prefix


* Thu Dec 13 2007 - groot@kde.org
- Initial version
