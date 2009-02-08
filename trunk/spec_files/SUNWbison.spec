#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# spec file for package SUNWgmp
#
# includes module(s): GNU gmp
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

Name:                    SUNWbison
Summary:                 bison - A YACC Replacement
Version:                 2.4.1
URL:                     http://www.gnu.org/software/bison/
Source:                  http://ftp.gnu.org/gnu/bison/bison-%{version}.tar.bz2
Source1:                 mapfile_noexstk

Patch1:                  bison-01-makefile.in.diff
SUNW_BaseDir:            /
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:                SUNWgcmn
Requires:                SUNWgccruntime

%prep
if [ "x`basename $CC`" = xgcc ]
then
	%error This spec file requires SUN Studio, set the CC and CXX env variables
fi

%setup -q -c -n %name-%version
cd bison-%{version}
%patch1 -p 1
cd ..

%ifarch amd64 sparcv9
cp -rp bison-%version bison-%version-64
%endif


%build
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT

export CFLAGS32="-xO4 -xspace -xstrconst -I/usr/gnu/include -I/usr/sfw/include"
export CFLAGS64="-xO4 -xspace -xstrconst -m64 -I/usr/gnu/include -I/usr/sfw/include"

ccpath=`dirname $CC`
PATH="${ccpath}:/usr/perl5/bin:/usr/sfw/bin:/usr/bin:/usr/ccs/bin"
export PATH

MAKE=/usr/bin/make
export MAKE

%ifarch amd64 sparcv9
cd bison-%version-64
CFLAGS="$CFLAGS64"
export CFLAGS

./configure --prefix=%{_basedir}

cd lib
LD_OPTIONS="-M %{SOURCE1}"
export LD_OPTIONS

/usr/bin/make liby.so.1
cd ../..
%endif

cd bison-%version
CFLAGS="$CFLAGS32"
export CFLAGS

./configure --prefix=%{_basedir}

LD_OPTIONS="-M %{SOURCE1}"
export LD_OPTIONS

/usr/bin/make
cd ..

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd bison-%version-64/lib
mkdir -p ${RPM_BUILD_ROOT}%{_basedir}/sfw/lib/%{_arch64}
cp liby.so.1 ${RPM_BUILD_ROOT}%{_basedir}/sfw/lib/%{_arch64}
chmod 0555 ${RPM_BUILD_ROOT}%{_basedir}/sfw/lib/%{_arch64}/*
cd ../..
%endif

cd bison-%version
make install DESTDIR=$RPM_BUILD_ROOT

rm -f ${RPM_BUILD_ROOT}%{_basedir}/lib/*.a
rm -f ${RPM_BUILD_ROOT}%{_basedir}/lib/charset.alias
mv ${RPM_BUILD_ROOT}%{_basedir}/lib/* ${RPM_BUILD_ROOT}%{_basedir}/sfw/lib
rmdir ${RPM_BUILD_ROOT}%{_basedir}/lib
mkdir -p ${RPM_BUILD_ROOT}%{_basedir}/sfw/bin
rm -f ${RPM_BUILD_ROOT}%{_basedir}/bin/yacc
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir
rm -f ${RPM_BUILD_ROOT}%{_mandir}/man1/yacc.1
(cd ${RPM_BUILD_ROOT}%{_basedir}/sfw/bin
  ln -s ../../bin/bison)

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, bin) %{_basedir}/bin
%dir %attr (0755, root, bin) %{_basedir}/sfw
%dir %attr (0755, root, bin) %{_basedir}/sfw/bin
%dir %attr (0755, root, bin) %{_basedir}/sfw/lib
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/bison
%dir %attr (0755, root, other) %{_datadir}/aclocal
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%dir %attr (0755, root, bin) %{_infodir}
%{_basedir}/bin/*
%{_datadir}/bison/*
%{_datadir}/aclocal/*
%{_infodir}/*
%{_mandir}/man1/*
%{_basedir}/sfw/bin/*
%{_basedir}/sfw/lib/liby.so.1

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_basedir}/sfw/lib/%{_arch64}
%{_basedir}/sfw/lib/%{_arch64}/liby.so.1
%endif

%changelog
* Sun Feb 08 2009 - moinakg@gmail.com
- Initial spec (migrated from SFW gate).

