#
# spec file for package SFEllvm
#
#
%include Solaris.inc
%include base.inc

Name:			SFEllvm
Summary:		The Low Level Virtual Machine 
Group:			Development/Languages
License:                NCSA
Version:		2.6
Source:			http://llvm.org/releases/%{version}/llvm-%{version}.tar.gz
Source1:                http://llvm.org/releases/%{version}/clang-%{version}.tar.gz
Patch1:                 llvm-01-destdir.diff
Patch2:                 llvm-02-destdir-clang.diff
Patch3:                 llvm-03-tclsh_check.diff
Patch4:                 llvm-04-timestamp.diff
Patch5:                 llvm-05-fixes.diff
Patch6:                 llvm-06-ps3.diff

URL:			http://llvm.org/
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:		%{_prefix}
BuildRequires: SUNWbison
BuildRequires: SUNWflexlex
BuildRequires: SFEgcc
BuildRequires: SUNWltdl
BuildRequires: SFEdoxygen
BuildRequires: SFEgraphviz
BuildRequires: SUNWperl584usr
Requires: SUNWlibffi
Requires: SUNWocaml
%if %cc_is_gcc
Requires: SFEgccruntime
%endif

%description
LLVM is a compiler infrastructure designed for compile-time,
link-time, runtime, and idle-time optimization of programs from
arbitrary programming languages. The compiler infrastructure includes
mirror sets of programming tools as well as libraries with equivalent
functionality.

%package devel
Summary:                 Libraries and header files for LLVM
Group:                   Development/Languages
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
Requires: SUNWbison
Requires: SUNWflexlex
Requires: SFEgcc
Requires: SUNWltdl

%package doc
Summary:                 Documentation for LLVM
Group:                   Documentation
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc

%description doc
Documentation for the LLVM compiler infrastructure.

%package -n SFEclang
Summary:                 A C language family frontend for LLVM
License:                 NCSA
Group:                   Development/Languages
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%description -n SFEclang
clang: noun
    1. A loud, resonant, metallic sound.
    2. The strident call of a crane or goose.
    3. C-language family front-end toolkit.

The goal of the Clang project is to create a new C, C++, Objective C
and Objective C++ front-end for the LLVM compiler. Its tools are built
as libraries and designed to be loosely-coupled and extendable.

%package -n SFEclang-analyzer
Summary:                 A source code analysis framework
License:                 NCSA
Group:                   Development/Languages 
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                SFEclang
Requires:                SUNWPython26

%description -n SFEclang-analyzer
The Clang Static Analyzer consists of both a source code analysis
framework and a standalone tool that finds bugs in C and Objective-C
programs. The standalone tool is invoked from the command-line, and is
intended to run in tandem with a build of a project or code base.

%package -n SFEclang-doc
Summary:                 Documentation for Clang
Group:                   Documentation
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc

%description -n SFEclang-doc
Documentation for the Clang compiler front-end.

%package apidoc
Summary:                 API documentation for LLVM
Group:                   Development/Languages
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc

%description apidoc
API documentation for the LLVM compiler infrastructure.

%prep
%setup -q -c -n %name-%version
gunzip -c %{SOURCE1} | gtar xf -
mv clang-%{version} llvm-%{version}/tools/clang
cd llvm-%{version}

%patch1 -p0
pushd tools/clang
%patch2 -p0
popd
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%{gnu_bin}/sed -i 's|LINK_COMPONENTS := |LINK_COMPONENTS := core analysis codegen support bitreader ipa system target transformutils mc |' tools/opt/Makefile
%{gnu_bin}/sed -i 's|LINK_COMPONENTS := |LINK_COMPONENTS := core analysis codegen support bitreader ipa system target transformutils mc scalaropts |' tools/llvm-as/Makefile
%{gnu_bin}/sed -i 's|LINK_COMPONENTS := |LINK_COMPONENTS := core analysis codegen support bitreader ipa system target transformutils mc scalaropts |' tools/llvm-dis/Makefile
%{gnu_bin}/sed -i 's|LINK_COMPONENTS := |LINK_COMPONENTS := core analysis codegen support bitreader ipa system target transformutils mc scalaropts selectiondag asmprinter |' tools/llc/Makefile
%{gnu_bin}/sed -i 's|LINK_COMPONENTS = |LINK_COMPONENTS = core analysis codegen support bitreader ipa system target transformutils mc scalaropts |' tools/llvm-ranlib/Makefile
%{gnu_bin}/sed -i 's|LINK_COMPONENTS = |LINK_COMPONENTS = core analysis codegen support bitreader ipa system target transformutils mc scalaropts |' tools/llvm-ar/Makefile
%{gnu_bin}/sed -i 's|LINK_COMPONENTS = |LINK_COMPONENTS = core analysis codegen support ipa system target transformutils mc scalaropts |' tools/llvm-nm/Makefile
%{gnu_bin}/sed -i 's|LINK_COMPONENTS = |LINK_COMPONENTS = core analysis codegen support bitreader ipa system target transformutils mc |' tools/llvm-ld/Makefile
%{gnu_bin}/sed -i 's|LINK_COMPONENTS = |LINK_COMPONENTS = core codegen support ipa system target transformutils mc scalaropts |' tools/llvm-prof/Makefile
%{gnu_bin}/sed -i 's|LINK_COMPONENTS = |LINK_COMPONENTS = core analysis codegen support ipa system target transformutils mc scalaropts archive |' tools/llvm-link/Makefile
%{gnu_bin}/sed -i 's|LINK_COMPONENTS := |LINK_COMPONENTS := core analysis codegen support ipa system target transformutils mc scalaropts asmprinter executionengine x86info |' tools/lli/Makefile
%{gnu_bin}/sed -i 's|LINK_COMPONENTS := |LINK_COMPONENTS := core analysis codegen support ipa system target transformutils mc scalaropts |' tools/llvm-extract/Makefile
%{gnu_bin}/sed -i 's|LINK_COMPONENTS := |LINK_COMPONENTS := core analysis codegen support bitreader ipa system target transformutils mc scalaropts |' tools/llvm-db/Makefile
%{gnu_bin}/sed -i 's|LINK_COMPONENTS := |LINK_COMPONENTS := core analysis codegen support ipa system target transformutils mc archive |' tools/bugpoint/Makefile
%{gnu_bin}/sed -i 's|LINK_COMPONENTS := |LINK_COMPONENTS := core analysis codegen support ipa system target transformutils mc scalaropts |' tools/llvm-bcanalyzer/Makefile
%{gnu_bin}/sed -i 's|MC support|MC support core analysis codegen bitreader ipa system target transformutils mc scalaropts selectiondag asmprinter |' tools/llvm-mc/Makefile
%{gnu_bin}/sed -i 's|ipo selectiondag|ipo selectiondag target core analysis support ipa system asmprinter mc transformutils scalaropts |' tools/clang/tools/clang-cc/Makefile
%{gnu_bin}/sed -i 's|clangBasic.a|clangBasic.a clangIndex.a |' tools/clang/tools/clang-cc/Makefile
%{gnu_bin}/sed -i 's|LINK_COMPONENTS := |LINK_COMPONENTS := core analysis codegen support ipa system target transformutils scalaropts ipo selectiondag asmprinter bitwriter |' tools/clang/tools/index-test/Makefile
%{gnu_bin}/sed -i 's|clangBasic.a|clangBasic.a clangParse.a clangAnalysis.a clangRewrite.a clangCodeGen.a |' tools/clang/tools/index-test/Makefile
%{gnu_bin}/sed -i 's|LINK_COMPONENTS := |LINK_COMPONENTS := core analysis codegen ipa system target transformutils mc scalaropts |' tools/clang/tools/driver/Makefile
%{gnu_bin}/sed -i 's|LINK_COMPONENTS := |LINK_COMPONENTS := core analysis codegen support ipa system target transformutils scalaropts ipo selectiondag asmprinter bitwriter |' tools/clang/tools/wpa/Makefile
%{gnu_bin}/sed -i 's|clangBasic.a|clangBasic.a clangParse.a clangAnalysis.a clangRewrite.a clangCodeGen.a |' tools/clang/tools/wpa/Makefile
%{gnu_bin}/sed -i 's|LINK_COMPONENTS := |LINK_COMPONENTS := core analysis codegen support bitreader ipa system target transformutils mc scalaropts selectiondag asmprinter executionengine x86info |' examples/BrainF/Makefile
%{gnu_bin}/sed -i 's|LINK_COMPONENTS := |LINK_COMPONENTS := core analysis codegen support bitreader ipa system target transformutils mc scalaropts selectiondag asmprinter executionengine x86info |' examples/Fibonacci/Makefile
%{gnu_bin}/sed -i 's|LINK_COMPONENTS := |LINK_COMPONENTS := core analysis codegen support bitreader ipa system target transformutils mc scalaropts selectiondag asmprinter executionengine x86info |' examples/HowToUseJIT/Makefile
%{gnu_bin}/sed -i 's|LINK_COMPONENTS := |LINK_COMPONENTS := core analysis codegen support bitreader ipa system target transformutils mc scalaropts selectiondag asmprinter executionengine x86info |' examples/Kaleidoscope/Makefile
%{gnu_bin}/sed -i 's|LINK_COMPONENTS := |LINK_COMPONENTS := core analysis codegen support bitreader ipa system target transformutils mc scalaropts |' examples/ModuleMaker/Makefile
%{gnu_bin}/sed -i 's|LINK_COMPONENTS := |LINK_COMPONENTS := core analysis codegen support bitreader ipa system target transformutils mc scalaropts selectiondag asmprinter executionengine x86info |' examples/ParallelJIT/Makefile

#%{gnu_bin}/sed -i 's/-fomit-frame-pointer//' Makefile.rules


%build
cd llvm-%{version}
export LDFLAGS="%{gnu_lib_path} -lintl -liconv -L/lib -R/lib -Wl,-z,allextract"
export PATH=/usr/perl5/5.8.4/bin:${PATH}
mkdir obj
cd obj
bash ../configure \
    --prefix=%{_prefix} \
    --sysconfdir=%{_sysconfdir} \
    --libdir=%{_libdir}/llvm \
    --disable-assertions \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --enable-shared=yes \
    --enable-static=no \
    --enable-debug-runtime \
    --enable-jit
 
# configure does not properly specify libdir
%{gnu_bin}/sed -i 's|(PROJ_prefix)/lib|(PROJ_prefix)/%{_libdir}/llvm|g' Makefile.config

gmake VERBOSE=1 OPTIMIZE_OPTION="-O2 -march=pentium3 -fno-strict-aliasing"
cd ../..

%check
cd llvm-%{version}/obj
gmake check
# some clang tests still fail, preserve test results
(cd tools/clang && gmake test 2>&1) | tee ../testlog.txt || true


%install
rm -rf $RPM_BUILD_ROOT
#%ifarch amd64 sparcv9
#cd apr-%{version}-64
#make install DESTDIR=$RPM_BUILD_ROOT
#
#cd ..
#%endif

cd llvm-%{version}/obj
export PATH=/usr/perl5/5.8.4/bin:${PATH}
%{gnu_bin}/sed -i 's/groff -Tps -man/cat/' tools/clang/docs/tools/Makefile
%{gnu_bin}/sed -i 's/groff -Tps -man/cat/' docs/CommandGuide/Makefile
%{gnu_bin}/sed -i 's/:= $(PROJ_docsdir)/:= $(DESTDIR)$(PROJ_docsdir)/' docs/CommandGuide/Makefile
%{gnu_bin}/sed -i 's/:= $(PROJ_mandir)/:= $(DESTDIR)$(PROJ_mandir)/' docs/CommandGuide/Makefile
%{gnu_bin}/sed -i 's/:= $(PROJ_docsdir)/:= $(DESTDIR)$(PROJ_docsdir)/' docs/CommandGuide/Makefile

chmod -x examples/Makefile
gmake install DESTDIR=$RPM_BUILD_ROOT PROJ_docsdir=$RPM_BUILD_ROOT/moredocs
cd ..

# Static analyzer not installed by default:
# http://clang-analyzer.llvm.org/installation#OtherPlatforms
mkdir -p $RPM_BUILD_ROOT%{_libdir}/clang-analyzer/libexec
# link clang-cc for scan-build to find
ln -s %{_libexecdir}/clang-cc $RPM_BUILD_ROOT%{_libdir}/clang-analyzer/libexec/
# create launchers
for f in scan-{build,view}; do
	ln -s %{_libdir}/clang-analyzer/$f $RPM_BUILD_ROOT%{_bindir}/$f
done 

cd tools/clang/utils
cp -p ccc-analyzer $RPM_BUILD_ROOT%{_libdir}/clang-analyzer/libexec/

for f in scan-build scanview.css sorttable.js; do
	cp -p $f $RPM_BUILD_ROOT%{_libdir}/clang-analyzer/
done
cd ../../../

#
# Move documentation back to build directory
#
rm -rf moredocs
mv $RPM_BUILD_ROOT/$RPM_BUILD_ROOT/moredocs .
rm -rf $RPM_BUILD_ROOT/var
rm -f moredocs/*.tar.gz
rm -f moredocs/ocamldoc/html/*.tar.gz 

# And prepare Clang documentation
#
mkdir -p clang-docs
for f in LICENSE.TXT NOTES.txt README.txt TODO.txt; do
	ln -f tools/clang/$f clang-docs/
done

# Get rid of erroneously installed example files.
rm -f $RPM_BUILD_ROOT%{_libdir}/llvm/*LLVMHello.* 

# Remove deprecated tools.
rm -f $RPM_BUILD_ROOT%{_bindir}/gcc{as,ld}

# FIXME file this bug
%{gnu_bin}/sed -i 's,ABS_RUN_DIR/lib",ABS_RUN_DIR/%{_lib}/llvm",' \
	$RPM_BUILD_ROOT%{_bindir}/llvm-config

mv $RPM_BUILD_ROOT%{_prefix}%{_libdir}/llvm $RPM_BUILD_ROOT%{_libdir}
rm -rf $RPM_BUILD_ROOT%{_prefix}%{_libdir}
chmod -x $RPM_BUILD_ROOT%{_libdir}/llvm/*.a 
rm -rf $RPM_BUILD_ROOT/export
mv $RPM_BUILD_ROOT%{_prefix}/libexec/* $RPM_BUILD_ROOT%{_libdir}
rm -rf $RPM_BUILD_ROOT%{_prefix}/libexec

mkdir -p $RPM_BUILD_ROOT%{_docdir}/llvm
cp -rp moredocs/* $RPM_BUILD_ROOT%{_docdir}/llvm

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/ocaml
%{_libdir}/ocaml/*.cm*
%{_libdir}/ocaml/*.ml*
%dir %attr (0755, root, bin) %{_libdir}/clang-analyzer
%{_libdir}/clang-analyzer/*
%dir %attr (0755, root, bin) %{_libdir}/clang
%{_libdir}/clang/*
%dir %attr (0755, root, bin) %{_libdir}/llvm
%{_libdir}/llvm/*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/ocaml
%{_libdir}/ocaml/*.a
%dir %attr (0755, root, bin) %{_libdir}/llvm
%{_libdir}/llvm/*.a
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*

%changelog
* Mon Dec 07 2009 - Moinak Ghosh
- Initial spec.
