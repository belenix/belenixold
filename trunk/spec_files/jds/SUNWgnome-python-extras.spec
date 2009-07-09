#
# spec file for package SUNWgnome-python-extras
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: dkenny
#
%include Solaris.inc

%define pythonver 2.4
%use gpe = gnome-python-extras.spec

Name:                    SUNWgnome-python-extras
Summary:                 Supplemental Python %{pythonver} bindings for GNOME
URL:                     %{gpe.url}
Version:                 %{gpe.version}
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                SUNWPython
Requires:                SUNWgnome-python-libs
Requires:                SUNWfirefox
Requires:                SUNWgksu
Requires:                SUNWgtkspell
BuildRequires:           SUNWgnome-python-libs-devel
BuildRequires:           SUNWfirefox-devel
BuildRequires:           SUNWgksu-devel
BuildRequires:           SUNWgtkspell-devel
BuildRequires:           SUNWpython-setuptools

%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
# the 2.6 devel package is required because it contains the headers
# (they are not duplicated in this package, since they would be identical)
Requires: SUNWgnome-python26-extras-devel

%prep
rm -rf %name-%version
mkdir -p %name-%version
%gpe.prep -d %name-%version

%build
export PYTHON=/usr/bin/python%{pythonver}
export PKG_CONFIG_PATH=/usr/lib/python%{pythonver}/pkgconfig
%gpe.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%gpe.install -d %name-%version

# included in SUNWggnome-python26-extras
rm -r $RPM_BUILD_ROOT%{_datadir}/pygtk

# move to subdir to avoid conflict with python 2.6
mv $RPM_BUILD_ROOT%{_libdir}/pkgconfig \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{pythonver}/vendor-packages/gtk-2.0/*
%doc -d gnome-python-extras-%{gpe.version} AUTHORS COPYING README
%doc(bzip2) -d gnome-python-extras-%{gpe.version} COPYING.GPL COPYING.LGPL ChangeLog NEWS
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, sys) %{_datadir}

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, other) %{_libdir}/python%{pythonver}/pkgconfig
%{_libdir}/python%{pythonver}/pkgconfig/*

%changelog
* Thu Feb 26 2009 - brian.cameron@sun.com
- Update to use base-spec.file.
* Tue Feb 24 2009 - laca@sun.com
- set PYTHON and PKG_CONFIG_PATH so the correct python version and
  dependencies are picked up
* Tue Feb 10 2009 - halton.huo@sun.com
- Add Requires: SUNWgtkspell to fix issue #3 for CR6753371
* Tue Nov 25 2008 - brian.lu@sun.com
- Remove "with-ff3" option, not needed any more
* Fri Sep 12 2008 - matt.keenn@sun.com
- Update copyright
* Fri May 30 2008 - evan.yan@sun.com
- Add option "--with-ff3" to enable building with Firefox3
- Add patch gnome-python-extras-02-using-firefox3.diff
* Wed May 21 2008 - damien.carbery@sun.com
- Add Build/Requires: SUNWfirefox/-devel and SUNWgksu/-devel after
  check-deps.pl run.
* Wed Feb 20 2007 - Darren Kenny <darren.kenny@sun.com>
- Move from spec-files-other since it's GNOME related.
* Mon Feb 18 2007 - Darren Kenny <darren.kenny@sun.com>
- Import into svn.opensolaris.org/spec-files-other
* Tue Jul 10 2007 - Brian Cameron <brian.cameron@sun.com>
- Bump to 2.19.1
* Fri Feb 9 2007 - Irene Huang <irene.huang@sun.com>
- created
