#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#

%include Solaris.inc
%define cc_is_gcc 1
%include usr-gnu.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

Name:                SFEexiv2
License:             GPL
Summary:             A C++ library and CLI utility to manage image metadata.
Version:             0.18.1
URL:                 http://www.exiv2.org/
Source:              http://www.exiv2.org/exiv2-%{version}.tar.gz
Patch1:              exiv2-01-makefile.diff
Patch2:              exiv2-02-deps.patch
Patch3:              exiv2-03-visibility.patch

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWzlib
Requires: SUNWTiff
BuildRequires: SUNWTiff-devel
Requires: SUNWpng
BuildRequires: SUNWpng-devel
Requires: SUNWjpg
BuildRequires: SUNWjpg-devel
Requires: SUNWgnome-libs
BuildRequires: SUNWgnome-libs-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -c -n %name-%version
cd exiv2-%{version}
%patch2 -p1
%patch3 -p1
cd ..

%ifarch amd64 sparcv9
cp -rp exiv2-%{version} exiv2-%{version}-64
%endif


%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=/usr/gnu/bin/gcc
export CXX=/usr/gnu/bin/g++

%ifarch amd64 sparcv9
cd exiv2-%{version}-64

export CFLAGS="%optflags64 -fPIC -I%{xorg_inc} -I%{gnu_inc} -D__C99FEATURES__ -D__EXTENSIONS__"
export CXXFLAGS="%cxx_optflags64 -I%{xorg_inc} -I%{gnu_inc} -D__C99FEATURES__ -D__EXTENSIONS__"
export LDFLAGS="%_ldflags64 %{gnu_lib_path64} %{xorg_lib_path64}"

extra_inc="%{xorg_inc}:%{gnu_inc}"

./configure --prefix=%{_prefix} \
            --mandir=%{_mandir} \
            --bindir=%{_bindir}/%{_arch64} \
            --libdir=%{_libdir}/%{_arch64} \
            --enable-shared=yes \
            --enable-static=no  \
            --enable-final      \
            --with-extra-includes="${extra_inc}"

# Fix makefiles as they assume /bin/sh is bash UGH
for mk in `find . -name Makefile`
do
        [ ! -f ${mk}.orig ] && cp ${mk} ${mk}.orig
        cat $mk | sed 's/SHELL = \/bin\/sh/SHELL = \/bin\/bash/' > ${mk}.new
        mv ${mk}.new ${mk}
done
(cd src; cat %{PATCH1} | gpatch -p0)

gmake
cd ..
%endif

cd exiv2-%{version}
export CFLAGS="%optflags -fPIC -I%{xorg_inc} -I%{gnu_inc} -D__C99FEATURES__ -D__EXTENSIONS__"
export CXXFLAGS="%cxx_optflags -I%{xorg_inc} -I%{gnu_inc} -D__C99FEATURES__ -D__EXTENSIONS__"
export LDFLAGS="%_ldflags %{gnu_lib_path} %{xorg_lib_path}"

extra_inc="%{xorg_inc}:%{gnu_inc}"

./configure --prefix=%{_prefix}	\
            --mandir=%{_mandir}	\
	    --libdir=%{_libdir} \
            --enable-shared=yes \
            --enable-static=no  \
            --enable-final	\
            --with-extra-includes="${extra_inc}"

# Fix makefiles as they assume /bin/sh is bash UGH
for mk in `find . -name Makefile`
do
	[ ! -f ${mk}.orig ] && cp ${mk} ${mk}.orig
	cat $mk | sed 's/SHELL = \/bin\/sh/SHELL = \/bin\/bash/' > ${mk}.new
	mv ${mk}.new ${mk}
done
(cd src; cat %{PATCH1} | gpatch -p0)

gmake
cd ..


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd exiv2-%{version}-64
gmake install DESTDIR=$RPM_BUILD_ROOT
%if %build_l10n
%else
rm -rf $RPM_BUILD_ROOT%{_localedir}
%endif
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.la
cd ..
%endif

cd exiv2-%{version}
gmake install DESTDIR=$RPM_BUILD_ROOT
%if %build_l10n
%else
rm -rf $RPM_BUILD_ROOT%{_localedir}
%endif
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
cd ..


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_basedir}/gnu
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/exiv2
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/exiv2
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_basedir}/gnu
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%if %build_l10n
%files l10n
%defattr (-, root, other)
%dir %attr (0755, root, bin) %{_basedir}/gnu
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/locale
%{_datadir}/locale/*
%endif

%changelog
* Fri May 29 2009 - Moinak Ghosh <moinakg@belenix(dot)org>
- Added 64Bit build.
- Bump version to 0.18.1.
* Wed Jan 30 2008 - moinak.ghosh@sun.com
- Initial spec.

