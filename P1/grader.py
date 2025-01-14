import json
import subprocess
import sys
import graderUtil

total_score = 0

for i in range(4):
    task_file_base = "task_" + str(i) + "_"
    for j in range(2):
        if (i >= 2) & (j == 0):
            continue
        task_file = task_file_base + str(j) + ".txt"
        cmd = [graderUtil.py_command, graderUtil.py_code, task_file]
        cmd = " ".join(cmd)
        print(cmd)
        
        # Run the submmision.py by tasks
        try:
            #p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, err = p.communicate()
            if err:
                raise Exception(err.strip())
        except OSError as e:
            print(e.errno)
        except:
            #print("Unexpected error:", sys.exc_info())
            print(sys.exc_info()[0])
        #output, err = p.communicate()     
        else:
            result = output.decode("utf-8")
            result = [x for x in result.split("\n") if x]
            result = result[-1]
            # Check the result format
            print(result)
            try:
                is_pass = graderUtil.check_format(i, j, result)
                if not is_pass:
                    print("\tYour result format is not correct!")
                    continue
            except:
                print(sys.exc_info()[0]) 

            # Verify the result
            try:
                result = json.loads(result)
            except ValueError as e:
                #print(sys.exc_info()[0])
                pass
            else:
                answers = graderUtil.load_answer_file("answer.txt")
                if i <= 3:
                #if i <= 1:
                    is_pass, total_score = graderUtil.verify_result(task_file, answers[task_file], i, j, result, total_score)
                    if is_pass:
                        print(task_file + " -- pass! current score: " + str(total_score))
                    print()
                else:
                    print("\ton-line testing ... ", result)

print("Totla Score: ", total_score)
