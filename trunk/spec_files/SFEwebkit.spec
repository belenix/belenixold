#
# spec file for package SFEwebkit
#
# includes module(s): webkit
#
%include Solaris.inc

Name:                    SFEwebkit
Summary:                 WetKit, an open source web browser engine that's used by Safari, Dashboard, Mail, and many other OS X applications.
Version:                 42662
Source:                  http://builds.nightly.webkit.org/files/trunk/src/WebKit-r%{version}.tar.bz2
URL:                     http://www.webkit.org/

# owner:alfred date:2008-11-26 type:bug
#Patch1:                  webkit-01-sun-studio-build-hack.diff
# owner:alfred date:2008-11-26 type:bug
#Patch2:                  webkit-02-explicit-const.diff
Patch0:                  webkit_preproc.0.diff

SUNW_BaseDir:            %{_basedir}
# copyright place holder.
# TODO: add the WebKit copyright
SUNW_Copyright:          SFEwebkit.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEgccruntime
Requires: SUNWcurl
Requires: SUNWgnu-idn
Requires: SUNWgnome-base-libs
Requires: SFEicu4c
Requires: SUNWlxml
Requires: SUNWopenssl-libraries
Requires: SUNWopenssl-include
Requires: SUNWpr
Requires: SUNWsqlite3
Requires: SUNWtls
Requires: SUNWzlib
BuildRequires: SFEgcc

%prep
%setup -q -n %name-%version -c -a1
cd WebKit-r%version
#%patch1 -p0
#%patch2 -p0
%patch0 -p1

%build

%if %cc_is_gcc
export CPP="/usr/gnu/bin/gcc -E"
export GCC="/usr/gnu/bin/gcc"
export CPPFLAGS="-D__EXTENSIONS__"
export CFLAGS=${CPPFLAGS}
export CXXFLAGS=${CPPFLAGS}
%else
export SunStudioPath=/opt/SunStudioExpress
export CXXFLAGS="-features=zla -I/usr/stdcxx/include/ -library=no%Cstd"
export LDFLAGS="-L/usr/stdcxx/lib/ -lstd -L${SunStudioPath}/lib -lCrun -R/usr/stdcxx/lib/"
%endif

cd WebKit-r%version
./WebKitTools/Scripts/build-webkit --gtk

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_prefix}/include/webkit-1.0/webkit
mkdir -p $RPM_BUILD_ROOT%{_prefix}/include/webkit-1.0/JavaScriptCore/API
mkdir -p $RPM_BUILD_ROOT%{_libdir}/pkgconfig

cd %{_builddir}/%name-%version/WebKit-r%version/
cp WebKit/gtk/webkit/*.h $RPM_BUILD_ROOT%{_prefix}/include/webkit-1.0/webkit
cp -pr JavaScriptCore/ForwardingHeaders/JavaScriptCore/* $RPM_BUILD_ROOT%{_prefix}/include/webkit-1.0/JavaScriptCore/
cp -pr JavaScriptCore/API/*.h $RPM_BUILD_ROOT%{_prefix}/include/webkit-1.0/JavaScriptCore/API

cd WebKitBuild/Release
chmod 644 WebKit/gtk/webkit/webkitversion.h
cp WebKit/gtk/webkit/*.h $RPM_BUILD_ROOT%{_prefix}/include/webkit-1.0/webkit

sed -e 's,local,,g' WebKit/gtk/webkit-1.0.pc > temp.pc
mv temp.pc $RPM_BUILD_ROOT%{_libdir}/pkgconfig/webkit-1.0.pc
cp .libs/libwebkit-1.0.so $RPM_BUILD_ROOT%{_libdir}/libwebkit-1.0.so.1
ln -s libwebkit-1.0.so.1 $RPM_BUILD_ROOT%{_libdir}/libwebkit-1.0.so

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libwebkit*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_prefix}/include
%{_prefix}/include/*

%changelog
* Tue Apr 21 2009 - moinakg@belenix.org
- Imported and versiong bumped from SFE gate.
- Changes to build with Gcc 4.4.
- Add patch to remove /usr/bin/gcc hardcoding.
* Wed Dec 03 2008 - alfred.peng@sun.com
- Re-arrange the development headers, pc and library.
  Verified to work with the latest 0.22 devhelp release.
* Wed Nov 26 2008 - alfred.peng@sun.com
- Initial version
