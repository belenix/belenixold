#
# spec file for package SFExlincity
#

%include Solaris.inc
Name:                    SFExlincity
Summary:                 xlincity - Simulation game based on opensourced components of S*mc*ty. 
Group:                   Game/Simulation
URL:                     http://lincity.sourceforge.net 
Version:                 1.12.1
Source:                  %{sf_download}/lincity/lincity-%{version}.tar.gz 
Patch1:			 xlincity-01-solaris.diff
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc


%prep
%setup -q  -n lincity-%{version} 
find ./intl -name \*.c -exec dos2unix {} {} \;
find ./intl -name \*.h -exec dos2unix {} {} \;
find ./intl -name \*.charset -exec dos2unix {} {} \;
%patch1 -p1

%build
export LDFLAGS="%{gnu_lib_path}"
./configure --prefix=%{_prefix}
gmake

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/charset.alias
mv ${RPM_BUILD_ROOT}%{_prefix}/man ${RPM_BUILD_ROOT}%{_mandir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%dir %attr (0755, root, bin) /usr/bin
/usr/bin/xlincity
%dir %attr (0755, root, sys) /usr/share
/usr/share/lincity/*

%dir %attr (0755, root, bin) /usr/share/man
%dir %attr (0755, root, bin) /usr/share/man/man6
/usr/share/man/man6/lincity.6

%defattr(-, root, other)
/usr/share/locale/ca/LC_MESSAGES/lincity.mo
/usr/share/locale/it/LC_MESSAGES/lincity.mo

%changelog
* Mon Nov 02 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Pulled in with mods from SFE repo.
* Wed Jan 23 2008 - Brian Nitz - <brian dot nitz at sun dot com> 
- Initial version.
