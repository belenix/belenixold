#
# spec file for package SFEcurl
#
# includes module(s): curl
#
Name:                    SFEcurl
Summary:                 curl - Get a file from FTP or HTTP server.
Version:                 7.19.0
URL:                     http://curl.haxx.se/
Source:                  http://curl.haxx.se/download/curl-%{version}.tar.bz2
Patch0:                  curl-01-Makefile.in.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWopenssl-libraries
Requires: SUNWopensslr
BuildRequires: SUNWopenssl-include
Requires: SUNWzlib

%prep
rm -rf %name-%version
%setup -q -n curl-%version
%patch0 -p1

%build

#
# Patch -lgssapi to -lgss in configure
#
if [ ! -f configure.orig ]
then
	cp configure configure.orig
fi
cat configure.orig | sed 's/-lgssapi/-lgss/' > configure

./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --includedir=%{_includedir}		\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}                 \
            --enable-rpath			\
	    --with-ssl=%{_prefix}               \
	    --with-gssapi-includes=%{_prefix}/include/gssapi \
	    --with-gssapi-libs=%{_prefix}/lib

make -j $CPUS all

%install
make DESTDIR=${RPM_BUILD_ROOT} install

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Fri Sep 18 2009 - moinakg(at)belenix<dot>org
- OpenSSL is now located in /lib.
* Tue Oct 28 2008 - moinakg@belenix.org
- Bump version, pull in patch from SFW gate and fix make invocation.
* Wed Dec 12 2997   Michal Bielicki
- split into base and non base spec to be able to do the 64bit stuff righ
* Mon Nov 26 2007 - Thomas Wagner
- move SFEcurl into /usr/gnu by %include usr-gnu.inc (never OS builds have SUNWcurl)
* Mon Oct 29 2007 - brian.cameron@sun.com
- Bump to 7.17.1
* Tue Sep 18 2007 - nonsea@users.sourceforge.net
- Bump to 7.17.0
* Mon May 28 2007 - Thomas Wagner
- bump to 7.16.2
- --disable-static
* Thu Feb 15 2007 - laca@sun.com
- bump to 7.16.1
* Wed Jan  3 2007 - laca@sun.com
- bump to 7.16.0
* Fri Jun 23 2006 - laca@sun.com
- rename to SFEcurl
- delete -share subpkg
- update attributes to match JDS
- add missing deps
* Sun May 14 2006 - mike kiedrowski (lakeside-AT-cybrzn-DOT-com)
- Delete *.la.
* Mon Apr  3 2006 - mike kiedrowski (lakeside-AT-cybrzn-DOT-com)
- Initial spec

