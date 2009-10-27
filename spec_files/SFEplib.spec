#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

Name:                SFEplib
Summary:             Set of portable libraries especially useful for games
Version:             1.8.5
License:             LGPLv2+
Source:              http://plib.sourceforge.net/dist/plib-%{version}.tar.gz
URL:                 http://plib.sourceforge.net/
Patch1:              plib-01-fullscreen.diff
Patch2:              plib-02-autorepeat.diff

SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SFEfreeglut
Requires: SUNWpng
Requires: SUNWxorg-clientlibs
Requires: SFEfreeglut-devel
Requires: SUNWpng-devel
Requires: SUNWxorg-headers

%description
This is a set of OpenSource (LGPL) libraries that will permit programmers
to write games and other realtime interactive applications that are 100%
portable across a wide range of hardware and operating systems. Here is
what you need - it's all free and available with LGPL'ed source code on
the web. All of it works well together.

%prep
%setup -q -c -n %name-%version
cd plib-%version
%patch1 -p1
%patch2 -p1
cd ..

%ifarch amd64 sparcv9
cp -rp plib-%version plib-%{version}-64
%endif


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

%ifarch amd64 sparcv9
cd plib-%{version}-64

export CFLAGS="%optflags64"
export CXXFLAGS="%cxx_optflags64"
export LDFLAGS="%_ldflags64"

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir}/%{_arch64} \
            --libdir=%{_libdir}/%{_arch64} \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir} \
            --includedir=%{_includedir} \
            --libexecdir=%{_libexecdir}

gmake -j$CPUS
cd ..
%endif

cd plib-%{version}
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags"

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

%ifarch amd64 sparcv9
cd plib-%{version}-64

gmake DESTDIR=$RPM_BUILD_ROOT install
cd ..
%endif

cd plib-%{version}
gmake DESTDIR=$RPM_BUILD_ROOT install
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.a

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/*.a
%endif

%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, bin) %{_includedir}/plib
%{_includedir}/plib/*.h

%changelog
* Mon Oct 19 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Initial version.
