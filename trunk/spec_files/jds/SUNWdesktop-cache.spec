#
# spec file for package SUNWdesktop-cache
#
# includes module(s): desktop-cache
#
# Owner: erwannc

%include Solaris.inc

Name:         SUNWdesktop-cache
License:      Other
Group:        System/Libraries
Version:      0.2.0
Summary:      desktop-cache is a set of SMF services used to update the various GNOME desktop caches.
Source:       http://dlc.sun.com/osol/jds/downloads/extras/desktop-cache/desktop-cache-smf-services-%{version}.tar.bz2
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
SUNW_BaseDir: /
SUNW_Copyright: %{name}.copyright

%include default-depend.inc
#Requires:    SUNWgnome-base-libs
#Requires:    SUNWgnome-vfs
#Requires:    SUNWgnome-config

%prep
%setup -q -n desktop-cache-smf-services-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

./configure --libdir=/lib \
            --datadir=/usr/share \
	    --sysconfdir=/var
make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%clean 
rm -rf $RPM_BUILD_ROOT

%files 
# don't use %_localstatedir here, because this is an absolute path
# defined by another package, so it has to be /var/svc even if this
# package's %_localstatedir is redefined
%doc README AUTHORS
%doc(bzip2) COPYING NEWS ChangeLog
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, sys) %{_datadir}
#%dir %attr (0755, root, other) %{_datadir}/doc
%attr (-, root, bin) %{_datadir}/desktop-cache
%defattr (-, root, sys)
%attr (-, root, sys) %class (manifest) /var/svc/manifest
%defattr (-, root, bin)
%dir %attr (0755, root, bin) /lib
/lib/svc
%defattr (-, root, sys)

%changelog
* Thu Apr  2 2009 - laca@sun.com
- bump to 0.2.0
* Mon Mar 23 2009 - jeff.cai@sun.com
- Since /lib/svc/method/gconf-cache (SUNWdesktop-cache) requires
  /usr/bin/gconftool-2 which is found in SUNWgnome-config, add the
  dependency.
- Since /lib/svc/method/icon-cache (SUNWdesktop-cache) requires
  /usr/bin/gtk-update-icon-cache which is found in SUNWgnome-base-libs,
  add the dependency.
- Since /lib/svc/method/mime-types-cache (SUNWdesktop-cache) requires
  /usr/bin/update-mime-database which is found in SUNWgnome-vfs, add
  the dependency.
* Wed Feb 02 2009 - ghee.teo@sun.com
- uprev tarball to 0.1.6 which contain fix to d.o.o #2399 
  tarball version 0.1.4 and 0.1.5 are bad fixes.
* Wed Sep 17 2008 - ghee.teo@sun.com
- uprev tarball to 0.1.2 to incldue CDDL COPYING file. add %doc to %files.
  Leave Laca's patch untouched to avoid having to roll another tarball when
  bug is fixed.
* Sat Jun 28 2008 - laca@sun.com
- add patch stability.diff that updates the stability classification
  in the manifests until smf's dtd is updated to the new interface
  taxonomy.
* Fri Jun 27 2008 - laca@sun.com
- bump to 0.1.1
* Thu Jun 5 2008 - laca@sun.com
- fix %files and delete unnecessary autotools to speed up build
* Tue Jun 3 2008 - erwann.chenede@sun.com
- Initial spec

