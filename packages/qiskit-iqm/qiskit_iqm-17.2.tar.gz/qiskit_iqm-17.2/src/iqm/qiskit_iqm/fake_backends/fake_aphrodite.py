# Copyright 2022-2023 Qiskit on IQM developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Fake (i.e. simulated) backend for IQM's 54-qubit Aphrodite architecture
"""
from iqm.iqm_client import QuantumArchitectureSpecification
from iqm.qiskit_iqm.fake_backends.iqm_fake_backend import IQMErrorProfile, IQMFakeBackend


def IQMFakeAphrodite() -> IQMFakeBackend:
    """Return IQMFakeBackend instance representing IQM's Aphrodite architecture."""
    # pylint: disable=duplicate-code
    qubits = [
        "QB1",
        "QB2",
        "QB3",
        "QB4",
        "QB5",
        "QB6",
        "QB7",
        "QB8",
        "QB9",
        "QB10",
        "QB11",
        "QB12",
        "QB13",
        "QB14",
        "QB15",
        "QB16",
        "QB17",
        "QB18",
        "QB19",
        "QB20",
        "QB21",
        "QB22",
        "QB23",
        "QB24",
        "QB25",
        "QB26",
        "QB27",
        "QB28",
        "QB29",
        "QB30",
        "QB31",
        "QB32",
        "QB33",
        "QB34",
        "QB35",
        "QB36",
        "QB37",
        "QB38",
        "QB39",
        "QB40",
        "QB41",
        "QB42",
        "QB43",
        "QB44",
        "QB45",
        "QB46",
        "QB47",
        "QB48",
        "QB49",
        "QB50",
        "QB51",
        "QB52",
        "QB53",
        "QB54",
    ]
    qubit_connectivity = [
        ["QB1", "QB2"],
        ["QB1", "QB5"],
        ["QB2", "QB6"],
        ["QB3", "QB4"],
        ["QB3", "QB9"],
        ["QB4", "QB5"],
        ["QB4", "QB10"],
        ["QB5", "QB6"],
        ["QB5", "QB11"],
        ["QB6", "QB7"],
        ["QB6", "QB12"],
        ["QB7", "QB13"],
        ["QB8", "QB9"],
        ["QB8", "QB16"],
        ["QB9", "QB10"],
        ["QB9", "QB17"],
        ["QB10", "QB11"],
        ["QB10", "QB18"],
        ["QB11", "QB12"],
        ["QB11", "QB19"],
        ["QB12", "QB13"],
        ["QB12", "QB20"],
        ["QB13", "QB14"],
        ["QB13", "QB21"],
        ["QB14", "QB22"],
        ["QB15", "QB16"],
        ["QB15", "QB23"],
        ["QB16", "QB17"],
        ["QB16", "QB24"],
        ["QB17", "QB18"],
        ["QB17", "QB25"],
        ["QB18", "QB19"],
        ["QB18", "QB26"],
        ["QB19", "QB20"],
        ["QB19", "QB27"],
        ["QB20", "QB21"],
        ["QB20", "QB28"],
        ["QB21", "QB22"],
        ["QB21", "QB29"],
        ["QB22", "QB30"],
        ["QB23", "QB24"],
        ["QB24", "QB25"],
        ["QB24", "QB32"],
        ["QB25", "QB26"],
        ["QB25", "QB33"],
        ["QB26", "QB27"],
        ["QB26", "QB34"],
        ["QB27", "QB28"],
        ["QB27", "QB35"],
        ["QB28", "QB29"],
        ["QB28", "QB36"],
        ["QB29", "QB30"],
        ["QB29", "QB37"],
        ["QB30", "QB31"],
        ["QB30", "QB38"],
        ["QB31", "QB39"],
        ["QB32", "QB33"],
        ["QB32", "QB40"],
        ["QB33", "QB34"],
        ["QB33", "QB41"],
        ["QB34", "QB35"],
        ["QB34", "QB42"],
        ["QB35", "QB36"],
        ["QB35", "QB43"],
        ["QB36", "QB37"],
        ["QB36", "QB44"],
        ["QB37", "QB38"],
        ["QB37", "QB45"],
        ["QB38", "QB39"],
        ["QB38", "QB46"],
        ["QB40", "QB41"],
        ["QB41", "QB42"],
        ["QB41", "QB47"],
        ["QB42", "QB43"],
        ["QB42", "QB48"],
        ["QB43", "QB44"],
        ["QB43", "QB49"],
        ["QB44", "QB45"],
        ["QB44", "QB50"],
        ["QB45", "QB46"],
        ["QB45", "QB51"],
        ["QB47", "QB48"],
        ["QB48", "QB49"],
        ["QB48", "QB52"],
        ["QB49", "QB50"],
        ["QB49", "QB53"],
        ["QB50", "QB51"],
        ["QB50", "QB54"],
        ["QB52", "QB53"],
        ["QB53", "QB54"],
    ]
    architecture = QuantumArchitectureSpecification(
        name="Aphrodite",
        operations={
            "prx": [[q] for q in qubits],
            "cz": list(qubit_connectivity),
            "measure": [[q] for q in qubits],
            "barrier": [],
        },
        qubits=qubits,
        qubit_connectivity=qubit_connectivity,
    )

    error_profile = IQMErrorProfile(
        t1s={
            "QB1": 49500.0,
            "QB2": 49400.0,
            "QB3": 41500.0,
            "QB4": 50300.0,
            "QB5": 49100.0,
            "QB6": 48700.0,
            "QB7": 48800.0,
            "QB8": 49900.0,
            "QB9": 48200.0,
            "QB10": 49600.0,
            "QB11": 42700.0,
            "QB12": 50100.0,
            "QB13": 47500.0,
            "QB14": 48300.0,
            "QB15": 39200.0,
            "QB16": 49000.0,
            "QB17": 49100.0,
            "QB18": 49200.0,
            "QB19": 41600.0,
            "QB20": 41800.0,
            "QB21": 49500.0,
            "QB22": 49400.0,
            "QB23": 41500.0,
            "QB24": 50300.0,
            "QB25": 49100.0,
            "QB26": 48700.0,
            "QB27": 48800.0,
            "QB28": 49900.0,
            "QB29": 48200.0,
            "QB30": 49600.0,
            "QB31": 42700.0,
            "QB32": 50100.0,
            "QB33": 47500.0,
            "QB34": 48300.0,
            "QB35": 39200.0,
            "QB36": 49000.0,
            "QB37": 49100.0,
            "QB38": 49200.0,
            "QB39": 41600.0,
            "QB40": 41800.0,
            "QB41": 49500.0,
            "QB42": 49400.0,
            "QB43": 41500.0,
            "QB44": 50300.0,
            "QB45": 49100.0,
            "QB46": 48700.0,
            "QB47": 48800.0,
            "QB48": 49900.0,
            "QB49": 48200.0,
            "QB50": 49600.0,
            "QB51": 42700.0,
            "QB52": 50100.0,
            "QB53": 47500.0,
            "QB54": 48300.0,
        },
        t2s={
            "QB1": 09100.0,
            "QB2": 10100.0,
            "QB3": 10900.0,
            "QB4": 09600.0,
            "QB5": 08900.0,
            "QB6": 10200.0,
            "QB7": 08500.0,
            "QB8": 09000.0,
            "QB9": 09300.0,
            "QB10": 09800.0,
            "QB11": 09400.0,
            "QB12": 09900.0,
            "QB13": 10000.0,
            "QB14": 09000.0,
            "QB15": 09500.0,
            "QB16": 09700.0,
            "QB17": 10100.0,
            "QB18": 09200.0,
            "QB19": 08200.0,
            "QB20": 12000.0,
            "QB21": 09100.0,
            "QB22": 10100.0,
            "QB23": 10900.0,
            "QB24": 09600.0,
            "QB25": 08900.0,
            "QB26": 10200.0,
            "QB27": 08500.0,
            "QB28": 09000.0,
            "QB29": 09300.0,
            "QB30": 09800.0,
            "QB31": 09400.0,
            "QB32": 09900.0,
            "QB33": 10000.0,
            "QB34": 09000.0,
            "QB35": 09500.0,
            "QB36": 09700.0,
            "QB37": 10100.0,
            "QB38": 09200.0,
            "QB39": 08200.0,
            "QB40": 12000.0,
            "QB41": 09100.0,
            "QB42": 10100.0,
            "QB43": 10900.0,
            "QB44": 09600.0,
            "QB45": 08900.0,
            "QB46": 10200.0,
            "QB47": 08500.0,
            "QB48": 09000.0,
            "QB49": 09300.0,
            "QB50": 09800.0,
            "QB51": 09400.0,
            "QB52": 09900.0,
            "QB53": 10000.0,
            "QB54": 09000.0,
        },
        single_qubit_gate_depolarizing_error_parameters={
            "prx": {
                "QB1": 0.00116,
                "QB2": 0.00102,
                "QB3": 0.00182,
                "QB4": 0.00100,
                "QB5": 0.00119,
                "QB6": 0.00110,
                "QB7": 0.00124,
                "QB8": 0.00109,
                "QB9": 0.00111,
                "QB10": 0.00132,
                "QB11": 0.00114,
                "QB12": 0.00116,
                "QB13": 0.00112,
                "QB14": 0.00107,
                "QB15": 0.00211,
                "QB16": 0.00119,
                "QB17": 0.00126,
                "QB18": 0.00133,
                "QB19": 0.00160,
                "QB20": 0.00115,
                "QB21": 0.00116,
                "QB22": 0.00102,
                "QB23": 0.00182,
                "QB24": 0.00100,
                "QB25": 0.00119,
                "QB26": 0.00110,
                "QB27": 0.00124,
                "QB28": 0.00109,
                "QB29": 0.00111,
                "QB30": 0.00132,
                "QB31": 0.00114,
                "QB32": 0.00116,
                "QB33": 0.00112,
                "QB34": 0.00107,
                "QB35": 0.00211,
                "QB36": 0.00119,
                "QB37": 0.00126,
                "QB38": 0.00133,
                "QB39": 0.00160,
                "QB40": 0.00115,
                "QB41": 0.00116,
                "QB42": 0.00102,
                "QB43": 0.00182,
                "QB44": 0.00100,
                "QB45": 0.00119,
                "QB46": 0.00110,
                "QB47": 0.00124,
                "QB48": 0.00109,
                "QB49": 0.00111,
                "QB50": 0.00132,
                "QB51": 0.00114,
                "QB52": 0.00116,
                "QB53": 0.00112,
                "QB54": 0.00107,
            }
        },
        two_qubit_gate_depolarizing_error_parameters={
            "cz": {
                ("QB1", "QB2"): 0.0120,
                ("QB1", "QB5"): 0.0150,
                ("QB2", "QB6"): 0.0121,
                ("QB3", "QB4"): 0.0102,
                ("QB3", "QB9"): 0.0150,
                ("QB4", "QB5"): 0.0150,
                ("QB4", "QB10"): 0.0103,
                ("QB5", "QB6"): 0.0150,
                ("QB5", "QB11"): 0.0150,
                ("QB6", "QB7"): 0.0160,
                ("QB6", "QB12"): 0.0117,
                ("QB7", "QB13"): 0.0098,
                ("QB8", "QB9"): 0.0210,
                ("QB8", "QB16"): 0.0150,
                ("QB9", "QB10"): 0.0187,
                ("QB9", "QB17"): 0.0135,
                ("QB10", "QB11"): 0.0141,
                ("QB10", "QB18"): 0.0150,
                ("QB11", "QB12"): 0.0192,
                ("QB11", "QB19"): 0.0150,
                ("QB12", "QB13"): 0.0183,
                ("QB12", "QB20"): 0.0133,
                ("QB13", "QB14"): 0.0150,
                ("QB13", "QB21"): 0.0109,
                ("QB14", "QB22"): 0.0150,
                ("QB15", "QB16"): 0.0150,
                ("QB15", "QB23"): 0.0134,
                ("QB16", "QB17"): 0.0150,
                ("QB16", "QB24"): 0.0150,
                ("QB17", "QB18"): 0.0150,
                ("QB17", "QB25"): 0.0150,
                ("QB18", "QB19"): 0.0150,
                ("QB18", "QB26"): 0.0150,
                ("QB19", "QB20"): 0.0150,
                ("QB19", "QB27"): 0.0150,
                ("QB20", "QB21"): 0.0122,
                ("QB20", "QB28"): 0.0100,
                ("QB21", "QB22"): 0.0201,
                ("QB21", "QB29"): 0.0180,
                ("QB22", "QB30"): 0.0127,
                ("QB23", "QB24"): 0.0142,
                ("QB24", "QB25"): 0.0150,
                ("QB24", "QB32"): 0.0191,
                ("QB25", "QB26"): 0.0150,
                ("QB25", "QB33"): 0.0150,
                ("QB26", "QB27"): 0.0146,
                ("QB26", "QB34"): 0.0162,
                ("QB27", "QB28"): 0.0133,
                ("QB27", "QB35"): 0.0220,
                ("QB28", "QB29"): 0.0190,
                ("QB28", "QB36"): 0.0114,
                ("QB29", "QB30"): 0.0120,
                ("QB29", "QB37"): 0.0121,
                ("QB30", "QB31"): 0.0102,
                ("QB30", "QB38"): 0.0150,
                ("QB31", "QB39"): 0.0103,
                ("QB32", "QB33"): 0.0160,
                ("QB32", "QB40"): 0.0117,
                ("QB33", "QB34"): 0.0098,
                ("QB33", "QB41"): 0.0210,
                ("QB34", "QB35"): 0.0187,
                ("QB34", "QB42"): 0.0135,
                ("QB35", "QB36"): 0.0141,
                ("QB35", "QB43"): 0.0192,
                ("QB36", "QB37"): 0.0183,
                ("QB36", "QB44"): 0.0133,
                ("QB37", "QB38"): 0.0109,
                ("QB37", "QB45"): 0.0134,
                ("QB38", "QB39"): 0.0122,
                ("QB38", "QB46"): 0.0100,
                ("QB40", "QB41"): 0.0201,
                ("QB41", "QB42"): 0.0180,
                ("QB41", "QB47"): 0.0150,
                ("QB42", "QB43"): 0.0127,
                ("QB42", "QB48"): 0.0150,
                ("QB43", "QB44"): 0.0142,
                ("QB43", "QB49"): 0.0150,
                ("QB44", "QB45"): 0.0191,
                ("QB44", "QB50"): 0.0146,
                ("QB45", "QB46"): 0.0162,
                ("QB45", "QB51"): 0.0133,
                ("QB47", "QB48"): 0.0150,
                ("QB48", "QB49"): 0.0150,
                ("QB48", "QB52"): 0.0150,
                ("QB49", "QB50"): 0.0150,
                ("QB49", "QB53"): 0.0150,
                ("QB50", "QB51"): 0.0220,
                ("QB50", "QB54"): 0.0190,
                ("QB52", "QB53"): 0.0114,
                ("QB53", "QB54"): 0.0120,
            }
        },
        single_qubit_gate_durations={"prx": 40.0},
        two_qubit_gate_durations={"cz": 120.0},
        readout_errors={
            "QB1": {"0": 0.051, "1": 0.052},
            "QB2": {"0": 0.049, "1": 0.048},
            "QB3": {"0": 0.057, "1": 0.049},
            "QB4": {"0": 0.049, "1": 0.048},
            "QB5": {"0": 0.050, "1": 0.050},
            "QB6": {"0": 0.053, "1": 0.055},
            "QB7": {"0": 0.051, "1": 0.052},
            "QB8": {"0": 0.058, "1": 0.050},
            "QB9": {"0": 0.052, "1": 0.049},
            "QB10": {"0": 0.044, "1": 0.049},
            "QB11": {"0": 0.056, "1": 0.049},
            "QB12": {"0": 0.051, "1": 0.050},
            "QB13": {"0": 0.053, "1": 0.051},
            "QB14": {"0": 0.050, "1": 0.050},
            "QB15": {"0": 0.046, "1": 0.049},
            "QB16": {"0": 0.050, "1": 0.050},
            "QB17": {"0": 0.048, "1": 0.048},
            "QB18": {"0": 0.050, "1": 0.050},
            "QB19": {"0": 0.050, "1": 0.050},
            "QB20": {"0": 0.056, "1": 0.057},
            "QB21": {"0": 0.051, "1": 0.052},
            "QB22": {"0": 0.049, "1": 0.048},
            "QB23": {"0": 0.057, "1": 0.049},
            "QB24": {"0": 0.049, "1": 0.048},
            "QB25": {"0": 0.050, "1": 0.050},
            "QB26": {"0": 0.053, "1": 0.055},
            "QB27": {"0": 0.051, "1": 0.052},
            "QB28": {"0": 0.058, "1": 0.050},
            "QB29": {"0": 0.052, "1": 0.049},
            "QB30": {"0": 0.044, "1": 0.049},
            "QB31": {"0": 0.056, "1": 0.049},
            "QB32": {"0": 0.051, "1": 0.050},
            "QB33": {"0": 0.053, "1": 0.051},
            "QB34": {"0": 0.048, "1": 0.049},
            "QB35": {"0": 0.046, "1": 0.049},
            "QB36": {"0": 0.044, "1": 0.051},
            "QB37": {"0": 0.048, "1": 0.048},
            "QB38": {"0": 0.049, "1": 0.052},
            "QB39": {"0": 0.050, "1": 0.051},
            "QB40": {"0": 0.056, "1": 0.057},
            "QB41": {"0": 0.051, "1": 0.052},
            "QB42": {"0": 0.049, "1": 0.048},
            "QB43": {"0": 0.057, "1": 0.049},
            "QB44": {"0": 0.049, "1": 0.048},
            "QB45": {"0": 0.050, "1": 0.051},
            "QB46": {"0": 0.053, "1": 0.055},
            "QB47": {"0": 0.050, "1": 0.050},
            "QB48": {"0": 0.050, "1": 0.050},
            "QB49": {"0": 0.050, "1": 0.050},
            "QB50": {"0": 0.051, "1": 0.052},
            "QB51": {"0": 0.058, "1": 0.050},
            "QB52": {"0": 0.052, "1": 0.049},
            "QB53": {"0": 0.044, "1": 0.049},
            "QB54": {"0": 0.056, "1": 0.049},
        },
        name="sample-aphrodite-noise-model",
    )

    return IQMFakeBackend(architecture, error_profile, name="IQMFakeAphroditeBackend")
