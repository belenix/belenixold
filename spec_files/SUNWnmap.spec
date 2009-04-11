#
# spec file for package SFEnmap
#
# includes module(s): nmap
#
%include Solaris.inc

Name:         SUNWnmap
Summary:      Network Mapper
License:      GPL
Version:      4.76
Group:        System/GUI/GNOME
Source:       http://download.insecure.org/nmap/dist/nmap-%{version}.tar.bz2
Patch1:       nmap-02-Makefile.diff

Source1:      nmapfe.desktop
Source2:      nmapfe.png

SUNW_BaseDir: %{_basedir}
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
URL:          http://insecure.org/nmap/index.html

%include default-depend.inc

%description
Nmap ("Network Mapper") is a free open source utility for network exploration or security auditing.

%prep
%setup -q -n nmap-%version
%patch1 -p1


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

%if %cc_is_gcc
export NMAP_CXX="$CXX"
%else
export NMAP_CXX="${CXX} -norunpath"
%endif

export CXXFLAGS="%cxx_optflags -I/usr/include/pcre -DHAVE_GETOPT_H"
export CFLAGS=${CXXFLAGS}

./configure --prefix=%{_prefix} \
            --mandir=%{_mandir} \
	    --localstatedir=%{_localstatedir} \
	    --with-zenmap \
	    --with-openssl=%{_prefix}/sfw \
	    --with-libpcap=%{_prefix} \
	    --with-libpcre=%{_prefix}

cat Makefile | sed 's/CPPFLAGS = /CPPFLAGS = $(DEFS) /' > Makefile.new
cp Makefile.new Makefile
touch makefile.dep 
make all CXX="$NMAP_CXX $CFLAGS"

%install
make DESTDIR=$RPM_BUILD_ROOT install
mkdir ${RPM_BUILD_ROOT}/usr/lib/python2.4/vendor-packages
mv ${RPM_BUILD_ROOT}/usr/lib/python2.4/site-packages/* ${RPM_BUILD_ROOT}/usr/lib/python2.4/vendor-packages
rmdir ${RPM_BUILD_ROOT}/usr/lib/python2.4/site-packages

mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/pixmaps
cp %{SOURCE1} ${RPM_BUILD_ROOT}%{_datadir}/applications
cp %{SOURCE2} ${RPM_BUILD_ROOT}%{_datadir}/pixmaps

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/nmap
%{_datadir}/nmap/*
%dir %attr (0755, root, bin) %{_datadir}/zenmap
%{_datadir}/zenmap/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/python2.4
%dir %attr (0755, root, bin) %{_libdir}/python2.4/vendor-packages
%{_libdir}/python2.4/vendor-packages/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*

%changelog
* SAt Apr 11 2009 - moinakg@gmail.com
- Name changed and imported from SFE gate.
- Build and packaging fixes.
* Thu Jan 11 2007 - dermot.mccluskey@sun.com
- Initial version
