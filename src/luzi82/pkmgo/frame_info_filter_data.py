from luzi82.pkmgo import common as vcommon

COMMON_NUMBER_TXT_REPLACE_DICT={
    'O':'0',
    'l':'1',
    'A':'4',
    'S':'5',
    'Z':'2',
    '\u00e9':'6',
}

CP_TXT_REPLACE_DICT=vcommon.combine_dict([
    COMMON_NUMBER_TXT_REPLACE_DICT,
    {
        '@':'CP'
    }
])

HP_TXT_REPLACE_DICT=vcommon.combine_dict([
    COMMON_NUMBER_TXT_REPLACE_DICT,
    {
        ' /':'/',
        '/ ':'/',
        'P ':'P',
    }
])

POWERUP_STARDUST_TXT_REPLACE_DICT=COMMON_NUMBER_TXT_REPLACE_DICT

POWERUP_CANDY_TXT_REPLACE_DICT=COMMON_NUMBER_TXT_REPLACE_DICT

CANDY_NAME_TXT_REPLACE_DICT={
    'NIDORAN9':'NIDORAN\u2640',
    'NIDORANd':'NIDORAN\u2642',
    'NIDORANo\u2018':'NIDORAN\u2642',
    'CI\u00a3FAIRY':'CLEFAIRY',
    'POUWAG':'POLIWAG',
    'GAST LY':'GASTLY',
    'CAN DY':'CANDY'
}
