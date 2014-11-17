# -*- coding: utf-8 -*-
"""
extract-hashes.py: Extracts hashes from a text file.

Version 0.3 - Nov/2014
Author: Daniel Marques (@0xc0da)
daniel _at_ codalabs _dot_ net - http://codalabs.net

The script reads a file and tries to extract hashes from it by using regex. 
Results are stored in separate files named as 'format-original_filename.txt'.
Supported formats and regex can be found in the 'regex_list' dictionary.

WARNING: Use carefully. It might return garbage or miss some hashes.


Copyright (c) 2014, Daniel C. Marques
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the <organization> nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL DANIEL C. MARQUES BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
import re
import sys
from os import path

def extract_hashes(source_file):
	regex_list = {
	
		'wordpress_md5': '\$P\$[\w\d./]+',
		'phpBB3_md5': '\$H\$[\w\d./]+',
		'sha1':  '(?<!\w)[a-f\d]{40}(?!\w)',
		'md5':  '(?<!\w)[a-f\d]{32}(?!\w)',
		'sha256':  '(?<!\w)[a-f\d]{64}(?!\w)',
		'sha512':  '(?<!\w)[a-f\d]{128}(?!\w)',
		'mysql':  '(?<!\w)[a-f\d]{16}(?!\w)',
		'mysql5': '\*[A-F\d]{40}'
	
	}
	
	result = {}
	
	fh = open(source_file, 'r')
	source_file_contents = fh.read()
	fh.close()
	
	for format in regex_list.keys():
		hashes = []
		regex = re.compile(regex_list[format])
		hashes = regex.findall(source_file_contents)
		if hashes:
			result[format] = hashes

	return result

def hashes_to_files(hashes, original_file):
	for format in hashes.keys():
		prefix = path.splitext(path.basename(original_file))[0]
		filename = '%s-%s.txt' % (format, prefix)
		with open(filename,'w') as output_file:
			for found_hash in hashes[format]:
				line = '%s\n' % found_hash
				output_file.write(line)

def main():
	extracted_hashes = {}
	
	print '%s: Extracts hashes from a text file' % sys.argv[0]

	if len(sys.argv) != 2:
		print 'Missing input file.'
		print 'Use: %s <filename>' % sys.argv[0]
		sys.exit(1)

	if not path.exists(sys.argv[1]):
		print 'File %s does not exists.' % sys.argv[1]
		sys.exit(1)

	extracted_hashes = extract_hashes(sys.argv[1])

	if extracted_hashes:
		hashes_to_files(extracted_hashes, sys.argv[1])
	
	print '\nExtracted hashes:'
	
	for format in extracted_hashes.keys():
		print '\t%s: %s' % (format, len(extracted_hashes[format]))


if __name__ == '__main__':
	main()
