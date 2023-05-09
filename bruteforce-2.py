def congruent(a, b, mod):
    return abs(a - b) % mod == 0

def valid_choise(prev, new):
    return congruent(prev, new, 7) or abs(prev - new) == 1

def triangle_bf(notes):
    notes_len = len(notes)

    if notes_len < 4:
        return False, 0, []
    
    melodies = [[] for _ in range(4)]
    
    mask = [False] * len(notes)

    max_note_count = [0]
    song = [[]]

    def bf(melody_index=0, note_count=0):
        if max_note_count[0] == notes_len:
            return
        
        if note_count > max_note_count[0]:
            max_note_count[0] = note_count
            song[0] = [m.copy() for m in melodies]
            if note_count == notes_len:
                return
        
        melody_index %= 4

        # `melody` is an array of tuples (k, note)
        # where `k` is `note`s index at `notes`
        melody = melodies[melody_index]

        # wheter or not at least one note was choosen for this melody
        #can_choose = False

        # index to start searching for the next note of the n-th melody
        # if `melody` has at least one note, then start searching
        # from `melody`s last note index + 1
        start = 0 if len(melody) == 0 else (melody[-1][0] + 1)
        if start < len(notes):
            for k, note in enumerate(notes[start:], start=start):
                if (not mask[k]) and (start == 0 or valid_choise(melody[-1][1], note)):
                    #can_choose = True
                    mask[k] = True
                    melody.append((k, note))
                    bf(melody_index + 1, note_count + 1)
                    melody.pop()
                    mask[k] = False
        
        #if not can_choose:
        #    bf(melody_index + 1, note_count)
    
    bf()

    return max_note_count != 0, max_note_count[0], song[0]
