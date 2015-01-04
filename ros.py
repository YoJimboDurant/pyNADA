#!/usr/bin/python2.7.6 -tt
import sys
import numpy
import hcPoints
from scipy.stats import norm
from scipy import stats


# ros is basic skeleton at this point. It needs flexible transformation added, but for now
# it uses natural log for foward transformation and exponent for reverse. 

def ros(obs, cens):
    # insert more defensive programming stuff here.
    obs = numpy.array(obs, dtype=float)
    cens = numpy.bool8(cens)
    assert len(obs) == len(cens)
    if len(obs[cens])/len(obs) > 0.8:
        print "warning: Input > 80% censored, results are tenuous.\n"
    
    ix = obs > max(obs[numpy.logical_not(cens)])
    if any(ix):
        print "Dropped censored values that exceed max of uncensored values.\n"
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

def main():
    # this does not work - I need a way to get a set of numbers in from the command line?
    obs = sys.argv([1])
    cens = sys.argv([2])
    ros(obs, cens)

# standard boilerplate:

if __name__ == '__main__':
    main()


    

