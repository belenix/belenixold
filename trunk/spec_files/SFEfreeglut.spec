#
# spec file for package SFEfreeglut.spec
#
# includes module(s): freeglut
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

%define src_name	freeglut
%define src_url		%{sf_download}/freeglut
%define src_version     2.6.0

Name:                   SFEfreeglut
Summary:                Free OpenGL Library
Version:                %{src_version}-rc1
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
Patch1:                 freeglut-01-GL-defines.diff

SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEjam

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
%setup -q -c -n %name-%version
cd %{src_name}-%{src_version}
%patch1 -p1
cd ..

%ifarch amd64 sparcv9
cp -rp %{src_name}-%{src_version} %{src_name}-%{src_version}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

%ifarch amd64 sparcv9
cd %{src_name}-%{src_version}-64
bash ./autogen.sh
chmod 755 ./configure

export CFLAGS="%optflags64 -I/usr/X11/include"
#export LDFLAGS="%_ldflags64 -lX11 -L/usr/X11/lib/%{_arch64} -R/usr/X11/lib/%{_arch64}"
export LDFLAGS="%_ldflags64"
export LD_OPTIONS="-i"

./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}/%{_arch64}	\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}/%{_arch64}	\
            --includedir=%{_prefix}/X11/include	\
            --datadir=%{_datadir}		\
            --libexecdir=%{_libexecdir}/%{_arch64} 	\
            --sysconfdir=%{_sysconfdir} 	\
	    --x-libraries=%{_prefix}/X11/lib/%{_arch64} \
	    --disable-warnings			\
            --enable-shared			\
	    --disable-static
make -j ${CPUS}
cd ..
%endif

cd %{src_name}-%{src_version}
bash ./autogen.sh
chmod 755 ./configure
export CFLAGS="%optflags -I/usr/X11/include"
#export LDFLAGS="%_ldflags -lX11 -L/usr/X11/lib -R/usr/X11/lib"
export LDFLAGS="%_ldflags"
export LD_OPTIONS="-i"

./configure --prefix=%{_prefix}                 \
            --bindir=%{_bindir}                 \
            --mandir=%{_mandir}                 \
            --libdir=%{_libdir}                 \
            --includedir=%{_prefix}/X11/include \
            --datadir=%{_datadir}               \
            --libexecdir=%{_libexecdir}         \
            --sysconfdir=%{_sysconfdir}         \
            --disable-warnings                  \
            --enable-shared                     \
            --disable-static
make -j ${CPUS}
cd ..


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd %{src_name}-%{src_version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/lib*.*a
cd ..
%endif

cd %{src_name}-%{src_version}
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/lib*.*a
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/*.so*
%endif

%files devel
%defattr (-, root, bin)
%{_prefix}/X11/include

%changelog
* Tue Apr 28 2009 - moinakg@belenix.org
- Bump version to 2.6.0-rc1 and add 64Bit build.
* Sat Oct 13 2007 - laca@sun.com
- add /usr/X11 to CFLAGS and LDFLAGS to be able to build with FOX
* Tue Jun  5 2007 - dougs@truemail.co.th
- Added SFEjam as a build requirement
* Sun May  6 2007 - dougs@truemail.co.th
- Initial version
