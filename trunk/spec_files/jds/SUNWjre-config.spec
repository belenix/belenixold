#
# spec file for package SUNWjre-config
#
# includes module(s): j2re-config
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: dermot
#
%include Solaris.inc

%use j2re_int = j2re-integration.spec

%define plugin_dir %{_libdir}/firefox/plugins
%define plugin_file libnpjp2.so

%ifarch i386
%define myarch i386
%endif

%ifarch sparc
%define myarch sparc
%endif


Name:                    SUNWjre-config
Summary:                 Java runtime integration
Version:                 1.0
SUNW_Category: 		 JDS,system,%{jds_version}
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:           SUNWfirefox
Requires:                SUNWj6rt

%package plugin
Summary:                 %{summary} - plugin
SUNW_Category: 		 JDS,system,%{jds_version}
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SUNWfirefox
Requires: SUNWj5rt

%prep
rm -rf %name-%version
mkdir %name-%version
%j2re_int.prep -d %name-%version


%install
cd %{_builddir}/%name-%version/j2re-integration

#setup mozilla plugin
#create dummy plugin
install --mode=755 -d ${RPM_BUILD_ROOT}%{_prefix}/java/jre/lib/%{myarch}/
touch ${RPM_BUILD_ROOT}%{_prefix}/java/jre/lib/%{myarch}/%{plugin_file}
install --mode=755 -d ${RPM_BUILD_ROOT}%{plugin_dir}
cd ${RPM_BUILD_ROOT}%{plugin_dir}
mkdir -p  ../../../java/jre/lib/%{myarch}
touch  ../../../java/jre/lib/%{myarch}/%{plugin_file}
ln -s ../../../java/jre/lib/%{myarch}/%{plugin_file} .
rm  ../../../java/jre/lib/%{myarch}/%{plugin_file}

rm -rf $RPM_BUILD_ROOT%{_prefix}/java

%clean
rm -rf $RPM_BUILD_ROOT


%files

%files plugin
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{plugin_dir}/%{plugin_file}


%changelog
* Wed Dec 10 2008 - dermot.mccluskey@sun.com
- 6782196, use new Java plugin
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Fri Jun 09 2006 - dermot.mccluskey@sun.com
- 6349214: remove files installed in java 1.4.2 dir /usr/j2se
  results in SUNWjre-config being empty - will completely remove pkg
  once ARC fasttrack is complete
- Update %install and %files as base spec file has removed multiple files.
* Thu Apr 13 2006 - dave.lin@sun.com
- changed firefox libdir to "/usr/lib"
* Thu Oct 14 2004 - laca@sun.com
- change CATEGORY to JDS3,system
* Tue Aug 17 2004 - laca@sun.com
- added SUNWj5rt dependency
* Fri Aug 06 2004 - takao.fujiwara@sun.com
- Added JavaIM.directory
* Tue Jul 15 2004 - dermot.mccluskey@sun.com
- mozilla's _prefix has changed to /usr/sfw

* Tue Jul 13 2004 - damien.carbery@sun.com
- Set perms for /usr/share/applications again.
* Mon Jul 12 2004 - damien.carbery@sun.com
- Unset perms for /usr/share/applications.
* Sat Jul 10 2004 - damien.carbery@sun.com
- Set perms for /usr/share/applications.
* Sat Jun 26 2004  shirley.woo@sun.com
- Changed install location to /usr/...
* Tue Jun 22 2004 - dermot.mccluskey@sun.com
- remove hardcoded /opt/jds
* Mon Jun 21 2004 - dermot.mccluskey@sun.com
- add Java Instant Messanger .desktop files
