#
# spec file for package SFEmeanwhile
#
# includes module(s): meanwhile
#
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

Name:                    SFEmeanwhile
Summary:                 Lotus Sametime Community Client library
Version:                 1.1.0
License:                 LGPLv2+
URL:                     http://meanwhile.sourceforge.net
Source:                  http://www.belenix.org/binfiles/meanwhile-%{version}.tar.bz2
Patch1:                  meanwhile-01-crash.diff

SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:               SUNWglib2
BuildRequires:          SUNWglib2-devel
BuildRequires:          SFEdoxygen
BuildRequires:          SUNWgnome-common-devel

%description
The heart of the Meanwhile Project is the Meanwhile library, providing the
basic Lotus Sametime session functionality along with the core services;
Presence Awareness, Instant Messaging, Multi-user Conferencing, Preferences
Storage, Identity Resolution, and File Transfer. This extensible client
interface allows additional services to be added to a session at runtime,
allowing for simple integration of future service handlers such as the user
directory and whiteboard and screen-sharing.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires:          SUNWglib2-devel
Requires:          SFEdoxygen
Requires:          SUNWgnome-common-devel

%package doc
Summary:                 %{summary} - documentation files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -c -n %name-%version
cd meanwhile-%{version}
%patch1 -p0
#%patch2 -p1
cd ..

%ifarch amd64 sparcv9
cp -rp meanwhile-%{version} meanwhile-%{version}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

%ifarch amd64 sparcv9
cd meanwhile-%{version}-64
export CFLAGS="%optflags64"
export LDFLAGS="%_ldflags64 -L%{_libdir}/%{_arch64} -R%{_libdir}/%{_arch64} -lsocket -lnsl"

bash ./autogen.sh
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --bindir=%{_bindir}/%{_arch64}          \
            --libdir=%{_libdir}/%{_arch64}          \
            --enable-shared		            \
            --disable-static                        \
            --enable-doxygen=yes                    \
            --enable-gtk-doc=yes

make -j$CPUS 
cd ..
%endif

cd meanwhile-%{version}
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -L%{_libdir} -R%{_libdir} -lsocket -lnsl"

bash ./autogen.sh
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --bindir=%{_bindir}                     \
            --libdir=%{_libdir}                     \
            --enable-shared		            \
            --disable-static                        \
            --enable-doxygen=yes                    \
            --enable-gtk-doc=yes

make -j$CPUS
cd ..


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd meanwhile-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/lib*.a
cd ..
%endif

cd meanwhile-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/lib*.a
cd ..

#
# Nuke unwanted latex doc
#
rm -rf $RPM_BUILD_ROOT%{_docdir}/meanwhile-doc-%{version}/latex

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%files doc
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*

%changelog
* Thu Jul 02 2009 - Moinak Ghosh <moinakg@belenix(dot)org>
- Initial version.
