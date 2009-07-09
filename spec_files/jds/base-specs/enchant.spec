#
# spec file for package enchant
#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: wangke
# bugdb: bugzilla.abisource.com
#

Name:     	enchant
License:	LGPL v2.1
Version: 	1.4.2
Release:	1
Vendor:		Sun Microsystems, Inc.
Distribution:	Java Desktop System
Copyright:	GPL
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
Docdir:         %{_datadir}/doc
Autoreqprov:    on
URL:		http://www.abisource.com/projects/enchant/
Source:		http://www.abisource.com/downloads/%{name}/%{version}/%{name}-%{version}.tar.gz
# date:2006-12-08 bugzilla:10667 owner:wangke type:bug
Patch1:         enchant-01-define_FILE.diff
# date:2008-11-19 owner:jefftsai type:branding
Patch2:         enchant-02-build-request-dict.diff
# This patch is applied until zemberek-server is implemented.
# date:2009-01-14 owner:fujiwara type:feature bugster:6793551
Patch3:         enchant-03-zemberek-segv.diff
# date:2009-01-14 owner:fujiwara type:feature
Patch4:         enchant-04-ordering.diff
Summary:	Generic spell checking library
Group:		Applications/Text

%description
Enchant is a generic spell checking library that presents an API/ABI to 
applications.

%files
%defattr(-, root, root)

%prep
%setup  -q -n %{name}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1


%build
%ifos linux
if [ -x /usr/bin/getconf ]; then
  CPUS=`getconf _NPROCESSORS_ONLN`
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

aclocal 
autoconf
automake -a -c -f
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --bindir=%{_bindir} \
    --sysconfdir=%{_sysconfdir} \
    --mandir=%{_mandir} \
    --infodir=%{_datadir}/info \
    --localstatedir=/var \
	--with-myspell-dir=/usr/share/spell/myspell \
    --disable-static

make -j $CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Jan 14 2009 - takao.fujiwara@sun.com
- Add patch zemberek-segv.diff to avoid segv on tr_TR.UTF-8
- Add patch ordering.diff so that we configure myspell by default.
* Wed Nov 19 2008 - jeff.cai@sun.com
- Add patch -02-build-request-dic to solve the build issue
  with SunStudio 12
* Mon Nov 10 2008 - jeff.cai@sun.com
- Remove patch -02-aspell-conversion.diff  because 
  it looks like not many users need to convert the local 
  aspell dictionary to myspell format. We don't like to 
  maintain a large Solaris only patch.
* Fri Oct 31 2008 - jeff.cai@sun.com
- Bump to 1.4.2
- Remove upstream patch -02-uninstalled-pc.diff
- Remove upstream patch -03-personaldic.diff
- Remove unused patch -02-aspell-conversion.diff
- Rework patch -01-define-FILE.diff
* Fri Oct 31 2008 - jeff.cai@sun.com
- Change the license tag.
* Mon Jul 07 2008 - jeff.cai@sun.com
- Move 'rm' lines to SUNgnome-spell.spec
* Sat Apr 28 2007 - irene.huang@sun.com
- split patch -03-personaldic.diff into two patches
  -03-personaldic.diff and -04-apsell-conversion.diff, since 
  -03 has been upsteamed to community and will be removed
  when enchant is bumped to a new version. 

* Sat Apr 28 2007 - irene.huang@sun.com
- change the dictionary path to /usr/share/spell/myspell
  this is the place where the dictionaries should go according
  to LASRC 2007/231, targeting build 65.

* Fri Apr 13 2007 - irene.huang@sun.com
- put enchant++.h back to the package. 

* Tue Apr 10 2007 - irene.huang@sun.com	
- Add patch enchant-02-personaldic.diff to enable personal dictionary support
  of enchant myspell backend and conversion of aspell personal dict to myspell
  format. Fixes bug 6529848 and 6529853.

* Wed Feb 14 2007 - jeff.cai@sun.com
- Make enchant use myspell instead of aspell.
- Add patch enchant-02-uninstalled-pc.diff to enable building in one spec file
  for gnome-spell and enchant.

* Mon Dec 11 2006 - damien.carbery@sun.com
- Remove unnecessary automake call; add autoconf and adjust aclocal calls.

* Fri Dec 08 2006 - damien.carbery@sun.com
- Initial spec.
