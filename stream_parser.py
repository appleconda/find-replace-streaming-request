from collections import deque
import json

# Python program for KMP Algorithm
def KMPSearch(mappings, chunks, logger):

    def decode_chunk(chunk):
        prefix = 'data: '
        try:
            json_data = json.loads(chunk[len(prefix):].split('\n\n')[0])
            logger.info(f"[Parser] --decode_chunk-- json_data: {json_data}")
            return json_data
        except json.JSONDecodeError:
            logger.info("[Parser] --decode_chunk-- Exception caught of type JSONDecodeError")
            pass
        if decoded_chunk == "data: [DONE]":
            return None

    def encode_chunk(chunk):
        return f"data: {json.dumps(chunk)}\n\n"

    # lps that will hold the longest prefix suffix

    mappings = [mapping + [[0]*len(mapping[0])] + [0] for mapping in mappings]
    # mapping now contains list of [to_find, replace_with, lpsj, j]

    # Preprocess the pattern (calculate lps[] array) for each mapping
    for i in range(len(mappings)):
        computeLPSArray(mappings[i][0], len(mappings[i][0]), mappings[i][2])

    start_idx = 0
    keep_idx = 0
    i = 0
    chunk_buffer = deque()
    buffer = deque()
    for chunk in chunks:

        decoded_chunk = decode_chunk(chunk)
        if decoded_chunk is None: # handle last chunk
            logger.info("[Parser] decoded chunk is null")
            # empty buffer
            while len(chunk_buffer) > 0:
                yield encode_chunk(chunk_buffer.popleft()[0])

            # yield the last chunk
            yield chunk 
            break

        chunk_buffer.append([decoded_chunk, i])
        for c in decoded_chunk["choices"][0]["delta"]["content"]:
            buffer.append(c)

        while i < start_idx + len(buffer):

            for mp_idx in range(len(mappings)):

                # bring substring match index backwards till match until it doesn't match
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
                        chunk_buffer[0][0]["choices"][0]["delta"]["content"] = chunk_buffer[0][0]["choices"][0]["delta"]["content"][: starting] + mappings[mp_idx][1] + chunk_buffer[0][0]["choices"][0]["delta"]["content"][ending: ]
                        chunk_buffer[0][1] += len(mappings[mp_idx][0]) - len(mappings[mp_idx][1])
                    else:
                        chunk_buffer[0][0]["choices"][0]["delta"]["content"] = chunk_buffer[0][0]["choices"][0]["delta"]["content"][: starting] + mappings[mp_idx][1]
                        for ii in range(1, len(chunk_buffer) - 1):
                            chunk_buffer[ii][0]["choices"][0]["delta"]["content"] = ''
                        chunk_buffer[-1][1] += ending
                        chunk_buffer[-1][0]["choices"][0]["delta"]["content"] = chunk_buffer[-1][0]["choices"][0]["delta"]["content"][ending: ]

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
        while len(chunk_buffer) > 0 and chunk_buffer[0][1] + len(chunk_buffer[0][0]["choices"][0]["delta"]["content"]) - 1 < keep_idx:
            yield encode_chunk(chunk_buffer.popleft()[0])
    while len(chunk_buffer) > 0:
        yield encode_chunk(chunk_buffer.popleft()[0])

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

# def make_gen(li):
#     for item in li:
#         yield item

# def perform_test(input, mappings):

#     expected_output = "".join(input)
#     for to_find, replace_with in mappings:
#         expected_output = expected_output.replace(to_find, replace_with)
#     input = make_gen(input)

#     gener = KMPSearch(mappings, make_gen(input))
#     output = ""
#     for chunk in gener:
#         output += chunk

#     print(expected_output)
#     print(output)
#     assert(expected_output == output)

# def wrap_up(chunks):
#     return [
#         {"choices": [{"delta": {"content": chunk}}]} for chunk in chunks
#     ]

# def enc(chunks):
#     return [
#         f"data: {json.dumps(chunk)}".encode('utf-8') for chunk in chunks
#     ]

# chunks = ['HiShelia Lopez', ' my', ' nameShelia LopezShelia Lopez', ' is', ' Shel', 'ia', ' LopezLOLO', 'N', 'O', 'T', ' S', 'h', 'e', 'l', 'i', 'a', ' ', 'L', 'o', 'p', 'e', 'z']
# # chunks = ['Hi', ' my', ' name', ' is', ' Shel', 'ia', ' LopezShelia', ' LopezN', 'O', 'T', 'XXXShe', '', '', 'l', 'i', 'a', ' ', 'L', 'o', 'p', 'e', 'z']
# # chunks = ['ha', 'jaha']

# mappings = [["Shelia Lopez", "Mark"], ["Hi", "YOOOO"], ["N", "HAHAHAHHAHAHAH"]]
# # mappings = [["ja", "yah"], ["haja", "nah"]]
# content = "".join(chunks)

# # print(enc(wrap_up(chunks)))
# inp = make_gen(enc(wrap_up(chunks)))

# gener = KMPSearch(mappings, inp)
# for chunk in gener:
#     print(f"'{chunk}'")
