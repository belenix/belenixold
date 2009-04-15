#
# spec file for package SFEopenexr.spec
#
# includes module(s): openexr
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

%define src_name	openexr
%define src_url		http://download.savannah.nongnu.org/releases/openexr

Name:                   SFEopenexr
Summary:                openexr - high dynamic-range (HDR) image file format
Version:                1.6.1
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEilmbase-devel
Requires: SFEilmbase

%package devel
Summary:                 openexr-devel - high dynamic-range (HDR) image file format development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
%setup -q -c -n %{name}-%{version}

%ifarch amd64 sparcv9
cp -pr %{src_name}-%{version} %{src_name}-%{version}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi


ln -s `which automake-1.9` automake
ln -s `which aclocal-1.9` aclocal
export PATH=$PWD:$PATH
CC32=$CC
CXX32=$CXX

%ifarch amd64 sparcv9
cd %{src_name}-%{version}-64

X11LIBS="-L/usr/X11/lib/%{_arch64} -R/usr/X11/lib/%{_arch64}"
SFWLIBS="-L/usr/sfw/lib/%{_arch64} -R/usr/sfw/lib/%{_arch64}"
export CC="${CC} -m64"
export CXX="${CXX} -m64"
export CPPFLAGS="-I/usr/X11/include"
export CXXFLAGS="-O3 -fno-omit-frame-pointer"
export CFLAGS="%optflags64"
export LDFLAGS="%_ldflags64 $X11LIBS $SFWLIBS -lstdc++"
export LD_OPTIONS="-i"
bash ./bootstrap
./configure --prefix=%{_prefix}         \
            --bindir=%{_bindir}/%{_arch64}         \
            --mandir=%{_mandir}         \
            --libdir=%{_libdir}/%{_arch64}         \
            --datadir=%{_datadir}       \
            --libexecdir=%{_libexecdir}/%{_arch64} \
            --sysconfdir=%{_sysconfdir} \
            --disable-rpath             \
            --enable-shared             \
            --disable-static
make -j $CPUS
cd ..
%endif

cd %{src_name}-%{version}

export CC=$CC32
export CXX=$CXX32
X11LIBS="-L/usr/X11/lib -R/usr/X11/lib"
SFWLIBS="-L/usr/sfw/lib -R/usr/sfw/lib"
export CPPFLAGS="-I/usr/X11/include"
export CXXFLAGS="-O3 -fno-omit-frame-pointer"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags $X11LIBS $SFWLIBS -lstdc++"
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
            --enable-shared		\
	    --disable-static
make -j $CPUS 

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd %{src_name}-%{version}-64

make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT/%{_libdir}/%{_arch64}/lib*.*a
cd ..
%endif

cd %{src_name}-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT/%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/lib*.so*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/*.so*
%endif

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755,root,bin) %{_libdir}
%dir %attr (0755,root,other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc
%dir %attr (0755,root,sys) %{_datadir}
%dir %attr (0755,root,other) %{_datadir}/doc
%dir %attr (0755,root,other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%{_datadir}/doc/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif


%changelog
* Wed Apr 15 2009 - moinakg@belenix.org
- Enable 64Bit build.
* Tue Oct 28 2008 - moinakg@belenix.org
- Bump version to 1.6.1
- Fix summary to have proper common names.
* Mon May  7 2007 - dougs@truemail.co.th
- Initial version
