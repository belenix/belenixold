#
# spec file for package SFEcppunit.spec
#
# includes module(s): cppunit
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

%define src_name	cppunit
Name:                   SFEcppunit
Summary:                C++ port of JUnit
Version:                1.12.1
URL:                    http://apps.sourceforge.net/mediawiki/cppunit/index.php?title=Main_Page
Source:                 %{sf_download}/%{src_name}/%{src_name}-%{version}.tar.gz
Patch1:                 cppunit-01-floatingpoint.diff

SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEdoxygen
BuildRequires: SFEgraphviz

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
%setup -q -c -n %name-%version
cd %{src_name}-%{version}
%patch1 -p1
cd ..

%ifarch amd64 sparcv9
cp -rp %{src_name}-%{version} %{src_name}-%{version}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

%ifarch amd64 sparcv9
cd %{src_name}-%{version}-64

libtoolize --force --copy
aclocal-1.9 -I config
autoheader
automake-1.9 -a
autoconf --force -I config
export CC=/usr/gnu/bin/gcc
export CXX=/usr/gnu/bin/g++
export CFLAGS="-m64 -O3 -Xlinker -i -fno-omit-frame-pointer"
export CXXFLAGS="-m64 -O3 -Xlinker -i -fno-omit-frame-pointer"
export LDFLAGS="%_ldflags64 %{gnu_lib_path64} %{xorg_lib_path64} -lX11"
./configure --prefix=%{_prefix}         \
            --bindir=%{_bindir}/%{_arch64} \
            --mandir=%{_mandir}         \
            --libdir=%{_libdir}/%{_arch64} \
            --datadir=%{_datadir}       \
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --disable-libtool-lock      \
            --enable-typeinfo-name      \
            --enable-shared             \
            --disable-static
make -j$CPUS
cd .. 
%endif

cd %{src_name}-%{version}

libtoolize --force --copy
aclocal-1.9 -I config
autoheader
automake-1.9 -a
autoconf --force -I config
export CC=/usr/gnu/bin/gcc
export CXX=/usr/gnu/bin/g++
export CFLAGS="-O3 -Xlinker -i -fno-omit-frame-pointer"
export CXXFLAGS="-O3 -Xlinker -i -fno-omit-frame-pointer"
export LDFLAGS="%_ldflags -lX11"
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --disable-libtool-lock      \
            --enable-typeinfo-name      \
            --enable-shared		\
	    --disable-static
make -j$CPUS 
cd ..


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd %{src_name}-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/lib*.*a
cd ..
%endif

cd %{src_name}-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/lib*.*a
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755,root,bin) %{_bindir}
%{_bindir}/cppunit-config
%{_bindir}/DllPlugInTester
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/lib*.so*

%ifarch amd64 sparcv9
%dir %attr (0755,root,bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/cppunit-config
%{_bindir}/%{_arch64}/DllPlugInTester
%dir %attr (0755,root,bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%dir %attr (0755,root,sys) %{_datadir}
%{_mandir}

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755,root,bin) %{_libdir}
%dir %attr (0755,root,other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc

%ifarch amd64 sparcv9
%dir %attr (0755,root,bin) %{_libdir}/%{_arch64}
%dir %attr (0755,root,other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%dir %attr (0755,root,sys) %{_datadir}
%dir %attr (0755,root,other) %{_datadir}/doc
%dir %attr (0755,root,other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%{_datadir}/doc/*


%changelog
* Fri May 29 2009 - Moinak Ghosh <moinakg@belenix(dot)org>
- Added 64Bit build.
* Mon May 04 2009 - moinakg@belenix.org
- Fix undefined symbol issue.
* Sun May 03 2009 - moinakg@belenix.org
- Bump version to 1.12.1, enable build using Gcc4.
* Fri Jan 18 2008 - moinak.ghosh@sun.com
- Added doxygen,graphviz as buildrequires
* Mon May  7 2007 - dougs@truemail.co.th
- Initial version
