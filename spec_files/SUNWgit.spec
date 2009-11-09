#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# spec file for package SUNWgit
#
# includes module(s): git
#
%include Solaris.inc

Name:                    SUNWgit
Summary:                 git - GNU Any to PostScript filter (root)
Version:                 1.6.5.2
URL:                     http://git-scm.com/
Source:                  http://kernel.org/pub/software/scm/git/git-%{version}.tar.bz2
Source1:                 http://www.kernel.org/pub/software/scm/git/git-manpages-%{version}.tar.bz2
SUNW_BaseDir:            /
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWperl584core
Requires: SUNWperl584usr
Requires: SUNWlexpt
Requires: SUNWTk
Requires: SUNWxcu4
Requires: SUNWbash
Requires: SUNWTcl
Requires: SUNWzlib
Requires: SUNWcurl
Requires: SUNWgzip

%prep
%setup -q -c -n %{name}-%{version}
bunzip2 -c %{SOURCE1} | gtar xf -

%build
cd git-%{version}
LDFLAGS="%_ldflags %{sfw_lib_path}"
CFLAGS="%optflags -I%{sfw_inc}"
PATH=${PATH}:%{sfw_bin}
PERL_LIB=`/usr/perl5/bin/perl -MConfig -e 'print "$Config{installvendorarch}"'`
export CC LDFLAGS CFLAGS PATH INSTALL

(cd perl
 [ ! -f Makefile.orig ] && cp Makefile Makefile.orig
 rm -f Makefile
 sed -e "s|\$(prefix)/lib|${PERL_LIB}|" \
     -e 's|echo $(DESTDIR)|echo |' Makefile.orig > Makefile )

# -e "s|.(instdir_SQ|\$(DESTDIR)&|g" 
./configure --prefix=%{_prefix} \
            --libexecdir=%{_libexecdir} \
            --without-openssl

DESTDIR=${RPM_BUILD_ROOT} \
PERL_PATH=/usr/perl5/bin/perl \
NO_PERL_MAKEMAKER=1 \
V=1 \
/usr/bin/gmake prefix=%{_prefix} all

%install
cd git-%{version}
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
DESTDIR=${RPM_BUILD_ROOT} /usr/bin/gmake prefix=%{_prefix} install
cd ..

mkdir -p $RPM_BUILD_ROOT%{_mandir}
cp -r man* $RPM_BUILD_ROOT%{_mandir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*
%dir %attr (0755, root, bin) %{_datadir}/gitk
%{_datadir}/gitk/*
%dir %attr (0755, root, bin) %{_datadir}/git-gui
%{_datadir}/git-gui/*
%dir %attr (0755, root, bin) %{_datadir}/git-core
%{_datadir}/git-core/*

%dir %attr (0755, root, bin) %{_basedir}/perl5
%dir %attr (0755, root, bin) %{_basedir}/perl5/vendor_perl
%dir %attr (0755, root, bin) %{_basedir}/perl5/vendor_perl/5.8.4
%dir %attr (0755, root, bin) %{_basedir}/perl5/vendor_perl/5.8.4/i86pc-solaris-64int
%attr (0444, root, bin) %{_basedir}/perl5/vendor_perl/5.8.4/i86pc-solaris-64int/*

%changelog
* Fri Feb 06 2009 - moinakg@gmail.com
- Initial spec (migrated and merged from SFW gate).

