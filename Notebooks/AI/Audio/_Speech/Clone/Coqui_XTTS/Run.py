"""Static version of Coqui XTTS Notebook."""
__title__  = "Coqui XTTS"
__author__ = "kubinka0505"
__date__   = "31st December 2023"
__title__  = __title__.replace(" ", "_")

#-=-=-=-#

# Does not print information about output file
Clear_console_output_after_each_prompt = False

# If None, the first found ".txt" file from the current directory is taken
Prompts_File = "prompts.txt"

Pause_on_finish = False

#-=-=-=-#

exec(open("src/setup_variables.pyw", "r", encoding = "UTF-8").read())
exec(open("src/setup_prompts.pyw", "r", encoding = "UTF-8").read())
exec(open("src/setup_tts.pyw", "r", encoding = "UTF-8").read())

__Run_Time_Start = time() - Runtime_Start
print("Setup took {0}".format(
	str(timedelta(seconds = __Run_Time_Start))[2:-3])
)

exec(open("src/setup_runner.pyw", "r", encoding = "UTF-8").read())
exec(open("src/setup_end.pyw", "r", encoding = "UTF-8").read())