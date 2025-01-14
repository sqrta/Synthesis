from GHZ import GHZ
from CondAdder import CondAdder
from FullAdder import FullAdder
from Inversion import Inversion
from QFT import QFT
from Uniform import Uniform
from RippleAdder import RippleAdder
from RippleSubtractor import RippleSubtractor
from ToffoliN import ToffoliN
from Teleportation import Teleportation

import qiskit.quantum_info as qi
import numpy as np

import json

def get_qsyn_spec(matrix,args,file):
    data = {'ID':args['ID'], "Spec Type": "Partial Spec"}
    size = args['size']
    spec = {"qreg_size": str(size),"max_inst_allowed": "10"}
    spec_object = []
    for i in range(2**size):
        input = np.zeros(2**size)
        input[i]=1
        output = matrix @ input
        spec_object.append({"input": ",".join([str(float(i)) for i in input]), "output": ",".join([str(float(i)) for i in output])})
    spec['spec_object']=spec_object
    data['Spec'] = spec
    with open(file, 'w') as f:
        json.dump(data,f)


benchmarks = [('Inversion',3),('GHZ',5), ('CondAdder',3), ('FullAdder',3), ('QFT',6), ("Uniform", 6), ('RippleAdder',3), ('RippleSubtractor',3), ('ToffoliN',5), ('Teleportation',2)]

def dump(file, arg):
    func = eval(file)
    circ = func(arg)
    size = circ.num_qubits
    op = qi.Operator(circ)
    np.savetxt(f"qfast\examples\{file}.unitary", op.data)
    get_qsyn_spec(op.data, {'ID':file+str(size), 'size':size}, f"qsyn/benchmarks/{file}.json")
    print(f"{file} done")

# circ = GHZ(5)
# op = qi.Operator(circ)
# file = 'GHZ5'
# np.savetxt(f"matrix/{file}.unitary", op.data)
# exit(0)


for bench in benchmarks:
    dump(bench[0], bench[1])

print("Specifications for QFast and Qsyn are generated in qfast/examples and qsyn/benchmarks")
exit(0)

circ = GHZ(5)
op = qi.Operator(circ)
file = 'GHZ6'
np.savetxt(f"matrix/{file}.unitary", op.data)
get_qsyn_spec(op.data, {'ID':"GHZ6", 'size':6}, f"matrix/{file}.json")

print("fulladder done")
circ = FullAdder(3)
op = qi.Operator(circ)
np.savetxt("matrix/FullAdder6.unitary", op.data)

print("toff done")
circ = ToffoliN(5)
op = qi.Operator(circ)
np.savetxt("matrix/ToffoliN6.unitary", op.data)

print("rippleadd done")
circ = RippleAdder(3)
op = qi.Operator(circ)
np.savetxt("matrix/RippleAdder6.unitary", op.data)

print("ripplesub done")
circ = RippleSubtractor(3)
op = qi.Operator(circ)
np.savetxt("matrix/RippleSubtractor6.unitary", op.data)

print("qft done")
circ = QFT(6)
op = qi.Operator(circ)
print(circ)
np.savetxt("matrix/QFT6.unitary", op.data)

print("tele done")
circ = Teleportation(2)
op = qi.Operator(circ)
np.savetxt("matrix/Teleportation6.unitary", op.data)