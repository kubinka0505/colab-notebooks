"""Notebook cleaner."""
import os
import json
import argparse
from pathlib import Path
from typing import Any, Dict

def load_json(path: str) -> Dict[str, Any]:
	with open(path, "r", encoding = "UTF-8") as f:
		return json.load(f)

def save_json(path: str, data: Dict[str, Any]) -> None:
	with open(path, "w", encoding = "UTF-8") as f:
		json.dump(data, f, indent = "\t", ensure_ascii = False)

def clean_code_cell(cell: Dict[str, Any]) -> None:
	# remove execution_count if < 1 or None
	if "execution_count" in cell:
		if cell["execution_count"] is None or cell["execution_count"] < 1:
			cell.pop("execution_count", None)

	# remove outputs if null or empty list
	if "outputs" in cell:
		outputs = cell["outputs"]

		if outputs is None or (isinstance(outputs, list) and not outputs):
			cell.pop("outputs", None)

def clean_cells(data: Dict[str, Any]) -> None:
	cells = data.get("cells")

	if not isinstance(cells, list):
		return

	for cell in cells:
		if cell.get("cell_type") == "code":
			clean_code_cell(cell)

def reorder_dict_with_key_first(
	d: Dict[str, Any],
	key_first: str
) -> Dict[str, Any]:
	"""
	Returns a new dict with `key_first` placed first if present,
	preserving relative order of remaining keys.
	"""
	if key_first not in d:
		return d

	reordered = {key_first: d[key_first]}

	for k, v in d.items():
		if k != key_first:
			reordered[k] = v

	return reordered

def ensure_colab_metadata(data: Dict[str, Any], script_name: str) -> None:
	metadata = data.setdefault("metadata", {})
	colab = metadata.setdefault("colab", {})

	# set name
	colab["name"] = script_name

	# remove provenance if empty list
	if isinstance(colab.get("provenance"), list) and not colab["provenance"]:
		colab.pop("provenance", None)

	metadata["colab"] = reorder_dict_with_key_first(colab, "name")

def clean_notebook_file(path: str, script_name: str) -> None:
	data = load_json(path)

	clean_cells(data)
	ensure_colab_metadata(data, script_name)

	save_json(path, data)

def json_file(path: str) -> str:
	if not os.path.isfile(path):
		raise argparse.ArgumentTypeError(f"File not found: {path}")

	if not path.lower().endswith((".json", ".ipynb")):
		raise argparse.ArgumentTypeError(
			f"Unsupported file type (expected .json or .ipynb): {path}"
		)

	try:
		with open(path, "r", encoding = "UTF-8") as f:
			json.load(f)
	except Exception as e:
		raise argparse.ArgumentTypeError(
			f"Invalid JSON file: {path} ({e})"
		)

	return path

def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(
		description = open(__file__).readlines()[0].replace('"', "")
	)

	parser.add_argument(
		"-i", "--inputs",
		nargs = "+",
		type = json_file,
		required = True,
		help = "Input .ipynb or .json files to clean",
	)

	return parser.parse_args()

def main() -> None:
	args = parse_args()

	for path in args.inputs:
		script_name = os.path.splitext(os.path.basename(
			str(Path(path).resolve())
		))[0]
		clean_notebook_file(path, script_name)

if __name__ == "__main__":
	main()