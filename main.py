import os
import timeit
import argparse

import pandas as pd 

from diffPrivacy import diffPrivacy

def get_arguments():
    parser = argparse.ArgumentParser(description='Argparse in DP_algorithms')
    parser.add_argument('--file', '-f', 
                    type=str, 
                    required = True, 
                    help='csv file for apply DP_algorithm')
    
    parser.add_argument('--epsilon', '-e', type=int, 
                    help='Epsilon for DP',
                    default = 10)
    
    parser.add_argument('--categorical', '-c', type=str, nargs='+',
                    help='categorical variable in csv file')

    args = parser.parse_args()
    epsilon, filename,  categorical_list = args.epsilon, args.file,args. categorical
    return epsilon, filename, categorical_list

def read_file(filename, id = False):
    #return pd.read_csv(filename).iloc[:100,:]
    return pd.read_csv(filename)

def create_folder(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def make_write_filename(read_filename, flag, epsilon):
    point_idx = read_filename.index(".")
    return f"{read_filename[:point_idx]}_{flag}_{epsilon}.csv"

def write_file(df, filename):
    df.to_csv(filename)

def write_outcomes(filename, epsilon, dp):
    output_path = "./outcome/"
    create_folder(output_path)

    write_filename = make_write_filename(filename, "norm", epsilon)
    write_file(dp.new_df, output_path + write_filename)
    
    write_filename = make_write_filename(filename, "DP", epsilon)
    write_file(dp.new_unnorm_df, output_path + write_filename)

if __name__ == "__main__":
    
    start = timeit.default_timer()
    
    epsilon, filename, categorical_list = get_arguments()
    method = "PM"

    raw_data = read_file(filename, False)
    
    # raw_data[categorical_list] = raw_data[categorical_list].apply(pd.Categorical)
    if categorical_list:
        raw_data[categorical_list] = raw_data[categorical_list].apply(pd.Categorical)
    
    ## Apply Differential Privacy
    dp = diffPrivacy(epsilon, raw_data, method) ## epsilon, matrix, method
    # Output file save
    write_outcomes(filename, epsilon, dp)

    # 실행 코드
    stop = timeit.default_timer()

    print(f"Total Time the algorithm spent:{stop - start}s")
