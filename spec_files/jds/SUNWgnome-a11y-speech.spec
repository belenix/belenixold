#
# spec file for package SUNWgnome-a11y-speech
#
# includes module(s): gnome-speech
#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: liyuan
#
%include Solaris.inc

%define build_dectalk %(test -f /usr/bin/say && echo 1 || echo 0)
%define build_swift %(test -d /opt/swift && echo 1 || echo 0)

%use gnome_speech = gnome-speech.spec

Name:                    SUNWgnome-a11y-speech
Summary:                 GNOME text-to-speech engine
Version:                 %{default_pkg_version}
Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-a11y-libs
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-component
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-component-devel

%package festival
Summary:                 %{summary} - Festival Synthesis Driver
SUNW_BaseDir:            %{_basedir}
Requires: SUNWgnome-a11y-speech
%include default-depend.inc

%package freetts
Summary:                 %{summary} - FreeTTS Synthesis Driver
SUNW_BaseDir:            %{_basedir}
Requires: SUNWgnome-a11y-speech
%include default-depend.inc

%if %build_dectalk
%package dectalk
Summary:                 %{summary} - Fonix DECtalk Synthesis Driver
SUNW_BaseDir:            %{_basedir}
Requires: SUNWgnome-a11y-speech
%include default-depend.inc
%endif

%package espeak
Summary:                 %{summary} - eSpeak Synthesis Driver
SUNW_BaseDir:            %{_basedir}
Requires: SUNWespeak
Requires: SUNWgnome-a11y-speech
BuildRequires: SUNWespeak-devel
%include default-depend.inc

%if %build_swift
%package swift
Summary:                 %{summary} - Cepstral Swift Synthesis Driver
SUNW_BaseDir:            %{_basedir}
Requires: SUNWgnome-a11y-speech
%include default-depend.inc
%endif

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir %name-%version
%gnome_speech.prep -d %name-%version
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build
export PKG_CONFIG_PATH=%{_pkg_config_path}
export MSGFMT="/usr/bin/msgfmt"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
if [ `uname -r` = 5.9 ]; then
export CFLAGS="%optflags -I%{_includedir} -I/usr/j2se/include -I/usr/j2se/include/solaris"
else
export CFLAGS="%optflags -I%{_includedir} -I/usr/jdk/instances/jdk1.5.0/include -I/usr/jdk/instances/jdk1.5.0/include/solaris"
fi
export RPM_OPT_FLAGS="$CFLAGS"
export LD_RUN_PATH="%{_libdir}"
export LDFLAGS="%_ldflags"
%gnome_speech.build -d %name-%version

%install
%gnome_speech.install -d %name-%version

# install man page
rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT


%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/test-speech
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libgnomespeech.so*
%{_libdir}/orbit-2.0/GNOME_Speech_module.*
%dir %attr (0755, root, sys) %{_datadir}
%doc -d gnome-speech-%{gnome_speech.version} README AUTHORS
%doc(bzip2) -d gnome-speech-%{gnome_speech.version} COPYING NEWS ChangeLog
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/idl/gnome-speech-*/GNOME_Speech*.idl
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*
%if %option_with_java
%{_datadir}/jar/gnome-speech.jar
%endif

%files festival
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/festival-synthesis-driver
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/bonobo/servers/GNOME_Speech_SynthesisDriver_Festival.server

%if %option_with_java
%files freetts
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/freetts-synthesis-driver
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libfreettsdriver.*
%{_libdir}/bonobo/servers/GNOME_Speech_SynthesisDriver_FreeTTS.server
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/jar/freetts-synthesis-driver.jar
%{_datadir}/gnome-speech/drivers/freetts/user_addenda.txt
%endif

%if %build_dectalk
%files dectalk
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/dectalk-synthesis-driver
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/bonobo/servers/GNOME_Speech_SynthesisDriver_Dectalk.server
%endif

%files espeak
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/espeak-synthesis-driver
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/bonobo/servers/GNOME_Speech_SynthesisDriver_Espeak.server

%if %build_swift
%files swift
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/swift-synthesis-driver
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/bonobo/servers/GNOME_Speech_SynthesisDriver_Swift.server
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/gnome-speech-*/gnome-speech/*.h

%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Thu Sep 18 2008 - li.yuan@sun.com
- Added %doc to %files for copyright.
* Wed Aug 20 2008 - william.walker@sun.com
- Require SUNWespeak.spec so it will be built prior to
  SUNWgnome-a11y-speech.
* Wed Aug 20 2008 - william.walker@sun.com
- Migrate SFEespeak.spec to SUNWespeak.spec
* Tue Aug 05 2008 - li-yan.zhang@sun.com
- Add manpages. 
* Thu Apr 21 2008 - william.walker@sun.com
- Add new optional espeak and swift packages.  Also change the way
  the DECtalk package was created since the DECtalk folks have
  different ways of shipping/installing their product.
* Mon Mar 31 2008 - li.yuan@sun.com
- Add copyright file
* Fri Sep 28 2007 - laca@sun.com
- disable packaging java stuff if the --without-java option is used
* Thu Jul 13 2006 - william.walker@sun.com
- Add new packaging scheme
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Tue May 09 2006 - laca@sun.com
- merge -share pkg(s) into the base pkg(s)
* Mon Feb 20 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Sat Oct 02 2004 - laca@sun.com
- added %pkgbuild_postprocess
* Wed Sep 22 2004 - damien.carbery@sun.com
- Correct JDK path in CFLAGS so jni.h can be found.
* Fri Jul 23 2004 - damien.carbery@sun.com
- Move freetts to SUNWgnome-a11y-libs.
* Tue Jun 22 2004 - shirley.woo@sun.com
- changed install location to /usr/lib and /usr/bin
* Thu Mar 11 2004 - damien.carbery@sun.com
- Add jar files that come from freetts module.
* Mon Mar 02 2004 - laca@sun.com
- add LD_RUN_PATH since -R{%_libdir} doesn't seem to work
* Mon Mar 01 2004 - laca@sun.com
- add share, devel subpkgs
