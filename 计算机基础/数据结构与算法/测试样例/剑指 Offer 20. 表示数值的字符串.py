class Solution(object):
    def isNumber(self, s):
        """
        :type s: str
        :rtype: bool
        """
        states = [
            {'b':0, 'p':1, 'n':2, 'd':3},
            {'n':2, 'd':3},
            {'n':2, 'd':3, 's':5, 'b':8},
            {'n':4, 's':5, 'b':8},
            {'n':4, 's':5, 'b':8},
            {'p':6, 'n':7},
            {'n':7},
            {'n':7, 'b':8},
            {'b':8}
        ]
        cur = 0
        for a in s:
            state = ""
            if '0' <= a <= '9':
                state = 'n'
            elif a == ' ':
                state = 'b'
            elif a in ['+', '-']:
                state = 'p'
            elif a in ['e', 'E']:
                state = 's'
            elif a == '.':
                state = 'd'
            else:
                return False
            
            if state not in states[cur]:
                return False
            else:
                cur = states[cur][state]

        return True
    
    
    
    
tests = ["+100","5e2","-123","3.1416","-1E-16",
         "0123", "12e","1a3.14","1.2.3","+-5","12e+5.4"]