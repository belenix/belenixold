#
# spec file for package SFEliveMedia
#
# includes module(s): liveMedia
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

Name:                    SFEliveMedia
Summary:                 liveMedia - live555 Streaming Media
Version:                 2009.04.20
Source:                  http://www.live555.com/liveMedia/public/live.%{version}.tar.gz
Patch1:                  liveMedia-01-SOLARIS-macro.diff
Patch2:                  liveMedia-02-config.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -c -n %name-%version
cd live
%patch1 -p1
%patch2 -p1
cd ..

%ifarch amd64 sparcv9
cp -rp live live-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

%ifarch amd64 sparcv9
cd live-64
./genMakefiles solaris-64bit
make -j$CPUS
cd ..
%endif

cd live
./genMakefiles solaris-32bit
make -j$CPUS 
cd ..

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/lib/live

%ifarch amd64 sparcv9
cd live-64

gtar fcp - liveMedia/libliveMedia.so groupsock/libgroupsock.so UsageEnvironment/libUsageEnvironment.so BasicUsageEnvironment/libBasicUsageEnvironment.so  | gtar -x -v -C $RPM_BUILD_ROOT/usr/lib/live -f -
mkdir -p $RPM_BUILD_ROOT/usr/lib/live/liveMedia/%{_arch64}
mv $RPM_BUILD_ROOT/usr/lib/live/liveMedia/libliveMedia.so $RPM_BUILD_ROOT/usr/lib/live/liveMedia/%{_arch64}
mkdir -p $RPM_BUILD_ROOT/usr/lib/live/groupsock/%{_arch64}
mv $RPM_BUILD_ROOT/usr/lib/live/groupsock/libgroupsock.so $RPM_BUILD_ROOT/usr/lib/live/groupsock/%{_arch64}
mkdir -p $RPM_BUILD_ROOT/usr/lib/live/UsageEnvironment/%{_arch64}
mv $RPM_BUILD_ROOT/usr/lib/live/UsageEnvironment/libUsageEnvironment.so $RPM_BUILD_ROOT/usr/lib/live/UsageEnvironment/%{_arch64}
mkdir -p $RPM_BUILD_ROOT/usr/lib/live/BasicUsageEnvironment/%{_arch64}
mv $RPM_BUILD_ROOT/usr/lib/live/BasicUsageEnvironment/libBasicUsageEnvironment.so $RPM_BUILD_ROOT/usr/lib/live/BasicUsageEnvironment/%{_arch64}

cd ..
%endif

cd live
gtar fcp - liveMedia/include groupsock/include UsageEnvironment/include BasicUsageEnvironment/include liveMedia/libliveMedia.so groupsock/libgroupsock.so UsageEnvironment/libUsageEnvironment.so BasicUsageEnvironment/libBasicUsageEnvironment.so  | gtar -x -v -C $RPM_BUILD_ROOT/usr/lib/live -f -
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%changelog
* Tue Apr 28 2009 - moinakg@belenix.org
- Bump version to 2009.04.20 and add 64Bit build.
* Tue Feb 12 2008 <pradhap (at) gmail.com>
- Bumped up the version to 2008.02.08
* Thu Dec 27 2007 - Thomas Wagner
- bump to 2007.12.27
* Mon Nov 5 2007 - markwright@internode.on.net
- Bump to 2007.11.01.  Add patch2 to use /usr/gnu/bin/ld and build
- shared libraries instead of static.
* Tue Sep 04 2007 - ananth@sun.com
- Bump to 2007.08.03a
* Wed Jul 25 2007 - daymobrew@users.sourceforge.net
- Bump to 2007.07.25.
* Fri Jul 13 2007 - dougs@truemail.co.th
- Bump to 2007.07.10.
* Tue Jun  5 2007 - dougs@truemail.co.th
- Bump to 2007.05.24.
* Sat Apr 21 2007 - dougs@truemail.co.th
- Bump to 2007.04.20.
* Fri Mar 30 2007 - daymobrew@users.souceforge.net
- Bump to 2007.02.20.
* Wed Jan 11 2007 - laca@sun.com
- bump to 2007.01.11
* Wed Jan  3 2007 - laca@sun.com
- bump to 2006.12.31, add patch SOLARIS-macro.diff
* Thu Dec 14 2006 - daymobrew@users.sourceforge.net
- Bump to 2006.12.08.
* Mon Nov  6 2006 - laca@sun.com
- bump to 2006.10.27
* Thu Sep 26 2006 - halton.huo@sun.com
- Bump to version 2006.09.20.
* Thu Jul 27 2006 - halton.huo@sun.com
- Bump to version 2006.07.04.
* Fri Jun 23 2006 - laca@sun.com
- Bumped to version 2006.06.22
- updated file attributes
- renamed to SFEliveMedia
* Mon Jun 13 2006 - drdoug007@yahoo.com.au
- Bumped version to 2006.05.17
* Mon May 8 2006 - drdoug007@yahoo.com.au
- Initial version
