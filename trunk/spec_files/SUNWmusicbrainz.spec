#
# spec file for package SUNWmusicbrainz
#
# includes module(s): libmusicbrainz3
#
%include Solaris.inc

%define	src_ver 2.1.5
%define	src_name libmusicbrainz
%define	src_url	ftp://ftp.musicbrainz.org/pub/musicbrainz

Name:		SUNWmusicbrainz
Summary:	library for accesing MusicBrainz servers (version 2.x)
Version:	%{src_ver}
License:	LGPL
Source:		%{src_url}/%{src_name}-%{version}.tar.gz
Patch1:		libmusicbrainz2-01-string.h.diff

SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
BuildRequires: SFEcmake
%if %(pkginfo -q SUNWneon && echo 1 || echo 0)
Requires: SUNWneon
%else
Requires: SFEneon
%endif
BuildRequires: SFElibdiscid-devel
Requires: SFElibdiscid
BuildRequires: SFEcppunit-devel
Requires: SFEcppunit
Requires: SUNWlexpt

%description
The MusicBrainz client library allows applications to make metadata
lookup to a MusicBrainz server, generate signatures from WAV data and
create CD Index Disk ids from audio CD roms.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %{src_name}-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export LDFLAGS="%_ldflags %{gnu_lib_path} -lstdc++"

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --libdir=%{_libdir} \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir} \
            --includedir=%{_includedir}

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT CMAKE_INSTALL_PREFIX=/usr
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Sat Sep 12 2009 - moinakg(at)belenix<dot>org
- Initial spec
