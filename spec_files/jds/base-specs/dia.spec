#
# spec file for package dia
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: mattman
#

Name:           dia
Summary:        Dia Diagram Editor
Version:        0.96.1
Source:		    http://ftp.gnome.org/pub/GNOME/sources/dia/0.96/dia-%{version}.tar.bz2
Source1:	l10n-configure.sh
# date:2008-10-23 type:bug owner:mattman bugzilla:558263
Patch1:		dia-01-remove-stdc++.diff
# date:2008-10-24 type:bug owner:mattman bugzilla:558264
Patch2:		dia-02-use-so-plugins.diff
# date:2008-10-31 type:bug owner:mattman bugzilla:558690
Patch3:		dia-03-help-docs.diff
# date:2008-12-03 type:bug owner:mattman bugzilla:563106 bugster:6779724
Patch4:		dia-04-gtk-spin-button.diff
# date:2008-12-22 type:bug owner:fujiwara bugzilla:564850 bugster:6786116 state:upstream
Patch5:		dia-05-g11n-filename.diff
## http://svn.gnome.org/viewvc/dia/trunk/app/app_procs.c?r1=3838&r2=3897&view=patch
# date:2009-01-06 type:feature owner:fujiwara state:upstream
Patch6:		dia-06-goption.diff
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %name-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

libtoolize --copy --force
intltoolize --automake --force --copy

bash -x %SOURCE1 --enable-copyright

aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f 
autoconf

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-gnome                   \
            --with-cairo                     \
            --disable-static

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm  $RPM_BUILD_ROOT%{_libdir}/dia/*.la
rmdir  $RPM_BUILD_ROOT%{_datadir}/oaf

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue Jan 06 2009 - takao.fujiwara@sun.com
- Add l10n-configure.sh for copyright.
- Add patch goption.diff from trunk.
* Mon Dec 22 2008 - takao.fujiwara@sun.com
- Add patch g11n-filename.diff to fix crash on none UTF-8.
* Wed Dec 03 2008 - Matt.Keenan@sun.com
- Fix GtkSpinButton warnings because of new gtk bugster:6779724, bugzilla:563106
* Wed Oct 22 2008 - Matt.Keenan@sun.com
- created
