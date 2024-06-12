from collections import deque

# Python program for KMP Algorithm
def KMPSearch(mappings, chunks):

    # lps that will hold the longest prefix suffix

    # For each pattern-replacement pair in mappings, we add two more elements
    mappings = [mapping + [[0]*len(mapping[0])] + [0] for mapping in mappings]
    # mapping now contains list of [to_find, replace_with, lps, j]

    # Preprocess the pattern (calculate lps[] array) for each mapping
    for i in range(len(mappings)):
        computeLPSArray(mappings[i][0], len(mappings[i][0]), mappings[i][2])

    start_idx = 0
    keep_idx = 0
    i = 0
    chunk_buffer = deque()
    buffer = deque()
    for chunk in chunks:
        chunk_buffer.append([chunk, i])
        for c in chunk:
            buffer.append(c)

        while i < start_idx + len(buffer):

            for mp_idx in range(len(mappings)):

                # bring substring match index backwards till match until it doesn't match
                # mappings[x][0] is the string to find
                # mappings[x][1] is the index of the string to replace with
                # mappings[x][2] is the lps of the pat
                # mappings[x][3] is the j
                while mappings[mp_idx][3] > 0 and mappings[mp_idx][0][mappings[mp_idx][3]] != buffer[i - start_idx]:
                    mappings[mp_idx][3] = mappings[mp_idx][2][mappings[mp_idx][3] - 1]

            found = False
            for mp_idx in range(len(mappings)):

                if mappings[mp_idx][0][mappings[mp_idx][3]] == buffer[i - start_idx]:
                    mappings[mp_idx][3] += 1

                if mappings[mp_idx][3] == len(mappings[mp_idx][0]):

                    starting = i + 1 - mappings[mp_idx][3] - chunk_buffer[0][1]
                    ending = i + 1 - chunk_buffer[-1][1]
                    if len(chunk_buffer) == 1:
                        chunk_buffer[0][0] = chunk_buffer[0][0][: starting] + mappings[mp_idx][1] + chunk_buffer[0][0][ending: ]
                        chunk_buffer[0][1] += len(mappings[mp_idx][0]) - len(mappings[mp_idx][1])
                    else:
                        chunk_buffer[0][0] = chunk_buffer[0][0][: starting] + mappings[mp_idx][1]
                        for ii in range(1, len(chunk_buffer) - 1):
                            chunk_buffer[ii][0] = ''
                        chunk_buffer[-1][1] += ending
                        chunk_buffer[-1][0] = chunk_buffer[-1][0][ending: ]

                    found = True
                    break

            if found:
                for ii in range(len(mappings)):
                    mappings[ii][3] = 0

            i += 1

            keep_idx = max(0, i - max(mapping[3] for mapping in mappings))

        while start_idx < keep_idx and len(buffer) > 0:
            buffer.popleft()
            start_idx += 1
        while len(chunk_buffer) > 0 and chunk_buffer[0][1] + len(chunk_buffer[0][0]) - 1 < keep_idx:
            yield chunk_buffer.popleft()[0]
    while len(chunk_buffer) > 0:
        yield chunk_buffer.popleft()[0]

def computeLPSArray(pat, M, lps):
    len = 0 # length of the previous longest prefix suffix

    lps[0] # lps[0] is always 0
    i = 1

    # the loop calculates lps[i] for i = 1 to M-1
    while i < M:
        if pat[i]== pat[len]:
            len += 1
            lps[i] = len
            i += 1
        else:
            # This is tricky. Consider the example.
            # AAACAAAA and i = 7. The idea is similar
            # to search step.
            if len != 0:
                len = lps[len-1]

                # Also, note that we do not increment i here
            else:
                lps[i] = 0
                i += 1
