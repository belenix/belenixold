#
# spec file for package SFEpoppler
#
# includes module(s): poppler
#
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

Name:                    SFEpoppler
Summary:                 PDF Rendering Library. Alternate build with Qt support.
Version:                 0.10.7
%define dataversion      0.2.1
URL:                     http://poppler.freedesktop.org/
Source:                  http://poppler.freedesktop.org/poppler-%{version}.tar.gz
Source1:                 http://poppler.freedesktop.org/poppler-data-%{dataversion}.tar.gz
Patch1:                  poppler-01-uninstalled.pc.diff
Patch2:                  poppler-02-64bit-fix.diff
License:                 GPLv2 and Redistributable, no modification permitted for charmap data

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:               SUNWgtk2
Requires:               SUNWcairo
Requires:               SUNWjpg
Requires:               SFEqt3
Requires:               SFEqt4
BuildRequires:          SUNWgtk2-devel
BuildRequires:          SUNWcairo-devel
BuildRequires:          SUNWjpg-devel
BuildRequires:          SFEqt3-devel
BuildRequires:          SFEqt4-devel
BuildRequires:          SUNWgnome-common-devel

%description
Poppler is a fork of the xpdf PDF viewer developed by Derek Noonburg
of Glyph and Cog, LLC.  The purpose of forking xpdf is twofold.
First, we want to provide PDF rendering functionality as a shared
library, to centralize the maintenence effort.  Today a number of
applications incorporate the xpdf code base, and whenever a security
issue is discovered, all these applications exchange patches and put
out new releases.  In turn, all distributions must package and release
new version of these xpdf based viewers.  It's safe to say that
there's a lot of duplicated effort with the current situaion.  Even if
poppler in the short term introduces yet another xpdf derived code
base to the world, we hope that over time these applications will
adopt poppler.  After all, we only need one application to use poppler
to break even.

Second, we would like to move libpoppler forward in a number of areas
that doesn't fit within the goals of xpdf.  By design, xpdf depends on
very few libraries and runs a wide range of X based platforms.  This
is a strong feature and reasonable design goal.  However, with poppler
we would like to replace parts of xpdf that are now available as
standard components of modern Unix desktop environments.  One such
example is fontconfig, which solves the problem of matching and
locating fonts on the system, in a standardized and well understood
way.  Another example is cairo, which provides high quality 2D
rendering.

%package devel
Summary:                 %{summary} - Development files for Qt4 Support
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires:          SUNWgtk2-devel
Requires:          SUNWcairo-devel
Requires:          SFEqt3-devel
Requires:          SFEqt4-devel
Requires:          SUNWgnome-common-devel


%prep
%setup -q -c -a1 -n %name-%version
cd poppler-%{version}
%patch1 -p1
%patch2 -p1
cd ..

%ifarch amd64 sparcv9
cp -rp poppler-%{version} poppler-%{version}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

%ifarch amd64 sparcv9
cd poppler-%{version}-64
export CFLAGS="%optflags64"
export CXXFLAGS="%cxx_optflags64"
export LDFLAGS="%_ldflags64 -L%{_libdir}/%{_arch64} -R%{_libdir}/%{_arch64} %{gnu_lib_path64} %{xorg_lib_path64}"
export QTINC=%{_includedir}/qt3
export QTLIB=%{_libdir}/%{_arch64}

./configure --prefix=%{_prefix}/poppler  \
            --bindir=%{_prefix}/poppler/bin/%{_arch64}          \
            --libdir=%{_prefix}/poppler/lib/%{_arch64}          \
            --enable-poppler-glib                               \
            --enable-zlib                                       \
            --enable-cairo-output                               \
            --enable-poppler-qt                                 \
            --enable-poppler-qt4                                \
            --enable-shared		                        \
            --disable-static

make -j$CPUS 
cd ..
%endif

cd poppler-%{version}
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags %{gnu_lib_path} %{xorg_lib_path}"
export QTINC=%{_includedir}/qt3
export QTLIB=%{_libdir}

./configure --prefix=%{_prefix}/poppler  \
            --enable-poppler-glib        \
            --enable-zlib                \
            --enable-cairo-output        \
            --enable-poppler-qt          \
            --enable-poppler-qt4         \
            --enable-shared		 \
            --disable-static

make -j$CPUS
cd ..

cd poppler-data-%{dataversion}
cp COPYING COPYING-poppler-data
cp README README-poppler-data
cd ..


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd poppler-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_prefix}/poppler/lib/%{_arch64}/*.la
cd ..
%endif

cd poppler-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_prefix}/poppler/lib/*.la
cd ..

cd poppler-data-%{dataversion}
make install DESTDIR=$RPM_BUILD_ROOT datadir=%{_prefix}/poppler/share
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}/poppler
%dir %attr (0755, root, bin) %{_prefix}/poppler/bin
%{_prefix}/poppler/bin/*
%dir %attr (0755, root, bin) %{_prefix}/poppler/lib
%{_prefix}/poppler/lib/lib*.so*
%dir %attr (0755, root, bin) %{_prefix}/poppler/share
%{_prefix}/poppler/share/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_prefix}/poppler/lib/%{_arch64}
%{_prefix}/poppler/lib/%{_arch64}/lib*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}/poppler
%dir %attr (0755, root, bin) %{_prefix}/poppler/include
%{_prefix}/poppler/include/*
%dir %attr (0755, root, bin) %{_prefix}/poppler/lib
%dir %attr (0755, root, other) %{_prefix}/poppler/lib/pkgconfig
%{_prefix}/poppler/lib/pkgconfig/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_prefix}/poppler/lib/%{_arch64}
%dir %attr (0755, root, other) %{_prefix}/poppler/lib/%{_arch64}/pkgconfig
%{_prefix}/poppler/lib/%{_arch64}/pkgconfig/*
%endif

%changelog
* Tue Jun 23 2009 - Moinak Ghosh <moinakg@belenix(dot)org>
- Initial version. Alternate poppler with Qt support.
