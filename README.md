vol-to-mole
===========

Converts volume fractions of liquid hydrocarbon mixtures to molar fractions. Also supports calculating the equilibrium composition given reactant mole fractions. The mole fractions of the fuel components, plus oxygen and nitrogen at stoichiometric conditions, are reported as results.

Currently supports the following species:

 * n-heptane (nc7h16)
 * iso-octane (ic8h18)
 * toluene (c6h5ch3)
 * n-decane (nc10h22)
 * n-dodecane (nc12h26)
 * n-hexadecane (cetane, nc16h34)
 * iso-cetane (hmn, ic16h34)
 * n-propylbenzene (nc9h12, c6h5ch2ch2ch3)
 * mesitylene (c6h3(ch3)3)
 * methyl decanoate (md, methyl caprate, c11h22o2)
 * 2-pentene (c5h10-2)
 * 1-hexene (c6h12-1)
 * methanol (ch3oh)
 * ethanol (c2h5oh)
 * propanol (c3h7oh)
 * n-butanol (c4h9oh)
 * isobutanol (2-methyl-1-propanol)

Usage
-------

From the command line, use `python vol-to-mole.py` for converting volume fraction to mole fraction. Or, if only obtaining the equilibrium composition is desired, use `python vol-to-mole.py equil`.

At the prompt, enter the reactant species names and volume (or mole) fractions: e.g., `nc7h16 0.2`.

License
-------

`vol-to-mole` is released under the modified BSD license, see LICENSE for details.

Author
------

Created by [Kyle Niemeyer](http://kyleniemeyer.com). Email address: [kyle.niemeyer@gmail.com](mailto:kyle.niemeyer@gmail.com)
