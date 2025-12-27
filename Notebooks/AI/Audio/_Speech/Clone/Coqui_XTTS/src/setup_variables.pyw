from time import time
Runtime_Start = time()

import os
import re
import torch
import langid
import torchaudio
from pathlib import Path
from shutil import rmtree
from datetime import timedelta
from rich import print as rprint
from mutagen import File as mFile

Use_Comma_Fix = True
Max_Prompt_Display_Length = 75
Truncate_Output_Name_After = 50

Length_GPT_Condition = 30
Length_GPT_Condition_Chunk = 4
Length_Reference_Max = 60
Repetition_Penalty = 5.0
Temperature = 0.75

#-=-=-=-#

is_NT = os.sys.platform.lower().startswith("win")

Languages = {
	#"id":   ("long_name",  characters_limit),
	"en":    ["English",    250],
	"es":    ["Spanish",    239],
	"fr":    ["French",     273],
	"de":    ["Deutsch",    253],
	"it":    ["Italian",    213],
	"pt":    ["Portuguese", 203],
	"tr":    ["Turkish",    226],
	"ru":    ["Russian",    182],
	"nl":    ["Dutch",      251],
	"pl":    ["Polish",     224],
	"cs":    ["Czech",      186],
	"ar":    ["Arabic",     166],
	"zh-cn": ["Chinese",     82],
	"ja":    ["Japanese",    71],
	"ko":    ["Korean",      95],
	"hu":    ["Hungarian",  224]
}

#-=-=-=-#
# Directories

Directory_Main = os.getcwd()
Directory_Main = os.path.abspath(Directory_Main)
Directory_Inputs = os.path.join(Directory_Main,  "_inputs")
Directory_Outputs = os.path.join(Directory_Main, "_outputs")

for Directory in Directory_Inputs, Directory_Outputs:
	os.makedirs(Directory, exist_ok = True)

#-=-=-=-#

def fdb_size(obj: str, extended_units: bool = False, bits: bool = False, recursive: bool = False) -> str:
	"""
	Args:
		obj: Bytes integer or string path of existing file or directory.
		extended_units: Extends the unit of the result, i.e. "Megabytes" instead of "MB".
		bits: Uses decimal divider (1000) instead of binary one. (1024)
		recursive: Iterate subdirectories, applicable only if `obj` is directory. (slow!)

	Returns:
		Human-readable files size string.
	"""
	# Setup

	if bits:
		Bits = 1000
		Bits_Display_Single = "bit"
		Bits_Display_Multiple = "bits"
	else:
		Bits = 1024
		Bits_Display_Single = "byte"
		Bits_Display_Multiple = "bytes"

	Units = {
		"":	 "",
		"K": "kilo",
		"M": "mega",
		"G": "giga",
		"T": "tera",
		"P": "peta",
		"E": "exa",
		"Z": "zetta",
		"Y": "yotta",
		"R": "ronna",
		"Q": "quetta"
	}

	#-=-=-=-#
	# Search for files

	if isinstance(obj, str):
		path = str(Path(obj).resolve())

		if not os.path.exists(path):
			raise FileNotFoundError(path)

		if os.path.isfile(obj):
			Files = [obj]
		else:
			Wildcard = "*"
			if recursive:
				Wildcard += "*/*"
			Files = list(Path(obj).glob(Wildcard))
			for File in Files:
				Files[Files.index(File)] = str(File.resolve())

		Files = map(os.path.getsize, Files)
		Bytes = sum(Files)
	else:
		Bytes = obj

	#-=-=-=-#
	# Calculate integer

	for Unit in Units:
		if Bytes < Bits:
			break
		Bytes /= Bits

	#-=-=-=-#
	# Ending conditions

	if extended_units:
		if Bytes == 1:
			Bits_Display = Bits_Display_Single
		else:
			Bits_Display = Bits_Display_Multiple
		Unit = (Units[Unit] + Bits_Display).capitalize()
	else:
		Unit += "B"

	#-=-=-=-#
	# Add zero to integer

	if "." in str(Bytes):
		Bytes = round(Bytes, 2)
		Bytes = str(Bytes).split(".")
		Bytes[1] = Bytes[1][:2]
		Bytes[1] = Bytes[1].ljust(2, "0")
		Bytes = ".".join(Bytes)

	Bytes = str(Bytes)

	#-=-=-=-#
	# Return string

	return " ".join((Bytes, Unit))