#!/usr/bin/env python3

import itertools
import enchant
import requests
import json
import sys
import argparse


# create parser for arguments
parser = argparse.ArgumentParser(
	description='program that shows all possible words from letters abcdef')
parser.add_argument('--length', 
					type=int, 
					nargs=1, 
					help='length of the words to show',
				)
parser.add_argument('--refresh', 
					help='(re)create dict in file hex-dictionary.json',
					action="store_true",
				)
parser.add_argument('--number', 
					type=int, 
					help='decimal number to search in dictionary'
				)
parser.add_argument('--word', help='search for a word', type=str)
args = parser.parse_args()

DICT_API_URL = "https://owlbot.info/api/v1/dictionary/"
di = enchant.Dict("en_US")


# TODO: lambda this
def print_word(word, number, definition):
	print('\t', word.upper(), '(', number, ') --\n', definition, '\n')
	return


def get_definition(word):
	"""
	takes 
		word : string
	returns
		definition : string - from owlbot
	"""
	r = requests.get(DICT_API_URL + word)
	print(r.json())

	# defEnition is a mistake in API respond
	return r.json()[0]['defenition'] if len(r.json()) else "Owl doesn't know." 


def refresh_dict():
	dictionary = {}

	# find words which lenght is in range from 2 to 8
	for i in range(2, 8):
		words = [''.join(s) for s in  itertools.product("abcdef", repeat=i)]
		for word in words:
			if di.check(word):
				dictionary[word] = {}
				dictionary[word]['number'] = int(word, 16)
				dictionary[word]['defenition'] = get_definition(word)

	# write results in file
	with open("hex-dictionary.json", 'w+') as file:
		json.dump(dictionary, file, indent=4)


def print_dict(hex_dict, length=None):
	if length < 2 or length > 7:
		print('No words with length', length, 'in current dictionary')
		return
	for word, v in hex_dict.items():
		if (length == None or len(word) == length) and v['defenition'] != "":
			print_word(word, v['number'], v['defenition'])
	return


def find_def(hex_dict, word):
	try:
		w = hex_dict[word]
		print_word(word, w['number'], w['defenition'])
	except KeyError as e:
		print('Sorry, there is no such word.')


def find_by_num(hex_dict, number):
	for word, v in hex_dict.items():
		if v['number'] == number:
			print_word(word, v['number'], v['defenition'])
			return
	print("There is no word coded by", number)
	return

if __name__ == '__main__':
	hex_dict = {}
	with open("hex-dictionary.json") as fp:
		hex_dict = json.load(fp)

	if args.refresh: refresh_dict()
	if args.length: print_dict(hex_dict, args.length[0])
	if args.number: find_by_num(hex_dict, args.number)
	if args.word: find_def(hex_dict, args.word)

