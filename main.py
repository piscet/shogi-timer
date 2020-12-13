import config as conf
from common import Prob
import time, sys, tty, termios, csv

def inputs(discription, f):
    while True:
        res = input(discription)
        if f(res):
            return res


def get_key():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        key = sys.stdin.read(1)
        if ord(key) == conf.KeyConf.ctrl_c:
            raise KeyboardInterrupt()
        else:
            return key
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def main():
    start = int(input("開始問題番号 >"))
    N = int(input("問題数 >"))
    max_cycle = int(input("見開きの問題数 >"))
    time_out = int(input("制限時間 [s] (必要ない場合は -1) >"))

    count = 0
    log_lst = []
    try:
        while True:
            cycle = min(max_cycle, N - count)
            for i in range(cycle):
                now_prob = count + i + start
                prob_data = Prob(now_prob, time_out)

                print()
                print(f"[{i + 1}/{cycle} : {now_prob} 問目(all:{N})]")
                input("Enterを押してスタート")

                start_time = time.time()

                print("計測中 ...")
                print("space を押して終了")
                print("ctrl + c で中断")

                while True:
                    key = ord(get_key())
                    if key == conf.KeyConf.space:
                        end_time = time.time()
                        break
                record = int(end_time - start_time)
                isTimeout = (time_out > 0 and record >= time_out)
                prob_data.add_time(record)
                log_lst.append(prob_data)

                print()
                print("time : {:3}s".format(record), end = '')
                print(" timeout..." if isTimeout else "")

            for i in range(cycle):
                # 結果を入力
                key = inputs(f'{count + i + 1} 問目の正答 [o/x]> ', lambda x: x in {'x', 'o'})
                log_lst[- cycle + i].add_result(key == 'o')
            count += cycle
            if count >= N:
                break

    except KeyboardInterrupt:
        print("中断しました")

    # 結果の表示
    ans = 0
    time_mean = 0
    for i in log_lst:
        ans += i.isSolve_int()
        time_mean += i.time
    ans_ratio = ans / N
    time_mean //= N
    print()
    print("------ result --------------------------")
    print()
    print("正答率 - {:2.1f}% ({:2}/{:2})".format(ans_ratio * 100, ans, N))
    print("平均解答時間 - {:2}:{:0>2}".format(time_mean // 60, time_mean % 60))
    print()
    for i in log_lst:
        print(i)

    # csv に保存
    FILE_NAME = "sample.csv"
    with open(f"csv/{FILE_NAME}", 'x') as df:
        writer = csv.writer(df)
        writer.writerow(["問題数", len(log_lst), "正解数", ans])
        writer.writerow([])

        for _data in log_lst:
            writer.writerow(_data.for_csv())



if __name__ == "__main__":
    main()