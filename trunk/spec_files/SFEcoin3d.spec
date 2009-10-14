#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

Name:                SFEcoin3d
Summary:             High-level retained-mode 3D graphics toolkit
Version:             3.1.1
License:             GPL
Source:              http://ftp.coin3d.org/coin/src/all/Coin-%{version}.tar.gz
URL:                 http://www.coin3d.org

SUNW_BaseDir:        %{_basedir}
#SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWbzip
Requires: SUNWfreetype2
Requires: SUNWfontconfig
Requires: SUNWzlib
Requires: SUNWxorg-mesa
Requires: SFEsimage
BuildRequires: SFEdoxygen
BuildRequires: SUNWxorg-headers
BuildRequires: SFEsimage-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name
Requires: SFEdoxygen
Requires: SUNWfreetype2
Requires: SUNWfontconfig
Requires: SUNWxorg-headers
Requires: SUNWzlib
Requires: SUNWbzip
Requires: SFEsimage-devel

%prep
%setup -q -c -n %name-%version
cd Coin-%version
cd ..

%ifarch amd64 sparcv9
cp -rp Coin-%version Coin-%{version}-64
%endif


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

%ifarch amd64 sparcv9
cd Coin-%{version}-64

export CFLAGS="%optflags64"
export CXXFLAGS="%cxx_optflags64"
export LDFLAGS="%_ldflags64 %{xorg_lib_path64} -lGL -lGLU %{gnu_lib_path64}"

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir}/%{_arch64} \
            --libdir=%{_libdir}/%{_arch64} \
            --sysconfdir=%{_sysconfdir} \
            --includedir=%{_includedir} \
            --libexecdir=%{_libexecdir} \
            --with-simage \
            --with-mesa \
            --enable-threadsafe \
            --enable-html 

           # --with-fontconfig \
           # --with-spidermonkey \
           # --with-freetype \
           # --with-zlib \
           # --with-bzip2 \

gmake -j$CPUS

cd ..
%endif

cd Coin-%{version}
export CFLAGS="%optflags `pkg-config --cflags mozilla-js`"
export CXXFLAGS="%cxx_optflags `pkg-config --cflags mozilla-js`"
export LDFLAGS="%_ldflags `pkg-config --libs mozilla-js` %{xorg_lib_path} -lGL -lGLU %{gnu_lib_path}"

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --libdir=%{_libdir} \
            --sysconfdir=%{_sysconfdir} \
            --includedir=%{_includedir} \
            --libexecdir=%{_libexecdir} \
            --mandir=%{_mandir} \
            --with-simage \
            --with-mesa \
            --enable-threadsafe \
            --enable-html

            #--with-fontconfig \
            #--with-spidermonkey \
            #--with-freetype \
            #--with-zlib \
            #--with-bzip2 \

gmake -j$CPUS
cd ..


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd Coin-%{version}-64

gmake DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/*.la

cat $RPM_BUILD_ROOT%{_datadir}/Coin/conf/coin-default.cfg | sed '{
    s#\-lCoin#\-lCoin \-lGL \-lGLU#
}' > $RPM_BUILD_ROOT%{_datadir}/Coin/conf/coin-default-64.cfg
mv $RPM_BUILD_ROOT%{_bindir}/%{_arch64}/coin-config $RPM_BUILD_ROOT%{_bindir}/%{_arch64}/coin-config.orig
cat $RPM_BUILD_ROOT%{_bindir}/%{_arch64}/coin-config.orig | sed '{
    s@prefix=`cd "\$wd/.."; pwd`@prefix=%{_prefix}@
    s@alternate=default@alternate=default-64@
}' > $RPM_BUILD_ROOT%{_bindir}/%{_arch64}/coin-config
chmod a+x $RPM_BUILD_ROOT%{_bindir}/%{_arch64}/coin-config
rm -f $RPM_BUILD_ROOT%{_bindir}/%{_arch64}/coin-config.orig
cd ..
%endif

cd Coin-%{version}
gmake DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

mv $RPM_BUILD_ROOT%{_datadir}/Coin/conf/coin-default.cfg \
   $RPM_BUILD_ROOT%{_datadir}/Coin/conf/coin-default.cfg.orig
cat $RPM_BUILD_ROOT%{_datadir}/Coin/conf/coin-default.cfg.orig | sed '{
    s#\-lCoin#\-lCoin \-lGL \-lGLU#
}' > $RPM_BUILD_ROOT%{_datadir}/Coin/conf/coin-default.cfg
rm $RPM_BUILD_ROOT%{_datadir}/Coin/conf/coin-default.cfg.orig
if [ -d $RPM_BUILD_ROOT%{_prefix}/man ]
then
	rm -rf $RPM_BUILD_ROOT%{_prefix}/man
fi
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, other) %{_datadir}/Coin
%{_datadir}/Coin/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/coin-config
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/coin-config
%endif

%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*.h
%dir %attr (0755, root, bin) %{_includedir}/Inventor
%{_includedir}/Inventor/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%changelog
* Sun Oct 04 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Initial version.
