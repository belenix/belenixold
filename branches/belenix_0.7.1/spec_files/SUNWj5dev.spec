#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

Name:                SUNWj5dev
Version:             1.5.0_14
%define jdk_dir jdk%{version}
%define archive_version 5.0u14
Summary:             JDK 5.0 Development Tools (%{version})
Source:              http://download.java.net/dlj/binaries/jdk-%{archive_version}-dlj-solaris-i586.sh
Source1:             http://download.java.net/dlj/binaries/jdk-%{archive_version}-dlj-solaris-amd64.sh

URL:                 https://jdk-distros.dev.java.net/
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:            SUNWj5rt

%package -n SUNWj5rt
Summary:             JDK 5.0 Runtime Environment (%{version})
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires:            SFEopenmotif
Requires:            SUNWlibC
Requires:            FSWxwrtl
Requires:            FSWxorg-clientlibs
Requires:            SUNWxwplr
Requires:            SUNWxwxft
Requires:            SUNWfontconfig

%package -n SUNWj5dmo
Summary:             JDK 5.0 Demo Programs (%{version})
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires:            SUNWj5rt

%package -n SUNWj5man
Summary:             JDK 5.0 Man Pages (%{version})
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires:            SUNWj5rt

%package -n SUNWj5rtx
Summary:             JDK 5.0 64-Bit Runtime Environment (%{version})
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires:            SUNWj5rt

%package -n SUNWj5dvx
Summary:             JDK 5.0 64-Bit Development Tools (%{version})
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires:            SUNWj5dev
Requires:            SUNWj5rtx

#%package -n SUNWj5dmx
#Summary:             JDK 5.0 64-Bit Demo Programs (%{version})
#SUNW_BaseDir:  %{_basedir}
#%include default-depend.inc
#Requires:            SUNWj5rtx

%prep
rm -rf %{name}-%{version}
mkdir %{name}-%{version}

%build
cd %{name}-%{version}
sh %{SOURCE} --accept-license --unpack

# Remove some files also delivered by the 64bit package
rm %{jdk_dir}/jre/LICENSE
rm %{jdk_dir}/jre/README
rm %{jdk_dir}/LICENSE
rm %{jdk_dir}/README.html

sh %{SOURCE1} --accept-license --unpack

%install

cd %{name}-%{version}
rm -rf ${RPM_BUILD_ROOT}
mkdir ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/jdk/instances
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
(cd ${RPM_BUILD_ROOT}%{_bindir}
    for prg in HtmlConverter appletviewer apt extcheck idlj jar jarsigner javac javadoc javah javap jdb native2ascii rmic serialver
    do
        ln -sf ../java/bin/$prg
    done
    for prg in ControlPanel java keytool orbd policytool rmid rmiregistry servertool tnameserv
    do
        ln -sf ../java/jre/bin/$prg
    done
    cd ..
    ln -s jdk/instances/%{jdk_dir} java)

(cd ${RPM_BUILD_ROOT}%{_prefix}/jdk/instances
    ln -sf %{jdk_dir} latest)

tar cpf - * | (cd ${RPM_BUILD_ROOT}%{_prefix}/jdk/instances; tar xpf - )

(cd ${RPM_BUILD_ROOT}
    find ./%{_prefix}/jdk/instances/%{jdk_dir}/jre \( -type f -o -type l \) | \
    grep -v amd64 | sed 's/^\.//') > rt_list.txt

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/HtmlConverter
%{_bindir}/appletviewer
%{_bindir}/apt
%{_bindir}/extcheck
%{_bindir}/idlj
%{_bindir}/jar
%{_bindir}/jarsigner
%{_bindir}/javac
%{_bindir}/javadoc
%{_bindir}/javah
%{_bindir}/javap
%{_bindir}/jdb
%{_bindir}/native2ascii
%{_bindir}/rmic
%{_bindir}/serialver
%dir %attr (0755, root, bin) %{_prefix}/jdk
%dir %attr (0755, root, bin) %{_prefix}/jdk/instances
%dir %attr (0755, root, bin) %{_prefix}/jdk/instances/%{jdk_dir}
%{_prefix}/jdk/instances/%{jdk_dir}/LICENSE
%{_prefix}/jdk/instances/%{jdk_dir}/README.html
%{_prefix}/jdk/instances/%{jdk_dir}/THIRDPARTYLICENSEREADME.txt
%{_prefix}/jdk/instances/%{jdk_dir}/src.zip
%dir %attr (0755, root, bin) %{_prefix}/jdk/instances/%{jdk_dir}/bin
%{_prefix}/jdk/instances/%{jdk_dir}/bin/HtmlConverter
%{_prefix}/jdk/instances/%{jdk_dir}/bin/appletviewer
%{_prefix}/jdk/instances/%{jdk_dir}/bin/apt
%{_prefix}/jdk/instances/%{jdk_dir}/bin/extcheck
%{_prefix}/jdk/instances/%{jdk_dir}/bin/idlj
%{_prefix}/jdk/instances/%{jdk_dir}/bin/jar
%{_prefix}/jdk/instances/%{jdk_dir}/bin/jarsigner
%{_prefix}/jdk/instances/%{jdk_dir}/bin/java-rmi.cgi
%{_prefix}/jdk/instances/%{jdk_dir}/bin/javac
%{_prefix}/jdk/instances/%{jdk_dir}/bin/javadoc
%{_prefix}/jdk/instances/%{jdk_dir}/bin/javah
%{_prefix}/jdk/instances/%{jdk_dir}/bin/javap
%{_prefix}/jdk/instances/%{jdk_dir}/bin/jconsole
%{_prefix}/jdk/instances/%{jdk_dir}/bin/jdb
%{_prefix}/jdk/instances/%{jdk_dir}/bin/jinfo
%{_prefix}/jdk/instances/%{jdk_dir}/bin/jmap
%{_prefix}/jdk/instances/%{jdk_dir}/bin/jps
%{_prefix}/jdk/instances/%{jdk_dir}/bin/jsadebugd
%{_prefix}/jdk/instances/%{jdk_dir}/bin/jstack
%{_prefix}/jdk/instances/%{jdk_dir}/bin/jstat
%{_prefix}/jdk/instances/%{jdk_dir}/bin/jstatd
%{_prefix}/jdk/instances/%{jdk_dir}/bin/native2ascii
%{_prefix}/jdk/instances/%{jdk_dir}/bin/rmic
%{_prefix}/jdk/instances/%{jdk_dir}/bin/serialver
%dir %attr (0755, root, bin) %{_prefix}/jdk/instances/%{jdk_dir}/include
%{_prefix}/jdk/instances/%{jdk_dir}/include/*
%dir %attr (0755, root, bin) %{_prefix}/jdk/instances/%{jdk_dir}/lib
%{_prefix}/jdk/instances/%{jdk_dir}/lib/*

%files -n SUNWj5rt -f rt_list.txt
%defattr (-, root, bin)
%{_prefix}/java
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/ControlPanel
%{_bindir}/java
%{_bindir}/keytool
%{_bindir}/orbd
%{_bindir}/policytool
%{_bindir}/rmid
%{_bindir}/rmiregistry
%{_bindir}/servertool
%{_bindir}/tnameserv
%dir %attr (0755, root, bin) %{_prefix}/jdk
%dir %attr (0755, root, bin) %{_prefix}/jdk/instances
%{_prefix}/jdk/instances/latest
%dir %attr (0755, root, bin) %{_prefix}/jdk/instances/%{jdk_dir}
%{_prefix}/jdk/instances/%{jdk_dir}/COPYRIGHT
%dir %attr (0755, root, bin) %{_prefix}/jdk/instances/%{jdk_dir}/bin
%{_prefix}/jdk/instances/%{jdk_dir}/bin/ControlPanel
%{_prefix}/jdk/instances/%{jdk_dir}/bin/java
%{_prefix}/jdk/instances/%{jdk_dir}/bin/javaws
%{_prefix}/jdk/instances/%{jdk_dir}/bin/keytool
%{_prefix}/jdk/instances/%{jdk_dir}/bin/orbd
%{_prefix}/jdk/instances/%{jdk_dir}/bin/pack200
%{_prefix}/jdk/instances/%{jdk_dir}/bin/policytool
%{_prefix}/jdk/instances/%{jdk_dir}/bin/rmid
%{_prefix}/jdk/instances/%{jdk_dir}/bin/rmiregistry
%{_prefix}/jdk/instances/%{jdk_dir}/bin/servertool
%{_prefix}/jdk/instances/%{jdk_dir}/bin/tnameserv
%{_prefix}/jdk/instances/%{jdk_dir}/bin/unpack200
%dir %attr (0755, root, bin) %{_prefix}/jdk/instances/%{jdk_dir}/jre
%dir %attr (0755, root, bin) %{_prefix}/jdk/instances/%{jdk_dir}/jre/bin
%dir %attr (0755, root, bin) %{_prefix}/jdk/instances/%{jdk_dir}/jre/lib
%dir %attr (0755, root, bin) %{_prefix}/jdk/instances/%{jdk_dir}/jre/lib/applet

%files -n SUNWj5dmo
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}/jdk
%dir %attr (0755, root, bin) %{_prefix}/jdk/instances
%dir %attr (0755, root, bin) %{_prefix}/jdk/instances/%{jdk_dir}
%dir %attr (0755, root, bin) %{_prefix}/jdk/instances/%{jdk_dir}/demo
%{_prefix}/jdk/instances/%{jdk_dir}/demo/*
%dir %attr (0755, root, bin) %{_prefix}/jdk/instances/%{jdk_dir}/sample
%{_prefix}/jdk/instances/%{jdk_dir}/sample/*

%files -n SUNWj5man
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}/jdk
%dir %attr (0755, root, bin) %{_prefix}/jdk/instances
%dir %attr (0755, root, bin) %{_prefix}/jdk/instances/%{jdk_dir}
%dir %attr (0755, root, bin) %{_prefix}/jdk/instances/%{jdk_dir}/man
%{_prefix}/jdk/instances/%{jdk_dir}/man/*

%files -n SUNWj5rtx
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}/jdk
%dir %attr (0755, root, bin) %{_prefix}/jdk/instances
%dir %attr (0755, root, bin) %{_prefix}/jdk/instances/%{jdk_dir}
%dir %attr (0755, root, bin) %{_prefix}/jdk/instances/%{jdk_dir}/bin
%dir %attr (0755, root, bin) %{_prefix}/jdk/instances/%{jdk_dir}/bin/amd64
%{_prefix}/jdk/instances/%{jdk_dir}/bin/amd64/java
%{_prefix}/jdk/instances/%{jdk_dir}/bin/amd64/keytool
%{_prefix}/jdk/instances/%{jdk_dir}/bin/amd64/orbd
%{_prefix}/jdk/instances/%{jdk_dir}/bin/amd64/pack200
%{_prefix}/jdk/instances/%{jdk_dir}/bin/amd64/policytool
%{_prefix}/jdk/instances/%{jdk_dir}/bin/amd64/rmid
%{_prefix}/jdk/instances/%{jdk_dir}/bin/amd64/rmiregistry
%{_prefix}/jdk/instances/%{jdk_dir}/bin/amd64/servertool
%{_prefix}/jdk/instances/%{jdk_dir}/bin/amd64/tnameserv
%{_prefix}/jdk/instances/%{jdk_dir}/bin/amd64/unpack200
%dir %attr (0755, root, bin) %{_prefix}/jdk/instances/%{jdk_dir}/jre
%dir %attr (0755, root, bin) %{_prefix}/jdk/instances/%{jdk_dir}/jre/bin
%dir %attr (0755, root, bin) %{_prefix}/jdk/instances/%{jdk_dir}/jre/bin/amd64
%{_prefix}/jdk/instances/%{jdk_dir}/jre/bin/amd64/*
%dir %attr (0755, root, bin) %{_prefix}/jdk/instances/%{jdk_dir}/jre/lib
%dir %attr (0755, root, bin) %{_prefix}/jdk/instances/%{jdk_dir}/jre/lib/amd64
%{_prefix}/jdk/instances/%{jdk_dir}/jre/lib/amd64/*

%files -n SUNWj5dvx
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}/jdk
%dir %attr (0755, root, bin) %{_prefix}/jdk/instances
%dir %attr (0755, root, bin) %{_prefix}/jdk/instances/%{jdk_dir}
%dir %attr (0755, root, bin) %{_prefix}/jdk/instances/%{jdk_dir}/bin
%{_prefix}/jdk/instances/%{jdk_dir}/bin/amd64/appletviewer
%{_prefix}/jdk/instances/%{jdk_dir}/bin/amd64/apt
%{_prefix}/jdk/instances/%{jdk_dir}/bin/amd64/extcheck
%{_prefix}/jdk/instances/%{jdk_dir}/bin/amd64/idlj
%{_prefix}/jdk/instances/%{jdk_dir}/bin/amd64/jar
%{_prefix}/jdk/instances/%{jdk_dir}/bin/amd64/jarsigner
%{_prefix}/jdk/instances/%{jdk_dir}/bin/amd64/javac
%{_prefix}/jdk/instances/%{jdk_dir}/bin/amd64/javadoc
%{_prefix}/jdk/instances/%{jdk_dir}/bin/amd64/javah
%{_prefix}/jdk/instances/%{jdk_dir}/bin/amd64/javap
%{_prefix}/jdk/instances/%{jdk_dir}/bin/amd64/jconsole
%{_prefix}/jdk/instances/%{jdk_dir}/bin/amd64/jdb
%{_prefix}/jdk/instances/%{jdk_dir}/bin/amd64/jinfo
%{_prefix}/jdk/instances/%{jdk_dir}/bin/amd64/jmap
%{_prefix}/jdk/instances/%{jdk_dir}/bin/amd64/jps
%{_prefix}/jdk/instances/%{jdk_dir}/bin/amd64/jsadebugd
%{_prefix}/jdk/instances/%{jdk_dir}/bin/amd64/jstack
%{_prefix}/jdk/instances/%{jdk_dir}/bin/amd64/jstat
%{_prefix}/jdk/instances/%{jdk_dir}/bin/amd64/jstatd
%{_prefix}/jdk/instances/%{jdk_dir}/bin/amd64/native2ascii
%{_prefix}/jdk/instances/%{jdk_dir}/bin/amd64/rmic
%{_prefix}/jdk/instances/%{jdk_dir}/bin/amd64/serialver

#%files -n SUNWj5dmx

%changelog
* Wed Feb 20 2008 - moinak.ghosh@sun.com
- Initial spec.
