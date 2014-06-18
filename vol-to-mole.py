#! /usr/bin/env python
# coding: utf-8
""" Converts hydrocarbon mixture volume fractions to mole fractions.

Unless otherwise indicated, species molecular weights and densities
were obtained using _Yaws' Handbook of Physical Properties for
Hydrocarbons and Chemicals_ at standard conditions (25°C and 1 atm).
"""

from __future__ import print_function, division

import sys
from collections import namedtuple

# density in units kg/m^3
Species = namedtuple('Species', 'mw, CAS, density, numC, numH, numO')
spec_list = {}
spec_list.update(dict.fromkeys(
                ['nc7h16', 'n-heptane'], 
                Species(100.204, '142-82-5', 682., 7, 16, 0)))
spec_list.update(dict.fromkeys(
                ['ic8h18', 'iso-octane', '2,2,4-trimethylpentane'], 
                Species(114.231, '540-84-1', 69.e1, 8, 18, 0)))
spec_list.update(dict.fromkeys(
                ['c6h5ch3', 'toluene'], 
                Species(92.1405, '108-88-3', 865., 7, 8, 0)))
spec_list.update(dict.fromkeys(
                ['nc9h12', 'n-propylbenzene'],
                Species(120.194, '103-65-1', 86.e1, 9, 12, 0)))
spec_list.update(dict.fromkeys(
                ['nc10h22', 'n-decane'],
                Species(142.285, '124-18-5', 728.0, 10, 22, 0)))
spec_list.update(dict.fromkeys(
                ['nc12h26', 'n-dodecane'], 
                Species(170.338, '112-40-3', 745.0, 12, 26, 0)))
spec_list.update(dict.fromkeys(
                ['nc16h34', 'n-hexadecane', 'cetane'], 
                Species(226.446, '544-76-3', 770.0, 16, 34, 0)))
spec_list.update(dict.fromkeys(
                ['ic16h34', 'hmn', 'iso-cetane', 
                '2,2,4,4,6,8,8-heptamethylnonane'], 
                Species(226.446, '4390-04-9', 772.2, 16, 34, 0)))
spec_list.update(dict.fromkeys(
                ['c6h3(ch3)3', 'mesitylene'],
                Species(120.194, '108-67-8', 861., 9, 12, 0)))
spec_list.update(dict.fromkeys(
                ['md', 'methyl decanoate', 'c11h22o2', 'methyl caprate'], 
                Species(186.294, '110-42-9', 873.0, 11, 22, 2)))
spec_list.update(dict.fromkeys(
                ['c5h10-2', '2-pentene', 'trans-2-pentene'], 
                Species(70.1344, '646-04-8', 643., 5, 10, 0)))
spec_list.update(dict.fromkeys(
                ['c6h12-1', 'c6h12-1', '1-hexene'], 
                Species(84.1613, '592-41-6', 667., 6, 12, 0)))

# alcohols
spec_list.update(dict.fromkeys(
                ['ch4o', 'ch3oh', 'methanol', 'methyl alcohol'], 
                Species(32.0422, '67-56-1', 787., 1, 4, 1)))
spec_list.update(dict.fromkeys(
                ['c2h6o', 'c2h5oh', 'ethanol', 'ethyl alcohol'], 
                Species(46.0684, '64-17-5', 787., 2, 6, 1)))
spec_list.update(dict.fromkeys(
                ['c3h8o', 'c3h7oh', 'propanol', '1-propanol',
                'propyl alcohol'], 
                Species(60.0959, '71-23-8', 802., 3, 8, 1)))
spec_list.update(dict.fromkeys(
                ['c4h10o', 'c4h9oh', 'n-butanol', '1-butanol', 'isobutanol'],
                Species(74.1228, '71-36-3', 806., 4, 10, 1)))
spec_list.update(dict.fromkeys(
                ['isobutanol', '2-methyl-1-propanol', 'isobutyl alcohol'],
                Species(74.1228, '78-83-1', 797., 4, 10, 1)))


def volToMole(equil):
    """Calculates molar fractions from volume fractions.
    
    equil: True if just equilibrium calculation
    """
    
    if equil:
        print('Enter species followed by mole fraction (e.g., nc7h16 0.2)')
    else:
        print('Enter species followed by volume fraction (e.g., nc7h16 0.2)')
    print('Hit return when complete.')
    
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
                density = spec_list[sp].density
            except ValueError:
                print('Number invalid')
                num = None
            except KeyError:
                print('Error: species ' + sp + ' not found.')
                sp = None
                num = None
        if not sp: break
        
        # get molecular weight and density
        if not equil:
            num = num * spec_list[sp].density
        
        specs.append(sp)
        nums.append(num)
    
    # need to calculate mass and mole fractions if starting with volume
    if not equil:
        massFrac = nums[:]
        massFrac = [n / sum(massFrac) for n in massFrac]
        
        sumMole = 0.0
        for sp, Y in zip(specs, massFrac):
            sumMole = sumMole + (Y / spec_list[sp].mw)
        
        moleFrac = []
        for sp, Y in zip(specs, massFrac):
            X = Y / (spec_list[sp].mw * sumMole)
            moleFrac.append(X)
    else:
        moleFrac = nums[:]
    
    # calculate elements in each fuel
    print('Mole fractions of reactants:')
    sumC = 0.0
    sumH = 0.0
    sumO = 0.0
    for sp, X in zip(specs, moleFrac):
        print('{:.4f} '.format(X) + sp)
        
        sumC = sumC + (X * spec_list[sp].numC)
        sumH = sumH + (X * spec_list[sp].numH)
        sumO = sumO + (X * spec_list[sp].numO)
    
    # count O atoms
    countO = 0.5 * ((2.0 * sumC) + (0.5 * sumH) - sumO)
    
    print('{:.4f} o2'.format(countO))
    print('{:.4f} n2'.format(countO * 3.76))
    
    # get mole fractions of products
    print('')
    print('{:.4f} co2'.format(sumC))
    print('{:.4f} h2o'.format(0.5 * sumH))
    print('{:.4f} n2'.format(countO * 3.76))


def moleToVol():
    """Calculates volume fractions from mole fractions.
    """
    
    print('Enter species followed by mole fraction (e.g., nc7h16 0.2)')
    print('Hit return when complete.')
    
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
                density = spec_list[sp].density
            except ValueError:
                print('Number invalid')
            except KeyError:
                print('Error: species ' + sp + ' not found.')
        if not sp: break
        
        #num = num / spec_list[sp].density
        
        specs.append(sp)
        nums.append(num)
    
    # calculate volume fractions
    moleFrac = nums[:]
    
    sumMole = 0.0
    for sp, X in zip(specs, moleFrac):
        sumMole = sumMole + (X * spec_list[sp].mw)
    
    # get mass fraction divided by density
    massFrac = []
    for sp, X in zip(specs, moleFrac):
        Y = (X * spec_list[sp].mw) / sumMole
        
        massFrac.append(Y / spec_list[sp].density)
    
    volFrac = [n / sum(massFrac) for n in massFrac]
    
    print('Volume fractions:')
    for sp, n in zip(specs, volFrac):
        print('{:.4f} '.format(n) + sp)


if __name__ == "__main__":
    
    if len(sys.argv) == 1:
        volToMole(False)
    elif len(sys.argv) == 2:
        if sys.argv[1].lower() == 'equil':
            volToMole(True)
        elif sys.argv[1].lower() == 'volume':
            moleToVol()
    else:
        print('Incorrect number of arguments. Either zero or one (equil)')