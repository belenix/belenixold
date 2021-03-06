#
# spec file for package SFEcurl
#
# includes module(s): curl
#
# 64 bit stuff shanelessly stolen from SFEncurses

%include Solaris.inc

Name:                    SUNWcurl
Summary:                 curl - Get a file from FTP or HTTP server.
Version:                 7.19.0
URL:                     http://curl.haxx.se/
Source:                  http://curl.haxx.se/download/curl-%{version}.tar.bz2
Source1:                 curlbuild_wrapper.h
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:               SUNWzlib
Requires:               SUNWgnu-idn
Requires:               SUNWopenssl-libraries
BuildRequires:          SUNWopenssl-include

%ifarch amd64 sparcv9
%include arch64.inc
%use curl64=curl.spec
%endif
%include base.inc
%use curl = curl.spec

%package devel
Summary:		 curl-devel - Curl library development files.
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:		 %name

%prep
rm -rf %name-%version
mkdir %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%curl64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%curl.prep -d %name-%version/%{base_arch}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

# -L/lib added to CFLAGS to workaround what seems to be a libtool bug
export CPPFLAGS="-I/usr/include"
export MSGFMT="/usr/bin/msgfmt"

%ifarch amd64 sparcv9
export CFLAGS="%optflags64 -I/usr/include -DANSICPP -L/lib/%_arch64 -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE"
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="-m64 %{gnu_lib_path64} -L/lib/%_arch64 -R/lib/%_arch64"
%curl64.build -d %name-%version/%_arch64
%endif

export LDFLAGS="%{gnu_lib_path} -L/lib -R/lib"
export CFLAGS="%optflags -I/usr/include -DANSICPP -L/lib -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE"
export RPM_OPT_FLAGS="$CFLAGS"
%curl.build -d %name-%version/%{base_arch}

%install
rm -rf ${RPM_BUILD_ROOT}
%ifarch amd64 sparcv9
%curl64.install -d %name-%version/%_arch64
mkdir -p ${RPM_BUILD_ROOT}/%{_includedir}/curl/64
mv ${RPM_BUILD_ROOT}/%{_includedir}/curl/curlbuild.h ${RPM_BUILD_ROOT}/%{_includedir}/curl/64
rm -f ${RPM_BUILD_ROOT}/%{_libdir}/%{_arch64}/*.a
rm -f ${RPM_BUILD_ROOT}/%{_libdir}/%{_arch64}/*.la
%endif

%curl.install -d %name-%version/%{base_arch}
cp %{SOURCE1} ${RPM_BUILD_ROOT}/%{_includedir}/curl/
cp ${RPM_BUILD_ROOT}/%{_includedir}/curl/curl.h .
cat curl.h | sed '{
    s@curlbuild.h@curlbuild_wrapper.h@
}' > ${RPM_BUILD_ROOT}/%{_includedir}/curl/curl.h
rm -f ${RPM_BUILD_ROOT}/%{_libdir}/*.a
rm -f ${RPM_BUILD_ROOT}/%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/curl
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/curl.1
%ifarch amd64 sparcv9
%{_bindir}/%_arch64/curl
%{_libdir}/%_arch64/lib*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/curl-config
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/curl-config.1
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*
%ifarch amd64 sparcv9
%dir %attr(0755, root, other) %{_libdir}/%_arch64/pkgconfig
%{_libdir}/%_arch64/pkgconfig/libcurl.pc
%{_bindir}/%_arch64/curl-config
%endif

%changelog
* Fri Sep 18 2009 - moinakg(at)belenix<dot>org
- Nuke libtool archives and fix build to locate OpenSSL in /lib.
* Tue Jul 07 2009 - moinakg(at)belenix<dot>org
- Fix paths to pick up correct libgcc.
* Fri May 22 2009 - moinakg@belenix.org
- Add supporting header for proper multilib functionality.
* Thu Oct 30 2008 - moinakg@belenix.org
- Add largefile support flags.
* Wed Oct 29 2008 - moinakg@belenix.org
- Rename to SUNWcurl and add merge modified build recipe from SFW gate.
* Thu Feb 21 2008 - moinak.ghosh@sun.com
- Fix 64Bit build flags to properly build with Gcc.
* Sun Jan 06 2008 - moinak.ghosh@sun.com
- Fixed pkgconfig directory permission
* Wed Dec 12 2007 - Michal Bielicki
- change the package to be combined 32/64 bit (thanks to Thomas Wagner for all his help with this)
* Mon Nov 26 2007 - Thomas Wagner
- move SFEcurl into /usr/gnu by %include usr-gnu.inc (never OS builds have SUNWcurl)
* Mon Oct 29 2007 - brian.cameron@sun.com
- Bump to 7.17.1
* Tue Sep 18 2007 - nonsea@users.sourceforge.net
- Bump to 7.17.0
* Mon May 28 2007 - Thomas Wagner
- bump to 7.16.2
- --disable-static
* Thu Feb 15 2007 - laca@sun.com
- bump to 7.16.1
* Wed Jan  3 2007 - laca@sun.com
- bump to 7.16.0
* Fri Jun 23 2006 - laca@sun.com
- rename to SFEcurl
- delete -share subpkg
- update attributes to match JDS
- add missing deps
* Sun May 14 2006 - mike kiedrowski (lakeside-AT-cybrzn-DOT-com)
- Delete *.la.
* Mon Apr  3 2006 - mike kiedrowski (lakeside-AT-cybrzn-DOT-com)
- Initial spec
