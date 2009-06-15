#
# spec file for package SFEaspell
#
# includes module(s): aspell
#
# Copyright (c) 2004 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jedy
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use aspell64 = aspell.spec
%endif

%include base.inc
%use aspell = aspell.spec

Name:          SFEaspell
Summary:       A Spell Checker
Version:       %{aspell.version}
SUNW_BaseDir:  %{_prefix}
BuildRoot:     %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
%if %cc_is_gcc
Requires:      SFEgccruntime
%else
Requires:      SUNWlibC
%endif
Requires:      SUNWlibms
Requires:      SUNWlibmsr
Requires:      SUNWperl584core
BuildConflicts:	SUNWaspell

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires:      SFEaspell

%prep
rm -rf %name-%version
%ifarch amd64 sparcv9
mkdir -p %name-%version/%_arch64
%aspell64.prep -d  %name-%version/%_arch64
%endif

mkdir -p %name-%version
%aspell.prep -d %name-%version

%build
%if %option_with_indiana_branding
export MSGFMT="/usr/gnu/bin/msgfmt"
%else
export MSGFMT="/usr/bin/msgfmt"
%endif

%ifarch amd64 sparcv9
%if %cc_is_gcc
export CFLAGS="%optflags64"
export LDFLAGS="%_ldflags64 -lm -lstdc++"
export CXXFLAGS="%cxx_optflags64"
%else
export CXX="$CXX -norunpath"
export CFLAGS="%optflags64"
export LDFLAGS="%_ldflags64 -lCrun -lm"
export CXXFLAGS="%cxx_optflags64 -staticlib=stlport4"
%endif

%aspell64.build -d %name-%version/%_arch64
%endif

%if %cc_is_gcc
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -lm -lstdc++"
export CXXFLAGS="%cxx_optflags"
%else
export CXX="$CXX -norunpath"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -lCrun -lm"
export CXXFLAGS="%cxx_optflags -staticlib=stlport4"
%endif

%aspell.build -d %name-%version

%install
%ifarch amd64 sparcv9
%aspell64.install -d %name-%version/%_arch64
rm -rf $RPM_BUILD_ROOT%{_datadir}
%endif

%aspell.install -d %name-%version
# The only stuff in datadir is doc, info and man which we do not want
# to package.  
#
rm -rf $RPM_BUILD_ROOT%{_datadir}

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}/bin
%{_prefix}/bin/*
%dir %attr (0755, root, bin) %{_prefix}/lib
%{_prefix}/lib/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Mon Jun 15 2009 - moinakg@belenix(dot)org
- Add 64Bit build and rebuild with Gcc4.4
* Sun Feb 24 2008 - moinakg@gmail.com
- Add from SFE repo.
* Sat Apr 21 2007 - dougs@truemail.co.th
- Added BuildConflicts: SUNWaspell
* Tue Mar 13 2007 - jeff.cai@sun.com
- Move to sourceforge from opensolaris.
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Fri Apr 21 2006 - halton.huo@sun.com
- Move all things under %{_bindir} to %{_libdir}/aspell,
  requested by ARC change.
* Thu Apr 20 2006 - halton.huo@sun.com
- Change aspell lib dir from %{_libdir}/aspell-0.60 to 
  %{_libdir}/aspell, request by LSARC/2006/231.
* Thu Feb  2 2006 - damien.carbery@sun.com
- Add SUNWlibmsr to fix 6318910.
* Fri Jan 27 2006 - damien.carbery@sun.com
- Remove '-library=stlport' from CXXFLAGS so it the library is not dynamically 
  linked into /usr/bin/aspell.
* Thu Oct 06 2005 - damien.carbery@sun.com
- Fix 6208701 (missing dependencies).
* Tue Sep 06 2005 - laca@sun.com
- fix build with new automake and libtool; remove unpackaged files
* Tue Jun 28 2005 - laca@sun.com
- fix stlport4 static linking with Vulcan FCS
* Sat Oct 02 2004 - laca@sun.com
- added %pkgbuild_postprocess
* Thu Mar 11 2004 - <laca@sun.com>
- initial version created
