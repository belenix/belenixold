#
#
# Copyright(c) 2009, BeleniX Team
#
#

%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc


Name:                SFElog4cxx
Summary:             A port to C++ of the Log4j project
Version:             0.10.0
License:             ASLv2.0
Source:              http://www.apache.org/dist/logging/log4cxx/%{version}/apache-log4cxx-%{version}.tar.gz
URL:                 http://logging.apache.org/log4cxx/index.html
Patch1:              log4cxx-01-cstring.diff

SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SFElibapr-devel
BuildRequires: SFEaprutil-devel
BuildRequires: SFEdoxygen
BuildRequires: SFEgraphviz
Requires: SFElibapr
Requires: SFEaprutil

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name
Requires: SFElibapr-devel
Requires: SFEaprutil-devel
Requires: SFEdoxygen

%prep
%setup -q -c -n %name-%version
cd apache-log4cxx-%version
%patch1 -p1
cd ..

%ifarch amd64 sparcv9
cp -rp apache-log4cxx-%version apache-log4cxx-%{version}-64
%endif


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi
OPATH="${PATH}"

%ifarch amd64 sparcv9
cd apache-log4cxx-%{version}-64

export CFLAGS="%optflags64"
export CXXFLAGS="%cxx_optflags64"
export LDFLAGS="%_ldflags64 -L/lib/%{_arch64} -R/lib/%{_arch64}"
export PATH="%{_prefix}/bin/%{_arch64}:%{_prefix}/gnu/bin/%{_arch64}:${PATH}"

cp configure configure.orig 
sed -e '/sys_lib_dlsearch_path_spec/s|/usr/lib |/usr/lib /usr/lib/%{_arch64} /lib /lib/%{_arch64} |' \
configure

./configure --prefix=%{_prefix}  \
            --bindir=%{_bindir}/%{_arch64} \
            --libdir=%{_libdir}/%{_arch64} \
            --mandir=%{_mandir}

make -j$CPUS
cd ..
%endif

cd apache-log4cxx-%{version}
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags -L/lib -R/lib"
export PATH="${OPATH}"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}

make -j$CPUS
cd ..


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd apache-log4cxx-%{version}-64

make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT/usr/lib/%{_arch64}/*.a
rm -rf $RPM_BUILD_ROOT/usr/lib/%{_arch64}/*.la
cd ..
%endif

cd apache-log4cxx-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT/usr/lib/*.a
rm -rf $RPM_BUILD_ROOT/usr/lib/*.la

mkdir -p ${RPM_BUILD_ROOT}%{_docdir}
mv ${RPM_BUILD_ROOT}%{_datadir}/log4cxx ${RPM_BUILD_ROOT}%{_docdir}
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*

%changelog
* Fri May 29 2009 - Moinak Ghosh <moinakg@belenix(dot)org>
- Initial version.
