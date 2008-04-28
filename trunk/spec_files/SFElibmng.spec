#
# spec file for package SFElibmng
#
# includes module(s): libmng
#
%include Solaris.inc

%ifarch amd64
%include arch64.inc
%endif

%include base.inc

Name:                    SFElibmng
Summary:                 libmng  - the MNG reference library
Version:                 1.0.10
Source:                  %{sf_download}/libmng/libmng-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFElcms-devel
Requires: SFElcms

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -c -n %name-%version

%ifarch amd64
cp -rp libmng-%version libmng-%version-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS32="%optflags"
export CFLAGS64="%optflags64"
export LDFLAGS32="%_ldflags"
export LDFLAGS64="%_ldflags64"

%ifarch amd64
export CFLAGS="$CFLAGS64"
export LDFLAGS="$LDFLAGS64"

cd libmng-%version-64
cp makefiles/configure.in .
cp makefiles/Makefile.am .
for f in *.[ch]; do dos2unix -ascii $f $f; done
libtoolize --force
aclocal $ACLOCAL_FLAGS
autoconf
automake -a -c -f
./configure --prefix=%{_prefix}              \
            --mandir=%{_mandir}              \
            --libdir=%{_libdir}/%{_arch64}   \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-shared		     \
	    --disable-static

make -j$CPUS 
cd ..
%endif

export CFLAGS="$CFLAGS32"
export LDFLAGS="$LDFLAGS43"

cd libmng-%version
cp makefiles/configure.in .
cp makefiles/Makefile.am .
for f in *.[ch]; do dos2unix -ascii $f $f; done
libtoolize --force
aclocal $ACLOCAL_FLAGS
autoconf
automake -a -c -f
./configure --prefix=%{_prefix}              \
            --mandir=%{_mandir}              \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-shared                  \
            --disable-static

make -j$CPUS


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64
cd libmng-%version-64
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/lib*a
cd ..
%endif

cd libmng-%version
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%ifarch amd64
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man5
%{_mandir}/man5/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%changelog
* Tue Apr 29 2008 - moinakg@gmail.com
- Enable building 32Bit and 64Bit libraries needed for Qt3.
* Sun Nov 4 2007 - markwright@internode.on.net
- Bump to 1.1.10
* Fri Mar 30 2007 - daymobrew@users.sourceforge.net
- Change source URL to one working sourceforge mirror

* Sun Jan  7 2007 - laca@sun.com
- create
