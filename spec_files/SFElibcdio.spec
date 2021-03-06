#
# spec file for package SUNWlibcdio
#
# includes module(s): libcdio
#
# Copyright (c) 2004 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Currently, libcdio doesn't work well on Solaris SPARC 
# because of endianess differences. A bug has been filed for it 
# at http://bugzilla.gnome.org/show_bug.cgi?id=377280. Patch
# has been provided as an workaround (please note that this
# is not a final solution). To make libcdio work on Solaris SPARC
# we suggest you applying the patch above.
%include Solaris.inc

%define with_hal %(pkginfo -q SUNWhal && echo 1 || echo 0)

%use libcdio = libcdio.spec

Name:                    SFElibcdio
Summary:                 GNU libcdio
Version:                 %{libcdio.version}
Patch1:                  libcdio-01-usehal.diff
Patch2:                  libcdio-02-stdint.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWlexpt
Requires: SUNWlibC
Requires: SUNWlibmsr
Requires: SUNWgccruntime
Requires: SUNWlibms
Requires: SUNWdbus
%if %with_hal
Requires: SUNWhal
%endif
BuildRequires: SUNWlexpt
BuildRequires: SUNWgcc
BuildRequires: SUNWdbus-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir %name-%version
%libcdio.prep -d %name-%version

cd %{_builddir}/%name-%version/libcdio-%{libcdio.version}
%if %with_hal
%patch1 -p1
%endif
%patch2 -p1

# Note, we have to build this with gcc, because Forte cannot handle
# the flexible arrays used in libcdio.  We should move to using Forte
# if this issue is resolved with the Forte compiler.
#
%build
export CFLAGS="%gcc_optflags"
export CC=/usr/gnu/bin/gcc
export CXX=/usr/gnu/bin/g++
%if %with_hal
export LDFLAGS="%_ldflags -lhal -ldbus-1"
%else
export LDFLAGS="%_ldflags"
%endif

%libcdio.build -d %name-%version

%install
%libcdio.install -d %name-%version

#rm -rf $RPM_BUILD_ROOT%{_mandir}
#rm -rf $RPM_BUILD_ROOT%{_prefix}/share
#rm -rf $RPM_BUILD_ROOT%{_prefix}/info
rm -f $RPM_BUILD_ROOT%{_prefix}/share/info/dir
(cd $RPM_BUILD_ROOT%{_libdir}
 ln -s libcdio.so.10 libcdio.so.7)

#%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, bin) %{_mandir}/jp
%dir %attr (0755, root, bin) %{_mandir}/jp/man1
%{_mandir}/jp/man1/*
%dir %attr (0755, root, bin) %{_infodir}
%{_infodir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/cdio

%changelog
* Sun Apr 17 2009 - moinakg@belenix.org
- Add a compatibility symlink.
* Tue Apr 28 2009 - moinakg@belenix.org
- Bump version to 0.81.
* Sat Jan 19 2008 - moinak.ghosh@sun.com
- Set g++ as cpp compiler
- Added back man and info files
* Sun Jan 06 2008 - moinak.ghosh@sun.com
- Changed reference to non-existent gcc_ldflags
* Sun Nov 4 2007 - markwright@internode.on.net
- Bump to 0.79.  Add libcdio-02-stdint.diff.
* Thu Oct 18 2007 - laca@sun.com
- use gcc specific compiler/linker flags
* Mon Jun 23 - irene.huang@sun.com
- created.
