#
# spec file for package SFEdjvulibre
#
# includes module(s): djvulibre
#
#
%include Solaris.inc
%include base.inc

Name:                    SFEdjvulibre
Summary:                 Viewers, encoders and utilities for the Djvu document format
Version:                 3.5.21
URL:                     http://djvu.sourceforge.net/
Source:                  %{sf_download}/djvu/djvulibre-%{version}.tar.gz
Patch1:                  djvulibre-01-ja-encoding.diff
Patch2:                  djvulibre-02-configure.diff

License:                 GPLv2+
SUNW_BaseDir:            %{_basedir}
#SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:               SUNWjpg
Requires:               SUNWTiff
Requires:               SFEqt3
Requires:               SUNWxdg-utils
BuildRequires:          SUNWjpg-devel
BuildRequires:          SUNWTiff-devel
BuildRequires:          SFEqt3-devel
BuildRequires:          SUNWgnome-common-devel

%description
DjVu is a web-centric format and software platform for distributing documents
and images. DjVu can advantageously replace PDF, PS, TIFF, JPEG, and GIF for
distributing scanned documents, digital documents, or high-resolution pictures.
DjVu content downloads faster, displays and renders faster, looks nicer on a
screen, and consume less client resources than competing formats. DjVu images
display instantly and can be smoothly zoomed and panned with no lengthy
re-rendering.

DjVuLibre is a free (GPL'ed) implementation of DjVu, including viewers,
decoders, simple encoders, and utilities. The browser plugin is in its own
separate sub-package.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires:          SUNWjpg-devel
Requires:          SUNWTiff
Requires:          SFEqt3-devel
Requires:          SUNWgnome-common-devel

%prep
%setup -q -c -n %name-%version
cd djvulibre-%{version}
%patch1 -p1
%patch2 -p1
cd ..

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

cd djvulibre-%{version}
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --bindir=%{_bindir}                  \
            --libdir=%{_libdir}                  \
            --enable-shared		                 \
            --disable-static

(cd i18n
 for d in cs de fr ja
 do
   cd ${d}
   cp Makefile Makefile.orig
   cat Makefile.orig | sed 's#RM = /usr/gnu/bin/rm#RM = /usr/gnu/bin/rm \-f#' > Makefile
   cd ..
 done
)
make -j$CPUS
cd ..


%install
rm -rf $RPM_BUILD_ROOT

cd djvulibre-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/firefox/plugins
mv ${RPM_BUILD_ROOT}%{_libdir}/netscape/plugins/* \
   ${RPM_BUILD_ROOT}%{_libdir}/firefox/plugins/
rm -rf ${RPM_BUILD_ROOT}%{_libdir}/netscape

find ${RPM_BUILD_ROOT}%{_libdir} -name '*.so*' | xargs chmod +x
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%post
# Register the djview3 menu entries.
%{_datadir}/djvu/djview3/desktop/register-djview-menu install || :
# Register the djvu mime types and icons
%{_datadir}/djvu/osi/desktop/register-djvu-mime install || :

%preun
# Unegister the djview3 menu entries.
%{_datadir}/djvu/djview3/desktop/register-djview-menu uninstall || :
# Unegister the djvu mime types and icons
%{_datadir}/djvu/osi/desktop/register-djvu-mime uninstall || :


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, bin) %{_libdir}/firefox
%dir %attr (0755, root, bin) %{_libdir}/firefox/plugins
%{_libdir}/firefox/plugins/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Tue Jun 23 2009 - Moinak Ghosh <moinakg@belenix(dot)org>
- Initial version
