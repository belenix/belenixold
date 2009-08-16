#
# spec file for package SUNWgnu-gettext
#
# includes module(s): GNU gettext
#
%include Solaris.inc
%include usr-gnu.inc

Name:                SUNWgnu-gettext
Summary:             GNU gettext
Version:             0.17
Source:              ftp://ftp.gnu.org/pub/gnu/gettext/gettext-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
#Patch1:              gettext-01-vasprintf.diff

#
# Disable acl_trivial usage from libsec for now. libsec brings in libidmap which
# brings in libldap which brings in system NSS/NSPR compiled using Studio.
# XULRunner and related tools built using Gcc and using a different NSS/NSPR
# will get confused when linked with GNU Gettext if there are 2 different NSS/NSPR
# linked into the same executable image built using different compilers. The
# typical result will be a crash!
#
Patch2:              gettext-02-disable-acl_trivial.diff
%include default-depend.inc
Requires: SUNWpostrun

%package devel
Summary:                 %{summary} - developer files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -c -n %name-%version
cd gettext-%{version}
#%patch1 -p1
%patch2 -p1
cd ..

%ifarch amd64 sparcv9
cp -pr gettext-%{version} gettext-%{version}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

%if %build_l10n
nlsopt=-enable-nls
%else
nlsopt=-disable-nls
%endif

export CFLAGS32="%optflags"
export CFLAGS64="%optflags64"
export CXXFLAGS32="%cxx_optflags"
export CXXFLAGS64="%cxx_optflags64"
export LDFLAGS32="%_ldflags"
export LDFLAGS64="%_ldflags"

%ifarch amd64 sparcv9

export CC=${CC64:-$CC}
export CXX=${CXX64:-$CXX}
export CFLAGS="$CFLAGS64"
export CXXFLAGS="$CXXFLAGS64"
export LDFLAGS="$LDFLAGS64"

cd gettext-%{version}-64

./configure --prefix=%{_prefix}			\
            --libdir=%{_libdir}/%{_arch64}	\
            --mandir=%{_mandir}			\
	    --infodir=%{_infodir}		\
	    --without-emacs			\
	    --disable-static			\
	    $nlsopt

make -j$CPUS
cd ..
%endif

cd gettext-%{version}

export CC=${CC32:-$CC}
export CXX=${CXX32:-$CXX}
export CFLAGS="$CFLAGS32"
export CXXFLAGS="$CXXFLAGS32"
export LDFLAGS="$LDFLAGS32"

./configure --prefix=%{_prefix}		\
            --libdir=%{_libdir}		\
            --mandir=%{_mandir}		\
	    --infodir=%{_infodir}	\
	    --without-emacs		\
	    --disable-static		\
	    $nlsopt

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
cd gettext-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_libdir}/%{_arch64}/*.a
rm -f $RPM_BUILD_ROOT/%{_libdir}/%{_arch64}/*.la
if [ -f ./gettext-runtime/intl/.libs/libgnuintl.so ]
then
	cp ./gettext-runtime/intl/.libs/libgnuintl.so $RPM_BUILD_ROOT/usr/gnu/lib/%{_arch64}/libintl.so.8.0.2
        chmod a+rx $RPM_BUILD_ROOT/usr/gnu/lib/%{_arch64}/libintl.so.8.0.2
        (cd $RPM_BUILD_ROOT/usr/gnu/lib/%{_arch64}
          ln -s libintl.so.8.0.2 libintl.so.8
          ln -s libintl.so.8.0.2 libintl.so)
fi
mkdir -p $RPM_BUILD_ROOT/usr/lib/%{_arch64}
(cd $RPM_BUILD_ROOT/usr/lib/%{_arch64}
 ln -s ../../gnu/lib/%{_arch64}/libintl.so libgnuintl.so)
 
cd ..
%endif


cd gettext-%{version}
make install DESTDIR=$RPM_BUILD_ROOT

cd $RPM_BUILD_ROOT%{_prefix}
ln -s share/man man

rm -rf $RPM_BUILD_ROOT%{_infodir}
rm $RPM_BUILD_ROOT%{_libdir}/charset.alias
rm $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/charset.alias

(cd $RPM_BUILD_ROOT/usr/lib
 ln -s ../gnu/lib/libintl.so libgnuintl.so)


%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}
%{_prefix}/man
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, bin) /usr/lib
/usr/lib/libgnuintl.so
%dir %attr (0755, root, bin) %{_libdir}/gettext
%{_libdir}/gettext/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/gettext
%{_datadir}/gettext/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*.1
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*.3
%dir %attr(0755, root, sys) %{_std_datadir}
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%dir %attr (0755, root, bin) /usr/lib/%{_arch64}
/usr/lib/%{_arch64}/libgnuintl.so
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}/gettext
%{_libdir}/%{_arch64}/gettext/*
%endif
%defattr (-, root, other)
%{_datadir}/doc

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sat Aug 15 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Add workaround to rename wrongly generated shared lib name.
* Sun Jul 26 2009 - moinakg<at>belenix(dot)org
- Avoid linking with libsec to avoid bringing in system NSS/NSPR.
* Tue May 12 2009 - moinakg@belenix.org
- Bump version to 0.17.
- Rename package to satisfy dependencies.
* Fri Jan 11 2008 - moinak.ghosh@sun.com
- Fix missing '$' in CC variable reference
- Add patch to fix invalid usage of a va_list variable
* Fri Apr 20 2007 - Doug Scott <dougs@truemail.co.th>
- Fixed %{_datadir}/doc group
* Fri Apr 20 2007 - Doug Scott <dougs@truemail.co.th>
- Removed gettext.info autosprintf.info - conflicts with SUNWgnome-common-devel
- Removed charset.alias - conficts with SFEcoreutils
* Sun Mar  7 2007 - Doug Scott <dougs@truemail.co.th>
- Initial spec
