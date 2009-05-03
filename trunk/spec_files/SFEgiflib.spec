#
# spec file for package SFEgiflib
#
# includes module(s): Giflib
#

%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

Name:                    SFEgiflib
Summary:                 A GIF decoding library
Version:                 4.1.6
URL:                     http://sourceforge.net/projects/giflib
Source:                  %{sf_download}/giflib/giflib-%{version}.tar.bz2

License:                 GPL2
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -c -n %name-%version

%ifarch amd64 sparcv9
cp -rp giflib-%{version} giflib-%{version}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

%ifarch amd64 sparcv9
cd giflib-%{version}-64

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
        --with-x --x-includes=/usr/X11/include --x-libraries=/usr/X11/lib/%{_arch64} \
        --enable-shared --disable-static --with-pic

make -j $CPUS
cd ..
%endif

cd giflib-%{version}
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
        --with-x --x-includes=/usr/X11/include --x-libraries=/usr/X11/lib \
        --enable-shared --disable-static --with-pic

make -j $CPUS
cd ..

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd giflib-%{version}-64
make install DESTDIR=${RPM_BUILD_ROOT}
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/lib*.a
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.la
cd ..
%endif

cd giflib-%{version}
make install DESTDIR=${RPM_BUILD_ROOT}
rm -f ${RPM_BUILD_ROOT}%{_libdir}/lib*.a
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/gif*
%{_bindir}/*gif
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%_arch64
%{_bindir}/%_arch64/gif*
%{_bindir}/%_arch64/*gif
%dir %attr (0755, root, bin) %{_libdir}/%_arch64
%{_libdir}/%_arch64/lib*.so*
%endif

%changelog
* Sun May 03 2009 - moinakg@belenix.org
- Initial spec file
