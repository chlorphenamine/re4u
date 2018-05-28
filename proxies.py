#! /usr/local/bin/python3

'''
'''

import re
import random

class IntProxy(object):
    '''
        http://www.re4u.ink

        Check the regular expression for int from x to y.
        Usage:
            ip = IntProxy(x=-20, y=200)
            ip.get_pattern()
        Return:
            r'^(?:-(?:20|1\d|[1-9])|(?:[1-9]?\d|1\d\d|200))$'

        http://www.forsythia.ink
    '''

    PATTERN_REPLACE_0 = re.compile(r'^0+')
    PATTERN_LAST_0000 = re.compile(r'0+$')
    PATTERN_LAST_9999 = re.compile(r'9+$')
    PATTERN_PREFIX_0 = re.compile(r'0{2,}(?=[1-9])')

    def __init__(self, *args, **kwds):
        self.__deploy(*args, **kwds)

    def __deploy(self, *args, **kwds):
        x = int(kwds.get('x'))
        y = int(kwds.get('y'))

        # from min to max
        (self.x, self.y) = (y, x) if x > y else (x, y)

    def __get_pattern(self, *args, **kwds):
        symbol = kwds.get('symbol', '')

        if self.a == self.b:
            options = [self.__str_a]
        elif self.__len_a == 1 and self.__len_b == 1:
            item = self.__get_item_by_number(self.a, self.b)
            options = [item]
        else:
            options = self.__get_options()

        if len(options) > 1:
            if not symbol:
                options.reverse()
            pattern = '{}(?:{})'.format(symbol, '|'.join(options))
        else:
            pattern = symbol + options[0]
        return pattern

    def __get_item_by_number(self, a, b):
        a = int(a)
        b = int(b)
        difference = b - a if b > a else a - b

        if difference == 0:
            return str(a)
        elif difference == 1:
            hyphen = ''
        elif difference == 2:
            hyphen = a + 1
        elif difference == 9:
            return r'\d'
        else:
            hyphen = '-'

        item = '[{}{}{}]'.format(a, hyphen, b)
        return item

    def __get_item_by_position(self, left, current, right):
        left = re.sub(IntProxy.PATTERN_REPLACE_0, '', left)
        n = len(right)
        right = r'\d' * n if n < 3 else r'\d{}{}{}'.format('{', n, '}')
        item = '{}{}{}'.format(left, current, right)
        return item

    def __get_options(self):
        '''
            i for a
            j for b
            check from max to min
        '''
        options = []

        for i, t in enumerate(zip(self.__str_a, self.__str_b)):
            # find the point where a < b
            if int(t[0]) < int(t[1]):
                point = i
                break

        # skip the last 0+9*$ or 9+$
        mb0 = IntProxy.PATTERN_LAST_0000.search(self.__str_b)
        mb9 = IntProxy.PATTERN_LAST_9999.search(self.__str_b)
        j = self.__len_b - 1
        if mb0:
            # the max number matched [1-9]0+$
            j = mb0.start() - 1
            options.append(self.__str_b)
        elif mb9:
            start = mb9.start()
            if start > point:
                j = start - 1
            else:
                j = point

        # check the numbers <= b before the point from right to left
        while j > point:
            left = self.__str_b[:j]
            x = int(self.__str_b[j])
            right = self.__str_b[j + 1:]

            # 17 should be 1[0-7]
            # 178 should be (?:17[0-8]|1[0-6]\d)
            # 179 should be 1[0-7]\d
            if not right or set(right) == set('9'):
                b = x
            else:
                b = x - 1

            # skip 0
            if b >= 0:
                current = self.__get_item_by_number(0, b)
                item = self.__get_item_by_position(left, current, right)
                options.append(item)

            j -= 1

        # check the point between a and b
        left = self.__str_a[:point]
        xa = int(self.__str_a[point])
        xb = int(self.__str_b[point])
        a_right = self.__str_a[point + 1:]
        b_right = self.__str_b[point + 1:]

        if not a_right:
            # the point is the last number
            a = xa
            b = xb
            i = self.__len_a
        elif self.a > 0 and set(a_right) == set('0'):
            # a matched point0+$
            a = xa
            # b matched point9+$
            b = xb if set(b_right) == set('9') else xb - 1
            i = self.__len_a
        else:
            # normal
            a = xa + 1
            b = xb if set(b_right) == set('9') else xb - 1
            i = point + 1

        if a <= b:
            current = self.__get_item_by_number(a, b)
            item = self.__get_item_by_position(left, current, a_right)
            options.append(item)

        # b is very bigger than a
        if self.__len_a > 4:
            if self.a == 0:
                item = '[1-9]\d{}0,{}{}'.format('{', self.__len_a - 2, '}')
                options.append(item)
                options.append('0')
                i = self.__len_a
            else:
                m = IntProxy.PATTERN_PREFIX_0.match(self.__str_a)
                if m:
                    t = len(m.group())
                    ta = self.__len_a - t
                    tb = self.__len_a - 2
                    if ta == tb:
                        item = '[1-9]\d{}{}{}'.format('{', ta, '}')
                    else:
                        item = '[1-9]\d{}{},{}{}'.format('{', ta, tb, '}')
                    options.append(item)
                    i = t

        # check the numbers >= a after the point from left to right
        while i < self.__len_a:
            left = self.__str_a[:i]
            x = int(self.__str_a[i])
            right = self.__str_a[i + 1:]

            if not right:
                # the last number
                a = x
                i = self.__len_a
            elif self.a > 0 and set(right) == set('0'):
                # the min number matched [1-9]0+$
                a = x
                i = self.__len_a
            else:
                a = x + 1

            # skip 9
            if a < 10:
                current = self.__get_item_by_number(a, 9)
                # 0-99 should be [1-9]?\d
                if self.a == 0 and right == '0':
                    current += '?'
                    i = self.__len_a

                item = self.__get_item_by_position(left, current, right)
                options.append(item)

            # the min number matched 9+$
            if set(right) == set('9'):
                options.append(str(self.__a))
                break

            i += 1

        return options

    def get_pattern(self, *args, **kwds):
        # return 'Just do it!'
        note = 'There is no pattern from {} to {} 4u.'.format(self.x, self.y)

        if self.x == self.y:
            return '^{}$'.format(self.__str_x)

        limit = 78
        if self.__len_x > limit or self.__len_y > limit:
            return note

        if (self.x + self.y == 0) and (self.x > 0 or self.y > 0):
            # symmetry numbers
            self.a = 1
            self.b = self.x if self.x > 0 else self.y
            pattern = self.__get_pattern()
            return '^(?:0|-?{})$'.format(pattern)

        if self.x < 0:
            if self.y <= 0:
                # negative numbers or 0
                self.a = 1 if self.y == 0 else self.y * -1
                self.b = self.x * -1
                pattern = self.__get_pattern(symbol='-')

                # special 0
                if self.y == 0:
                    pattern = '(?:{}|0)'.format(pattern)
            else:
                # negative numbers
                self.a = 1
                self.b = self.x * -1
                negative = self.__get_pattern(symbol='-')

                # 0 or positive numbers
                self.a = 0
                self.b = self.y
                positive = self.__get_pattern()

                # all numbers
                pattern = '(?:{}|{})'.format(negative, positive)
        else:
            # 0 or positive numbers
            self.a = self.x
            self.b = self.y
            pattern = self.__get_pattern()

        return '^{}$'.format(pattern)


    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        self.__x = int(value)
        self.__str_x = str(self.__x)
        self.__len_x = len(self.__str_x)

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        self.__y = int(value)
        self.__str_y = str(self.__y)
        self.__len_y = len(self.__str_y)

    @property
    def a(self):
        return self.__a

    @a.setter
    def a(self, value):
        self.__a = int(value)
        self.__str_a = str(self.__a)
        self.__len_a = len(self.__str_a)

    @property
    def b(self):
        return self.__b

    @b.setter
    def b(self, value):
        self.__b = int(value)
        self.__str_b = str(self.__b)
        self.__len_b = len(self.__str_b)
        # prefix 0 for a
        self.__str_a = '{}:0{}d{}'.format('{', self.__len_b, '}').format(self.a)
        self.__len_a = self.__len_b



class StepProxy(object):
    '''
        http://www.re4u.ink

        Step the int regular expression to a list.
        Usage:
            sp = StepProxy(pattern=r'^(?:-(?:20|1\d|[1-9])|(?:[1-9]?\d|1\d\d|200))$')
            sp.get_list()
        Return:
            [
                {'indent': 0, 'pattern': '^', 'note': 'string start'},
                {'indent': 1, 'pattern': '(?:', 'note': 'logic start'},
                {'indent': 2, 'pattern': '-(?:', 'note': 'negative logic start'},
                {'indent': 3, 'pattern': '20', 'note': '20'},
                {'indent': 3, 'pattern': '|', 'note': 'or'},
                {'indent': 3, 'pattern': '1\\d', 'note': '14'},
                {'indent': 3, 'pattern': '|', 'note': 'or'},
                {'indent': 3, 'pattern': '[1-9]', 'note': 5},
                {'indent': 2, 'pattern': ')', 'note': 'logic end'},
                {'indent': 2, 'pattern': '|', 'note': 'or'},
                {'indent': 2, 'pattern': '(?:', 'note': 'logic start'},
                {'indent': 3, 'pattern': '[1-9]?\\d', 'note': '0'},
                {'indent': 3, 'pattern': '|', 'note': 'or'},
                {'indent': 3, 'pattern': '1\\d\\d', 'note': '180'},
                {'indent': 3, 'pattern': '|', 'note': 'or'},
                {'indent': 3, 'pattern': '200', 'note': '200'},
                {'indent': 2, 'pattern': ')', 'note': 'logic end'},
                {'indent': 1, 'pattern': ')', 'note': 'logic end'},
                {'indent': 0, 'pattern': '$', 'note': 'string end'}
            ]

        http://www.forsythia.ink
    '''

    PATTERN_OPEN = re.compile(r'\^|(?:-\??)?\(\?:')
    PATTERN_APPEND = re.compile(r'\||[^|)$]+')
    PATTERN_CLOSE = re.compile(r'[)$]')
    
    PATTERN_MULTIPLE_NUMBER = re.compile(r'\\d{(\d+)(,\d+)?}')
    PATTERN_ONLY_NUMBER = re.compile(r'^-?\d+$')
    PATTERN_ONLY_NUMBER_GROUP = re.compile(r'^\[[-\d]+\]$')
    PATTERN_NUMBER_GROUP = re.compile(r'\[[-\d]+\]\??')

    def __init__(self, *args, **kwds):
        self.__pattern = kwds.get('pattern')

    def get_number(self, *args, **kwds):
        pattern = kwds.get('pattern')
        if not pattern:
            return ''

        match_multiple_number = StepProxy.PATTERN_MULTIPLE_NUMBER.search(pattern)
        match_only_number = StepProxy.PATTERN_ONLY_NUMBER.match(pattern)
        match_only_number_group = StepProxy.PATTERN_ONLY_NUMBER_GROUP.match(pattern)
        match_number_group = StepProxy.PATTERN_NUMBER_GROUP.search(pattern)

        if match_multiple_number:
            # \d{a,b}
            group = match_multiple_number.group()
            a = int(match_multiple_number.group(1))
            b = match_multiple_number.group(2)
            if b:
                b = int(b[1:]) + 1
                q = list(range(a, b))
                r = random.choice(q)
            else:
                r = a
            pattern = pattern.replace(group, r'\d' * r)
        if match_only_number:
            return pattern
        elif match_only_number_group:
            if '-' in pattern:
                q = range(int(pattern[1]), int(pattern[-2]) + 1)
                return random.choice(list(q))
            else:
                return random.choice(pattern[1:-1])
        elif match_number_group:
            group = match_number_group.group()
            if '-' in group:
                if '?' in group and random.random() < .5:
                    r = ''
                else:
                    q = range(int(group[1]), int(group[3]) + 1)
                    r = str(random.choice(list(q)))
            else:
                r = random.choice(group[1:-1])

            pattern = pattern.replace(group, r)
        else:
            pass

        while r'\d' in pattern:
            q = range(0, 10)
            r = random.choice(list(q))
            pattern = pattern.replace(r'\d', str(r), 1)

        return pattern

    def get_list(self, *args, **kwds):
        if not self.__pattern:
            return []

        indent = 0
        queue = []
        pattern = self.__pattern

        while pattern:
            match_open = StepProxy.PATTERN_OPEN.match(pattern)
            match_append = StepProxy.PATTERN_APPEND.match(pattern)
            match_close = StepProxy.PATTERN_CLOSE.match(pattern)

            if match_open:
                group = match_open.group()
                item = {'indent': indent, 'pattern': group}
                indent += 1
            elif match_close:
                indent -= 1
                group = match_close.group()
                item = {'indent': indent, 'pattern': group}
            elif match_append:
                group = match_append.group()
                item = {'indent': indent, 'pattern': group}

            if group == '^':
                note = 'string start'
            elif group == '$':
                note = 'string end'
            elif group == '(?:':
                note = 'logic start'
            elif group == '-(?:':
                note = 'negative logic start'
            elif group == '-?(?:':
                note = 'nonzero numbers start'
            elif group == '|':
                note = 'or'
            elif group == ')':
                note = 'logic end'
            else:
                note = self.get_number(pattern=group)

            item['note'] = note
            queue.append(item)
            pattern = pattern[len(group):]
        else:
            return queue






def main():
    ip = IntProxy(x=-20, y=200)
    pattern = ip.get_pattern()
    print(pattern)

    sp = StepProxy(pattern=pattern)
    steps = sp.get_list()
    print(steps)

if __name__ == '__main__':
    main()








