#
# spec file for package SFEocaml-findlib
#
#
%include Solaris.inc
%include base.inc

Name:			SFEocaml-findlib
License:		BSD
Group:			Development/Libraries
Version:		1.1
Summary:		Objective CAML package manager and build helper
Source:			http://download.camlcity.org/download/findlib-%{version}.tar.gz

URL:			http://projects.camlcity.org/projects/findlib.html
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:		/
Requires:      SUNWocaml
BuildRequires: SUNWgm4
BuildRequires: SFEgawk

%description
Objective CAML package manager and build helper.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            /
%include default-depend.inc
Requires: %{name}
Requires: SUNWgm4
Requires: SFEgawk

%prep
%setup -q -c -n %name-%version
cd findlib-%{version}
cd ..

%build
cd findlib-%{version}
ocamlc -version
ocamlc -where
(cd tools/extract_args && make)
tools/extract_args/extract_args -o src/findlib/ocaml_args.ml ocamlc ocamlcp ocamlmktop ocamlopt ocamldep ocamldoc ||:
cat src/findlib/ocaml_args.ml
./configure \
    -config %{_sysconfdir}/ocamlfind.conf \
    -bindir %{_bindir} \
    -sitelib "`ocamlc -where`" \
    -mandir %{_mandir} \
    -with-toolbox

make all
make opt
rm doc/guide-html/TIMESTAMP

%install
rm -rf $RPM_BUILD_ROOT
cd findlib-%{version}
mkdir -p $RPM_BUILD_ROOT%{_bindir}
make install prefix=$RPM_BUILD_ROOT OCAMLFIND_BIN=$RPM_BUILD_ROOT%{_bindir}
mv $RPM_BUILD_ROOT/$RPM_BUILD_ROOT%{_bindir}/* $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_docdir}/ocaml-findlib
cp -r doc/* $RPM_BUILD_ROOT%{_docdir}/ocaml-findlib
cp LICENSE $RPM_BUILD_ROOT%{_docdir}/ocaml-findlib
rm -rf $RPM_BUILD_ROOT/var

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/ocaml
%{_libdir}/ocaml/topfind
%{_libdir}/ocaml/num-top
%{_libdir}/ocaml/findlib/META
%{_libdir}/ocaml/findlib/topfind.cmi
%{_libdir}/ocaml/findlib/findlib_top.cma
%{_libdir}/ocaml/findlib/findlib.cmi
%{_libdir}/ocaml/findlib/fl_metascanner.cmi
%{_libdir}/ocaml/findlib/findlib.cma
%{_libdir}/ocaml/findlib/fl_package_base.cmi
%{_libdir}/ocaml/unix
%{_libdir}/ocaml/threads
%{_libdir}/ocaml/num
%{_libdir}/ocaml/dynlink
%{_libdir}/ocaml/dbm
%{_libdir}/ocaml/graphics
%{_libdir}/ocaml/bigarray
%{_libdir}/ocaml/str
%{_libdir}/ocaml/stdlib
%{_libdir}/ocaml/labltk
%{_libdir}/ocaml/camlp4

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*
%dir %attr (0755, root, sys) %{_sysconfdir}
%config(noreplace) %{_sysconfdir}/ocamlfind.conf

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/ocaml
%dir %attr (0755, root, bin) %{_libdir}/ocaml/findlib
%{_libdir}/ocaml/findlib/*.a
%{_libdir}/ocaml/findlib/*.cmxa
%{_libdir}/ocaml/findlib/*.mli
%{_libdir}/ocaml/findlib/Makefile.config
%{_libdir}/ocaml/findlib/make_wizard
%{_libdir}/ocaml/findlib/make_wizard.pattern

%changelog
* Fri Jul 17 2009 - moinakg(at)belenix<dot>org
- Initial spec.
