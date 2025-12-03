from re import search, findall
from collections import defaultdict

data = """Begin in state A.
Perform a diagnostic checksum after 12399302 steps.

In state A:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state B.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the right.
    - Continue with state C.

In state B:
  If the current value is 0:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state A.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the right.
    - Continue with state D.

In state C:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state D.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state A.

In state D:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state E.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state D.

In state E:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state F.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state B.

In state F:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state A.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state E."""

test = """Begin in state A.
Perform a diagnostic checksum after 6 steps.

In state A:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state B.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state B.

In state B:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state A.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state A."""

def run(data):
  nested_dict = lambda: defaultdict(nested_dict)
  fsm = defaultdict(nested_dict)

  for description in findall(r'In state (\w):\s+If the current value is 0:\s+- Write the value (\d).\s+- Move one slot to the (\w+).\s+- Continue with state (\w).\s+If the current value is 1:\s+- Write the value (\d).\s+- Move one slot to the (\w+).\s+- Continue with state (\w).',data):
    state, w0, m0, ns0, w1, m1, ns1 = description
    fsm[state][0]['write'] = int(w0)
    fsm[state][0]['move'] = 1 if m0 == "right" else -1
    fsm[state][0]['next'] = ns0
    fsm[state][1]['write'] = int(w1)
    fsm[state][1]['move'] = 1 if m1 == "right" else -1
    fsm[state][1]['next'] = ns1

  lines = data.split("\n")[:2]
  state = search(r'\ABegin in state (\w)',lines[0]).group(1)
  checksum = int(search(r'\APerform a diagnostic checksum after (\d+) steps.',lines[1]).group(1))

  tape = [0]
  pos = 0
  for _ in range(checksum):
    todo = fsm[state][tape[pos]]
    tape[pos] = todo['write']
    pos += todo['move']
    if pos < 0:
      tape.insert(0,0)
      pos += 1
    elif pos == len(tape):
      tape.append(0)
    state = todo['next']

  return sum(tape)

print(run(test))
print(run(data))
