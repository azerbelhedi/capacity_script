import re
import os

structures = ['BEA', 'BEB', 'BEC', 'EMT', 'ITT', 'ISV',
              'FAU_1', 'FAU_2', 'FAU_3', 'IRR_1', 'IRR_2', 'SAO']
f_keyword = 'F= '
toten_keyword = 'TOTEN  =     '
selected_index = 7

empty_framework_lookup_table = [-2128.77756025, -1915.22192918, -923.01584230, 0, 0, 0, -1676.15891242, -1469.26608210]

selected_structure = structures[selected_index]
keyword = toten_keyword
target_file = 'OUTCAR'

def EnergyDFTsingle(working_dir):
    logfile = os.path.join(working_dir, target_file)

    # read VASP logfile
    with open(logfile, 'r') as f:
        lines = f.readlines()

    # print(f'file:{logfile}' )

    # convergence check
    """ if 'reached required accuracy' not in lines[-1]:
        raise Exception('job {} not converge'.format(job)) """

    # extract energy
    for line in lines[::-1]:
        # print(f'keyword: {keyword}, {keyword in line} ')
        if keyword in line:
            str_to_search = ''
            if(keyword == f_keyword):
                str_to_search = r'(?<={})[-+]?([0-9]+)?\.?[0-9]*[Ee](?:\ *[-+]?\ *[0-9]+)?'.format(
                keyword)
            else:
                str_to_search = r'(?<={})[-+]?([0-9]+)?\.?[0-9]*[Ee]?'.format(
                keyword)
            match = re.search(str_to_search, line)
            print(f'match group: {match.group()}')
            energy = float(match.group())

            # return result
            return energy  # calculate single Na energy


def EnergyDFT(working_dir):

    result_DFT = {}
        
    for job in os.listdir(working_dir):
        logfile = os.path.join(working_dir, job, target_file)
        print(f'Checking {logfile}')
        if(selected_structure not in job):
            continue

        # inserted atoms
        inserted_atoms_str = job.split('Na')[1]
        if inserted_atoms_str == '':
            inserted_atoms = 1
        else:
            inserted_atoms = int(inserted_atoms_str)

        # read VASP logfile
        with open(logfile, 'r') as f:
            lines = f.readlines()

        # convergence check
        # if 'reached required accuracy' not in lines[-1]:
            # not converged, skip
        #     continue

        # extract energy
        for line in lines[::-1]:
            if keyword in line:
                str_to_search = ''
                if(keyword == f_keyword):
                    str_to_search = r'(?<={})[-+]?([0-9]+)?\.?[0-9]*[Ee](?:\ *[-+]?\ *[0-9]+)?'.format(
                    keyword)
                else:
                    str_to_search = r'(?<={})[-+]?([0-9]+)?\.?[0-9]*[Ee]?'.format(
                    keyword)
                match = re.search(str_to_search, line)
                print(f'energy string{match.group()}')
                energy = float(match.group())
                break

        # save results to dictionary
        result_DFT[inserted_atoms] = energy

    # return sorted inserted atoms and energy
    # return result_DFT
    return dict(sorted(result_DFT.items()))


SingleAtomEnergyNa = -23.49398145 / 16
print(f'single Na energy: {SingleAtomEnergyNa}')
# discover strcutres of a single framework: name and path for logfile (E)

# calculate empy framework energy
# energyC = EnergyDFTsingle(os.path.join('results_C', selected_structure))
energyC = empty_framework_lookup_table[selected_index]
print(f'energy in empty c framework: {energyC}')

# calculate structure energy
energyC_Na = EnergyDFT(".")
# print(energyC_Na)
# print(f'energy in structure: {energyC_Na}')
# calculate pot for every structure

# calculate pot for every structure
# pot = -(energyC_Na- energyC - 4*SingleAtomEnergyNa)/4
# print(f'pot: {pot}')

for key in energyC_Na.keys():
    # print(energyC_Na[key])
    nb_Na = key
    pot = -(energyC_Na[key] - energyC - nb_Na*SingleAtomEnergyNa)/nb_Na
    print(f'energy capacity structure: Na: {nb_Na}: {pot}')

