#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc
%define sunw_gnu_iconv %(pkginfo -q SUNWgnu-libiconv && echo 1 || echo 0)

Name:                SFEwv2
License:             GPL
Summary:             A library that allows access to Microsoft Word files (series 2)
Version:             0.4.0
URL:                 http://wvware.sourceforge.net/
Source:              %{sf_download}/wvware/wv2-%{version}.tar.bz2
Patch1:              wv2-01-ustring.cpp.diff

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:            SUNWgnome-base-libs
Requires:            SUNWlxml
Requires:            SUNWzlib
Requires:            SUNWlibmsr
Requires:            SUNWbzip
Requires:            SUNWcslr
Requires:            SFElibgsf
BuildRequires:       SUNWgnome-base-libs-devel
BuildRequires:       SUNWlxml-devel
BuildRequires:       SFElibgsf-devel
%if %sunw_gnu_iconv
Requires: SUNWgnu-libiconv
Requires: SUNWgnu-gettext
%else
Requires: SFElibiconv
Requires: SFEgettext
%endif

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%prep
%setup -q -n wv2-%version
%patch1 -p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags -I%{gnu_inc} -D__C99FEATURES__"
export CXXFLAGS="%cxx_optflags -I%{gnu_inc}"
export LDFLAGS="%_ldflags %{gnu_lib_path}"
gnu_prefix=`dirname %{gnu_bin}`

export CMAKE_LIBRARY_PATH="%{xorg_lib}:%{gnu_lib}:%{_prefix}/lib:/lib:%{sfw_lib}"

cmake   . -DCMAKE_INSTALL_PREFIX=%{_prefix}      \
        -DCMAKE_BUILD_TYPE=Release                                      \
        -DCMAKE_C_COMPILER:FILEPATH=${CC}                               \
        -DCMAKE_C_FLAGS:STRING="${CFLAGS}"                              \
        -DCMAKE_CXX_COMPILER:FILEPATH=${CXX}                            \
        -DCMAKE_CXX_FLAGS_RELEASE:STRING="${CXXFLAGS}"                  \
        -DCMAKE_INCLUDE_PATH="%{gnu_inc}"                               \
        -DCMAKE_SKIP_RPATH:BOOL=YES                                     \
        -DINCLUDE_INSTALL_DIR=%{_includedir}                            \
        -DSYSCONF_INSTALL_DIR=%{_sysconfdir}                            \
        -DICONV_INCLUDE_DIR=%{gnu_inc}					\
        -DICONV_LIBRARIES=%{gnu_lib}					\
        -DBUILD_SHARED_LIBS=On                                          \
        -DCMAKE_VERBOSE_MAKEFILE=1 > config.log 2>&1

make VERBOSE=1 -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

cp $RPM_BUILD_ROOT/usr/bin/wv2-config $RPM_BUILD_ROOT/usr/bin/wv2-config.orig
cat $RPM_BUILD_ROOT/usr/bin/wv2-config.orig | sed '{
    s#\-l/usr/gnu/lib#\-L/usr/gnu/lib \-R/usr/gnu/lib#
}' > $RPM_BUILD_ROOT/usr/bin/wv2-config
rm -f $RPM_BUILD_ROOT/usr/bin/wv2-config.orig

find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, bin) %{_libdir}/wvWare
%{_libdir}/wvWare/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Mon Sep 28 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Bump version, changes to build with cmake and fix config file.
* Fri Sep 18 2009 - moinakg(at)belenix<dot>org
- Remove commented patch lines.
* Sat Jan 26 2008 - moinak.ghosh@sun.com
- Initial spec.
