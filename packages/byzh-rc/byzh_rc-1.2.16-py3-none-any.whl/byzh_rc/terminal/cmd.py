import subprocess
def BRunCmd(*args, show=True):
    '''
    可传入多个字符串, 在cmd中运行
    :param args:
    :param show: 若show=True, 则会单开一个cmd, 在cmd中运行
    :return:
    '''
    command = ''
    for i in range(len(args)):
        if i == len(args) - 1:
            command += str(args[i])
            break
        command += str(args[i]) + ' && '
    if show:
        command = f'start cmd /K "{command}"'
    # print(command)
    subprocess.run(command, shell=True)

def BRunPython(*args):
    '''
    可传入多个字符串, 在当前python环境下运行
    :param args: 以python开头, 用于运行.py文件
    :param show:
    :return:
    '''
    for string in args:
        command_lst = string.split(' ')
        subprocess.run(command_lst)

    print("BRunPython结束:")
    for string in args:
        print("\t"+string)

if __name__ == '__main__':
    BRunCmd("echo hello","echo world","echo awa", show=True)
    # BRunPython("python E:\\byzh_workingplace\\test1.py")