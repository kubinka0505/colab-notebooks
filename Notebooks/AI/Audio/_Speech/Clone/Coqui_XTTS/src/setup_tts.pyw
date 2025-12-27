print()
rprint("[b #FFCC00]Importing TTS modules...[/]")

from TTS.api import TTS
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts
from TTS.utils.manage import ModelManager
from TTS.utils.generic_utils import get_user_data_dir

os.environ["COQUI_TOS_AGREED"] = "1"

#-=-=-=-#

rprint("[b #FFCC00]Retrieving model...[/]")

# Download XTTS
model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
model_path = os.path.join(get_user_data_dir("tts"), model_name.replace("/", "--"))
ckpt_path = os.path.join(model_path, "model.pth")

config_json = os.path.join(model_path, "config.json")
vocab_json = os.path.join(model_path, "vocab.json")

if not os.path.exists(model_path):
	# Download model
	rprint("[b #FFCC00]Downloading model...[/]")
	ModelManager().download_model(model_name)
#else:
#	rmtree(model_path)

rprint("[b #FFCC00]Configuring...[/]")
config = XttsConfig()
config.load_json(config_json)

# Loading model
model = Xtts.init_from_config(config)
model.load_checkpoint(
	config,
	checkpoint_path = ckpt_path,
	vocab_path = vocab_json,
	eval = True,
	use_deepspeed = False
)
model.cuda()

supported_languages = config.languages

print("\n" + "─" * 32 + "\n")