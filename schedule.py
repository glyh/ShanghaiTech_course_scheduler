
import sys
import pprint
import crawler


class BadParameter(ValueError):
    def __init__(self, unkown_parameter: str):
        Exception.__init__(self, 'Unknown parameter: {}'.
                           format(unkown_parameter))

help_string = '''Usage: python3 schedule.py [OPTION]
Auto crawl cousrses from EAMS and schdule.
    -s  [SESSION]                 Set the session ID for EAMS
    -a  [USERNAME] [PASSWORD]     Set the username and password for EAMS
    -i  [SEMESTER]                Set the semester you want to examine
    -h                            Show this help'''
if __name__ == '__main__':
    try:
        inputs = {'SEMESTER': 123}
        it = iter(sys.argv)

        it.__next__()  # Drop the file name
        for i in it:
            # The SESSION ID of https://eams.shanghaitech.edu.cn/
            if i == '-s':
                inputs['SESSION'] = it.__next__()
            elif i == '-a':
                inputs['USERNAME'] = it.__next__()
                inputs['PASSWORD'] = it.__next__()
            elif i == '-i':
                inputs['SEMESTER'] = it.__next__()
            elif i == '-h':
                print(help_string)
                exit()
            else:
                raise BadParameter(i)
        _crawler = crawler.Crawler()
        if 'SESSION' in inputs:
            _crawler.set_SESSION(inputs['SESSION'])
        elif 'USERNAME' in inputs and 'PASSWORD' in inputs:
            #print(inputs['USERNAME'], inputs['PASSWORD'])
            _crawler.login(inputs['USERNAME'], inputs['PASSWORD'])
            
            # HTTP bin test
            #print(_crawler.login_response.json())
            with open('out.html', 'wb') as f:
                f.write(_crawler.login_response.content)
            exit()
        else:
            print("Please input SESSION or (USERNAME, PASSWORD)!")
            print(help_string)
            exit()
        result = _crawler \
            .set_goal(int(inputs['SEMESTER'])) \
            .crawl_courses_status()
        print(result)
    except BadParameter as e:
        print(e)
        print()
        print(help_string)
    except Exception as e:
        print(e)
