import os
import os.path
import shutil
import inspect
from re import search
from datetime import datetime


# 같은 이름의 폴더가 없으면 폴더 생성
def create_folder(args):
    try:
        if not os.path.exists(args):
            os.makedirs(args)
    except OSError:
        pass

# 확장자가 없는 파일 , 폴더 제외


def files_filter(x):
    if x.find('.') != -1:
        return x


def files_mover(target_dir, set_dir, filter_files):

    file_counter = 0  # 파일 이름이 중복될 경우 앞에 숫자
    result_time = datetime.today().strftime(
        "%Y%m%d%H%M%S")  # 결과 파일명으로 지정할 현재 날짜 , 시간을 구함
    file_name = '\\result_' + result_time + '.txt'
    file = open(target_dir + file_name, 'w')

    for move_dir in set_dir:
        for move_file in filter_files:
            if move_dir.split('\\')[-1] == move_file.split('.')[-1]:
                if os.path.isfile(move_dir + '\\' + move_file):  # 이동시킬 경로에 이름이 같은 파일이 있으면
                    shutil.move(target_dir+'\\'+move_file, move_dir + '\\' + '(' +
                                str(file_counter) + ')' + move_file)  # 파일명 앞에 (숫자) 붙여서 덮어쓰기 방지
                    print(target_dir+'\\'+move_file + ' - - - ----> ' +
                          move_dir + '\\' + '(' + str(file_counter) + ')' + move_file)
                    file_counter += 1  # 숫자 증가
                    file.writelines(target_dir+'\\'+move_file + '- - - - ->' +
                                    move_dir + '(' + str(file_counter) + ')' + move_file+'\n')
                else:
                    shutil.move(target_dir+'\\'+move_file,
                                move_dir + '\\' + move_file)  # 파일이동
                    print(target_dir+'\\'+move_file +
                          ' - - - ----> ' + move_dir + '\\' + move_file)
                    file.writelines(
                        target_dir+'\\'+move_file + '- - - - ->' + move_dir + '\\' + move_file + '\n')

    file.close()


def main(src, args,fullscan_flag):  # 정리할 경로 , 정리할 확장자들의 리스트
    files = []
    # 입력값이 '/' 이라면 현재 경로 아니면 입력한 경로
    if src == '/':

        
        target_dir = os.getcwd()  # 현재 경로를 입력
        is_me = inspect.getfile(inspect.currentframe()).split(
            '\\')[-1]  # 파일 자기 자신 경로

        if fullscan_flag == True:
            for (path , dir , file) in os.walk(target_dir):
                for i in file:
                    files.append(os.path.join(path, i))

        else:
            files = os.listdir(target_dir)  # 입력한 경로에 파일목록을 추출

        filter_files = [x for x in files if files_filter(x)]
        filter_files.remove(is_me)  # 자기자신은 이동x

    else:

        target_dir = src  # 정리할 경로를 입력

        if fullscan_flag == True:
            for (path , dir , file) in os.walk(target_dir):
                for i in file:
                    files.append(os.path.join(path, i))
        else:
            files = os.listdir(target_dir)  # 입력한 경로에 파일목록을 추출

        filter_files = [x for x in files if files_filter(x)]


    result = []  # 최종적으로 정리할 리스트


    if args[0] == '/':  # '/' 이라면 전부 정리
        result = filter_files
    else:
        for i in filter_files:
            for j in args:
                if search(str(j)+'$', i) != None:
                    result.append(i)
                    continue

    print('\n')
    print('Files List\n')
    print('------------------------------------------\n')
    for i in result[:]:
        print(i)
    print('------------------------------------------\n')

    while True:  # 최종확인을 받기위해 무한반복
        check = None  # 잘못된 입력을 방지하기위해 None 할당
        check = input('정리합니까? Y/N : ').upper()  # 소문자 대문자
        if check == 'Y':  # while문 탈출
            break
        elif check == 'N':  # main 함수 종료
            return
        else:
            print('다시입력하세요')
            pass

    extensions = []  # 확장자들이 있는 파일을 담을 리스트

    for i in result:
        # 확장자가 있는 파일들을 '.'으로 스플릿 후 2번째 확장자만 추출
        extensions.append(i.split('.')[1])

    set_extensions = set(extensions)  # 중복된 확장자가 있을 수 있으므로 set 화 시켜서 중복 제거

    set_dir = []  # 옮김 폴더의 경로를 담음

    for i in set_extensions:
        create_folder(target_dir + '\\' + str(i))  # 입력받은 주소를 기준으로 확장자명의 폴더 생성
        set_dir.append(target_dir + '\\' + str(i))  # 만든 폴더에 경로를 리스트 저장

    files_mover(target_dir, set_dir, result)


if __name__ == '__main__':

    print('- - - - File Extension Mover - - - -\n')
    src = input('정리할 폴더 경로를 입력해주세요 : ')
    args = list(map(str, input('정리할 확장자들을 입력해주세요 스페이스로 구분합니다 : ').split()))

    
    while True:
        fullscan_flag = None
        fullscan_check = str(input('폴더 전체를 탐색할까요? Y/N').upper())
        if fullscan_check == 'Y':
            fullscan_flag = True
            break

        elif fullscan_check == 'N':
            fullscan_flag = False

        else:
            print('다시입력하세요')
            

    main(src, args,fullscan_flag)
    print('작업이 완료됫습니다')
    os.system('pause')
