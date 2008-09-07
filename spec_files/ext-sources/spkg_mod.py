#
#    Advanced SVR4 package and repository management layer
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
import re
import traceback
import gettext
import string
import tsort
import time
from stat import *
from subprocess import *
from urlparse import urlparse
from decimal import *

class Cl_pkgentry(object):
	"""Class that holds all fields of a package entry in the catalog including site related entries."""

	def __init__(self, entry, sitevars):
		self.cname = entry[0]
		self.version = entry[1]
		self.pkgname = entry[2]
		self.pkgfile = entry[3]
		self.md5sum = entry[4]
		self.sitevars = sitevars
		self.refername = ""
		self.deplist = []
		self.action = 0

	def update(self, entry, sitevars):
		self.cname = entry[0]
		self.version = entry[1]
		self.pkgname = entry[2]
		self.pkgfile = entry[3]
		self.md5sum = entry[4]
		self.sitevars = sitevars
		

class Cl_sitevars(object):
	"""Class that holds site - specific variables."""

	def __init__(self, site, RELEASE, RTYPE, SPKG_VAR_DIR):
		so = urlparse(site)
		self.site = site
		self.psite = so
                self.fullurl = "%s/%s/%s" % (site, RELEASE, RTYPE)
                self.catalog = "%s/catalog-%s" % (SPKG_VAR_DIR, so[1])
                self.desc = "%s/desc-%s" % (SPKG_VAR_DIR, so[1])
                self.metadir = "%s/metainfo-%s" % (SPKG_VAR_DIR, so[1])
		self.tcat = "%s/catalog" % SPKG_VAR_DIR
		self.tmeta = "%s/metainfo.tar.7z" % SPKG_VAR_DIR
		self.tmetadir = "%s/metainfo" % SPKG_VAR_DIR
		self.tdesc = "%s/descriptions" % SPKG_VAR_DIR 

		
class Cl_vars(object):
	"""Class that holds some globally used values."""
	def __init__(self):
		self.cnffile = ""
		self.ALTROOT = ""
		self.RTYPE = "unstable"
		self.PKGSITES = ["http://pkg.belenix.org"]
		self.PKGADDFLAGS = ""
		self.SPKG_PRESERVE_DOWNLOADS = False
		self.USE_GPG = True
		self.USE_MD5 = True
		self.WGET = "/usr/sfw/bin/wget"
		self.SZIP = "/usr/bin/7za"
		self.OSREL = "5.11"
		self.CPU = "i386"
		self.SPKG_VAR_DIR = "/var/spkg"
		self.SPKG_DWN_DIR = "/var/spkg/downloads"
		self.RELEASE = "belenix_0.7.1"
		self.PKGSITEVARS = []
		self.INSTPKGDIR = "/var/sadm/pkg"
		self.ADMINFILE = self.SPKG_VAR_DIR + "/admin"

		# Fields numbers in a catalog entry for a package
		self.CNAMEF = 0; self.VERSIONF = 1
		self.PKGNAMEF = 2; self.PKGFILEF = 3
		self.MD5SUMF = 4

		# Action codes for packages
		self.INSTALL = 1; self.UPGRADE = 2

	def set_altroot(self, apath):
		if self.ALTROOT == "":
			self.ALTROOT = ""
			self.SPKG_VAR_DIR = apath + self.SPKG_VAR_DIR
        		self.SPKG_DWN_DIR = apath + self.SPKG_DWN_DIR
        		self.INSTPKGDIR = apath + self.INSTPKGDIR
        		self.ADMINFILE = apath + self.ADMINFILE
		else:
			self.SPKG_VAR_DIR = self.SPKG_VAR_DIR.replace(self.ALTROOT, apath)
			self.SPKG_DWN_DIR = self.SPKG_DWN_DIR.replace(self.ALTROOT, apath)
			self.INSTPKGDIR = self.INSTPKGDIR.replace(self.ALTROOT, apath)
			self.ADMINFILE = self.ADMINFILE.replace(self.ALTROOT, apath)
			self.ALTROOT = apath


class PKGVersError(Exception):
	"""Invalid version exception"""

	def __init__(self, message):
		self.message = message

class PKGError(Exception):
	"""General packaging error"""

	def __init__(self, message):
		self.message = message

vars = Cl_vars()

def usage():
	print >> sys.stderr, _("""\
Usage:
	spkg [options] subcommand [cmd_options] [operands]

Subcommands:
	spkg updatecatalog   Updates download site metadata
	spkg install [-nvq]  <package names>
			     Install one or more packages/package clusters
	spkg upgrade <Upgrade Type>|<package list>
			Upgrades already installed packages if possible
			Upgrade type can be one of:
			core - Upgrade the core distro (Kernel, core libs etc.)
			all - Upgrade the entire distribution.
	spkg available       Lists the available packages in all catalogs
	spkg compare         Shows installed package versions vs available
	spkg list            List all installed packages by name
	spkg init <dir>      Initialize an Alternate Root image in the fiven dir
			     The dir is created if it does not exist
	spkg download	     Just download the package, do not install
	spkg describe        List one line descriptions for all available packages

Options:
	-R <dir>             Perform all operations onto an Alternate Root image in the dir
	-s http://site/dir   Temporarily override site to get from

Environment Valriables:
	ALTROOT		     Directory that contains an Alternate root image
			     This variable can be used in lieu of -R
	http_proxy	     Http proxy server
	ftp_proxy	     Ftp proxy server""")
	sys.exit(2)

#
# Useful utility functions
#
def removef(path):
	"""Emulate rm -f <filename>"""
	try:
		os.unlink(path)
	except:
		pass

def exec_prog(cmd, outp):
	"""Execute an external program and return stdout if needed."""

	err_file = os.tmpfile()

	output = ""
	if outp == 1:
		pipe = Popen(cmd, shell=True, stdout=PIPE, stderr=err_file, close_fds=True)
		output = pipe.stdout.read()
	else:
		pipe = Popen(cmd, shell=True, stdout=None, stderr=None, close_fds=False)
	rt = pipe.wait()

	if rt != 0:
		err_file.seek(0)
		print >> sys.stderr, \
		    "WARNING: " + cmd + " had errors\n" + err_file.read()
		output = "-EE-"
	err_file.close()

	return string.strip(output)


def load_config():
	"""Load configuration file and also detect environment settings."""

	rt = 0
	# Hardcoded for now
	vars.cnffile = "/etc/spkg.conf"
	com = re.compile("^#")

	fl = open(vars.cnffile, "r")
	for line in fl:
		if com.match(line):
			continue

		line = string.strip(line)
		fields = line.split("=")
		if len(fields) < 2:
			continue

		if fields[0] == "RTYPE":
			vars.RTYPE = fields[1]
		elif fields[0] == "PKGSITES":
			vars.PKGSITES = fields[1].split(" ")
		elif fields[0] == "FTP_PROXY":
			if not os.environ.has_key("ftp_proxy"):
				os.environ["ftp_proxy"] = fields[1]
		elif fields[0] == "HTTP_PROXY":
			if not os.environ.has_key("http_proxy"):
				os.environ["http_proxy"] = fields[1]
		elif fields[0] == "PKGADDFLAGS":
			vars.PKGADDFLAGS = fields[1]
		elif fields[0] == "SPKG_DOWNLOAD_DIR":
			vars.SPKG_DOWNLOAD_DIR = fields[1]
		elif fields[0] == "SPKG_PRESERVE_DOWNLOADS":
			if fields[1] == "true":
				vars.SPKG_PRESERVE_DOWNLOADS = True
		elif fields[0] == "USE_GPG":
			if fields[1] == "true":
				vars.USE_GPG = True
		elif fields[0] == "USE_MD5":
			if fields[1] == "true":
				vars.USE_MD5 = True

	vars.OSREL = exec_prog("uname -r", 1)
	vars.ARCH = exec_prog("uname -p", 1)

	if vars.OSREL == "-EE-" or vars.ARCH == "-EE-":
		rt = 1
	else:
		# Initialize site-specific variables
		#
		for site in vars.PKGSITES:
			sitevars = Cl_sitevars(site, \
			    vars.RELEASE, vars.RTYPE, vars.SPKG_VAR_DIR)
			vars.PKGSITEVARS.append(sitevars)

	return rt

#
# Download from a given URL to a given file. It can also take
# a file:// url in which case it copies the given file.
#
def downloadurl(url, targ):
	"""Use a downloader to fetch the given URL. Return the size or -1 for error."""

	# TODO: Move to prozilla later
	wgetopts = "-c -O %s" % targ
	if url[:7] == "file://":
		fl = url[8:]
		if not os.path.isfile(fl):
			print >> sys.stderr, \
			    "ERROR: file %s does not exist" % fl
			return 1
		shutil.copyfile(fl, targ)
	elif url[:6] == "ftp://":
		wgetopts = "-O %s --passive-ftp" %targ

	ret = 0
	out = exec_prog("%s %s %s" % (vars.WGET, wgetopts, url), 0)
	if out == "-EE-":
		ret = -1
	else:
		sz = 0
		try:
			sz = os.path.getsize(targ)
		except OSError, o:
			pass
		ret = sz
	return ret

#
# Given a package revision string of the form:
# VERSION=11.11,REV=2008.07.10.02.06
# it can compute a an uniform numeric version sting of the form:
# 1111.0000.1075.9724.46
#
def compute_version(verstr):
	"""Compute an uniform version string given a package revision string"""

	_version, _revision = verstr.split(",")
	_revision.replace(".0", ".")
	_revision.replace("..", ".0.")

	version = _version.split("=")[1]
	if len(version) == 0:
		version = "1"

	revision = _revision.split("=")[1]
	rv = revision.split(".")
	ln = len(rv)

	cnv1 = Decimal(535680);  cnv2 = Decimal(44640)
	cnv3 = Decimal(1440);    cnv4 = Decimal(60)

	if ln == 8:
		pkgrev = Decimal(rv[3]) * cnv1 + Decimal(rv[4]) * cnv2 + \
		    Decimal(rv[5]) * cnv3 + Decimal(rv[6]) * cnv4 + Decimal(rv[7])
	elif ln == 5:
		pkgrev = Decimal(rv[0])  * cnv1 + Decimal(rv[1]) * cnv2 + \
		    Decimal(rv[2]) * cnv3 + Decimal(rv[3]) * cnv4 + Decimal(rv[4])
	elif ln == 4:
		pkgrev = Decimal(rv[0]) + Decimal(rv[1]) * cnv1 + Decimal(rv[2]) * cnv2 + \
		    Decimal(rv[3]) * cnv3
	elif ln == 3:
		pkgrev = Decimal(rv[0]) * cnv1 + Decimal(rv[1]) * cnv2 + Decimal(rv[2]) * cnv3
	else:
		rv = time.strftime("%Y.%m.%d.%H.%M")
		pkgrev = Decimal(rv[0])  * cnv1 + Decimal(rv[1]) * cnv2 + \
		    Decimal(rv[2]) * cnv3 + Decimal(rv[3]) * cnv4 + Decimal(rv[4])


	version = version.replace(".", "").ljust(8, "0")
	revline = version + str(pkgrev)
	tot = len(revline)
	cnt = 0
	num = 1
	vstr = []
	while cnt < tot:
		dig = revline[cnt]
		vstr.append(dig)
		cnt = cnt + 1
		if num % 4 == 0 and cnt < tot:
			vstr.append('.')
        	num = num + 1

	return ''.join(vstr)

#
# Compare the version part or first 2 components of the version string
# ver1 > ver2:  return 1
# ver1 == ver2:  return 0
# ver1 < ver2;  return -1
#
def compare_version(vstr1, vstr2):
	"""Compare only the version parts of the given version strings.
	First 2 segments of the version string give the upstream package
	version."""

	vers1 = Decimal(''.join(vstr1.split(".")[0:2]))
	vers2 = Decimal(''.join(vstr2.split(".")[0:2]))

	return str(vers1.compare(vers2))


#
# Compare the revision portion of the version string.
# ver1 > ver2:  return 1
# ver1 == ver2:  return 0
# ver1 < ver2;  return -1
#
def compare_revision(vstr1, vstr2):
	"""Compare onyl the revision portion of the given version strings.
	All segments after first 2 in the version string constitute package revision."""

	rev1 = Decimal(''.join(vstr1.split(".")[2:]))
	rev2 = Decimal(''.join(vstr2.split(".")[2:]))

	return str(rev1.compare(rev2))

#
# Compare the full version string
# ver1 > ver2:  return 1
# ver1 == ver2:  return 0
# ver1 < ver2;  return -1
#
def compare_vers(vstr1, vstr2):
	"""Compare the complete version string"""

	ver1 = Decimal(vstr1.replace(".", ""))
	ver1 = Decimal(vstr2.replace(".", ""))

	return str(ver1.compare(ver1))

def fetch_local_version(vars, pkgname):
	"""Return the installed package version in uniform version format"""

	vf = open("%/%s/pkginfo" % (vars.INSTPKGDIR, pkgname))
	for line in vf:
		if line[0:4] == "VERS":
			vf.close()
			return (compute_version(line.strip()))

	raise PKGVersError("FATAL: VERSION field not found for package %s" % pkgname)

#
# Generic catalog search routine to support spkg search
#
def searchcatalog(sitevars, srchre, fieldnum):
	"""Search the site's catalog for the given regexp in the given field."""

	catf = open(sitevars.catalog, "r")
	matches = []
	for line in catf:
		entry = line.split(" ")
		if srchre.match(entry[fieldnum]):
			matches.append(Cl_pkgentry(entry, sitevars))

	return matches

#
# Download catalogs and package metadata for all configured sites
#
def updatecatalog(vars, pargs):
	"""Refresh catalogs and other metadata for all sites."""

	failed_sites = []
	errored = 0

	for sv in vars.PKGSITEVARS:
		removef(sv.tcat)

		#
		# Try to fetch the catalog first
		#
		ret = downloadurl("%s/%s/%s/catalog" % (sv.fullurl, vars.ARCH, vars.OSREL), 
		    sv.tcat)
		if ret <= 0:
			if ret < 0:
				failed_sites.append((sv.site, \
				    _("ERROR: Could retrieve catalog file")))
			else:
				failed_sites.append((sv.site, \
				    _("ERROR: catalog file is zero length.")))
			errored = 1
			removef(sv.tcat)
			continue

		## TODO GPG signature checking
		print "Updating Catalog for site %s\n" % sv.site
		shutil.copyfile(sv.tcat, sv.catalog)
		removef(sv.tcat)

		#
		# Try to fetch the metainfo. This is required
		#
		ret = downloadurl("%s/trunk/%s/%s/%s/metainfo.tar.7z" % \
		    (sv.site, vars.RTYPE, vars.ARCH, vars.OSREL), sv.tmeta)
		if ret <= 0:
			if ret < 0:
				failed_sites.append((sv.site, \
				    _("ERROR: Could not retrieve metainfo")))
			else:
				failed_sites.append((sv.site, \
				    _("ERROR: metainfo is zero length.")))
			errored = 1
			removef(sv.tmeta)
			continue
		else:
			## TODO GPG signature checking
			print "\nUpdating metainfo for site %s\n" % sv.site
			out = exec_prog("%s e -so %s | (cd %s; tar xf -)" % \
			    (vars.SZIP, sv.tmeta, vars.SPKG_VAR_DIR), 0)
			if out == "-EE-":
				failed_sites.append((sv.site, \
				    _("ERROR: Could not extract metainfo")))
				errored = 1
				removef(sv.tmeta)
				shutil.rmtree(sv.tmetadir, True)
				continue
			shutil.rmtree(sv.metadir, True)
			os.rename(sv.tmetadir, sv.metadir)
			removef(sv.tmeta)

		# Now fetch descriptions file if any
		removef(sv.tdesc)
		downloadurl("%s/%s/%s/descriptions" % (sv.fullurl, vars.ARCH, vars.OSREL), sv.tdesc)
		sz = 0
		try:
			sz = os.path.getsize(sv.tdesc)
			if sz > 0:
				shutil.copyfile(sv.tdesc, sv.desc)
			removef(sv.tdesc)
		except OSError, o:
			removef(sv.tdesc)
	if errored == 1:
		print "\n\n"
		print "ERROR: Failed to update metadata for some sites. Log follows: \n"
		for stuple in failed_sites:
			print "%s :: \n" % stuple[0]
			print "              %s\n" % stuple[1]
		return 1
	return 0

#
# Core package scanning and dependency list scanning logic. However does not
# build a dependency sorted list. Rather it returns the fully resolved package
# hash with all dependencies.
# type == 1   Install packages
# type == 2   Upgrade packages
# type == 0   Do both
#
# type is either 1 or 2 only at the top level invocation of this function.
# subsequent recursive calls always pass type as 0 since for both upgrade
# and install dependencies my need to be upgraded or installed.
#
def build_pkglist(vars, pkgs, pdict, type):
	"""Build a complete list of packages to be installed/upgraded
	including resolved dependencies"""

	if len(pkgs) == 0:
		return 0

	ret = 0
	#
	# Identify site containing packages. First site in list having the
	# package is used.
	#
	for sv in vars.PKGSITEVARS:
		catf = open(sv.catalog, "r")

		# All packages already found in an earlier site, so bail
		if len(pkgs) == 0: break

		# Scan catalog for the site
		# After scanning pdict will have the latest version entry from the catalog
		rmlist = []
		for line in catf:
			entry = line.split(" ")
			if len(entry) != 5: continue
			for name in pkgs:
				if name == entry[vars.CNAMEF] or name == entry[vars.PKGNAMEF]:
					nm = entry[vars.PKGNAMEF]
					if pdict.has_key(nm):
						if compare_vers(entry[vars.VERSIONF], \
						    pdict[nm].version) > 0:
							pdict[nm].update(entry, sv)
							continue
					else:
						pdict[nm] = Cl_pkgentry(entry, sv)
						pdict[nm].refername = name
						rmlist.append(name)
		#
		# Remove packages that have already been found
		#
		for name in rmlist:
			pkgs.remove(name)
	catf.close()

	# Check for packages not found
	if len(pkgs) > 0:
		print >> sys.stderr, \
		    _("ERROR: The following packages not found in any catalog")
		for name in pkgs:
			print "%s " % name
		return 1

	deplist = []
	for pkgname in pdict.keys():
		#
		# pdict now has latest versions of all specified packages
		# Now based on what we are doing check for installed packages
		# and versions.
		#
		if os.path.exists("%s/%s" % (vars.INSTPKGDIR, pkgname)):
			if type == 1:
				print >> sys.stderr, \
				    "Package %s already installed" % name
				return 1
			elif type == 2 or type == 0:
				localver = fetch_local_version(vars, pkgname)
				if compare_vers(localver, pdict[pkgname].version) > 0:
					pdict[pkgnamne].action = vars.UPGRADE
				else:
					print >> sys.stderr, \
					    "Package %s is up to date\n", pkgname
					del pdict[pkgname]
		else:
			if type == 1 or type == 0:
				pdict[pkgname].action = vars.INSTALL

			elif type == 2:
				print >> sys.stderr, \
				    "Package %s is not installed" % name
				return 1

		depends = "%s/%s/%s/depend" % (pdict[pkgname].sitevars.metadir, \
		    pkgname, pdict[pkgname].version)
		depf = open(depends, "r")
		for line in depf:
			if line[0] == "P":
				# Get rid of TABs
				line = line.replace("	", " ")
				de = line.split(" ")

				#
				# Ignore already installed dependencies when installing.
				#
				if type == 1:
					if os.path.exists("%s/%s" % (vars.INSTPKGDIR, de[1])):
						continue
				try:
					i = deplist.index(de[1])
				except ValueError:
					if not pdict.has_key(de[1]):
						deplist.append(de[1])
					pdict[pkgname].deplist.append(de[1])
		depf.close()

	#
	# Recursion to scan the dependency list. Circular dependencies
	# are taken care of by the pdict check above.
	#
	if type == 1:
		#
		# If we are installing, we only install not upgrade any packages.
		# TODO: Advanced version based dependency checks will change this
		#
		ret = build_pkglist(vars, deplist, pdict, 1)
	else:
		#
		# If we are upgrading we can install or upgrade dependencies as
		# well.
		#
		ret = build_pkglist(vars, deplist, pdict, 0)

	return ret

def install_pkg(vars, ent, pkgfile):
	"""Install the given package. pkgfile is a compressed 7Zip datastream package"""

	if vars.ALTROOT != "":
		PKGADDFLAGS = "-R %s -n -a %s" % (vars.ALTROOT, vars.ADMINFILE)
	else:
		PKGADDFLAGS = "-n -a %s" % vars.ADMINFILE

	pkgfileds = pkgfile + ".tmp"

	ret = exec_prog("7za e -so %s > %s" % (pkgfile, pkgfileds), 0)
	if ret == "-EE-":
		os.unlink(pkgfile);  os.unlink(pkgfileds)
		raise PKGError("Failed to decompress package %s" % ent.refername)

	ret = exec_prog("pkgadd %s -d %s %s" % (PKGADDFLAGS, pkgfileds, ent.pkgname), 0)
	if ret == "-EE-":
		os.unlink(pkgfile);  os.unlink(pkgfileds)
		raise PKGError("Failed to install package %s" % ent.refername)

	os.unlink(pkgfile);  os.unlink(pkgfileds)

#
# Main package installation routine
#
def install(vars, pargs):
	"""Install one or more packages listed on the command line"""
	if len(pargs) == 0:
		print >> sys.stderr, \
		    "No packages specified to install."
		return

	#########################################
	# Installation plan creation phase
	#########################################
	ret = 0
	pdict = {}
	ret = build_pkglist(vars, pargs, pdict, 1)

	if ret != 0:
		return ret

	#
	# We now have a dictionary of the full list of package objects to be installed
	# We now need to build a partial dependency dict and do a topological sort on
	# that to get the proper order of installation.
	#
	graphdict = {}
	for name, entry in pdict.iteritems():
		for dep in entry.deplist:
			if graphdict.has_key(dep):
				graphdict[dep].append(name)
			else:
				graphdict[dep] = [name]

	#
	# Add circular self depdencies for packages with no deps listed otherwise the
	# topo sort complains. These circular deps are properly handled.
	#
	for name in pdict.keys():
		if not graphdict.has_key(name):
			graphdict[name] = [name]

	sorted_list = tsort.robust_topological_sort(graphdict)
	#########################################
	# End of Installation plan creation phase
	#########################################

	for titem in sorted_list:
		for pkgname in titem:
			ent = pdict[pkgname]
			pkgurl = "%s/%s/%s/%s" % \
			    (ent.sitevars.fullurl, vars.ARCH, vars.OSREL, ent.pkgfile)
			tfile = "%s/%s" % (vars.SPKG_DWN_DIR, ent.pkgfile)
			ret = downloadurl(pkgurl, tfile)

			if ret <=0:
				print >> sys.stderr, \
				    "FATAL: Download failed for package %s" % \
				    ent.refername
				return 1
			if ent.action == vars.INSTALL:
				install_pkg(vars, ent, tfile)

	return ret

def upgrade(vars, pargs):
	return 0

def available(vars, pargs):
	return 0

def compare(vars, pargs):
	return 0

def list(vars, pargs):
	return 0

def download(vars, pargs):
	return 0

def describe(vars, pargs):
	return 0

def info(vars, pargs):
	return 0

def do_main():
	"""Main entry point."""
	gettext.install("spkg", "/usr/lib/locale");

	ret = 0
	try:
		opts, pargs = getopt.getopt(sys.argv[1:], "s:R:")
	except getopt.GetoptError, e:
		print >> sys.stderr, \
		    _("spkg: illegal global option -- %s") % e.opt
		usage()

	if pargs == None or len(pargs) == 0:
		usage()
		sys.exit(2)

	subcommand = pargs[0]
	del pargs[0]

	if subcommand == "init":
		ret = init(vars, pargs)
		return ret

	ALTROOT = ""
	for opt, arg in opts:
		if opt == "-R":
			ALTROOT = arg

	if os.environ.has_key("ALTROOT"):
		ALTROOT = os.environ["ALTROOT"]

	if ALTROOT != "":
		if not os.path.isfile(ALTROOT + '/etc/spkg.conf') or \
		    not os.path.isfile(ALTROOT + '/var/spkg/admin'):
			print >> sys.stderr, \
			    _("'%s' is not a valid Alternate Root image") % vars.ALTROOT
			return 1
		vars.set_altroot(ALTROOT)

	relfile = "%s/etc/release_tag" % vars.ALTROOT
	if os.path.isfile(relfile):
		rf = open(relfile, "r")
		vars.RELEASE = string.strip(rf.readline())
		rf.close()

	if subcommand == "updatecatalog":
		ret = updatecatalog(vars, pargs)
	elif subcommand == "install":
		ret = install(vars, pargs)
	elif subcommand == "upgrade":
		ret = upgrade(vars, pargs)
	elif subcommand == "available":
		ret = available(vars, pargs)
	elif subcommand == "compare":
		ret = compare(vars, pargs)
	elif subcommand == "list":
		ret = list(vars, pargs)
	elif subcommand == "download":
		ret = download(vars, pargs)
	elif subcommand == "describe":
		ret = describe(vars, pargs)
	elif subcommand == "info":
		ret = info(vars, pargs)
	else:
		print >> sys.stderr, \
		    "spkg: unknown subcommand '%s'" % subcommand

	return ret


