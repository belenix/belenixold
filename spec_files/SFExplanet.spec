#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include base.inc

Name:                SFExplanet
Summary:             Render a planetary image into an X window
Version:             1.2.1
License:             GPLv2
Source:              http://downloads.sourceforge.net/xplanet/xplanet-%{version}.tar.gz
URL:                 http://xplanet.sourceforge.net/
Patch1:              xplanet-01-gcc44.diff

SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWlexpt
Requires: SUNWglib2
Requires: SUNWxwsvr
Requires: FSWxorg-clientlibs
Requires: SUNWxorg-clientlibs
Requires: SUNWjpg
Requires: SFEgiflib
Requires: SUNWTiff
Requires: SFEnetpbm
Requires: SUNWpango
BuildRequires: SUNWlexpt
BuildRequires: SUNWglib2-devel
BuildRequires: FSWxorg-headers
BuildRequires: SUNWxorg-headers
BuildRequires: SUNWjpg-devel
BuildRequires: SFEgiflib
BuildRequires: SUNWTiff-devel
BuildRequires: SFEnetpbm-devel
BuildRequires: SUNWpango-devel

%prep
%setup -q -c -n %name-%version
cd xplanet-%version
%patch1 -p1
cd ..

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

cd xplanet-%{version}
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -lm"

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --libdir=%{_libdir} \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir} \
            --includedir=%{_includedir} \
            --libexecdir=%{_libexecdir}

gmake -j$CPUS

cd ..


%install
rm -rf $RPM_BUILD_ROOT
cd xplanet-%{version}
gmake DESTDIR=$RPM_BUILD_ROOT install
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_datadir}/xplanet
%{_datadir}/xplanet/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%changelog
* Fri Aug 14 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Initial version.
