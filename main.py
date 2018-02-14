from json_parser import JsonParser
import sys

if __name__ == '__main__':
    j = JsonParser(sys.argv[1])
    j.read_all()

    print('Total records number {}'.format( j.records_counter))
    print('Actions counter :')
    for k,v in j.actions.items():
        print('\t {} : {}'.format(k,v))
    print('Success percent {:.2f}%'.format(float(j.success_counter)/j.logs_counter*100))