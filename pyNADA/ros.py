#!/usr/bin/python2.7.6 -tt

import sys
import warnings

import numpy
from scipy.stats import norm
from scipy import stats

import hcPoints
import pyNADA.entry.plugin

# ros is basic skeleton at this point. It needs flexible transformation added, but for now
# it uses natural log for foward transformation and exponent for reverse.

def ros(obs, cens):
    # insert more defensive programming stuff here.
    obs = numpy.array(obs, dtype=float)
    cens = numpy.bool8(cens)
    assert len(obs) == len(cens)
    if len(obs[cens])/len(obs) > 0.8:
        warnings.warn("warning: Input > 80% censored, results are tenuous.", warnings.UserWarning)

    ix = obs > max(obs[numpy.logical_not(cens)])
    if any(ix):
        warnings.warn("Dropped censored values that exceed max of uncensored values.", warnings.UserWarning)
        obs = obs[numpy.logical_not(ix)]
        cens = cens[numpy.logical_not(ix)]
    ix = obs.argsort()
    obs = obs[ix]
    cens = cens[ix]
    pp = numpy.array([])
    pp = hcPoints.hcPoints(obs, cens)
    pp_nq = norm.ppf(pp[numpy.logical_not(cens)])
    obs_transformed = numpy.log(obs[numpy.logical_not(cens)])
    slope, intercept, r_value, p_value, std_err = stats.linregress(pp_nq, obs_transformed)
    predicted = norm.ppf(pp[cens]) * slope + intercept
    predicted = numpy.exp(predicted)
    modeled = obs
    modeled[numpy.logical_not(cens)] = obs[numpy.logical_not(cens)]
    modeled[cens] = predicted
    return(modeled)

class ROSEntry(pyNADA.entry.plugin.Plugin):
    @classmethod
    def registerSubparser(cls, parent):
        import argparse # forces minimum python version of 2.7

        parser = parent.add_parser('ros', help='Run ros from the command line')
        parser.set_defaults(subcommand=ROSEntry())

        parser.add_argument('files', nargs='*', help='CSV files containing the observations or - for stdin.')
        parser.add_argument('--selector', dest='selector', default='*',
            help='A glob pattern that is used to select rows by the "sample number" column.')

    def __call__(self, args):
        import csv
        import fileinput
        import itertools
        import re
        import fnmatch

        selector = re.compile(fnmatch.translate(args.selector))

        obs, cens = zip(
            *itertools.imap(lambda row: (float(row['obs']), int(row['cens'])),
                itertools.ifilter(lambda row: selector.match(row['sample number']),
                    csv.DictReader(fileinput.input(args.files)))))

        print ros(obs, cens)
