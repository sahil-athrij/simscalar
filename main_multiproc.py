import argparse
import csv
import os
import pprint
import re
import subprocess
import multiprocessing
from multiprocessing import Process

parser = argparse.ArgumentParser(
    prog='Simple Scalar Simulation Generator',
    description='allow you to run simple scalar benchmarks with different'
                ' input and benchmark files and different architecture modes'
                ' put the architechture and options in comma separated format'
                ' in a file called options for each model for example \n'
                ' sim-outorder,-bpred:2lev 1 512 4 0\n'
                ' put the bench_marks in a file called bench_marks in the same'
                ' folder.\n'
                ' put the cli input files (if any) into a file called cli_input'
                ' in the same folder',
    epilog='call for help')

parser.add_argument('-i', '--input', default='inputs', help='input directory location')
parser.add_argument('-o', '--output', default='output', help='output directory location')

args = parser.parse_args()

options = open(os.path.join(args.input, 'options')).readlines()
bench_marks = open(os.path.join(args.input, 'bench_mark')).readlines()
cli_input = open(os.path.join(args.input, 'cli_input')).readlines()


def expandvars(path, default=None, skip_escaped=False):
    """Expand environment variables of form $var and ${var}.
       If parameter 'skip_escaped' is True, all escaped variable references
       (i.e. preceded by backslashes) are skipped.
       Unknown variables are set to 'default'. If 'default' is None,
       they are left unchanged.
    """

    def replace_var(m):
        return os.environ.get(m.group(2) or m.group(1), m.group(0) if default is None else default)

    reVar = (r'(?<!\\)' if skip_escaped else '') + r'\$(\w+|\{([^}]*)\})'
    return re.sub(reVar, replace_var, path)


required_fields_outorder = [
    'sim_total_insn',
    'sim_total_refs',
    'sim_num_insn',
    'sim_num_refs',
    'sim_total_branches',
    'sim_cycle',
    'sim_CPI',
    'pred_miss_rate',
    'il1.miss_rate',
    'dl1.miss_rate',
    'ul2.miss_rate',
    'mem.page_mem'
]
required_fields_fast = [
    'sim_num_insn',
    'mem.page_mem'
]
required_fields_cache = [
    'sim_num_insn',
    'sim_num_refs',
    'il1.miss_rate',
    'dl1.miss_rate',
    'mem.page_mem',

]

required = {
    'sim-fast': required_fields_fast,
    'sim-cache': required_fields_cache,
    'sim-outorder': required_fields_outorder
}

extra_header = [
    'model',
    'bench mark',
    'parameters',
]


def process_info(stat_dict, required_fields):
    results = {}
    for i in required_fields:
        results[i] = stat_dict[i]
    return results


def main(option):
    option = option.strip()
    print(option)

    csv_all = os.path.join(args.output, 'out.csv')
    csv_global = open(csv_all, 'a')
    writer_global = csv.DictWriter(csv_global, fieldnames=extra_header + required_fields_outorder)
    dir_path = os.path.join(args.output, option).strip().replace(':', ' ')

    os.makedirs(dir_path, exist_ok=True)
    file_path_csv = os.path.join(dir_path, 'out.csv')
    csvfile = open(file_path_csv, 'w')
    option_lst = option.strip().split(',')

    model = option_lst[0]
    b_pred_type = 'bimod'
    if len(option_lst) > 1:
        extra_options = option_lst[1:]
        for opt in extra_options:
            if '-bpred' in opt:
                b_pred_type = opt.split()[0].split(':')[1]
    else:
        extra_options = []

    writer = csv.DictWriter(csvfile, fieldnames=extra_header + required[model])
    writer.writeheader()

    for num, test in enumerate(bench_marks):
        input_file = '' if num >= len(cli_input) else cli_input[num].strip()
        bench_mark_name = test.split()[0].split('/')[-1]
        bench_mark_name_file = bench_mark_name.split(".")[0]
        out_result_file = os.path.join(dir_path, f'{bench_mark_name_file}.txt')
        out_sim_file = os.path.join(dir_path, f'{bench_mark_name_file}_sim.txt')
        test = test.strip()
        print(test)
        print(input_file)
        final_cmd = option_lst + [test]
        if input_file:
            result = subprocess.run([' '.join(final_cmd)], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    stdin=open(expandvars(input_file)), shell=True)
        else:
            result = subprocess.run([' '.join(final_cmd)], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    shell=True)

        with open(out_result_file, 'w') as f:
            f.write(result.stdout.decode())
        with open(out_sim_file, 'w') as f:
            f.write(result.stderr.decode())
        sim_results = result.stderr.decode().split('sim: ** simulation statistics **')
        sim_results_list = sim_results[-1].strip().split('\n')

        stat_dict = {}
        for data in sim_results_list:
            if data:
                stat_name, stat_data = data.split(' # ')[0].split()
                stat_dict[stat_name] = stat_data

        if model == 'sim-outorder':
            stat_dict['pred_miss_rate'] = float(stat_dict[f'bpred_bimod.misses']) / float(
                stat_dict[f'bpred_bimod.lookups'])
        stat_final = process_info(stat_dict, required[option_lst[0]])
        stat_final['model'] = model
        stat_final['bench mark'] = bench_mark_name
        stat_final['parameters'] = ' '.join(extra_options)

        writer.writerow(stat_final)
        writer_global.writerow(stat_final)


if __name__ == '__main__':
    csv_all1 = os.path.join(args.output, 'out.csv')
    csv_global1 = open(csv_all1, 'a')
    writer_global1 = csv.DictWriter(csv_global1, fieldnames=extra_header + required_fields_outorder)
    writer_global1.writeheader()
    p = multiprocessing.Pool(6)
    with p:
        p.map(main, options)
