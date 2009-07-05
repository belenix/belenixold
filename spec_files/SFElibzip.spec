#
# spec file for package SFElibzip
#
# includes module(s): libzip
#
#
%include Solaris.inc
%include base.inc

Name:                    SFElibzip
Summary:                 A library for reading and writing zip archives
Version:                 0.9
URL:                     http://www.nih.at/libzip/index.html
Source:                  http://www.nih.at/libzip/libzip-%{version}.tar.gz

License:                 BSD
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:               SUNWzlib
BuildRequires:          SUNWgnome-common-devel

%description
libzip is a C library for reading, creating, and modifying zip archives. Files
can be added from data buffers, files, or compressed data copied directly from 
other zip archives. Changes made without closing the archive can be reverted. 

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires:          SUNWgnome-common-devel

%prep
%setup -q -c -n %name-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

cd libzip-%{version}
export CFLAGS="%optflags `/usr/bin/getconf LFS_CFLAGS`"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --bindir=%{_bindir}                  \
            --libdir=%{_libdir}                  \
            --enable-shared		                 \
            --disable-static

make -j$CPUS
cd ..


%install
rm -rf $RPM_BUILD_ROOT

cd libzip-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Sun Jul 05 2009 - moinakg<at>gmail(dot)com
- Add largefile support flags.
* Tue Jun 23 2009 - Moinak Ghosh <moinakg@belenix(dot)org>
- Initial version
