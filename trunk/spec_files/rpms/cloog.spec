Name:           cloog
Summary:        CLooG is a free software and library to generate code for scanning Z-polyhedra
Version:        0.15.9
URL:            http://www.cloog.org
Source:         ftp://gcc.gnu.org/pub/gcc/infrastructure/cloog-ppl-%{version}.tar.gz
Release:        1%{?dist}
Group:          System Environment/Libraries
License:        GPLv2+
BuildRoot:      %{_tmppath}/cloog-ppl-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: zlib
#Requires: SUNWlibms
Requires: ppl >= 0.10
Requires: gmp >= 4.1.3
Requires: libgcc
BuildRequires: gcc >= 4.4.0
BuildRequires: ppl-devel >= 0.10
BuildRequires: gmp-devel >= 4.1.3

%description
CLooG is a software which generates loops for scanning Z-polyhedra. That is,
CLooG finds the code or pseudo-code where each integral point of one or more
parametrized polyhedron or parametrized polyhedra union is reached. CLooG is
designed to avoid control overhead and to produce a very efficient code.

%package devel
Summary:        Development tools for the ppl based version of Chunky Loop Generator
Group:          Development/Libraries
Requires: %name = %{version}-%{release}
Requires: gcc >= 4.4.0
Requires: ppl-devel >= 0.10
Requires: gmp-devel >= 4.1.3

%description devel
The header files and dynamic shared libraries of the Chunky Loop Generator.

%prep
%setup -q -c -n %name-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

cd cloog-ppl-%{version}
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags"
export CPPFLAGS="-I/usr/include -I/usr/include/gmp"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --bindir=%{_bindir}              \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --infodir=%{_infodir}           \
            --with-pic                       \
            --with-ppl                       \
            --enable-shared                  \
            --disable-static

gmake -j $CPUS
cd ..


%install
rm -rf $RPM_BUILD_ROOT

cd cloog-ppl-%{version}
gmake install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
cd ..

rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir


%clean
rm -rf $RPM_BUILD_ROOT

%post devel
PATH=/usr/bin:/usr/sfw/bin; export PATH
for info in cloog.info
do
  install-info --quiet --info-dir=%{_infodir} %{_infodir}/$info
done

%preun devel
PATH=/usr/bin:/usr/sfw/bin; export PATH
for info in cloog.info
do
  install-info --quiet --info-dir=%{_infodir} --delete %{_infodir}/$info
done

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/cloog
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_infodir}
%{_infodir}/*

%changelog
* Wed May 06 2009 - moinakg@belenix.org
- Initial spec file.
