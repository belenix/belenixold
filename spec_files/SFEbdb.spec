#
# spec file for package SFEbdb
#
# includes module(s): bdb
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc


Name:                    SFEbdb
Summary:                 Berkeley DB
Version:                 4.5.20
Source:                  http://download-west.oracle.com/berkeley-db/db-%{version}.tar.gz
URL:                     http://www.oracle.com/technology/software/products/berkeley-db/index.html
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
%if %cc_is_gcc
Requires: SFEgccruntime
%endif
BuildRequires: SUNWTcl
BuildRequires: SUNWj6dev

%package devel
Summary:                 %{summary} - Development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%package doc
Summary:                 %{summary} - Documentation files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name


%prep
%setup -q -c -n %name-%version
%ifarch amd64 sparcv9
cp -rp db-%{version} db-%{version}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

%ifarch amd64 sparcv9
cd db-%{version}-64
export CFLAGS="%optflags64"
export CXXFLAGS="%cxx_optflags64"
export LDFLAGS="%{_ldflags64} %{gnu_lib_path64} -lstdc++"
cd build_unix
../dist/configure                           \
        --prefix=%{_prefix}                 \
        --bindir=%{_bindir}/%{_arch64}      \
        --libdir=%{_libdir}/%{_arch64}      \
        --libexecdir=%{_libexecdir}         \
        --mandir=%{_mandir}                 \
        --datadir=%{_datadir}               \
        --infodir=%{_datadir}/info          \
        --datadir=%{_localstatedir}/bdb/data \
        --localstatedir=%{_localstatedir}/bdb \
        --disable-warnings                  \
        --disable-debug                     \
        --enable-cryptography               \
        --enable-hash                       \
        --enable-queue                      \
        --enable-verify                     \
        --enable-cxx                        \
        --enable-java                       \
        --enable-tcl --with-tcl=%{_libdir}/%{_arch64} \
        --enable-posixmutexes               \
        --enable-rpc                        \
        --enable-largefile                  \
        --enable-shared                     \
        --disable-static

make -j$CPUS
cd ../..
%endif

cd db-%{version}
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%{_ldflags} %{gnu_lib_path} -lstdc++"
cd build_unix
../dist/configure                           \
        --prefix=%{_prefix}                 \
        --libexecdir=%{_libexecdir}         \
        --mandir=%{_mandir}                 \
        --datadir=%{_datadir}               \
        --infodir=%{_datadir}/info          \
        --datadir=%{_localstatedir}/bdb/data \
        --localstatedir=%{_localstatedir}/bdb \
        --disable-warnings                  \
        --disable-debug                     \
        --enable-cryptography               \
        --enable-hash                       \
        --enable-queue                      \
        --enable-verify                     \
        --enable-cxx                        \
        --enable-java                       \
        --enable-tcl --with-tcl=%{_libdir}  \
        --enable-posixmutexes               \
        --enable-rpc                        \
        --enable-largefile                  \
        --enable-shared                     \
        --disable-static

make -j$CPUS 
cd ../..

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd db-%{version}-64

cd build_unix
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/*.la
mkdir -p $RPM_BUILD_ROOT%{_prefix}/share/doc
mv $RPM_BUILD_ROOT%{_prefix}/docs $RPM_BUILD_ROOT%{_prefix}/share/doc/bdb
(cd $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/
    ln -s libdb.so libdb.so.1)
cd ../..
%endif

cd db-%{version}
cd build_unix
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
mkdir -p $RPM_BUILD_ROOT%{_prefix}/share/doc
mv $RPM_BUILD_ROOT%{_prefix}/docs $RPM_BUILD_ROOT%{_prefix}/share/doc/bdb
(cd $RPM_BUILD_ROOT%{_libdir}
    ln -s libdb.so libdb.so.1)
cd ../..


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/db*
%{_bindir}/berkeley*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libdb*
%{_libdir}/*.jar

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/db*
%{_bindir}/%{_arch64}/berkeley*
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/libdb*
%{_libdir}/%{_arch64}/*.jar
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%files doc
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%changelog
* Fri May 22 2009 - moinakg@belenix.org
- Add 64Bit build.
- Split package into base, devel and doc.
- Update configure options.
* Mon Feb 18 2008 - moinak.ghosh@sun.com
- Add link to libdb.so.1
* Fri Jan 05 2007 - daymobrew@users.sourceforge.net
- Add URL.
* Tue Nov 07 2006 - glynn.foster@sun.com
- Initial spec file
