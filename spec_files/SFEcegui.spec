#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define cc_is_gcc 1
%include base.inc
Name:                SFEcegui
Summary:             Free library providing windowing and widgets for graphics APIs / engines
Version:             0.6.2
License:             MIT
Source:              %{sf_download}/crayzedsgui/CEGUI-%{version}.tar.gz
Source1:             %{sf_download}/crayzedsgui/CEGUI-%{version}-DOCS.tar.gz
Patch1:		     cegui-01-release-as-so-ver.diff
Patch2:		     cegui-02-userverso.diff
Patch3:              cegui-03-new-DevIL.diff
Patch4:              cegui-04-solaris.diff

URL:                 http://www.cegui.org.uk
Group:               System Environment/Libraries
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFElibdevil
BuildRequires: SFElibdevil-devel
Requires: SUNWlexpt
Requires: SUNWfreetype2
Requires: SUNWlxml
Requires: SUNWxorg-mesa
BuildRequires: SUNWxorg-headers
Requires: SFElua
Requires: SUNWpcre
Requires: SFESilly
BuildRequires: SFESilly-devel
Requires: SFExerces-c
BuildRequires: SFExerces-c-devel
Requires: SFEtoluapp
BuildRequires: SFEtoluapp-devel
Requires: SFEglew

%description
Crazy Eddie's GUI System is a free library providing windowing and widgets for
graphics APIs / engines where such functionality is not natively available, or
severely lacking. The library is object orientated, written in C++, and
targeted at games developers who should be spending their time creating great
games, not building GUI sub-systems! 

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SFElibdevil-devel
Requires: SUNWxorg-headers
Requires: SFElua
Requires: SFESilly-devel
Requires: SFExerces-c-devel
Requires: SFEtoluapp-devel
Requires: SFEglew

%prep
%setup -q -n CEGUI-%{version}
%patch1 -p1 
%patch2 -p1 
%patch3 -p1 
%patch4 -p1 

# Permission fixes for debuginfo RPM
chmod -x include/falagard/*.h

# Delete zero length file
rm -f documentation/api_reference/keepme 

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags"
export Lua_CFLAGS="-I%{_includedir}"
export Lua_LIBS="-llua"

./configure --prefix=%{_prefix} --disable-static --disable-corona --enable-devil \
            --enable-lua-module --disable-irrlicht-renderer --disable-samples \
            --disable-directfb-renderer \
            --with-default-xml-parser=ExpatParser --enable-silly \
            --with-default-image-codec=SILLYImageCodec --with-pic

# We do not want to get linked against a system copy of ourselves!
sed -i 's|-L%{_libdir}||g' RendererModules/OpenGLGUIRenderer/Makefile
# Don't use rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
gmake -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
gmake install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

mkdir -p $RPM_BUILD_ROOT%{_docdir}/CEGUI
cp -r documentation $RPM_BUILD_ROOT%{_docdir}/CEGUI

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/CEGUI
%{_datadir}/CEGUI/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%doc %{_docdir}/*

%changelog
* Sat Nov 21 2009 - Moinak Ghosh
- Initial version
