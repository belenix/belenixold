Name:            libxml2
Summary:         Library providing XML and HTML support
Version:         2.7.8
Release:         1%{?dist}
License:         MIT
Group:           Development/Libraries
Source:          ftp://xmlsoft.org/libxml2/libxml2-%{version}.tar.gz
URL:             http://xmlsoft.org/
BuildRoot:       %{_tmppath}/%{name}-%{version}-root
#BuildRequires:   python python-devel
BuildRequires:   zlib-devel pkgconfig

%description
This library allows to manipulate XML files. It includes support 
to read, modify and write XML and HTML files. There is DTDs support
this includes parsing and validation even with complex DtDs, either
at parse time or later once the document has been modified. The output
can be a simple SAX stream or and in-memory DOM like representations.
In this case one can use the built-in XPath and XPointer implementation
to select subnodes or ranges. A flexible Input/Output mechanism is
available, with existing HTTP and FTP modules and combined to an
URI library.

%package devel
Summary: Libraries, includes, etc. to develop XML and HTML applications
Group: Development/Libraries
Requires: libxml2 = %{version}-%{release}
Requires: zlib-devel
Requires: pkgconfig

%description devel
Libraries, include files, etc you can use to develop XML applications.
This library allows to manipulate XML files. It includes support 
to read, modify and write XML and HTML files. There is DTDs support
this includes parsing and validation even with complex DtDs, either
at parse time or later once the document has been modified. The output
can be a simple SAX stream or and in-memory DOM like representations.
In this case one can use the built-in XPath and XPointer implementation
to select subnodes or ranges. A flexible Input/Output mechanism is
available, with existing HTTP and FTP modules and combined to an
URI library.

%package python
Summary: Python bindings for the libxml2 library
Group: Development/Libraries
Requires: libxml2 = %{version}-%{release}

%description python
The libxml2-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by the libxml2 library to manipulate XML files.

This library allows to manipulate XML files. It includes support 
to read, modify and write XML and HTML files. There is DTDs support
this includes parsing and validation even with complex DTDs, either
at parse time or later once the document has been modified.

%prep
%bsetup

%build
cd libxml2-%{version}
export LDFLAGS="%_ldflags -flto"
export CFLAGS="%optflags -std=gnu99"
export CXXFLAGS="%cxx_optflags"
export PATH="%{_bindir}:${PATH}"
export PYTHON="%{_bindir}/%{pyname}"

%if %{build_64bit}
CFLAGS="${CFLAGS} %{gcc_opt_sse2} -flto %{gcc_opt_graphite}"
%else
CFLAGS="${CFLAGS} -flto %{gcc_opt_graphite}"
%endif

./configure --prefix=%{_prefix}         \
            --bindir=%{_bindir}         \
            --libdir=%{_libdir}         \
            --mandir=%{_mandir}         \
            --datadir=%{_datadir}       \
            --docdir=%{_docdir}/libxml2-%{version} \
            --sysconfdir=%{_sysconfdir} \
            --with-python=%{_bindir}/%{pyname}    \
            --enable-shared=yes         \
            --disable-static

gmake 

%install
rm -fr %{buildroot}
cd libxml2-%{version}
gmake install DESTDIR=${RPM_BUILD_ROOT}

gzip -9 doc/libxml2-api.xml
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

# multiarch crazyness on timestamp differences or Makefile/binaries for examples
touch -m --reference=$RPM_BUILD_ROOT/%{_includedir}/libxml2/libxml/parser.h $RPM_BUILD_ROOT/%{_bindir}/xml2-config
(cd doc/examples ; make clean ; rm -rf .deps Makefile)
cp AUTHORS NEWS README Copyright TODO ${RPM_BUILD_ROOT}%{_docdir}/libxml2-%{version}
mkdir ${RPM_BUILD_ROOT}%{_docdir}/libxml2-%{version}/python
cp python/TODO python/libxml2class.txt python/tests/*.py doc/*.py doc/python.html ${RPM_BUILD_ROOT}%{_docdir}/libxml2-%{version}/python
rm -f ${RPM_BUILD_ROOT}%{_libdir32}/%{pyname}/site-packages/*.la
mkdir -p ${RPM_BUILD_ROOT}%{_libdir32}/%{pyname}/vendor-packages
mkdir -p ${RPM_BUILD_ROOT}%{_libdir32}/%{pyname}/lib-dynload
mv ${RPM_BUILD_ROOT}%{_libdir32}/%{pyname}/site-packages/*.py* ${RPM_BUILD_ROOT}%{_libdir32}/%{pyname}/vendor-packages
reldir=$(echo %{_libdir} | gsed 's,/$,,;s,/[^/]\+,../,g')%{_lib}
mkdir -p ${RPM_BUILD_ROOT}%{_lib}
(cd ${RPM_BUILD_ROOT}%{_libdir}
 for f in *.so*
 do
   mv ${f} ${reldir}
   ln -s ${reldir}/${f}
 done)

%if %{build_64bit}
mkdir ${RPM_BUILD_ROOT}%{_libdir32}/%{pyname}/lib-dynload/64
mv ${RPM_BUILD_ROOT}%{_libdir32}/%{pyname}/site-packages/*.so ${RPM_BUILD_ROOT}%{_libdir32}/%{pyname}/lib-dynload/64
%else
mv ${RPM_BUILD_ROOT}%{_libdir32}/%{pyname}/site-packages/*.so ${RPM_BUILD_ROOT}%{_libdir32}/%{pyname}/lib-dynload
%endif

rm -rf ${RPM_BUILD_ROOT}%{_libdir32}/%{pyname}/site-packages
rm -rf ${RPM_BUILD_ROOT}%{_gtkdocdir}
rm -rf ${RPM_BUILD_ROOT}%{_docdir}/libxml2-python-%{version}

%clean
rm -fr %{buildroot}

%files
%defattr(-, root, bin)
%{_mandir}/*

%{_lib}/lib*.so*
%{_libdir}/lib*.so*
%{_bindir}/xmllint
%{_bindir}/xmlcatalog
%{_bindir}/xml2-config

%files devel
%defattr(-, root, bin)
%{_includedir}/*
%{_aclocaldir}/libxml.m4
%{_pkgconfigdir}/libxml-2.0.pc

%defattr(0755, root, bin)
%{_libdir}/*.sh
%dir %{_docdir}/libxml2-%{version}

%defattr(-, root, other)
%{_docdir}/libxml2-%{version}/AUTHORS
%{_docdir}/libxml2-%{version}/Copyright
%{_docdir}/libxml2-%{version}/examples
%{_docdir}/libxml2-%{version}/html
%{_docdir}/libxml2-%{version}/NEWS
%{_docdir}/libxml2-%{version}/README
%{_docdir}/libxml2-%{version}/TODO

%files python
%defattr(-, root, bin)
%dir %{_libdir32}/%{pyname}
%dir %{_libdir32}/%{pyname}/vendor-packages
%dir %{_libdir32}/%{pyname}/lib-dynload
%{_libdir32}/%{pyname}/vendor-packages/*
%{_libdir32}/%{pyname}/lib-dynload/*

%dir %{_docdir}/libxml2-%{version}
%dir %{_docdir}/libxml2-%{version}/python

%defattr(-, root, other)
%{_docdir}/libxml2-%{version}/python/*

%changelog


