#
# spec file for package SFEopenbabel
#
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc
%define python_version   2.6
Name:			SFEopenbabel
License:		GPLv2
Group:			Applications/File
Version:		2.2.2
Summary:		Chemistry software file format converter
Source:			%{sf_download}/openbabel/openbabel-%{version}.tar.gz
Patch1:                 openbabel-01-vector3_isfinite.diff
Patch2:                 openbabel-02-sysmode_vnode.diff

URL:			http://openbabel.org/wiki/Main_Page
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:		%{_prefix}
Requires:      SFEinchi
Requires:      SUNWlxml
Requires:      SUNWperl584usr
Requires:      SUNWPython26
Requires:      SUNWruby18u
Requires:      SUNWzlib
Requires:      SFEinchi
BuildRequires: SFEinchi-devel
BuildRequires: SUNWlxml-devel
BuildRequires: SUNWPython26-devel
BuildRequires: SFEswig
BuildRequires: SFEinchi-devel

%description
Open Babel is a free, open-source version of the Babel chemistry file
translation program. Open Babel is a project designed to pick up where
Babel left off, as a cross-platform program and library designed to
interconvert between many file formats used in molecular modeling,
computational chemistry, and many related areas.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
Requires: SFEinchi-devel
Requires: SUNWlxml-devel
Requires: SUNWPython26-devel
Requires: SFEswig
Requires: SUNWzlib
Requires: SUNWruby18u
Requires: SUNWperl584usr

%package python
Summary:                 %{summary} - Python bindings
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%prep
%setup -q -c -n %name-%version
cd openbabel-%{version}
%patch1 -p1
%patch2 -p1
cd ..

%ifarch amd64 sparcv9
cp -pr openbabel-%{version} openbabel-%{version}-64
%endif

%build
ln -sf ${CC} cc
export PATH=`pwd`:${PATH}
OPATH="$PATH"

%ifarch amd64 sparcv9
cd openbabel-%{version}-64
export CFLAGS="%optflags64 -D__C99FEATURES__"
export CXXFLAGS="%cxx_optflags64 -D__C99FEATURES__"
export LDFLAGS="%_ldflags64"
export PYTHON="%{_bindir}/%{_arch64}/python%{python_version}"
export PATH="%{_bindir}/%{_arch64}:%{_prefix}/gnu/bin/%{_arch64}:${PATH}"

./configure \
    --prefix=%{_prefix} \
    --bindir=%{_bindir}/%{_arch64} \
    --libdir=%{_libdir}/%{_arch64} \
    --enable-shared=yes \
    --enable-static=no \
    --with-pic \
    --mandir=%{_mandir} \
    --infodir=%{_infodir}

make -j 2

(cd scripts/python
 ${PYTHON} setup.py build
)

cd ..
%endif

cd openbabel-%{version}
SRCDIR=`pwd`
export CFLAGS="%optflags -D__C99FEATURES__"
export CXXFLAGS="%cxx_optflags -D__C99FEATURES__"
export LDFLAGS="%_ldflags"
export PYTHON="%{_bindir}/python%{python_version}"
export PATH="${OPATH}"

./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --enable-shared=yes \
    --enable-static=no \
    --with-pic \
    --mandir=%{_mandir} \
    --infodir=%{_infodir}

make -j 2

#
# Re-attempt fixing Perl build in future. Just too many issues
# now.
#
#(cd scripts/perl
# export LD_LIBRARY_PATH=${SRCDIR}/src/.libs:%{_libdir}:%{_prefix}/gnu/lib
# perl Makefile.PL INSTALLDIRS="vendor"
# cp Makefile Makefile.orig
# cat Makefile.orig | sed '{
#   s#-KPIC#-fPIC -DPIC#
#   s#-G#-shared#
#   s#-xO3#-O3#
#   s#-xspace##
#   s#-xildoff##
# }' > Makefile
#
# make -j 2
#)

(cd scripts/python
 ${PYTHON} setup.py build
)


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd openbabel-%{version}-64
export PYTHON="%{_bindir}/%{_arch64}/python%{python_version}"

make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/lib*a
(cd scripts/python
 ${PYTHON} setup.py install --skip-build --root $RPM_BUILD_ROOT
 ${PYTHON} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
)
cd ..
%endif

cd openbabel-%{version}
export PYTHON="%{_bindir}/python%{python_version}"

make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a
(cd scripts/python
 ${PYTHON} setup.py install --skip-build --root $RPM_BUILD_ROOT
 ${PYTHON} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
)
mv $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages \
   $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages

mkdir -p $RPM_BUILD_ROOT%{_docdir}/openbabel/%{version}
cp doc/*.html $RPM_BUILD_ROOT%{_docdir}/openbabel/%{version}
cp doc/*.inc $RPM_BUILD_ROOT%{_docdir}/openbabel/%{version}
cp doc/README* $RPM_BUILD_ROOT%{_docdir}/openbabel/%{version}
cp doc/dioxin* $RPM_BUILD_ROOT%{_docdir}/openbabel/%{version}
cp COPYING $RPM_BUILD_ROOT%{_docdir}/openbabel/%{version}
cp README $RPM_BUILD_ROOT%{_docdir}/openbabel/%{version}

find $RPM_BUILD_ROOT -name _openbabel.so | xargs chmod 0755
find $RPM_BUILD_ROOT -name "*.la" | xargs rm
cd ..


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, other) %{_docdir}
%doc %{_docdir}/openbabel/%{version}/*
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, bin) %{_libdir}/openbabel
%{_libdir}/openbabel/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*
%dir %attr (0755, root, bin) %{_datadir}/openbabel
%{_datadir}/openbabel/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}/openbabel
%{_libdir}/%{_arch64}/openbabel/*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%files python
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}/vendor-packages
%{_libdir}/python%{python_version}/vendor-packages/*


%changelog
* Thu Jul 16 2009 - moinakg(at)belenix<dot>org
- Initial spec.
