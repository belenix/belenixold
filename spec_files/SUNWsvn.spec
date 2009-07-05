#
# spec file for package SFEsubversion
#
# includes module(s): subversion
#
%include Solaris.inc

Name:			SUNWsvn
License:		Apache,LGPL,BSD
Group:			system/dscm
Version:		1.5.6
Release:		1
Summary:		Subversion SCM
Source:			http://subversion.tigris.org/downloads/subversion-%{version}.tar.bz2

# Home-grown svn-config needed by kdesdk
Source1:                svn-config
Source2:                svn-libtool
Patch1:                 subversion-01-libneon.la.diff
Patch2:                 subversion-02-Makefile.diff
Patch3:                 subversion-03-swigutil_pl.c.diff
Patch4:                 subversion-05-core.c.diff
Patch5:                 subversion-04-Makefile.PL.in.diff

URL:			http://subversion.tigris.org/
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:		%{_prefix}
Requires: SUNWcsl
Requires: SUNWcsr
Requires: SFEgdbm
Requires: SUNWlibms
Requires: SUNWzlib
Requires: SUNWpostrun
Requires: SUNWopenssl-libraries
Requires: SUNWlexpt
Requires: SUNWneon
Requires: SFElibapr
BuildRequires: SUNWPython26
BuildRequires: SUNWopenssl-include
BuildRequires: SFEgdbm-devel
BuildRequires: SFElibapr-devel
BuildRequires: SUNWapch22u

%description
Subversion source code management system.

%package devel
Summary:                 Subversion headers
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
Requires:                SUNWbash
Requires: SUNWopenssl-include
Requires: SFEgdbm-devel
Requires: SUNWPython26
Requires: SUNWperl584core
Requires: SUNWperl584usr
Requires: SFElibapr-devel
Requires: SUNWapch22u

%package perl
Summary:                 Subversion Perl Bindings
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
Requires: SUNWperl584core
Requires: SUNWperl584usr

%package python
Summary:                 Subversion Python bindings
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
Requires: SUNWPython

%package java
Summary:                 Subversion Java bindings
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
Requires: SUNWj6rt

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n subversion-%{version}
%patch1 -p1 -b .patch01
%patch2 -p1 -b .patch02
%patch3 -p1 -b .patch03
%patch4 -p1 -b .patch04
%if %cc_is_gcc
%patch5 -p1 -b .patch05
%endif

%build
%if %cc_is_gcc
%else
export PATH=/usr/ccs/bin:/usr/bin:/usr/sbin:/bin:/usr/sfw/bin:/opt/SUNWspro/bin:/usr/gnu/bin
%endif
export CFLAGS="%optflags -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"
export LD=/usr/ccs/bin/ld
export LDFLAGS="%_ldflags -L$RPM_BUILD_ROOT%{_libdir} -Wl,-zmuldefs -L/lib -R/lib"
ln -s %{_bindir}/python2.6 python
export PATH=`pwd`:$PATH:%{_prefix}/apache2/2.2/bin
export ACLOCAL_FLAGS="-I build/ac-macros"

./autogen.sh
./configure \
    --prefix=%{_prefix} \
    --exec-prefix=%{_prefix} \
    --disable-static \
    --enable-shared \
    --with-pic \
    --with-installbuilddir=%{_datadir}/apr/build \
    --disable-mod-activation \
    --mandir=%{_mandir} \
    --with-ssl \
    --infodir=%{_infodir} \
    --without-berkeley-db \
    --with-apr=%{gnu_bin}/apr-1-config \
    --with-apr-util=%{gnu_bin}/apu-1-config \
    --with-neon=%{_prefix} \
    --with-apxs=%{_prefix}/apache2/2.2/bin/apxs \
    --with-jdk=%{_prefix}/java \
    --enable-javahl \
    --with-swig --libdir=%{_libdir}/svn

cp %{SOURCE2} ./libtool
chmod +x ./libtool 

gmake
gmake swig-py
gmake swig-pl
gmake javahl

%install
rm -rf $RPM_BUILD_ROOT
export PATH=`pwd`:$PATH:%{_prefix}/apache2/2.2/bin

gmake install DESTDIR=$RPM_BUILD_ROOT
gmake install-swig-py DESTDIR=$RPM_BUILD_ROOT
gmake install-swig-pl DESTDIR=$RPM_BUILD_ROOT
gmake install-javahl DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_infodir}
rm -rf $RPM_BUILD_ROOT%{_mandir}/man1
rm -rf $RPM_BUILD_ROOT%{_mandir}/man5
rm -rf $RPM_BUILD_ROOT%{_mandir}/man8

rm -f $RPM_BUILD_ROOT%{_libdir}/svn/lib*a
rm -f $RPM_BUILD_ROOT%{_libdir}/svn/*.exp

cp %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}

# Patch svn-config with the correct version
cat $RPM_BUILD_ROOT%{_bindir}/svn-config | sed s/SVN_VERSION/%{version}/ > $RPM_BUILD_ROOT%{_bindir}/svn-config.new
mv $RPM_BUILD_ROOT%{_bindir}/svn-config.new $RPM_BUILD_ROOT%{_bindir}/svn-config
chmod 0755 $RPM_BUILD_ROOT%{_bindir}/svn-config

#
# Put Java binding in correct location
#
mkdir -p $RPM_BUILD_ROOT%{_datadir}/lib/java
mv $RPM_BUILD_ROOT%{_libdir}/svn/svn-javahl/svn-javahl.jar $RPM_BUILD_ROOT%{_datadir}/lib/java
rm -rf $RPM_BUILD_ROOT%{_libdir}/svn/svn-javahl

#
# Fix Perl binding path
#
mv $RPM_BUILD_ROOT%{_prefix}/perl5/site_perl $RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl
rm -rf $RPM_BUILD_ROOT%{_prefix}/perl5/5.8.4/lib

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/svn*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/svn/libsvn_client*
%{_libdir}/svn/libsvn_delta*
%{_libdir}/svn/libsvn_diff*
%{_libdir}/svn/libsvn_fs*
%{_libdir}/svn/libsvn_ra*
%{_libdir}/svn/libsvn_repos*
%{_libdir}/svn/libsvn_subr*
%{_libdir}/svn/libsvn_wc*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}

#
# TODO: Commented till we send SUNWsfman to the dustbin!
#
#%dir %attr (0755, root, bin) %{_mandir}/man1
#%{_mandir}/man1/*
#%dir %attr (0755, root, bin) %{_mandir}/man5
#%{_mandir}/man5/*
#%dir %attr (0755, root, bin) %{_mandir}/man8
#%{_mandir}/man8/*
%{_prefix}/apache2

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%files perl
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}/perl5
%dir %attr (0755, root, bin) %{_prefix}/perl5/5.8.4
%dir %attr (0755, root, bin) %{_prefix}/perl5/5.8.4/man
%dir %attr (0755, root, bin) %{_prefix}/perl5/5.8.4/man/man3
%{_prefix}/perl5/5.8.4/man/man3/*
%dir %attr (0755, root, bin) %{_prefix}/perl5/vendor_perl
%attr (0755, root, bin) %{_prefix}/perl5/vendor_perl/5.8.4
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/svn/libsvn_swig_perl*

%files python
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}/python2.4
%attr (0755, root, bin) %{_libdir}/python2.4/vendor-packages
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/svn/libsvn_swig_py*

%files java
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/svn/libsvnjava*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, sys) %{_datadir}/lib
%dir %attr (0755, root, sys) %{_datadir}/lib/java
%{_datadir}/lib/java/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sun Jul 05 2009 - moinakg<at>gmail(dot)com
- Bump version, add new patches and update build to use system apr lib.
* Fri Jan 09 2009 - moinakg@belenix.org
- Initial version derived from SFEsubversion and SFW gate.
