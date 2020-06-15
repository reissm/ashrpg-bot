import random
import re

class RollClient():

    regex = '((\d+)d(\d+)\s*([+|-]\s*\d+)?)+'

    def __init__(self):
        self.pattern = re.compile(self.regex)

    def roll_dice(self, query):
        parsed = re.match(self.pattern, query)
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

        total_roll = f"({' + '.join(result[:int(parsed.group(2))])}) {' '.join(result[int(parsed.group(2)):])} = {total}"
        return total_roll
