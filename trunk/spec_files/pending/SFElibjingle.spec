#
# spec file for package SFElibjingle
#
# includes module(s): libjingle
#
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc


Name:                    SFElibjingle
Summary:                 Google Talk's implementation of Jingle and Jingle-Audio
Version:                 0.4.0
Source:                  %{sf_download}/libjingle/libjingle-%{version}.tar.gz
Patch1:                  libjingle-01-unixfilesystem.cc.diff

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlexpt
Requires: SUNWopenssl-libraries
BuildRequires: SUNWopenssl-include
Requires: SFEgccruntime
BuildRequires: SFEgcc

%prep
%setup -q -c -n %name-%version
cd libjingle-%version
%patch1 -p1

cp talk/base/basictypes.h talk/base/basictypes.h.orig
chmod +w talk/base/basictypes.h
cat talk/base/basictypes.h.orig | sed "{
s/typedef char int8;/typedef char int8;\n#include <string.h>/
}" > talk/base/basictypes.h

cp talk/base/network.cc talk/base/network.cc.orig
chmod +w talk/base/network.cc
cat talk/base/network.cc.orig | sed "{
s@#include <net/if.h>@#include <net/if.h>\n#include <sys/sockio.h>@
}" > talk/base/network.cc

cp talk/base/asynctcpsocket.cc talk/base/asynctcpsocket.cc.orig
chmod +w talk/base/asynctcpsocket.cc
cat talk/base/asynctcpsocket.cc.orig | sed "{
s@#include \"talk/base/logging.h\"@#include \"talk/base/logging.h\"\n#include <string.h>@
s@std::strerror@strerror@g
}" > talk/base/asynctcpsocket.cc

for fl in talk/base/stringutils.h talk/base/base64.h talk/xmpp/xmppclient.h \
          talk/p2p/base/sessionmanager.h talk/base/host.cc talk/base/cryptstring.h \
          talk/base/urlencode.h talk/base/testclient.cc talk/base/socketadapters.cc \
          talk/base/natserver.cc talk/base/natsocketfactory.cc talk/base/host.h \
          talk/p2p/base/stun.cc talk/p2p/base/port.cc talk/p2p/base/relayport.cc \
          talk/p2p/base/relayserver_main.cc talk/p2p/base/stunserver.cc \
          talk/p2p/base/stunserver_main.cc talk/p2p/base/session_unittest.cc \
          talk/session/fileshare/fileshare.cc talk/examples/pcp/pcp_main.cc
do
	cp ${fl} ${fl}.orig
	chmod +w ${fl}
        if [ "$fl" = "talk/base/stringutils.h" ]; then
		cat ${fl}.orig | sed "{
		s@Traits<char>::@@
		s@#include <stdio.h>@#include <stdio.h>\n#include <stdlib.h>\n#include <strings.h>@
		}" > ${fl}
	elif [ "$fl" = "talk/base/cryptstring.h" -o "$fl" = "talk/base/urlencode.h" ]; then
		cat ${fl}.orig | sed "{
		s@#include <string>@#include <string>\n#include <string.h>\n#include <stdlib.h>@
		}" > ${fl}
	elif [ "$fl" = "talk/base/testclient.cc" -o \
		"$fl" = "talk/base/socketadapters.cc" -o \
		"$fl" = "talk/base/natserver.cc" -o \
		"$fl" = "talk/base/natsocketfactory.cc" -o \
		"$fl" = "talk/p2p/base/stun.cc" -o \
		"$fl" = "talk/p2p/base/port.cc" -o \
		"$fl" = "talk/p2p/base/relayport.cc" -o \
		"$fl" = "talk/p2p/base/relayserver_main.cc" -o \
		"$fl" = "talk/p2p/base/stunserver.cc" -o \
		"$fl" = "talk/p2p/base/stunserver_main.cc" -o \
		"$fl" = "talk/p2p/base/session_unittest.cc" ]; then
		cat ${fl}.orig | sed "{
		s@std::strerror@strerror@g
		s@std::memcmp@memcmp@g
		s@std::memcpy@memcpy@g
		}" > ${fl}
	elif [ "$fl" = "talk/base/host.h" ]; then
		cat ${fl}.orig | sed "{
		s@include <string>@include <string>\n#include <stdlib.h>@
		}" > ${fl}
	elif [ "$fl" = "talk/session/fileshare/fileshare.cc" ]; then
		cat ${fl}.orig | sed "{
		s@_min@_min<unsigned int>@
		}" > ${fl}
	elif [ "$fl" = "talk/examples/pcp/pcp_main.cc" ]; then
		cat ${fl}.orig | sed "{
		s@#include <sys/wait.h>@#include <sys/wait.h>\n#include <sys/termios.h>@
		}" > ${fl}
	else
		cat ${fl}.orig | sed '{
		s@Traits<char>::@@
		s@Base64::@@
		s@std::exit@exit@
		s@XmppClient::@@
		s@SessionManager::CreateErrorMessage@CreateErrorMessage@
		}' > ${fl}
	fi
done

for fl in talk/base/httpbase.cc talk/base/httpbase.h talk/base/httpclient.cc \
          talk/base/tarstream.cc talk/base/tarstream.h
do
	cp ${fl} ${fl}.orig
	chmod +w ${fl}
	cat ${fl}.orig | sed '{
	s@M_NONE@J_M_NONE@g
	s@M_READ@J_M_READ@g
	s@M_WRITE@J_M_WRITE@g
	}' > ${fl}
done

cd ..

%ifarch amd64 sparcv9
cp -rp libjingle-%{version} libjingle-%{version}-64
%endif

%if %cc_is_gcc
%else
%error "This spec file needs Gcc4. Please set your CC and CXX environment variables."
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

%ifarch amd64 sparcv9
cd libjingle-%{version}-64
export CFLAGS="%optflags64"
export CXXFLAGS="%cxx_optflags64"
export LDFLAGS="%_ldflags64 -lsocket -lnsl -R/usr/gnu/lib/%{_arch64} -L/usr/gnu/lib/%{_arch64} -L/usr/sfw/lib/%{_arch64} -R/usr/sfw/lib/%{_arch64}"

libtoolize --force --copy
aclocal
autoconf --force

bash ./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --bindir=%{_bindir}/%{_arch64}              \
            --libdir=%{_libdir}/%{_arch64}

make -j$CPUS 
cd ..
%endif

cd libjingle-%{version}
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags -lsocket -lnsl -R/usr/gnu/lib -L/usr/gnu/lib -L/usr/sfw/lib -R/usr/sfw/lib"

libtoolize --force --copy
aclocal
autoconf --force

bash ./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --bindir=%{_bindir}              \
            --libdir=%{_libdir}

make -j$CPUS
cd ..


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd libjingle-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.la
cd ..
%endif

cd libjingle-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
cd ..

exit 1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/relayserver
%{_bindir}/stunserver
%{_bindir}/pcp
%{_bindir}/login

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/relayserver
%{_bindir}/%{_arch64}/stunserver
%{_bindir}/%{_arch64}/pcp
%{_bindir}/%{_arch64}/login
%endif

%changelog
* Mon May 8 2006 - drdoug007@yahoo.com.au
- Initial version
