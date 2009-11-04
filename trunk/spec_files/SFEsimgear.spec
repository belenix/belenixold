#
# spec file for package SFESimGear.spec
# Gilles Dauphin
#
# includes module(s): SimGear
#
%include Solaris.inc

%define src_name	SimGear
%define src_url		ftp://ftp.de.simgear.org/pub/simgear/Source
#ftp://ftp.de.simgear.org/pub/simgear/Source/SimGear-1.0.0.tar.gz
#ftp://ftp.simgear.org/pub/simgear/Source/SimGear-1.0.0.tar.gz

Name:                   SFESimGear
Summary:                Simulator Construction Tools
Version:                1.9.1
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:		SFEopenal-devel
Requires:		SFEopenal
BuildRequires:		SFEfreealut-devel
Requires:		SFEfreealut
Requires:		SFEplib
Requires:		SFEosg
BuildRequires:		SFEosg-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
%setup -q -c -n  %{name}

%build
cd %{src_name}-%{version}
export CPPFLAGS="-I%{_includedir}/boost/gcc4"
export LDFLAGS="-L%{_libdir}/boost/gcc4 -R%{_libdir}/boost/gcc4 %{gnu_lib_path}"
/bin/bash ./configure CONFIG_SHELL=/bin/bash --prefix=%{_prefix}
make

%install
rm -rf $RPM_BUILD_ROOT
cd %{src_name}-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
# TODO: make shared libs
#rm $RPM_BUILD_ROOT/%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr(0755,root,bin) %{_libdir}
%{_libdir}/lib*.a*

%files devel
%defattr (-, root, bin)
%{_includedir}

%changelog
* Mon Nov 02 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Pulled in with mods from SFE repo.
* Mon Nov 17 2008 - dauphin@enst.fr
- Initial version
