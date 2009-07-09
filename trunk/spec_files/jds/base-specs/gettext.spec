#
# spec file for package gettext
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: laca
# bugdb: https://savannah.gnu.org/bugs/?group=gettext
#
Name:			gettext-tools
License:		GPL
Group:			system/library
# Don't upgrade to 0.17 and later for now as it's licensed GPLv3
# and we don't have a policy around GPLv3 code yet (as of 2008-04-14)
Version:		0.16.1
Release:		1
Distribution:		Sun Java Desktop System
Vendor:			Sun Microsystems, Inc.
Summary:		GNU gettext tools
Source:			http://ftp.gnu.org/pub/gnu/gettext/gettext-%{version}.tar.gz
URL:			http://www.gnu.org/
BuildRoot:		%{_tmppath}/%{name}-%{version}-build

%define gettextdir %{_libdir}/intltool/gettext-tools

%description
GNU gettext tools for use in intltool in the JDS build environment

%prep
%setup -q -n gettext-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi
CFLAGS="$RPM_OPT_FLAGS"		\
./configure --disable-nls \
    --prefix=%{_prefix} \
    --bindir=%{gettextdir} \
    --libdir=%{gettextdir}/lib \
    --datadir=%{gettextdir}/share \
    --includedir=%{gettextdir}/include \
    --without-emacs
old_IFS="$IFS"
IFS=:
for d in $PATH; do
    test -x $d/libtool || continue
    cp $d/libtool gettext-runtime/libasprintf
    break
done
IFS="$old_IFS"
perl -pi -e 's,^LTCC=".*/(cc|gcc)"$,LTCC="'"$CC"'",' \
    gettext-runtime/libasprintf/libtool
perl -pi -e 's,^CC=".*/(cc|gcc)"$,CC="'"$CC"'",' \
    gettext-runtime/libasprintf/libtool
perl -pi -e 's,^LTCC=".*/(CC|g\+\+)"$,LTCC="'"$CXX"'",' \
    gettext-runtime/libasprintf/libtool
perl -pi -e 's,^CC=".*/(CC|g\+\+)"$,CC="'"$CXX"'",' \
    gettext-runtime/libasprintf/libtool

make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{gettextdir}/share
rm -rf $RPM_BUILD_ROOT%{gettextdir}/include
rm -f $RPM_BUILD_ROOT%{gettextdir}/gettext
rm -f $RPM_BUILD_ROOT%{gettextdir}/msgfmt
rm -f $RPM_BUILD_ROOT%{gettextdir}/lib/*a
rm -rf $RPM_BUILD_ROOT%{_prefix}/info
rm -rf $RPM_BUILD_ROOT%{gettextdir}/share/emacs

rm -f $RPM_BUILD_ROOT%{gettextdir}/autopoint
rm -f $RPM_BUILD_ROOT%{gettextdir}/envsubst
rm -f $RPM_BUILD_ROOT%{gettextdir}/gettext*
rm -f $RPM_BUILD_ROOT%{gettextdir}/msg[acefgiu]*
rm -f $RPM_BUILD_ROOT%{gettextdir}/ngettext

rm -f $RPM_BUILD_ROOT%{gettextdir}/lib/libas*
rm -f $RPM_BUILD_ROOT%{gettextdir}/lib/preloa*
rm -rf $RPM_BUILD_ROOT%{gettextdir}/lib/gettext
rm -f $RPM_BUILD_ROOT%{gettextdir}/lib/libgettextpo*

# Change /usr/bin/perl to /usr/perl5/bin/perl. Preempting bugs like 5100958.
export PERL=/usr/perl5/bin/perl
cd $RPM_BUILD_ROOT%{_datadir}/doc/gettext/examples/hello-c++-kde/admin
for f in debianrules conf.change.pl cvs-clean.pl am_edit config.pl
do
  sed "s|/usr/bin/perl|$PERL|" $f >$f.$$
  mv $f.$$ $f
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
# this is just a skeleton spec file for use in SUNWgnome-common-devel.spec

%changelog
* Mon Apr 14 2008 - laca@sun.com
- unbump to 0.16.1
* Mon Dec 10 2007 - brian.cameron@sun.com
- Bump to 0.17.  Add patch gettext-01-fixlink.diff to fix build issue.
* Wed Oct 10 2007 - damien.carbery@sun.com
- Add code to %install to change the #!/usr/bin/perl to #!/usr/perl5/bin/perl
  to preempt bugs like 5100958.
* Mon Mar 12 2007 - laca@sun.com
- add --without-emacs option
* Tue Feb 27 2007  <brian.cameron@sun.com>
- Bump to 0.16.1.  Remove upstream patch.
* Mon May 01 2006  <laca@sun.com>
- integrate into the JDS build (copied from the JDS CBE)
* Fri Sep 02 2004  <laca@sun.com>
- remove unpackaged files
* Sat Oct 02 2004  <laca@sun.com>
- add %_datadir/gettext to %files
* Sun Sep 05 2004  <laca@sun.com>
- update to 0.14.1
- build and package the tools
- enable parallel build
* Fri Mar 05 2004  <laca@sun.com>
- fix %files
- change the pkg category
