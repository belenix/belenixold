#
# spec file for package SFEeet
#
# includes module(s): Eet
#

%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

Name:                    SFEeet
Summary:                 Library for speedy data storage, retrieval, and compression
Version:                 1.1.0
URL:                     http://web.enlightenment.org/p.php?p=about/efl/eet
Source:                  http://download.enlightenment.org/snapshots/2008-09-25/eet-%{version}.tar.bz2
%define tarball_dir eet-%{version}

License:                 GPLv2+
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:                SUNWjpg
Requires:                SUNWzlib
BuildRequires:           SUNWjpg-devel
BuildRequires:           SUNWzlib
BuildRequires:           SUNWgnome-common-devel

%description
Eet is a tiny library designed to write an arbitary set of chunks of
data to a file and optionally compress each chunk (very much like a
zip file) and allow fast random-access reading of the file later
on. It does not do zip as a zip itself has more complexity than is
needed, and it was much simpler to implement this once here.

It also can encode and decode data structures in memory, as well as
image data for saving to eet files or sending across the network to
other machines, or just writing to arbitary files on the system. All
data is encoded in a platform independent way and can be written and
read by any architecture.

%package                 devel
Summary:                 Development files for %{name}
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%prep
%if %cc_is_gcc
%else
%error "This SPEC should be built with Gcc. Please set CC and CXX env variables"
%endif

%setup -q -c -n %name-%version
cd %{tarball_dir}
cd ..

%ifarch amd64 sparcv9
cp -rp %{tarball_dir} %{tarball_dir}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

%ifarch amd64 sparcv9
cd %{tarball_dir}-64

export CFLAGS="%optflags64"
export CPPFLAGS="%optflags64"
export LDFLAGS="%_ldflags64 -L/usr/lib/%{_arch64} -R/usr/lib/%{_arch64} %{gnu_lib_path64}"

./configure \
        --prefix=%{_prefix} \
        --bindir=%{_bindir}/%{_arch64} \
        --sbindir=%{_sbindir}/%{_arch64} \
        --libdir=%{_libdir}/%{_arch64} \
        --libexecdir=%{_libexecdir}/%{_arch64} \
        --localstatedir=%{_localstatedir} \
        --enable-shared --disable-static

make -j $CPUS
cd ..
%endif

cd %{tarball_dir}
accel=x86
export CFLAGS="%optflags"
export CPPFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure \
        --prefix=%{_prefix} \
        --bindir=%{_bindir} \
        --sbindir=%{_sbindir} \
        --libdir=%{_libdir} \
        --libexecdir=%{_libexecdir} \
        --localstatedir=%{_localstatedir} \
        --enable-shared --disable-static 

make -j $CPUS
cd ..

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd %{tarball_dir}-64
make install DESTDIR=${RPM_BUILD_ROOT}
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/lib*.a
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.la
cd ..
%endif

cd %{tarball_dir}
make install DESTDIR=${RPM_BUILD_ROOT}
rm -f ${RPM_BUILD_ROOT}%{_libdir}/lib*.a
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/eet
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libeet*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/{%_arch64}/eet
%dir %attr (0755, root, bin) %{_libdir}/%_arch64
%{_libdir}/%_arch64/libeet*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/eet.pc

%ifarch amd64 sparcv9
%dir %attr (0755, root, other) %{_libdir}/%_arch64/pkgconfig
%{_libdir}/%_arch64/pkgconfig/eet.pc
%endif

%changelog
* Mon Jun 15 2009 - moinakg@belenix(dot)org
- Initial version.
