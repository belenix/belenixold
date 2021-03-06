#
# spec file for package SFEgnupg
#
# includes module(s): gnupg
#
#

%include Solaris.inc
%use gnupg = gnupg2.spec
%define sunw_gnu_iconv %(pkginfo -q SUNWgnu-libiconv && echo 1 || echo 0)

Name:          SFEgnupg2
Summary:       %{gnupg.summary}
Version:       %{gnupg.version}
Patch1:        gnupg2-01-asschk.diff
Patch2:        gnupg2-02-inittests.diff
SUNW_BaseDir:  %{_basedir}
BuildRoot:     %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWbzip
Requires: SUNWzlib
Requires: SFEreadline
BuildRequires: SFEreadline-devel
Requires: SUNWcurl
%if %build_l10n
%if %sunw_gnu_iconv
Requires: SUNWgnu-libiconv
Requires: SUNWgnu-gettext
%else
Requires: SFEgettext
Requires: SFElibiconv
%endif
%endif

%if %build_l10n
%package l10n
Summary:        %{summary} - l10n files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires:       %{name}
%endif

%prep
rm -rf %name-%version
mkdir -p %name-%version
%gnupg.prep -d %name-%version
cd %name-%version
%patch1 -p0
%patch2 -p0
cd ..

%build
export CFLAGS="%optflags"
export MSGFMT="/usr/bin/msgfmt"
export LDFLAGS="%_ldflags -lsocket"
%if %build_l10n
LDFLAGS="$LDFLAGS -L/usr/gnu/lib -R/usr/gnu/lib -lintl -liconv"
LIBINTL="/usr/gnu/lib/libintl.so"
%endif
%gnupg.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%gnupg.install -d %name-%version
rm -rf $RPM_BUILD_ROOT%{_libdir}/lib*a
rm -rf $RPM_BUILD_ROOT%{_libdir}/charset.alias
rm -rf $RPM_BUILD_ROOT%{_datadir}/info

#
# Rename 2 files to be compatible with SFEgnupg (GnuPG version 1.x)
# package.
#
mv $RPM_BUILD_ROOT%{_datadir}/gnupg/FAQ \
    $RPM_BUILD_ROOT%{_datadir}/gnupg/FAQ2
mv $RPM_BUILD_ROOT%{_datadir}/gnupg/faq.html \
    $RPM_BUILD_ROOT%{_datadir}/gnupg/faq2.html

%if %build_l10n
%else
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (0755, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gnupg
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%if %build_l10n
%files l10n
%defattr (0755, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (0755, root, other) %{_datadir}/locale
%endif

%changelog
* Thu Feb 21 2008 - moinak.ghosh@sun.com
- Build with SUNWgnu-gettext/libiconv from JDS gate for Indiana environment.
* Sun Jan 20 2008 - moinak.ghosh@sun.com
- Fixed various nits.
- Fixed build using SUN Studio.
* Sat Dec 29 2007 - jijun.yu@sun.com
- initial version created
