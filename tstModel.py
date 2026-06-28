
from model.model import Model

myModel=Model()

myModel.buildGraph("Brazil")
nodi, archi= myModel.getGraphDetails()
print(f"Nodi: {nodi}, Archi: {archi}")