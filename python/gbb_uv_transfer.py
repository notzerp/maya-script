# transferUv_v0.2
# WIP version
import pymel.core as pm

source_compareList = []
target_compareList = []

sel = pm.selected()
pm.delete(sel, ch=True)

if len(sel) != 2:
    pm.warning('Nope')

else:
    sGrpSel = sel[0]
    tGrpSel = sel[1]

    sourceGrp = pm.ls(sGrpSel, dag=True, s=True)
    for sourceGeo in sourceGrp:
        sGeoName = sourceGeo.split('|')[-1]
        source_compareList.append(sGeoName)

    targetGrp = pm.ls(tGrpSel, dag=True, s=True)
    for targetGeo in targetGrp:
        tGeoName = targetGeo.split('|')[-1]
        target_compareList.append(tGeoName)

    source_compareList.sort()
    target_compareList.sort()

    # print source_compareList
    # print target_compareList

    if source_compareList == target_compareList:
        pm.warning('Good stuff')

        for tItem in targetGrp:
            wtgDel = sourceGrp[0]
            pm.polyTransfer(tItem, uv=True, ao=wtgDel)
            sourceGrp.remove(wtgDel)
        pm.warning('All match, successfully transferred uv')

    else:
        pm.warning('Watch out, something does not match')
        for tItem in targetGrp:
            tItemName = tItem.split('|')[-1]
            if tItemName in source_compareList:
                for sItem in sourceGrp:
                    sItemName = sItem.split('|')[-1]
                    if sItemName == tItemName:
                        pm.polyTransfer(tItem, uv=True, ao=sItem)
                        # pm.delete(sel ,ch=True)
                    else:
                        pass
            else:
                pm.warning('Failed to perform uv transfer for {}'.format(tItemName))
                # add exception
                pass
