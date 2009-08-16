#
# spec file for package SUNWlibcompizconfig
####################################################################
# Libcompizconfig is an alternative configuration system for compiz
####################################################################
#
# Copyright 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: erwannc
#


%include Solaris.inc

%define src_name libcompizconfig
%define  gnu_share /usr/gnu/share

Name:                    SFElibcompizconfig
Summary:                 compizconfig libraries - is an alternative configuration system for compiz
Version:                 0.7.8
Source:			 http://releases.compiz-fusion.org/%{version}/%{src_name}-%{version}.tar.bz2
Patch1:			 libcompizconfig-01-solaris-port.diff
Patch2:			 libcompizconfig-02-no-null-def.diff
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright

%ifnarch sparc
# these packages are only avavilable on x86
# =========================================

BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
# add build and runtime dependencies here:
BuildRequires:  SFEcompiz
Requires:	SFEcompiz
# the base pkg should depend on the -root subpkg, if there is one:
Requires: %{name}-root

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package devel
Summary:		 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
Requires:                %{name} = %{version}
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%version
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

rm -f ltmain.sh
libtoolize --force

%if %cc_is_gcc
aclocal -I%{gnu_share}/aclocal
%else
aclocal
%endif

autoheader
automake -a -c -f
autoconf

export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="%{_ldflags} -L/usr/X11/lib -L/usr/openwin/lib -R/usr/X11/lib -R/usr/openwin/lib -lX11 -lXext"
export MSGFMT="/usr/bin/msgfmt"

./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --sysconfdir=%{_sysconfdir}		\
	    --includedir=%{_includedir}		\
            --libdir=%{_libdir}

make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.*a
rm -f $RPM_BUILD_ROOT%{_libdir}/compiz/*.*a
rm -f $RPM_BUILD_ROOT%{_libdir}/compizconfig/backends/*.*a

# Remove the empty locale dir.
rmdir $RPM_BUILD_ROOT%{_datadir}/locale

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/compiz
%{_libdir}/compizconfig
%{_libdir}/lib*.so*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, other) %{_datadir}/compiz
%{_datadir}/compiz/*
%{_datadir}/compizconfig/*
%doc(bzip2) COPYING
%dir %attr (0755, root, other) %{_datadir}/doc

%files root
%defattr (0755, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

# endif for "ifnarch sparc"
%endif

%changelog
* Sat Aug 15 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Fix build with SFEgcc.
* Sun May 03 2009 - moinakg@belenix.org
- Copy over updated spec from JDS repo.
* Sun Feb 22 2009 - dave.lin@sun.com
- Add patch 02-no-null-def.diff to fix nudefined symbol NULL issue.
* Wed Sep 17 2008 - matt.keenn@sun.com
- Update copyright
* Tue Jun 01 2008 - damien.carbery@sun.com
- Fix perms in %files.
* Wed Mar 26 2008 - dave.lin@sun.com
- change to not build this component on SPARC
* Fri Mar 07 2008 - damien.carbery@sun.com
- Move %{_datadir} files from root pkg to base pkg.
* Mon Feb 18 2008 - damien.carbery@sun.com
- Remove l10n stuff as there are no l10n files installed. Remove empty
  %{_datadir}/locale during %install.
* Wed Feb 13 2008 - erwann@sun.com
- moved to SFO
* Wed Nov 14 2007 - daymobrew@users.sourceforge.net
- Add l10n package.
* Mon Oct 29 2007 - trisk@acm.jhu.edu
- Bump to 0.6.0
* Sat Sep 15 2007 - trisk@acm.jhu.edu
- Fix patch rule
* Sat Sep 08 2007 - trisk@acm.jhu.edu
- Update rules
* Fri Aug 31 2007 - trisk@acm.jhu.edu
- Fix duplicate package contents
* Fri Aug  14 2007 - erwann@sun.com
- Initial spec
