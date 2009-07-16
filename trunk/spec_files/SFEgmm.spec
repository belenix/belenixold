#
# spec file for package SFEgmm
#
#
%include Solaris.inc
%include base.inc

Name:			SFEgmm
License:		LGPLv2+
Group:			Development/Libraries
Version:		3.1
Summary:		A generic C++ template library for sparse, dense and skyline matrices
Source:			http://download.gna.org/getfem/stable/gmm-%{version}.tar.gz

URL:			http://home.gna.org/getfem/gmm_intro
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:		%{_prefix}
Requires: SFEgccruntime
BuildRequires: SFEgcc

%description
Gmm++ is a generic C++ template library for sparse, dense and
skyline matrices. It is built as a set of generic algorithms
(mult, add, copy, sub-matrices, dense and sparse solvers ...)
for any interfaced vector type or matrix type. It can be viewed
as a glue library allowing cooperation between several vector
and matrix types. 

%prep
%setup -q -c -n %name-%version

%build
cd gmm-%{version}
export CFLAGS="%optflags -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"
export LD=/usr/ccs/bin/ld
export LDFLAGS="%_ldflags -L/lib -R/lib -L$RPM_BUILD_ROOT%{_libdir}"
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --enable-shared \
    --with-pic \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --enable-reentrant
 
#%patch1 -p1

make -j 2

%install
rm -rf $RPM_BUILD_ROOT
cd gmm-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Thu Jul 16 2009 - moinakg(at)belenix<dot>org
- Initial spec.
