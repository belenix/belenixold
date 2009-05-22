#
# spec file for package SFErasqal
#
# includes module(s): rasqal
#
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc


Name:                    SFErasqal
Summary:                 A free software / Open Source C library that handles Resource Description Framework (RDF) query syntaxes.
Version:                 0.9.16
URL:                     http://librdf.org/rasqal/
Source:                  http://download.librdf.org/source/rasqal-%{version}.tar.gz

SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
License:                 LGPL
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEraptor
Requires: SFEbdb
Requires: SUNWpcre
Requires: SUNWsqlite3
Requires: SFEgmp
Requires: SFEmpfr
BuildRequires: SFEraptor-devel
BuildRequires: SUNWpcre
BuildRequires: SFEgmp-devel
BuildRequires: SFEmpfr-devel
BuildRequires: SUNWgtk-doc
BuildRequires: SFEbdb-devel
BuildRequires: SUNWsqlite3-devel

%description
Rasqal is a free software / Open Source C library that handles
Resource Description Framework (RDF) query syntaxes, query
construction and query execution returning result bindings.
The supported query languages are SPARQL and RDQL.

Rasqal was designed to work closely with the Redland RDF library
but is entirely separate. It is intended to be a portable library
working across many POSIX systems (Unix, GNU/Linux, BSDs, OSX,
cygwin) win32 and others. 

This is a beta quality library - the code is mature but the API
is still changing and the SPARQL support is under active
development.


%package devel
Summary:                 Development files for the rasqal package.
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SFEgcc
Requires: SUNWlxml-devel
Requires: SUNWlxsl-devel

%package doc
Summary:                 Documentation files for the rasqal package.
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name


%prep
%setup -q -c -n %name-%version
%ifarch amd64 sparcv9
cp -rp rasqal-%{version} rasqal-%{version}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
OPATH=${PATH}
export CPPFLAGS="-I%{_includedir}/gmp -I%{_includedir}/mpfr"

%ifarch amd64 sparcv9
cd rasqal-%{version}-64
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
            --with-pic                       \
            --with-pcre-config=%{_prefix}/bin/%{_arch64}/pcre-config \
            --with-xml2-config=%{_prefix}/bin/%{_arch64}/xml2-config \
            --enable-gtk-doc \
            --with-html-dir=%{_docdir}

make -j$CPUS 
cd ..
%endif

cd rasqal-%{version}
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
            --with-pic                       \
            --with-pcre-config=%{_prefix}/bin/pcre-config \
            --with-xml2-config=%{_prefix}/bin/xml2-config \
            --enable-gtk-doc \
            --with-html-dir=%{_docdir}

make -j$CPUS
cd ..


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd rasqal-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.la
cd ..
%endif

cd rasqal-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
cd ..


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/roqet
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/roqet
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/rasqal-config
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/rasqal-config
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
* Fri May 22 2009 - moinakg@belenix.org
- Initial version
