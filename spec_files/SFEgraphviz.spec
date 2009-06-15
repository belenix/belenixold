#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

%define SFEfreetype %(/usr/bin/pkginfo -q SFEfreetype && echo 1 || echo 0)
%define perl_vers 5.8.4
%define ruby_vers 1.8
%define python_vers python2.4
%define tcl_vers tcl8.4

Name:                SFEgraphviz
Summary:             Graph drawing tools and libraries
Version:             2.22.2
Source:              http://www.graphviz.org/pub/graphviz/ARCHIVE/graphviz-%{version}.tar.gz
URL:                 http://www.graphviz.org
SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWlibtool
Requires: SUNWgd2
Requires: SUNWlexpt
Requires: SUNWfontconfig
Requires: SUNWlexpt
%if %{SFEfreetype}
Requires: SFEfreetype
%else
Requires: SUNWfreetype2
%endif
Requires: SUNWgnome-base-libs
Requires: SUNWjpg
%if %cc_is_gcc
Requires: SFEgccruntime
%else
Requires: SUNWlibC
%endif
Requires: SUNWpng
%if %{SFEfreetype}
BuildRequires: SFEfreetype-devel
%else
BuildRequires: SUNWfreetype2
%endif
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWlibtool
BuildRequires: SUNWPython-devel
BuildRequires: SUNWTcl
BuildRequires: SUNWperl584core
BuildRequires: SUNWruby18u
BuildRequires: SFEswig

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%prep
%setup -q -c -n %name-%version
%ifarch amd64 sparcv9
cp -rp graphviz-%{version} graphviz-%{version}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

OPATH="$PATH"

%ifarch amd64 sparcv9
cd graphviz-%{version}-64

export CPPFLAGS="-I%{_prefix}/X11/include -I%{_prefix}/include/gd2 -D_SYS_MODE_H"
export CFLAGS="%optflags64"
export CXXFLAGS="%cxx_optflags64"
export LDFLAGS="%_ldflags64 %{xorg_lib_path64} -lgd"
export PATH="%{_bindir}/%{_arch64}:%{_prefix}/gnu/bin/%{_arch64}:${OPATH}"

#libtoolize --copy --force
#aclocal $ACLOCAL_FLAGS
#autoheader
#automake -a -c -f
#autoconf
#bash ./autogen.sh

# Perl, Ruby are disabled in 64bit build as there is no 64bit perl in default osol
# base.
./configure --prefix=%{_prefix}  \
            --bindir=%{_bindir}/%{_arch64} \
            --libdir=%{_libdir}/%{_arch64} \
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
            --disable-perl \
            --disable-ruby \
            $TCL_OPTS

make -j$CPUS
cd ..
%endif

cd graphviz-%{version}
export CPPFLAGS="-I%{_prefix}/X11/include -I%{_prefix}/include/gd2 -D_SYS_MODE_H"
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags %{xorg_lib_path} -lgd"
export PATH="$OPATH"

#libtoolize --copy --force
#aclocal $ACLOCAL_FLAGS
#autoheader
#automake -a -c -f
#autoconf
#bash ./autogen.sh
./configure --prefix=%{_prefix}  \
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
            $TCL_OPTS

make -j$CPUS
cd ..


%install
rm -rf $RPM_BUILD_ROOT
OPATH="$PATH"

%ifarch amd64 sparcv9
cd graphviz-%{version}-64
export PATH="%{_bindir}/%{_arch64}:%{_prefix}/gnu/bin/%{_arch64}:${OPATH}"

make install DESTDIR=$RPM_BUILD_ROOT
cd ..
%endif

cd graphviz-%{version}
export PATH="$OPATH"
make install DESTDIR=$RPM_BUILD_ROOT
cd ..

find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

rm -rf ${RPM_BUILD_ROOT}%{_mandir}/mann

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_bindir}/dot -c

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, bin) %{_libdir}/graphviz
%{_libdir}/graphviz/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}/graphviz
%{_libdir}/%{_arch64}/graphviz/*
%endif

%dir %attr (0755, root, bin) %{_prefix}/perl5
%dir %attr (0755, root, bin) %{_prefix}/perl5/vendor_perl
%dir %attr (0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_vers}
%dir %attr (0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_vers}/i86pc-solaris-64int
%{_prefix}/perl5/vendor_perl/%{perl_vers}/i86pc-solaris-64int/*
%dir %attr (0755, root, bin) %{_prefix}/ruby
%dir %attr (0755, root, bin) %{_prefix}/ruby/%{ruby_vers}
%dir %attr (0755, root, bin) %{_prefix}/ruby/%{ruby_vers}/lib
%dir %attr (0755, root, bin) %{_prefix}/ruby/%{ruby_vers}/lib/ruby
%dir %attr (0755, root, bin) %{_prefix}/ruby/%{ruby_vers}/lib/ruby/site_ruby
%dir %attr (0755, root, bin) %{_prefix}/ruby/%{ruby_vers}/lib/ruby/site_ruby/%{ruby_vers}
%dir %attr (0755, root, bin) %{_prefix}/ruby/%{ruby_vers}/lib/ruby/site_ruby/%{ruby_vers}/i386-solaris2.11
%{_prefix}/ruby/%{ruby_vers}/lib/ruby/site_ruby/%{ruby_vers}/i386-solaris2.11/*
%dir %attr (0755, root, bin) %{_libdir}/%{python_vers}
%dir %attr (0755, root, bin) %{_libdir}/%{python_vers}/site-packages
%{_libdir}/%{python_vers}/site-packages/*
%dir %attr (0755, root, bin) %{_libdir}/%{tcl_vers}
%{_libdir}/%{tcl_vers}/*

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*.1
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*.3*
%dir %attr (0755, root, bin) %{_mandir}/man7
%{_mandir}/man7/*.7

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/graphviz
%{_datadir}/graphviz/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%changelog
* Mon Jun 15 2009 - moinakg@belenix(dot)org
- Add 64Bit build.
* Sat Jun 21 2008 - moinakg@gmail.com
- Fix build
- Add entries for Perl, Tcl and Python plugins.
* Mon Apr 28 2008 - <shivakumar dot gn at gmail dot com>
- Fixed usage of macro in if condition
* Thu Jan 24 2008 - nonsea@users.sourceforge.net
- Replace SFEruby to SUNWruby18u
* Wed Jan 17 2008 - moinak.ghosh@sun.com
- Do not disable perl.
- Prevent sys/mode.h from being pulled in via perl.h by defining _SYS_MODE_H. This
- allows the perl plugin to be built.
* Wed Jan 16 2008 - moinak.ghosh@sun.com
- Bump version to 2.16.1
- Remove SUNWfontconfig-devel from BuildRequires. SUNWfontconfig package includes
- devel components.
- Changed SFElibtool dep to SUNWlibtool.
- Remove unneeded patches.
* Thu Oct 25 2007 - nonsea@users.sourceforge.net
- Add configure option --disale-perl 
- Add patch gd-ldflags.diff
- Add /usr/include/gd2 to CFLAGS
* Wed Oct 17 2007 - laca@sun.com
- add /usr/X11 to search paths for FOX
- allow building with either SUNWlexpt or SFEexpat
* Mon Sep 24 2007 - trisk@acm.jhu.edu
- Allow building with Tcl 8.4 (newer SUNWTcl)
* Thu Mar 22 2007 - nonsea@users.sourceforge.net
- Add patch arith-h to export arith.h to let anjuta build pass.
  This patch is already in cvs head, should be removed in next release.
* Fri Aug 17 2007 - trisk@acm.jhu.edu
- Bump to 2.14
- Update dependencies, disable optional plugins
* Thu Mar 22 2007 - nonsea@users.sourceforge.net
- Add patch tclsh.diff and ruby-lib.diff to build pass.
- Add Requires/BuildRequries after check-deps.pl run.
* Wed Mar 07 2007 - daymobrew@users.sourceforge.net
- Bump to 2.12. Delete more *.la files in %install. Add URL field.
* Tue Nov 07 2006 - Eric Boutilier
- Initial spec
