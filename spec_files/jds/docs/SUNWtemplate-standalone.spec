#
# spec file for package SUNWfoo
#
# Copyright 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

####################################################################
# This is a simple example where we don't use Linux spec files
# For a template of a typical JDS package, where we can build
# the same stuff on Linux and Solaris, see SUNWtemplate.spec
####################################################################

%include Solaris.inc

Name:                    SUNWfoo
Summary:                 foo libraries - This program does foo
# use the version number of the community package if possible, but
# don't include non-numerics, like 6.2b or 1.5.1alpha
Version:                 0.0.0
# make sure the Source is a url that actually works
Source:			 
# Use -p1 unified diffs (see man patch)
Patch1:			 
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
# Use the copyright-extractor script to create a copyright file.
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
# add build and runtime dependencies here:
BuildRequires: SUNWbar-devel
Requires: SUNWbar
# the base pkg should depend on the -root subpkg, if there is one:
Requires: %{name}-root

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

#Please DON'T create share pkgs, we stopped using them in JDS4
#%package share   (delete me)

%package devel
Summary:		 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
Requires:                %{name} = %{version}
%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                 foo - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

#
## runtime pkgs:
#
# SUNWpackage-name:                    the main package, binaries, libs,
#                                      file in %{_datadir} needed at runtime
# SUNWpackage-name-root:               /etc, /var stuff
#
## development pkgs:
#
# SUNWpackage-name-devel:              include files, pkgconfig files,
#                                      files in %{_datadir}, like aclocal
#                                      macros and gtk-docs and
#                                      binaries only needed for development
# SUNWpackage-name-devel-root:         any root files that are only needed
#                                      for development


%prep
%setup -q -n foo-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="%{_ldflags}"
export MSGFMT="/usr/bin/msgfmt"

./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --sysconfdir=%{_sysconfdir}		\
	    --includedir=%{_includedir}		\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}

make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/*.la

#
# when not building -l10n packages, remove anything l10n related from
# $RPM_BUILD_ROOT
#
%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/[a-z]*
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z]*.omf
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%{_datadir}/foo
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

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

#
# The files included here should match the ones removed in %install
#
%if %build_l10n
%files l10n
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/locale
%{_datadir}/gnome/help/*/[a-z]*
%{_datadir}/omf/*/*-[a-z]*.omf
%endif

%changelog
* Fri Jun  2 2006 - laca@sun.com
- Initial spec
