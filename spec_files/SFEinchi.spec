#
# spec file for package SFEinchi
#
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

Name:			SFEinchi
License:		LGPLv2+
Group:			Development/Libraries
Version:		1.0.2b
Summary:		The IUPAC International Chemical Identifier library
Source:			http://www.iupac.org/inchi/download/inchi102b.zip

URL:			http://www.iupac.org/inchi/
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:		%{_prefix}

%description
The IUPAC International Chemical Identifier (InChITM) is a non-proprietary
identifier for chemical substances that can be used in printed and
electronic data sources thus enabling easier linking of diverse data
compilations. It was developed under IUPAC Project 2000-025-1-800 during
the period 2000-2004. Details of the project and the history of its
progress are available from the project web site.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%prep
%setup -q -c -n %name-%version
%ifarch amd64 sparcv9
cp -pr InChI-1-software-1-02-beta InChI-1-software-1-02-beta-64
%endif

%build
%ifarch amd64 sparcv9
cd InChI-1-software-1-02-beta-64
export CFLAGS="%optflags64"
export CXXFLAGS="%cxx_optflags64"
export LDFLAGS="%_ldflags64"

(cd INCHI_API/gcc_so_makefile
make C_OPTIONS="$CFLAGS -c" LINUX_MAP=-Wl,-M,inchi.map SHARED_LINK="gcc -shared -m64" LINKER="gcc -m64 -s" -j 2 )

cd ..
%endif

cd InChI-1-software-1-02-beta
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags"

(cd INCHI_API/gcc_so_makefile
make C_OPTIONS="$CFLAGS -c" LINUX_MAP=-Wl,-M,inchi.map -j 2 )

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
cd InChI-1-software-1-02-beta-64
mkdir -p $RPM_BUILD_ROOT%{_libdir}/%{_arch64}
mkdir -p $RPM_BUILD_ROOT%{_includedir}/inchi
rm -f INCHI_API/gcc_so_makefile/result/libinchi.so.*.gz
install -p INCHI_API/gcc_so_makefile/result/libinchi.so.* $RPM_BUILD_ROOT%{_libdir}/%{_arch64}
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/libinchi.so.1
(cd $RPM_BUILD_ROOT%{_libdir}/%{_arch64}
 ln -s libinchi.so.* libinchi.so.1
 ln -s libinchi.so.1 libinchi.so
)
sed -i 's/\r//' INCHI_API/INCHI_DLL/inchi_api.h
install -pm644 INCHI_API/INCHI_DLL/inchi_api.h $RPM_BUILD_ROOT%{_includedir}/inchi
sed -i 's/\r//' LICENSE readme.txt
cd ..
%endif

cd InChI-1-software-1-02-beta
rm -f INCHI_API/gcc_so_makefile/result/libinchi.so.*.gz
install -p INCHI_API/gcc_so_makefile/result/libinchi.so.* $RPM_BUILD_ROOT%{_libdir}
rm -f $RPM_BUILD_ROOT%{_libdir}/libinchi.so.1
(cd $RPM_BUILD_ROOT%{_libdir}
 ln -s libinchi.so.* libinchi.so.1
 ln -s libinchi.so.1 libinchi.so
)
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
* Fri Jul 17 2009 - moinakg(at)belenix<dot>org
- Initial spec.
