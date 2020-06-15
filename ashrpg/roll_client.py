import random
import re

class RollClient():

    # regex = '(\s*(\d+)d(\d+)\s*([+|-]\s*\d+)?)'
    regex = '(\s*((\d+)d(\d+)|((?!d)\d+))\s*([+-])?)'

    def __init__(self):
        self.pattern = re.compile(self.regex)

    def roll_dice(self, query):
        next_q = query
        result = []
        total = 0
        max = 100 # Lets prevent endless loops, shall we?
        next_op = '+'

        try:
            while next_q and max >= 0:
                s, t, o, r = self.handle_rolled_section(next_q)
                next_q = next_q.replace(r, '')

                if next_op == '+':
                    total += t
                else:
                    total -= t
                result.append(s)
                result.append(o if o and next_q else '')
                next_op = o
                max -= 1

            total_roll = f"{' '.join(result)} = {total}"
            return total_roll
        except:
            return None

    def handle_rolled_section(self, part):
        parsed = re.match(self.pattern, part)
        result = []
        total = 0

        if not parsed:
            raise RuntimeError("Unable to parse request")

        # First check if it is a Dice Roll
        if parsed.group(3) and parsed.group(4):
            for x in range(int(parsed.group(3))):
                roll = random.randint(1,int(parsed.group(4)))
                total += roll
                result.append(str(roll))
        # A group 5 existence means only the number is there
        elif parsed.group(5):
            extra = parsed.group(5)
            result.append(extra)
            total += int(extra)

        # If group 6 exists, then there is an operator following and must be accounted for
        return f"({' + '.join(result)})" if not parsed.group(5) else f"{' + '.join(result)}", total, parsed.group(6), parsed.group(1)
