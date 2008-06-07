#
# spec file for package SFElcms
#
# includes module(s): liblcms
#
%include Solaris.inc

%ifarch amd64
%include arch64.inc
%endif

%include base.inc

%define python_version 2.4

Name:                    SFElcms
Summary:                 Little ColorManagement System
Version:                 1.17
Source:                  http://www.littlecms.com/lcms-%{version}.tar.gz
Patch1:                  lcms-01-python-libs.diff
URL:                     http://www.littlecms.com
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires: SUNWTiff
Requires: SUNWjpg
Requires: SUNWzlib
Requires: SUNWlibms
Requires: SUNWPython
Requires: SUNWlibC
BuildRequires: SUNWPython-devel
BuildRequires: SUNWTiff-devel
BuildRequires: SUNWjpg-devel
BuildRequires: SUNWzlib
BuildRequires: SFEswig
%include default-depend.inc

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -c -n %name-%version
cd lcms-%version
%patch1 -p1
cd ..

%ifarch amd64
cp -rp lcms-%version lcms-%version-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS32="%optflags"
export CFLAGS64="%optflags64"
export CXXFLAGS32="%cxx_optflags"
export CXXFLAGS64="%cxx_optflags64"
export LDFLAGS32="%{_ldflags}"
export LDFLAGS64="%{_ldflags64}"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"

%if %cc_is_gcc
%else
export CXX="${CXX} -norunpath"
%endif

%ifarch amd64
export CFLAGS="$CFLAGS64"
export CXXFLAGS="$CXXFLAGS64"
export LDFLAGS="$LDFLAGS64"

cd lcms-%version-64
aclocal $ACLOCAL_FLAGS
automake -c -f
./configure --prefix=%{_prefix} --bindir=%{_bindir}/%{_arch64}     \
            --libdir=%{_libdir}/%{_arch64}      \
            --includedir=%{_includedir} \
            --with-python=no --mandir=%{_mandir} --enable-static=no
make -j$CPUS
cd ..
%endif

export CFLAGS="$CFLAGS32"
export CXXFLAGS="$CXXFLAGS32"
export LDFLAGS="$LDFLAGS32"

cd lcms-%version
aclocal $ACLOCAL_FLAGS
automake -c -f
./configure --prefix=%{_prefix} --bindir=%{_bindir}/%{base_isa}     \
            --libdir=%{_libdir}/      \
            --includedir=%{_includedir} \
            --with-python --mandir=%{_mandir} --enable-static=no
make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64
cd lcms-%version-64
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/lib*a
cd ..
%endif

cd lcms-%version
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

cd $RPM_BUILD_ROOT%{_libdir}/python%{python_version}
mv site-packages vendor-packages
rm vendor-packages/_lcms.la

#
# Prepare isaexec links
#
for f in `ls -1 $RPM_BUILD_ROOT%{_bindir}/%{base_isa}`
do
  if [ -f $RPM_BUILD_ROOT%{_bindir}/%{base_isa}/$f -a -x $RPM_BUILD_ROOT%{_bindir}/%{base_isa}/$f ]
  then
    echo "Linking to isaexec: $RPM_BUILD_ROOT%{_bindir}/$f"

    # how many "/" below $RPM_BUILD_ROOT - add "../" to isaexec path depending how many "/" arein $f
    ISAEXECOFFSET=`echo %{_bindir}/ | sed -e 's?/\{0,1\}\w*\(/\)?../?g' | sed -e 's?\(\w*$\)??'`
    ln -s ${ISAEXECOFFSET}usr/lib/isaexec $RPM_BUILD_ROOT%{_bindir}/$f
  fi
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%if %can_isaexec
%{_bindir}/%{_arch64}/*
%{_bindir}/%{base_isa}/*
%hard %{_bindir}/icc2ps
%hard %{_bindir}/icclink
%hard %{_bindir}/icctrans
%hard %{_bindir}/jpegicc
%hard %{_bindir}/tiffdiff
%hard %{_bindir}/tifficc
%hard %{_bindir}/wtpt
%else
%{_bindir}/*
%endif

%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/python%{python_version}

%ifarch amd64
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%ifarch amd64
%dir %attr (0755, root, other)  %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*.pc
%endif

%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Sat Jun 07 2008 - moinakg@gmail.com
- Fix symlink depth.
* Tue Apr 29 2008 - moinakg@gmail.com
- Enable building 32Bit and 64Bit libraries needed for Qt3.
* Sun Sep 16 2007 - dougs@truemail.co.th
- Bump to 1.17
* Tue Feb  6 2007 - damien.carbery@sun.com
- Bump to 1.16. Add aclocal call because automake version mismatch.
* Fri Jun 23 2006 - laca@sun.com
- rename to SFElcms
- update file attributes to match JDS
* Tue Mar 21 2006 - damien.carbery@sun.com
- Minor mods to %files (/usr/lib -> %{_libdir}).
* Fri Mar 17 2006 - markgraf@neuro2.med.uni.magdeburg.de
- Initial spec
