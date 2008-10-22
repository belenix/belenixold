#
# spec file for package SFEmrxvt
#
# includes module(s): Mrxvt
#
%include Solaris.inc

%define src_name	gnuchess
%define src_version	5.07
%define pkg_release	1

SUNW_Pkg: %{src_name}
SUNW_ProdVers:	%{src_version}
SUNW_BaseDir:	/

Name:                    gnuchess
Summary:                 gnuchess - The GNU Chess program
Version:                 %{src_version}
Source:                  http://ftp.gnu.org/pub/gnu/chess/%{src_name}-%{src_version}.tar.gz
URL:                     http://ftp.gnu.org/pub/gnu/chess/
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %{src_name}-%version

%build
./configure --prefix=%{_prefix} \
            --mandir=%{_mandir} \
            --libdir=%{_libdir} \
            --libexecdir=%{_libexecdir} \
            --infodir=%{_infodir} \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir}
make

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, sys)

%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%changelog
* Sun Oct 19 2008 - moinak.ghosh@sun.com
- Initial gnuchess spec file

