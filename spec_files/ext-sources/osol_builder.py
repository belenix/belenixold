#!/usr/bin/python
#
#    Automated ON builder
#    Copyright (C) 2008  The BeleniX team
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#    Author: Moinak Ghosh
#

import sys
import os
import shutil
import getopt
import gettext
import string
import tarfile
import time
import traceback
import platform
from subprocess import Popen, PIPE, STDOUT


class BLDError(Exception):
	"""
	Build errors.
	"""
	def __init__(self, message):
		self.message = message

	def __str__(self):
		return repr(self.message)

class Workspace(object):
	"""
	This is the main workspace instance that validates directories, patches and flags and builds.
	"""

	def __init__(self, basedir, distroname, arch, incremental):
		self.basedir = basedir
		self.distroname = distroname
		self.arch = arch
		self.downloads = os.path.join(basedir, "downloads")
		self.patches = os.path.join(basedir, "patches")
		self.on_patches = os.path.join(self.patches, "on_patches")
		self.xvm_patches = os.path.join(self.patches, "xvm_patches")
		self.nightly_options = os.path.join(self.patches, "nightly.options")
		self.on_src = os.path.join(self.downloads, "on-src.tar.bz2")
		self.on_closed_bins = os.path.join(self.downloads, "on-closed-bins-nd." + arch + ".tar.bz2")
		self.xvm_src = os.path.join(self.downloads, "xvm-src.tar.bz2")
		self.sunwonbld_pkg = os.path.join(self.downloads, "SUNWonbld." + arch + ".tar.bz2")
		self.on_ws = os.path.join(self.basedir, "on_ws")
		self.xvm_ws = os.path.join(self.basedir, "xvm_ws")
		self.env_file = os.path.join(self.on_ws, "opensolaris.sh")
		self.incremental = incremental
		self.nightly_attrs = []
		self.patchdir = "/var/osol_builder/ON_patches"

	def check(self):
		print "*** Checking workspace\n"
		if not os.path.isdir(self.basedir):
			raise BLDError(_(self.basedir + " directory not found"))
		if not os.path.isdir(self.downloads):
			raise BLDError(_(self.downloads + " directory not found"))
		if not os.path.isdir(self.patches):
			raise BLDError(_(self.patches + " directory not found"))
		if not os.path.isfile(self.on_src):
			raise BLDError(_(self.on_src + " not found"))
		if not os.path.isfile(self.on_closed_bins):
			raise BLDError(_(self.on_closed_bins + " not found"))
		if not os.path.isfile(self.xvm_src):
			raise BLDError(_(self.xvm_src + " not found"))
		if not os.path.isfile(self.sunwonbld_pkg):
			raise BLDError(_(self.sunwonbld_pkg + " not found"))
		if not os.path.isfile("/opt/SUNWspro/bin/cc"):
			raise BLDError(_("/opt/SUNWspro/bin/cc not found."))

		#
		# Load attributes for replacing in the nightly environment file
		#
		if os.path.isfile(self.nightly_options):
			nf = open(self.nightly_options, "r")
			for line in nf:
				if line[0] == "#":
					continue
				nl = line.strip()
				if nl == "":
					continue

				attr = nl.split("=")
				self.nightly_attrs.append(attr)
			nf.close()
		self.nightly_attrs.append(["GATE", "on_ws;	export GATE"])
		self.nightly_attrs.append(["CODEMGR_WS", \
		    self.on_ws + ";	export CODEMGR_WS"])
		self.nightly_attrs.append(["VERSION", \
		    self.distroname + ";	export VERSION"])


	def extract_tar(self, fname, tdir):
		"""
		Extract all members from the given tarfile into the given directory. The
		tarfile can be gzip or bzip2 compressed.
		This is not needed in Python 2.5 due to extractall api.
		"""

		count = 1
		tarf = tarfile.open(fname, "r")
		member = tarf.next()
		while member:
			tarf.extract(member, tdir)
			member = tarf.next()
			if count % 200 == 0:
				sys.stdout.write(".")
				sys.stdout.flush()
			count += 1
		tarf.close()
		print " "

	def write_admin(self):
		adminf = open(os.path.join(self.basedir, "admin"), "w")
		print >> adminf, """\
mail=
instance=overwrite
partial=nocheck
runlevel=nocheck
idepend=nocheck
rdepend=nocheck
space=nocheck
setuid=nocheck
conflict=nocheck
action=nocheck
basedir=default"""
		adminf.close()

	def write_hgrc(self):
		"""
		Generate a hgrc file needed to successfully update XVM source
		"""

		hgrc = os.path.join(os.environ["HOME"], ".hgrc")
		hgrco = os.path.join(os.environ["HOME"], ".hgrc.orig")
		if os.path.exists(hgrc) and not os.path.exists(hgrco):
			shutil.copyfile(hgrc, hgrco)
		hgf = open(hgrc, "w")
		print >> hgf, """\
[extensions]
hgext.mq=
hgext.cdm=/opt/onbld/lib/python/onbld/hgext/cdm.py
[diff]
git=True
[trusted]
groups = staff user
[cdm-hooks]
precommitchk=False
[ui]
merge=/opt/onbld/bin/hgmerge"""
		hgf.close()

	def fixup_tools(self):
		#
		# Create /opt/onnv-tools since XVM makefiles have some hardcoding
		#
		if not os.path.isdir("/opt/onnv-tools"):
			os.mkdir("/opt/onnv-tools")
		if not os.path.islink("/opt/onnv-tools/SUNWspro"):
			os.symlink("../SUNWspro", "SUNWspro")
		if not os.path.islink("/opt/onnv-tools/onbld"):
			os.symlink("../onbld", "onbld")

	def replace_keys(self, fname, attrs):
		#
		# Replace env vars from attrs list in the given file
		#
		flst = []
		ef = open(fname, "r")
		for line in ef:
			if line.find("=") > -1:
				kv = line.split("=")
				for attr in attrs:
					if kv[0] == attr[0]:
						kv[1] = attr[1] + "\n"
				nl = "=".join(kv)
				flst.append(nl)
			else:
				flst.append(line)
		ef.close()
		ef = open(fname, "w")
		for line in flst:
			ef.write(line)
		ef.close()

	def patch_on(self, src_present):
		"""
		Apply patches if any to ON source.
		"""

		if self.incremental and src_present:
			if os.path.isfile(self.env_file):
				return

		#
		# First modify env file
		#
		shutil.copyfile(self.on_ws + "/usr/src/tools/env/opensolaris.sh", self.env_file)
		self.replace_keys(self.env_file, self.nightly_attrs)

		#
		# Now enable ksh93switch
		#
		ksh93_attr = (["ON_BUILD_KSH93_AS_BINKSH", "1"])
		self.replace_keys(self.on_ws + "/usr/src/Makefile.ksh93switch", ksh93_attr)

		#
		# Copy must-needed patches and the nightly options file
		#
		if not os.path.isdir(self.on_patches):
			os.makedirs(self.on_patches)
		shutil.copyfile(os.path.join(self.patchdir, "Makefiles.diff"), \
		    os.path.join(self.on_patches, "Makefiles.diff"))
		shutil.copyfile(os.path.join(self.patchdir, "nightly.options"), \
		    os.path.join(self.patches, "nightly.options"))

		pwd = os.getcwd()
		os.chdir(self.on_ws)
		patches = os.listdir(self.on_patches)
		patches.sort()
		for patch in patches:
			if patch.endswith(".script"):
				#
				# This is a patch script, execute it giving the ON workspace
				# directory as the argument.
				#
				cmd = "sh %s %s" % (os.path.join(self.on_patches, patch), self.on_ws)
				pipe = Popen(cmd, shell=True, stdout=None, stderr=None, close_fds=False)
				rt = pipe.wait()
				if rt != 0:
					raise BLDError("%s failed." % cmd)
				continue

			cmd = "cat %s | gpatch --fuzz=0 -p0" % os.path.join(self.on_patches, patch)
			pipe = Popen(cmd, shell=True, stdout=None, stderr=None, close_fds=False)
			rt = pipe.wait()
			if rt != 0:
				raise BLDError("%s failed." % cmd)
		os.chdir(pwd)

	def patch_xvm(self):
		"""
		Apply additional XVM patches if any and create /opt/onnv-tools
		"""

		pwd = os.getcwd()
		os.chdir(self.xvm_ws)
		print "*** Fixing up some XVM proto directories "
		os.makedirs("proto/staging/include")
		shutil.copytree("xen.hg/xen/include/public", "proto/staging/include/xen")

		if not os.path.isdir(self.xvm_patches):
			os.chdir(pwd)
			return

		for patch in os.listdir(self.xvm_patches).sort():
			cmd = "gpatch --fuzz=0 -p0 %s" % patch
			pipe = Popen(cmd, shell=True, stdout=None, stderr=None, close_fds=False)
			rt = pipe.wait()
			if rt != 0:
				raise BLDError("%s failed." % cmd)
		os.chdir(pwd)

	def prepare(self):
		"""
		Prepare the workspace to make it ready for a build. All patches are applied here.
		"""

		if not os.path.exists(os.path.join(self.patchdir, "Makefiles.diff")):
			raise BLDError("Must-needed patches not found. Please run osol_builder prereq.")

		#
		# Extract ON source
		#
		isonsrc = True
		if not os.path.exists(self.on_ws):
			os.mkdir(self.on_ws)
			isonsrc = False
		else:
			if not self.incremental:
				print "*** [" + str(time.time()) + \
				    "]: Cleaning up  " + self.on_ws + "\n"
				shutil.rmtree(self.on_ws)
				os.mkdir(self.on_ws)

		if not self.incremental or not isonsrc:
			print "*** [" + str(time.time()) + \
			    "]: Extracting ON source into " + self.on_ws + "\n"
			self.extract_tar(self.on_src, self.on_ws)
			self.extract_tar(self.on_closed_bins, self.on_ws)
			print "*** [" + str(time.time()) + "]: Done extracting ON source. \n"

		#
		# Extract XVM source
		#
		isxvmsrc = True
		if not os.path.exists(self.xvm_ws):
			os.mkdir(self.xvm_ws)
			isxvmsrc = False
		else:
			if not self.incremental:
				print "*** [" + str(time.time()) + \
				    "]: Cleaning up  " + self.xvm_ws + "\n"
				shutil.rmtree(self.xvm_ws)
				os.mkdir(self.xvm_ws)

		if not self.incremental or not isxvmsrc:
			count = 1
			print "*** [" + str(time.time()) + \
			    "]: Extracting XVM source into " + self.xvm_ws + "\n"
			self.extract_tar(self.xvm_src, self.xvm_ws)
			print "*** [" + str(time.time()) + "]: Done extracting XVM source. \n"
	
		#
		# Extract and install SUNWonbld
		#
		self.write_admin()
		isonbld = True
		if not os.path.isdir("/var/sadm/pkg/SUNWonbld") or not self.incremental:
			if os.path.isdir("/var/sadm/pkg/SUNWonbld") and not self.incremental:
				print "*** Removing existing copy of SUNWonbld"
				cmd = "/usr/sbin/pkgrm -n -a %s SUNWonbld" % \
				    os.path.join(self.basedir, "admin")
				pipe = Popen(cmd, shell=True, stdout=None, stderr=None, close_fds=False)
				rt = pipe.wait()
				if rt != 0:
					raise BLDError("pkgrm of SUNWonbld failed.")
			elif self.incremental:
				isonbld = False

			if isonbld:
				print "*** Installing SUNWonbld"
				self.extract_tar(self.sunwonbld_pkg, self.basedir)
				cmd = "/usr/sbin/pkgadd -n -a %s -d %s all" % \
				    (os.path.join(self.basedir, "admin"), \
				    os.path.join(self.basedir, "onbld"))
				pipe = Popen(cmd, shell=True, stdout=None, stderr=None, close_fds=False)
				rt = pipe.wait()
				if rt != 0:
					raise BLDError("pkgadd of SUNWonbld failed.")

		#
		# Apply ON patches
		#
		print "*** Applying ON patches ..."
		self.patch_on(isonsrc)

		#
		# Some environmental setup
		#
		self.write_hgrc()
		self.fixup_tools()

		#
		# Prepare XVM dir
		#
		print "*** Preparing XVM source ..."
		pwd = os.getcwd()
		os.chdir(self.xvm_ws)
		cmd = 'ws xen.hg -c "hg qpush -a"'
		pipe = Popen(cmd, shell=True, stdout=None, stderr=None, close_fds=False)
		rt = pipe.wait()
		if rt != 0:
			raise BLDError(cmd + " failed.")
		os.chdir(pwd)

		print "*** Patching XVM source ..."
		self.patch_xvm()

	def do_build(self):
		"""
		Run all the builds with fingers crossed!
		"""

		#
		# First run ON build
		#
		pwd = os.getcwd()
		os.chdir(self.on_ws)

		if self.incremental:
			print "*** Running nightly ON incremental build"
			cmd = "nightly -i ./opensolaris.sh"
		else:
			print "*** Running nightly ON full build"
			cmd = "nightly ./opensolaris.sh"
		pipe = Popen(cmd, shell=True, stdout=None, stderr=None, close_fds=False)
		rt = pipe.wait()
		if rt != 0:
			raise BLDError("ON nightly build failed.")

		#
		# Now massage ON pkgdefs
		#
		self.process_pkgdefs()
		os.chdir(self.on_ws)

		#
		# We want ksh93 for /sbin/sh
		#
		proto = os.path.join(self.on_ws, "proto/root_" + self.arch)
		sbin_sh = os.path.join(proto, "sbin/sh")
		ksh93 = os.path.join(proto, "usr/bin/i86/ksh93")
		shutil.copyfile(ksh93, sbin_sh)

		#
		# Now replace some files in the proto dir for a properly functional distro
		#
		proto_replace = os.path.join(self.patchdir, "proto_replace")
		if os.path.isdir(proto_replace):
			lf = open(os.path.join(proto_replace, "proto_replace.files"), "r")
			for line in lf:
				print line
				path = line.strip()
				src_path = os.path.join(proto_replace, path)
				proto_path = os.path.join(proto, path)
				shutil.copyfile(src_path, proto_path)
			lf.close()

		#
		# Build ON packages
		#
		cmd = "bldenv ./opensolaris.sh 'cd usr/src/pkgdefs; make install'"
		pipe = Popen(cmd, shell=True, stdout=None, stderr=None, close_fds=False)
		rt = pipe.wait()
		if rt != 0:
			raise BLDError("ON package build failed.")
		os.chdir(pwd)

		#
		# Run XVM build
		#
		print "*** Running XVM build ..."
		os.chdir(self.xvm_ws)
		cmd = "EMAIL=nobody@localhost; export EMAIL;"
		cmd += " XVM_WS=%s; export XVM_WS;" % self.xvm_ws
		cmd += " EDITOR=/usr/bin/vi; export EDITOR;"
		cmd += ' ws sunos.hg -c "./bin/build-all nondebug"'
		pipe = Popen(cmd, shell=True, stdout=None, stderr=None, close_fds=False)
		rt = pipe.wait()
		if rt != 0:
			raise BLDError("XVM build failed")

	def process_pkgdefs(self):
		"""
		Massage the SVR4 package definitions in an OpenSolaris workspace to allow
		packages to be built successfully. This is needed since the pkgdefs reference
		closed non-redistributable objects only available inside SUN's firewall.
		These references need to be removed from the prototype files so that
		OpenSolaris packages can be built. In some cases entire packages are left
		out.
		"""

		pkgd_flag = os.path.join(self.on_ws, ".pkgdefs_processed")
		if self.incremental and os.path.exists(pkgd_flag):
			return

		print "*** Processing ON package definitions ..."
		omits = []
		arch = self.arch
		wksp = self.on_ws
		dr = os.path.join(wksp, "usr/src/pkgdefs")
		if not os.path.isdir(dr):
			raise BLDError("ERROR: " + wksp + " is not a valid OpenSolaris workspace.")

		proto = os.path.join(wksp, "proto/root_" + arch)
		if not os.path.isdir(proto):
			raise BLDError("ERROR: The OpenSolaris workspace appears not to be built.")
		
		#
		# This weird looking entry needs to be left untouched!
		#
		ign_list = ["usr/lib/font/devpost/charlib/~=usr/lib/font/devpost/charlib/~="]
		
		omitsf = open("omitted_paths.txt", "w")
		omitsp = open("omitted_pkgs.txt", "w")
		
		for sd in os.listdir(dr):
			if len(sd) < 4 or \
			    (sd[:4] != "BRCM" and sd[:3] != "PHX" and sd[:4] != "SUNW"):
				continue
		
			pkgdir = os.path.join(dr, sd)
			pkginfo = os.path.join(pkgdir, "pkginfo")
			if not os.path.exists(pkginfo): continue
		
			paths = 0
			dpaths = 0
			dir_only = True
			nexist = []
			noproto = 0
		
			# Fetch the BASEDIR (/ is default)
			basedir = ""
			pkginf = open(pkginfo, "r")
			for line in pkginf:
				line = line.strip()
				if line[:4] == "BASE":
					key, val = line.split("=")
					basedir = val
			pkginf.close()
		
			proto_com = os.path.join(pkgdir, "prototype_com")
			proto_arch = os.path.join(pkgdir, "prototype_" + arch)
		
			if basedir == "/":
				basedir = ""
			elif basedir[:1] == "/":
				basedir = basedir[1:]
		
			for protofile in (proto_com, proto_arch):
				if not os.path.exists(protofile):
					noproto += 1
					continue
				protoorig = protofile + ".orig"
				if not os.path.exists(protoorig):
					shutil.copyfile(protofile, protoorig)
		
				pf = open(protoorig, "r")
				pfo = open(protofile, "w")
				for line in pf:
					ln = line.strip()
					if ln == "":
						pfo.write(line)
						continue
		
					pentry = ln.split()
					if len(pentry) >= 3 and pentry[2] in ign_list:
						pfo.write(line)
						continue
		
					if pentry[0] == 'f' or pentry[0] == 'e' or \
					    pentry[0] == 'v':
						#
						# If it is a file, check if it exists in the proto.
						# Alternatively it can be file pulled in via a given
						# path. Check for that as well.
						# However device entries are preserved as is.
						#
						dfile="__junk__"
						dl = pentry[2].split("=")
						if len(dl) > 1:
							if dl[1][:2] == "..":
								dfile = os.path.normpath(\
								    os.path.join(proto, dl[1]))
							else:
								dfile = os.path.normpath(\
								    os.path.join(proto, basedir,
								    dl[1]))
						pfile = os.path.normpath(os.path.join(proto, \
						    basedir, pentry[2]))
						if os.path.exists(pfile) or \
						   os.path.exists(dfile) or \
						    (len(pentry[2]) > 3 and pentry[2][:3] == "dev"):
							pfo.write(line)
							paths += 1
						else:
							print >> omitsf, "Omitting: " + ln
							nexist.append(pentry[2])
						dir_only = False
		
					elif pentry[0] == 's':
						#
						# If it is a symlink check if the link target was
						# omitted earlier or not preset in proto.
						# However device links are preserved as is.
						#
						src, tgt = pentry[2].split("=")
						srcdir = os.path.dirname(src)
						tgtf = os.path.normpath(\
						    os.path.join(proto, srcdir, tgt))
						if tgtf not in nexist:
							if os.path.exists(tgtf) or \
							    (len(pentry[2]) > 3 and \
							    pentry[2][:3] == "dev"):
								pfo.write(line)
								paths += 1
							else:
								print >> omitsf, "Omitting: " + ln
						else:
							print "Omitting: " + ln
						dir_only = False
		
					elif pentry[0] == 'd':
						pfo.write(line)
						dpaths += 1
		
					else:
						pfo.write(line)
				pf.close()
				pfo.close()
		
			if dir_only:
				paths += dpaths
		
			if (paths == 0 and len(nexist) > 0) or noproto == 2:
				print "Omitting pkg " + sd
				print >> omitsp, "Omitting pkg " + sd
				omits.append(sd)
		
		#
		# Check for dependencies and omit packages whose dependencies are
		# not satisfied.
		#
		print "Verifying dependencies ..."
		for sd in os.listdir(dr):
			if sd in omits:
				continue
		
			if len(sd) < 4 or (sd[:4] != "BRCM" and sd[:3] != "PHX" and sd[:4] != "SUNW"):
				continue
		
			pkgdir = os.path.join(dr, sd)
			dependf = os.path.join(pkgdir, "depend")
			if not os.path.exists(dependf):
				continue
		
			df = open(dependf, "r")
			for line in df:
				line = line.strip()
				if line == "": continue
		
				ln = line.split()
				if ln[0] == "P":
					if ln[1] in omits:
						print "Broken dep: " + sd + " -> " + ln[1]
						print "            Omitting " + sd
						print >> omitsp, "Broken dep: " + sd + " -> " + ln[1]
						print >> omitsp, "            Omitting " + sd
						omits.append(sd)
		
			df.close()
		
		omitsf.close()
		omitsp.close()
		
		#
		# Now we have the list of packages to be omitted. Patch the toplevel
		# Makefile to remove those package references.
		#
		mkorig = os.path.join(dr, "Makefile.orig")
		mkfile = os.path.join(dr, "Makefile")
		if not os.path.exists(mkorig):
			shutil.copyfile(mkfile, mkorig)
		
		mknew = os.path.join(dr, "Makefile.new")
		mkfi = open(mkorig, "r")
		mkfo = open(mknew, "w")
		
		for line in mkfi:
			ln = line.strip().split()
			if line == "":
				continue
			skip = False
			for item in ln:
				if item in omits:
					skip = True
					break
			if skip: continue
			mkfo.write(line)
		
		mkfi.close()
		mkfo.close()
		
		shutil.copyfile(mknew, mkfile)
		open(pkgd_flag, "w").close()

def usage():
	"""
	Print usage info.
	"""
	
	print >> sys.stdout, _("""\

osol_builder prereq 
	Check system for presence of prerequsities for building ON. This can automatically
	fetch necessary packages and files except for SUN Studio 12 compiler.

osol_builder build -R <base dir> [-d <distro name tag>] [-i] [-b]
	-R <base dir> - Directory containing downloaded ON and XVM source 
	tarballs and patches.
	Structure of this directory is as follows:
	
	<base dir>/downloads
	<base dir>/patches
	
	<base dir>/on_ws and <base dir>/xvm_ws will be created.

	-d <distro name tag>
	This is the name that will be compiled into the kernel and will be
	printed via uname -v

	-i
	Do an incremental build

	-b
	Just run the build and skip the initial preparation steps. This is useful
	to rerun build full or incremental when the workspace is already properly
	setup.""")


def do_main():
	"""
	Main build controller.
	"""
	gettext.install("spkg", "/usr/lib/locale");

	ret = 0
	use_site = ""
	basedir = ""
	distroname = ""
	incremental = False
	plat = platform.uname()
	arch = plat[5]
	build_only = False

	try:
		opts, pargs = getopt.getopt(sys.argv[1:], "R:d:ib")
	except getopt.GetoptError, e:
		print >> sys.stderr, \
		    _("build_on: illegal global option -- %s") % e.opt
		usage()

	if len(opts) == 0:
		usage()
		sys.exit(1)

	for opt, arg in opts:
		if opt == "-R":
			basedir = arg
		elif opt == "-d":
			distroname = arg
		elif opt == "-i":
			incremental = True
		elif opt == "-b":
			build_only = True

	if basedir == "":
		print >> sys.stderr, \
		    _("osol_builder build: -R <basedir> not specified")
		usage()
		sys.exit(1)
		

	wksp = Workspace(basedir, distroname, arch, incremental)
	if not build_only:
		wksp.check()
		wksp.prepare()
	wksp.do_build()

if __name__ == "__main__":
	try:
		ret = 0
		ret = do_main()
	except SystemExit, e:
		raise e
	except KeyboardInterrupt:
		print "Interrupted"
		sys.exit(1)
	except IOError, ie:
		if ie.errno != 32:
			traceback.print_exc()
	except BLDError, pe:
		print pe.message
		sys.exit(1)
	except:
		traceback.print_exc()
		sys.exit(99)
	sys.exit(ret)


