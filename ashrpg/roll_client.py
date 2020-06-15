import random
import re

class RollClient():

    regex = '(\s*(\d+)d(\d+)\s*([+|-]\s*\d+)?)'

    def __init__(self):
        self.pattern = re.compile(self.regex)

    def roll_dice(self, query):
        next_q = query
        parsed = re.match(self.pattern, next_q)
        result = []
        total = 0
        max = 100 # Lets prevent endless loops, shall we?

        while parsed and max >= 0:
            s, t = self.handle_rolled_section(next_q)
            next_q = next_q.replace(parsed.group(1), '')
            total += t
            result.append(s)
            parsed = re.match(self.pattern, next_q)
            max -= 1

        total_roll = f"{' + '.join(result)}= {total}"
        return total_roll

    def handle_rolled_section(self, part):
        parsed = re.match(self.pattern, part)
        result = []
        total = 0

        if not parsed:
            return None

        for x in range(int(parsed.group(2))):
            roll = random.randint(1,int(parsed.group(3)))
            total += roll
            result.append(str(roll))

        if parsed.group(4):
            extra = parsed.group(4)
            result.append(extra[0])
            result.append(extra[1:])

            if extra[0] == '+':
                total += int(extra[1:])
            else:
                total -= int(extra[1:])

        return f"({' + '.join(result[:int(parsed.group(2))])}) {' '.join(result[int(parsed.group(2)):])}", total
