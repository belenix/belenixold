#
# spec file for package SUNWgegl
#
# includes module(s):gegl
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: bewitche

%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use gegl_64 = gegl_64.spec
%endif
%include base.inc
%use gegl = gegl.spec

Name:                    SUNWgegl
Summary:                 GEGL (Generic Graphics Library) is a graph based image processing framework.
Version:                 %{default_pkg_version}
Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:		 SUNWgegl.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:                SUNWbabl
Requires:                SFEopenexr
Requires:                SFEsdl
Requires:                SFEgraphviz
Requires:                SUNWlibrsvg
Requires:                SUNWjpg
Requires:                SUNWpng
Requires:                SUNWglib2
Requires:                SUNWgtk2
Requires:                SUNWcairo
Requires:                SUNWpango
BuildRequires:           SUNWbabl-devel
BuildRequires:           SFEopenexr-devel
BuildRequires:           SUNWlibrsvg-devel
BuildRequires:           SUNWjpg-devel
BuildRequires:           SUNWpng-devel
BuildRequires:           SUNWglib2-devel
BuildRequires:           SUNWgtk2-devel
BuildRequires:           SUNWcairo-devel
BuildRequires:           SUNWpango-devel
BuildRequires:           SFEsdl-devel
BuildRequires:           SFEffmpeg-devel
buildRequires:           SFEgraphviz-devel
%if %cc_is_gcc
Requires:                SFEgccruntime
%endif

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires:                SUNWbabl-devel
Requires:                SFEopenexr-devel
Requires:                SFEsdl-devel
Requires:                SUNWlibrsvg-devel
Requires:                SUNWjpg-devel
Requires:                SUNWpng-devel
Requires:                SUNWglib2-devel
Requires:                SUNWgtk2-devel
Requires:                SUNWcairo-devel
Requires:                SUNWpango-devel
Requires:                SFEgraphviz-devel

%package ffmpeg-plugin
Summary:                 Gegl plugin for FFmpeg
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires:                SFEffmpeg

%prep
rm -rf %name-%version
mkdir %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%gegl_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%gegl_64.prep -d %name-%version/%{base_arch}
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar -xf -

%build
%if %cc_is_gcc
LDFLAGS="-L/usr/gnu/lib -R/usr/gnu/lib"
export LDFLAGS
%endif
%gegl.build -d %name-%version/%{base_arch}

%ifarch amd64 sparcv9
%if %cc_is_gcc
LDFLAGS="-L/usr/gnu/lib/%{_arch64} -R/usr/gnu/lib/%{_arch64}"
export LDFLAGS
%endif
%gegl_64.build -d %name-%version/%_arch64
%endif



%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%gegl_64.install -d %name-%version/%_arch64
%endif

%gegl.install -d %name-%version/%{base_arch}
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc -d %{base_arch} gegl-%{gegl.version}/AUTHORS
%doc -d %{base_arch} gegl-%{gegl.version}/README
%doc(bzip2) -d %{base_arch} gegl-%{gegl.version}/ChangeLog
%doc(bzip2) -d %{base_arch} gegl-%{gegl.version}/COPYING
%doc(bzip2) -d %{base_arch} gegl-%{gegl.version}/NEWS
%doc(bzip2) -d %{base_arch} gegl-%{gegl.version}/COPYING.LESSER
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}/gegl-0.0
%{_libdir}/%{_arch64}/gegl-0.0/save-buffer.so
%{_libdir}/%{_arch64}/gegl-0.0/dst-over.so
%{_libdir}/%{_arch64}/gegl-0.0/divide.so
%{_libdir}/%{_arch64}/gegl-0.0/src-atop.so
%{_libdir}/%{_arch64}/gegl-0.0/difference-of-gaussians.so
%{_libdir}/%{_arch64}/gegl-0.0/multiply.so
%{_libdir}/%{_arch64}/gegl-0.0/snn-mean.so
%{_libdir}/%{_arch64}/gegl-0.0/remap.so
%{_libdir}/%{_arch64}/gegl-0.0/svg-load.so
%{_libdir}/%{_arch64}/gegl-0.0/lighten.so
%{_libdir}/%{_arch64}/gegl-0.0/stress.so
%{_libdir}/%{_arch64}/gegl-0.0/pixbuf.so
%{_libdir}/%{_arch64}/gegl-0.0/threshold.so
%{_libdir}/%{_arch64}/gegl-0.0/exclusion.so
%{_libdir}/%{_arch64}/gegl-0.0/fractal-explorer.so
%{_libdir}/%{_arch64}/gegl-0.0/over.so
%{_libdir}/%{_arch64}/gegl-0.0/dst-out.so
%{_libdir}/%{_arch64}/gegl-0.0/src-out.so
%{_libdir}/%{_arch64}/gegl-0.0/affine.so
%{_libdir}/%{_arch64}/gegl-0.0/screen.so
%{_libdir}/%{_arch64}/gegl-0.0/difference.so
%{_libdir}/%{_arch64}/gegl-0.0/color-temperature.so
%{_libdir}/%{_arch64}/gegl-0.0/display.so
%{_libdir}/%{_arch64}/gegl-0.0/darken.so
%{_libdir}/%{_arch64}/gegl-0.0/color-burn.so
%{_libdir}/%{_arch64}/gegl-0.0/gamma.so
%{_libdir}/%{_arch64}/gegl-0.0/magick-load.so
%{_libdir}/%{_arch64}/gegl-0.0/path.so
%{_libdir}/%{_arch64}/gegl-0.0/invert.so
%{_libdir}/%{_arch64}/gegl-0.0/src.so
%{_libdir}/%{_arch64}/gegl-0.0/src-over.so
%{_libdir}/%{_arch64}/gegl-0.0/unsharp-mask.so
%{_libdir}/%{_arch64}/gegl-0.0/dst-atop.so
%{_libdir}/%{_arch64}/gegl-0.0/layer.so
%{_libdir}/%{_arch64}/gegl-0.0/svg-luminancetoalpha.so
%{_libdir}/%{_arch64}/gegl-0.0/add.so
%{_libdir}/%{_arch64}/gegl-0.0/mblur.so
%{_libdir}/%{_arch64}/gegl-0.0/raw-load.so
%{_libdir}/%{_arch64}/gegl-0.0/grey.so
%{_libdir}/%{_arch64}/gegl-0.0/svg-saturate.so
%{_libdir}/%{_arch64}/gegl-0.0/stretch-contrast.so
%{_libdir}/%{_arch64}/gegl-0.0/normal.so
%{_libdir}/%{_arch64}/gegl-0.0/clone.so
%{_libdir}/%{_arch64}/gegl-0.0/nop.so
%{_libdir}/%{_arch64}/gegl-0.0/png-load.so
%{_libdir}/%{_arch64}/gegl-0.0/c2g.so
%{_libdir}/%{_arch64}/gegl-0.0/write-buffer.so
%{_libdir}/%{_arch64}/gegl-0.0/shift.so
%{_libdir}/%{_arch64}/gegl-0.0/exr-load.so
%{_libdir}/%{_arch64}/gegl-0.0/rectangle.so
%{_libdir}/%{_arch64}/gegl-0.0/noise.so
%{_libdir}/%{_arch64}/gegl-0.0/svg-matrix.so
%{_libdir}/%{_arch64}/gegl-0.0/brightness-contrast.so
%{_libdir}/%{_arch64}/gegl-0.0/checkerboard.so
%{_libdir}/%{_arch64}/gegl-0.0/gaussian-blur.so
%{_libdir}/%{_arch64}/gegl-0.0/open-buffer.so
%{_libdir}/%{_arch64}/gegl-0.0/load-buffer.so
%{_libdir}/%{_arch64}/gegl-0.0/value-invert.so
%{_libdir}/%{_arch64}/gegl-0.0/soft-light.so
%{_libdir}/%{_arch64}/gegl-0.0/hard-light.so
%{_libdir}/%{_arch64}/gegl-0.0/load.so
%{_libdir}/%{_arch64}/gegl-0.0/box-blur.so
%{_libdir}/%{_arch64}/gegl-0.0/text.so
%{_libdir}/%{_arch64}/gegl-0.0/jpg-load.so
%{_libdir}/%{_arch64}/gegl-0.0/svg-multiply.so
%{_libdir}/%{_arch64}/gegl-0.0/src-in.so
%{_libdir}/%{_arch64}/gegl-0.0/levels.so
%{_libdir}/%{_arch64}/gegl-0.0/subtract.so
%{_libdir}/%{_arch64}/gegl-0.0/convert-format.so
%{_libdir}/%{_arch64}/gegl-0.0/dst-in.so
%{_libdir}/%{_arch64}/gegl-0.0/overlay.so
%{_libdir}/%{_arch64}/gegl-0.0/whitebalance.so
%{_libdir}/%{_arch64}/gegl-0.0/xor.so
%{_libdir}/%{_arch64}/gegl-0.0/plus.so
%{_libdir}/%{_arch64}/gegl-0.0/contrast-curve.so
%{_libdir}/%{_arch64}/gegl-0.0/png-save.so
%{_libdir}/%{_arch64}/gegl-0.0/mono-mixer.so
%{_libdir}/%{_arch64}/gegl-0.0/clear.so
%{_libdir}/%{_arch64}/gegl-0.0/tonemap.so
%{_libdir}/%{_arch64}/gegl-0.0/introspect.so
%{_libdir}/%{_arch64}/gegl-0.0/dropshadow.so
%{_libdir}/%{_arch64}/gegl-0.0/svg-huerotate.so
%{_libdir}/%{_arch64}/gegl-0.0/bilateral-filter.so
%{_libdir}/%{_arch64}/gegl-0.0/color-dodge.so
%{_libdir}/%{_arch64}/gegl-0.0/opacity.so
%{_libdir}/%{_arch64}/gegl-0.0/save-pixbuf.so
%{_libdir}/%{_arch64}/gegl-0.0/color.so
%{_libdir}/%{_arch64}/gegl-0.0/dst.so
%{_libdir}/%{_arch64}/gegl-0.0/crop.so
%endif
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, bin) %{_libdir}/gegl-0.0
%{_libdir}/gegl-0.0/save-buffer.so
%{_libdir}/gegl-0.0/dst-over.so
%{_libdir}/gegl-0.0/divide.so
%{_libdir}/gegl-0.0/src-atop.so
%{_libdir}/gegl-0.0/difference-of-gaussians.so
%{_libdir}/gegl-0.0/multiply.so
%{_libdir}/gegl-0.0/snn-mean.so
%{_libdir}/gegl-0.0/remap.so
%{_libdir}/gegl-0.0/svg-load.so
%{_libdir}/gegl-0.0/lighten.so
%{_libdir}/gegl-0.0/stress.so
%{_libdir}/gegl-0.0/pixbuf.so
%{_libdir}/gegl-0.0/threshold.so
%{_libdir}/gegl-0.0/exclusion.so
%{_libdir}/gegl-0.0/fractal-explorer.so
%{_libdir}/gegl-0.0/over.so
%{_libdir}/gegl-0.0/dst-out.so
%{_libdir}/gegl-0.0/src-out.so
%{_libdir}/gegl-0.0/affine.so
%{_libdir}/gegl-0.0/screen.so
%{_libdir}/gegl-0.0/difference.so
%{_libdir}/gegl-0.0/color-temperature.so
%{_libdir}/gegl-0.0/display.so
%{_libdir}/gegl-0.0/darken.so
%{_libdir}/gegl-0.0/color-burn.so
%{_libdir}/gegl-0.0/gamma.so
%{_libdir}/gegl-0.0/magick-load.so
%{_libdir}/gegl-0.0/path.so
%{_libdir}/gegl-0.0/invert.so
%{_libdir}/gegl-0.0/src.so
%{_libdir}/gegl-0.0/src-over.so
%{_libdir}/gegl-0.0/unsharp-mask.so
%{_libdir}/gegl-0.0/dst-atop.so
%{_libdir}/gegl-0.0/layer.so
%{_libdir}/gegl-0.0/svg-luminancetoalpha.so
%{_libdir}/gegl-0.0/add.so
%{_libdir}/gegl-0.0/mblur.so
%{_libdir}/gegl-0.0/raw-load.so
%{_libdir}/gegl-0.0/grey.so
%{_libdir}/gegl-0.0/svg-saturate.so
%{_libdir}/gegl-0.0/stretch-contrast.so
%{_libdir}/gegl-0.0/normal.so
%{_libdir}/gegl-0.0/clone.so
%{_libdir}/gegl-0.0/nop.so
%{_libdir}/gegl-0.0/png-load.so
%{_libdir}/gegl-0.0/c2g.so
%{_libdir}/gegl-0.0/write-buffer.so
%{_libdir}/gegl-0.0/shift.so
%{_libdir}/gegl-0.0/exr-load.so
%{_libdir}/gegl-0.0/rectangle.so
%{_libdir}/gegl-0.0/noise.so
%{_libdir}/gegl-0.0/svg-matrix.so
%{_libdir}/gegl-0.0/brightness-contrast.so
%{_libdir}/gegl-0.0/checkerboard.so
%{_libdir}/gegl-0.0/gaussian-blur.so
%{_libdir}/gegl-0.0/open-buffer.so
%{_libdir}/gegl-0.0/load-buffer.so
%{_libdir}/gegl-0.0/value-invert.so
%{_libdir}/gegl-0.0/soft-light.so
%{_libdir}/gegl-0.0/hard-light.so
%{_libdir}/gegl-0.0/load.so
%{_libdir}/gegl-0.0/box-blur.so
%{_libdir}/gegl-0.0/text.so
%{_libdir}/gegl-0.0/jpg-load.so
%{_libdir}/gegl-0.0/svg-multiply.so
%{_libdir}/gegl-0.0/src-in.so
%{_libdir}/gegl-0.0/levels.so
%{_libdir}/gegl-0.0/subtract.so
%{_libdir}/gegl-0.0/convert-format.so
%{_libdir}/gegl-0.0/dst-in.so
%{_libdir}/gegl-0.0/overlay.so
%{_libdir}/gegl-0.0/whitebalance.so
%{_libdir}/gegl-0.0/xor.so
%{_libdir}/gegl-0.0/plus.so
%{_libdir}/gegl-0.0/contrast-curve.so
%{_libdir}/gegl-0.0/png-save.so
%{_libdir}/gegl-0.0/mono-mixer.so
%{_libdir}/gegl-0.0/clear.so
%{_libdir}/gegl-0.0/tonemap.so
%{_libdir}/gegl-0.0/introspect.so
%{_libdir}/gegl-0.0/dropshadow.so
%{_libdir}/gegl-0.0/svg-huerotate.so
%{_libdir}/gegl-0.0/bilateral-filter.so
%{_libdir}/gegl-0.0/color-dodge.so
%{_libdir}/gegl-0.0/opacity.so
%{_libdir}/gegl-0.0/save-pixbuf.so
%{_libdir}/gegl-0.0/color.so
%{_libdir}/gegl-0.0/dst.so
%{_libdir}/gegl-0.0/crop.so
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, bin) %{_includedir}/gegl-0.0
%{_includedir}/gegl-0.0/*.h
%dir %attr (0755, root, bin) %{_includedir}/gegl-0.0/operation
%{_includedir}/gegl-0.0/operation/*.h
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %dir %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %dir %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/gtk-doc
%dir %attr (0755, root, bin) %{_datadir}/gtk-doc/html
%dir %attr (0755, root, bin) %{_datadir}/gtk-doc/html/gegl
%{_datadir}/gtk-doc/html/gegl/*

%files ffmpeg-plugin
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/gegl-0.0
%{_libdir}/gegl-0.0/ff-load.so

#%ifarch amd64 sparcv9
#%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
#%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}/gegl-0.0
#%{_libdir}/%{_arch64}/gegl-0.0/ff-load.so
#%endif

%changelog
* Thu Mar 26 2009  chris.wang@sun.com
- Correct copyright file
* Fri Feb 20 2009  chris.wang@sun.com
- Add manpage
* Thu Feb 6  2008 - chris.wang@sun.com
- Add SUNWsdl and SUNWrsvg as required packages
* Tue Dec 16 2008 - chris.wang@sun.com
- Fix SparcV9 file section problem
* Wed Nov 26 2008 - chris.wang@sun.com
- Initial Create
