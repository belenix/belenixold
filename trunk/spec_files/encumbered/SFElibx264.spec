
# spec file for package SFEx264
#
# includes module(s): x264
#

%include Solaris.inc

%ifarch amd64
%include arch64.inc
%endif

%include base.inc

%define         snap    20090424
%define         snaph   2245
%define src_name x264-snapshot
%define src_url	 ftp://ftp.videolan.org/pub/videolan/x264/snapshots

Name:                    SFElibx264
Summary:                 H264 encoder library
Version:                 20090424
Source:                  %{src_url}/%{src_name}-%{snap}-%{snaph}.tar.bz2
URL:                     http://www.videolan.org/developers/x264.html
#Patch1:			 libx264-01-gccisms.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEyasm
BuildRequires: SFEgpac-devel
Requires: SFEgpac

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -c -n %name-%version
cd %{src_name}-%{snap}-%{snaph}
#%patch1 -p1
cd ..

%ifarch amd64
cp -rp %{src_name}-%{snap}-%{snaph} %{src_name}-%{snap}-%{snaph}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

%if %build_l10n
nlsopt=-enable-nls
%else
nlsopt=-disable-nls
%endif

%ifarch amd64
cd %{src_name}-%{snap}-%{snaph}-64

export CC=gcc
export CFLAGS="%optflags64 -D__C99FEATURES__"
export LDFLAGS="%_ldflags64 -lm"
export PATH="/usr/gnu/bin/%{_arch64}:/usr/bin/%{_arch64}:/usr/sfw/bin/%{_arch64}:${PATH}"
bash ./configure	\
    --prefix=%{_prefix} \
    --bindir=%{_bindir}/%{_arch64} \
    --libdir=%{_libdir}/%{_arch64} \
    --enable-mp4-output	\
    --enable-gtk	\
    --enable-pthread	\
    --enable-pic	\
    --enable-shared	\
    --enable-visualize  \
    --host=x86_64-pc-solaris2.11 \
    $nlsopt

#
# Kludge till we figure proper PIC generation yasm
#
cat Makefile | sed 's/-shared/-G/g' > Makefile.new
chmod +w Makefile
cp Makefile.new Makefile
make
cd ..
%endif

cd %{src_name}-%{snap}-%{snaph}

export CC=gcc
export CFLAGS="%optflags -D__C99FEATURES__"
export LDFLAGS="%_ldflags -lm"
export PATH="/usr/gnu/bin:${PATH}"
bash ./configure        \
    --prefix=%{_prefix} \
    --enable-mp4-output \
    --enable-gtk        \
    --enable-pthread    \
    --enable-pic        \
    --enable-shared     \
    --enable-visualize  \
    $nlsopt

#
# Kludge till we figure proper PIC generation yasm
#
cat Makefile | sed 's/-shared/-G/g' > Makefile.new
chmod +w Makefile
cp Makefile.new Makefile
make
cd ..


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64
cd %{src_name}-%{snap}-%{snaph}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/lib*.*a
cd ..
%endif

cd %{src_name}-%{snap}-%{snaph}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a
cd ..

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/x264
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
#%dir %attr (0755, root, sys) %{_datadir}
#%{_datadir}/x264

%ifarch amd64
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/x264
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif


%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%ifarch amd64
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

#%if %build_l10n
#%files l10n
#%defattr (-, root, bin)
#%dir %attr (0755, root, sys) %{_datadir}
#%attr (-, root, other) %{_datadir}/locale
#%endif

%changelog
* Tue Apr 28 2009 - moinakg@belenix.org
- Bump version to 20090424 and add 64Bit build.
- Move to encumbered specs.
* Thu Feb 21 2008 - moinak.ghosh@sun.com
- Add /usr/gnu/bin to PATH to enable use of xgettext from GNU gettext in Indiana env.
* tue Jan 08 2008 - moinak.ghosh@sun.com
- Build with gcc and enable C99FEATURES.
* Tue Nov 20 2007 - daymobrew@users.sourceforge.net
- Bump to 20071119 and add Url.
* Sun Aug 12 2007 - dougs@truemail.co.th
- Added SFEgpac as Required
* Fri Aug  3 2007 - dougs@truemail.co.th
- initial version
