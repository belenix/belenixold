#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

Name:                FSWjavapluginlink
Summary:             Symbolic link enabling Java Plugin in Firefox
Version:             5.11

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
Requires:            SUNWfirefox

%prep
rm -rf %{name}-%{version}-build
mkdir %{name}-%{version}-build

%build
cd %{name}-%{version}-build

%install

cd %{name}-%{version}-build
rm -rf ${RPM_BUILD_ROOT}
mkdir ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/firefox/plugins
cd ${RPM_BUILD_ROOT}%{_libdir}/firefox/plugins
ln -sf /usr/jdk/instances/latest/jre/plugin/i386/ns7/libjavaplugin_oji.so

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/firefox
%dir %attr (0755, root, bin) %{_libdir}/firefox/plugins
%{_libdir}/firefox/plugins/*

%changelog
* Sat Aug 03 2008 - moinakg@gmail.com
- Initial spec.
