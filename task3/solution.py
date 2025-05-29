def merge_intervals(intervals):
    """
    Объединяет пересекающиеся интервалы.
    """
    if not intervals:
        return []

    intervals.sort()
    merged = [intervals[0]]

    for start, end in intervals[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:
            merged[-1][1] = max(last_end, end)
        else:
            merged.append([start, end])

    return merged


def cut_to_lesson(intervals, lesson_start, lesson_end):
    """
    Обрезает интервалы по границам урока.
    """
    result = []
    for start, end in intervals:
        if end <= lesson_start or start >= lesson_end:
            continue
        start = max(start, lesson_start)
        end = min(end, lesson_end)
        result.append([start, end])
    return result


def count_overlap(pupil, tutor):
    """
    Считает пересечение двух списков интервалов.
    """
    i = j = 0
    total = 0
    while i < len(pupil) and j < len(tutor):
        start1, end1 = pupil[i]
        start2, end2 = tutor[j]

        overlap_start = max(start1, start2)
        overlap_end = min(end1, end2)

        if overlap_start < overlap_end:
            total += overlap_end - overlap_start

        if end1 < end2:
            i += 1
        else:
            j += 1
    return total


def appearance(intervals: dict[str, list[int]]) -> int:
    lesson = intervals['lesson']
    pupil_raw = intervals['pupil']
    tutor_raw = intervals['tutor']

    # Преобразуем интервалы в пары [начало, конец]
    pupil_intervals = [[pupil_raw[i], pupil_raw[i + 1]] for i in range(0, len(pupil_raw), 2)]
    tutor_intervals = [[tutor_raw[i], tutor_raw[i + 1]] for i in range(0, len(tutor_raw), 2)]

    # Объединяем и обрезаем интервалы
    pupil_merged = merge_intervals(pupil_intervals)
    tutor_merged = merge_intervals(tutor_intervals)

    pupil_cut = cut_to_lesson(pupil_merged, lesson[0], lesson[1])
    tutor_cut = cut_to_lesson(tutor_merged, lesson[0], lesson[1])

    return count_overlap(pupil_cut, tutor_cut)


tests = [
    {'intervals': {'lesson': [1594663200, 1594666800],
             'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
             'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
    },
    {'intervals': {'lesson': [1594702800, 1594706400],
             'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
             'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
    'answer': 3577
    },
    {'intervals': {'lesson': [1594692000, 1594695600],
             'pupil': [1594692033, 1594696347],
             'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
    'answer': 3565
    },
]

if __name__ == '__main__':
    for i, test in enumerate(tests):
        result = appearance(test['intervals'])
        assert result == test['answer'], f'Test {i} failed: got {result}, expected {test["answer"]}'
    print("Все тесты прошли")