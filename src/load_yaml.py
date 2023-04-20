import yaml
from omegaconf import OmegaConf
from typing import Any, Dict
from pathlib import Path


import yaml
from dataclasses import dataclass, field, make_dataclass
from typing import Any, Dict, List, Tuple

import pickle
import zmq
from functools import partial
from typing import Any, Callable, Type


import tkinter as tk
from tkinter import ttk
from typing import List, Type


import pickle
import zmq
from functools import partial
from typing import Any, Callable

def on_value_change(socket: zmq.Socket, dataclass_type: Type, entries: List[tk.Entry]) -> None:
    data = {field_name: entry.get() for field_name, entry in entries.items()}
    instance = dataclass_type(**data)
    pickled_instance = pickle.dumps(instance)
    socket.send_multipart([dataclass_type.__name__.encode(), pickled_instance])


def load_yaml(file_path: str) -> Dict[str, Any]:
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def generate_dataclass_from_yaml(yaml_file_path: str) -> Tuple[Any, List[Dict[str, Any]]]:
    yaml_dict = load_yaml(yaml_file_path)
    class_name = yaml_dict["name"]
    fields = yaml_dict["fields"]
    data = yaml_dict["data"]

    dataclass_fields = [(field_def["name"], eval(field_def["type"])) for field_def in fields]
    DataClass = make_dataclass(class_name, dataclass_fields)

    return DataClass, data




def on_value_change(socket: zmq.Socket, dataclass_type: Type, entries: List[tk.Entry]) -> None:
    data = {field_name: entry.get() for field_name, entry in entries.items()}
    #instance = dataclass_type(**data)
    pickled_instance = pickle.dumps(data)
    socket.send_multipart([b'data',pickled_instance])
    print('Changed value.')

def create_dataclass_gui(dataclasses: List[Type], on_change_callback: Callable[[zmq.Socket, Type, List[tk.Entry]], Any]) -> None:
    # Set up the ZeroMQ context and publisher socket
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind("tcp://*:5555")

    # Create the main window
    root = tk.Tk()
    root.title("Dataclass GUI")

    # Create the tab control
    tab_control = ttk.Notebook(root)

    for dataclass_type in dataclasses:
        # Create a tab for the dataclass
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text=dataclass_type.pipe_id)

        # Create entry fields for each dataclass attribute
        entries = {}
        for idx, (field_name, field_type) in enumerate(dataclass_type.__annotations__.items()):
            label = ttk.Label(tab, text=f"{field_name} ({field_type.__name__}):")
            label.grid(column=0, row=idx, padx=10, pady=5, sticky="e")
            entry = ttk.Entry(tab)
            #set the initial value of the entry
            entry.insert(0, getattr(dataclass_type, field_name))
            entry.grid(column=1, row=idx, padx=10, pady=5, sticky="w")
            entries[field_name] = entry
        for filed_name, entry in entries.items():
            entry.bind(
                "<KeyRelease>",
                lambda event, s=publisher, t=dataclass_type, e=entries: on_change_callback(s, t, e)
                )

    # Pack the tab control and start the main loop
    tab_control.pack(expand=True, fill="both")
    root.mainloop()

if __name__ == "__main__":
    # Example usage:
    yaml_file = Path("GGTP4\data\example.yaml")
    CityPipe, pipe_data = generate_dataclass_from_yaml(yaml_file)

    pipes = [CityPipe(**pipe) for pipe in pipe_data]
    for pipe in pipes:
        print(pipe)

    dataclasses = pipes
    create_dataclass_gui(dataclasses, on_value_change)
