#
# spec file for package SFEraptor
#
# includes module(s): raptor
#
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc


Name:                    SFEraptor
Summary:                 Raptor RDF Parser Toolkit for Redland
Version:                 1.4.18
URL:                     http://librdf.org/raptor/
Source:                  http://download.librdf.org/source/raptor-%{version}.tar.gz

SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
License:                 LGPL
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlxml
Requires: SFEgccruntime
Requires: SUNWcurl
Requires: SUNWlxsl
BuildRequires: SFEgcc
BuildRequires: SUNWlxml-devel
BuildRequires: SUNWcurl-devel
BuildRequires: SUNWlxsl-devel

%description
Raptor is the RDF Parser Toolkit for Redland that provides a set of
Resource Description Framework (RDF) parsers and serializers,
generating RDF triples from the following syntaxes: RDF/XML,
N-Triples, TRiG, Turtle, RSS tag soup including all versions of RSS,
Atom 1.0 and 0.3, GRDDL and microformats for HTML, XHTML and XML. The
serializing RDF triples to syntaxes are: RDF/XML, RSS 1.0, Atom 1.0,
N-Triples, XMP, Turtle, GraphViz DOT and JSON.


%package devel
Summary:                 Development files for the raptor package.
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SFEgcc
Requires: SUNWlxml-devel
Requires: SUNWcurl-devel
Requires: SUNWlxsl-devel

%package doc
Summary:                 Documentation files for the raptor package.
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name


%prep
%setup -q -c -n %name-%version
%ifarch amd64 sparcv9
cp -rp raptor-%{version} raptor-%{version}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
OPATH=${PATH}

%ifarch amd64 sparcv9
cd raptor-%{version}-64
export CFLAGS="%optflags64"
export CXXFLAGS="%cxx_optflags64"
export LDFLAGS="%_ldflags64"
export PATH="%{_prefix}/bin/%{_arch64}:%{_prefix}/gnu/bin/%{_arch64}:${PATH}"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --bindir=%{_bindir}/%{_arch64}              \
            --libdir=%{_libdir}/%{_arch64}              \
            --libexecdir=%{_libexecdir}/%{_arch64}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-shared		     \
	    --disable-static                 \
            --with-www=curl                  \
            --with-curl-config=%{_bindir}/%{_arch64}/curl-config

make -j$CPUS 
cd ..
%endif

cd raptor-%{version}
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags"
export PATH="${OPATH}"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --bindir=%{_bindir}              \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-shared                  \
            --disable-static                 \
            --with-www=curl                  \
            --with-curl-config=%{_bindir}/curl-config

make -j$CPUS
cd ..


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd raptor-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.la
cd ..
%endif

cd raptor-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
cd ..


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/rapper
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/rapper
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/raptor-config
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/raptor-config
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

%dir %attr (0755, root, bin) %{_datadir}/gtk-doc
%{_datadir}/gtk-doc/*

%changelog
* Fri May 22 2009 - moinakg@belenix.org
- Initial version
