import time


def data_to_tuple(field, data):
    return map(lambda x: (
        int(time.mktime(x.get_record()['observation'].timetuple())), x.get_record()[field]), data)


def data_to_string(data):
    return ',\n'.join(map(lambda x: "{ x: %s, y: %.2f }" % x, data))


def sub_sample(data, rate):
    sampled_length = (len(data) / rate) + (0 if (len(data) % rate == 0) else 1)
    sampled = []

    for i in xrange(sampled_length):
        index = i * rate
        part = data[index:index + rate]

        s = 0.0
        for j in xrange(len(part)):
            s += part[j][1]

        # select middle date time
        sampled.append((data[index + int(len(part) / 2)][0], (s / len(part))))

    return sampled
