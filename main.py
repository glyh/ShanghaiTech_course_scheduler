
import sys

import crawler


class BadParameter(ValueError):
    def __init__(self, unkown_parameter: str):
        Exception.__init__(self, 'Unknown parameter: {}'.
                           format(unkown_parameter))

def help() -> str:
    return \
'''
    
'''
if __name__ == '__main__':
    try:
        inputs = {'SEMESTER': 123}
        it = iter(sys.argv)

        it.__next__()  # Drop the file name
        for i in it:
            # The JSESSIONID of https://eams.shanghaitech.edu.cn/
            if i == '-J':
                inputs['JSESSION'] = it.__next__()
            elif i == '-U':
                inputs['USERNAME'] = it.__next__()
            elif i == '-P':
                inputs['PASSWORD'] = it.__next__()
            elif i == '-p':
                inputs['PROJECT'] = it.__next__()
            elif i == '-s':
                inputs['SEMESTER'] = it.__next__()
            elif i == '-h':
                # TODO: Implement help.
                pass
            else:
                raise BadParameter(i)
        crawler = crawler.Crawler()
        if 'JSESSION' in inputs:
            crawler.set_JSESSION(inputs['JSESSION'])
        elif 'USERNAME' in inputs and 'PASSWORD' in inputs:
            print('Sorry, but the method is not implemented yet. ')
            exit()
        result = crawler \
            .set_goal(int(inputs['SEMESTER'])) \
            .crawl_courses_status()
        print(result)
    except BadParameter as e:
        print(e)
    except Exception as e:
        print(e)
