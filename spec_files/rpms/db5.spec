## WORK IN PROGRESS ##

Name:                    db5
Summary:                 The Berkeley DB database library (version 5) for C/C++
Version:                 5.1.19
Release:                 1%{?dist}
License:                 BSD
Group:                   System Environment/Libraries
Source:                  http://download-west.oracle.com/berkeley-db/db-%{version}.tar.gz
URL:                     http://www.oracle.com/technology/software/products/berkeley-db/index.html
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%if %gcc_compiler
Requires: libgcc
%endif
#Requires: tcl
#BuildRequires: tcl-devel
#BuildRequires: java6-devel

%description
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. The Berkeley DB includes B+tree, Extended
Linear Hashing, Fixed and Variable-length record access methods,
transactions, locking, logging, shared memory caching, and database
recovery. The Berkeley DB supports C, C++, Java, and Perl APIs. It is
used by many applications, including Python and Perl, so this should
be installed on all systems.

%package devel
Summary:                 C/C++ development files for the Berkeley DB (version 5) library
Group:                   Development/Libraries
Requires: %name = %{version}-%{release}
#Requires: tcl-devel
#Requires: java6-devel

%description devel
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. This package contains the header files,
libraries, and documentation for building programs which use the
Berkeley DB.

%package doc
Summary:                 Documentation files for the Berkeley DB (version 5) library
Requires: %name = %{version}-%{release}

%description doc
HTML documentation files for the Berkeley DB (version 5) library.

%prep
%bsetup

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

cd db-%{version}
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%{_ldflags} -lstdc++"
cd build_unix
../dist/configure  -C                       \
        --prefix=%{_prefix}                 \
        --bindir=%{_bindir}                 \
        --libdir=%{_libdir}                 \
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
        --enable-sql                        \
        --enable-sql_codegen                \
        --enable-posixmutexes               \
        --enable-largefile                  \
        --enable-shared                     \
        --disable-static                    \
        --program-transform-name=s,^db,db51,

gmake -j$CPUS 
cd ../..

%install
rm -rf $RPM_BUILD_ROOT

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
%{_bindir}/db*
%{_libdir}/libdb*
%{_libdir}/*.jar

%files devel
%defattr (-, root, bin)
%{_includedir}/*

%files doc
%defattr (-, root, bin)
%{_datadir}/doc/*

%changelog
