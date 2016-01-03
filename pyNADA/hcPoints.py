#!/usr/bin/python2.7.6 -tt
import numpy

# ppoints, cohn, hc_ppoints_cen, hc_ppoints_uncen are all called by
# hcPoints function.
# ppoints calculates ploting positions for completely uncensored data:
def ppoints(n):
    n = numpy.array(n)
    if len(n) == 1 and n == 0:
        ppoints = 0
    else:
        if len(n) <= 10:
            a = float(3./8.)
        else:
            a = 1./2.
        nlength = len(n)
        n = range(1, nlength + 1)
        n = numpy.array(n)
        n = n - a
        nx = nlength + 1 - 2 * a
        ppoints = n/nx    
    return(ppoints)    


# cohn Calculates "Cohn" Numbers -- quantities described by
# Helsel and Cohn's (1988) reformulation of a prob-plotting formula
# described by Hirsch and Stedinger (1987).
#
# The Cohn Numbers are:
# A_j   = the number of uncensored obs above the jth threshold.
# B_j   = the number of observations (cen & uncen) below the jth threshold.
# C_j   = the number of censored observations at the jth threshold
# P_j   = the probability of exceeding the jth threshold

def cohn(obs, cens):
    import pandas as pd
    # obs = pd.Series([obs])
    # cens = pd.Series([cens], dtype='bool8')
    uncen = obs[numpy.logical_not(cens)]
    cen = obs[cens]
    # A = B = C = P

    limit = numpy.unique(cen)
    a = len(uncen[uncen < limit[0]])
    if a > 0:
        limit = numpy.append(0, limit)
    # Get upper end values for A, B, C then use loops to get the other values.
    A_0 = sum(uncen >= limit[len(limit)-1])
    B_0 = len(obs[obs <= limit[len(limit)-1]])-len(uncen[uncen == limit[len(limit)-1]])
    P = [float(A_0)/(A_0 + B_0)] * len(limit)
    i = len(limit)
    i = i - 1   # yes, I could use the shortcut
    i = range(0, i)

    # calculate A
    A = [[limit[j] <= a < limit[j+1] for a in uncen] for j in i]
    A = [sum(a) for a in A]
    A.append(A_0)
    A = numpy.array(A)
    # calculate B
    B_1 = [[a <= limit[j] for a in obs] for j in i]
    B_1 = [sum(b) for b in B_1]
    B_2 = [[a == limit[j] for a in uncen] for j in i]
    B_2 = [sum(b) for b in B_2]
    B = numpy.array(B_1) - numpy.array(B_2)
    B = numpy.append(B, B_0)
    C = [[a == b for a in cen] for b in limit]
    C = [sum(c) for c in C]
    C = numpy.array(C)
    # do P
    for i in i:
        P[i] = P[i+1] + ((float(A[i])/(A[i] + B[i])) * (1 - P[i + 1]))
    P = numpy.array(P)
    #print([A,B,C,P,limit])
    return([A, B, C, P, limit])

#calculates ploting positing for uncensored observations
def hc_ppoints_uncen(obs, cens, cn):
    # insert defensive code here.
    A = cn[0]
    B = cn[1]
    C = cn[2]
    P = cn[3]
    limit = cn[4]
    nonzero = A != 0
    A = A[nonzero]
    B = B[nonzero]
    P = P[nonzero]
    limit = limit[nonzero]
    n = len(limit)
    pp = []
    for i in range(0,n):
        R = range(1, A[i]+1)
        if i+1 > len(P)-1:
            k = 0
        else:
            k = P[i+1]
        pp_x = [(1 - P[i]) + ((P[i] - k) * R[r]) / (A[i] + 1) for r in range(0, len(R))]
        pp.append(pp_x)
    pp = numpy.array(pp)
    pp = numpy.hstack(pp)
    return(pp)

# hc_ppoints_cen calculates censored plotting positions
def hc_ppoints_cen(obs, cens, cn):
    #insert defensive stuff here
    #obs = numpy.array(obs)
    #cens = numpy.array(cens)
    C = cn[2]
    P = cn[3]
    limit = cn[4]

    if P[0] == 1:
        C = C[1:]
        P = P[1:]
        limit = limit[1:]
    pp = ([])
    for i in range(0, len(limit)):
        c_i = C[i]
        for r in range(1, c_i +1):
            pp.append((1-P[i]) * r/(c_i + 1))
    pp = numpy.array(pp)
    return(pp)


# hcPoints calculates plotting positions using above functions
def hcPoints(obs, cens):
    #print ("HELLO")
    import pandas as pd
    # insert defensive algorythm here or before?
    assert len(obs) == len(cens)
    #cens = numpy.bool8(cens)
    #obs = numpy.array(obs)
    pp = pd.Series(numpy.random.rand(len(obs)))
    if not any(cens):
        pp = ppoints(obs)
    else:
        cn = cohn(obs, cens)
        hcPPointsUncen = hc_ppoints_uncen(obs, cens, cn)
        pp[numpy.logical_not(cens)] = hcPPointsUncen
        hcPPointsCen = hc_ppoints_cen(obs, cens, cn)
        pp[cens] = hcPPointsCen
        pp = pd.Series(pp)
    return(pp)
