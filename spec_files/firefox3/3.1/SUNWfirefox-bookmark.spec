#
# spec file for package SUNWfirefox-bookmark
#
# includes module(s): firefox-bookmark
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: Alfred
#
%include Solaris.inc
%use firefox = firefox.spec

Name:                    SUNWfirefox-bookmark
Summary:                 Firefox's default bookmark
Version:                 %{firefox.version}
Vendor:                  Sun Microsystems, Inc.
# default bookmarks for OpenSolaris
Source:                  opensolaris-default-bookmarks.html
# default bookmarks for development Solaris builds
Source1:                 firefox-default-bookmarks.html
SUNW_Copyright:          SUNWfirefox.copyright

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-build
%include default-depend.inc
Requires: SUNWfirefox

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_libdir}/firefox/defaults/profile/
%if %option_with_indiana_branding
cp %{SOURCE} $RPM_BUILD_ROOT%{_libdir}/firefox/defaults/profile/bookmarks.html
%else
cp %{SOURCE1} $RPM_BUILD_ROOT%{_libdir}/firefox/defaults/profile/bookmarks.html
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%changelog
* Sat Dec 20 2008 - alfred.peng@sun.com
- Change the mod bits of the bookmark file to 0644.
* Fri Nov 28 2008 - alfred.peng@sun.com
- Initial version
