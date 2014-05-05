'''
Created on May 5, 2014

@author: perk
'''
import ROI

p = 677557.0
r = 2842.0
deal = ROI.Deal('SM', p, 0.8, 0.02*p , 67.0, 9.0, r, 0.0, 515.30, 21.872, 4.1, 30, 100.0, 1)

print(deal)

for y in [1, 5, 10, 20, 40]:
    roi = deal.ROIatYear(y,2.0)
    print(roi)

