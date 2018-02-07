from collections import defaultdict
import os
import random
import time

import numpy as np

from getcharacter import _Getch


class Log:
    def __init__(self, timestamp, key, typed_key, elapsed):
        self.timestamp = int(timestamp)
        self.key = key
        self.typed_key = typed_key
        self.elapsed = round(float(elapsed), 2)

    @property
    def is_error(self):
        return self.key != self.typed_key

    @property
    def is_correct(self):
        return not self.is_error

    def serialize(self):
        return ', '.join([str(self.timestamp),
                          self.key,
                          self.typed_key,
                          str(self.elapsed)])

    @staticmethod
    def deserialize(string):
        return Log(*string.split(', '))


class Stat:
    def __init__(self, count=0, n_errors=0, average_time=0):
        self.count = int(count)
        self.n_errors = int(n_errors)
        self.average_time = average_time
        assert self.count >= self.n_errors

    def update(self, log):
        self.count += 1
        self.n_errors += log.is_error
        self.average_time *= (self.count - 1) / self.count
        self.average_time += log.elapsed / self.count

    @property
    def error_rate(self):
        if self.count == 0:
            return 0
        return self.n_errors / self.count

    @property
    def average_reward(self):
        # Hand crafted reward
        return 2 * self.error_rate + self.average_time

    def UCB_score(self, total_counts):
        if self.count == 0:
            # If the character was not tested yet, we need to test it
            return np.inf
        return self.average_reward + np.sqrt(np.log(total_counts) / (2 * self.count))


def read_chars(path):
    with open(path, 'r') as f:
        return [line.strip('\n') for line in f]

def read_logs(path):
    if not os.path.exists(path):
        return []
    logs = []
    with open(path, 'r') as f:
        for line in f:
            logs.append(Log.deserialize(line))
    return logs


def compute_stats(logs, chars):
    stats = {char: Stat() for char in chars}
    for log in logs:
        stats[log.key].update(log)
    return stats


def read_stats(path):
    if not os.path.exists(path):
        return initialize_stats()
    stats = {}
    with open(path, 'r') as f:
        for line in f:
            char, count, n_errors = line.split(', ')
            stats[char] = Stat(count, n_errors)
    return stats


def write_stats(stats, path):
    with open(path, 'w') as f:
        for char, stat in sorted(stats.items(), key=lambda kv: kv[1].count, reverse=True):
            print(f'{char}, {stat.count}, {stat.n_errors}', file=f)


def write_logs(logs, path):
    with open(path, 'w') as f:
        for log in logs:
            print(log.serialize(), file=f)


def choose_character(stats):
    total_counts = sum([stat.count for stat in stats.values()])
    chars, stats_list = zip(*stats.items())
    scores = [stat.UCB_score(total_counts) for stat in stats_list]
    return chars[np.argmax(scores)]


current_script_dir = os.path.dirname(os.path.realpath(__file__))
logs_path = os.path.join(current_script_dir, 'logs.txt')
chars_path = os.path.join(current_script_dir, 'chars.txt')
logs = read_logs(logs_path)
chars = read_chars(chars_path)

getch = _Getch()
print('Welcome to typing trainer!')
input('Press any key to continue')
print('-' * 50)
for _ in range(20):
    stats = compute_stats(logs, chars)
    key = choose_character(stats)
    print(f"Type: {key}\t(Attempts: {stats[key].count}, Errors: {stats[key].n_errors}, Reward: {round(stats[key].average_reward, 2)})")
    while True:
        start = time.time()
        typed_key = getch()
        elapsed = time.time() - start
        log = Log(start, key, typed_key, elapsed)
        logs.append(log)
        if log.is_correct:
            break

write_logs(logs, logs_path)
stats_path = os.path.join(current_script_dir, 'stats.txt')
write_stats(stats, stats_path)
