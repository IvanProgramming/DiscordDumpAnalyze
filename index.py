import json
import math
import re
import collections

file = open("MESSAGES.json", "r")
data = json.loads(file.read())
file.close()
emoji_regexp = ":[a-zA-Z_\-0-9]+:"
total_stats = {"average_chars": 0,
               "average_words": 0,
               "punc_mark": 0,
               "en_chars": 0,
               "ru_symbols": 0,
               "symbol_total": 0,
               "words_total": 0,
               "total_reactions": 0,
               "max_length_message": "",
               "total_messages": 0,
               "total_attachments": 0,
               "total_emotes": 0}
users = {}
users_ttl = {}

print("[+] Total messages - {}".format(data["messageCount"]))
print("[+] Starting analyze...")
analyzed = 0
total_messages = data["messageCount"]
total_stats["total_messages"] = int(total_messages)

for message in data["messages"]:
    if message["type"] == "Default":
        ru_chars = 0
        en_chars = 0
        total = len(message["content"])
        punc_mark = 0
        emotes = len(re.findall(emoji_regexp, message["content"]))
        words = len(message["content"].split(" "))
        for char in list(message["content"]):
            if char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
                en_chars += 1
            if char in "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ":
                ru_chars += 1
            if char in '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~':
                punc_mark += 1

        analyzed += 1
        total_stats["words_total"] += words
        total_stats["symbol_total"] += total
        total_stats["en_chars"] += en_chars
        total_stats["ru_symbols"] += ru_chars
        total_stats["punc_mark"] += punc_mark
        total_stats["total_reactions"] += len(message["reactions"])
        total_stats["total_attachments"] += len(message["attachments"])
        total_stats["total_emotes"] += emotes
        try:
            if users[message["author"]["id"]] and not message["author"]["isBot"]:
                users_ttl[message["author"]["id"]] += 1
        except:
            users[message["author"]["id"]] = {
                "name": message["author"]["name"],
                "discriminator": message["author"]["discriminator"]
            }
            users_ttl[message["author"]["id"]] = 1
        if total > len(total_stats["max_length_message"]):
            total_stats["max_length_message"] = message["content"]
        print("[+] Analyzed message {0}/{1}. Found {2} words, {3} symbols, {4} en symbols, {5} ru symbols, "
              "{6} punc symbols, {7} reactions, {8} attacments "
              .format(analyzed, total_messages, words, total, ru_chars, en_chars, punc_mark, len(message["reactions"]),
                      len(message["attachments"])))

total_stats["average_chars"] = math.ceil((total_stats["symbol_total"] / total_messages) * 10) / 10
total_stats["average_words"] = math.ceil((total_stats["words_total"] / total_messages) * 10) / 10

print("[+] Information about channel")
print("[+] -------- Averages --------")
print("[+] Chars in message  = {}".format(total_stats["average_chars"]))
print("[+] Words in message  = {}".format(total_stats["average_words"]))
print("[+] Message per user  = {}".format(math.ceil((total_messages / len(users)) * 10) / 10))
print("[+] --------- Totals ---------")
print("[+] Total Messages    = {}".format(total_messages))
print("[+] Total Chars       = {}".format(total_stats["symbol_total"]))
print("[+] Total Words       = {}".format(total_stats["words_total"]))
print("[+] Total Attachments = {}".format(total_stats["total_attachments"]))
print("[+] Total Reactions   = {}".format(total_stats["total_reactions"]))
print("[+] Total Emoji       = {}".format(total_stats["total_emotes"]))
print("[+] ------- Chars Info -------")
print("[+] Punctuation Marks = {}".format(total_stats["punc_mark"]))
print("[+] En Chars          = {}".format(total_stats["en_chars"]))
print("[+] Ru Chars          = {}".format(total_stats["ru_symbols"]))
print("[+] ---------- Tops ----------")

users_ttl = sorted(users_ttl.items(), reverse=True, key=lambda x: x[1])
count = 0
for elem in users_ttl[:10]:
    count += 1
    print("[+] {4}. {0}#{1} - {2} msg. {3}%".format(users[elem[0]]["name"], users[elem[0]]["discriminator"], elem[1], math.ceil((elem[1]/total_messages) * 1000) / 10, count))
