#
# spec file for package SFElibmad
#
# includes module(s): libmad
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc


Name:                    SFElibmad
Summary:                 libmad  - a high-quality MPEG audio decoder
Version:                 0.15.1.2
%define tarball_version  0.15.1b
Source:                  %{sf_download}/mad/libmad-%{tarball_version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -c -n %name-%version

%ifarch amd64 sparcv9
cp -rp libmad-%{tarball_version} libmad-%{tarball_version}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

%define fp_arch	 default
%if %cc_is_gcc
%define fpm_option --enable-fpm
%else
# asm stuff breaks with sun studio :(
%define fpm_option --disable-fpm
%endif

export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export MSGFMT="/usr/bin/msgfmt"

%ifarch amd64 sparcv9
cd libmad-%{tarball_version}-64
export CFLAGS="%optflags64"

%ifarch amd64
%define fp_arch 64bit
%endif
%ifarch sparcv9
%define fp_arch sparcv9
%endif

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}/%{_arch64}   \
            --libexecdir=%{_libexecdir}/%{_arch64}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-fpm=%{fp_arch}          \
            --enable-shared                  \
            --enable-accuracy                \
            %fpm_option                      \
            --disable-static

make -j$CPUS 
cd ..
%endif


%ifarch i386
%define fp_arch intel
%endif
%ifarch sparc
%define fp_arch sparc
%endif

cd libmad-%{tarball_version}
export CFLAGS="%optflags"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-fpm=%{fp_arch}          \
            --enable-shared		     \
            --enable-accuracy                \
            %fpm_option                      \
	    --disable-static

make -j$CPUS 
cd ..

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd libmad-%{tarball_version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/lib*a
cd ..
%endif

cd libmad-%{tarball_version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a
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
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Tue Apr 28 2009 - moinakg@belenix.org
- Add 64Bit build.
* Thu Jul 27 2006 - halton.huo@sun.com
- Correct Source url s/kend/kent
* Mon Jun 12 2006 - laca@sun.com
- renamed to SFElibmad
- changed to root:bin to follow other JDS pkgs.
- disable fpm when using sun studio, as the inline assembly syntax is different
  and breaks the build
* Mon May 8 2006 - drdoug007@yahoo.com.au
- Initial version
