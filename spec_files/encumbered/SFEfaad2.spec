#
# spec file for package SUNWfaad2.spec
#
# includes module(s): faad2
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc


Name:                    SFEfaad2
Summary:                 faad2 - a high-quality MPEG audio decoder
Group:                   libraries/multimedia
Version:                 2.7
Source:                  %{sf_download}/faac/faad2-%{version}.tar.gz
URL:                     http://www.audiocoding.com/
Patch4:                  faad-04-wall.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEid3lib
BuildRequires: SFEid3lib-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -c -n %name-%version

cd faad2-%{version}
%patch4 -p1

cd ..

%ifarch amd64 sparcv9
cp -rp faad2-%{version} faad2-%{version}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export MSGFMT="/usr/bin/msgfmt"

%if %cc_is_gcc
export B_CXXFLAGS=""
export B_CFLAGS=""
%else
export CXX="${CXX} -norunpath"
export B_CFLAGS="-D__inline= "
%endif
%ifarch sparc
export B_CXXFLAGS="-norunpath -xO5 -xlibmil -xlibmopt -features=tmplife"
%else
export B_CXXFLAGS="-norunpath -xO3 -xlibmil -xlibmopt -features=tmplife"
%endif

%ifarch amd64 sparcv9
cd faad2-%{version}-64
export CFLAGS="%optflags64 ${B_CFLAGS}"
export LDFLAGS="-m64"
export CXXFLAGS="${B_CXXFLAGS} -m64"

autoreconf --install
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --bindir=%{_bindir}/%{_arch64}   \
            --libdir=%{_libdir}/%{_arch64}   \
            --libexecdir=%{_libexecdir}/%{_arch64}      \
            --sysconfdir=%{_sysconfdir}      \
            --with-mp4v2                     \
            --enable-shared		     \
	    --disable-static

make -j$CPUS 
cd ..
%endif

cd faad2-%{version}
export CFLAGS="%optflags ${B_CFLAGS}"
export CXXFLAGS="${B_CXXFLAGS}"
export LDFLAGS=""

autoreconf --install
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --with-mp4v2                     \
            --enable-shared                  \
            --disable-static

make -j$CPUS
cd ..

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd faad2-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/lib*a
cd ..
%endif

cd faad2-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a
cd ..

if [ -d ${RPM_BUILD_ROOT}%{_mandir}/manm ]
then
	mv ${RPM_BUILD_ROOT}%{_mandir}/manm ${RPM_BUILD_ROOT}%{_mandir}/man1m
fi


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/faad
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1m
%{_mandir}/man1m/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/faad
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Tue Apr 28 2009 - moinakg@belenix.org
- Bump version to 2.7, remove unneded patches and add 64Bit build.
* Mon Nov 5 2007 - markwright@internode.on.net
- Bump to 2.6.1.  Bump patch2 and patch4.  Comment patch1, patch3 and patch5.
* Fri Jun 23 2005 - laca@sun.com
- rename to SFEfaad2
- update file attributes
- remove lib*a
* Mon May  8 2006 - drdoug007@yahoo.com.au
- Initial version
