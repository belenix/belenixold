#
# spec file for package lua scripting language
#
%include Solaris.inc
%define source_name tolua++
%define solib tolua++-5.1

Name:                    SFEtoluapp
Summary:                 A tool to integrate C/C++ code with Lua
Version:                 1.0.92
Group:                   Development/Tools
License:                 Freely redistributable without restriction
Source:                  http://www.codenix.com/~tolua/tolua++-%{version}.tar.bz2
URL:                     http://www.codenix.com/~tolua/
Patch1:                  toluapp-01-makeso.diff
Patch2:                  toluapp-02-gcc43.diff

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{source_name}-%{version}-build
%include default-depend.inc
Requires: SFElua
BuildRequires: SFEscons

%description
tolua++ is an extended version of tolua, a tool to integrate C/C++ code with
Lua. tolua++ includes new features oriented to C++ 

%package devel
Summary:                 Development files for tolua++
Group:                   Development/Libraries
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{source_name}-%{version}-build
Requires: %{name}
Requires: SFEscons

%prep
%setup -q -n %{source_name}-%{version}
%patch1 -p1
%patch2 -p1
%{gnu_bin}/sed -i 's/\r//' doc/%{source_name}.html

%build
scons -Q CC="${CC}" CCFLAGS="%{optflags} -I%{_includedir}" tolua_lib=%{solib} 
#Recompile the exe without the soname. An ugly hack.
#gcc -o bin/%{name} src/bin/tolua.o src/bin/toluabind.o -Llib -l%{solib} -llua -ldl -lm

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir $RPM_BUILD_ROOT%{_libdir}
mkdir $RPM_BUILD_ROOT%{_includedir}
ginstall -m0755 bin/%{source_name} $RPM_BUILD_ROOT%{_bindir}
ginstall -m0755 lib/lib%{solib}.so $RPM_BUILD_ROOT%{_libdir}
ginstall -m0644 include/%{source_name}.h $RPM_BUILD_ROOT%{_includedir}
mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{source_name}
cp -rp doc/* $RPM_BUILD_ROOT%{_docdir}/%{source_name}

cd $RPM_BUILD_ROOT%{_libdir}
ln -s lib%{solib}.so libtolua++.so 

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%doc %{_docdir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Mon Nov 30 2009 - Moinak Ghosh
- Initial version

