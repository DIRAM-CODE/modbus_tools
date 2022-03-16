# enum for metter_types
from enum import Enum

class MetterTypes(Enum):
    """Enumeracion para acotar los tipos de medidores soportados
    """
    G4 = 'G4'
    G4G3 = 'G4G3'
    PBB = 'PBB'

class RegName(Enum):
    """ 'Register Name' Estandarizacion de nombres y registros a leer para medidores PureBB y G44XX
    """
    
    V1N = 'V1N',
    I1 = 'I1',
    V3N = 'V3N',
    I3 = 'I3',
    V2N = 'V2N',
    I2 = 'I2',
    V23 = 'V23',
    V12 = 'V12',
    V31 = 'V31',
    P1 = 'P1',
    P3 = 'P3',
    P2 = 'P2',
    PT = 'PT',
    Q1 = 'Q1',
    Q3 = 'Q3',
    Q2 = 'Q2',
    QT = 'QT',
    S1 = 'S1',
    S3 = 'S3',
    S2 = 'S2',
    ST = 'ST',
    PF1 = 'PF1',
    PF3 = 'PF3',
    PF2 = 'PF2',
    PFT = 'PFT',
    EPinT = 'EPinT',
    EPoutT = 'EPoutT',
    EQinT = 'EQinT',
    EQoutT = 'EQoutT',
    PST23 = 'PST23',
    PST12 = 'PST12',
    PST31 = 'PST31',
    THDI1 = 'THDI1',
    THDI3 = 'THDI3',
    THDI2 = 'THDI2',
    V1pos = 'V1pos',
    I1pos = 'I1pos',
    V1neg = 'V1neg',
    I1neg = 'I1neg',
    V1zero = 'V1zero',
    I1zero = 'I1zero',
    # hI1 = 'hI1', # I1 Subgroup Harmonics 1-50th
    # hI2 = 'hI2',
    # hI3 = 'hI3'

class RegMapping():    

    PBB_h1_group = [
        'hI1_0',
        'hI1_1',
        'hI1_2',
        'hI1_3',
        'hI1_4',
        'hI1_5',
        'hI1_6',
        'hI1_7',
        'hI1_8',
        'hI1_9',
        'hI1_10',
        'hI1_11',
        'hI1_12',
        'hI1_13',
        'hI1_14',
        'hI1_15',
        'hI1_16',
        'hI1_17',
        'hI1_18',
        'hI1_19',
        'hI1_20',
        'hI1_21',
        'hI1_22',
        'hI1_23',
        'hI1_24',
        'hI1_25',
        'hI1_26',
        'hI1_27',
        'hI1_28',
        'hI1_29',
        'hI1_30',
        'hI1_31',
        'hI1_32',
        'hI1_33',
        'hI1_34',
        'hI1_35',
        'hI1_36',
        'hI1_37',
        'hI1_38',
        'hI1_39',
        'hI1_40',
        'hI1_41',
        'hI1_42',
        'hI1_43',
        'hI1_44',
        'hI1_45',
        'hI1_46',
        'hI1_47',
        'hI1_48',
        'hI1_49',
        'hI1_50'
    ]

    PBB_h2_group = [
        'hI2_0',
        'hI2_1',
        'hI2_2',
        'hI2_3',
        'hI2_4',
        'hI2_5',
        'hI2_6',
        'hI2_7',
        'hI2_8',
        'hI2_9',
        'hI2_10',
        'hI2_11',
        'hI2_12',
        'hI2_13',
        'hI2_14',
        'hI2_15',
        'hI2_16',
        'hI2_17',
        'hI2_18',
        'hI2_19',
        'hI2_20',
        'hI2_21',
        'hI2_22',
        'hI2_23',
        'hI2_24',
        'hI2_25',
        'hI2_26',
        'hI2_27',
        'hI2_28',
        'hI2_29',
        'hI2_30',
        'hI2_31',
        'hI2_32',
        'hI2_33',
        'hI2_34',
        'hI2_35',
        'hI2_36',
        'hI2_37',
        'hI2_38',
        'hI2_39',
        'hI2_40',
        'hI2_41',
        'hI2_42',
        'hI2_43',
        'hI2_44',
        'hI2_45',
        'hI2_46',
        'hI2_47',
        'hI2_48',
        'hI2_49',
        'hI2_50'
    ]

    PBB_h3_group = [
        'hI3_0',
        'hI3_1',
        'hI3_2',
        'hI3_3',
        'hI3_4',
        'hI3_5',
        'hI3_6',
        'hI3_7',
        'hI3_8',
        'hI3_9',
        'hI3_10',
        'hI3_11',
        'hI3_12',
        'hI3_13',
        'hI3_14',
        'hI3_15',
        'hI3_16',
        'hI3_17',
        'hI3_18',
        'hI3_19',
        'hI3_20',
        'hI3_21',
        'hI3_22',
        'hI3_23',
        'hI3_24',
        'hI3_25',
        'hI3_26',
        'hI3_27',
        'hI3_28',
        'hI3_29',
        'hI3_30',
        'hI3_31',
        'hI3_32',
        'hI3_33',
        'hI3_34',
        'hI3_35',
        'hI3_36',
        'hI3_37',
        'hI3_38',
        'hI3_39',
        'hI3_40',
        'hI3_41',
        'hI3_42',
        'hI3_43',
        'hI3_44',
        'hI3_45',
        'hI3_46',
        'hI3_47',
        'hI3_48',
        'hI3_49',
        'hI3_50'
    ]

    PBB = {
        RegName.V1N.name: 'V1N',
        RegName.I1.name: 'I1',
        RegName.V3N.name: 'V3N',
        RegName.I3.name: 'I3',
        RegName.V2N.name: 'V2N',
        RegName.I2.name: 'I2',
        RegName.V23.name: 'V23',
        RegName.V12.name: 'V12',
        RegName.V31.name: 'V31',
        RegName.P1.name: 'P1',
        RegName.P3.name: 'P3',
        RegName.P2.name: 'P2',
        RegName.PT.name: 'PT',
        RegName.Q1.name: 'Q1',
        RegName.Q3.name: 'Q3',
        RegName.Q2.name: 'Q2',
        RegName.QT.name: 'QT',
        RegName.S1.name: 'S1',
        RegName.S3.name: 'S3',
        RegName.S2.name: 'S2',
        RegName.ST.name: 'ST',
        RegName.PF1.name: 'PF1',
        RegName.PF3.name: 'PF3',
        RegName.PF2.name: 'PF2',
        RegName.PFT.name: 'PFT',
        RegName.EPinT.name: 'EPinT',
        RegName.EPoutT.name: 'EPoutT',
        RegName.EQinT.name: 'EQinT',
        RegName.EQoutT.name: 'EQoutT',
        RegName.PST23.name: 'PST23',
        RegName.PST12.name: 'PST12',
        RegName.PST31.name: 'PST31',
        RegName.THDI1.name: 'THDI1',
        RegName.THDI3.name: 'THDI3',
        RegName.THDI2.name: 'THDI2',
        RegName.V1pos.name: 'V1pos',
        RegName.I1pos.name: 'I1pos',
        RegName.V1neg.name: 'V1neg',
        RegName.I1neg.name: 'I1neg',
        RegName.V1zero.name: 'V1zero',
        RegName.I1zero.name: 'I1zero',
        # RegName.hI1.name: PBB_h1_group, # I1 Subgroup Harmonics 1-50th #TODO decidir como incluir armonicos
        # RegName.hI2.name: PBB_h2_group,
        # RegName.hI3.name: PBB_h3_group
    }

def sort_regs_to_read(regsToRead, jsonRegs):
    """ Simple 'bubble sort' from: https://realpython.com/sorting-algorithms-python/#the-bubble-sort-algorithm-in-python

    Args:
        array (list(str)): unsorted array

    Returns:
        list(str): sorted array
    """

    n = len(regsToRead)

    for i in range(n):
        # Create a flag that will allow the function to
        # terminate early if there's nothing left to sort
        already_sorted = True

        # Start looking at each item of the list one by one,
        # comparing it with its adjacent value. With each
        # iteration, the portion of the array that you look at
        # shrinks because the remaining items have already been
        # sorted.
        for j in range(n - i - 1):
            
            ind = j
            ind_adjacent = j + 1

            reg = list(filter(lambda r: r['name'] == regsToRead[ind], jsonRegs))
            if len(reg) > 1:
                print('ERROR en modbus_tools/utils.py / sort_regs_to_read()')
            regInd = reg[0]['memory_block_adress']
            reg_adjacent = list(filter(lambda r: r['name'] == regsToRead[ind_adjacent], jsonRegs))
            if len(reg_adjacent) > 1:
                print('ERROR en modbus_tools/utils.py / sort_regs_to_read()')
            regInd_adjacent = reg_adjacent[0]['memory_block_adress']

            if regInd > regInd_adjacent: # regsToRead[ind] > regsToRead[ind_adjacent]:
                # If the item you're looking at is greater than its
                # adjacent value, then swap them
                regsToRead[ind], regsToRead[ind_adjacent] = regsToRead[ind_adjacent], regsToRead[ind]

                # Since you had to swap two elements,
                # set the `already_sorted` flag to `False` so the
                # algorithm doesn't finish prematurely
                already_sorted = False

        # If there were no swaps during the last iteration,
        # the array is already sorted, and you can terminate
        if already_sorted:
            break

    return regsToRead
