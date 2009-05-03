%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

%define src_name	clucene-core
Name:                   SFEclucene-core
Version:                0.9.20
Summary:                Clucene is a high-performance full text-search engine.
URL:                    http://sourceforge.net/projects/clucene/
Source:                 %{sf_download}/clucene/%{src_name}-%{version}.tar.gz
License:                LGPLv2|APLv2

SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -c -n %name-%version

%ifarch amd64 sparcv9
cp -rp %{src_name}-%{version} %{src_name}-%{version}-64
%endif

%build
UNAMEP="`uname -p`"

if [ "x${UNAMEP}" = "xsparc" ] ; then
    BASE_CFLAGS="-DFLT_EVAL_METHOD=1 -D__FLT_EVAL_METHOD__=1"
    BASE_CXXFLAGS="-DFLT_EVAL_METHOD=1 -D__FLT_EVAL_METHOD__=1"
else
%if %cc_is_gcc
    BASE_CFLAGS="-DFLT_EVAL_METHOD=1"
    BASE_CXXFLAGS="-DFLT_EVAL_METHOD=1"
%else
    BASE_CFLAGS="-fprecision=double -DFLT_EVAL_METHOD=1 -D__FLT_EVAL_METHOD__=1"
    BASE_CXXFLAGS="-fprecision=double -DFLT_EVAL_METHOD=1 -D__FLT_EVAL_METHOD__=1"
%endif
fi

%ifarch amd64 sparcv9
cd %{src_name}-%{version}-64

export CFLAGS="%optflags64 ${BASE_CFLAGS}"
export CXXFLAGS="%cxx_optflags64 ${BASE_CXXFLAGS}"
export LDFLAGS="%_ldflags64 -L/usr/gnu/lib/%{_arch64} -R/usr/gnu/lib/%{_arch64}"

# Clucene-core doesn't like the -xc99=%all option :(
export CFLAGS="`echo $CFLAGS | sed -e 's/-xc99=%all//g'`"
export CFLAGS="`echo $CFLAGS | sed -e 's/-std=c99//g'`"

chmod 0755 configure

./configure --prefix=%{_prefix} \
        --bindir=%{_bindir}/%{_arch64} \
        --datadir=%{_datadir} \
        --includedir=%{_includedir} \
        --infodir=%{_infodir} \
        --libdir=%{_libdir}/%{_arch64} \
        --libexecdir=%{_libexecdir}/%{_arch64} \
        --localstatedir=%{_localstatedir} \
        --mandir=%{_mandir} \
        --sbindir=%{_sbindir}/%{_arch64} \
        --sysconfdir=%{_sysconfdir} \
        --enable-shared \
        --disable-static \
        --disable-libtool-lock \
        --enable-multithreading \
        --enable-largefile \
        --with-pic

make
cd ..
%endif

cd %{src_name}-%{version}

export CFLAGS="%optflags ${BASE_CFLAGS}"
export CXXFLAGS="%cxx_optflags ${BASE_CXXFLAGS}"
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib"

# Clucene-core doesn't like the -xc99=%all option :(
export CFLAGS="`echo $CFLAGS | sed -e 's/-xc99=%all//g'`"
export CFLAGS="`echo $CFLAGS | sed -e 's/-std=c99//g'`"

chmod 0755 configure

./configure --prefix=%{_prefix} \
        --bindir=%{_bindir} \
        --datadir=%{_datadir} \
        --includedir=%{_includedir} \
        --infodir=%{_infodir} \
        --libdir=%{_libdir} \
        --libexecdir=%{_libexecdir} \
        --localstatedir=%{_localstatedir} \
        --mandir=%{_mandir} \
        --sbindir=%{_sbindir} \
        --sysconfdir=%{_sysconfdir} \
        --enable-shared \
        --disable-static \
        --disable-libtool-lock \
        --enable-multithreading \
        --enable-largefile \
        --with-pic

make
cd ..


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd %{src_name}-%{version}-64

mkdir -p $RPM_BUILD_ROOT%{_libdir}/%{_arch64}
mkdir -p $RPM_BUILD_ROOT%{_includedir}
mkdir -p $RPM_BUILD_ROOT%{_docdir}

make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/*.la $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/*.a

mv $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/CLucene/clucene-config.h $RPM_BUILD_ROOT%{_includedir}/CLucene/
rmdir $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/CLucene/

cd ..
%endif

cd %{src_name}-%{version}

mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_includedir}
mkdir -p $RPM_BUILD_ROOT%{_docdir}

make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la $RPM_BUILD_ROOT%{_libdir}/*.a

rm $RPM_BUILD_ROOT%{_libdir}/CLucene/clucene-config.h
rmdir $RPM_BUILD_ROOT%{_libdir}/CLucene/

cd ..


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%_arch64
%{_libdir}/%_arch64/lib*.so*
%endif
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/CLucene.h
%{_includedir}/CLucene/*


%changelog
* Sun May 03 2009 - moinakg@belenix.org
- Initial version
