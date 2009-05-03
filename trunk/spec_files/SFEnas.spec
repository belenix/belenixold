#
# spec file for package SFEnas
#
# includes module(s): nas
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

%define	src_ver 1.9.2
%define	src_name nas
%define	src_url	http://downloads.sourceforge.net/nas

Name:		SFEnas
Summary:	Network Audio System
Version:	%{src_ver}
License:	Free
Source:		%{src_url}/%{src_name}-%{version}.src.tar.gz
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc

%package doc
Summary:                 %{summary} - documentation files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
Requires:       FSWxorg-clientlibs
Requires:       SUNWxwplt
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
%setup -q -c -n %name-%version
%ifarch amd64 sparcv9
cp -rp %{src_name}-%{version} %{src_name}-%{version}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

%ifarch amd64 sparcv9
cd %{src_name}-%{version}-64

export CPPFLAGS="-I/usr/X11/include"
export CFLAGS="%optflags64"
export LDFLAGS="%_ldflags64 -L/usr/X11/lib/%{_arch64} -lX11 -lXt"
export PATH="${PATH}:/usr/X11/bin"

xmkmf

make Makefiles
for mf in `find . -name Makefile `
do
	cp ${mf} ${mf}.orig
	cat ${mf}.orig | sed '{
	    s/CC = cc/CC = cc -m64/
	    s/CXX = CC/CXX = CC -m64/
	    s/MODCC = cc/MODCC = cc -m64/
	}' > ${mf}
done

make clean
make includes
make depend
make -k all

cd ..
%endif

cd %{src_name}-%{version}

export CPPFLAGS="-I/usr/X11/include"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -L/usr/X11/lib -lX11 -lXt"
export PATH="${PATH}:/usr/X11/bin"

xmkmf

make World
cd ..


%install
rm -rf $RPM_BUILD_ROOT
export PATH="${PATH}:/usr/X11/bin"

%ifarch amd64 sparcv9
cd %{src_name}-%{version}-64
make install install.man DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT/usr/X11/lib/lib*.*a
mkdir -p $RPM_BUILD_ROOT%{_libdir}/%{_arch64}
mkdir -p $RPM_BUILD_ROOT%{_bindir}/%{_arch64}
mv $RPM_BUILD_ROOT/usr/X11/lib/lib*.so* $RPM_BUILD_ROOT%{_libdir}/%{_arch64}
mv $RPM_BUILD_ROOT/usr/X11/bin/* $RPM_BUILD_ROOT%{_bindir}/%{_arch64}
chmod a+x $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/lib*.so*
rmdir $RPM_BUILD_ROOT/usr/X11/bin

cd ..
%endif

cd %{src_name}-%{version}
make install install.man DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT/usr/X11/lib/lib*.*a
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_datadir}
mkdir -p $RPM_BUILD_ROOT/usr/X11/share/X11
mv $RPM_BUILD_ROOT/usr/X11/lib/lib*.so* $RPM_BUILD_ROOT%{_libdir}
mv $RPM_BUILD_ROOT/usr/X11/bin/* $RPM_BUILD_ROOT%{_bindir}
mv $RPM_BUILD_ROOT/usr/X11/include $RPM_BUILD_ROOT%{_includedir}
mv $RPM_BUILD_ROOT/usr/X11/man $RPM_BUILD_ROOT%{_datadir}
mv $RPM_BUILD_ROOT/usr/X11/lib/X11/AuErrorDB $RPM_BUILD_ROOT/usr/X11/share/X11
(cd $RPM_BUILD_ROOT/usr/X11/lib/X11
    ln -s ../../share/X11/AuErrorDB)
chmod a+x $RPM_BUILD_ROOT%{_libdir}/lib*.so*
rmdir $RPM_BUILD_ROOT/usr/X11/bin

cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/auphone
%{_bindir}/playbucket
%{_bindir}/nasd
%{_bindir}/autool
%{_bindir}/auscope
%{_bindir}/aupanel
%{_bindir}/issndfile
%{_bindir}/aurecord
%{_bindir}/auplay
%{_bindir}/auconvert
%{_bindir}/auinfo
%{_bindir}/auwave
%{_bindir}/checkmail
%{_bindir}/auedit
%{_bindir}/audial
%{_bindir}/audemo
%{_bindir}/auctl
%{_bindir}/soundtoh

%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/auphone
%{_bindir}/%{_arch64}/playbucket
%{_bindir}/%{_arch64}/nasd
%{_bindir}/%{_arch64}/autool
%{_bindir}/%{_arch64}/auscope
%{_bindir}/%{_arch64}/aupanel
%{_bindir}/%{_arch64}/issndfile
%{_bindir}/%{_arch64}/aurecord
%{_bindir}/%{_arch64}/auplay
%{_bindir}/%{_arch64}/auconvert
%{_bindir}/%{_arch64}/auinfo
%{_bindir}/%{_arch64}/auwave
%{_bindir}/%{_arch64}/checkmail
%{_bindir}/%{_arch64}/auedit
%{_bindir}/%{_arch64}/audial
%{_bindir}/%{_arch64}/audemo
%{_bindir}/%{_arch64}/auctl
%{_bindir}/%{_arch64}/soundtoh

%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/*.so*
%endif

%dir %attr (0755, root, bin) /usr/X11
%dir %attr (0755, root, bin) /usr/X11/share
%dir %attr (0755, root, bin) /usr/X11/share/X11
/usr/X11/share/X11/*
%dir %attr (0755, root, bin) /usr/X11/lib
%dir %attr (0755, root, bin) /usr/X11/lib/X11
/usr/X11/lib/X11/*

%files doc
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}

%files devel
%defattr (-, root, bin)
%{_includedir}

%files root
%defattr (-, root, sys)
%{_sysconfdir}

%changelog
* Sun May 03 2009 - moinakg@belenix.org
- Add 64Bit build and documentation package.
- Bump version to 1.9.2
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
