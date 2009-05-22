#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include usr-gnu.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

Name:                SFEcyrus-sasl
Summary:             Simple Authentication and Security Layer library
Version:             2.1.23
Source:              ftp://ftp.andrew.cmu.edu/pub/cyrus-mail/cyrus-sasl-%{version}.tar.gz
Source1:             saslauthd.xml
URL:                 http://asg.web.cmu.edu/sasl/
Patch1:              cyrus-sasl-01.diff
Patch2:              cyrus-sasl-02-ipc_doors.c.diff

SUNW_BaseDir:        /
SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWsqlite3
BuildRequires: SUNWsqlite3-devel
Requires: SUNWopenssl-libraries
BuildRequires: SUNWopenssl-include
Requires: SFElibntlm
BuildRequires: SFElibntlm-devel

%description
SASL is the Simple Authentication and Security Layer, a method
for adding authentication support to connection-based protocols.
To use SASL, a protocol includes a command for identifying and
authenticating a user to a server and for optionally negotiating
protection of subsequent protocol interactions. If its use is
negotiated, a security layer is inserted between the protocol
and the connection.

%prep
%setup -q -c -n %name-%version
cd cyrus-sasl-%{version}
%patch1 -p1
%patch2 -p1
cd ..

%ifarch amd64 sparcv9
cp -rp cyrus-sasl-%{version} cyrus-sasl-%{version}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

%ifarch amd64 sparcv9
cd cyrus-sasl-%{version}-64

export CFLAGS="%optflags64 -I%{gnu_inc} -I%{sfw_inc} -fno-strict-aliasing"
export LDFLAGS="-m64 %{gnu_lib_path64} %{sfw_lib_path64}"

./configure --prefix %{_prefix} \
           --sbindir=%{_sbindir}/%{_arch64}      \
           --libdir=%{_libdir}/%{_arch64}      \
           --with-plugindir=%{_libdir}/%{_arch64}/sasl2 \
           --enable-shared=yes \
           --enable-static=no \
           --with-dbpath=%{_sysconfdir}/sasldb2 \
           --sysconfdir %{_sysconfdir} \
           --mandir %{_mandir} \
           --with-ipctype=doors \
           --with-openssl=%{_prefix}/sfw

cp config.h config.h.orig
cat config.h.orig | sed '{
    s@#define WITH_DES@#define WITH_DES 1@
    s@#define WITH_RC4@#define WITH_RC4 1@
}' > config.h

make -j$CPUS
cd ..
%endif

cd cyrus-sasl-%{version}
export CFLAGS="%optflags -I%{gnu_inc} -I%{sfw_inc} -fno-strict-aliasing"
export LDFLAGS="%{gnu_lib_path} %{sfw_lib_path}"

./configure --prefix %{_prefix} \
           --sbindir=%{_sbindir}      \
           --libdir=%{_libdir}      \
           --enable-shared=yes \
           --enable-static=no \
           --with-dbpath=%{_sysconfdir}/sasldb2 \
           --sysconfdir %{_sysconfdir} \
           --mandir %{_mandir} \
           --with-ipctype=doors \
           --with-openssl=%{_prefix}/sfw

cp config.h config.h.orig
cat config.h.orig | sed '{
    s@#define WITH_DES@#define WITH_DES 1@
    s@#define WITH_RC4@#define WITH_RC4 1@
}' > config.h

make -j$CPUS
cd ..


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd cyrus-sasl-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT

rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.a
rm -f ${RPM_BUILD_ROOT}%{_libdir}/sasl2/*.la
if [ -d ${RPM_BUILD_ROOT}%{_libdir}/sasl2 ]
then
	mv ${RPM_BUILD_ROOT}%{_libdir}/sasl2 ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}
fi

cd ..
%endif

cd cyrus-sasl-%{version}
make install DESTDIR=$RPM_BUILD_ROOT

rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/sasl2/*.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.a

mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}/%{base_arch}
(cd ${RPM_BUILD_ROOT}%{_sbindir}
 for prg in pluginviewer saslauthd sasldblistusers2 saslpasswd2 testsaslauthd
 do
   mv ${prg} %{base_arch}/
   ln -sf ../../lib/isaexec ${prg}
 done)

mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/application
cp %{SOURCE1} ${RPM_BUILD_ROOT}/var/svc/manifest/application

cd ..


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) /usr
%dir %attr (0755, root, bin) %{_prefix}
%dir %attr (0755, root, bin) %{_prefix}/sbin
%hard %{_prefix}/sbin/pluginviewer
%hard %{_prefix}/sbin/saslauthd
%hard %{_prefix}/sbin/sasldblistusers2
%hard %{_prefix}/sbin/saslpasswd2
%hard %{_prefix}/sbin/testsaslauthd

%dir %attr (0755, root, bin) %{_prefix}/sbin/%{base_arch}
%{_prefix}/sbin/%{base_arch}/pluginviewer
%{_prefix}/sbin/%{base_arch}/saslauthd
%{_prefix}/sbin/%{base_arch}/sasldblistusers2
%{_prefix}/sbin/%{base_arch}/saslpasswd2
%{_prefix}/sbin/%{base_arch}/testsaslauthd

%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, other) %{_libdir}/sasl2
%{_libdir}/sasl2/lib*.so*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_prefix}/sbin/%{_arch64}
%{_prefix}/sbin/%{_arch64}/pluginviewer
%{_prefix}/sbin/%{_arch64}/saslauthd
%{_prefix}/sbin/%{_arch64}/sasldblistusers2
%{_prefix}/sbin/%{_arch64}/saslpasswd2
%{_prefix}/sbin/%{_arch64}/testsaslauthd
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/sasl2
%{_libdir}/%{_arch64}/sasl2/lib*.so*
%endif

%dir %attr (0755, root, sys) /var
%dir %attr (0755, root, sys) /var/svc
%dir %attr (0755, root, sys) /var/svc/manifest
%dir %attr (0755, root, sys) /var/svc/manifest/application
%class(manifest) %attr (0755, root, sys) /var/svc/manifest/application/saslauthd.xml

%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, other) %{_includedir}/sasl
%{_includedir}/sasl/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*
%dir %attr (0755, root, bin) %{_mandir}/man8
%{_mandir}/man8/*

%changelog
* Fri May 22 2009 - moinakg@belenix.org
- Bump version, add 64Bit build.
- Major packaging/functionality upddates.
* Sun Feb 24 2008 - moinakg@gmail.com
- Updated sqlite dependency.
* Sun Feb 03 2008 - moinak.ghosh@sun.com
- Add dependency on SFElibntlm.
* Tue Jan 15 2008 - moinak.ghosh@sun.com
- Initial spec.
