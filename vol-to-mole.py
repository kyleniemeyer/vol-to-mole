#! /usr/bin/env python

# species densities via NIST Chemistry Webbook and Yaws' Handbook (via Knovel) 
# at room tempetature (298 K and 1 atm)

import readline
from collections import namedtuple

# density in units kg/m^3
Species = namedtuple('Species', 'mw, density, numC, numH, numO')
specList = {
    'nc7h16': Species(100.21, 679.72, 7, 16, 0),
    'n-heptane': Species(100.21, 679.72, 7, 16, 0),
    'ic8h18': Species(114.23, 698.39, 8, 18, 0),
    'iso-octane': Species(114.23, 698.39, 8, 18, 0),
    'c6h5ch3': Species(92.14, 862.38, 7, 8, 0),
    'toluene': Species(92.14, 862.38, 7, 8, 0),
    'nc10h22': Species(142.28, 726.64, 10, 22, 0),
    'n-decane': Species(142.28, 726.64, 10, 22, 0),
    'nc12h26': Species(170.34, 745.84, 12, 26, 0),
    'n-dodecane': Species(170.34, 745.84, 12, 26, 0),
    'nc16h34': Species(226.441, 770.27, 16, 34, 0),
    'n-hexadecane': Species(226.441, 770.27, 16, 34, 0),
    'cetane': Species(226.441, 770.27, 16, 34, 0),
    'ic16h34': Species(226.441, 793.0, 16, 34, 0),
    'hmn': Species(226.441, 793.0, 16, 34, 0),
    'iso-cetane': Species(226.441, 793.0, 16, 34, 0),
    'nc9h12': Species(120.192, 859.7, 9, 12, 0),
    'n-propylbenzene': Species(120.192, 859.7, 9, 12, 0),
    'c6h5ch2ch2ch3': Species(120.192, 859.7, 9, 12, 0),
    'c6h3(ch3)3': Species(120.192, 858.2, 9, 12, 0),
    'mesitylene': Species(120.192, 858.2, 9, 12, 0),
    'md': Species(186.291, 869.2, 11, 22, 2),
    'methyl decanoate': Species(186.291, 869.2, 11, 22, 2),
    'c11h22o2': Species(186.291, 869.2, 11, 22, 2),
    'methyl caprate': Species(186.291, 869.2, 11, 22, 2),
    'c5h10-2': Species(70.13, 650.0, 5, 10, 0),
    '2-pentene': Species(70.13, 650.0, 5, 10, 0),
    'c6h12-1': Species(84.1608, 673.0, 6, 12, 0),
    '1-hexene': Species(84.1608, 673.0, 6, 12, 0),
    'ch4o': Species(32.0419, 786.5, 1, 4, 1),
    'ch3oh': Species(32.0419, 786.5, 1, 4, 1),
    'methanol': Species(32.0419, 786.5, 1, 4, 1),
    'c2h6o': Species(46.0684, 785.6, 2, 6, 1),
    'c2h5oh': Species(46.0684, 785.6, 2, 6, 1),
    'ethanol': Species(46.0684, 785.6, 2, 6, 1),
    'c3h8o': Species(60.0950, 787.6, 3, 8, 1),
    'c3h7oh': Species(60.0950, 787.6, 3, 8, 1),
    'propanol': Species(60.0950, 787.6, 3, 8, 1),
    'c4h10o': Species(74.1216, 794.3, 4, 10, 1),
    'c4h9oh': Species(74.1216, 794.3, 4, 10, 1),
    'n-butanol': Species(74.1216, 794.3, 4, 10, 1),
    '1-butanol': Species(74.1216, 794.3, 4, 10, 1),
    'isobutanol': Species(74.1216, 787.4, 4, 10, 1)
}

def volToMole(equil):
    """Calculates molar fractions from volume fractions.
    
    equil: True if just equilibrium calculation
    """
    
    if equil:
        print 'Enter species followed by mole fraction (e.g., nc7h16 0.2)'
    else:
        print 'Enter species followed by volume fraction (e.g., nc7h16 0.2)'
    print 'Hit return when complete.'
    
    specs = []
    nums = []
    while True:
        sp = None
        num = None
        while not num:
            try:
                line = raw_input('Entry: ')
                if not line: break
                sp, num = line.split()
                num = float(num)
                
                # check if species in list
                density = specList[sp].density
            except ValueError:
                print 'Number invalid'
            except KeyError:
                print 'Error: species ' + sp + ' not found.'
        if not sp: break
        
        # get molecular weight and density
        if not equil:
            num = num * specList[sp].density
        
        specs.append(sp)
        nums.append(num)
    
    # need to calculate mass and mole fractions if starting with volume
    if not equil:
        massFrac = nums[:]
        massFrac = [n / sum(massFrac) for n in massFrac]
        
        sumMole = 0.0
        for sp, Y in zip(specs, massFrac):
            sumMole = sumMole + (Y / specList[sp].mw)
        
        moleFrac = []
        for sp, Y in zip(specs, massFrac):
            X = Y / (specList[sp].mw * sumMole)
            moleFrac.append(X)
    else:
        moleFrac = nums[:]
    
    # calculate elements in each fuel
    print 'Mole fractions of reactants:'
    sumC = 0.0
    sumH = 0.0
    sumO = 0.0
    for sp, X in zip(specs, moleFrac):
        print '{:.4f} '.format(X) + sp
        
        sumC = sumC + (X * specList[sp].numC)
        sumH = sumH + (X * specList[sp].numH)
        sumO = sumO + (X * specList[sp].numO)
    
    # count O atoms
    countO = 0.5 * ((2.0 * sumC) + (0.5 * sumH) - sumO)
    
    print '{:.4f} o2'.format(countO)
    print '{:.4f} n2'.format(countO * 3.76)
    
    # get mole fractions of products
    print ''
    print '{:.4f} co2'.format(sumC)
    print '{:.4f} h2o'.format(0.5 * sumH)
    print '{:.4f} n2'.format(countO * 3.76)


def moleToVol():
    """Calculates volume fractions from mole fractions.
    """
    
    print 'Enter species followed by mole fraction (e.g., nc7h16 0.2)'
    print 'Hit return when complete.'
    
    specs = []
    nums = []
    while True:
        sp = None
        num = None
        while not num:
            try:
                line = raw_input('Entry: ')
                if not line: break
                sp, num = line.split()
                num = float(num)
                
                # check if species in list
                density = specList[sp].density
            except ValueError:
                print 'Number invalid'
            except KeyError:
                print 'Error: species ' + sp + ' not found.'
        if not sp: break
        
        #num = num / specList[sp].density
        
        specs.append(sp)
        nums.append(num)
    
    # calculate volume fractions
    moleFrac = nums[:]
    
    sumMole = 0.0
    for sp, X in zip(specs, moleFrac):
        sumMole = sumMole + (X * specList[sp].mw)
    
    # get mass fraction divided by density
    massFrac = []
    for sp, X in zip(specs, moleFrac):
        Y = (X * specList[sp].mw) / sumMole
        
        massFrac.append(Y / specList[sp].density)
    
    volFrac = [n / sum(massFrac) for n in massFrac]
    
    print 'Volume fractions:'
    for sp, n in zip(specs, volFrac):
        print '{:.4f} '.format(n) + sp
    


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) == 1:
        volToMole(False)
    elif len(sys.argv) == 2:
        if sys.argv[1].lower() == 'equil':
            volToMole(True)
        elif sys.argv[1].lower() == 'volume':
            moleToVol()
    else:
        print 'Incorrect number of arguments. Either zero or one (equil)'