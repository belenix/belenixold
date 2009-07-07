#
# spec file for package SFEredland
#
# includes module(s): redland
#
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc


Name:                    SFEredland
Summary:                 A set of free software C libraries that provide support for the Resource Description Framework (RDF).
Version:                 1.0.9
URL:                     http://librdf.org/
Source:                  http://download.librdf.org/source/redland-%{version}.tar.gz

SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
License:                 LGPL
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEraptor
Requires: SUNWsqlite3
Requires: SUNWcurl
Requires: SFEbdb
Requires: SUNWgnu-idn
Requires: SFEgmp
Requires: SFEmpfr
Requires: SUNWopensslr
Requires: SUNWlxml
BuildRequires: SFEraptor-devel
BuildRequires: SUNWsqlite3-devel
BuildRequires: SUNWcurl-devel
BuildRequires: SFEgmp-devel
BuildRequires: SFEmpfr-devel
BuildRequires: SFEbdb-devel
BuildRequires: SUNWopenssl-include
BuildRequires: SUNWlxml-devel

%description
Redland is a set of free software C libraries that provide support
for the Resource Description Framework (RDF).

  * Modular, object based libraries and APIs for manipulating the
    RDF graph, triples, URIs and Literals.
  * Storage for graphs in memory and persistently with Sleepycat/Berkeley
    DB, MySQL 3-5, PostgreSQL, AKT Triplestore, SQLite, files or URIs.
  * Support for multiple syntaxes for reading and writing RDF as RDF/XML,
    N-Triples and Turtle Terse RDF Triple Language, RSS and Atom syntaxes
    via the Raptor RDF Parser Library.
  * Querying with SPARQL and RDQL using the Rasqal RDF Query Library.
  * Data aggregation and recording provenance support with Redland contexts.
  * Language Bindings in Perl, PHP, Python and Ruby via the Redland Bindings
    package.
  * Command line utility programs rdfproc (RDF), rapper (parsing) and
    roqet (query).
  * Portable, fast and with no known memory leaks.


%package devel
Summary:                 Development files for the redland package.
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SFEgcc
Requires: SUNWlxml-devel
Requires: SUNWcurl-devel
Requires: SFEraptor-devel
Requires: SUNWsqlite3-devel
Requires: SFEgmp-devel
Requires: SFEmpfr-devel
Requires: SFEbdb-devel
Requires: SUNWopenssl-include

%package doc
Summary:                 Documentation files for the redland package.
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name


%prep
%setup -q -c -n %name-%version
%ifarch amd64 sparcv9
cp -rp redland-%{version} redland-%{version}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
OPATH=${PATH}
export CPPFLAGS="-I%{_includedir}/gmp -I%{_includedir}/mpfr"

%ifarch amd64 sparcv9
cd redland-%{version}-64
export CFLAGS="%optflags64"
export CXXFLAGS="%cxx_optflags64"
export LDFLAGS="%_ldflags64 %{gnu_lib_path64}"
export PATH="%{_prefix}/bin/%{_arch64}:%{_prefix}/gnu/bin/%{_arch64}:${PATH}"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --bindir=%{_bindir}/%{_arch64}              \
            --libdir=%{_libdir}/%{_arch64}              \
            --libexecdir=%{_libexecdir}/%{_arch64}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-shared		     \
	    --disable-static                 \
            --with-pic                       \
            --with-mysql=no --with-postgresql=no \
            --with-sqlite-version=3 --with-sqlite=3 \
            --with-bdb=%{_prefix} -with-bdb-lib=%{_libdir}/%{_arch64} \
            --with-bdb-include=%{_includedir} \
            --with-openssl-digests            \
            --enable-release                  \
            --with-sqlite=3                   \
            --with-postgresql=no --with-mysql=no \
            --with-bdb-lib=%{_prefix}/lib/%{_arch64} \
            --with-bdb-include=%{_includedir} \
            --with-threads                    \
            --enable-gtk-doc=no

cp src/Makefile src/Makefile.orig 
cat src/Makefile.orig | sed '{
    s#librdf_storage_sqlite_la_LIBADD = -lsqlite3#librdf_storage_sqlite_la_LIBADD = -lsqlite3 -lrdf#
}' > src/Makefile

make -j$CPUS 
cd ..
%endif

cd redland-%{version}
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags %{gnu_lib_path}"
export PATH="${OPATH}"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --bindir=%{_bindir}              \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-shared                  \
            --disable-static                 \
            --with-pic                       \
            --with-mysql=no --with-postgresql=no \
            --with-sqlite-version=3 --with-sqlite=3 \
            --with-bdb=%{_prefix} -with-bdb-lib=%{_libdir} \
            --with-bdb-include=%{_includedir} \
            --with-openssl-digests            \
            --enable-release                  \
            --with-sqlite=3                   \
            --with-postgresql=no --with-mysql=no \
            --with-bdb-lib=%{_prefix}/lib/%{_arch64} \
            --with-bdb-include=%{_includedir} \
            --with-threads                    \
            --enable-gtk-doc=yes              \
            --with-html-dir=%{_docdir}

cp src/Makefile src/Makefile.orig 
cat src/Makefile.orig | sed '{
    s#librdf_storage_sqlite_la_LIBADD = -lsqlite3#librdf_storage_sqlite_la_LIBADD = -lsqlite3 -lrdf#
}' > src/Makefile

make -j$CPUS
cd ..


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd redland-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/redland/*.la
cd ..
%endif

cd redland-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/redland/*.la
cd ..

rm -rf ${RPM_BUILD_ROOT}%{_datadir}/gtk-doc


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/rdfproc
%{_bindir}/redland-db-upgrade
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%dir %attr (0755, root, bin) %{_libdir}/redland
%{_libdir}/redland/*.so

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/rdfproc
%{_bindir}/%{_arch64}/redland-db-upgrade
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/*.so*
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}/redland
%{_libdir}/%{_arch64}/redland/*.so
%endif

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, sys) %{_datadir}/redland
%{_datadir}/redland/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/redland-config
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/redland-config
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%files doc
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*

%changelog
* Tue Jul 07 2009 - moinakg(at)belenix<dot>org
- Fix build to link with correct libraries.
* Fri May 22 2009 - moinakg@belenix.org
- Initial version
