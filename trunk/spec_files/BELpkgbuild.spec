#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include base.inc

Name:                BELpkgbuild
Summary:             An rpmbuild-like tool for building Solaris packages (modified for BeleniX)
Version:             1.3.3
License:             GPL
Source:              http://www.belenix.org/binfiles/pkgbuild-%{version}.tar.bz2
URL:                 http://pkgbuild.sourceforge.net/

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWperl584core

%prep
%setup -q -c -n %name-%version

%build
echo "Done"

%install
rm -rf $RPM_BUILD_ROOT
cp -r . $RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT/.pkgbuild*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%changelog
* Sun Aug 16 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Initial version.
