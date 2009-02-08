#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# spec file for package SUNWgmp
#
# includes module(s): GNU gmp
#
%include Solaris.inc

Name:                    SUNWa2ps
Summary:                 a2ps - GNU Any to PostScript filter (root)
Version:                 4.13
%define tarball_version  4.13b
URL:                     http://www.gnu.org/software/a2ps/
Source:                  http://ftp.gnu.org/gnu/a2ps/a2ps-%{tarball_version}.tar.gz
Source1:                 a2ps.fd

Patch1:                  a2ps-01-configure.diff
Patch2:                  a2ps-02-sheets.map.diff
SUNW_BaseDir:            /
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgcmn
Requires: SUNWbash
Requires: SUNWpsutils
Requires: SUNWimagick
Requires: SUNWlibms
Requires: SUNWlibmsr
Requires: SUNWperl584core
BuildRequires: SUNWpsutils

%prep
if [ "x`basename $CC`" = xgcc ]
then
	%error This spec file requires SUN Studio, set the CC and CXX env variables
fi

rm -rf a2ps-%{version}
%setup -q -n a2ps-%version

cat %{PATCH1} | gpatch -p 1
cat %{PATCH2} | gpatch -p 1

%build
CC="${CC} -xc99=%all"
LDFLAGS="%_ldflags %{sfw_lib_path}"
CFLAGS="%optflags -I%{sfw_inc}"
EMACS=no
PATH=${PATH}:%{sfw_bin}
export CC LDFLAGS CFLAGS EMACS PATH INSTALL

./configure --with-medium=letter \
            --enable-shared \
            --sysconfdir=%{_sysconfdir}/gnu \
            --prefix=%{_basedir} \
            --mandir=%{_mandir} \
            --infodir=%{_infodir}

/usr/bin/gmake

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT

/usr/bin/gmake install DESTDIR=${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/lp/fd
cp %{SOURCE1} ${RPM_BUILD_ROOT}%{_sysconfdir}/lp/fd

mkdir -p ${RPM_BUILD_ROOT}%{sfw_bin}
(cd ${RPM_BUILD_ROOT}%{sfw_bin}
 for prg in a2ps card composeglyphs fixnt fixps ogonkify pdiff psmandup \
     psset texi2dvi4a2ps
 do
        ln -s ../../..%{_basedir}/bin/$prg
 done)

rm -f ${RPM_BUILD_ROOT}%{_basedir}/lib/*.a
rm -f ${RPM_BUILD_ROOT}%{_basedir}/lib/*.la
rm -f ${RPM_BUILD_ROOT}/*.el

%clean
rm -rf $RPM_BUILD_ROOT

%iclass preserve -f i.preserve

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, sys) %{_sysconfdir}
%dir %attr (0755, root, bin) %{_sysconfdir}/gnu
%dir %attr (0755, lp, lp) %{_sysconfdir}/lp
%dir %attr (0755, root, lp) %{_sysconfdir}/lp/fd
%config %class(preserve) %attr (0644, root, bin) %{_sysconfdir}/gnu/a2ps.cfg
%config %class(preserve) %attr (0644, root, bin) %{_sysconfdir}/gnu/a2ps-site.cfg
%attr (0755, root, lp) %{_sysconfdir}/lp/fd/a2ps.fd

%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, root) %{_datadir}/a2ps
%dir %attr (0755, root, root) %{_datadir}/a2ps/afm
%dir %attr (0755, root, root) %{_datadir}/a2ps/encoding
%dir %attr (0755, root, root) %{_datadir}/a2ps/fonts
%dir %attr (0755, root, root) %{_datadir}/a2ps/ppd
%dir %attr (0755, root, root) %{_datadir}/a2ps/ps
%dir %attr (0755, root, root) %{_datadir}/a2ps/sheets
%dir %attr (0755, root, root) %{_datadir}/ogonkify
%dir %attr (0755, root, root) %{_datadir}/ogonkify/afm
%dir %attr (0755, root, root) %{_datadir}/ogonkify/fonts
%attr (0755, root, bin) %{_datadir}/a2ps/README
%attr (0755, root, bin) %{_datadir}/ogonkify/README
%attr (0755, root, bin) %{_datadir}/ogonkify/*.enc
%attr (0755, root, bin) %{_datadir}/ogonkify/*.ps
%{_datadir}/a2ps/afm/*
%{_datadir}/a2ps/encoding/*
%{_datadir}/a2ps/fonts/*
%{_datadir}/a2ps/ppd/*
%{_datadir}/a2ps/ps/*
%{_datadir}/a2ps/sheets/*
%{_datadir}/ogonkify/afm/*
%{_datadir}/ogonkify/fonts/*

%dir %attr (0755, root, bin) %{_infodir}
%{_infodir}/*
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*

%dir %attr (0755, root, bin) %{_basedir}/sfw
%dir %attr (0755, root, bin) %{_basedir}/sfw/bin
%{_basedir}/sfw/bin/*

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_localedir}
%{_localedir}/*

%changelog
* Fri Feb 06 2009 - moinakg@gmail.com
- Initial spec (migrated and merged from SFW gate).

