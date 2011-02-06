
## *** WORK IN PROGRESS *** ##

%define perl_vers 5.10.0
%define ruby_vers 1.8
%define tcl_v %(echo 'puts $tcl_version' | tclsh)
%define tcl_vers tcl%{tcl_v}

Name:                graphviz
Summary:             Graph drawing tools and libraries
Version:             2.26.3
Release:             1%{?dist}
Group:               Applications/Multimedia
License:             CPL
Source:              http://www.graphviz.org/pub/graphviz/ARCHIVE/graphviz-%{version}.tar.gz
URL:                 http://www.graphviz.org
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

Requires: graphviz-tclpkg
Requires: zlib
#Requires: tcl8
#Requires: SUNWlibtool
#Requires: SUNWgd2
#Requires: SUNWlexpt
#Requires: SUNWfontconfig
#Requires: SUNWlexpt
#Requires: SUNWfreetype2
#Requires: SUNWgnome-base-libs
#Requires: SUNWjpg
#%if %gcc_compiler
#Requires: SFEgccruntime
#%else
#Requires: SUNWlibC
#%endif
#Requires: SUNWpng
BuildRequires: zlib-devel
#BuildRequires: SUNWfreetype2
#BuildRequires: SUNWgnome-base-libs-devel
#BuildRequires: SUNWlibtool
#BuildRequires: SUNWPython-devel
#BuildRequires: SUNWTcl
#BuildRequires: SUNWperl584core
#BuildRequires: SUNWruby18u
#BuildRequires: SFEswig

%description
A collection of tools for the manipulation and layout of graphs (as in nodes 
and edges, not as in barcharts).

%package devel
Summary:             %{summary} - development files
Group:               Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
A collection of tools for the manipulation and layout of graphs (as in nodes 
and edges, not as in barcharts). This package contains development files for 
graphviz.

%package doc
Group:               Documentation
Summary:             PDF and HTML documents for graphviz

%description doc
Provides some additional PDF and HTML documentation for graphviz.

%package python
Group:               Applications/Multimedia
Summary:             Python extension for graphviz
Requires:            %{name} = %{version}-%{release}
#Requires:           python

%description python
Python extension for graphviz.

%if !%{build_64bit}
%package perl
Group:               Applications/Multimedia
Summary:             Perl extension for graphviz
Requires:            %{name} = %{version}-%{release}
#Requires:           perl5

%description perl
Perl extension for graphviz.

%package ruby
Group:               Applications/Multimedia
Summary:             Ruby extension for graphviz
Requires:            %{name} = %{version}-%{release}
#Requires:            ruby18

%description ruby
Ruby extension for graphviz.
%endif

%prep
%bsetup

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

cd graphviz-%{version}
export CPPFLAGS="-I%{_prefix}/X11/include -I%{_prefix}/include/gd2 -D_SYS_MODE_H"
%if %{build_64bit}
export CFLAGS="%optflags %{gcc_opt_sse2} %{gcc_opt_graphite}"
export CXXFLAGS="%cxx_optflags %{gcc_opt_sse2} %{gcc_opt_graphite}"
export LDFLAGS="%_ldflags -lgd"
export PYTHON=%{_bindir}/python
%else
export CFLAGS="%optflags %{gcc_opt_graphite}"
export CXXFLAGS="%cxx_optflags %{gcc_opt_graphite}"
export LDFLAGS="%_ldflags -lgd"
export PYTHON=%{_bindir}/%{pyname}
export PERL=%{_prefix}/perl5/%{perl_vers}/bin/perl
export RUBY=%{_bindir}/ruby
%endif

./configure --prefix=%{_prefix}  \
            --bindir=%{_bindir} \
            --libdir=%{_libdir} \
            --mandir=%{_mandir} \
            --enable-static=no \
            --enable-ltdl \
            --disable-rpath \
            --disable-sharp \
            --disable-guile \
            --disable-io \
            --disable-java \
            --disable-lua \
            --disable-ocaml \
            --disable-php \
%if %{build_64bit}
            --enable-ruby=no \
            --enable-perl=no \
%endif
            --with-tcl=%{_bindir}/tclsh \
            $TCL_OPTS

gmake -j$CPUS
cd ..


%install
rm -rf $RPM_BUILD_ROOT
cd graphviz-%{version}
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

rm -rf ${RPM_BUILD_ROOT}%{_mandir}/mann
mkdir -p ${RPM_BUILD_ROOT}%{_libdir32}/%{pyname}/vendor-packages
mkdir -p ${RPM_BUILD_ROOT}%{_libdir32}/%{pyname}/lib-dynload
mv ${RPM_BUILD_ROOT}%{_libdir32}/%{pyname}/site-packages/*.py* ${RPM_BUILD_ROOT}%{_libdir32}/%{pyname}/vendor-packages

%if %{build_64bit}
mkdir ${RPM_BUILD_ROOT}%{_libdir32}/%{pyname}/lib-dynload/64
mv ${RPM_BUILD_ROOT}%{_libdir32}/%{pyname}/site-packages/*.so ${RPM_BUILD_ROOT}%{_libdir32}/%{pyname}/lib-dynload/64
%else
mv ${RPM_BUILD_ROOT}%{_libdir32}/%{pyname}/site-packages/*.so ${RPM_BUILD_ROOT}%{_libdir32}/%{pyname}/lib-dynload
%endif
rm -rf ${RPM_BUILD_ROOT}%{_libdir32}/%{pyname}/site-packages
rm -rf ${RPM_BUILD_ROOT}%{_libdir32}/%{tcl_vers}

%clean
rm -rf $RPM_BUILD_ROOT

%post
LD_LIBRARY_PATH=${PKG_INSTALL_ROOT}%{_libdir}:${PKG_INSTALL_ROOT}%{_prefix}/gnu/lib
export LD_LIBRARY_PATH
$PKG_INSTALL_ROOT%{_bindir}/dot -c

%files
%defattr (-, root, bin)
%{_bindir}/*
%{_libdir}/lib*.so*
%dir %attr (0755, root, bin) %{_libdir}/graphviz
%{_libdir}/graphviz/*.so*
%dir %attr (0755, root, bin) %{_libdir}/graphviz/tcl
%{_libdir}/graphviz/tcl/*

%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*
%{_mandir}/man7/*.7*

%files devel
%defattr (-, root, bin)
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, other) %{_datadir}/graphviz
%{_datadir}/graphviz/*

%files python
%defattr(-, root, bin)
%dir %{_libdir32}/%{pyname}
%dir %{_libdir32}/%{pyname}/vendor-packages
%dir %{_libdir32}/%{pyname}/lib-dynload
%{_libdir32}/%{pyname}/vendor-packages/*
%{_libdir32}/%{pyname}/lib-dynload/*
%dir %attr (0755, root, bin) %{_libdir}/graphviz/python
%{_libdir}/graphviz/python/*

%if !%{build_64bit}
%files perl
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}/perl5
%dir %attr (0755, root, bin) %{_prefix}/perl5/vendor_perl
%dir %attr (0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_vers}
%dir %attr (0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_vers}/i86pc-solaris-64int
%{_prefix}/perl5/vendor_perl/%{perl_vers}/i86pc-solaris-64int/*
%dir %attr (0755, root, bin) %{_libdir}/graphviz/perl
%{_libdir}/graphviz/perl/*

%files ruby
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}/ruby
%dir %attr (0755, root, bin) %{_prefix}/ruby/%{ruby_vers}
%dir %attr (0755, root, bin) %{_prefix}/ruby/%{ruby_vers}/lib
%dir %attr (0755, root, bin) %{_prefix}/ruby/%{ruby_vers}/lib/ruby
%dir %attr (0755, root, bin) %{_prefix}/ruby/%{ruby_vers}/lib/ruby/site_ruby
%dir %attr (0755, root, bin) %{_prefix}/ruby/%{ruby_vers}/lib/ruby/site_ruby/%{ruby_vers}
%dir %attr (0755, root, bin) %{_prefix}/ruby/%{ruby_vers}/lib/ruby/site_ruby/%{ruby_vers}/i386-solaris2.11
%{_prefix}/ruby/%{ruby_vers}/lib/ruby/site_ruby/%{ruby_vers}/i386-solaris2.11/*
%dir %attr (0755, root, bin) %{_libdir}/graphviz/ruby
%{_libdir}/graphviz/ruby/*
%endif

%changelog
