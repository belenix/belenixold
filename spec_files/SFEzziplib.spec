#
# spec file for package SFEzziplib.spec
#
# includes module(s): zziplib
#
%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%endif
%include base.inc

%define src_name	zziplib

Name:                   SFEzziplib
Summary:                Lightweight library to easily extract data from zip files 
Version:                0.13.58
Source:                 %{sf_download}/%{src_name}/%{src_name}-%{version}.tar.bz2
Patch1:			zziplib-01-ldflags.diff
Patch2:			zziplib-02-export-inline.diff
Patch3:                 zziplib-03-multilib.diff

SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEsdl
BuildRequires: SFEsdl-devel
Requires: SUNWzlib
Requires: SUNWzlib

%description
The zziplib library is intentionally lightweight, it offers the ability to
easily extract data from files archived in a single zip file. Applications
can bundle files into a single zip archive and access them. The implementation
is based only on the (free) subset of compression with the zlib algorithm
which is actually used by the zip/unzip tools. 

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
%setup -q -c -n %name-%version
cd %{src_name}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
cp zzip/_config.h ../_config.h
cd .. 

%ifarch amd64 sparcv9
cp -rp %{src_name}-%{version} %{src_name}-%{version}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

%ifarch amd64 sparcv9
cd %{src_name}-%{version}-64

libtoolize --force --copy
aclocal-1.10 -I m4
automake-1.10 -a
autoconf --force
export CFLAGS="%optflags64"
export LDFLAGS="%_ldflags64"
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}/%{_arch64}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}/%{_arch64}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir}/%{_arch64} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared		\
	    --disable-static
make -j$CPUS 
cd ..
%endif

cd %{src_name}-%{version}
libtoolize --force --copy
aclocal-1.10 -I m4
automake-1.10 -a
autoconf --force
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix}         \
            --bindir=%{_bindir}         \
            --mandir=%{_mandir}         \
            --libdir=%{_libdir}         \
            --datadir=%{_datadir}       \
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared             \
            --disable-static
make -j$CPUS
cd ..

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
cd ..

# Overwrite the platform specific _config.h with our own modified common one
rm -f $RPM_BUILD_ROOT%{_includedir}/zzip/_config.h
ginstall -p -m 0644 _config.h $RPM_BUILD_ROOT%{_includedir}/zzip/_config.h 


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/*.so*
%dir %attr (0755,root,sys) %{_datadir}
%{_mandir}

%ifarch amd64 sparcv9
%dir %attr (0755,root,bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/*.so*
%endif

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755,root,other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755,root,sys) %{_datadir}
%dir %attr (0755,root,other) %{_datadir}/aclocal
%{_datadir}/aclocal/*

%ifarch amd64 sparcv9
%dir %attr (0755,root,other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%changelog
* Mon Nov 30 2009 - Moinak Ghosh
- Initial version
