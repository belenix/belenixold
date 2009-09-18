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
# owner:alfred date:2008-11-26 type:bug
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

cd %{_builddir}/%name-%version/WebKit-r%version/WebKitBuild/Release
make install DESTDIR=$RPM_BUILD_ROOT
mv ${RPM_BUILD_ROOT}/usr/local/* ${RPM_BUILD_ROOT}/usr
rmdir ${RPM_BUILD_ROOT}/usr/local
sed -e 's,local,,g' WebKit/gtk/webkit-1.0.pc > $RPM_BUILD_ROOT%{_libdir}/pkgconfig/webkit-1.0.pc
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/libwebkit-1.0.so.2
mv $RPM_BUILD_ROOT%{_libdir}/libwebkit-1.0.so.2.* $RPM_BUILD_ROOT%{_libdir}/libwebkit-1.0.so.2
rm -f $RPM_BUILD_ROOT%{_libdir}/libwebkit-1.0.so
ln -s libwebkit-1.0.so.2 $RPM_BUILD_ROOT%{_libdir}/libwebkit-1.0.so

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libwebkit*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_prefix}/include
%{_prefix}/include/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/webkit-1.0
%{_datadir}/webkit-1.0/*

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_localedir}
%{_localedir}/*

%changelog
* Fri Sep 18 2009 - moinakg(at)belenix<dot>org
- Remove commented patch lines.
* Tue Apr 28 2009 - moinakg@belenix.org
- Fix install script and update paths.
* Tue Apr 21 2009 - moinakg@belenix.org
- Imported and versiong bumped from SFE gate.
- Changes to build with Gcc 4.4.
- Add patch to remove /usr/bin/gcc hardcoding.
* Wed Dec 03 2008 - alfred.peng@sun.com
- Re-arrange the development headers, pc and library.
  Verified to work with the latest 0.22 devhelp release.
* Wed Nov 26 2008 - alfred.peng@sun.com
- Initial version
