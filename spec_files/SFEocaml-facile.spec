#
# spec file for package SFEocaml-facile
#
#
%include Solaris.inc
%include base.inc

Name:			SFEocaml-facile
License:		LGPLv2+
Group:			Development/Libraries
Version:		1.1
Summary:		OCaml library for constraint programming
Source:			http://www.recherche.enac.fr/opti/facile/distrib/facile-%{version}.tar.gz
Patch1:                 ocaml-facile-01-makefile.diff

URL:			http://www.recherche.enac.fr/opti/facile/
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:		%{_prefix}
Requires:      SUNWocaml
Requires:      SFEocaml-findlib
BuildRequires: SFEocaml-findlib-devel

%description
FaCiLe is a constraint programming library on integer and integer set finite
domains written in OCaml.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
Requires: SFEocaml-findlib-devel

%prep
%setup -q -c -n %name-%version
cd facile-%{version}
%patch1 -p1
cd ..

%build
cd facile-%{version}
./configure --faciledir $RPM_BUILD_ROOT%{_libdir}/ocaml/facile
make


%install
rm -rf $RPM_BUILD_ROOT
cd facile-%{version}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/ocaml
make install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/ocaml
%dir %attr (0755, root, bin) %{_libdir}/ocaml/facile
%{_libdir}/ocaml/facile/facile.cmi
%{_libdir}/ocaml/facile/facile.cma

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/ocaml
%dir %attr (0755, root, bin) %{_libdir}/ocaml/facile
%{_libdir}/ocaml/facile/*.a
%{_libdir}/ocaml/facile/*.cmxa
%{_libdir}/ocaml/facile/*.mli

%changelog
* Fri Jul 17 2009 - moinakg(at)belenix<dot>org
- Initial spec.
