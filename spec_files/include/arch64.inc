#
# 64-bit platform settings for Solaris packages
#
# Copyright 2007 Sun Microsystems, Inc.
#
# Solaris.inc must be included before this file

%ifarch amd64 sparcv9

%ifarch amd64
%define _arch64 amd64
%else
%define _arch64 sparcv9
%endif

%define opt_arch64 1
%define can_isaexec 1
%define gtk_doc_option --disable-gtk-doc
%define gnu_iconv_ldadd -Wl,-zignore -R/usr/gnu/lib/%{_arch64} -lgnuintl -lgnuiconv

%if %option_with_gnu_iconv
%define arch_ldadd -L%{_libdir} -R%{_libdir} %{gnu_iconv_ldadd}
%else
%define arch_ldadd -L%{_libdir} -R%{_libdir}
%endif

%ifarch amd64
%define opt_amd64 1
%define bld_arch	"amd64"
%else
%define opt_sparcv9 1
%define bld_arch	"sparcv9"
%endif

%if %debug_build
%define pkgbuild_postprocess /bin/true
%define _cc64_opt_level      -g
%define _cxx64_opt_level     -g
%define _gcc64_opt_level      -g
%define _gxx64_opt_level     -g
%else
%if %cc_is_gcc
%define _gcc64_opt_level      -O3
%define _gxx64_opt_level     -O3
%else
%define _cc64_opt_level      -xO4 -xspace
%define _cxx64_opt_level     -xO3 -xspace
%endif
%endif

%ifarch sparc
%define gcc_optflags64           %_gcc64_opt_level -mcpu=ultrasparc -m64 -Xlinker -i %gcc_picflags
%define gcc_cxx_optflags64       %gcc_optflags64
%define gcc_ldflags64		-m64
%endif

%ifarch i386
%define gcc_optflags64           %_gcc64_opt_level -march=opteron -m64 -Xlinker -i -fno-omit-frame-pointer %gcc_picflags
%define gcc_cxx_optflags64       %gcc_optflags64
%define gcc_ldflags64		-m64
%endif

%ifarch sparc
%define suncc_optflags64           %_cc64_opt_level -xstrconst -xarch=v9 -xcode=pic32 -mr
%define suncc_cxx_optflags64       %_cxx64_opt_level -xarch=v9 -xcode=pic32 -mr -norunpath
%define suncc_ldflags64
%endif

%ifarch i386
%define suncc_optflags64           %_cc64_opt_level -xstrconst -m64 -Kpic -xregs=no%%frameptr
%define suncc_cxx_optflags64       %_cxx64_opt_level -m64 -Kpic -pentium -mr -norunpath -xregs=no%%frameptr
%define suncc_ldflags64
%endif

%if %cc_is_gcc

%define picflags %gcc_picflags
%define optflags64 %gcc_optflags64
%define cxx_optflags64 %gcc_cxx_optflags64
%define _gpp_version %(g++ --version | head -1 | cut -f3 -d' ')
%define _cxx_libdir	   %{_prefix}/lib/g++/%{_gpp_version}/%{_arch64}
%define _ldflags64 %gcc_ldflags64
%define _bit64flag %gcc_ldflags64

%else
# cc is not gcc

%define picflags %suncc_picflags
%define optflags64 %suncc_optflags64
%define cxx_optflags64 %suncc_cxx_optflags64
%define _cxx_libdir %{_prefix}/lib
%define _ldflags64 %suncc_ldflags64
%define _bit64flag %suncc_ldflags64

%endif

%define optflags %optflags64 ${EXTRA_CFLAGS}
%define cxx_optflags %cxx_optflags64 ${EXTRA_CXXFLAGS}
%define _ldflags %__ldflags %_ldflags64
%if %option_with_gnu_iconv
%define _ldflags64 %{_bit64flag} -L%{_libdir}/%{_arch64} -R%{_libdir}/%{_arch64} %{gnu_iconv_ldadd} %{_ldopt}
%else
%define _ldflags64 %{_bit64flag} -L%{_libdir}/%{_arch64} -R%{_libdir}/%{_arch64} %{_ldopt}
%endif


%define _bindir		 %{_prefix}/bin/%{bld_arch}
%define _libdir		 %{_prefix}/lib/%{bld_arch}
%define _libexecdir	 %{_prefix}/lib/%{bld_arch}
%define _pkg_config_path %{_libdir}/pkgconfig:%{_prefix}/gnu/lib/%{bld_arch}/pkgconfig
%define _pkg_config_path64 %{_prefix}/lib/%{_arch64}/pkgconfig:%{_prefix}/gnu/lib/%{_arch64}/pkgconfig

%endif

# Define some standard directories
%define gnu_bin         /usr/gnu/bin/%{bld_arch}
%define gnu_inc         /usr/gnu/include
%define gnu_lib         /usr/gnu/lib/%{bld_arch}
%define gnu_lib_path    -L%gnu_lib -R%gnu_lib
%define gnu_lib64       /usr/gnu/lib/%{_arch64}
%define gnu_lib_path64  -L%gnu_lib64 -R%gnu_lib64
%define sfw_bin         /usr/sfw/bin/%{bld_arch}
%define sfw_inc         /usr/sfw/include
%define sfw_lib         /usr/sfw/lib/%{bld_arch}
%define sfw_lib64       /usr/sfw/lib/%{_arch64}
%define sfw_lib_path    -L%sfw_lib -R%sfw_lib
%define sfw_lib_path64  -L%sfw_lib64 -R%sfw_lib64
%define xorg_bin        /usr/X11/bin/%{bld_arch}
%define xorg_lib        /usr/X11/lib/%{bld_arch}
%define xorg_lib64      /usr/X11/lib/%{_arch64}
%define xorg_inc        /usr/X11/include
%define xorg_lib_path   -L%xorg_lib -R%xorg_lib
%define xorg_lib_path64 -L%xorg_lib64 -R%xorg_lib64
%define qt4_bin_path64  /usr/qt4/bin/%{_arch64}

# ChangeLog:
# 2009-05-29  moinakg@belenix(dot)org
# - Update _ldflags64 with proper flags.
# 2009-05-17  moinakg@belenix.org
# - Fix 64Bit Gnu lib paths.
# 2009-05-16  moinakg@belenix.org
# - Add 64Bit Gnu lib paths.
# 2008-02-21  moinak.ghosh@sun.com
# - Add definitions to properly define 64Bit LDFLAGS for Gcc.
# - Merge in definitions from SFE repo for building with gnu gettext.
# 2008-02-17  Laszlo (Laca) Peter  <laca@sun.com>
# - define _cxx_libdir and _gpp_version for building C++ libs
# 2007-03-20  Doug Scott  <dougs@truemail.co.th>
# added %_cc64_opt_level to suncc_optflags64
# added standard directories definitions
# 2007-03-19  Doug Scott  <dougs@truemail.co.th>
# - Fixed -fno-omit-frame-pointer flag
# 2007-03-15  Laszlo (Laca) Peter  <laca@sun.com>
# - renamed from amd64.inc
# - updated to work for either amd64 or sparcv9
# 2007-03-12  Doug Scott  <dougs@truemail.co.th>
