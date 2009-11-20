#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

Name:                SFEvegastrike
Summary:             3D OpenGL spaceflight simulator
Version:             0.5.0
License:             GPLv2+
Group:               Amusements/Games
Source:              %{sf_download}/vegastrike/vegastrike-src-%{version}.tar.bz2
Source1:             vegastrike.desktop
Source3:             vegastrike.png
Patch0:              vegastrike-00-char-fix.diff
Patch1:              vegastrike-01-paths-fix.diff
Patch3:              vegastrike-03-vssetup-fix.diff
Patch4:              vegastrike-04-64-bit.diff
Patch5:              vegastrike-05-openal.diff
Patch6:              vegastrike-06-sys-python.diff
Patch7:              vegastrike-07-boost-make_shared.diff
Patch8:              vegastrike-08-gcc44.diff
Patch9:              vegastrike-09-solaris.diff

URL:                 http://vegastrike.sourceforge.net/
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWxorg-mesa
BuildRequires: SUNWxorg-headers
Requires: SFEfreeglut
BuildRequires: SFEfreeglut-devel
Requires: SUNWgtk2
BuildRequires: SUNWgtk2-devel
Requires: SUNWjpg
BuildRequires: SUNWjpg-devel
Requires: SFEboost-gpp
BuildRequires: SFEboost-gpp-devel
Requires: SFEfreealut
BuildRequires: SFEfreealut-devel
Requires: SUNWlexpt
Requires: SUNWpng
BuildRequires: SUNWpng-devel
Requires: SUNWPython26
BuildRequires: SUNWPython26-devel
Requires: SUNWogg-vorbis
BuildRequires: SUNWogg-vorbis-devel
Requires: SFEopenal
BuildRequires: SFEopenal-devel
Requires: SFEfreealut
BuildRequires: SFEfreealut-devel
Requires: SFEsdl-mixer
BuildRequires: SFEsdl-mixer-devel
Requires: SUNWgnome-desktop-prefs
BuildRequires: SUNWgnome-common-devel
Requires: SUNWgnome-themes
BuildRequires: SUNWxdg-utils
Requires: SFEogre
BuildRequires: SFEogre-devel
Requires: SFEcegui
BuildRequires: SFEcegui-devel
Requires: SFEvegastrike-data

%description
Vega Strike is a GPL 3D OpenGL Action RPG space sim that allows a player to
trade and bounty hunt. You start in an old beat up Wayfarer cargo ship, with
endless possibility before you and just enough cash to scrape together a life.
Yet danger lurks in the space beyond.

%prep
%setup -q -c -n %name-%version
ln -s %{_libdir}/boost/gcc4/libboost_python-mt.so libboost_python.so
cd vegastrike-source-%{version}
%patch0 -p1
%patch1 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1 
%patch9 -p1 

%{gnu_bin}/sed -i 's/-lboost_python-st/-lboost_python/g' Makefile.in
# we want to use the system version of expat.h
rm objconv/mesher/expat.h

#
# Munge usages of _X due to clash with ctype.h
# There is a comment in IcePreprocessor.h: '// Silly Cygwin defines _X in ctypes.h'
# followed by '#undef _X'
# This approach is silly with potential to mess other stuff in system headers which it
# does on Solaris. Why not change the variable name !
#
# We also need to munge WRAP and quad. WRAP comes in from termios hdr via Python 2.6 and quad
# comes in from sys/types.h being used by UFS - this arguably is a bad Solaris bug.
#
for f in `find . \( -name "*.h*" -o -name "*.c*" \) | fgrep -v ".svn" | xargs egrep -w "_X|WRAP|quad" | cut -f1 -d":" | uniq`
do
	%{gnu_bin}/sed -i 's/\<_X\>/_X_/g' ${f}
	%{gnu_bin}/sed -i 's/\<WRAP\>/_WRAP_/g' ${f}
	%{gnu_bin}/sed -i 's/\<quad\>/_quad_/g' ${f}
done

%build
PDIR=`pwd`
cd vegastrike-source-%{version}
export LDFLAGS="-lsocket -lnsl -lm -L%{_libdir}/boost/gcc4 -R%{_libdir}/boost/gcc4 %{gnu_lib_path} -L${PDIR}"
export CPPFLAGS="-DBOOST_PYTHON_NO_PY_SIGNATURES -DSOLARIS -DBYTE_ORDER=0 -DBIG_ENDIAN=1 -march=pentium3 -I%{_includedir}/boost/gcc4"

#
# Configure refuses --with-python-version=2.6 so we force this backdoor.
#
%{gnu_bin}/sed -i "s#with_python_version=2.4#with_python_version=2.6#" configure
./configure --prefix=%{_prefix} --with-data-dir=%{_datadir}/vegastrike --with-boost=system \
 	--enable-release \
	--disable-ffmpeg \
	--enable-stencil-buffer

#
# Unfortunately configure does not respect LDFLAGS
#
%{gnu_bin}/sed -i "s#-L/usr/X11R6/lib#-lsocket -lnsl -lm -L/usr/X11/lib -R/usr/X11/lib -L%{_libdir}/boost/gcc4 -R%{_libdir}/boost/gcc4 %{gnu_lib_path}  -L${PDIR}#" Makefile
gmake

%install
rm -rf $RPM_BUILD_ROOT
cd vegastrike-source-%{version}
gmake install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_libexecdir}/vegastrike
chmod +x $RPM_BUILD_ROOT%{_prefix}/objconv/*
mv $RPM_BUILD_ROOT%{_prefix}/objconv/* $RPM_BUILD_ROOT%{_libexecdir}/vegastrike
rmdir $RPM_BUILD_ROOT%{_prefix}/objconv

for i in asteroidgen base_maker mesh_xml mesher replace tempgen trisort \
	vsrextract vsrmake; do
	mv $RPM_BUILD_ROOT%{_bindir}/$i $RPM_BUILD_ROOT%{_libexecdir}/vegastrike
done

#  below is the desktop file and icon stuff.
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
	desktop-file-install --vendor fedora \
	--dir $RPM_BUILD_ROOT%{_datadir}/applications \
	%{SOURCE1} 

mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps/
ginstall -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps/vegastrike.png

%clean
rm -rf $RPM_BUILD_ROOT

%post
update-desktop-database %{_datadir}/applications 2>/dev/null || :
gtk-update-icon-cache -qf %{_datadir}/icons/hicolor 2>/dev/null || : 

%postun
update-desktop-database %{_datadir}/applications 2>/dev/null || :
gtk-update-icon-cache -qf %{_datadir}/icons/hicolor 2>/dev/null || :

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr(0755, root, sys) %{_datadir}

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/icons
%{_datadir}/icons/*

%changelog
* Fri Nov 20 2009 - Moinak Ghosh
- Initial version
