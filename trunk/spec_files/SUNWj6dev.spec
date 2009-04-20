#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define vers         1.6.0
%define bld          13

Name:                SUNWj6dev
Version:             %{vers}_%{bld}
%define jdk_dir jdk%{version}
%define archive_version 6u%{bld}
%define derby_version 10.4.1.3
Summary:             JDK 6.0 Development Tools (%{version})
Source:              http://download.java.net/dlj/binaries/jdk-%{archive_version}-dlj-solaris-i586.sh
Source1:             http://download.java.net/dlj/binaries/jdk-%{archive_version}-dlj-solaris-amd64.sh

URL:                 https://jdk-distros.dev.java.net/
SUNW_BaseDir:        /
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:            SUNWj6rt

%package -n SUNWj6rt
Summary:             JDK 6.0 Runtime Environment (%{version})
SUNW_BaseDir:        /
%include default-depend.inc
Requires:            SFEopenmotif
Requires:            SUNWlibC
Requires:            FSWxwrtl
Requires:            FSWxorg-clientlibs
Requires:            SUNWxwplr
Requires:            SUNWxwxft
Requires:            SUNWfontconfig

%post -n SUNWj6rt
do_update=0
if [ -n "$SUNW_PKG_INSTALL_ZONENAME" -a \
    "$SUNW_PKG_INSTALL_ZONENAME" == "global" ]; then
	do_update=1
fi

if [ -z "$SUNW_PKG_INSTALL_ZONENAME" ]; then
	do_update=1
fi

if [ $do_update -eq 1 ]; then
	(cd ${BASEDIR}%{_bindir}
	for prg in ControlPanel java keytool orbd policytool rmid \
	    rmiregistry servertool tnameserv
	do
		ln -sf ../java/jre/bin/$prg
	done
	cd ..
	rm -f java
	ln -s jdk/instances/%{jdk_dir} java)

	(cd ${BASEDIR}%{_prefix}/jdk/instances
	rm -f latest
	ln -sf %{jdk_dir} latest
        ln -sf %{jdk_dir} %{vers})

fi

%postun -n SUNWj6rt
do_update=0
if [ -n "$SUNW_PKG_INSTALL_ZONENAME" -a \
    "$SUNW_PKG_INSTALL_ZONENAME" == "global" ]; then
	do_update=1
fi

if [ -z "$SUNW_PKG_INSTALL_ZONENAME" ]; then
	do_update=1
fi

if [ $do_update -eq 1 ]; then
	(cd ${BASEDIR}%{_prefix}
	rm java
	for nm in `ls -tr jdk/instances`
	do
		if [ -d jdk/instances/${nm} ]
		then
			ln -sf jdk/instances/${nm} java
			cd jdk/instances
			rm -f latest
			ln -sf ${nm} latest
			break
		fi
	done)
fi

%package -n SUNWj6dmo
Summary:             JDK 6.0 Demo Programs (%{version})
SUNW_BaseDir:        /
%include default-depend.inc
Requires:            SUNWj6rt

%package -n SUNWj6man
Summary:             JDK 6.0 Man Pages (%{version})
SUNW_BaseDir:        /
%include default-depend.inc
Requires:            SUNWj6rt

%package -n SUNWj6rtx
Summary:             JDK 6.0 64-Bit Runtime Environment (%{version})
SUNW_BaseDir:        /
%include default-depend.inc
Requires:            SUNWj6rt

%package -n SUNWj6dvx
Summary:             JDK 6.0 64-Bit Development Tools (%{version})
SUNW_BaseDir:        /
%include default-depend.inc
Requires:            SUNWj6dev
Requires:            SUNWj6rtx

%package -n SUNWjavadb
Summary:             Apache Derby Java Database
SUNW_BaseDir:        /opt
Version:             10.4.1.3
%include default-depend.inc
Requires:            SUNWj6rt

#%package -n SUNWj6dmx
#Summary:             JDK 6.0 64-Bit Demo Programs (%{version})
#SUNW_BaseDir:        /
#%include default-depend.inc
#Requires:            SUNWj6rtx

%post
do_update=0
if [ -n "$SUNW_PKG_INSTALL_ZONENAME" -a \
    "$SUNW_PKG_INSTALL_ZONENAME" == "global" ]; then
	do_update=1
fi

if [ -z "$SUNW_PKG_INSTALL_ZONENAME" ]; then
	do_update=1
fi

if [ $do_update -eq 1 ]; then
	(cd ${BASEDIR}%{_bindir}
	for prg in HtmlConverter appletviewer apt extcheck idlj jar \
	    jarsigner javac javadoc javah javap jdb native2ascii \
	    rmic serialver
	do
		ln -sf ../java/bin/$prg
	done)
fi

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

tar cpf - * | (cd ${RPM_BUILD_ROOT}%{_prefix}/jdk/instances; tar xpf - )

(cd ${RPM_BUILD_ROOT}
    find ./%{_prefix}/jdk/instances/%{jdk_dir}/jre \( -type f -o -type l \) | \
    grep -v amd64 | sed 's/^\.//') > rt_list.txt

mkdir ${RPM_BUILD_ROOT}/opt
mv ${RPM_BUILD_ROOT}%{_prefix}/jdk/instances/%{jdk_dir}/db ${RPM_BUILD_ROOT}/opt/SUNWjavadb
chmod 0755 ${RPM_BUILD_ROOT}%{_prefix}/jdk/instances/%{jdk_dir}/jre/lib/ext

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_bindir}
%dir %attr (0755, root, bin) %{_prefix}/jdk
%dir %attr (0755, root, bin) %{_prefix}/jdk/instances
%dir %attr (0755, root, bin) %{_prefix}/jdk/instances/%{jdk_dir}
%{_prefix}/jdk/instances/%{jdk_dir}/LICENSE
%{_prefix}/jdk/instances/%{jdk_dir}/README.html
%{_prefix}/jdk/instances/%{jdk_dir}/README_ja.html
%{_prefix}/jdk/instances/%{jdk_dir}/README_zh_CN.html
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
%{_prefix}/jdk/instances/%{jdk_dir}/bin/jvisualvm
%{_prefix}/jdk/instances/%{jdk_dir}/bin/xjc
%{_prefix}/jdk/instances/%{jdk_dir}/bin/wsgen
%{_prefix}/jdk/instances/%{jdk_dir}/bin/wsimport
%{_prefix}/jdk/instances/%{jdk_dir}/bin/jhat
%{_prefix}/jdk/instances/%{jdk_dir}/bin/jcontrol
%{_prefix}/jdk/instances/%{jdk_dir}/bin/schemagen
%{_prefix}/jdk/instances/%{jdk_dir}/bin/jrunscript
%dir %attr (0755, root, bin) %{_prefix}/jdk/instances/%{jdk_dir}/include
%{_prefix}/jdk/instances/%{jdk_dir}/include/*
%dir %attr (0755, root, bin) %{_prefix}/jdk/instances/%{jdk_dir}/lib
%{_prefix}/jdk/instances/%{jdk_dir}/lib/*

%files -n SUNWj6rt -f rt_list.txt
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_bindir}
%dir %attr (0755, root, bin) %{_prefix}/jdk
%dir %attr (0755, root, bin) %{_prefix}/jdk/instances
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

%files -n SUNWj6dmo
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_prefix}/jdk
%dir %attr (0755, root, bin) %{_prefix}/jdk/instances
%dir %attr (0755, root, bin) %{_prefix}/jdk/instances/%{jdk_dir}
%dir %attr (0755, root, bin) %{_prefix}/jdk/instances/%{jdk_dir}/demo
%{_prefix}/jdk/instances/%{jdk_dir}/demo/*
%dir %attr (0755, root, bin) %{_prefix}/jdk/instances/%{jdk_dir}/sample
%{_prefix}/jdk/instances/%{jdk_dir}/sample/*

%files -n SUNWj6man
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_prefix}/jdk
%dir %attr (0755, root, bin) %{_prefix}/jdk/instances
%dir %attr (0755, root, bin) %{_prefix}/jdk/instances/%{jdk_dir}
%dir %attr (0755, root, bin) %{_prefix}/jdk/instances/%{jdk_dir}/man
%{_prefix}/jdk/instances/%{jdk_dir}/man/*

%files -n SUNWj6rtx
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
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

%files -n SUNWj6dvx
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
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
%{_prefix}/jdk/instances/%{jdk_dir}/bin/amd64/wsimport
%{_prefix}/jdk/instances/%{jdk_dir}/bin/amd64/jhat
%{_prefix}/jdk/instances/%{jdk_dir}/bin/amd64/wsgen
%{_prefix}/jdk/instances/%{jdk_dir}/bin/amd64/jrunscript
%{_prefix}/jdk/instances/%{jdk_dir}/bin/amd64/schemagen
%{_prefix}/jdk/instances/%{jdk_dir}/bin/amd64/xjc

%files -n SUNWjavadb
%defattr (1, root, sys)
/opt/*

#%files -n SUNWj6dmx

%changelog
* Sat Apr 18 2009 - moinakg@belenix.org
- Bump to latest version and fix permission of a dir.
* Sat Dec 06 2008 - moinakg@belenix.org
- Initial spec.
