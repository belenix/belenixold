#
# spec file for package SFEcompizconfig-python
####################################################################
# Python bindings for the compizconfig library
####################################################################
#
# Copyright 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: erwannc


%include Solaris.inc

%define src_name compizconfig-python

Name:                    SFEcompizconfig-python
Summary:                 compizconfig libraries - is an alternative configuration system for compiz
Version:                 0.7.8
Source:			 http://releases.compiz-fusion.org/%{version}/%{src_name}-%{version}.tar.bz2
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright

%ifnarch sparc
# these packages are only avavilable on x86
# =========================================

BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
# add build and runtime dependencies here:
BuildRequires:  SUNWPython-devel
BuildRequires:  SFElibcompizconfig
BuildRequires:  SUNWpython-setuptools
Requires:       SUNWPython
Requires:       SFElibcompizconfig

%package devel
Summary:		 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
Requires:                %{name} = %{version}
%include default-depend.inc

%define pythonver 2.4

%prep
%setup -q -n %{src_name}-%version

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
            --libdir=%{_libdir}

make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages

rm -f $RPM_BUILD_ROOT%{_libdir}/*.*a
rm -f $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{pythonver}/vendor-packages/*
%doc(bzip2) COPYING
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

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
- Moved to SFO
* Wed Nov 14 2007 - daymobrew@users.sourceforge.net
- Add l10n package.
* Mon Oct 29 2007 - trisk@acm.jhu.edu
- Bump to 0.6.0.1
* Fri Sep 07 2007 - trisk@acm.jhu.edu
- Update rules, fix Python library location
* Fri Aug  14 2007 - erwann@sun.com
- Initial spec
