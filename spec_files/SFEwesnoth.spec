#
# spec file for package SFEwesnoth.spec
#
%include Solaris.inc

# For binary packages on wesnoth.org
#%define _basedir /opt/games

%define wesnoth_datadir %{_datadir}/wesnoth

# Relative path on prefix 
%define python_vers 2.6

%define src_version 1.6.4

Name:                    	SFEwesnoth
Summary:                 	Battle for Wesnoth is a fantasy turn-based strategy game
Version:                 	1.6.4
License:			GPLv2
URL:				http://www.wesnoth.org
SUNW_Copyright:			wesnoth.copyright
Source:                  	%{sf_download}/wesnoth/wesnoth-%{src_version}.tar.bz2
Patch2:			        wesnoth-02-fixusleep.diff
Patch3:			        wesnoth-03-fixtolower.diff
Patch4:			        wesnoth-04-fixatoi.diff
Patch5:			        wesnoth-05-fixround.diff
Patch6: 		        wesnoth-06-fixreturn.diff
Patch7:			        wesnoth-07-fixserver.diff
Patch9:			        wesnoth-09-fixrand.diff
Patch10:		        wesnoth-10-fixstd.diff
Source1:                        FindBoost.cmake

BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEsdl-devel
Requires: SFEsdl
BuildRequires:		SFEsdl-mixer-devel
BuildRequires:		SFEsdl-ttf-devel
BuildRequires:		SFEsdl-net-devel
BuildRequires:		SFEsdl-image-devel
BuildRequires:		SFEcmake
BuildRequires:          SUNWgnome-common-devel
BuildRequires:          SUNWgnu-gettext
#BuildRequires:	        SFElibfribidi-devel
BuildRequires:	        SUNWpng-devel
BuildRequires:          SFEboost-gpp-devel
BuildRequires:	        SUNWpango-devel
Requires:	        SFEsdl-mixer
Requires:	        SFEsdl-ttf
Requires:	        SFEsdl-net
Requires:	        SFEsdl-image
Requires:   	        SFEboost-gpp
Requires:	        SUNWPython26
#Requires:	        SFElibfribidi
Requires:	        SUNWpng
Requires:	        SUNWpango
Requires:	        SUNWfontconfig
Requires:	        SUNWzlib
SUNW_BaseDir:     /

%package server
Summary:		Deamon to run Wesnoth game server
SUNW_BaseDir:     /
Requires:		%{name}

%prep
%setup -q -n wesnoth-%{src_version}
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch9 -p1
%patch10 -p1
cp %{SOURCE1} cmake

#
# Needed till we fix BOOST headers
#
for mk in `find . -name Makefile.in`
do
	[ ! -f ${mk}.orig ] && cp ${mk} ${mk}.orig
	cat ${mk}.orig | sed 's/\-Werror//g' > ${mk}
done

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export MSGFMT=/usr/gnu/bin/msgfmt
export SHELL="/bin/bash"
export CONFIG_SHELL="/bin/bash"
export MAKESHELL="/bin/bash"
export GCC="yes"
export CC=%{_prefix}/gnu/bin/gcc
export CXX=%{_prefix}/gnu/bin/g++
#export CMAKE_INCLUDE_PATH="%{gnu_inc}:%{xorg_inc}"
OPATH=${PATH}

#mkdir -p wesnothbld
#cd wesnothbld

#
# SFE paths are needed for libusb
#
export CPPFLAGS="-I%{_includedir}/boost/gcc4"
export BOOST_CPPFLAGS="$CPPFLAGS"
export CFLAGS="-march=pentium3 -fno-omit-frame-pointer -fPIC -DPIC -I%{gnu_inc}"
export CXXFLAGS="-march=pentium3 -fno-omit-frame-pointer -fPIC -DPIC -I%{gnu_inc}"
export LDFLAGS="%_ldflags -lsocket -lnsl -L/lib -R/lib %{gnu_lib_path} -lstdc++ %{xorg_lib_path} -L%{_libdir}/boost/gcc4 -R%{_libdir}/boost/gcc4"
export PATH="%{gnu_bin}:%{_prefix}/sfw/bin:${OPATH}"
export PKG_CONFIG_PATH=%{_prefix}/lib/pkgconfig:%{_prefix}/gnu/lib/pkgconfig
#export CMAKE_LIBRARY_PATH="%{xorg_lib}:%{gnu_lib}:%{_prefix}/lib:/lib"

#cmake   .. -DCMAKE_INSTALL_PREFIX=%{_prefix}      \
#        -DCMAKE_BUILD_TYPE=Release                                      \
#        -DCMAKE_C_COMPILER:FILEPATH=${CC}                               \
#        -DCMAKE_C_FLAGS:STRING="${CFLAGS}"                              \
#        -DCMAKE_CXX_COMPILER:FILEPATH=${CXX}                            \
#        -DCMAKE_CXX_FLAGS_RELEASE:STRING="${CXXFLAGS}"                  \
#        -DCMAKE_INCLUDE_PATH="%{gnu_inc}"                               \
#        -DCMAKE_SKIP_RPATH:BOOL=YES                                     \
#        -DINCLUDE_INSTALL_DIR=%{_includedir}                            \
#        -DSYSCONF_INSTALL_DIR=%{_sysconfdir}                            \
#        -DBOOST_INCLUDEDIR=%{_includedir}/boost/gcc4                    \
#        -DBOOST_LIBRARYDIR=%{_libdir}/boost/gcc4                        \
#        -DBoost_IOSTREAMS_LIBRARY=%{_libdir}/boost/gcc4/libboost_iostreams-mt.so \
#        -DBoost_REGEX_LIBRARY=%{_libdir}/boost/gcc4/libboost_regex-mt.so \
#        -DBUILD_SHARED_LIBS=On                                          \
#        -DCMAKE_VERBOSE_MAKEFILE=1 > config.log 2>&1

# Use autotools now and switch to cmake/scons when it is complete

[ ! -f configure.orig ] && cp configure configure.orig 
cat configure.orig | sed '{
    s#/opt/local/include#%{_includedir}/boost/gcc4#
    s#\-Werror##g
}' > configure
bash ./configure --prefix=%{_prefix} \
                 --localstatedir=%{_localstatedir} \
                 --enable-python-install \
                 --enable-tools \
                 --enable-campaign-server \
                 --enable-bandwidth-monitor

gmake -j$CPUS

%install
rm -Rf $RPM_BUILD_ROOT
gmake install DESTDIR=$RPM_BUILD_ROOT

mv ${RPM_BUILD_ROOT}/lib ${RPM_BUILD_ROOT}%{_prefix}
mv ${RPM_BUILD_ROOT}%{_prefix}/lib/python ${RPM_BUILD_ROOT}%{_prefix}/lib/python2.6

#
# make install is broken unfortunately
#
cp -r data ${RPM_BUILD_ROOT}%{_datadir}/wesnoth
cp -r fonts ${RPM_BUILD_ROOT}%{_datadir}/wesnoth
cp -r icons ${RPM_BUILD_ROOT}%{_datadir}/wesnoth
cp -r images ${RPM_BUILD_ROOT}%{_datadir}/wesnoth
cp -r sounds ${RPM_BUILD_ROOT}%{_datadir}/wesnoth
cd ..

%clean
rm -Rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/wesnoth
%{_bindir}/wml*
%{_bindir}/exploder
%{_bindir}/cutter
%{_bindir}/campaignd
%{_bindir}/wesnoth_addon_manager
%defattr (0755, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*
%defattr (-, root, other)
%dir %attr (0755, root, other) %{wesnoth_datadir}
%{wesnoth_datadir}/*
%dir %attr (0755, root, other) %{_datadir}/icons
%{_datadir}/icons/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, other) %{_docdir}/wesnoth
%{_docdir}/wesnoth/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/python%{python_vers}
%dir %attr (0755, root, bin) %{_libdir}/python%{python_vers}/site-packages
%{_libdir}/python%{python_vers}/site-packages/*

%files server
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/wesnothd
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, sys) %{_localstatedir}/run
%dir %attr (0750, root, other) %{_localstatedir}/run/wesnothd

%changelog
* Mon Oct 12 2009 - Moinak Ghosh
- Adapted and modified from SFE repo.
* Fri Aug 07 2009 - Petr Sobotka sobotkap@gmail.com
- Bump to version 1.6.4
* Sat Apr 18 2009 - Petr Sobotka sobotkap@gmail.com
- Bump to 1.6.1 (merged from SFEwesnoth-dev)
* Sat Mar 14 2009 - Milan Jurik
- Bump to 1.4.7
* Sun Oct 12 2008 - Petr Sobotka <sobotkap@gmail.com>
- Bump to 1.4.5
* Mon Jul 28 2008 - Petr Sobotka <sobotkap@gmail.com>
- Bump to 1.4.4
* Sun Jun 22 2008 - Petr Sobotka <sobotkap@gmail.com>
- Bump to 1.4.3 version
* Wed May 07 2008 - Petr Sobotka <sobotkap@centrum.cz>
- Bump to 1.4.2 version
* Mon Mar 10 2008 - Petr Sobotka <sobotkap@centrum.cz>
- Bump to 1.4 stable version.
- Changed preferences dir to ~/.wesnoth from ~/.wesnoth-dev which will 
	be used for development releases in future.
* Sun Feb 24 2008 - Petr Sobotka <sobotkap@centrum.cz>
- Bump to 1.3.19 (last rc release before 1.4)
* Tue Feb 19 2008 - Petr Sobotka <sobotkap@centrum.cz>
- Bump to 1.3.18
* Thu Feb 14 2008 - Petr Sobotka <sobotkap@centrum.cz>
- Bump to 1.3.16
* Tue Jan 29 2008 - Petr Sobotka <sobotkap@centrum.cz>
- Bump to 1.3.15
* Wed Jan 16 2008 - Petr Sobotka <sobotkap@centrum.cz>
- Bump to 1.3.14
* Sat Jan 05 2008 - Petr Sobotka <sobotkap@centrum.cz>
- Removed --enable-dummy-locales option from configure as it cause warning 
* Tue Jan 01 2008 - Petr Sobotka <sobotkap@centrum.cz>
- Bump to 1.3.13
- Introduced new dependency SFEboost
- Changed compiler from gcc to sun studio + stlport4 (need to be same as for boost)
* Sat Dec 01 2007 - Petr Sobotka <sobotkap@centrum.cz>
- Bump to 1.3.12
* Mon Nov 19 2007 - Petr Sobotka <sobotkap@centrum.cz>
- Bump to 1.3.11
* Thu Nov 15 2007 - daymobrew@users.sourceforge.net
- Enable building with either SUNWlibsdl or SFEsdl.
* Sun Nov 11 2007 Petr Sobotka <sobotkap@centrum.cz>
- bump to 1.3.10
* Fri Oct 19 2007 Petr Sobotka <sobotkap@centrum.cz>
- bump to 1.3.9
- add html documentation
* Wed Sep 19 2007 Petr Sobotka <sobotkap@centrum.cz>
- bump to 1.3.8
* Thu Sep 6 2007 Petr Sobotka <sobotkap@centrum.cz>
- Initial version
