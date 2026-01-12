Runtime = time()
Counter = 1

def commaFix(s: str) -> str:
	return re.sub("([^\x00-\x7F]|\w)(\.|\。|\?)", r"\1 \2\2", s)

#-=-=-=-#

for Line in Prompts_List:
	Elements = Line.split("|")
	Elements = [Element.strip() for Element in Elements]

	#-=-=-=-#

	Speaker_Name = Elements[0]
	Language = Elements[1]
	Prompt_String = Elements[2]

	Speaker_Path = os.path.join(Directory_Inputs, Speaker_Name) + ".flac"
	Speaker_Display = os.path.splitext(os.path.basename(Speaker_Path))[0]

	if Language.lower().startswith(("auto", "none", "x")):
		Language = None

	if Use_Comma_Fix:
		Prompt_String = commaFix(Prompt_String)

	if Language:
		if Language in Languages:
			Language = IDs[Languages[Language][0]]
		else:
			raise ValueError("Unsupported language")
	else:
		Predicted = langid.classify(Prompt_String)[0].strip()

		if Predicted == "zh":
			Predicted = "zh-cn"

		if Language != Predicted:
			Language = Predicted

	MaxLen = Languages[Language][1]
	Language_Display = Languages[Language][0]

	#-=-=-=-#
	# Errors

	if os.path.basename(Speaker_Path) not in os.listdir(Directory_Inputs):
		raise FileNotFoundError(Speaker_Path)

	if len(Prompt_String) > MaxLen:
		rprint(f"[b #44AAFF]Prompt string length exceeds {MaxLen}, truncating[/]")
		Prompt_String = Prompt_String[:MaxLen]

	if len(Prompt_String) < Max_Prompt_Display_Length:
		Prompt_Display = f'"{Prompt_String}"'
	else:
		Prompt_Display = f'"{Prompt_String[:Max_Prompt_Display_Length]}(...)"'

	#-=-=-=-#
	# Print information

	Counter_Display = str(Counter).rjust(len(str(len(Prompts_List))) + 1, "0")

	print(f"{Counter_Display}.")
	print("    Speaker Name: ", Speaker_Display)
	print("    Language:     ", "{0} ({1} characters limit)".format(Language_Display, MaxLen))
	print("    Prompt:       ", Prompt_Display)

	#-=-=-=-#
	# Setup output file name

	if len(Elements) > 3:
		output_name = Elements[3]
		rprint("    Output Name:  ", output_name)
	else:
		output_name = re.sub(r"[,.;@#?!&$]+\ *", "_", Prompt_String).replace("_", " ")
		output_name = output_name.split()
		output_name = "_".join([x for x in output_name if output_name])

	output_name = output_name[:Truncate_Output_Name_After]
	output_path = os.path.join(Directory_Outputs, Speaker_Display, output_name + ".wav")
	output_path = os.path.abspath(output_path)

	output_dir = os.path.dirname(output_path)

	if not os.path.exists(output_dir):
		os.makedirs(output_dir, exist_ok = True)

	if os.path.exists(output_path):
		os.remove(output_path)

	# Run
	if not Length_Reference_Max:
		Length_Reference_Max = round(mFile(Speaker_Path).info.length)

	torch.cuda.empty_cache()

	#-=-=-=-#

	(gpt_cond_latent, speaker_embedding) = model.get_conditioning_latents(
		audio_path         = Speaker_Path,
		gpt_cond_len       = Length_GPT_Condition,
		gpt_cond_chunk_len = Length_GPT_Condition_Chunk,
		max_ref_length     = Length_Reference_Max
	)

	out = model.inference(
		Prompt_String, Language,
		gpt_cond_latent, speaker_embedding,
		repetition_penalty = Repetition_Penalty,
		temperature = Temperature,
	)

	torchaudio.save(
		output_path,
		torch.tensor(out["wav"]).unsqueeze(0),
		24000
	)

	if Clear_console_output_after_each_prompt:
		if Line != Prompts_List[-1]:
			cmd = "cls" if is_NT else "clear"
			os.system(cmd)
	else:
		print()

		rprint('[b][#44AAFF]\nSaved to "{0}" [#A0A0A0]({1}s) ({2})[/][/]'.format(
			os.path.relpath(output_path, Directory_Main),
			round(mFile(output_path).info.length, 3),
			fdb_size(output_path)
		))

		if Line != Prompts_List[-1]:
			print("\n" + "─" * 32 + "\n")

	Counter += 1

#-=-=-=-#

__Run_Time = time() - Runtime
print("\n" + "─" * 32 + "\n")
rprint("[b #00CC00]Done![/]")
rprint("Runtime: [b #44AAFF]{0}[/] [i #A0A0A0](avg. {1} per line)[/]".format(
	str(timedelta(seconds = __Run_Time))[2:-3],
	str(timedelta(seconds = __Run_Time / len(Prompts_List)))[2:-3]
))