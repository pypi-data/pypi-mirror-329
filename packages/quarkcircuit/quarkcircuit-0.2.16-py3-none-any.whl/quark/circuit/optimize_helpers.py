# Copyright (c) 2024 XX Xiao

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files(the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and / or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

r""" 
This module contains the `GateCompressor` class, which is designed to optimize quantum circuits by 
merging or compressing adjacent gates. The primary functionality of this class is to reduce the number 
of gates in a quantum circuit, thereby improving its efficiency and making it more suitable for execution 
on quantum hardware.
"""
import numpy as np
from .quantumcircuit import (QuantumCircuit,
                             one_qubit_gates_available,
                             two_qubit_gates_available,
                             one_qubit_parameter_gates_available,
                             two_qubit_parameter_gates_available,
                             )
from .dag import qc2dag,dag2qc
from .decompose_helpers import u3_decompose
from .matrix import u_mat,gate_matrix_dict

class GateCompressor:
    def __init__(self,qc:QuantumCircuit):
        self.nqubits = qc.nqubits
        self.ncbits = qc.ncbits
        self.dag = qc2dag(qc)
        self.compressible_gates = ['id','x', 'y', 'z', 'h', 'cx', 'cnot', 'cy', 'cz', 'swap', 'rx', 'ry', 'rz', 'p', 'u', 'rxx', 'ryy', 'rzz']
        self._idx = 1000 

    def is_adjacent_gates(self,node1,node2):
        # 是否是相邻且可以合并的门
        gate1 = node1.split('_')[0]
        gate2 = node2.split('_')[0]
        qubits1 = self.dag.nodes[node1]['qubits']
        qubits2 = self.dag.nodes[node2]['qubits']
        if (gate1==gate2 and 
            gate1 in self.compressible_gates and 
            qubits1==qubits2 and 
            list(self.dag.out_edges(node1))==list(self.dag.in_edges(node2))
            ):
            return True
        else:
            return False
    def has_adjacent_gates(self):
        # 是否存在相邻且可以合并的门
        for edge in self.dag.edges():
            if self.is_adjacent_gates(edge[0],edge[1]):
                return True
        return False
    
    def compress_adjacent_single_qubit_gates(self,node1,node2):
        # compress single qubit gate
        nodes_remove = [node1,node2]
        nodes_added = []
        edges_added = []
        node1_predecessors = list(self.dag.predecessors(node1)) # len = 0 or 1
        if len(node1_predecessors) == 0:
            node1_pre = None
        elif len(node1_predecessors) == 1:
            node1_pre = node1_predecessors[0]
        node2_successors = list(self.dag.successors(node2)) # len = 0 or 1
        if len(node2_successors) == 0:
            node2_suc = None
        elif len(node1_predecessors) == 1:
            node2_suc = node2_successors[0]
        if node1_pre is not None and node2_suc is not None:
            # node1_pre and node2_suc 如果都是双比特门的话可能存在直接连接，判断有没有这种情况？
            if self.dag.has_edge(node1_pre,node2_suc):
                # 若有 则更新边上的qubit
                qubit = self.dag.nodes[node1_pre]['qubits']
                edges_added.append((node1_pre,node2_suc,{'qubit':list(sorted(qubit))}))
            else:
                qubit = self.dag.get_edge_data(node1,node2)['qubit']
                edges_added.append((node1_pre,node2_suc,{'qubit':qubit}))
        return nodes_remove,nodes_added,edges_added
    
    def compress_adjacent_single_parameter_qubit_gates(self,node1,node2):
        # compress single qubit gate
        nodes_remove = [node1,node2]
        nodes_added = []
        edges_added = []
        node1_predecessors = list(self.dag.predecessors(node1)) # len = 0 or 1
        if len(node1_predecessors) == 0:
            node1_pre = None
        elif len(node1_predecessors) == 1:
            node1_pre = node1_predecessors[0]
        node2_successors = list(self.dag.successors(node2)) # len = 0 or 1
        if len(node2_successors) == 0:
            node2_suc = None
        elif len(node1_predecessors) == 1:
            node2_suc = node2_successors[0]
        gate = node1.split('_')[0]
        params1 = self.dag.nodes[node1]['params']
        params2 = self.dag.nodes[node2]['params']
        if gate == 'u':
            u_mat1 = u_mat(*params1)
            u_mat2 = u_mat(*params2)
            new_u = u_mat2 @ u_mat1
            theta, phi, lamda, _ = u3_decompose(new_u)
            params = [theta, phi, lamda]                    
        else:
            params = [params1[indx] + params2[indx] for indx in range(len(params1))]
        mat = gate_matrix_dict[gate](*params)
        id = np.eye(mat.shape[0])
        if np.allclose(mat,id):
            if node1_pre is not None and node2_suc is not None:
                # node1_pre and node2_suc 如果都是双比特门的话可能存在直接连接，判断有没有这种情况？
                if self.dag.has_edge(node1_pre,node2_suc):
                    # 若有 则更新边上的qubit
                    qubit = self.dag.nodes[node1_pre]['qubits']
                    edges_added.append((node1_pre,node2_suc,{'qubit':list(sorted(qubit))}))
                else:
                    qubit = self.dag.get_edge_data(node1,node2)['qubit']
                    edges_added.append((node1_pre,node2_suc,{'qubit':qubit}))
        else:
            qubits = self.dag.nodes[node1]['qubits']
            new_node_info = (gate+'_'+str(self.idx)+'_'+str(qubits),{'qubits':qubits,'params':params})
            nodes_added.append(new_node_info)
            if node1_pre is not None:
                qubit = self.dag.get_edge_data(node1_pre,node1)['qubit']
                edges_added.append((node1_pre,new_node_info[0],{'qubit':qubit}))
            if node2_suc is not None:
                qubit = self.dag.get_edge_data(node2,node2_suc)['qubit']
                edges_added.append((new_node_info[0],node2_suc,{'qubit':qubit}))
        return nodes_remove,nodes_added,edges_added
    
    def _qubit2line(self,qubit):
        line = ''
        for q in qubit:
            line += 'q'+str(q)
        return line
    
    def _line2qubit(self,line):
        import re
        qubit = [int(num) for num in re.findall(r'\d+', line)]
        return list(sorted(qubit))
    
    def compress_adjacent_two_qubit_gates(self,node1,node2):
        # compress single qubit gate
        nodes_remove = [node1,node2]
        nodes_added = []
        edges_added = []
        node1_predecessors = list(self.dag.predecessors(node1)) 
        if len(node1_predecessors) == 0:
            node1_pre_dic = None
        else:
            node1_pre_dic = {}
            for node1_pre in node1_predecessors:
                qubit = self.dag.get_edge_data(node1_pre,node1)['qubit']
                line = self._qubit2line(qubit)
                node1_pre_dic[line] = node1_pre
        node2_successors = list(self.dag.successors(node2))
        if len(node2_successors) == 0:
            node2_suc_dic = None
        else:
            node2_suc_dic = {}
            for node2_suc in node2_successors:
                qubit = self.dag.get_edge_data(node2,node2_suc)['qubit']
                line = self._qubit2line(qubit)         
                node2_suc_dic[line] = node2_suc
        if node1_pre_dic is not None and node2_suc_dic is not None:
            for line1,node1_pre in node1_pre_dic.items():
                for line2,node2_suc in node2_suc_dic.items():
                    #print('line1 line2',line1,line2)
                    if line1 == line2:
                        # node1_pre and node2_suc 如果都是双比特门的话可能存在直接连接，判断有没有这种情况？
                        if self.dag.has_edge(node1_pre,node2_suc):
                            # 若有 则更新边上的qubit
                            qubit = self.dag.nodes[node1_pre]['qubits']
                            edges_added.append((node1_pre,node2_suc,{'qubit':qubit}))
                        else:
                            qubit = self._line2qubit(line1)
                            edges_added.append((node1_pre,node2_suc,{'qubit':qubit}))                        
                    elif line1 in line2:
                        qubit = self._line2qubit(line1)
                        edges_added.append((node1_pre,node2_suc,{'qubit':qubit}))
                    elif line2 in line1:
                        qubit = self._line2qubit(line2)
                        edges_added.append((node1_pre,node2_suc,{'qubit':qubit}))
        return nodes_remove,nodes_added,edges_added

    def compress_adjacent_two_qubit_parameter_gates(self,node1,node2):
        # compress single qubit gate
        nodes_remove = [node1,node2]
        nodes_added = []
        edges_added = []
        node1_predecessors = list(self.dag.predecessors(node1)) 
        if len(node1_predecessors) == 0:
            node1_pre_dic = None
        else:
            node1_pre_dic = {}
            for node1_pre in node1_predecessors:
                qubit = self.dag.get_edge_data(node1_pre,node1)['qubit']
                line = self._qubit2line(qubit)
                node1_pre_dic[line] = node1_pre
        node2_successors = list(self.dag.successors(node2))
        if len(node2_successors) == 0:
            node2_suc_dic = None
        else:
            node2_suc_dic = {}
            for node2_suc in node2_successors:
                qubit = self.dag.get_edge_data(node2,node2_suc)['qubit']
                line = self._qubit2line(qubit)         
                node2_suc_dic[line] = node2_suc

        gate = node1.split('_')[0]
        params1 = self.dag.nodes[node1]['params']
        params2 = self.dag.nodes[node2]['params']
        params = [params1[indx] + params2[indx] for indx in range(len(params1))]
        mat = gate_matrix_dict[gate](*params)
        id = np.eye(mat.shape[0])
        if np.allclose(mat,id):
            if node1_pre_dic is not None and node2_suc_dic is not None:
                for line1,node1_pre in node1_pre_dic.items():
                    for line2,node2_suc in node2_suc_dic.items():
                        #print('line1 line2',line1,line2)
                        if line1 == line2:
                            # node1_pre and node2_suc 如果都是双比特门的话可能存在直接连接，判断有没有这种情况？
                            if self.dag.has_edge(node1_pre,node2_suc):
                                # 若有 则更新边上的qubit
                                qubit = self.dag.nodes[node1_pre]['qubits']
                                edges_added.append((node1_pre,node2_suc,{'qubit':qubit}))
                            else:
                                qubit = self._line2qubit(line1)
                                edges_added.append((node1_pre,node2_suc,{'qubit':qubit}))                        
                        elif line1 in line2:
                            qubit = self._line2qubit(line1)
                            edges_added.append((node1_pre,node2_suc,{'qubit':qubit}))
                        elif line2 in line1:
                            qubit = self._line2qubit(line2)
                            edges_added.append((node1_pre,node2_suc,{'qubit':qubit}))
        else:
            qubits = self.dag.nodes[node1]['qubits']
            new_node_info = (gate+'_'+str(self.idx)+'_'+str(qubits),{'qubits':qubits,'params':params})
            nodes_added.append(new_node_info)
            if node1_pre_dic is not None:
                for line1,node1_pre in node1_pre_dic.items():
                    qubit = self._line2qubit(line1)
                    #print((node1_pre,new_node_info[0],{'qubit':qubit}))
                    edges_added.append((node1_pre,new_node_info[0],{'qubit':qubit}))
            if node2_suc_dic is not None:
                for line2,node2_suc in node2_suc_dic.items():
                    qubit = self._line2qubit(line2)
                    edges_added.append((new_node_info[0],node2_suc,{'qubit':qubit}))
        return nodes_remove,nodes_added,edges_added
        
    def run_compress_once(self,node1,node2):
        gate = node1.split('_')[0]
        if gate in one_qubit_gates_available.keys():
            return self.compress_adjacent_single_qubit_gates(node1,node2)
        elif gate in one_qubit_parameter_gates_available.keys():
            return self.compress_adjacent_single_parameter_qubit_gates(node1,node2)
        elif gate in two_qubit_gates_available.keys():
            return self.compress_adjacent_two_qubit_gates(node1,node2)
        elif gate in two_qubit_parameter_gates_available.keys():
            return self.compress_adjacent_two_qubit_parameter_gates(node1,node2)

    
    @property
    def idx(self):
        self._idx += 1
        return self._idx
    
    def run(self):
        compress = self.has_adjacent_gates()
        while compress:
            for edge in self.dag.edges():
                node1,node2 = edge
                if self.is_adjacent_gates(node1,node2):
                    nodes_remove,nodes_added,edges_added = self.run_compress_once(node1,node2)
                    self.dag.remove_nodes_from(nodes_remove)
                    self.dag.add_nodes_from(nodes_added)
                    self.dag.add_edges_from(edges_added)
                    #print('edge_added',edges_added)
                    break
            compress = self.has_adjacent_gates()
        
        qc = dag2qc(self.dag,self.nqubits,self.ncbits)
        #qc.qubits = self.qubits
        return qc