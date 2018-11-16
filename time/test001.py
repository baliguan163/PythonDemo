#-*-coding:utf-8-*-

__author__ = 'Administrator'

import datetime


def main2():
    begin = datetime.time(0, 0, 0)
    end = datetime.time(23,59,59)
    print(end)
    # for i in range((end - begin) + 1):
    #     day = begin + datetime.timedelta(days=i)
    #     print(str(day))


def main():
    begin = datetime.date(2016, 9, 10)
    end = datetime.date(2017, 9, 20)
    for i in range((end - begin).days + 1):
        day = begin + datetime.timedelta(days=i)
        print(str(day))


if __name__ == '__main__':
    main()
    # date_list = []
    # begin_date = datetime.date(2016, 9, 10)
    # end_date = datetime.date(2017, 9, 20)
    # begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    # end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    # while begin_date <= end_date:
    #     date_str = begin_date.strftime("%m-%d")
    #     date_list.append(date_str)
    #     begin_date += datetime.timedelta(days=1)
    # print(str(date_list))

