# GGTP4
General Gui Tool Package with the help of gpt4

## Scope
Often the scripts for a specific task are written with the help of a chatbot quite fast. Luccyly the paramteres space of most non-trivial functions are quite lage.
By biulding end-to-end pipelines which are definded by a data-class stae, the most complex systems become controlable by a simple text file.

I would like to supplment with this project the text file with a simple GUI which represent the dataclass entries.

As an example a generator of a Haulemann-Machine for a lastercutter will be used. Since zmq will be a central part of the GUI Socket, it should easyily be adaptent to any zmq compatible usecase.

## Requirments
zmq
python
dataclass2gui

# Installation
pip install GGTP4

#Example

import ggtp4
import example_dataclass

dc = example_dataclass.create_random_dataclass(elements=8)
gui = ggtp4.make_gui(dc, subscriber_port=2420, dealer_port = 9999)
gui.make_fancy()
gui.show('22:22')
