#
# spec file for package SUNWimagick.spec
#
# includes module(s): imagemagick
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

%define src_name	ImageMagick
%define src_url		ftp://ftp.imagemagick.org/pub/%src_name
%define major		6.5.3
%define minor		-4

Name:                   SUNWimagick
Summary:                ImageMagick - Image Manipulation Utilities and Libraries
Version:                %{major}%{minor}
Source:                 %{src_url}/%{src_name}-%{version}.tar.bz2
Patch1:                 ImageMagick-01-Makefile.PL.in.diff
Patch2:                 ImageMagick-02-Magick.xs.diff

SUNW_BaseDir:           %{_basedir}
SUNW_Copyright:        %{name}.copyright
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
%include perl-depend.inc
Requires:               SUNWbzip
Requires:               SUNWxwplt
Requires:               SUNWxorg-clientlibs
Requires:               SUNWzlib
Requires:               SUNWfontconfig
Requires:               SUNWfreetype2
Requires:               SFEgraphviz
Requires:               SUNWjpg
Requires:               SFElcms
Requires:               SFEopenexr
Requires:               SUNWpng
Requires:               SUNWlibrsvg
Requires:               SUNWcairo
Requires:               SUNWTiff
Requires:               SUNWlxml
BuildRequires:          SUNWxorg-headers
BuildRequires:          SFEgraphviz-devel
BuildRequires:          SUNWjpg-devel
BuildRequires:          SFElcms-devel
BuildRequires:          SFEopenexr-devel
BuildRequires:          SUNWpng-devel
BuildRequires:          SUNWlibrsvg-devel
BuildRequires:          SUNWgnome-common-devel
BuildRequires:          SUNWlxml-devel

%description
ImageMagick is an image display and manipulation tool for the X
Window System. ImageMagick can read and write JPEG, TIFF, PNM, GIF,
and Photo CD image formats. It can resize, rotate, sharpen, color
reduce, or add special effects to an image, and when finished you can
either save the completed work in the original format or a different
one. ImageMagick also includes command line programs for creating
animated or transparent .gifs, creating composite images, creating
thumbnail images, and more.

ImageMagick is one of your choices if you need a program to manipulate
and display images. If you want to develop your own applications
which use ImageMagick code or APIs, you need to install
ImageMagick-devel as well.


%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires:               SUNWxorg-headers
Requires:               SFEgraphviz-devel
Requires:               SUNWjpg-devel
Requires:               SFElcms-devel
Requires:               SFEopenexr-devel
Requires:               SUNWpng-devel
Requires:               SUNWlibrsvg-devel
Requires:               SUNWgnome-common-devel
Requires:               SUNWlxml-devel

%prep
%setup -q -c -n %name-%version
%if %cc_is_gcc
cd %{src_name}-%{version}
%patch1 -p1
%patch2 -p1
cd ..
%endif

%ifarch amd64 sparcv9
cp -rp %{src_name}-%{version} %{src_name}-%{version}-64
%endif


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

%if %cc_is_gcc
GCC_EXTRA_OPTS="-mmmx -msse -msse2 -msse3 -m3dnow -ffast-math -ftree-vectorize -funroll-loops -finline-functions -findirect-inlining -ftree-loop-linear -floop-interchange -floop-strip-mine -floop-block -ftree-loop-distribution -fivopts -ftree-loop-im"
%endif
 
%ifarch amd64 sparcv9
cd %{src_name}-%{version}-64

export CPPFLAGS="-I%{_prefix}/include/freetype2 -I%{xorg_inc} -I%{_prefix}/include/libxml2"
export LDFLAGS="%_ldflags64 -L%{xorg_lib} -R%{xorg_lib}"
export CFLAGS="-O3 -march=opteron -m64 -fno-omit-frame-pointer -fno-strict-aliasing -fPIC -DPIC ${GCC_EXTRA_OPTS}"
export CXXFLAGS="-O3 -march=opteron -m64 -fno-omit-frame-pointer -fno-strict-aliasing -fPIC -DPIC ${GCC_EXTRA_OPTS}"
./configure --prefix=%{_prefix}         \
            --bindir=%{_bindir}/%{_arch64}         \
            --mandir=%{_mandir}         \
            --libdir=%{_libdir}/%{_arch64}         \
            --datadir=%{_datadir}       \
            --libexecdir=%{_libexecdir}/%{_arch64} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared             \
            --disable-static            \
            --with-magick_plus_plus     \
            --without-perl

make -j$CPUS
cd ..
%endif

cd %{src_name}-%{version}
export CPPFLAGS="-I%{_prefix}/include/freetype2 -I%{xorg_inc}"
export LDFLAGS="%_ldflags -L%{xorg_lib} -R%{xorg_lib}"
export CFLAGS="-O3 -march=pentium4 -fomit-frame-pointer -fno-strict-aliasing -fPIC -DPIC ${GCC_EXTRA_OPTS}"
export CXXFLAGS="-O3 -march=pentium4 -fomit-frame-pointer -fno-strict-aliasing -fPIC -DPIC ${GCC_EXTRA_OPTS}"
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared		\
	    --disable-static            \
            --with-magick_plus_plus

make -j$CPUS 
cd ..

%install
rm -rf $RPM_BUILD_ROOT

ln -sf %{_prefix}/gnu/bin/gcc cc
export PATH=`pwd`:${PATH}

%ifarch amd64 sparcv9
cd %{src_name}-%{version}-64

make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a
find $RPM_BUILD_ROOT%{_libdir} -name lib\*.\*a -exec rm {} \;
cd ..
%endif

cd %{src_name}-%{version}

make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a
find $RPM_BUILD_ROOT%{_libdir} -name lib\*.\*a -exec rm {} \;
site_perl=$RPM_BUILD_ROOT/usr/perl5/site_perl
vendor_perl=$RPM_BUILD_ROOT/usr/perl5/vendor_perl
mv ${site_perl}/* $vendor_perl

find $RPM_BUILD_ROOT -name perllocal.pod | xargs rm -f 
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/%{src_name}-%{major}

%ifarch amd64 sparcv9
%dir %attr (0755,root,bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%{_libdir}/%{_arch64}/%{src_name}-%{major}
%endif

%dir %attr (0755,root,sys) %{_datadir}
%{_datadir}/%{src_name}-%{major}
%{_mandir}
%dir %attr (0755,root,other) %{_datadir}/doc
%{_datadir}/doc/*
%{_prefix}/perl5

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755,root,bin) %{_libdir}
%dir %attr (0755,root,other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%ifarch amd64 sparcv9
%dir %attr (0755,root,bin) %{_libdir}/%{_arch64}
%dir %attr (0755,root,other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%changelog
* Mon Jun 15 2009 - moinakg@belenix(dot)org
- Bump version to 6.5.3-4.
- Add 64Bit build.
* Sat Jan 26 2008 - moinak.ghosh@sun.com
- Bump version to 6.3.6-10.
- Add check to prevent build using Gcc.
- Add dependency on Perl.
* Sun Nov 18 2007 - daymobrew@users.sourceforge.net
- Bump to 6.3.6-9.
* Tue Jul 10 2007 - brian.cameron@sun.com
- Bump to 6.3.5.  Remove the -xc99=%none from CFLAGS since
  it is breaking the build.
* Tue Jun  5 2007 - dougs@truemail.co.th
- Initial version - version in sfw is too old :(
