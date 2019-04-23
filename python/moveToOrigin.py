#moveToOrigin.py

import pymel.core as pm

obj = pm.selected()

box = pm.exactWorldBoundingBox(obj)
bottom = [(box[0]+ box[3])/2, box[1], (box[2] + box[5])/2]
pm.xform( obj, piv=bottom, ws=True )
pm.move( 0, 0, 0, obj, rpr=True, ws=True )
pm.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
