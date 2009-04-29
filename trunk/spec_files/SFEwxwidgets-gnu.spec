#
# spec file for package SFEwxwidgets-spp
#
# includes module(s): wxWidgets
#

%include Solaris.inc
%include usr-gnu.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

%define using_gld %(gcc -v 2>&1 | /usr/xpg4/bin/grep -q with-gnu-ld && echo 1 || echo 0)
%define SUNWlibsdl      %(/usr/bin/pkginfo -q SUNWlibsdl && echo 1 || echo 0)

Name:                    SFEwxwidgets-gnu
Summary:                 wxWidgets - Cross-Platform GUI Library (g++)
URL:                     http://wxwidgets.org/
Version:                 2.8.10
%define tarball_version  2.8.10
Source:			 %{sf_download}/wxwindows/wxWidgets-%{tarball_version}.tar.bz2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SUNWgnome-libs
Requires:      SUNWgnome-vfs
%if %SUNWlibsdl
Requires:      SUNWlibsdl
%else
Requires:      SFEsdl
%endif
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-vfs-devel
%ifarch i386 amd64
BuildRequires: SUNWxorg-mesa
%endif
%if %SUNWlibsdl
BuildRequires: SUNWlibsdl-devel
%else
BuildRequires: SFEsdl-devel
%endif

%package devel
Summary:		 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:      %name

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -c -n %name-%version

%ifarch amd64 sparcv9
cp -rp wxWidgets-%{tarball_version} wxWidgets-%{tarball_version}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

%ifarch amd64 sparcv9
cd wxWidgets-%{tarball_version}-64

export CPPFLAGS="-I/usr/X11/include"
export CC=gcc
export CFLAGS="%{gcc_optflags64}"
export CXX=g++
export CXXFLAGS="%{gcc_cxx_optflags64}"
%if %using_gld
  export LDFLAGS="-L%{_libdir}/%{_arch64} -L/usr/X11/lib/%{_arch64} -R%{_libdir}/%{_arch64} -R/usr/X11/lib/%{_arch64} -lm"
  CFLAGS="$( echo $CFLAGS | sed 's/ -Xlinker -i//' )"
  CXXFLAGS="$( echo $CXXFLAGS | sed 's/ -Xlinker -i//' )"
%else
  export LDFLAGS="%{_ldflags64} -lm"
  export LD_OPTIONS="-i -L%{_libdir}/%{_arch64} -L/usr/X11/lib/%{_arch64} -R%{_libdir}/%{_arch64}:/usr/X11/lib/%{_arch64}"
%endif

export SDL_CONFIG=/usr/bin/%{_arch64}/sdl-config
export PKG_CONFIG_PATH=%{_prefix}/lib/%{_arch64}/pkgconfig:/usr/lib/%{_arch64}/pkgconfig:/usr/lib/pkgconfig

# keep PATH from being mangled by SDL check (breaks grep -E and tr A-Z a-z)
perl -pi -e 's,PATH=".*\$PATH",:,' configure
./configure --prefix=%{_prefix}                 \
            --bindir=%{_bindir}/%{_arch64}      \
            --includedir=%{_includedir}         \
            --libdir=%{_libdir}/%{_arch64}      \
            --enable-gtk2                       \
            --enable-unicode                    \
            --enable-mimetype                   \
            --enable-gui                        \
            --enable-xrc                        \
            --with-gtk                          \
            --with-subdirs                      \
            --without-expat                     \
            --with-sdl                          \
            --with-gnomeprint                   \
            --with-gnomevfs                     \
            --with-opengl                       \
            --without-libmspack

cat bk-make-pch | sed 's/MMD/MM/' > bk-make-pch.new
cp bk-make-pch.new bk-make-pch

make -j$CPUS
cd contrib
make -j$CPUS
cd ..
cd locale
make allmo
cd ..
cd ..
%endif

cd wxWidgets-%{tarball_version}
export CPPFLAGS="-I/usr/X11/include"
export CC=gcc
export CFLAGS="%{gcc_optflags}"
export CXX=g++
export CXXFLAGS="%{gcc_cxx_optflags}"
%if %using_gld
  export LDFLAGS="-L%{_libdir} -L/usr/X11/lib -R%{_libdir} -R/usr/X11/lib -lm"
  CFLAGS="$( echo $CFLAGS | sed 's/ -Xlinker -i//' )"
  CXXFLAGS="$( echo $CXXFLAGS | sed 's/ -Xlinker -i//' )"
%else
  export LDFLAGS="%{_ldflags} -lm"
  export LD_OPTIONS="-i -L%{_libdir} -L/usr/X11/lib -R%{_libdir}:/usr/X11/lib"
%endif

# keep PATH from being mangled by SDL check (breaks grep -E and tr A-Z a-z)
perl -pi -e 's,PATH=".*\$PATH",:,' configure
./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}/%{base_isa}	\
	    --includedir=%{_includedir}		\
            --libdir=%{_libdir}			\
            --enable-gtk2			\
            --enable-unicode			\
            --enable-mimetype			\
            --enable-gui			\
            --enable-xrc			\
            --with-gtk				\
            --with-subdirs			\
            --without-expat                     \
            --with-sdl                          \
            --with-gnomeprint			\
            --with-gnomevfs			\
            --with-opengl			\
            --without-libmspack

cat bk-make-pch | sed 's/MMD/MM/' > bk-make-pch.new
cp bk-make-pch.new bk-make-pch

make -j$CPUS
cd contrib
make -j$CPUS
cd ..
cd locale
make allmo
cd ..
cd ..

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
cd wxWidgets-%{tarball_version}-64
make install DESTDIR=$RPM_BUILD_ROOT
cd contrib
make install DESTDIR=$RPM_BUILD_ROOT
cd ..
cd ..

CWD=`pwd`
cd $RPM_BUILD_ROOT%{_bindir}/%{_arch64}
rm -f wx-config
ln -s ../../lib/%{_arch64}/wx/config/gtk2-unicode-release-* wx-config
perl -pi -e 's,-pthreads,,' wx-config
cd ${CWD}

%endif

cd wxWidgets-%{tarball_version}
make install DESTDIR=$RPM_BUILD_ROOT
cd contrib
make install DESTDIR=$RPM_BUILD_ROOT
cd ..
cd ..

cd $RPM_BUILD_ROOT%{_bindir}/%{base_isa}
rm -f wx-config
ln -s ../../lib/wx/config/gtk2-unicode-release-* wx-config
perl -pi -e 's,-pthreads,,' wx-config

cd $RPM_BUILD_ROOT%{_bindir}
ln -sf %{base_isa}/wx-config wx-config


%if %build_l10n
# Rename zh dir to zh_CN as zh is a symlink to zh_CN and causing installation
# problems as a dir.
cd $RPM_BUILD_ROOT%{_datadir}/locale
mv zh zh_CN
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/wx-config
%dir %attr (0755, root, bin) %{_bindir}/%{base_isa}
%{_bindir}/%{base_isa}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%{_libdir}/wx

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/*
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/*.so*
%{_libdir}/%{_arch64}/wx
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, sys) %{_datadir}/bakefile
%dir %attr(0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%{_datadir}/bakefile/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Tue Apr 28 2009 - moinakg@belenix.org
- Bump version to 2.8.10 and add 64Bit build.
* Thu Feb 21, 2008 - trisk@acm.jhu.edu
- Bump to 2.8.7
- Add SFEsdl dependency, add --with-gnomevfs, fix building subdirs
* Sat Sep 22 2007 - dougs@truemail.co.th
- Modified for GNU ld with gcc
* Tue Sep 18 2007 - brian.cameron@sun.com
- Bump to 2.8.5.  Remove upstream patch wxwidgets-02-sqrt.diff.
* Wed Aug 15 2007 - dougs@truemail.co.th
- removed -pthreads from wx-config to stop it infecting other builds
* Sat Aug 11 2007 - trisk@acm.jhu.edu
- Bump to 2.8.4 for compatibility with SFEwxwidgets
- Use CC=gcc to be consistent and not confuse build system
* Sat Jul 14 2007 - dougs@truemail.co.th
- Converted from SFEwxwidgets.spec
