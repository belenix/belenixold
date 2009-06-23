#
# spec file for package SUNWghostscriptu
#
# includes module(s): ghostscriptu
#
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

Name:                    SUNWghostscriptu
Summary:                 A PostScript interpreter and renderer (usr).
Version:                 8.64
%define gs_dot_ver       8.64
URL:                     http://www.ghostscript.com/
Source:                  http://ghostscript.com/releases/ghostscript-%{version}.tar.bz2

#
# Non-unified patches from SFE gate UGH!
#
Source1:                 ghostscript-01-4776996.diff
Source2:                 ghostscript-02-4795491.diff
Source3:                 ghostscript-03-5045800.diff
Source4:                 ghostscript-04-unixinst.mak.diff
Source5:                 ghostscript-05-devs.mak.diff
Source6:                 ghostscript-06-ijs.automake.diff
Source7:                 ghostscript-07-fixmswrd.pl.diff
Source8:                 ghostscript-08-CVE-2009-0583,0584.diff
Source9:                 ghostscript-09-CVE-2009-0792.diff
Source10:                ghostscript-10-CVE-2009-0196.diff
Source11:                ghostscript-11-CVE-2008-6679.diff

#
# Good patches from FC11
#
Patch12:                 ghostscript-12-fPIC.diff
Patch13:                 ghostscript-13-gs-executable.diff
Patch14:                 ghostscript-14-system-jasper.diff
Patch15:                 ghostscript-15-multilib.diff

License:                 GPLv2
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SUNWgsfst
Requires:      SFEcups
Requires:      SUNWghostscriptr
Requires:      SUNWperl584core
Requires:      SUNWgtk2
Requires:      SUNWglib2
Requires:      SUNWTiff
Requires:      SFEjasper
Requires:      SUNWlxml
Requires:      SUNWzlib
Requires:      SUNWpng
Requires:      SUNWjpg
BuildRequires: SFEcups-devel
BuildRequires: SUNWgtk2-devel
BuildRequires: SUNWglib2-devel
BuildRequires: SUNWTiff-devel
BuildRequires: SFEjasper-devel
BuildRequires: SUNWpng-devel
BuildRequires: SUNWjpg-devel

%description
Ghostscript is a set of software that provides a PostScript
interpreter, a set of C procedures (the Ghostscript library, which
implements the graphics capabilities in the PostScript language) and
an interpreter for Portable Document Format (PDF) files. Ghostscript
translates PostScript code into many common, bitmapped formats, like
those understood by your printer or screen. Ghostscript is normally
used to display PostScript files and to print PostScript files to
non-PostScript printers.

If you need to display PostScript files or print them to
non-PostScript printers, you should install ghostscript. If you
install ghostscript, you also need to install the ghostscript-fonts
package.


%package -n SUNWghostscriptr
Summary:                 A PostScript interpreter and renderer (root).
SUNW_BaseDir:            /
%include default-depend.inc

%package -n SUNWghostscriptd
Summary:                 A PostScript interpreter and renderer - Development files.
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:      %{name}

%prep
%setup -q -c -n %name-%version
cd ghostscript-%{version}
cat %{SOURCE1} | gpatch -p0
cat %{SOURCE2} | gpatch -p0
cat %{SOURCE3} | gpatch -p0
cat %{SOURCE4} | gpatch -p0
cat %{SOURCE5} | gpatch -p0
cat %{SOURCE6} | gpatch -p0
cat %{SOURCE7} | gpatch -p0
cat %{SOURCE8} | gpatch -p0
cat %{SOURCE9} | gpatch -p0
cat %{SOURCE10} | gpatch -p0
cat %{SOURCE12} | gpatch -p0
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
rm -rf libpng zlib jpeg jasper
cd ..

%ifarch amd64 sparcv9
cp -rp ghostscript-%{version} ghostscript-%{version}-64
%endif

%build
FONTPATH="/usr/share/ghostscript/%{version}/Resource:/usr/share/ghostscript/%{version}/Resource/Font:/usr/share/ghostscript/fonts:/usr/openwin/lib/X11/fonts/Type1:/usr/openwin/lib/X11/fonts/TrueType:/usr/openwin/lib/X11/fonts/Type3:/usr/X11/lib/X11/fonts/Type1:/usr/X11/lib/fonts/TrueType:/usr/X11/lib/X11/fonts/Type3:/usr/X11/lib/X11/fonts/Resource:/usr/X11/lib/X11/Resource/Font"

%ifarch amd64 sparcv9
cd ghostscript-%{version}-64
export CC="/usr/gnu/bin/gcc -m64"
export CFLAGS="-march=opteron -m64 -Xlinker -i -fno-omit-frame-pointer -fPIC -DPIC-fno-strict-aliasing"
export LDFLAGS="%_ldflags64"

./autogen.sh
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --bindir=%{_bindir}/%{_arch64}              \
            --libdir=%{_libdir}/%{_arch64}              \
            --with-drivers=ALL                          \
            --with-ijs                                  \
            --with-jbig2dec                             \
            --disable-cups                              \
            --disable-compile-inits                     \
            --with-fontpath="$FONTPATH"                 \
            --enable-dynamic

# Build IJS
cd ijs
./autogen.sh
./configure --prefix=%{_prefix} \
            --bindir=%{_bindir}/%{_arch64} \
            --libdir=%{_libdir}/%{_arch64} \
            --enable-shared --enable-static
make
cd ..

make so RPM_OPT_FLAGS="${CFLAGS}" prefix=%{_prefix}
make RPM_OPT_FLAGS="${CFLAGS}" prefix=%{_prefix}

cd ..
%endif

cd ghostscript-%{version}
unset CC
export CFLAGS="-march=pentium4 -Xlinker -i -fno-omit-frame-pointer -fPIC -DPIC -fno-strict-aliasing"
export LDFLAGS="%_ldflags"
export CUPSCONFIG=%{_bindir}/cups-config

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --bindir=%{_bindir}                  \
            --libdir=%{_libdir}                  \
            --with-drivers=ALL                          \
            --with-ijs                                  \
            --with-jbig2dec                             \
            --enable-cups                               \
            --disable-compile-inits                     \
            --with-fontpath="$FONTPATH"                 \
            --enable-dynamic

# Build IJS
cd ijs
./autogen.sh
./configure --prefix=%{_prefix} --enable-shared --enable-static
make
cd ..

make so RPM_OPT_FLAGS="${CFLAGS}" prefix=%{_prefix}
make RPM_OPT_FLAGS="${CFLAGS}" prefix=%{_prefix}
make cups
cd ..


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{%{_mandir},%{_bindir},%{_datadir},%{_docdir}}
mkdir -p $RPM_BUILD_ROOT/{%{_libdir},%{_includedir}/ijs}

%ifarch amd64 sparcv9
cd ghostscript-%{version}-64
make install soinstall \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	datadir=$RPM_BUILD_ROOT%{_datadir} \
	gsincludedir=$RPM_BUILD_ROOT%{_includedir}/ghostscript/ \
	bindir=$RPM_BUILD_ROOT%{_bindir}/%{_arch64} \
	libdir=$RPM_BUILD_ROOT%{_libdir}/%{_arch64} \
	docdir=$RPM_BUILD_ROOT%{_docdir}/ghostscript-%{gs_dot_ver} \
	gsdir=$RPM_BUILD_ROOT%{_datadir}/ghostscript \
	gsdatadir=$RPM_BUILD_ROOT%{_datadir}/ghostscript/%{gs_dot_ver} \
	gssharedir=$RPM_BUILD_ROOT%{_libdir}/%{_arch64}/ghostscript/%{gs_dot_ver}

mv -f $RPM_BUILD_ROOT%{_bindir}/%{_arch64}/gsc $RPM_BUILD_ROOT%{_bindir}/%{_arch64}/gs

cd ijs
make install DESTDIR=${RPM_BUILD_ROOT}
cd ..

cd ..
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.a
%endif

cd ghostscript-%{version}
make install soinstall \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	datadir=$RPM_BUILD_ROOT%{_datadir} \
	gsincludedir=$RPM_BUILD_ROOT%{_includedir}/ghostscript/ \
	bindir=$RPM_BUILD_ROOT%{_bindir} \
	libdir=$RPM_BUILD_ROOT%{_libdir} \
	docdir=$RPM_BUILD_ROOT%{_docdir}/ghostscript-%{gs_dot_ver} \
	gsdir=$RPM_BUILD_ROOT%{_datadir}/ghostscript \
	gsdatadir=$RPM_BUILD_ROOT%{_datadir}/ghostscript/%{gs_dot_ver} \
	gssharedir=$RPM_BUILD_ROOT%{_libdir}/ghostscript/%{gs_dot_ver} \
	CUPSSERVERROOT=$RPM_BUILD_ROOT`cups-config --serverroot` \
	CUPSSERVERBIN=$RPM_BUILD_ROOT`cups-config --serverbin` \
	CUPSDATA=$RPM_BUILD_ROOT`cups-config --datadir`

mv -f $RPM_BUILD_ROOT%{_bindir}/gsc $RPM_BUILD_ROOT%{_bindir}/gs
cd ijs
make install DESTDIR=${RPM_BUILD_ROOT}
cd ..

install -m0644 base/errors.h $RPM_BUILD_ROOT%{_includedir}/ghostscript
cd ..
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.a

echo ".so man1/gs.1" > $RPM_BUILD_ROOT/%{_mandir}/man1/ghostscript.1
ln -sf gs $RPM_BUILD_ROOT%{_bindir}/ghostscript

mkdir -p $RPM_BUILD_ROOT%{_datadir}/ghostscript/conf.d
mkdir -p $RPM_BUILD_ROOT/etc/ghostscript/%{gs_dot_ver}
touch $RPM_BUILD_ROOT/etc/ghostscript/%{gs_dot_ver}/Fontmap.local
touch $RPM_BUILD_ROOT/etc/ghostscript/%{gs_dot_ver}/cidfmap.local


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, bin) %{_libdir}/cups
%{_libdir}/cups/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/cups
%{_datadir}/cups/*
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*
%dir %attr (0755, root, bin) %{_datadir}/ghostscript
%{_datadir}/ghostscript/*

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%files -n SUNWghostscriptd
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%files -n SUNWghostscriptr
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/*

%changelog
* Tue Jun 23 2009 - Moinak Ghosh <moinakg@belenix(dot)org>
- Initial version to replace the poorly packaged one in SFW gate.
