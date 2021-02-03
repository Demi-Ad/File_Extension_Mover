import os
import os.path
import shutil
from datetime import datetime


def File_Deep_Search(path):

    File_List = []
    File_Extensions = []

    for (Root, Path, Files) in os.walk(path):
        for File in Files:
            File_List.append(os.path.join(Root, File))
            File_Extensions.append(File.split('.')[-1])

    return File_List, set(File_Extensions), File_Extensions


def File_Search(path):

    File_List = []
    File_Extensions = []

    for File in os.listdir(path):
        if os.path.isfile(os.path.join(path, File)) == True:
            File_List.append(File)
            File_Extensions.append(File.split('.')[-1])

    return File_List, set(File_Extensions), File_Extensions


def Extension_Filter(File_Extension, Input_Extension):
    temp = []
    for i in File_Extension:
        for j in Input_Extension:
            if i == j:
                temp.append(i)

    return temp


def create_folder(path, Extensions):
    Path_re = []
    for Extension in Extensions:
        try:
            if not os.path.exists(os.path.join(path, Extension)):
                os.makedirs(os.path.join(path, Extension))
                Path_re.append(os.path.join(path, Extension))
            else:
                Path_re.append(os.path.join(path, Extension))
        except:
            pass
    return Path_re


def File_Mover(path, File_List, Extension_Path):
    count = 1
    Result_Time = datetime.today().strftime("%Y%m%d%H%M%S")
    Result_Name = 'result_{0}{1}'.format(Result_Time, '.txt')
    Result = open(os.path.join(path, Result_Name), 'a')
    Result_Text = ' - - - - > '

    for File in File_List:
        
        for Extension in Extension_Path:

            if File.split('\\')[-1].split('.')[-1] == Extension.split('\\')[-1]:

                if os.path.isfile(os.path.join(Extension, File.split('\\')[-1])):

                    Ex_Temp = Extension + '\\' + File.split('\\')[-1].split(
                        '.')[0] + '(' + str(count) + ')' + '.' + File.split('\\')[-1].split('.')[1]
                    shutil.move(File, Ex_Temp)
                    Result.writelines(File + Result_Text+Ex_Temp+'\n')
                    count += 1

                else:
                    shutil.move(File, Extension)
    Result.close()


def main(Path, Deep_flag):

    Files_List = []
    File_Extension = []

    if Deep_flag == True:
        Files_List, File_Extension, temp_list = File_Deep_Search(Path)
    else:
        Files_List, File_Extension, temp_list = File_Search(Path)

    print("- - - Get Extensions - - -\n")
    for i in File_Extension:
        print(i, temp_list.count(i), sep=' : ')

    Input_Extension = input('\n정리할 확장자를 입력해주세요(Enter is All) : ').split(' ')

    if Input_Extension[0] == '' and len(Input_Extension) == 1:
        pass
    else:
        File_Extension = Extension_Filter(File_Extension, Input_Extension)

    Path_re = create_folder(path=Path, Extensions=File_Extension)

    File_Mover(Path, Files_List, Path_re)


if __name__ == '__main__':
    Input_Path = input('경로를 입력해주세요 : ')

    while True:
        Deep_Scan_Flag = None
        Deep_Scan_Check = input('폴더 전체를 탐색할까요? Y/N : ').upper()
        if Deep_Scan_Check == 'Y':
            Deep_Scan_Flag = True
            break
        elif Deep_Scan_Check == 'N':
            Deep_Scan_Flag = False
            break
        else:
            print('Y/N 둘중 하나를 입력해주세요')

    main(Path=Input_Path, Deep_flag=Deep_Scan_Flag)
    print('작업완료')
