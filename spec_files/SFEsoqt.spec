#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

Name:                SFEsoqt
Summary:             Qt Bindings
Version:             1.4.1
License:             GPL
URL:                 http://www.coin3d.org
Source:              http://ftp.coin3d.org/coin/src/all/SoQt-%{version}.tar.gz
Patch1:              soqt-01-gcc44.diff

SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SFEcoin3d
Requires: SUNWxorg-mesa
BuildRequires: SFEdoxygen
BuildRequires: SUNWxorg-headers
BuildRequires: SFEcoin3d-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name
Requires: SFEdoxygen
Requires: SFEcoin3d-devel
Requires: SUNWxorg-headers
Requires: SUNWxorg-mesa

%prep
%setup -q -c -n %name-%version
cd SoQt-%version
%patch1 -p1
cd ..

%ifarch amd64 sparcv9
cp -rp SoQt-%version SoQt-%{version}-64
%endif


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CPPFLAGS="-I%{_includedir}/qt4 -I%{_includedir}/qt4/Qt"
export OPATH="$PATH"

%ifarch amd64 sparcv9
cd SoQt-%{version}-64

export CFLAGS="%optflags64 ${CPPFLAGS}"
export CXXFLAGS="%cxx_optflags64 ${CPPFLAGS}"
export LDFLAGS="%_ldflags64 %{gnu_lib_path64}"
export PKG_CONFIG_PATH="%{_pkg_config_path64}"
export PATH="%{_prefix}/qt4/bin/%{_arch64}:%{_bindir}/%{_arch64}:%{_prefix}/gnu/bin/%{_arch64}:${OPATH}"
export MOC=%{_prefix}/qt4/bin/%{_arch64}/moc
export CONFIG_QTLIBS=`pkg-config --libs QtGui`

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir}/%{_arch64} \
            --libdir=%{_libdir}/%{_arch64} \
            --sysconfdir=%{_sysconfdir} \
            --includedir=%{_includedir} \
            --libexecdir=%{_libexecdir} \
            --mandir=%{_mandir} \
            --with-alternate=default-64 \
            --with-mesa \
            --with-qt=true \
            --enable-threadsafe \
            --enable-html

gmake -j$CPUS

cp soqt-config soqt-config.orig
cat soqt-config.orig | sed '{
    s#/usr/include/Inventor/annex#/usr/include/Inventor/Qt#
    s#-lqt-mt##
}' > soqt-config

cd ..
%endif

cd SoQt-%{version}
export CFLAGS="%optflags ${CPPFLAGS}"
export CXXFLAGS="%cxx_optflags ${CPPFLAGS}"
export LDFLAGS="%_ldflags %{gnu_lib_path}"
export PKG_CONFIG_PATH="%{_pkg_config_path}"
export PATH="%{_prefix}/qt4/bin:$OPATH"
export MOC=%{_prefix}/qt4/bin/moc
export CONFIG_QTLIBS=`pkg-config --libs QtGui`

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --libdir=%{_libdir} \
            --sysconfdir=%{_sysconfdir} \
            --includedir=%{_includedir} \
            --libexecdir=%{_libexecdir} \
            --mandir=%{_mandir} \
            --with-mesa \
            --with-qt=true \
            --enable-threadsafe \
            --enable-html

gmake -j$CPUS

cp soqt-config soqt-config.orig
cat soqt-config.orig | sed '{
    s#/usr/include/Inventor/annex#/usr/include/Inventor/Qt#
    s#-lqt-mt##
}' > soqt-config

cd ..


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd SoQt-%{version}-64

gmake DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/*.la
cd ..
%endif

cd SoQt-%{version}
gmake DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

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
%dir %attr(0755, root, other) %{_datadir}/SoQt
%{_datadir}/SoQt/*
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
%{_bindir}/soqt-config
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%dir %attr (0755, root, other) %{_datadir}/Coin
%{_datadir}/Coin/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/soqt-config
%endif

%changelog
* Sun Oct 04 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Initial version.
