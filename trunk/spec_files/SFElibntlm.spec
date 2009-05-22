#
# spec file for package SFElibntlm
#
# includes module(s): libntlm
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

%define	src_name libntlm
%define	src_url	http://josefsson.org/libntlm/releases

Name:                SFElibntlm
Summary:             Microsoft's NTLM authentication library
Version:             1.1
License:             LGPLv2.1+
Source:              %{src_url}/%{src_name}-%{version}.tar.gz
URL:                 http://josefsson.org/libntlm

SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%description
Libntlm is a library that implement Microsoft's NTLM authentication.
It is an improved version of the original libntlm library distributed
from ftp://ftp.visi.com/users/grante/ntlm.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%prep
%setup -q -c -n %name-%version

%ifarch amd64 sparcv9
cp -rp %{src_name}-%version %{src_name}-%{version}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

%ifarch amd64 sparcv9
cd %{src_name}-%{version}-64

export CFLAGS="%optflags64"
export LDFLAGS="%_ldflags64"

./configure --prefix=%{_prefix}			\
            --bindir=%{_bindir}/%{_arch64}	\
            --libdir=%{_libdir}/%{_arch64}	\
            --sysconfdir=%{_sysconfdir}		\
            --includedir=%{_includedir} 	\
            --mandir=%{_mandir}			\
	    --infodir=%{_infodir}		\
	    --disable-rpath			\
	    --disable-static			\
	    --enable-shared

make -j$CPUS
cd ..
%endif

cd %{src_name}-%{version}
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}                 \
            --bindir=%{_bindir}                 \
            --libdir=%{_libdir}                 \
            --sysconfdir=%{_sysconfdir}         \
            --includedir=%{_includedir}         \
            --mandir=%{_mandir}                 \
            --infodir=%{_infodir}               \
            --disable-rpath                     \
            --disable-static                    \
            --enable-shared

make -j$CPUS
cd .. 

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
cd %{src_name}-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/lib*.*a
cd ..
%endif

cd %{src_name}-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a
cd ..

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
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%changelog
* Fri May 22 2009 - moinakg@belenix.org
- Bump version and add 64Bit build.
* Fri Jul 27 2007 - dougs@truemail.co.th
- Initial spec
