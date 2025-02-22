from typing import Any

from rdkit import Chem
from rdkit.Chem import QED, Mol
from rdkit.Chem.Crippen import MolLogP
from rdkit.Chem.Descriptors import MolWt
from rdkit.Chem.Lipinski import NumHDonors, NumHAcceptors, NumRotatableBonds
from sapiopylib.rest.User import SapioUser


class RdKitHelper:
    """
    A class designed for simplifying and better documenting the behavior of commonly used RDKit functions.
    """
    user: SapioUser
    exp_id: int
    tab_prefix: str

    def __init__(self, user: SapioUser, exp_id: int, tab_prefix: str | None = None):
        """
        :param user: The user to make requests from.
        :param exp_id: The ID of the experiment that the user is in.
        :param tab_prefix: The prefix of the tab for displaying results of functions in.
        """
        self.user = user
        self.exp_id = exp_id
        self.tab_prefix = tab_prefix

    @staticmethod
    def filter_drug_like_compounds(compounds: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """
        Filter the compounds based on Lipinski's Rule of Five and QED score to prioritize drug-like molecules.

        :param compounds: A list of dictionaries, where each dictionary represents a compound with the following
            expected fields:
            - "smiles" (str): SMILES representation of the compound.
            - "record_id" (Any): Unique identifier for the compound.
            - "name" (str): Name of the compound.
        :return: A list of dictionaries representing drug-like compounds with the following fields:
            - "smiles" (str): SMILES representation of the compound.
            - "record_id" (Any): Unique identifier for the compound.
            - "name" (str): Name of the compound.
            - "mw" (float): Molecular weight of the compound.
            - "logp" (float): LogP (lipophilicity) value.
            - "hbd" (int): Number of hydrogen bond donors.
            - "hba" (int): Number of hydrogen bond acceptors.
            - "num_rotatable_bonds" (int): Number of rotatable bonds.
            - "qed_score" (float): QED (Quantitative Estimation of Drug-likeness) score.
        """
        drug_like_compounds: list[dict[str, Any]] = []

        for compound in compounds:
            smiles: str = compound.get("smiles", "")
            try:
                mol: Mol = Chem.MolFromSmiles(smiles)
                if mol is not None:
                    Chem.SanitizeMol(mol)
                    QED.properties(mol)

                    mw = MolWt(mol)
                    logp = MolLogP(mol)
                    hbd = NumHDonors(mol)
                    hba = NumHAcceptors(mol)
                    num_rotatable_bonds = NumRotatableBonds(mol)
                    qed_score = QED.qed(mol)

                    if mw <= 500 and logp <= 5 and hbd <= 5 and hba <= 10 and qed_score >= 0.5:
                        drug_like_compounds.append({
                            "smiles": smiles,
                            "record_id": compound["record_id"],
                            "name": compound["name"],
                            "mw": mw,
                            "logp": logp,
                            "hbd": hbd,
                            "hba": hba,
                            "num_rotatable_bonds": num_rotatable_bonds,
                            "qed_score": qed_score
                        })
            except Exception as e:
                print(f"Error processing SMILES: {smiles} - {e}")

        return drug_like_compounds
