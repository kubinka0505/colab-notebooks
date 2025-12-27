print("\a")

if Pause_on_finish:
	cmd = "pause" if is_NT else 'read -n1 -r -p "Press any key to continue. . ." key'
	os.system(cmd)