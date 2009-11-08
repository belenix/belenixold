#
# spec file for package SFEsupertuxkart.spec
#
# includes module(s): supertuxkart
#
%include Solaris.inc

%define src_name	supertuxkart

Name:                   SFEsupertuxkart
Summary:                Super Tux Kart Racing game
Version:                0.6.2a
Source:                 %{sf_download}/supertuxkart/%{src_name}-%{version}-src.tar.bz2

SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWxorg-headers
Requires: SUNWxorg-mesa
BuildRequires: SUNWogg-vorbis-devel
Requires: SUNWogg-vorbis
BuildRequires: SFEsdl-image-devel
Requires: SFEsdl-image
BuildRequires: SFEopenal-devel
Requires: SFEopenal
BuildRequires: SFEplib

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
%setup -q -c -n %{name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

cd %{src_name}-%{version}

export LDFLAGS="%_ldflags -lsocket -lnsl %{gnu_lib_path} %{xorg_lib_path} -lGLU"
export CFLAGS="-D_XPG4_2"
export CXXFLAGS="-D_XPG4_2"

./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared		\
	    --disable-static

gmake -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
cd %{src_name}-%{version}
gmake install DESTDIR=${RPM_BUILD_ROOT}
mv ${RPM_BUILD_ROOT}%{_prefix}/games ${RPM_BUILD_ROOT}%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755,root,sys) %{_datadir}
%{_datadir}/games
%dir %attr (0755,root,other) %{_datadir}/doc
%dir %attr (0755,root,other) %{_datadir}/applications
%dir %attr (0755,root,other) %{_datadir}/pixmaps
%{_datadir}/doc/*
%{_datadir}/applications/*
%{_datadir}/pixmaps/*

%changelog
* Sun Nov 08 2009 - Moinak Ghosh
- Initial version
