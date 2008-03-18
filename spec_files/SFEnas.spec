#
# spec file for package SFEnas
#
# includes module(s): nas
#
%include Solaris.inc

%define	src_ver 1.9.1
%define	src_name nas
%define	src_url	http://downloads.sourceforge.net/nas

Name:		SFEnas
Summary:	Network Audio System
Version:	%{src_ver}
License:	Free
Source:		%{src_url}/%{src_name}-%{version}.src.tar.gz
Patch1:         nas-01-libaudio.diff

SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
Requires:       FSWxorg-clientlibs
Requires:       FSWxwpft
BuildRequires:  FSWxorg-client-programs
Requires:       %{name}-root

%description
This package contains a network-transparent, client/server audio
system, with a library. Key features of the Network Audio System
include:
 - Device-independent audio over the network
 - Lots of audio file and data formats
 - Can store sounds in server for rapid replay
 - Extensive mixing, separating, and manipulation of audio data
 - Simultaneous use of audio devices by multiple applications
 - Use by a growing number of ISVs
 - Small size
 - Free! No obnoxious licensing terms.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CPPFLAGS="-I/usr/X11/include"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -L/usr/X11/lib -lX11 -lXt"
export PATH="${PATH}:/usr/X11/bin"

xmkmf

make World

%install

export PATH="${PATH}:/usr/X11/bin"
rm -rf $RPM_BUILD_ROOT
make install install.man 	\
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT/usr/X11/lib/lib*.*a
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_datadir}
mkdir -p $RPM_BUILD_ROOT/usr/X11/share/X11
mv $RPM_BUILD_ROOT/usr/X11/lib/lib*.so* $RPM_BUILD_ROOT%{_libdir}
mv $RPM_BUILD_ROOT/usr/X11/bin $RPM_BUILD_ROOT%{_bindir}
mv $RPM_BUILD_ROOT/usr/X11/include $RPM_BUILD_ROOT%{_includedir}
mv $RPM_BUILD_ROOT/usr/X11/man $RPM_BUILD_ROOT%{_datadir}
mv $RPM_BUILD_ROOT/usr/X11/lib/X11/AuErrorDB $RPM_BUILD_ROOT/usr/X11/share/X11
(cd $RPM_BUILD_ROOT/usr/X11/lib/X11
    ln -s ../../share/X11/AuErrorDB)
chmod a+x $RPM_BUILD_ROOT%{_libdir}/lib*.so*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}
%dir %attr (0755, root, bin) /usr/X11
%dir %attr (0755, root, bin) /usr/X11/share
%dir %attr (0755, root, bin) /usr/X11/share/X11
/usr/X11/share/X11/*
%dir %attr (0755, root, bin) /usr/X11/lib
%dir %attr (0755, root, bin) /usr/X11/lib/X11
/usr/X11/lib/X11/*

%files devel
%defattr (-, root, bin)
%{_includedir}

%files root
%defattr (-, root, sys)
%{_sysconfdir}

%changelog
* Tue Mar 18 2008 - moinakg@gmail.com
- Add missing dependency on root package.
* Sun Feb 24 2008 - moinakg@gmail.com
- Rework to build with FOX.
* Thu Feb 14 2008 - moinak.ghosh@sun.com
- Add patch to Imakefile to add proper linker flags for libaudio.
* Fri Jan 11 2008 - moinak.ghosh@sun.com
- Update source URL, bumped version to 1.9.1
- Add openwinbin to PATH, use rm -f to quiesce rm
* Fri Aug  3 2007 - dougs@truemail.co.th
- Initial spec
