#
# spec file for package SFEautoconf213
#
#
%include Solaris.inc
%include usr-gnu.inc

Name:			SFEautoconf213
License:		Apache,LGPL,BSD
Version:		2.13
Summary:		GNU Autoconf 2.13
Source:			http://ftp.gnu.org/gnu/autoconf/autoconf-2.13.tar.gz
Patch1:                 autoconf213-01-Makefile.in.diff

URL:			http://www.gnu.org/software/autoconf/
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:		%{_prefix}
%if %cc_is_gcc
Requires: SFEgccruntime
%endif

%prep
%setup -q -c -n %name-%version
cd autoconf-%{version}
%patch1 -p1
cd ..

%build
cd autoconf-%{version}
export CFLAGS="%optflags -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"
export LD=/usr/ccs/bin/ld
export LDFLAGS="%_ldflags -L/lib -R/lib -L$RPM_BUILD_ROOT%{_libdir}"
./configure \
    --prefix=%{_prefix} \
    --sysconfdir=%{_sysconfdir} \
    --libdir=%{_libdir} \
    --disable-static \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --program-suffix=-%{version}

make

%install
rm -rf $RPM_BUILD_ROOT
cd autoconf-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_infodir}

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.exp
rmdir ${RPM_BUILD_ROOT}/usr/share

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/*

%changelog
* Tue Jul 07 2009 - moinakg(at)belenix<dot>org
- Initial spec.
