#
# spec file for package SFElibidn
#
# includes module(s): GNU libidn
#
%include Solaris.inc

%ifarch amd64
%include arch64.inc
%endif

%include base.inc

Name:                SFEidnkit
Summary:             Internationalized Domain Name library
Version:             1.0
URL:                 http://www.nic.ad.jp/ja/idn/idnkit/download/
Source:              http://www.nic.ad.jp/ja/idn/idnkit/download/sources/idnkit-%{version}-src.tar.gz
SUNW_BaseDir:        /
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWpostrun

%package devel
Summary:                 %{summary} - developer files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name


%prep
%setup -q -c -n %name-%version

%ifarch amd64
cp -rp idnkit-%version-src idnkit-%version-src-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS32="%optflags"
export LDFLAGS32="%_ldflags"

export CFLAGS64="%optflags64"
export LDFLAGS64="%_ldflags64"

%ifarch amd64
export CFLAGS="$CFLAGS64"
export LDFLAGS="$LDFLAGS64"
cd idnkit-%version-src-64

./configure --prefix=%{_prefix}         \
           --libdir=%{_libdir}/%{_arch64} \
           --sysconfdir=%{_sysconfdir} \
           --mandir=%{_mandir}         \
           --infodir=%{_infodir}       \
           --disable-static

make -j $CPUS
cd ..
%endif

export CFLAGS="$CFLAGS32"
export LDFLAGS="$LDFLAGS32"
cd idnkit-%version-src

./configure --prefix=%{_prefix}         \
           --mandir=%{_mandir}         \
           --sysconfdir=%{_sysconfdir} \
           --infodir=%{_infodir}       \
           --disable-static

make -j $CPUS
cd ..

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64
cd idnkit-%version-src-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_includedir}/idn/punycode.h

#
# We only need 32Bit executables
#
rm $RPM_BUILD_ROOT%{_bindir}/*
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/*.la
cd ..
%endif

cd idnkit-%version-src
make install DESTDIR=$RPM_BUILD_ROOT

#
# Avoid conflict with punycode from GNU idn
#
mv $RPM_BUILD_ROOT%{_includedir}/idn/punycode.h $RPM_BUILD_ROOT%{_includedir}/idn/punycode_idnkit.h
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%ifarch amd64
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*.1
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*.3
%dir %attr (0755, root, bin) %{_mandir}/man5
%{_mandir}/man5/*.5

%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/*

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_datadir}/idnkit
%{_datadir}/idnkit/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Sun 18 May 2008 - moinakg@gmail.com
- Initial spec
