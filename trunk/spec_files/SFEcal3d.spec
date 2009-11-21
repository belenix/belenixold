#
# spec file for package SFEcal3d.spec
#
# includes module(s): cal3d
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

%define src_name	cal3d
%define src_url		http://download.gna.org/cal3d/sources

Name:                   SFEcal3d
Summary:                skeletal based 3D character animation library
Version:                0.11.0
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
Patch1:                 cal3d-01-gcc43.diff

SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWgnome-doc-utils

%description
Cal3D is a skeletal based 3-D character animation library written in C++
in a platform-/graphic API-independent way. 

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: SUNWgnome-doc-utils

%description devel
This package contains the header files, libraries and documentation
for Cal3D.

%prep
%setup -q -c -n %name-%version
cd %{src_name}-%{version}
%patch1 -p0
cd ..

%ifarch amd64 sparcv9
cp -pr %{src_name}-%{version} %{src_name}-%{version}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

%ifarch amd64 sparcv9
cd %{src_name}-%{version}-64

export CXXFLAGS="-m64 -O3 -Xlinker -i -fno-omit-frame-pointer"
export CFLAGS="%optflags64"
export LDFLAGS="%_ldflags64 -L%{_prefix}/lib/%{_arch64} -R%{_prefix}/lib/%{_arch64} %{gnu_lib_path64}"

./configure --prefix=%{_prefix}         \
            --bindir=%{_bindir}/%{_arch64}         \
            --mandir=%{_mandir}         \
            --libdir=%{_libdir}/%{_arch64}         \
            --datadir=%{_datadir}       \
            --libexecdir=%{_libexecdir}/%{_arch64} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared             \
            --disable-static
gmake -j$CPUS
cd ..
%endif

cd %{src_name}-%{version}
export CXXFLAGS="-O3 -Xlinker -i -fno-omit-frame-pointer"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared		\
	    --disable-static
gmake -j$CPUS 
cd docs
gmake doc-api
cd ../..

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
cd %{src_name}-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/lib*.*a
cd ..
%endif

cd %{src_name}-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/lib*.*a

mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{src_name}
cp -rp docs/api/html $RPM_BUILD_ROOT%{_docdir}/%{src_name}
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755,root,sys) %{_datadir}
%{_mandir}

%ifarch amd64 sparcv9
%dir %attr (0755,root,bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755,root,bin) %{_libdir}
%dir %attr (0755,root,other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755,root,sys) %{_datadir}
%dir %attr (0755,root,other) %{_docdir}
%{_docdir}/*

%ifarch amd64 sparcv9
%dir %attr (0755,root,bin) %{_libdir}/%{_arch64}
%dir %attr (0755,root,other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%changelog
* Sat Nov 21 2009 - Moinak Ghosh
- Initial version.
