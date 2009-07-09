#
# spec file for package SUNWlibgmime
#
# includes module(s): gmime
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jerrytan
#

%include Solaris.inc

%use gmime = gmime.spec

Name:          SUNWlibgmime
Version:       %{gmime.version}
Summary:       Libraries and binaries to parse and index mail messages
SUNW_BaseDir:  %{_basedir}
SUNW_Copyright:%{name}.copyright
BuildRoot:     %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:      SUNWzlib
Requires:      SUNWlibms
Requires:      SUNWgnome-base-libs
BuildRequires: SUNWgnome-base-libs-devel

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires:      %name

%prep
rm -rf %name-%version
mkdir %name-%version
%gmime.prep -d %name-%version

%build
export PKG_CONFIG_PATH=%{_pkg_config_path}
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="%_ldflags"

%gmime.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%gmime.install -d %name-%version

# conflicts with SUNWesu
rm $RPM_BUILD_ROOT%{_bindir}/uuencode
rm $RPM_BUILD_ROOT%{_bindir}/uudecode
##Uncomment rmdir line when bumped to 2.3.x.
##rmdir $RPM_BUILD_ROOT%{_bindir}

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):unsupported" $RPM_BUILD_ROOT}

%clean 
rm -rf $RPM_BUILD_ROOT

%files 
%doc -d gmime-%{gmime.version} README AUTHORS 
%doc(bzip2) -d gmime-%{gmime.version} NEWS COPYING ChangeLog
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %dir %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %dir %{_libdir}
%{_libdir}/*.sh
%{_libdir}/*.so*

%files devel
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %dir %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %dir %{_datadir}
%{_datadir}/gtk-doc

%changelog
* Fri Jun 06 2008 - damien.carbery@sun.com
- Revert to 2.2.21 as tracker does not yet support 2.3.x.
* Fri May 30 2008 - damien.carbery@sun.com
- Remove %{_bindir} and %{_libdir} from %files as 2.3.0 tarball does not 
  deliver files to there anymore.
* Thu Mar 27 2008 - halton.huo@sun.com
- Add copyright file
* Sun Mar 02 2008 - simon.zheng@sun.com
- Correct package version numbers.
* Web Feb 27 2008 - Jerry.tan@sun.com
- rename from SUNWgmime to SUNWlibgmime
* Tue Jan 29 2008 - patrick.ale@gmail.com
- Remove no_gtk_doc validation. Always install gtk-doc
* Thu Jan 24 2008 - nonsea@users.sourceforge.net
- Remove mono stuff
- Add gtk-doc for %files devel
* Wed Jan 02 2008 - nonsea@users.sourceforge.net
- Rename from SFEgmime to SUNWgmime.
* Tue Jul 24 2007 - nonsea@users.sourceforge.net
- Bump to 2.2.10.
* Wed May  2 2007 - halton.huo@sun.com
- Bump to 2.2.8.
- Add check mono condition.
* Wed Sep  7 2006 - jedy.wang@sun.com
- bump to 2.2.3
* Sun Jul 13 2006 - laca@sun.com
- rename to SFEgmime
- include Solaris.inc
- correct patch file name, update CFLAGS, add gtk-docs to %files
* Wed Jul 12 2006 - jedy.wang@sun.com
- Initial spec
