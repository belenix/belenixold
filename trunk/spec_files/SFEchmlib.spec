#
# spec file for package SFEchmlib
#
# includes module(s): Chmlib
#

%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

Name:                    SFEchmlib
Summary:                 A library for dealing with Microsoft ITSS/CHM format files
Version:                 0.39
URL:                     http://www.jedrea.com/chmlib/
Source:                  http://www.jedrea.com/chmlib/chmlib-%{version}.tar.bz2

License:                 LGPL
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          LICENSE.LGPL
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -c -n %name-%version

%ifarch amd64 sparcv9
cp -rp chmlib-%{version} chmlib-%{version}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

%ifarch amd64 sparcv9
cd chmlib-%{version}-64

export CFLAGS="%optflags64"
export CPPFLAGS="%optflags64"
export LDFLAGS="%_ldflags64"

./configure --prefix=%{_prefix} \
        --bindir=%{_bindir}/%{_arch64} \
        --datadir=%{_datadir} \
        --includedir=%{_includedir} \
        --infodir=%{_infodir} \
        --libdir=%{_libdir}/%{_arch64} \
        --libexecdir=%{_libexecdir}/%{_arch64} \
        --mandir=%{_mandir} \
        --sbindir=%{_sbindir}/%{_arch64} \
        --sysconfdir=%{_sysconfdir} \
        --enable-shared --disable-static --with-pic

make -j $CPUS
cd ..
%endif

cd chmlib-%{version}
export CFLAGS="%optflags"
export CPPFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix} \
        --bindir=%{_bindir} \
        --datadir=%{_datadir} \
        --includedir=%{_includedir} \
        --infodir=%{_infodir} \
        --libdir=%{_libdir} \
        --libexecdir=%{_libexecdir} \
        --mandir=%{_mandir} \
        --sbindir=%{_sbindir} \
        --sysconfdir=%{_sysconfdir} \
        --enable-shared --disable-static --with-pic

make -j $CPUS
cd ..

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd chmlib-%{version}-64
make install DESTDIR=${RPM_BUILD_ROOT}
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/lib*.a
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.la
rm -rf ${RPM_BUILD_ROOT}%{_bindir}
cd ..
%endif

cd chmlib-%{version}
make install DESTDIR=${RPM_BUILD_ROOT}
rm -f ${RPM_BUILD_ROOT}%{_libdir}/lib*.a
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
rm -rf ${RPM_BUILD_ROOT}%{_bindir}
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%_arch64
%{_libdir}/%_arch64/lib*.so*
%endif

%changelog
* Sun May 03 2009 - moinakg@belenix.org
- Initial spec file
