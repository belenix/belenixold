#
# spec file for package SFEcups
#
# includes module(s): cups
#
%include Solaris.inc

%define	src_ver 1.3.9
%define	src_name cups
%define	src_url	http://ftp.easysw.com/pub/%{src_name}/%{src_ver}

%define cups_user lp
%define cups_group lp
%define cupsdir	/usr/cups
%define cupsbin	%{cupsdir}/bin
%define cupssbin %{cupsdir}/sbin
%define cupsdata %{cupsdir}/share
%define cupsman %{cupsdir}/man

Name:		SFEcups
Summary:	Common Unix Printing System
Version:	%{src_ver}
License:	GPL/LGPL
Source:		%{src_url}/%{src_name}-%{version}-source.tar.bz2

Source1:        ManageCUPS.html
Source2:        desktop-print-management
Source3:        desktop-print-management-applet

Patch0:         cups-00-man.patch
Patch1:         cups-01-cups-config.patch
Patch2:         cups-02-smf.patch
Patch3:         cups-03-cups.pc.patch
Patch4:         cups-06-cupsd.conf.in.patch
Patch5:         cups-07-scf-active.patch
Patch6:         cups-08-usb-hack.patch

SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
Requires:       %{name}-root

%description
CUPS provides a portable printing layer for UNIX-based operating
systems. It has been developed by Easy Software Products to promote a
standard printing solution for all UNIX vendors and users. CUPS
provides the System V and Berkeley command-line interfaces. CUPS uses
the Internet Printing Protocol ("IPP") as the basis for managing print
jobs and queues. The Line Printer Daemon ("LPD") Server Message Block
("SMB"), and AppSocket (a.k.a. JetDirect) protocols are also supported
with reduced functionality. CUPS adds network printer browsing and
PostScript Printer Description ("PPD") based printing options to
support real-world printing under UNIX.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package doc
Summary:                 %{summary} - Documentation
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %{src_name}-%version
gpatch -p0 --fuzz=0 < %{PATCH0}
gpatch -p0 --fuzz=0 < %{PATCH1}
gpatch -p0 --fuzz=0 < %{PATCH2}
gpatch -p0 --fuzz=0 < %{PATCH3}
gpatch -p0 --fuzz=0 < %{PATCH4}
gpatch -p0 --fuzz=0 < %{PATCH5}
gpatch -p0 --fuzz=0 < %{PATCH6}
#%patch0 -p0
#%patch1 -p0
#%patch2 -p0
#%patch3 -p0
#%patch4 -p0
#%patch5 -p0
#%patch6 -p0

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CPPFLAGS="-I/usr/X11/include"
export CFLAGS="-O3 -fno-omit-frame-pointer -fPIC -DPIC"
export LDFLAGS="%_ldflags -lX11"

glib-gettextize --force
libtoolize --force --copy
aclocal 
autoconf -f
./configure --prefix=%{_prefix}				\
	    --bindir=%{cupsbin}				\
	    --sbindir=%{cupssbin}			\
	    --libdir=%{_libdir}				\
	    --mandir=%{_mandir}				\
	    --datadir=%{_datadir}			\
	    --sysconfdir=%{_sysconfdir}			\
	    --localstatedir=%{_localstatedir}		\
	    --enable-openssl				\
	    --with-cups-user=%{cups_user}		\
	    --with-cups-group=%{cups_group}		\
	    --localedir=%{_datadir}/locale		\
	    --with-openssl-libs=/usr/sfw/lib		\
	    --with-openssl-includes=/usr/sfw/include	\
            --with-fontpath=/usr/X11/lib		\
            --with-logdir=%{_localstatedir}/log/cups	\
            --with-domain-socket=%{_localstatedir}/run/cups-socket	\
            --with-smfmanifestdir=%{_localstatedir}/svc/manifest/application	\
            --with-printcap=%{_sysconfdir}/printers.conf		\
	    --disable-static				\
	    --enable-shared				\
            --disable-gnutls				\
            --enable-dbus				\
            --enable-threads				\
            --enable-64bit

make MAN1EXT="1cups" MAN8EXT="1cups" MAN8DIR="1cups"

%install

rm -rf $RPM_BUILD_ROOT
make install BUILDROOT=$RPM_BUILD_ROOT MAN1EXT="1cups" MAN8EXT="1cups" MAN8DIR="1cups"
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/rc*.d
mkdir -p $RPM_BUILD_ROOT%{cupsdata}
mv $RPM_BUILD_ROOT%{_mandir} $RPM_BUILD_ROOT%{cupsdata}
mkdir -p $RPM_BUILD_ROOT%{_bindir}
( 
  cd $RPM_BUILD_ROOT%{_bindir}
  ln -s ../cups/bin/cups-config 
  for i in cancel lp lpr lpq lprm lpstat ; do
    ln -s ../cups/bin/${i} ${i}-cups
  done
  cd $RPM_BUILD_ROOT%{_sindir}
  for i in accept lpc lpmove lpadmin lpinfo reject ; do
    ln -s ../cups/sbin/${i} ${i}-cups
  done
  ln -s ../cups/sbin/cupsenable enable-cups
  ln -s ../cups/sbin/cupsdisable disable-cups
)

mkdir -p $RPM_BUILD_ROOT%{_libdir}/%{_arch64}
mv $RPM_BUILD_ROOT%{_libdir}/64/* $RPM_BUILD_ROOT%{_libdir}/%{_arch64}
rmdir $RPM_BUILD_ROOT%{_libdir}/64

# fix to not conflict with JDS
mkdir -p $RPM_BUILD_ROOT%{_datadir}/locale/zh_CN
rm -r $RPM_BUILD_ROOT%{_datadir}/locale/zh
ln -sf zh_CN $RPM_BUILD_ROOT%{_datadir}/locale/zh

mv $RPM_BUILD_ROOT%{_sysconfdir}/cups/cupsd.conf.default $RPM_BUILD_ROOT%{_sysconfdir}/cups/cupsd.conf
touch $RPM_BUILD_ROOT%{_sysconfdir}/cups/command.types

# add a link for foomatic ppds
ln -sf ../../ppd $RPM_BUILD_ROOT%{_datadir}/cups/model/ppds

# install the smf help
mkdir -p $RPM_BUILD_ROOT%{_libdir}/help/auths/locale
cp %{SOURCE1} $RPM_BUILD_ROOT%{_libdir}/help/auths/locale
chmod 0444 $RPM_BUILD_ROOT%{_libdir}/help/auths/locale/*

mkdir $RPM_BUILD_ROOT%{_libdir}/help/auths/locale/C
cp %{SOURCE1} $RPM_BUILD_ROOT%{_libdir}/help/auths/locale/C
chmod 0444 $RPM_BUILD_ROOT%{_libdir}/help/auths/locale/C/*

# install the desktop menu related bits
install -m 0555 %{SOURCE2} $RPM_BUILD_ROOT%{cupsbin}
install -m 0555 %{SOURCE3} $RPM_BUILD_ROOT%{cupsbin}

#rm $RPM_BUILD_ROOT/usr/share/applications/cups.desktop
#rmdir $RPM_BUILD_ROOT%{_localstatedir}/run/cups/certs $RPM_BUILD_ROOT%{_localstatedir}/run/cups


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{cupsdir}
%{cupsbin}
%{cupssbin}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/cups
%{_libdir}/lib*.so*
%{_libdir}/%{_arch64}/lib*.so*
%dir %attr (0755, root, bin) %{_libdir}/help
%dir %attr (0755, root, bin) %{_libdir}/help/auths
%dir %attr (0755, root, bin) %{_libdir}/help/auths/locale
%dir %attr (0755, root, bin) %{_libdir}/help/auths/locale/C
%{_libdir}/help/auths/locale/ManageCUPS.html
%{_libdir}/help/auths/locale/C/ManageCUPS.html

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, sys) %{cupsdata}
%{cupsdata}/man
%{_datadir}/cups
%{_datadir}/locale
%defattr (-, root, other)
%{_datadir}/applications
%{_datadir}/icons

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%files root
%defattr (-, root, sys)
%{_sysconfdir}
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, sys) %{_localstatedir}/svc
%dir %attr (0755, root, sys) %{_localstatedir}/svc/manifest
%dir %attr (0755, root, sys) %{_localstatedir}/svc/manifest/application
%attr (0755, root, sys) %{_localstatedir}/svc/manifest/application/cups.xml
%dir %attr (0755, root, bin) %{_localstatedir}/spool
%dir %attr (0644, %{cups_user}, %{cups_group}) %{_localstatedir}/spool/cups
%dir %attr (0644, %{cups_user}, %{cups_group}) %{_localstatedir}/spool/cups/tmp
%dir %attr (0755, root, sys) %{_localstatedir}/run
%dir %attr (0644, %{cups_user}, %{cups_group}) %{_localstatedir}/run/cups
%dir %attr (0644, %{cups_user}, %{cups_group}) %{_localstatedir}/run/cups/certs
%dir %attr (0755, root, sys) %{_localstatedir}/log
%dir %attr (0644, %{cups_user}, %{cups_group}) %{_localstatedir}/log/cups
%dir %attr (0644, %{cups_user}, %{cups_group}) %{_localstatedir}/cache
%dir %attr (0644, %{cups_user}, %{cups_group}) %{_localstatedir}/cache/cups/rss

%files doc
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%changelog
* Wed Apr 15 2009 - moinakg@belenix.org
- Merge Patches and build changes from SFW gate.
* Tue Mar 18 2008 - moinakg@gmail.com
- Add missing dependency on root package.
* Wed Aug 15 2007 - dougs@truemail.co.th
- bump to 1.3.0, added --disable-gssapi
* Fri Aug  3 2007 - dougs@truemail.co.th
- Initial spec
