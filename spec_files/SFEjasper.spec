#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#

%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

Name:                SFEjasper
License:             Jasper Software License
Summary:             A free software-based reference implementation of the JPEG-2000 Part-1 CODEC
Version:             1.900.1
URL:                 http://www.ece.uvic.ca/~mdadams/jasper/
Source:              http://www.ece.uvic.ca/~mdadams/jasper/software/jasper-%{version}.zip
Source1:             http://www.ece.uvic.ca/~mdadams/jasper/LICENSE

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%prep
%setup -q -c -n %name-%version
%ifarch amd64 sparcv9
cp -rp jasper-%{version} jasper-%{version}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

%ifarch amd64 sparcv9
cd jasper-%{version}-64
export CFLAGS="%optflags64 -I%{gnu_inc} -D__C99FEATURES__"
export LDFLAGS="%_ldflags64 %{gnu_lib_path64}"

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir}/%{_arch64} \
            --libdir=%{_libdir}/%{_arch64} \
            --mandir=%{_mandir} \
            --enable-shared=yes \
            --enable-static=no  \
            --with-pic          \
            --without-docs

make -j$CPUS
cd ..
%endif

cd jasper-%{version}
export CFLAGS="%optflags -I%{gnu_inc} -D__C99FEATURES__"
export LDFLAGS="%_ldflags %{gnu_lib_path}"

./configure --prefix=%{_prefix}	\
            --mandir=%{_mandir}	\
            --enable-shared=yes \
            --enable-static=no  \
            --with-pic          \
            --without-docs

make -j$CPUS
cd ..

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd jasper-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
cd ..
%endif

cd jasper-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
cd ..

find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

mkdir -p $RPM_BUILD_ROOT%{_datadir}/doc/jasper
cp %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/doc/jasper

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/*.so*
%endif

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Mon Nov 02 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Add 64Bit build.
* Wed Jan 30 2008 - moinak.ghosh@sun.com
- Initial spec.
