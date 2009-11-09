#
# spec file for package SFEpovray
#
# includes module(s): povray
#
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc


Name:                    SFEpovray
Summary:                 Freeware multi-platform ray-tracing package
Version:                 2.03
URL:                     http://www.oberhumer.com/opensource/povray/
Source:                  http://www.oberhumer.com/opensource/povray/download/povray-%{version}.tar.gz
Patch1:                  povray-01-Makefile.diff

SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
License:                 GPLv2
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEgccruntime
BuildRequires: SFEgcc

%description
LZO is a data compression library which is suitable for data
de-/compression in real-time. This means it favours speed over
compression ratio.

LZO is written in ANSI C. Both the source code and the compressed
data format are designed to be portable across platforms.


%package devel
Summary:                 Development files for the povray package.
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SFEgcc

%prep
%setup -q -c -n %name-%version
cd povray-%{version}
%patch1 -p1
cd ..

%ifarch amd64 sparcv9
cp -rp povray-%{version} povray-%{version}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

%ifarch amd64 sparcv9
cd povray-%{version}-64
export CFLAGS="%optflags64"
export CXXFLAGS="%cxx_optflags64"
export LDFLAGS="%_ldflags64"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --bindir=%{_bindir}/%{_arch64}              \
            --libdir=%{_libdir}/%{_arch64}              \
            --libexecdir=%{_libexecdir}/%{_arch64}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-shared		     \
	    --disable-static

make -j$CPUS 
cd ..
%endif

cd povray-%{version}
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --bindir=%{_bindir}              \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-shared                  \
            --disable-static

make -j$CPUS
cd ..


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd povray-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.la
cd ..
%endif

cd povray-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
cd ..



%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Mon May 8 2006 - drdoug007@yahoo.com.au
- Initial version
