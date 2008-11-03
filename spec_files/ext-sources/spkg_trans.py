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
import traceback
import gettext
import string
import time
import cPickle

class transaction_log(object):
	"""
	This exposes an API to create and update a simple transaction log of current
	packaging operations.
	"""

	def __init__(self, logdir, type, transid = None):
		if not os.path.exists(logdir):
			os.makedirs(logdir)

		self.altroot = ""
		if not transid:
			transid = str(time.time())
			tpath = os.path.join(logdir, transid)
			os.mkdir(tpath)
			self.type = type
			self.transid = transid
			self.tpath = tpath
			self.statefile = os.path.join(self.tpath, "state")
			self.planfile = os.path.join(self.tpath, "plan.pickle")

			tf = open(os.path.join(tpath, "type"), "w")
			tf.write(type)
			tf.close()
			self.put_state("BEGIN")
			self.mode = "NEW"

		else:
			tpath = os.path.join(logdir, transid)
			self.transid = transid
			self.tpath = tpath

			tf = open(os.path.join(tpath, "type"), "r")
			self.type = tf.read()
			tf.close()

			self.statefile = os.path.join(tpath, "state")
			if os.path.exists(self.statefile):
				statef = open(self.statefile, "r")
				self.state = statef.read()
				statef.close()
			else:
				self.state = "BEGIN"
			self.planfile = os.path.join(self.tpath, "plan.pickle")
			self.mode = "RESUME"

	def put_state(self, state):
		statef = open(self.statefile, "w")
		statef.write(state)
		statef.flush()
		statef.close()
		self.state = state

	def get_state(self):
		return self.state

	def get_mode(self):
		return self.mode

	def put_data(self, data):
		dataf = open(os.path.join(self.tpath, "data"), "a+")
		dataf.write(data)
		dataf.close()

	def get_data(self):
		df = os.path.join(self.tpath, "data")
		if os.path.exists(df):
			dataf = open(df, "r")
			dat = dataf.read()
			dataf.close()
			return dat
		return ""

	def put_plan(self, plan):
		plst = []
		sdict = {}
		for pn in plan.sorted_list:
			pkgl, sv = plan.pdict[pn[0]].tolist()
			sdict[sv[0]] = sv
			plst.append(pkgl)
		svl = sdict.values()
		planinfo = [plst, plan.action, plan.num, svl]
		pf = open(self.planfile, "w")
		cPickle.dump(planinfo, pf, 2)
		pf.close()

	def get_plan(self, plan, pkgcl, svcl):
		pf = open(self.planfile, "r")
		planinfo = cPickle.load(pf)
		pf.close()
		plan.action = planinfo[1]
		plan.num = planinfo[2]
		sdict = {}
		for sv in planinfo[3]:
			sdict[sv[0]] = svcl(sv[0], sv[1], sv[2], sv[3])
		for pl in planinfo[0]:
			pkg = pkgcl(None, None, pl)
			pkg.sitevars = sdict[pl[8]]
			plan.sorted_list.append((pkg.pkgname,))
			plan.pdict[pkg.pkgname] = pkg
		return plan

	def done(self):
		if os.path.exists(self.tpath):
			shutil.rmtree(self.tpath)

def check_pending_trans(logdir):
	lst = []
	if os.path.exists(logdir):
		for transid in os.listdir(logdir):
			typefl = os.path.join(logdir, transid, "type")
			typef = open(typefl, "r")
			type = typef.read()
			typef.close()
			lst.append("%s*%s" % (transid, type))
	return lst

def list_pending_trans(logdir):
	if os.path.exists(logdir):
		tlist = os.listdir(logdir)
		tlist.sort()
		if not tlist or len(tlist) == 0:
			print "No pending transactions\n"
			return

		print ""
		for transid in tlist:
			typefl = os.path.join(logdir, transid, "type")
			typef = open(typefl, "r")
			type = typef.read()
			typef.close()
			print "Transaction ID: %s, Type: %s, Started on: %s" % \
			    (transid, type, time.strftime("%b %d %Y %H:%M", \
			    time.localtime(float(transid))))
		print ""
