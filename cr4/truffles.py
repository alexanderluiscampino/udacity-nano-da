import operator


def take_one(box, truffle):
    """
    Calculate probability of pulling truffle of given type.
    :param box: dict of {type: count}.
    :return (float, box): probability and updated box.
    """
    total_truffles = sum(box.values())
    prob = (0. + box[truffle]) / total_truffles
    if box[truffle]:
        box[truffle] -= 1
    return prob, box


def take_sequence(box, seq):
    """Calculate probability of sequence of truffles.
    :param box: dict of {type: count}.
    :param seq: string
    :return float
    """
    probs = []
    for truffle in seq:
        p, box = take_one(box, truffle)
        probs.append(p)
    return reduce(operator.mul, probs, 1)


if __name__ == '__main__':
    total_prob = 0
    for seq in ['CCOO', 'OCCO', 'OOCC', 'COOC', 'COCO', 'OCOC']:
        box = {'O': 6, 'C': 4}
        ps = take_sequence(box, seq)
        print '- {}: {}'.format(seq, ps)
        total_prob += ps
    print 'Result', total_prob
