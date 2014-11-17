extract-hashes.py
=================

The script reads a file and tries to extract hashes from it by using regex. 
Results are stored in separate files named as 'format-original_filename.txt'.
Supported formats and regex can be found in the 'regex_list' dictionary.

**WARNING: Use carefully. It might return garbage or miss some hashes.**

Usage: `extract-hash.py <filename>`

Sampel output

```
python extract-hash.py hashes.txt 
extract-hash.py: Extracts hashes from a text file

Extracted hashes:
	wordpress_md5: 5
	md5: 192
```

