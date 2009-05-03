#
# spec file for package  SUNWcompizconfig-backend-gconf
####################################################################
# The gconf backend for CompizConfig. It uses the Gnome configuration
# system and provides integration into the Gnome desktop environment.
####################################################################
#
# Copyright 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
# 
# Owner: erwannc


%include Solaris.inc

%define src_name compizconfig-backend-gconf

Name:                    SFEcompizconfig-gconf
Summary:                 cgconf backend for CompizConfig
Version:                 0.7.8
Source:			 http://releases.compiz-fusion.org/%{version}/%{src_name}-%{version}.tar.bz2
Patch1:			 compizconfig-backend-gconf-01-solaris-port.diff
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright

%ifnarch sparc
# these packages are only avavilable on x86
# =========================================

BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
# add build and runtime dependencies here:
BuildRequires:	SUNWgnome-libs-devel
BuildRequires:	SUNWgnome-config-devel
BuildRequires:  SFElibcompizconfig
Requires:	SUNWgnome-libs
Requires:	SUNWgnome-config
Requires:	SFElibcompizconfig

%prep
%setup -q -n %{src_name}-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

rm -f ltmain.sh
libtoolize --force
aclocal
autoheader
automake -a -c -f
autoconf

export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="%{_ldflags}"
export MSGFMT="/usr/bin/msgfmt"

./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --sysconfdir=%{_sysconfdir}		\
	    --includedir=%{_includedir}		\
            --libdir=%{_libdir}

make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/compizconfig/backends/*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/compizconfig
%{_libdir}/compizconfig/*
%doc(bzip2) COPYING
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc

# endif for "ifnarch sparc"
%endif

%changelog
* Sun May 03 2009 - moinakg@belenix.org
- Copy over updated spec from JDS repo.
* Wed Sep 17 2008 - matt.keenn@sun.com
- Update copyright
* Wed Mar 26 2008 - dave.lin@sun.com
- change to not build this component on SPARC
* Wed Feb 13 2008 - erwann@sun.com
- moved to SFO
* Wed Nov 14 2007 - daymobrew@users.sourceforge.net
- Add l10n package.
* Mon Oct 29 2007 - trisk@acm.jhu.edu
- Bump to 0.6.0
* Fri Sep 07 2007 - trisk@acm.jhu.edu
- Update rules
* Fri Aug  14 2007 - erwann@sun.com
- Initial spec
