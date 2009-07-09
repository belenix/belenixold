#
# spec file for package SUNWxdg-utils
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: dkenny
#

%include Solaris.inc

Name:                SUNWxdg-utils
Summary:             The Portland Project's desktop integration tools
Version:             1.0.2
Source:              http://portland.freedesktop.org/download/xdg-utils-%{version}.tgz
# date:2008-02-13 owner:dkenny type:bug
Patch1:              xdg-utils-01-bash.diff
# date:2008-02-13 owner:dkenny type:bug
Patch2:              xdg-utils-02-path.diff
# date:2008-02-19 owner:dkenny type:bug
Patch3:              xdg-utils-03-nawk.diff
# date:2009-02-19 owner:mattman type:branding
Patch4:              xdg-utils-04-manpages.diff
SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWbash

%prep
%setup -q -n xdg-utils-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

./configure --prefix=%{_prefix}  \
            --bindir=%{_bindir} \
            --mandir=%{_mandir} 

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%{_mandir}
%dir %attr (0755, root, sys) %{_datadir}
%doc LICENSE scripts/README tests/debug/README
%doc(bzip2) ChangeLog README tests/README
%dir %attr (0755, root, other) %{_datadir}/doc

%changelog
* Thu Feb 02 2009 - matt.keenn@sun.com
- Add manpage patch, addds attributes to all delivered manpages
* Tue Sep 16 2008 - matt.keenn@sun.com
- Update copyright
* Thu Mar 15 2008 - lin.ma@sun.com
- Add SUNWbash dependency.
* Wed Feb 19 2008 - darren.kenny@sun.com
- Add patch to use nawk instead of awk
* Wed Feb 13 2008 - darren.kenny@sun.com
- Add patch to prepend X dirs to PATH.
* Tue Feb 12 2008 - dermot.mccluskey@sun.com
- initial version
