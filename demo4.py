import sys
from itertools import product

# canonical 3x3 digit patterns (concatenated rows -> 9-char key)
DIGITS = {
    " _ " + "| |" + "|_|": "0",
    "   " + "  |" + "  |": "1",
    " _ " + " _|" + "|_ ": "2",
    " _ " + " _|" + " _|": "3",
    "   " + "|_|" + "  |": "4",
    " _ " + "|_ " + " _|": "5",
    " _ " + "|_ " + "|_|": "6",
    " _ " + "  |" + "  |": "7",
    " _ " + "|_|" + "|_|": "8",
    " _ " + "|_|" + " _|": "9",
}

OPS = ['+','-','*','%']

# which positions in 3x3 can be toggled as horizontal/vertical segments
H_POS = {1, 4, 7}          # can be '_' or space
V_POS = {3, 5, 6, 8}       # can be '|' or space
TOGGLE_POS = sorted(list(H_POS | V_POS))

def read_input_blocks():
    data = sys.stdin.read().splitlines()
    if not data:
        return 0, []
    # skip leading empty lines
    idx = 0
    while idx < len(data) and data[idx].strip() == "":
        idx += 1
    if idx >= len(data):
        return 0, []
    N = int(data[idx].strip()); idx += 1
    # next 3 lines are the 3 rows of the display
    rows = []
    # allow possible blank lines between; take next 3 non-missing lines (but preserve spaces)
    for _ in range(3):
        if idx < len(data):
            rows.append(data[idx].rstrip('\n'))
            idx += 1
        else:
            rows.append("")
    # ensure each row length is at least 3*N (pad with spaces)
    rows = [r + " " * max(0, 3*N - len(r)) if len(r) < 3*N else r[:3*N] for r in rows]
    # build blocks
    blocks = []
    for i in range(N):
        block = rows[0][3*i:3*i+3] + rows[1][3*i:3*i+3] + rows[2][3*i:3*i+3]
        blocks.append(block)
    return N, blocks

def try_toggle_and_check(N, blocks):
    # candidate '=' indices: j where blocks[j] is not a digit and all blocks to the right are digits
    candidate_eq = []
    for j in range(1, N-1):
        ok = True
        for k in range(j+1, N):
            if blocks[k] not in DIGITS:
                ok = False; break
        if ok and blocks[j] not in DIGITS:
            candidate_eq.append(j)

    for j in candidate_eq:
        rhs_str = "".join(DIGITS[blocks[k]] for k in range(j+1, N))
        rhs_val = int(rhs_str)

        # try toggling each left-side character (positions 0..j-1)
        for t in range(0, j):
            orig = blocks[t]
            for pos in TOGGLE_POS:
                ch = orig[pos]
                # determine toggle possibility
                if pos in H_POS:
                    if ch == '_':
                        new_ch = ' '
                    elif ch == ' ':
                        new_ch = '_'
                    else:
                        continue
                else:
                    if ch == '|':
                        new_ch = ' '
                    elif ch == ' ':
                        new_ch = '|'
                    else:
                        continue
                new_block = orig[:pos] + new_ch + orig[pos+1:]
                new_blocks = list(blocks)
                new_blocks[t] = new_block

                # parse LHS (0..j-1) into tokens: numbers (ints) and operator-shape placeholders (strings)
                is_digit = [ (new_blocks[i] in DIGITS) for i in range(j) ]
                tokens = []
                i = 0
                valid_parse = True
                while i < j:
                    if is_digit[i]:
                        s = DIGITS[new_blocks[i]]
                        i += 1
                        while i < j and is_digit[i]:
                            s += DIGITS[new_blocks[i]]
                            i += 1
                        # avoid leading zeros problem? numbers can start with 0; allowed.
                        tokens.append(int(s))
                    else:
                        # operator placeholder (the 9-char shape)
                        tokens.append(new_blocks[i])
                        i += 1
                # tokens must be [num, op, num, op, num, ...] (odd length, numbers at even indices)
                if len(tokens) == 0 or not isinstance(tokens[0], int):
                    continue
                if len(tokens) % 2 == 0:
                    continue
                ok_seq = True
                for idx_tok, tk in enumerate(tokens):
                    if idx_tok % 2 == 0:
                        if not isinstance(tk, int):
                            ok_seq = False; break
                    else:
                        if isinstance(tk, int):
                            ok_seq = False; break
                if not ok_seq:
                    continue

                # collect unique operator shapes (placeholders)
                shapes = []
                for idx_tok in range(1, len(tokens), 2):
                    shape = tokens[idx_tok]
                    if shape not in shapes:
                        shapes.append(shape)
                k = len(shapes)
                if k > 4:
                    continue  # only 4 operator types exist

                # enumerate assignments of shapes -> ops
                for assignment in product(OPS, repeat=k):
                    mapping = { shapes[i]: assignment[i] for i in range(k) }
                    # evaluate left-to-right
                    try:
                        res = tokens[0]
                        for idx_tok in range(1, len(tokens), 2):
                            op_sym = mapping[tokens[idx_tok]]
                            num = tokens[idx_tok+1]
                            if op_sym == '+':
                                res = res + num
                            elif op_sym == '-':
                                res = res - num
                            elif op_sym == '*':
                                res = res * num
                            elif op_sym == '%':
                                if num == 0:
                                    raise ZeroDivisionError
                                res = res % num
                    except ZeroDivisionError:
                        continue
                    if res == rhs_val:
                        return t + 1
    return -1

def main():
    N, blocks = read_input_blocks()
    if N == 0:
        print(-1)
        return
    ans = try_toggle_and_check(N, blocks)
    if ans == -1:
        # problem guarantees a solution; print -1 as fallback
        print(-1)
    else:
        print(ans)

if __name__ == "__main__":
    main()
