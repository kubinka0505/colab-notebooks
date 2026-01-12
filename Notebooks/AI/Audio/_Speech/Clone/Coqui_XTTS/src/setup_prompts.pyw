# Setup prompts
rprint("[b #00CC00]Retrieving prompts...[/]")

IDs = {v[0]: k for k, v in Languages.items()}

#-=-=-=-#

if Prompts_File:
	Prompts_File = os.path.abspath(Prompts_File)

	if not os.path.exists(Prompts_File):
		raise FileNotFoundError(Prompts_File)
else:
	Prompts_File = [str(File.resolve()) for File in Path().glob("*.txt")]

	if not Prompts_File:
		raise FileNotFoundError("No .txt files has been found in the current directory")

	Prompts_File = sorted(Prompts_File, key = os.path.getmtime)[0]

with open(Prompts_File, "r", encoding = "UTF-8") as File:
	Prompts = File.read()

#-=-=-=-#
# Old

Prompts_List = Prompts.strip("\n")
Prompts_List = Prompts_List.split("\n")
Prompts_List = [Line for Line in Prompts_List if Line]
__Lines_Old = len(Prompts_List)

# New
Prompts_List = [Line for Line in Prompts_List if not Line.startswith("#")]
__Lines_New = len(Prompts_List)

__Ignored = __Lines_Old - __Lines_New

rprint("[b #{0}]Found {1} prompts, {2} {3} ignored.[/]".format(
	"00CC00" if __Lines_New else "FF0000",
	__Lines_New, __Ignored,
	"was" if __Ignored == 1 else "were"
))

if not Prompts_List:
	print()
	raise ValueError("No prompts found.")