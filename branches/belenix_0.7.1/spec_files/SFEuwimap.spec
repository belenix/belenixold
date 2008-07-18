#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEuwimap
Summary:             University of Washington IMAP toolkit
Version:             2007b
Source:              ftp://ftp.cac.washington.edu/mail/imap.tar.Z
Patch:		     imap-01.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

%prep
rm -rf %{name}-%{version}
mkdir %{name}-%{version}
cd %{name}-%{version}
uncompress -c %{SOURCE} | tar xf -
cd imap-%{version}
%patch -p0

%build
cd %{name}-%{version}/imap-%{version}

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

make clean
make soc EXTRACFLAGS='-fast -xipo -xtarget=generic %optflags'

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_basedir}/imap/bin
mkdir -p $RPM_BUILD_ROOT/%{_basedir}/imap/lib
mkdir -p $RPM_BUILD_ROOT/%{_basedir}/imap/include

cd %{name}-%{version}/imap-%{version}
cp c-client/*.h $RPM_BUILD_ROOT/%{_basedir}/imap/include
cp c-client/c-client.a $RPM_BUILD_ROOT/%{_basedir}/imap/lib
cp imapd/imapd $RPM_BUILD_ROOT/%{_basedir}/imap/bin
cp ipopd/ipop2d $RPM_BUILD_ROOT/%{_basedir}/imap/bin
cp ipopd/ipop3d $RPM_BUILD_ROOT/%{_basedir}/imap/bin
cp dmail/dmail $RPM_BUILD_ROOT/%{_basedir}/imap/bin
cp mailutil/mailutil $RPM_BUILD_ROOT/%{_basedir}/imap/bin
cp mlock/mlock $RPM_BUILD_ROOT/%{_basedir}/imap/bin
cp mtest/mtest $RPM_BUILD_ROOT/%{_basedir}/imap/bin
cp tmail/tmail $RPM_BUILD_ROOT/%{_basedir}/imap/bin

chmod a+x $RPM_BUILD_ROOT/%{_basedir}/imap/bin/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_basedir}/imap
%dir %attr (0755, root, bin) %{_basedir}/imap/bin
%{_basedir}/imap/bin/*
%dir %attr (0755, root, bin) %{_basedir}/imap/lib
%{_basedir}/imap/lib/*
%dir %attr (0755, root, bin) %{_basedir}/imap/include
%{_basedir}/imap/include/*

%changelog
* Thu Jul 03 2008 - moinakg@gmail.com
- Initial spec
