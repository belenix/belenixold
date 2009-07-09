#
# spec file for package j2re-integration
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: dermot
#
Name:         		j2re-integration
License:      		GPL
Group:        		Development/Tools
BuildArchitectures:     noarch
Version:      		0.0.3
Release:      		269
Distribution: 		Java Desktop System
Vendor:       		Sun Microsystems, Inc.
Summary:      		Java integration
Source:			font.properties.zh_CN.Sun
Source1:		font.properties.zh_CN_UTF8.Sun
Source2:		font.properties.zh_HK.Sun
Source3:		font.properties.zh_HK_UTF8.Sun
Source4:		font.properties.zh_TW.Sun
Source5:		font.properties.zh_TW_UTF8.Sun
Source6:                javaws.mime
Source7:                javaws.keys
Source8:                javaws.applications
URL:          		http://www.sun.com
BuildRoot:    		%{_tmppath}/%{name}-%{version}-build

%define plugin_dir %{_libdir}/mozilla/plugins
%define j2re jdk1.5.0_03
%define j2re_dir %{_prefix}/java/%{j2re}

Requires:               jdk >= 1.5.0
PreReq:                 jdk
BuildRequires:          jdk

%description
Java integration.

%prep
%setup -T -c -n j2re-integration
cp %SOURCE0 .
cp %SOURCE1 .
cp %SOURCE2 .
cp %SOURCE3 .
cp %SOURCE4 .
cp %SOURCE5 .
cp %SOURCE6 .
cp %SOURCE7 .
cp %SOURCE8 .



%install
install --mode=755 -d ${RPM_BUILD_ROOT}%{j2re_dir}/lib
install --mode=644 font.properties.zh_CN.Sun ${RPM_BUILD_ROOT}%{j2re_dir}/lib/font.properties.zh_CN.Sun.new
install --mode=644 font.properties.zh_CN_UTF8.Sun ${RPM_BUILD_ROOT}%{j2re_dir}/lib/font.properties.zh_CN_UTF8.Sun.new
install --mode=644 font.properties.zh_HK.Sun ${RPM_BUILD_ROOT}%{j2re_dir}/lib/font.properties.zh_HK.Sun
install --mode=644 font.properties.zh_HK_UTF8.Sun ${RPM_BUILD_ROOT}%{j2re_dir}/lib/font.properties.zh_HK_UTF8.Sun
install --mode=644 font.properties.zh_TW.Sun ${RPM_BUILD_ROOT}%{j2re_dir}/lib/font.properties.zh_TW.Sun.new
install --mode=644 font.properties.zh_TW_UTF8.Sun ${RPM_BUILD_ROOT}%{j2re_dir}/lib/font.properties.zh_TW_UTF8.Sun.new
install -d ${RPM_BUILD_ROOT}/usr/share/mime-info
install --mode=644 javaws.mime ${RPM_BUILD_ROOT}/usr/share/mime-info/javaws.mime
install --mode=644 javaws.keys ${RPM_BUILD_ROOT}/usr/share/mime-info/javaws.keys
install -d ${RPM_BUILD_ROOT}/usr/share/application-registry
install --mode=644 javaws.applications ${RPM_BUILD_ROOT}/usr/share/application-registry/javaws.applications

#Setup relative symlinks

#Link j2redefault to jre sub-dir of JDK install dir
install --mode=755 -d ${RPM_BUILD_ROOT}%{_prefix}/java/%{j2re}
cd ${RPM_BUILD_ROOT}%{_prefix}/java
ln -s %{j2re}/jre j2redefault

#link the java program, using a dummy file to keep ln happy
install --mode=755 -d ${RPM_BUILD_ROOT}%{_prefix}/java/%{j2re}/bin
touch ${RPM_BUILD_ROOT}%{_prefix}/java/%{j2re}/bin/java
touch ${RPM_BUILD_ROOT}%{_prefix}/java/%{j2re}/bin/javac
touch ${RPM_BUILD_ROOT}%{_prefix}/java/%{j2re}/bin/javaws
install --mode=755 -d ${RPM_BUILD_ROOT}%{_bindir}
cd ${RPM_BUILD_ROOT}%{_bindir}
ln -s ../java/j2redefault/bin/java java
ln -s ../java/%{j2re}/bin/javac javac
ln -s ../java/%{j2re}/bin/javaws javaws

#setup mozilla plugin
#create dummy plugin
install --mode=755 -d ${RPM_BUILD_ROOT}%{_prefix}/java/%{j2re}/plugin/i386/ns7/
touch ${RPM_BUILD_ROOT}%{_prefix}/java/%{j2re}/plugin/i386/ns7/libjavaplugin_oji.so
install --mode=755 -d ${RPM_BUILD_ROOT}%{plugin_dir}
cd ${RPM_BUILD_ROOT}%{plugin_dir}
ln -s ../../../java/j2redefault/plugin/i386/ns7/libjavaplugin_oji.so libjavaplugin_oji.so
#Remove 0 sized dummy files
rm $RPM_BUILD_ROOT%{j2re_dir}/bin/java
rm $RPM_BUILD_ROOT%{_prefix}/java/%{j2re}/bin/javac
rm $RPM_BUILD_ROOT%{_prefix}/java/%{j2re}/bin/javaws
rm $RPM_BUILD_ROOT%{j2re_dir}/plugin/i386/ns7/libjavaplugin_oji.so

%clean
rm -rf $RPM_BUILD_ROOT

%post
#Move the originals out of the way and link our ones in
for file in font.properties.zh_CN.Sun font.properties.zh_CN_UTF8.Sun font.properties.zh_TW.Sun font.properties.zh_TW_UTF8.Sun
do
	if [ -f %{j2re_dir}/lib/$file ]; then
		#If it is a symlink remove it, otherwise back it up.
		if [ ! -L %{j2re_dir}/lib/$file ]; then
			mv %{j2re_dir}/lib/$file %{j2re_dir}/lib/$file.original
		else
			rm %{j2re_dir}/lib/$file
		fi
	fi
	if [ ! -f %{j2re_dir}/lib/$file ]; then
		ln -s %{j2re_dir}/lib/$file.new %{j2re_dir}/lib/$file
	fi
done

%preun
if [ $1 -eq 0 ]; then
	#we are uninstalling, not upgrading
	for file in font.properties.zh_CN.Sun font.properties.zh_CN_UTF8.Sun font.properties.zh_TW.Sun font.properties.zh_TW_UTF8.Sun
	do
		if [ -L %{j2re_dir}/lib/$file ]; then
			rm %{j2re_dir}/lib/$file
		fi
		if [ -f %{j2re_dir}/lib/$file.original ]; then
			mv %{j2re_dir}/lib/$file.original %{j2re_dir}/lib/$file
		fi
	done
fi

%files
%defattr(-, root, root)
%{_bindir}/java
%{_bindir}/javac
%{_bindir}/javaws
%{_prefix}/java/j2redefault
%{_prefix}/share/mime-info/*
%{_prefix}/share/application-registry/*
%{j2re_dir}/lib/font.properties.*
%{plugin_dir}/libjavaplugin_oji.so

%changelog
* Fri Jun 02 2006 - glynn.foster@sun.com
- Remove the Java IM menu entries.

* Mon May 09 2005 - dermot.mccluskey@sun.com
- New jdk (1.5.0_03)

* Fri Jan 14 2005 - damien.carbery@sun.com
- Fix 5108782: Add symlinks for javac (for Netbeans) and javaws.

* Wed Sep 15 2004 - dermot.mccluskey@sun.com
- new install dir for JDK 1.5.0

* Mon Aug 23 2004 - dermot.mccluskey@sun.com
- removed double entry for vfolders/* in %files

* Fri Aug 06 2004 - takao.fujiwara@sun.com
- Added JavaIM.directory

* Fri Jul 09 2004 - niall.power@sun.com
- Dependency on jdk=1.5.0 breaks with jdk-1.5.0-beta3
  allow more flexability by specifying jdk >= 1.5.0

* Fri Jul 09 2004 - niall.power@sun.com
- too much crack going on here. tidy up for rpm4

* Sun May 30 2004 - dermot.mccluskey@sun.com
- new JDK

* Fri May 28 2004 - dermot.mccluskey@sun.com
- fixed typo in moz plugin lib

* Fri May 28 2004 - dermot.mccluskey@sun.com
- changed location of java plugin lib for jdk 1.5.0

* Fri Apr 30 2004 - dermot.mccluskey@sun.com
- link j2redefault to the ./jre subdir under j2sdk 1.5.0

* Tue Apr 20 2004 - dermot.mccluskey@sun.com
- switched from jre 1.4.2_04 to j2sdk 1.5.0

* Mon Jan 19 2004 - stephen.browne@sun.com
- Rev'd J2re to _04

* Thu Dec 11 2003 - stephen.browne@sun.com
- Added installation of Java IM Demo menu entries

* Thu Oct 02 2003 - stephen.browne@sun.com
- Bumped j2re version

* Thu Sep 25 2003 - stephen.browne@sun.com
- Added jnlp mimetype and javaws application registration

* Fri Sep 19 2003 - michael.twomey@sun.com
- Create j2redefault symlinks in %install section instead of %post
- Moved postun action to a preun
- Tightened up post and preun actions to check for files before changing them.

* Fri Sep 05 2003 - michael.twomey@sun.com
- Moved j2re symlinking to post/postun actions.
- Added Chinese font.properties files for zh_HK.
- Added post/postun to link Chinese font.properties files over 
  existing files for zh_CN and zh_TW.
- Fixes 4916359.

* Wed Aug 21 2003 - dermot.mccluskey@sun.com
- Added PreReq on j2re - needed to ensure correct install order

* Fri Aug 08 2003 - dermot.mccluskey@sun.com
- Add dependency on j2re - this makes everything simpler

* Thu Jul 31 2003 - Stephen.Browne@sun.com
- Remove .desktop file, fix links and add java plugin link

* Mon Jul 28 2003 - Stephen.Browne@sun.com
- Install Java convenience links
