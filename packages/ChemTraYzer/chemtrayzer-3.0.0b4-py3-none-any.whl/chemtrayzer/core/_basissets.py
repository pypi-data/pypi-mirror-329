from chemtrayzer.core.lot import BasisSet

BasisSet._warn_on_creation = True

_basis_sets = {
    "2ZaPa-NR": BasisSet(
        name="2ZaPa-NR",
        description="Double Zeta augmented + polarization (nonrelativistic)",
    ),
    "2ZaPa-NR-CV": BasisSet(
        name="2ZaPa-NR-CV",
        description="Double zeta augmented +polarization (nonrelativistic + "
        "core-valence)",
    ),
    "3-21G": BasisSet(name="3-21G", description="3-21G Split-valence basis set"),
    "3ZaPa-NR": BasisSet(
        name="3ZaPa-NR",
        description="Triple Zeta augmented + polarization (nonrelativistic)",
    ),
    "3ZaPa-NR-CV": BasisSet(
        name="3ZaPa-NR-CV",
        description="Triple zeta augmented + polarization (nonrelativistic +"
        " core-valence)",
    ),
    "4-31G": BasisSet(name="4-31G", description="4-31G valence double-zeta basis set"),
    "4ZaPa-NR": BasisSet(
        name="4ZaPa-NR",
        description="Quadruple Zeta augmented + polarization " "(nonrelativistic)",
    ),
    "4ZaPa-NR-CV": BasisSet(
        name="4ZaPa-NR-CV",
        description="Quadruple zeta augmented + polarization "
        "(nonrelativistic + core-valence)",
    ),
    "5-21G": BasisSet(name="5-21G", description="5-21G Split-valence basis set"),
    "5ZaPa-NR": BasisSet(
        name="5ZaPa-NR",
        description="Quintuple Zeta augmented + polarization " "(nonrelativistic)",
    ),
    "5ZaPa-NR-CV": BasisSet(
        name="5ZaPa-NR-CV",
        description="Quintuple zeta augmented + polarization "
        "(nonrelativistic + core-valence)",
    ),
    "6-21G": BasisSet(name="6-21G", description="6-21G Split-valence basis set"),
    "6-31++G": BasisSet(name="6-31++G", description="6-31G + diffuse on all atoms"),
    "6-31++G*": BasisSet(
        name="6-31++G*",
        description="6-31G + diffuse functions on all atoms, polarization on"
        " heavy atoms",
    ),
    "6-31++G**": BasisSet(
        name="6-31++G**",
        description="6-31G + diffuse and polarization functions on all atoms",
    ),
    "6-31++G**-J": BasisSet(name="6-31++G**-J", description="6-31++G**-J"),
    "6-31+G": BasisSet(name="6-31+G", description="6-31G + diffuse on heavy atoms"),
    "6-31+G*": BasisSet(
        name="6-31+G*",
        description="6-31G + diffuse and polarization functions on heavy " "atoms",
    ),
    "6-31+G*-J": BasisSet(name="6-31+G*-J", description="6-31+G*-J"),
    "6-31+G**": BasisSet(
        name="6-31+G**",
        description="6-31G + diffuse functions on heavy atoms, polarization " "on all",
    ),
    "6-311++G": BasisSet(
        name="6-311++G",
        description="VTZ Valence Triple Zeta: 3 Funct.'s/Valence AO with "
        "diffuse on all atoms",
    ),
    "6-311++G(2d,2p)": BasisSet(name="6-311++G(2d,2p)", description="6-311++G(2d,2p)"),
    "6-311++G(3df,3pd)": BasisSet(
        name="6-311++G(3df,3pd)", description="6-311++G(3df,3pd)"
    ),
    "6-311++G*": BasisSet(
        name="6-311++G*",
        description="VTZ Valence Triple Zeta: 3 Funct.'s/Valence AO with "
        "diffuse on all atoms, polarization on "
        "heavy atoms",
    ),
    "6-311++G**": BasisSet(
        name="6-311++G**",
        description="VTZ Valence Triple Zeta: 3 Funct.'s/Valence AO with "
        "diffuse+polarization on all atoms",
    ),
    "6-311++G**-J": BasisSet(name="6-311++G**-J", description="6-311++G**-J"),
    "6-311+G": BasisSet(
        name="6-311+G",
        description="VTZ Valence Triple Zeta: 3 Funct.'s/Valence AO with "
        "diffuse on heavy atoms",
    ),
    "6-311+G(2d,p)": BasisSet(name="6-311+G(2d,p)", description="6-311+G(2d,p)"),
    "6-311+G*": BasisSet(
        name="6-311+G*",
        description="VTZ Valence Triple Zeta: 3 Funct.'s/Valence AO with "
        "diffuse+polarization on heavy atoms",
    ),
    "6-311+G*-J": BasisSet(name="6-311+G*-J", description="6-311+G*-J"),
    "6-311+G**": BasisSet(
        name="6-311+G**",
        description="VTZ Valence Triple Zeta: 3 Funct.'s/Valence AO with "
        "diffuse on heavy atoms, polarization "
        "on all atoms",
    ),
    "6-311G": BasisSet(
        name="6-311G", description="VTZ Valence Triple Zeta: 3 Funct.'s/Valence AO"
    ),
    "6-311G(2df,2pd)": BasisSet(name="6-311G(2df,2pd)", description="6-311G(2df,2pd)"),
    "6-311G(d,p)": BasisSet(
        name="6-311G(d,p)", description="VTZ Valence Triple Zeta: 3 Funct.'s/Valence AO"
    ),
    "6-311G-J": BasisSet(name="6-311G-J", description="6-311G-J"),
    "6-311G*": BasisSet(
        name="6-311G*", description="VTZ Valence Triple Zeta: 3 Funct.'s/Valence AO"
    ),
    "6-311G**": BasisSet(
        name="6-311G**", description="VTZ Valence Triple Zeta: 3 Funct.'s/Valence AO"
    ),
    "6-311G**-RIFIT": BasisSet(
        name="6-311G**-RIFIT", description="RI-MP2 auxiliary basis for 6-311G** basis"
    ),
    "6-311xxG(d,p)": BasisSet(
        name="6-311xxG(d,p)", description="6-311xxG(d,p) basis set"
    ),
    "6-31G": BasisSet(name="6-31G", description="6-31G valence double-zeta"),
    "6-31G(2df,p)": BasisSet(name="6-31G(2df,p)", description="6-31G(2df,p)"),
    "6-31G(3df,3pd)": BasisSet(name="6-31G(3df,3pd)", description="6-31G(3df,3pd)"),
    "6-31G(d,p)": BasisSet(
        name="6-31G(d,p)", description="6-31G + polarization on all atoms"
    ),
    "6-31G-Blaudeau": BasisSet(
        name="6-31G-Blaudeau",
        description="VDZ     Valence Double Zeta: 2 Funct.'s/Valence AO",
    ),
    "6-31G-J": BasisSet(name="6-31G-J", description="6-31G-J"),
    "6-31G*": BasisSet(
        name="6-31G*", description="6-31G + polarization on heavy atoms"
    ),
    "6-31G*-Blaudeau": BasisSet(
        name="6-31G*-Blaudeau",
        description="VDZP    Valence Double Zeta + Polarization on All Atoms",
    ),
    "6-31G**": BasisSet(
        name="6-31G**", description="6-31G + polarization on all atoms"
    ),
    "6-31G**-RIFIT": BasisSet(
        name="6-31G**-RIFIT", description="RI-MP2 auxiliary basis for 6-31G** basis"
    ),
    "6ZaPa-NR": BasisSet(
        name="6ZaPa-NR",
        description="Sextuple Zeta augmented + polarization " "(nonrelativistic)",
    ),
    "7ZaPa-NR": BasisSet(
        name="7ZaPa-NR", description="7Zeta augmented + polarization (nonrelativistic)"
    ),
    "acv2z-J": BasisSet(
        name="acv2z-J",
        description="acv2z-J basis for indirect nuclear spin-spin coupling",
    ),
    "acv3z-J": BasisSet(
        name="acv3z-J",
        description="acv3z-J basis for indirect nuclear spin-spin coupling",
    ),
    "acv4z-J": BasisSet(
        name="acv4z-J",
        description="acv4z-J basis for indirect nuclear spin-spin coupling",
    ),
    "admm-1": BasisSet(
        name="admm-1",
        description="Auxiliary basis with diffuse functions for use with "
        "pcseg-1 and the Auxiliary-Density "
        "Matrix Method (ADMM)",
    ),
    "admm-2": BasisSet(
        name="admm-2",
        description="Auxiliary basis with diffuse functions for use with "
        "pcseg-2 and the Auxiliary-Density "
        "Matrix Method (ADMM)",
    ),
    "admm-3": BasisSet(
        name="admm-3",
        description="Auxiliary basis with diffuse functions for use with "
        "pcseg-3 and the Auxiliary-Density "
        "Matrix Method (ADMM)",
    ),
    "AHGBS-5": BasisSet(
        name="AHGBS-5",
        description="Hydrogenic Gaussian basis set formed at tolerance "
        "10^{-5} without polarization, with "
        "more diffuse functions",
    ),
    "AHGBS-7": BasisSet(
        name="AHGBS-7",
        description="Hydrogenic Gaussian basis set formed at tolerance "
        "10^{-7} without polarization, with "
        "more diffuse functions",
    ),
    "AHGBS-9": BasisSet(
        name="AHGBS-9",
        description="Hydrogenic Gaussian basis set formed at tolerance "
        "10^{-9} without polarization, with "
        "more diffuse functions",
    ),
    "AHGBSP1-5": BasisSet(
        name="AHGBSP1-5",
        description="Hydrogenic Gaussian basis set formed at tolerance "
        "10^{-5} with 1 polarization shell, "
        "with more diffuse functions",
    ),
    "AHGBSP1-7": BasisSet(
        name="AHGBSP1-7",
        description="Hydrogenic Gaussian basis set formed at tolerance "
        "10^{-7} with 1 polarization shell, "
        "with more diffuse functions",
    ),
    "AHGBSP1-9": BasisSet(
        name="AHGBSP1-9",
        description="Hydrogenic Gaussian basis set formed at tolerance "
        "10^{-9} with 1 polarization shell, "
        "with more diffuse functions",
    ),
    "AHGBSP2-5": BasisSet(
        name="AHGBSP2-5",
        description="Hydrogenic Gaussian basis set formed at tolerance "
        "10^{-5} with 2 polarization shells, "
        "with more diffuse functions",
    ),
    "AHGBSP2-7": BasisSet(
        name="AHGBSP2-7",
        description="Hydrogenic Gaussian basis set formed at tolerance "
        "10^{-7} with 2 polarization shells, "
        "with more diffuse functions",
    ),
    "AHGBSP2-9": BasisSet(
        name="AHGBSP2-9",
        description="Hydrogenic Gaussian basis set formed at tolerance "
        "10^{-9} with 2 polarization shells, "
        "with more diffuse functions",
    ),
    "AHGBSP3-5": BasisSet(
        name="AHGBSP3-5",
        description="Hydrogenic Gaussian basis set formed at tolerance "
        "10^{-5} with 3 polarization shells, "
        "with more diffuse functions",
    ),
    "AHGBSP3-7": BasisSet(
        name="AHGBSP3-7",
        description="Hydrogenic Gaussian basis set formed at tolerance "
        "10^{-7} with 3 polarization shells, "
        "with more diffuse functions",
    ),
    "AHGBSP3-9": BasisSet(
        name="AHGBSP3-9",
        description="Hydrogenic Gaussian basis set formed at tolerance "
        "10^{-9} with 3 polarization shells, "
        "with more diffuse functions",
    ),
    "Ahlrichs pVDZ": BasisSet(
        name="Ahlrichs pVDZ",
        description="VDZP    Valence Double Zeta + Polarization on All Atoms",
    ),
    "Ahlrichs TZV": BasisSet(
        name="Ahlrichs TZV",
        description="VTZ     Valence Triple Zeta: 3 Funct.'s/Valence AO",
    ),
    "Ahlrichs VDZ": BasisSet(
        name="Ahlrichs VDZ",
        description="VDZ     Valence Double Zeta: 2 Funct.'s/Valence AO",
    ),
    "Ahlrichs VTZ": BasisSet(
        name="Ahlrichs VTZ",
        description="VTZ     Valence Triple Zeta: 3 Funct.'s/Valence AO",
    ),
    "ANO-DK3": BasisSet(name="ANO-DK3", description="ANO-DK3"),
    "ANO-R": BasisSet(name="ANO-R", description="ANO-R"),
    "ANO-R0": BasisSet(name="ANO-R0", description="ANO-R0"),
    "ANO-R1": BasisSet(name="ANO-R1", description="ANO-R1"),
    "ANO-R2": BasisSet(name="ANO-R2", description="ANO-R2"),
    "ANO-R3": BasisSet(name="ANO-R3", description="ANO-R3"),
    "ANO-RCC": BasisSet(name="ANO-RCC", description="Full ANO-RCC basis"),
    "ANO-RCC-MB": BasisSet(name="ANO-RCC-MB", description="ANO-RCC-MB"),
    "ANO-RCC-VDZ": BasisSet(name="ANO-RCC-VDZ", description="ANO-RCC-VDZ"),
    "ANO-RCC-VDZP": BasisSet(name="ANO-RCC-VDZP", description="ANO-RCC-VDZP"),
    "ANO-RCC-VQZP": BasisSet(name="ANO-RCC-VQZP", description="ANO-RCC-VQZP"),
    "ANO-RCC-VTZ": BasisSet(name="ANO-RCC-VTZ", description="ANO-RCC-VTZ"),
    "ANO-RCC-VTZP": BasisSet(name="ANO-RCC-VTZP", description="ANO-RCC-VTZP"),
    "ANO-VT-DZ": BasisSet(
        name="ANO-VT-DZ",
        description="ANO-VT-DZ (Atomic Natural Orbital - Virial Theorem - "
        "Double Zeta)",
    ),
    "ANO-VT-QZ": BasisSet(
        name="ANO-VT-QZ",
        description="ANO-VT-QZ (Atomic Natural Orbital - Virial Theorem - "
        "Quadruple Zeta)",
    ),
    "ANO-VT-TZ": BasisSet(
        name="ANO-VT-TZ",
        description="ANO-VT-TZ (Atomic Natural Orbital - Virial Theorem - "
        "Triple Zeta)",
    ),
    "apr-cc-pV(Q+d)Z": BasisSet(
        name="apr-cc-pV(Q+d)Z", description="apr-cc-pV(Q+d)Z basis of Papajak/Truhlar"
    ),
    "ATZP-ZORA": BasisSet(
        name="ATZP-ZORA",
        description="ATZP-ZORA, augmented all-electron triple-zeta basis for"
        " calculations with the ZORA approach",
    ),
    "aug-admm-1": BasisSet(
        name="aug-admm-1",
        description="Auxiliary basis with diffuse functions for use with "
        "aug-pcseg-1 and the Auxiliary-Density "
        "Matrix Method (ADMM)",
    ),
    "aug-admm-2": BasisSet(
        name="aug-admm-2",
        description="Auxiliary basis with diffuse functions for use with "
        "aug-pcseg-2 and the Auxiliary-Density "
        "Matrix Method (ADMM)",
    ),
    "aug-admm-3": BasisSet(
        name="aug-admm-3",
        description="Auxiliary basis with diffuse functions for use with "
        "aug-pcseg-3 and the Auxiliary-Density "
        "Matrix Method (ADMM)",
    ),
    "aug-cc-pCV5Z": BasisSet(
        name="aug-cc-pCV5Z",
        description="5ZP Quintuple Zeta + Polarization + Tight Core + " "Diffuse",
    ),
    "aug-cc-pCVDZ": BasisSet(
        name="aug-cc-pCVDZ",
        description="DZP Double Zeta + Polarization + Tight Core + Diffuse",
    ),
    "aug-cc-pCVDZ-DK": BasisSet(
        name="aug-cc-pCVDZ-DK",
        description="VDZP Douglas-Kroll Valence Double Zeta + Polarization +"
        " Tight core + Diffuse",
    ),
    "aug-cc-pCVQZ": BasisSet(
        name="aug-cc-pCVQZ",
        description="QZP Quadruple Zeta + Polarization + Tight Core + " "Diffuse",
    ),
    "aug-cc-pCVQZ-DK": BasisSet(
        name="aug-cc-pCVQZ-DK",
        description="QZ3PD Douglas-Kroll Valence Double Zeta + Polarization "
        "+ Tight core + Diffuse",
    ),
    "aug-cc-pCVTZ": BasisSet(
        name="aug-cc-pCVTZ",
        description="TZP Triple Zeta + Polarization + Tight Core + Diffuse",
    ),
    "aug-cc-pCVTZ-DK": BasisSet(
        name="aug-cc-pCVTZ-DK",
        description="Triple-Zeta Douglas-Kroll Valence Double Zeta + "
        "Polarization + Tight core + Diffuse",
    ),
    "aug-cc-pV(5+d)Z": BasisSet(name="aug-cc-pV(5+d)Z", description="aug-cc-pV(5+d)Z"),
    "aug-cc-pV(D+d)Z": BasisSet(name="aug-cc-pV(D+d)Z", description="aug-cc-pV(D+d)Z"),
    "aug-cc-pV(Q+d)Z": BasisSet(name="aug-cc-pV(Q+d)Z", description="aug-cc-pV(Q+d)Z"),
    "aug-cc-pV(T+d)Z": BasisSet(name="aug-cc-pV(T+d)Z", description="aug-cc-pV(T+d)Z"),
    "aug-cc-pV5Z": BasisSet(name="aug-cc-pV5Z", description="aug-cc-pV5Z"),
    "aug-cc-pV5Z-DK": BasisSet(
        name="aug-cc-pV5Z-DK",
        description="V5ZPD   All-electron Douglas-Kroll Valence Quintuple "
        "Zeta + Polarization",
    ),
    "aug-cc-pV5Z-OPTRI": BasisSet(
        name="aug-cc-pV5Z-OPTRI", description="aug-cc-pV5Z-OPTRI"
    ),
    "aug-cc-pV5Z-PP": BasisSet(name="aug-cc-pV5Z-PP", description="aug-cc-pV5Z-PP"),
    "aug-cc-pV5Z-PP-OPTRI": BasisSet(
        name="aug-cc-pV5Z-PP-OPTRI", description="aug-cc-pV5Z-PP-OPTRI"
    ),
    "aug-cc-pV5Z-PP-RIFIT": BasisSet(
        name="aug-cc-pV5Z-PP-RIFIT", description="aug-cc-pV5Z-PP-RIFIT"
    ),
    "aug-cc-pV5Z-RIFIT": BasisSet(
        name="aug-cc-pV5Z-RIFIT",
        description="RI Fitting basis for use with aug-cc-pV5Z",
    ),
    "aug-cc-pV6Z": BasisSet(name="aug-cc-pV6Z", description="aug-cc-pV6Z"),
    "aug-cc-pV6Z-RIFIT": BasisSet(
        name="aug-cc-pV6Z-RIFIT",
        description="RI Fitting basis for use with aug-cc-pV6Z",
    ),
    "aug-cc-pV7Z": BasisSet(name="aug-cc-pV7Z", description="aug-cc-pV7Z"),
    "aug-cc-pVDZ": BasisSet(name="aug-cc-pVDZ", description="aug-cc-pVDZ"),
    "aug-cc-pVDZ-DK": BasisSet(
        name="aug-cc-pVDZ-DK",
        description="VDZ2PD All-electron Douglas-Kroll Valence Double Zeta +"
        " Polarization",
    ),
    "aug-cc-pVDZ-DK3": BasisSet(name="aug-cc-pVDZ-DK3", description="aug-cc-pVDZ-DK3"),
    "aug-cc-pVDZ-OPTRI": BasisSet(
        name="aug-cc-pVDZ-OPTRI", description="aug-cc-pVDZ-OPTRI"
    ),
    "aug-cc-pVDZ-PP": BasisSet(name="aug-cc-pVDZ-PP", description="aug-cc-pVDZ-PP"),
    "aug-cc-pVDZ-PP-OPTRI": BasisSet(
        name="aug-cc-pVDZ-PP-OPTRI", description="aug-cc-pVDZ-PP-OPTRI"
    ),
    "aug-cc-pVDZ-PP-RIFIT": BasisSet(
        name="aug-cc-pVDZ-PP-RIFIT", description="aug-cc-pVDZ-PP-RIFIT"
    ),
    "aug-cc-pVDZ-RIFIT": BasisSet(
        name="aug-cc-pVDZ-RIFIT",
        description="RI Fitting basis for use with aug-cc-pVDZ",
    ),
    "aug-cc-pVDZ-X2C": BasisSet(name="aug-cc-pVDZ-X2C", description="aug-cc-pVDZ-X2C"),
    "aug-cc-pVQZ": BasisSet(name="aug-cc-pVQZ", description="aug-cc-pVQZ"),
    "aug-cc-pVQZ-DK": BasisSet(
        name="aug-cc-pVQZ-DK",
        description="VQZPD   All-electron Douglas-Kroll Valence Quadruple "
        "Zeta + Polarization",
    ),
    "aug-cc-pVQZ-DK3": BasisSet(name="aug-cc-pVQZ-DK3", description="aug-cc-pVQZ-DK3"),
    "aug-cc-pVQZ-OPTRI": BasisSet(
        name="aug-cc-pVQZ-OPTRI", description="aug-cc-pVQZ-OPTRI"
    ),
    "aug-cc-pVQZ-PP": BasisSet(name="aug-cc-pVQZ-PP", description="aug-cc-pVQZ-PP"),
    "aug-cc-pVQZ-PP-OPTRI": BasisSet(
        name="aug-cc-pVQZ-PP-OPTRI", description="aug-cc-pVQZ-PP-OPTRI"
    ),
    "aug-cc-pVQZ-PP-RIFIT": BasisSet(
        name="aug-cc-pVQZ-PP-RIFIT", description="aug-cc-pVQZ-PP-RIFIT"
    ),
    "aug-cc-pVQZ-RIFIT": BasisSet(
        name="aug-cc-pVQZ-RIFIT",
        description="RI Fitting basis for use with aug-cc-pVQZ",
    ),
    "aug-cc-pVQZ-X2C": BasisSet(name="aug-cc-pVQZ-X2C", description="aug-cc-pVQZ-X2C"),
    "aug-cc-pVTZ": BasisSet(name="aug-cc-pVTZ", description="aug-cc-pVTZ"),
    "aug-cc-pVTZ-DK": BasisSet(
        name="aug-cc-pVTZ-DK",
        description="VTZ2P   All-electron Douglas-Kroll Valence Triple Zeta "
        "+ Polarization",
    ),
    "aug-cc-pVTZ-DK3": BasisSet(name="aug-cc-pVTZ-DK3", description="aug-cc-pVTZ-DK3"),
    "aug-cc-pVTZ-J": BasisSet(name="aug-cc-pVTZ-J", description="aug-cc-pVTZ-J"),
    "aug-cc-pVTZ-OPTRI": BasisSet(
        name="aug-cc-pVTZ-OPTRI", description="aug-cc-pVTZ-OPTRI"
    ),
    "aug-cc-pVTZ-PP": BasisSet(name="aug-cc-pVTZ-PP", description="aug-cc-pVTZ-PP"),
    "aug-cc-pVTZ-PP-OPTRI": BasisSet(
        name="aug-cc-pVTZ-PP-OPTRI", description="aug-cc-pVTZ-PP-OPTRI"
    ),
    "aug-cc-pVTZ-PP-RIFIT": BasisSet(
        name="aug-cc-pVTZ-PP-RIFIT", description="aug-cc-pVTZ-PP-RIFIT"
    ),
    "aug-cc-pVTZ-RIFIT": BasisSet(
        name="aug-cc-pVTZ-RIFIT",
        description="RI Fitting basis for use with aug-cc-pVTZ",
    ),
    "aug-cc-pVTZ-X2C": BasisSet(name="aug-cc-pVTZ-X2C", description="aug-cc-pVTZ-X2C"),
    "aug-cc-pwCV5Z": BasisSet(
        name="aug-cc-pwCV5Z",
        description="5Z4P    Quintuple Zeta + Polarization + Tight Core + " "Diffuse",
    ),
    "aug-cc-pwCV5Z-DK": BasisSet(
        name="aug-cc-pwCV5Z-DK",
        description="V5ZPD   All-electron Douglas-Kroll Core-Valence "
        "Quintuple Zeta + Polarization",
    ),
    "aug-cc-pwCV5Z-PP": BasisSet(
        name="aug-cc-pwCV5Z-PP", description="aug-cc-pwCV5Z-PP"
    ),
    "aug-cc-pwCV5Z-PP-OPTRI": BasisSet(
        name="aug-cc-pwCV5Z-PP-OPTRI", description="aug-cc-pwCV5Z-PP-OPTRI"
    ),
    "aug-cc-pwCV5Z-PP-RIFIT": BasisSet(
        name="aug-cc-pwCV5Z-PP-RIFIT", description="aug-cc-pwCV5Z-PP-RIFIT"
    ),
    "aug-cc-pwCV5Z-RIFIT": BasisSet(
        name="aug-cc-pwCV5Z-RIFIT",
        description="RI Fitting basis for use with aug-cc-pwCV5Z",
    ),
    "aug-cc-pwCVDZ": BasisSet(
        name="aug-cc-pwCVDZ",
        description="DZP     Double Zeta + Polarization + Tight Core + " "Diffuse",
    ),
    "aug-cc-pwCVDZ-DK3": BasisSet(
        name="aug-cc-pwCVDZ-DK3", description="aug-cc-pwCVDZ-DK3"
    ),
    "aug-cc-pwCVDZ-PP": BasisSet(
        name="aug-cc-pwCVDZ-PP", description="aug-cc-pwCVDZ-PP"
    ),
    "aug-cc-pwCVDZ-PP-OPTRI": BasisSet(
        name="aug-cc-pwCVDZ-PP-OPTRI", description="aug-cc-pwCVDZ-PP-OPTRI"
    ),
    "aug-cc-pwCVDZ-PP-RIFIT": BasisSet(
        name="aug-cc-pwCVDZ-PP-RIFIT", description="aug-cc-pwCVDZ-PP-RIFIT"
    ),
    "aug-cc-pwCVDZ-RIFIT": BasisSet(
        name="aug-cc-pwCVDZ-RIFIT",
        description="RI Fitting basis for use with aug-cc-pwCVDZ",
    ),
    "aug-cc-pwCVDZ-X2C": BasisSet(
        name="aug-cc-pwCVDZ-X2C", description="aug-cc-pwCVDZ-X2C"
    ),
    "aug-cc-pwCVQZ": BasisSet(
        name="aug-cc-pwCVQZ",
        description="QZ3P    Quadruple Zeta + Polarization + Tight Core + " "diffuse",
    ),
    "aug-cc-pwCVQZ-DK": BasisSet(
        name="aug-cc-pwCVQZ-DK",
        description="VQZPD   All-electron Douglas-Kroll Core-Valence "
        "Quadruple Zeta + Polarization",
    ),
    "aug-cc-pwCVQZ-DK3": BasisSet(
        name="aug-cc-pwCVQZ-DK3", description="aug-cc-pwCVQZ-DK3"
    ),
    "aug-cc-pwCVQZ-PP": BasisSet(
        name="aug-cc-pwCVQZ-PP", description="aug-cc-pwCVQZ-PP"
    ),
    "aug-cc-pwCVQZ-PP-OPTRI": BasisSet(
        name="aug-cc-pwCVQZ-PP-OPTRI", description="aug-cc-pwCVQZ-PP-OPTRI"
    ),
    "aug-cc-pwCVQZ-PP-RIFIT": BasisSet(
        name="aug-cc-pwCVQZ-PP-RIFIT", description="aug-cc-pwCVQZ-PP-RIFIT"
    ),
    "aug-cc-pwCVQZ-RIFIT": BasisSet(
        name="aug-cc-pwCVQZ-RIFIT",
        description="RI Fitting basis for use with aug-cc-pwCVQZ",
    ),
    "aug-cc-pwCVQZ-X2C": BasisSet(
        name="aug-cc-pwCVQZ-X2C", description="aug-cc-pwCVQZ-X2C"
    ),
    "aug-cc-pwCVTZ": BasisSet(
        name="aug-cc-pwCVTZ",
        description="TZ2P    Triple Zeta + Polarization + Tight Core + " "Diffuse",
    ),
    "aug-cc-pwCVTZ-DK": BasisSet(
        name="aug-cc-pwCVTZ-DK",
        description="VTZ2P   All-electron Douglas-Kroll Core-Valence Triple "
        "Zeta + Polarization",
    ),
    "aug-cc-pwCVTZ-DK3": BasisSet(
        name="aug-cc-pwCVTZ-DK3", description="aug-cc-pwCVTZ-DK3"
    ),
    "aug-cc-pwCVTZ-PP": BasisSet(
        name="aug-cc-pwCVTZ-PP", description="aug-cc-pwCVTZ-PP"
    ),
    "aug-cc-pwCVTZ-PP-OPTRI": BasisSet(
        name="aug-cc-pwCVTZ-PP-OPTRI", description="aug-cc-pwCVTZ-PP-OPTRI"
    ),
    "aug-cc-pwCVTZ-PP-RIFIT": BasisSet(
        name="aug-cc-pwCVTZ-PP-RIFIT", description="aug-cc-pwCVTZ-PP-RIFIT"
    ),
    "aug-cc-pwCVTZ-RIFIT": BasisSet(
        name="aug-cc-pwCVTZ-RIFIT",
        description="RI Fitting basis for use with aug-cc-pwCVTZ",
    ),
    "aug-cc-pwCVTZ-X2C": BasisSet(
        name="aug-cc-pwCVTZ-X2C", description="aug-cc-pwCVTZ-X2C"
    ),
    "aug-ccX-5Z": BasisSet(
        name="aug-ccX-5Z",
        description="Augmented basis set for calculation of core excitations"
        " by the correlated wave function "
        "linear response and equation-of-motion"
        " methods",
    ),
    "aug-ccX-DZ": BasisSet(
        name="aug-ccX-DZ",
        description="Augmented basis set for calculation of core excitations"
        " by the correlated wave function "
        "linear response and equation-of-motion"
        " methods",
    ),
    "aug-ccX-QZ": BasisSet(
        name="aug-ccX-QZ",
        description="Augmented basis set for calculation of core excitations"
        " by the correlated wave function "
        "linear response and equation-of-motion"
        " methods",
    ),
    "aug-ccX-TZ": BasisSet(
        name="aug-ccX-TZ",
        description="Augmented basis set for calculation of core excitations"
        " by the correlated wave function "
        "linear response and equation-of-motion"
        " methods",
    ),
    "aug-mcc-pV5Z": BasisSet(name="aug-mcc-pV5Z", description="aug-mcc-pV5Z"),
    "aug-mcc-pV6Z": BasisSet(name="aug-mcc-pV6Z", description="aug-mcc-pV6Z"),
    "aug-mcc-pV7Z": BasisSet(name="aug-mcc-pV7Z", description="aug-mcc-pV7Z"),
    "aug-mcc-pV8Z": BasisSet(name="aug-mcc-pV8Z", description="aug-mcc-pV8Z"),
    "aug-mcc-pVQZ": BasisSet(name="aug-mcc-pVQZ", description="aug-mcc-pVQZ"),
    "aug-mcc-pVTZ": BasisSet(name="aug-mcc-pVTZ", description="aug-mcc-pVTZ"),
    "aug-pc-0": BasisSet(name="aug-pc-0", description="aug-pc-0"),
    "aug-pc-1": BasisSet(name="aug-pc-1", description="aug-pc-1"),
    "aug-pc-2": BasisSet(name="aug-pc-2", description="aug-pc-2"),
    "aug-pc-3": BasisSet(name="aug-pc-3", description="aug-pc-3"),
    "aug-pc-4": BasisSet(name="aug-pc-4", description="aug-pc-4"),
    "aug-pcH-1": BasisSet(name="aug-pcH-1", description="aug-pcH-1"),
    "aug-pcH-2": BasisSet(name="aug-pcH-2", description="aug-pcH-2"),
    "aug-pcH-3": BasisSet(name="aug-pcH-3", description="aug-pcH-3"),
    "aug-pcH-4": BasisSet(name="aug-pcH-4", description="aug-pcH-4"),
    "aug-pcJ-0": BasisSet(
        name="aug-pcJ-0", description="Contracted version of the aug-pcJ-0 basis"
    ),
    "aug-pcJ-0_2006": BasisSet(name="aug-pcJ-0_2006", description="aug-pcJ-0_2006"),
    "aug-pcJ-1": BasisSet(
        name="aug-pcJ-1", description="Contracted version of the aug-pcJ-1 basis"
    ),
    "aug-pcJ-1_2006": BasisSet(name="aug-pcJ-1_2006", description="aug-pcJ-1_2006"),
    "aug-pcJ-2": BasisSet(
        name="aug-pcJ-2", description="Contracted version of the aug-pcJ-2 basis"
    ),
    "aug-pcJ-2_2006": BasisSet(name="aug-pcJ-2_2006", description="aug-pcJ-2_2006"),
    "aug-pcJ-3": BasisSet(
        name="aug-pcJ-3", description="Contracted version of the aug-pcJ-3 basis"
    ),
    "aug-pcJ-3_2006": BasisSet(name="aug-pcJ-3_2006", description="aug-pcJ-3_2006"),
    "aug-pcJ-4": BasisSet(
        name="aug-pcJ-4", description="Contracted version of the aug-pcJ-4 basis"
    ),
    "aug-pcJ-4_2006": BasisSet(name="aug-pcJ-4_2006", description="aug-pcJ-4_2006"),
    "aug-pcS-0": BasisSet(name="aug-pcS-0", description="aug-pcS-0"),
    "aug-pcS-1": BasisSet(name="aug-pcS-1", description="aug-pcS-1"),
    "aug-pcS-2": BasisSet(name="aug-pcS-2", description="aug-pcS-2"),
    "aug-pcS-3": BasisSet(name="aug-pcS-3", description="aug-pcS-3"),
    "aug-pcS-4": BasisSet(name="aug-pcS-4", description="aug-pcS-4"),
    "aug-pcseg-0": BasisSet(
        name="aug-pcseg-0",
        description="Segmented contracted version of the aug-pc-0 basis",
    ),
    "aug-pcseg-1": BasisSet(
        name="aug-pcseg-1",
        description="Segmented contracted version of the aug-pc-1 basis",
    ),
    "aug-pcseg-2": BasisSet(
        name="aug-pcseg-2",
        description="Segmented contracted version of the aug-pc-2 basis",
    ),
    "aug-pcseg-3": BasisSet(
        name="aug-pcseg-3",
        description="Segmented contracted version of the aug-pc-3 basis",
    ),
    "aug-pcseg-4": BasisSet(
        name="aug-pcseg-4",
        description="Segmented contracted version of the aug-pc-4 basis",
    ),
    "aug-pcSseg-0": BasisSet(
        name="aug-pcSseg-0",
        description="Segmented contracted version of the aug-pcS-0 basis",
    ),
    "aug-pcSseg-1": BasisSet(
        name="aug-pcSseg-1",
        description="Segmented contracted version of the aug-pcS-1 basis",
    ),
    "aug-pcSseg-2": BasisSet(
        name="aug-pcSseg-2",
        description="Segmented contracted version of the aug-pcS-2 basis",
    ),
    "aug-pcSseg-3": BasisSet(
        name="aug-pcSseg-3",
        description="Segmented contracted version of the aug-pcS-3 basis",
    ),
    "aug-pcSseg-4": BasisSet(
        name="aug-pcSseg-4",
        description="Segmented contracted version of the aug-pcS-4 basis",
    ),
    "aug-pcX-1": BasisSet(
        name="aug-pcX-1",
        description="Jensen aug-pcX basis set (containing diffuse functions)"
        " optimized for core-spectroscopy",
    ),
    "aug-pcX-2": BasisSet(
        name="aug-pcX-2",
        description="Jensen aug-pcX basis set (containing diffuse functions)"
        " optimized for core-spectroscopy",
    ),
    "aug-pcX-3": BasisSet(
        name="aug-pcX-3",
        description="Jensen aug-pcX basis set (containing diffuse functions)"
        " optimized for core-spectroscopy",
    ),
    "aug-pcX-4": BasisSet(
        name="aug-pcX-4",
        description="Jensen aug-pcX basis set (containing diffuse functions)"
        " optimized for core-spectroscopy",
    ),
    "aug-pV7Z": BasisSet(
        name="aug-pV7Z",
        description="V7Z6P   Valence Septuple Zeta + Polarization on All " "Atoms",
    ),
    "binning 641": BasisSet(name="binning 641", description="Binning/Curtiss 641"),
    "binning 641(d)": BasisSet(
        name="binning 641(d)", description="Binning/Curtiss 641 + d polarization"
    ),
    "binning 641(df)": BasisSet(
        name="binning 641(df)", description="Binning/Curtiss 641 + df polarization"
    ),
    "binning 641+": BasisSet(
        name="binning 641+", description="Binning/Curtiss 641 + diffuse"
    ),
    "binning 641+(d)": BasisSet(
        name="binning 641+(d)",
        description="Binning/Curtiss 641 + d polarization + diffuse",
    ),
    "binning 641+(df)": BasisSet(
        name="binning 641+(df)",
        description="Binning/Curtiss 641 + df polarization + diffuse",
    ),
    "binning 962": BasisSet(name="binning 962", description="Binning/Curtiss 962"),
    "binning 962(d)": BasisSet(
        name="binning 962(d)", description="Binning/Curtiss 962 + d polarization"
    ),
    "binning 962(df)": BasisSet(
        name="binning 962(df)", description="Binning/Curtiss 962 + df polarization"
    ),
    "binning 962+": BasisSet(
        name="binning 962+", description="Binning/Curtiss 962 + diffuse"
    ),
    "binning 962+(d)": BasisSet(
        name="binning 962+(d)",
        description="Binning/Curtiss 962 + d polarization + diffuse",
    ),
    "binning 962+(df)": BasisSet(
        name="binning 962+(df)",
        description="Binning/Curtiss 962 + df polarization + diffuse",
    ),
    "cc-pCV5Z": BasisSet(name="cc-pCV5Z", description="cc-pCV5Z"),
    "cc-pCVDZ": BasisSet(
        name="cc-pCVDZ", description="DZP Double Zeta + Polarization + Tight Core"
    ),
    "cc-pCVDZ-DK": BasisSet(
        name="cc-pCVDZ-DK",
        description="VDZP Douglas-Kroll Valence Double Zeta + Polarization +"
        " Tight core",
    ),
    "cc-pCVDZ-F12": BasisSet(name="cc-pCVDZ-F12", description="cc-pCVDZ-F12"),
    "cc-pCVDZ-F12-OPTRI": BasisSet(
        name="cc-pCVDZ-F12-OPTRI", description="cc-pCVDZ-F12-OPTRI"
    ),
    "cc-pCVDZ-F12-RIFIT": BasisSet(
        name="cc-pCVDZ-F12-RIFIT", description="cc-pCVDZ-F12 RI Fitting"
    ),
    "cc-pCVQZ": BasisSet(
        name="cc-pCVQZ",
        description="QZ3P    Quadruple Zeta + Polarization + Tight Core",
    ),
    "cc-pCVQZ-DK": BasisSet(
        name="cc-pCVQZ-DK",
        description="QZ3PD Douglas-Kroll Valence Double Zeta + Polarization "
        "+ Tight core",
    ),
    "cc-pCVQZ-F12": BasisSet(name="cc-pCVQZ-F12", description="cc-pCVQZ-F12"),
    "cc-pCVQZ-F12-OPTRI": BasisSet(
        name="cc-pCVQZ-F12-OPTRI", description="cc-pCVQZ-F12-OPTRI"
    ),
    "cc-pCVQZ-F12-RIFIT": BasisSet(
        name="cc-pCVQZ-F12-RIFIT", description="cc-pCVQZ-F12 RI Fitting"
    ),
    "cc-pCVTZ": BasisSet(
        name="cc-pCVTZ", description="TZ2P    Triple Zeta + Polarization + Tight Core"
    ),
    "cc-pCVTZ-DK": BasisSet(
        name="cc-pCVTZ-DK",
        description="Triple-Zeta Douglas-Kroll Valence Double Zeta + "
        "Polarization + Tight core",
    ),
    "cc-pCVTZ-F12": BasisSet(name="cc-pCVTZ-F12", description="cc-pCVTZ-F12"),
    "cc-pCVTZ-F12-OPTRI": BasisSet(
        name="cc-pCVTZ-F12-OPTRI", description="cc-pCVTZ-F12-OPTRI"
    ),
    "cc-pCVTZ-F12-RIFIT": BasisSet(
        name="cc-pCVTZ-F12-RIFIT", description="cc-pCVTZ-F12 RI Fitting"
    ),
    "cc-pV(5+d)Z": BasisSet(name="cc-pV(5+d)Z", description="cc-pV(5+d)Z"),
    "cc-pV(D+d)Z": BasisSet(name="cc-pV(D+d)Z", description="cc-pV(D+d)Z"),
    "cc-pV(Q+d)Z": BasisSet(name="cc-pV(Q+d)Z", description="cc-pV(Q+d)Z"),
    "cc-pV(T+d)Z": BasisSet(name="cc-pV(T+d)Z", description="cc-pV(T+d)Z"),
    "cc-pV5Z": BasisSet(name="cc-pV5Z", description="cc-pV5Z"),
    "cc-pV5Z(fi/sf/fw)": BasisSet(
        name="cc-pV5Z(fi/sf/fw)",
        description="V5Z4P   Relativistic Valence Quintuple Zeta + " "Polarization",
    ),
    "cc-pV5Z(fi/sf/lc)": BasisSet(
        name="cc-pV5Z(fi/sf/lc)",
        description="V5Z4P   Relativistic Valence Quintuple Zeta + " "Polarization",
    ),
    "cc-pV5Z(fi/sf/sc)": BasisSet(
        name="cc-pV5Z(fi/sf/sc)",
        description="V5Z4P   Relativistic Valence Quintuple Zeta + " "Polarization",
    ),
    "cc-pV5Z(pt/sf/fw)": BasisSet(
        name="cc-pV5Z(pt/sf/fw)",
        description="V5Z4P   Relativistic Valence Quintuple Zeta + " "Polarization",
    ),
    "cc-pV5Z(pt/sf/lc)": BasisSet(
        name="cc-pV5Z(pt/sf/lc)",
        description="V5Z4P   Relativistic Valence Quintuple Zeta + " "Polarization",
    ),
    "cc-pV5Z(pt/sf/sc)": BasisSet(
        name="cc-pV5Z(pt/sf/sc)",
        description="V5Z4P   Relativistic Valence Quintuple Zeta + " "Polarization",
    ),
    "cc-pV5Z-DK": BasisSet(
        name="cc-pV5Z-DK",
        description="V5Z4P Douglas-Kroll Valence Quintuple Zeta + " "Polarization",
    ),
    "cc-pV5Z-F12": BasisSet(name="cc-pV5Z-F12", description="cc-pV5Z-F12"),
    "cc-pV5Z-F12(rev2)": BasisSet(
        name="cc-pV5Z-F12(rev2)", description="cc-pV5Z-F12(rev2)"
    ),
    "cc-pV5Z-JKFIT": BasisSet(
        name="cc-pV5Z-JKFIT", description="JK Fitting basis for use with cc-pV5Z"
    ),
    "cc-pV5Z-PP": BasisSet(name="cc-pV5Z-PP", description="cc-pV5Z-PP"),
    "cc-pV5Z-PP-RIFIT": BasisSet(
        name="cc-pV5Z-PP-RIFIT", description="cc-pV5Z-PP-RIFIT"
    ),
    "cc-pV5Z-RIFIT": BasisSet(
        name="cc-pV5Z-RIFIT", description="RI Fitting basis for use with cc-pV5Z"
    ),
    "cc-pV6Z": BasisSet(name="cc-pV6Z", description="cc-pV6Z"),
    "cc-pV6Z-RIFIT": BasisSet(
        name="cc-pV6Z-RIFIT", description="RI Fitting basis for use with cc-pV6Z"
    ),
    "cc-pV8Z": BasisSet(name="cc-pV8Z", description="cc-pV8Z"),
    "cc-pV9Z": BasisSet(
        name="cc-pV9Z",
        description="V7Z6P   Valence Octuple Zeta + Polarization on All " "Atoms",
    ),
    "cc-pVDZ": BasisSet(name="cc-pVDZ", description="cc-pVDZ"),
    "cc-pVDZ(fi/sf/fw)": BasisSet(
        name="cc-pVDZ(fi/sf/fw)",
        description="VDZP    Relativistic Valence Double Zeta + Polarization",
    ),
    "cc-pVDZ(fi/sf/lc)": BasisSet(
        name="cc-pVDZ(fi/sf/lc)",
        description="VDZP    Relativistic Valence Double Zeta + Polarization",
    ),
    "cc-pVDZ(fi/sf/sc)": BasisSet(
        name="cc-pVDZ(fi/sf/sc)",
        description="VDZP    Relativistic Valence Double Zeta + Polarization",
    ),
    "cc-pVDZ(pt/sf/fw)": BasisSet(
        name="cc-pVDZ(pt/sf/fw)",
        description="VDZP    Relativistic Valence Double Zeta + Polarization",
    ),
    "cc-pVDZ(pt/sf/lc)": BasisSet(
        name="cc-pVDZ(pt/sf/lc)",
        description="VDZP    Relativistic Valence Double Zeta + Polarization",
    ),
    "cc-pVDZ(pt/sf/sc)": BasisSet(
        name="cc-pVDZ(pt/sf/sc)",
        description="VDZP    Relativistic Valence Double Zeta + Polarization",
    ),
    "cc-pVDZ(seg-opt)": BasisSet(
        name="cc-pVDZ(seg-opt)",
        description="VDZP    Valence Double Zeta + Polarization on All Atoms",
    ),
    "cc-pVDZ-DK": BasisSet(
        name="cc-pVDZ-DK",
        description="VDZP Douglas-Kroll Valence Double Zeta + Polarization",
    ),
    "cc-pVDZ-DK3": BasisSet(name="cc-pVDZ-DK3", description="cc-pVDZ-DK3"),
    "cc-pVDZ-F12": BasisSet(
        name="cc-pVDZ-F12",
        description="VDZ for explicitly correlated F12 variants of "
        "wavefunction methods",
    ),
    "cc-pVDZ-F12(rev2)": BasisSet(
        name="cc-pVDZ-F12(rev2)", description="cc-pVDZ-F12(rev2)"
    ),
    "cc-pVDZ-F12-OPTRI": BasisSet(
        name="cc-pVDZ-F12-OPTRI", description="cc-pVDZ-F12-OPTRI"
    ),
    "cc-pVDZ-PP": BasisSet(name="cc-pVDZ-PP", description="cc-pVDZ-PP"),
    "cc-pVDZ-PP-RIFIT": BasisSet(
        name="cc-pVDZ-PP-RIFIT", description="cc-pVDZ-PP-RIFIT"
    ),
    "cc-pVDZ-RIFIT": BasisSet(
        name="cc-pVDZ-RIFIT", description="RI Fitting basis for use with cc-pVDZ"
    ),
    "cc-pVDZ-X2C": BasisSet(name="cc-pVDZ-X2C", description="cc-pVDZ-X2C"),
    "cc-pVQZ": BasisSet(name="cc-pVQZ", description="cc-pVQZ"),
    "cc-pVQZ(fi/sf/fw)": BasisSet(
        name="cc-pVQZ(fi/sf/fw)",
        description="VQZ3P   Relativistic Valence Quadruple Zeta + " "Polarization",
    ),
    "cc-pVQZ(fi/sf/lc)": BasisSet(
        name="cc-pVQZ(fi/sf/lc)",
        description="VQZ3P   Relativistic Valence Quadruple Zeta + " "Polarization",
    ),
    "cc-pVQZ(fi/sf/sc)": BasisSet(
        name="cc-pVQZ(fi/sf/sc)",
        description="VQZ3P   Relativistic Valence Quadruple Zeta + " "Polarization",
    ),
    "cc-pVQZ(pt/sf/fw)": BasisSet(
        name="cc-pVQZ(pt/sf/fw)",
        description="VQZ3P   Relativistic Valence Quadruple Zeta + " "Polarization",
    ),
    "cc-pVQZ(pt/sf/lc)": BasisSet(
        name="cc-pVQZ(pt/sf/lc)",
        description="VQZ3P   Relativistic Valence Quadruple Zeta + " "Polarization",
    ),
    "cc-pVQZ(pt/sf/sc)": BasisSet(
        name="cc-pVQZ(pt/sf/sc)",
        description="VQZ3P   Relativistic Valence Quadruple Zeta + " "Polarization",
    ),
    "cc-pVQZ(seg-opt)": BasisSet(
        name="cc-pVQZ(seg-opt)",
        description="VQZ3P   Valence Quadruple Zeta + Polarization on All " "Atoms",
    ),
    "cc-pVQZ-DK": BasisSet(
        name="cc-pVQZ-DK",
        description="VQZ3P Douglas-Kroll Valence Quadruple Zeta + " "Polarization",
    ),
    "cc-pVQZ-DK3": BasisSet(name="cc-pVQZ-DK3", description="cc-pVQZ-DK3"),
    "cc-pVQZ-F12": BasisSet(
        name="cc-pVQZ-F12",
        description="VQZ for explicitly correlated F12 variants of "
        "wavefunction methods",
    ),
    "cc-pVQZ-F12(rev2)": BasisSet(
        name="cc-pVQZ-F12(rev2)", description="cc-pVQZ-F12(rev2)"
    ),
    "cc-pVQZ-F12-OPTRI": BasisSet(
        name="cc-pVQZ-F12-OPTRI", description="cc-pVQZ-F12-OPTRI"
    ),
    "cc-pVQZ-JKFIT": BasisSet(
        name="cc-pVQZ-JKFIT", description="JK Fitting basis for use with cc-pVQZ"
    ),
    "cc-pVQZ-PP": BasisSet(name="cc-pVQZ-PP", description="cc-pVQZ-PP"),
    "cc-pVQZ-PP-RIFIT": BasisSet(
        name="cc-pVQZ-PP-RIFIT", description="cc-pVQZ-PP-RIFIT"
    ),
    "cc-pVQZ-RIFIT": BasisSet(
        name="cc-pVQZ-RIFIT", description="RI Fitting basis for use with cc-pVQZ"
    ),
    "cc-pVQZ-X2C": BasisSet(name="cc-pVQZ-X2C", description="cc-pVQZ-X2C"),
    "cc-pVTZ": BasisSet(name="cc-pVTZ", description="cc-pVTZ"),
    "cc-pVTZ(fi/sf/fw)": BasisSet(
        name="cc-pVTZ(fi/sf/fw)",
        description="VTZ2P   Relativistic Valence Triple Zeta + Polarization",
    ),
    "cc-pVTZ(fi/sf/lc)": BasisSet(
        name="cc-pVTZ(fi/sf/lc)",
        description="VTZ2P   Relativistic Valence Triple Zeta + Polarization",
    ),
    "cc-pVTZ(fi/sf/sc)": BasisSet(
        name="cc-pVTZ(fi/sf/sc)",
        description="VTZ2P   Relativistic Valence Triple Zeta + Polarization",
    ),
    "cc-pVTZ(pt/sf/fw)": BasisSet(
        name="cc-pVTZ(pt/sf/fw)",
        description="VTZ2P   Relativistic Valence Triple Zeta + Polarization",
    ),
    "cc-pVTZ(pt/sf/lc)": BasisSet(
        name="cc-pVTZ(pt/sf/lc)",
        description="VTZ2P   Relativistic Valence Triple Zeta + Polarization",
    ),
    "cc-pVTZ(pt/sf/sc)": BasisSet(
        name="cc-pVTZ(pt/sf/sc)",
        description="VTZ2P   Relativistic Valence Triple Zeta + Polarization",
    ),
    "cc-pVTZ(seg-opt)": BasisSet(
        name="cc-pVTZ(seg-opt)",
        description="VTZ2P   Valence Triple Zeta + Polarization on All Atoms",
    ),
    "cc-pVTZ-DK": BasisSet(
        name="cc-pVTZ-DK",
        description="VTZ2P Douglas-Kroll Valence Triple Zeta + Polarization",
    ),
    "cc-pVTZ-DK3": BasisSet(name="cc-pVTZ-DK3", description="cc-pVTZ-DK3"),
    "cc-pVTZ-F12": BasisSet(
        name="cc-pVTZ-F12",
        description="VTZ for explicitly correlated F12 variants of "
        "wavefunction methods",
    ),
    "cc-pVTZ-F12(rev2)": BasisSet(
        name="cc-pVTZ-F12(rev2)", description="cc-pVTZ-F12(rev2)"
    ),
    "cc-pVTZ-F12-OPTRI": BasisSet(
        name="cc-pVTZ-F12-OPTRI", description="cc-pVTZ-F12-OPTRI"
    ),
    "cc-pVTZ-JKFIT": BasisSet(
        name="cc-pVTZ-JKFIT", description="JK Fitting basis for use with cc-pVTZ"
    ),
    "cc-pVTZ-PP": BasisSet(name="cc-pVTZ-PP", description="cc-pVTZ-PP"),
    "cc-pVTZ-PP-RIFIT": BasisSet(
        name="cc-pVTZ-PP-RIFIT", description="cc-pVTZ-PP-RIFIT"
    ),
    "cc-pVTZ-RIFIT": BasisSet(
        name="cc-pVTZ-RIFIT", description="RI Fitting basis for use with cc-pVTZ"
    ),
    "cc-pVTZ-X2C": BasisSet(name="cc-pVTZ-X2C", description="cc-pVTZ-X2C"),
    "cc-pwCV5Z": BasisSet(
        name="cc-pwCV5Z",
        description="5Z4P    Quintuple Zeta + Polarization + Tight Core",
    ),
    "cc-pwCV5Z-DK": BasisSet(name="cc-pwCV5Z-DK", description="cc-pwCV5Z-DK"),
    "cc-pwCV5Z-PP": BasisSet(name="cc-pwCV5Z-PP", description="cc-pwCV5Z-PP"),
    "cc-pwCV5Z-PP-RIFIT": BasisSet(
        name="cc-pwCV5Z-PP-RIFIT", description="cc-pwCV5Z-PP-RIFIT"
    ),
    "cc-pwCV5Z-RIFIT": BasisSet(
        name="cc-pwCV5Z-RIFIT", description="RI Fitting basis for use with cc-pwCV5Z"
    ),
    "cc-pwCVDZ": BasisSet(
        name="cc-pwCVDZ", description="DZP     Double Zeta + Polarization + Tight Core"
    ),
    "cc-pwCVDZ-DK3": BasisSet(name="cc-pwCVDZ-DK3", description="cc-pwCVDZ-DK3"),
    "cc-pwCVDZ-PP": BasisSet(name="cc-pwCVDZ-PP", description="cc-pwCVDZ-PP"),
    "cc-pwCVDZ-PP-RIFIT": BasisSet(
        name="cc-pwCVDZ-PP-RIFIT", description="cc-pwCVDZ-PP-RIFIT"
    ),
    "cc-pwCVDZ-RIFIT": BasisSet(
        name="cc-pwCVDZ-RIFIT", description="RI Fitting basis for use with cc-pwCVDZ"
    ),
    "cc-pwCVDZ-X2C": BasisSet(name="cc-pwCVDZ-X2C", description="cc-pwCVDZ-X2C"),
    "cc-pwCVQZ": BasisSet(
        name="cc-pwCVQZ",
        description="QZ3P    Quadruple Zeta + Polarization + Tight Core",
    ),
    "cc-pwCVQZ-DK": BasisSet(
        name="cc-pwCVQZ-DK",
        description="QZ3P    All-electron Douglas-Kroll Core-Valence "
        "Quadruple Zeta + Polarization",
    ),
    "cc-pwCVQZ-DK3": BasisSet(name="cc-pwCVQZ-DK3", description="cc-pwCVQZ-DK3"),
    "cc-pwCVQZ-PP": BasisSet(name="cc-pwCVQZ-PP", description="cc-pwCVQZ-PP"),
    "cc-pwCVQZ-PP-RIFIT": BasisSet(
        name="cc-pwCVQZ-PP-RIFIT", description="cc-pwCVQZ-PP-RIFIT"
    ),
    "cc-pwCVQZ-RIFIT": BasisSet(
        name="cc-pwCVQZ-RIFIT", description="RI Fitting basis for use with cc-pwCVQZ"
    ),
    "cc-pwCVQZ-X2C": BasisSet(name="cc-pwCVQZ-X2C", description="cc-pwCVQZ-X2C"),
    "cc-pwCVTZ": BasisSet(
        name="cc-pwCVTZ", description="TZ2P    Triple Zeta + Polarization + Tight Core"
    ),
    "cc-pwCVTZ-DK": BasisSet(name="cc-pwCVTZ-DK", description="cc-pwCVTZ-DK"),
    "cc-pwCVTZ-DK3": BasisSet(name="cc-pwCVTZ-DK3", description="cc-pwCVTZ-DK3"),
    "cc-pwCVTZ-PP": BasisSet(name="cc-pwCVTZ-PP", description="cc-pwCVTZ-PP"),
    "cc-pwCVTZ-PP-RIFIT": BasisSet(
        name="cc-pwCVTZ-PP-RIFIT", description="cc-pwCVTZ-PP-RIFIT"
    ),
    "cc-pwCVTZ-RIFIT": BasisSet(
        name="cc-pwCVTZ-RIFIT", description="RI Fitting basis for use with cc-pwCVTZ"
    ),
    "cc-pwCVTZ-X2C": BasisSet(name="cc-pwCVTZ-X2C", description="cc-pwCVTZ-X2C"),
    "ccemd-2": BasisSet(
        name="ccemd-2",
        description="ccemd-2: Correlation-consistent electron momentum " "density",
    ),
    "ccemd-3": BasisSet(
        name="ccemd-3",
        description="ccemd-3: Correlation-consistent electron momentum " "density",
    ),
    "ccJ-pV5Z": BasisSet(name="ccJ-pV5Z", description="ccJ-pV5Z"),
    "ccJ-pVDZ": BasisSet(name="ccJ-pVDZ", description="ccJ-pVDZ"),
    "ccJ-pVQZ": BasisSet(name="ccJ-pVQZ", description="ccJ-pVQZ"),
    "ccJ-pVTZ": BasisSet(name="ccJ-pVTZ", description="ccJ-pVTZ"),
    "ccX-5Z": BasisSet(
        name="ccX-5Z",
        description="Basis set for calculation of core excitations by the "
        "correlated wave function linear "
        "response and equation-of-motion "
        "methods",
    ),
    "ccX-DZ": BasisSet(
        name="ccX-DZ",
        description="Basis set for calculation of core excitations by the "
        "correlated wave function linear "
        "response and equation-of-motion "
        "methods",
    ),
    "ccX-QZ": BasisSet(
        name="ccX-QZ",
        description="Basis set for calculation of core excitations by the "
        "correlated wave function linear "
        "response and equation-of-motion "
        "methods",
    ),
    "ccX-TZ": BasisSet(
        name="ccX-TZ",
        description="Basis set for calculation of core excitations by the "
        "correlated wave function linear "
        "response and equation-of-motion "
        "methods",
    ),
    "coemd-2": BasisSet(
        name="coemd-2",
        description="coemd-2: completness-optimized for electron momentum " "density",
    ),
    "coemd-3": BasisSet(
        name="coemd-3",
        description="coemd-3: completness-optimized for electron momentum " "density",
    ),
    "coemd-4": BasisSet(
        name="coemd-4",
        description="coemd-4: completness-optimized for electron momentum " "density",
    ),
    "coemd-ref": BasisSet(
        name="coemd-ref",
        description="coemd-ref: completness-optimized for electron momentum " "density",
    ),
    "Cologne DKH2": BasisSet(name="Cologne DKH2", description="Cologne DKH2"),
    "CRENBL": BasisSet(
        name="CRENBL", description="CRENBL designed for use with small core potentials"
    ),
    "CRENBL ECP": BasisSet(
        name="CRENBL ECP",
        description="CRENBL ECP (Large ECP orbital basis for use with small "
        "core potentials)",
    ),
    "CRENBS": BasisSet(
        name="CRENBS", description="CRENBS designed for use with large core potentials"
    ),
    "CRENBS ECP": BasisSet(
        name="CRENBS ECP",
        description="CRENBS ECP (Small ECP orbital basis for use with "
        "relativistic, large core ECPs)",
    ),
    "d-aug-cc-pV5Z": BasisSet(
        name="d-aug-cc-pV5Z",
        description="V5Z4PD  Valence Quintuple Zeta + Polarization + Diffuse",
    ),
    "d-aug-cc-pV6Z": BasisSet(
        name="d-aug-cc-pV6Z",
        description="V6Z5P   Valence Sextuple Zeta + Polarization + Diffuse",
    ),
    "d-aug-cc-pVDZ": BasisSet(
        name="d-aug-cc-pVDZ",
        description="VDZ2PD  Valence Double Zeta + Polarization + Diffuse",
    ),
    "d-aug-cc-pVQZ": BasisSet(
        name="d-aug-cc-pVQZ",
        description="VQZ3PD  Valence Quadruple Zeta + Polarization + Diffuse",
    ),
    "d-aug-cc-pVTZ": BasisSet(
        name="d-aug-cc-pVTZ",
        description="VTZ2PD  Valence Triple Zeta + Polarization + Diffuse",
    ),
    "def2-ECP": BasisSet(
        name="def2-ECP", description="ECP for use with Ahlrichs def2 basis sets"
    ),
    "def2-QZVP": BasisSet(name="def2-QZVP", description="def2-QZVP"),
    "def2-QZVP-RIFIT": BasisSet(
        name="def2-QZVP-RIFIT", description="RIMP2 auxiliary basis for def2-QZVPP"
    ),
    "def2-QZVPD": BasisSet(name="def2-QZVPD", description="def2-QZVPD"),
    "def2-QZVPP": BasisSet(name="def2-QZVPP", description="def2-QZVPP"),
    "def2-QZVPP-RIFIT": BasisSet(
        name="def2-QZVPP-RIFIT", description="RIMP2 auxiliary basis for def2-QZVPP"
    ),
    "def2-QZVPPD": BasisSet(name="def2-QZVPPD", description="def2-QZVPPD"),
    "def2-QZVPPD-RIFIT": BasisSet(
        name="def2-QZVPPD-RIFIT", description="def2-QZVPPD-RIFIT"
    ),
    "def2-SV(P)": BasisSet(name="def2-SV(P)", description="def2-SV(P)"),
    "def2-SV(P)-JKFIT": BasisSet(
        name="def2-SV(P)-JKFIT",
        description="Coulomb/Exchange fitting auxiliary basis for def2 basis" " sets",
    ),
    "def2-SV(P)-RIFIT": BasisSet(
        name="def2-SV(P)-RIFIT", description="RIMP2 auxiliary basis for def2-SV(P)"
    ),
    "def2-SVP": BasisSet(name="def2-SVP", description="def2-SVP"),
    "def2-SVP-RIFIT": BasisSet(name="def2-SVP-RIFIT", description="def2-SVP-RIFIT"),
    "def2-SVPD": BasisSet(name="def2-SVPD", description="def2-SVPD"),
    "def2-SVPD-RIFIT": BasisSet(name="def2-SVPD-RIFIT", description="def2-SVPD-RIFIT"),
    "def2-TZVP": BasisSet(name="def2-TZVP", description="def2-TZVP"),
    "def2-TZVP-RIFIT": BasisSet(
        name="def2-TZVP-RIFIT", description="RIMP2 auxiliary basis for def2-TZVP"
    ),
    "def2-TZVPD": BasisSet(name="def2-TZVPD", description="def2-TZVPD"),
    "def2-TZVPD-RIFIT": BasisSet(
        name="def2-TZVPD-RIFIT", description="def2-TZVPD-RIFIT"
    ),
    "def2-TZVPP": BasisSet(name="def2-TZVPP", description="def2-TZVPP"),
    "def2-TZVPP-RIFIT": BasisSet(
        name="def2-TZVPP-RIFIT", description="def2-TZVPP-RIFIT"
    ),
    "def2-TZVPPD": BasisSet(name="def2-TZVPPD", description="def2-TZVPPD"),
    "def2-TZVPPD-RIFIT": BasisSet(
        name="def2-TZVPPD-RIFIT", description="def2-TZVPPD-RIFIT"
    ),
    "def2-universal-JFIT": BasisSet(
        name="def2-universal-JFIT",
        description="Coulomb fitting auxiliary basis for def2 basis sets",
    ),
    "def2-universal-JKFIT": BasisSet(
        name="def2-universal-JKFIT",
        description="Coulomb/Exchange fitting auxiliary basis for def2 basis" " sets",
    ),
    "deMon2k-DZVP-GGA": BasisSet(
        name="deMon2k-DZVP-GGA", description="DZVP-GGA basis of the deMon2k code"
    ),
    "DFO+-NRLMOL": BasisSet(name="DFO+-NRLMOL", description="DFO+ basis from NRLMOL"),
    "DFO-1": BasisSet(
        name="DFO-1",
        description="Optimized gaussian basis set for Density-functional "
        "calculations",
    ),
    "DFO-1-BHS": BasisSet(
        name="DFO-1-BHS",
        description="Optimized gaussian basis set for Density-functional "
        "calculations (requiring "
        "pseudopotential)",
    ),
    "DFO-2": BasisSet(
        name="DFO-2",
        description="Optimized gaussian basis set for Density-functional "
        "calculations",
    ),
    "DFO-NRLMOL": BasisSet(name="DFO-NRLMOL", description="DFO basis from NRLMOL"),
    "dgauss-a1-dftjfit": BasisSet(
        name="dgauss-a1-dftjfit", description="DGauss A1 DFT Columb Fitting"
    ),
    "dgauss-a1-dftxfit": BasisSet(
        name="dgauss-a1-dftxfit", description="DGauss A1 DFT Exchange Fitting"
    ),
    "dgauss-a2-dftjfit": BasisSet(
        name="dgauss-a2-dftjfit", description="DGauss A2 DFT Columb Fitting"
    ),
    "dgauss-a2-dftxfit": BasisSet(
        name="dgauss-a2-dftxfit", description="DGauss A2 DFT Exchange Fitting"
    ),
    "dgauss-dzvp": BasisSet(
        name="dgauss-dzvp",
        description="VDZP Valence Double Zeta + Polarization designed for " "DFT",
    ),
    "dgauss-dzvp2": BasisSet(
        name="dgauss-dzvp2",
        description="VDZP Valence Double Zeta + Polarization designed for " "DFT",
    ),
    "dgauss-tzvp": BasisSet(
        name="dgauss-tzvp",
        description="VTZP Valence Triple Zeta + Polarization designed for " "DFT",
    ),
    "dhf-ECP": BasisSet(name="dhf-ECP", description="dhf-ECP"),
    "dhf-QZVP": BasisSet(name="dhf-QZVP", description="dhf-QZVP"),
    "dhf-QZVPP": BasisSet(name="dhf-QZVPP", description="dhf-QZVPP"),
    "dhf-SV(P)": BasisSet(name="dhf-SV(P)", description="dhf-SV(P)"),
    "dhf-SVP": BasisSet(name="dhf-SVP", description="dhf-SVP"),
    "dhf-TZVP": BasisSet(name="dhf-TZVP", description="dhf-TZVP"),
    "dhf-TZVPP": BasisSet(name="dhf-TZVPP", description="dhf-TZVPP"),
    "DZ (Dunning-Hay)": BasisSet(
        name="DZ (Dunning-Hay)", description="DZ      Double Zeta: 2 Functions/AO"
    ),
    "DZ + Double Rydberg (Dunning-Hay)": BasisSet(
        name="DZ + Double Rydberg (Dunning-Hay)",
        description="DZ2R    Double Zeta + Double Rydberg Functions",
    ),
    "DZ + Rydberg (Dunning-Hay)": BasisSet(
        name="DZ + Rydberg (Dunning-Hay)",
        description="DZ1R    Double Zeta: 2 Functions/AO",
    ),
    "DZP (Dunning-Hay)": BasisSet(
        name="DZP (Dunning-Hay)",
        description="DZP     Double Zeta + Polarization on All Atoms",
    ),
    "DZP + Diffuse (Dunning-Hay)": BasisSet(
        name="DZP + Diffuse (Dunning-Hay)",
        description="DZPD    Double Zeta + Polarization + Diffuse",
    ),
    "DZP + Rydberg (Dunning-Hay)": BasisSet(
        name="DZP + Rydberg (Dunning-Hay)",
        description="DZP1R   Double Zeta + Polarization on All Atoms",
    ),
    "FANO-5Z": BasisSet(
        name="FANO-5Z", description="Frozen Atomic Natural Orbital - 5-Zeta"
    ),
    "FANO-6Z": BasisSet(
        name="FANO-6Z", description="Frozen Atomic Natural Orbital - 6-Zeta"
    ),
    "FANO-DZ": BasisSet(
        name="FANO-DZ", description="Frozen Atomic Natural Orbital - Double Zeta"
    ),
    "FANO-QZ": BasisSet(
        name="FANO-QZ", description="Frozen Atomic Natural Orbital - Quadruple Zeta"
    ),
    "FANO-TZ": BasisSet(
        name="FANO-TZ", description="Frozen Atomic Natural Orbital - Triple Zeta"
    ),
    "HGBS-5": BasisSet(
        name="HGBS-5",
        description="Hydrogenic Gaussian basis set formed at tolerance "
        "10^{-5} without polarization",
    ),
    "HGBS-7": BasisSet(
        name="HGBS-7",
        description="Hydrogenic Gaussian basis set formed at tolerance "
        "10^{-7} without polarization",
    ),
    "HGBS-9": BasisSet(
        name="HGBS-9",
        description="Hydrogenic Gaussian basis set formed at tolerance "
        "10^{-9} without polarization",
    ),
    "HGBSP1-5": BasisSet(
        name="HGBSP1-5",
        description="Hydrogenic Gaussian basis set formed at tolerance "
        "10^{-5} with 1 polarization shell",
    ),
    "HGBSP1-7": BasisSet(
        name="HGBSP1-7",
        description="Hydrogenic Gaussian basis set formed at tolerance "
        "10^{-7} with 1 polarization shell",
    ),
    "HGBSP1-9": BasisSet(
        name="HGBSP1-9",
        description="Hydrogenic Gaussian basis set formed at tolerance "
        "10^{-9} with 1 polarization shell",
    ),
    "HGBSP2-5": BasisSet(
        name="HGBSP2-5",
        description="Hydrogenic Gaussian basis set formed at tolerance "
        "10^{-5} with 2 polarization shells",
    ),
    "HGBSP2-7": BasisSet(
        name="HGBSP2-7",
        description="Hydrogenic Gaussian basis set formed at tolerance "
        "10^{-7} with 2 polarization shells",
    ),
    "HGBSP2-9": BasisSet(
        name="HGBSP2-9",
        description="Hydrogenic Gaussian basis set formed at tolerance "
        "10^{-9} with 2 polarization shells",
    ),
    "HGBSP3-5": BasisSet(
        name="HGBSP3-5",
        description="Hydrogenic Gaussian basis set formed at tolerance "
        "10^{-5} with 3 polarization shells",
    ),
    "HGBSP3-7": BasisSet(
        name="HGBSP3-7",
        description="Hydrogenic Gaussian basis set formed at tolerance "
        "10^{-7} with 3 polarization shells",
    ),
    "HGBSP3-9": BasisSet(
        name="HGBSP3-9",
        description="Hydrogenic Gaussian basis set formed at tolerance "
        "10^{-9} with 3 polarization shells",
    ),
    "IGLO-II": BasisSet(
        name="IGLO-II",
        description="VDZP Valence Double Zeta + Polarization on All Atoms",
    ),
    "IGLO-III": BasisSet(
        name="IGLO-III",
        description="VTZP Valence Triple Zeta + Polarization on All Atoms",
    ),
    "jgauss-dzp": BasisSet(
        name="jgauss-dzp", description="dzp basis of Schafer/Horn/Ahlrichs/Gauss"
    ),
    "jgauss-qz2p": BasisSet(
        name="jgauss-qz2p", description="qz2p basis of Schafer/Horn/Ahlrichs/Gauss"
    ),
    "jgauss-qzp": BasisSet(
        name="jgauss-qzp", description="qzp basis of Schafer/Horn/Ahlrichs/Gauss"
    ),
    "jgauss-tzp1": BasisSet(
        name="jgauss-tzp1", description="tzp1 basis of Schafer/Horn/Ahlrichs/Gauss"
    ),
    "jgauss-tzp2": BasisSet(
        name="jgauss-tzp2", description="tzp2 basis of Schafer/Horn/Ahlrichs/Gauss"
    ),
    "jorge-5ZP": BasisSet(
        name="jorge-5ZP", description="5ZP: 5 zeta valence quality plus polarization"
    ),
    "jorge-5ZP-DKH": BasisSet(
        name="jorge-5ZP-DKH",
        description="5ZP-DKH: 5 zeta valence quality plus polarization (DKH)",
    ),
    "jorge-6ZP": BasisSet(
        name="jorge-6ZP", description="6ZP: 6 zeta valence quality plus polarization"
    ),
    "jorge-6ZP-DKH": BasisSet(
        name="jorge-6ZP-DKH",
        description="6ZP-DKH: 6 zeta valence quality plus polarization (DKH)",
    ),
    "jorge-A5ZP": BasisSet(
        name="jorge-A5ZP",
        description="A5ZP: Augmented 5 zeta valence quality plus " "polarization",
    ),
    "jorge-ADZP": BasisSet(
        name="jorge-ADZP",
        description="ADZP: Augmented double zeta valence quality plus " "polarization",
    ),
    "jorge-AQZP": BasisSet(
        name="jorge-AQZP",
        description="AQZP: Augmented quadruple zeta valence quality plus "
        "polarization",
    ),
    "jorge-ATZP": BasisSet(
        name="jorge-ATZP",
        description="ATZP: Augmented triple zeta valence quality plus " "polarization",
    ),
    "jorge-DZP": BasisSet(
        name="jorge-DZP",
        description="DZP: Double zeta valence quality plus polarization",
    ),
    "jorge-DZP-DKH": BasisSet(
        name="jorge-DZP-DKH",
        description="DZP-DKH: Double zeta valence quality plus polarization " "(DKH)",
    ),
    "jorge-QZP": BasisSet(
        name="jorge-QZP",
        description="QZP: Quadruple zeta valence quality plus polarization",
    ),
    "jorge-QZP-DKH": BasisSet(
        name="jorge-QZP-DKH",
        description="QZP-DKH: Quadruple zeta valence quality plus "
        "polarization (DKH)",
    ),
    "jorge-TZP": BasisSet(
        name="jorge-TZP",
        description="TZP: Triple zeta valence quality plus polarization",
    ),
    "jorge-TZP-DKH": BasisSet(
        name="jorge-TZP-DKH",
        description="TZP-DKH: Triple zeta valence quality plus polarization " "(DKH)",
    ),
    "jul-cc-pV(D+d)Z": BasisSet(
        name="jul-cc-pV(D+d)Z", description="jul-cc-pV(D+d)Z basis of Papajak/Truhlar"
    ),
    "jul-cc-pV(Q+d)Z": BasisSet(
        name="jul-cc-pV(Q+d)Z", description="jul-cc-pV(Q+d)Z basis of Papajak/Truhlar"
    ),
    "jul-cc-pV(T+d)Z": BasisSet(
        name="jul-cc-pV(T+d)Z", description="jul-cc-pV(T+d)Z basis of Papajak/Truhlar"
    ),
    "jun-cc-pV(D+d)Z": BasisSet(
        name="jun-cc-pV(D+d)Z", description="jun-cc-pV(D+d)Z basis of Papajak/Truhlar"
    ),
    "jun-cc-pV(Q+d)Z": BasisSet(
        name="jun-cc-pV(Q+d)Z", description="jun-cc-pV(Q+d)Z basis of Papajak/Truhlar"
    ),
    "jun-cc-pV(T+d)Z": BasisSet(
        name="jun-cc-pV(T+d)Z", description="jun-cc-pV(T+d)Z basis of Papajak/Truhlar"
    ),
    "Koga unpolarized": BasisSet(
        name="Koga unpolarized",
        description="Non-relativistic unpolarized basis sets for atomic "
        "calculations, designed for use in "
        "uncontracted form",
    ),
    "LANL08": BasisSet(name="LANL08", description="LANL08(uncontracted)"),
    "LANL08(d)": BasisSet(
        name="LANL08(d)", description="LANL08 + polarization and diffuse"
    ),
    "LANL08(f)": BasisSet(name="LANL08(f)", description="LANL08(f)"),
    "LANL08+": BasisSet(name="LANL08+", description="LANL08+ diffuse"),
    "LANL2DZ": BasisSet(name="LANL2DZ", description="LANL2DZ"),
    "LANL2DZ ECP": BasisSet(name="LANL2DZ ECP", description="LANL2DZ ECP"),
    "LANL2DZdp": BasisSet(
        name="LANL2DZdp", description="DZP  Double Zeta + Polarization + Diffuse ECP"
    ),
    "LANL2TZ": BasisSet(name="LANL2TZ", description="LANL2TZ"),
    "LANL2TZ(f)": BasisSet(name="LANL2TZ(f)", description="LANL2TZ(f)"),
    "LANL2TZ+": BasisSet(
        name="LANL2TZ+", description="LANL2TZ+ with diffuse d functions"
    ),
    "m6-31G": BasisSet(name="m6-31G", description="m6-31G"),
    "m6-31G*": BasisSet(name="m6-31G*", description="m6-31G*"),
    "maug-cc-pV(D+d)Z": BasisSet(
        name="maug-cc-pV(D+d)Z", description="jun-cc-pV(D+d)Z basis of Papajak/Truhlar"
    ),
    "maug-cc-pV(Q+d)Z": BasisSet(
        name="maug-cc-pV(Q+d)Z", description="apr-cc-pV(Q+d)Z basis of Papajak/Truhlar"
    ),
    "maug-cc-pV(T+d)Z": BasisSet(
        name="maug-cc-pV(T+d)Z", description="may-cc-pV(T+d)Z basis of Papajak/Truhlar"
    ),
    "may-cc-pV(Q+d)Z": BasisSet(
        name="may-cc-pV(Q+d)Z", description="may-cc-pV(Q+d)Z basis of Papajak/Truhlar"
    ),
    "may-cc-pV(T+d)Z": BasisSet(
        name="may-cc-pV(T+d)Z", description="may-cc-pV(T+d)Z basis of Papajak/Truhlar"
    ),
    "MIDI": BasisSet(name="MIDI", description="Huzinaga MIDI"),
    "MIDI!": BasisSet(
        name="MIDI!",
        description="VDZP Valence Double Zeta + Polarization on some atoms",
    ),
    "MIDIX": BasisSet(
        name="MIDIX",
        description="VDZP Valence Double Zeta + Polarization on some atoms",
    ),
    "MINI": BasisSet(name="MINI", description="Huzinaga MINI"),
    "modified-LANL2DZ": BasisSet(
        name="modified-LANL2DZ",
        description="Couty-Hall Modified LANL2DZ Basis Sets for Transition " "Metals",
    ),
    "NASA Ames ANO": BasisSet(
        name="NASA Ames ANO",
        description="VQZ3P   Valence Quadruple Zeta + Polarization on All " "Atoms",
    ),
    "NASA Ames ANO2": BasisSet(
        name="NASA Ames ANO2",
        description="VQZ3P   Valence Quadruple Zeta + Polarization on All " "Atoms",
    ),
    "NASA Ames cc-pCV5Z": BasisSet(
        name="NASA Ames cc-pCV5Z", description="NASA Ames cc-pCV5Z"
    ),
    "NASA Ames cc-pCVQZ": BasisSet(
        name="NASA Ames cc-pCVQZ", description="NASA Ames cc-pCVQZ"
    ),
    "NASA Ames cc-pCVTZ": BasisSet(
        name="NASA Ames cc-pCVTZ", description="NASA Ames cc-pCVTZ"
    ),
    "NASA Ames cc-pV5Z": BasisSet(
        name="NASA Ames cc-pV5Z", description="NASA Ames cc-pV5Z"
    ),
    "NASA Ames cc-pVQZ": BasisSet(
        name="NASA Ames cc-pVQZ", description="NASA Ames cc-pVQZ"
    ),
    "NASA Ames cc-pVTZ": BasisSet(
        name="NASA Ames cc-pVTZ", description="NASA Ames cc-pVTZ"
    ),
    "NLO-V": BasisSet(
        name="NLO-V",
        description="NLO-V (V=1-3) used to calculate linear and mainly "
        "nonlinear optical properties for "
        "molecules",
    ),
    "NMR-DKH (TZ2P)": BasisSet(
        name="NMR-DKH (TZ2P)", description="NMR-DKH (TZ2P) triple-zeta doubly-polarized"
    ),
    "ORP": BasisSet(
        name="ORP", description="ORP (Optical Rotation Prediction) Basis Set"
    ),
    "Partridge Uncontracted 1": BasisSet(
        name="Partridge Uncontracted 1", description="Partridge Uncontracted 1"
    ),
    "Partridge Uncontracted 2": BasisSet(
        name="Partridge Uncontracted 2", description="Partridge Uncontracted 2"
    ),
    "Partridge Uncontracted 3": BasisSet(
        name="Partridge Uncontracted 3", description="Partridge Uncontracted 3"
    ),
    "Partridge Uncontracted 4": BasisSet(
        name="Partridge Uncontracted 4", description="Partridge Uncontracted 4"
    ),
    "pc-0": BasisSet(name="pc-0", description="pc-0(unpolarized)"),
    "pc-1": BasisSet(name="pc-1", description="pc-1"),
    "pc-2": BasisSet(name="pc-2", description="pc-2"),
    "pc-3": BasisSet(name="pc-3", description="pc-3"),
    "pc-4": BasisSet(name="pc-4", description="pc-4"),
    "pcemd-2": BasisSet(
        name="pcemd-2",
        description="pcemd-2: polarization-consistent electron momentum " "density",
    ),
    "pcemd-3": BasisSet(
        name="pcemd-3",
        description="pcemd-3: polarization-consistent electron momentum " "density",
    ),
    "pcemd-4": BasisSet(
        name="pcemd-4",
        description="pcemd-4: polarization-consistent electron momentum " "density",
    ),
    "pcH-1": BasisSet(name="pcH-1", description="pcH-1"),
    "pcH-2": BasisSet(name="pcH-2", description="pcH-2"),
    "pcH-3": BasisSet(name="pcH-3", description="pcH-3"),
    "pcH-4": BasisSet(name="pcH-4", description="pcH-4"),
    "pcJ-0": BasisSet(
        name="pcJ-0", description="Contracted version of the pcJ-0 basis"
    ),
    "pcJ-0_2006": BasisSet(name="pcJ-0_2006", description="pcJ-0_2006"),
    "pcJ-1": BasisSet(
        name="pcJ-1", description="Contracted version of the pcJ-1 basis"
    ),
    "pcJ-1_2006": BasisSet(name="pcJ-1_2006", description="pcJ-1_2006"),
    "pcJ-2": BasisSet(
        name="pcJ-2", description="Contracted version of the pcJ-2 basis"
    ),
    "pcJ-2_2006": BasisSet(name="pcJ-2_2006", description="pcJ-2_2006"),
    "pcJ-3": BasisSet(
        name="pcJ-3", description="Contracted version of the pcJ-3 basis"
    ),
    "pcJ-3_2006": BasisSet(name="pcJ-3_2006", description="pcJ-3_2006"),
    "pcJ-4": BasisSet(
        name="pcJ-4", description="Contracted version of the pcJ-4 basis"
    ),
    "pcJ-4_2006": BasisSet(name="pcJ-4_2006", description="pcJ-4_2006"),
    "pcS-0": BasisSet(name="pcS-0", description="pcS-0"),
    "pcS-1": BasisSet(name="pcS-1", description="pcS-1"),
    "pcS-2": BasisSet(name="pcS-2", description="pcS-2"),
    "pcS-3": BasisSet(name="pcS-3", description="pcS-3"),
    "pcS-4": BasisSet(name="pcS-4", description="pcS-4"),
    "pcseg-0": BasisSet(
        name="pcseg-0", description="Segmented contracted version of the pc-0 basis"
    ),
    "pcseg-1": BasisSet(
        name="pcseg-1", description="Segmented contracted version of the pc-1 basis"
    ),
    "pcseg-2": BasisSet(
        name="pcseg-2", description="Segmented contracted version of the pc-2 basis"
    ),
    "pcseg-3": BasisSet(
        name="pcseg-3", description="Segmented contracted version of the pc-3 basis"
    ),
    "pcseg-4": BasisSet(
        name="pcseg-4", description="Segmented contracted version of the pc-4 basis"
    ),
    "pcSseg-0": BasisSet(
        name="pcSseg-0", description="Segmented contracted version of the pcS-0 basis"
    ),
    "pcSseg-1": BasisSet(
        name="pcSseg-1", description="Segmented contracted version of the pcS-1 basis"
    ),
    "pcSseg-2": BasisSet(
        name="pcSseg-2", description="Segmented contracted version of the pcS-2 basis"
    ),
    "pcSseg-3": BasisSet(
        name="pcSseg-3", description="Segmented contracted version of the pcS-3 basis"
    ),
    "pcSseg-4": BasisSet(
        name="pcSseg-4", description="Segmented contracted version of the pcS-4 basis"
    ),
    "pcX-1": BasisSet(
        name="pcX-1", description="Jensen pcX basis set optimized for core-spectroscopy"
    ),
    "pcX-2": BasisSet(
        name="pcX-2", description="Jensen pcX basis set optimized for core-spectroscopy"
    ),
    "pcX-3": BasisSet(
        name="pcX-3", description="Jensen pcX basis set optimized for core-spectroscopy"
    ),
    "pcX-4": BasisSet(
        name="pcX-4", description="Jensen pcX basis set optimized for core-spectroscopy"
    ),
    "pSBKJC": BasisSet(
        name="pSBKJC",
        description="Electrically polarized valence basis sets for the SBKJC"
        " effective core potential developed "
        "for calculations of dynamic "
        "polarizabilities and Raman intensities",
    ),
    "Pt - mDZP": BasisSet(name="Pt - mDZP", description="Pt - mDZP"),
    "pV6Z": BasisSet(
        name="pV6Z",
        description="V6Z5P   Valence Sextuple Zeta + Polarization on All " "Atoms",
    ),
    "pV7Z": BasisSet(name="pV7Z", description="pV7Z"),
    "Roos Augmented Double Zeta ANO": BasisSet(
        name="Roos Augmented Double Zeta ANO",
        description="Roos Augmented Double Zeta ANO",
    ),
    "Roos Augmented Triple Zeta ANO": BasisSet(
        name="Roos Augmented Triple Zeta ANO",
        description="Roos Augmented Triple Zeta ANO",
    ),
    "s3-21G": BasisSet(name="s3-21G", description="s3-21G"),
    "s3-21G*": BasisSet(name="s3-21G*", description="s3-21G*"),
    "s6-31G": BasisSet(name="s6-31G", description="s6-31G"),
    "s6-31G*": BasisSet(name="s6-31G*", description="s6-31G*"),
    "Sadlej pVTZ": BasisSet(
        name="Sadlej pVTZ", description="Sadlej polarized-valence-triple-zeta"
    ),
    "Sadlej+": BasisSet(name="Sadlej+", description="Sadlej+"),
    "sap_grasp_large": BasisSet(name="sap_grasp_large", description="sap_grasp_large"),
    "sap_grasp_small": BasisSet(name="sap_grasp_small", description="sap_grasp_small"),
    "sap_helfem_large": BasisSet(
        name="sap_helfem_large", description="sap_helfem_large"
    ),
    "sap_helfem_small": BasisSet(
        name="sap_helfem_small", description="sap_helfem_small"
    ),
    "Sapporo-DKH3-DZP": BasisSet(
        name="Sapporo-DKH3-DZP", description="Sapporo-DKH3-DZP [deprecated]"
    ),
    "Sapporo-DKH3-DZP-2012": BasisSet(name="Sapporo-DKH3-DZP-2012", description=""),
    "Sapporo-DKH3-DZP-2012-diffuse": BasisSet(
        name="Sapporo-DKH3-DZP-2012-diffuse", description=""
    ),
    "Sapporo-DKH3-DZP-diffuse": BasisSet(
        name="Sapporo-DKH3-DZP-diffuse",
        description="Sapporo-DKH3-DZP-diffuse [deprecated]",
    ),
    "Sapporo-DKH3-QZP": BasisSet(
        name="Sapporo-DKH3-QZP", description="Sapporo-DKH3-QZP [deprecated]"
    ),
    "Sapporo-DKH3-QZP-2012": BasisSet(name="Sapporo-DKH3-QZP-2012", description=""),
    "Sapporo-DKH3-QZP-2012-diffuse": BasisSet(
        name="Sapporo-DKH3-QZP-2012-diffuse", description=""
    ),
    "Sapporo-DKH3-QZP-diffuse": BasisSet(
        name="Sapporo-DKH3-QZP-diffuse",
        description="Sapporo-DKH3-QZP-diffuse [deprecated]",
    ),
    "Sapporo-DKH3-TZP": BasisSet(
        name="Sapporo-DKH3-TZP", description="Sapporo-DKH3-TZP [deprecated]"
    ),
    "Sapporo-DKH3-TZP-2012": BasisSet(name="Sapporo-DKH3-TZP-2012", description=""),
    "Sapporo-DKH3-TZP-2012-diffuse": BasisSet(
        name="Sapporo-DKH3-TZP-2012-diffuse", description=""
    ),
    "Sapporo-DKH3-TZP-diffuse": BasisSet(
        name="Sapporo-DKH3-TZP-diffuse",
        description="Sapporo-DKH3-TZP-diffuse [deprecated]",
    ),
    "Sapporo-DZP": BasisSet(name="Sapporo-DZP", description="Sapporo-DZP [deprecated]"),
    "Sapporo-DZP-2012": BasisSet(name="Sapporo-DZP-2012", description=""),
    "Sapporo-DZP-2012-diffuse": BasisSet(
        name="Sapporo-DZP-2012-diffuse", description=""
    ),
    "Sapporo-DZP-diffuse": BasisSet(
        name="Sapporo-DZP-diffuse", description="Sapporo-DZP-diffuse [deprecated]"
    ),
    "Sapporo-QZP": BasisSet(name="Sapporo-QZP", description="Sapporo-QZP [deprecated]"),
    "Sapporo-QZP-2012": BasisSet(name="Sapporo-QZP-2012", description=""),
    "Sapporo-QZP-2012-diffuse": BasisSet(
        name="Sapporo-QZP-2012-diffuse", description=""
    ),
    "Sapporo-QZP-diffuse": BasisSet(
        name="Sapporo-QZP-diffuse", description="Sapporo-QZP-diffuse [deprecated]"
    ),
    "Sapporo-TZP": BasisSet(name="Sapporo-TZP", description="Sapporo-TZP [deprecated]"),
    "Sapporo-TZP-2012": BasisSet(name="Sapporo-TZP-2012", description=""),
    "Sapporo-TZP-2012-diffuse": BasisSet(
        name="Sapporo-TZP-2012-diffuse", description=""
    ),
    "Sapporo-TZP-diffuse": BasisSet(
        name="Sapporo-TZP-diffuse", description="Sapporo-TZP-diffuse [deprecated]"
    ),
    "SARC-DKH2": BasisSet(name="SARC-DKH2", description="SARC-DKH2"),
    "SARC-ZORA": BasisSet(name="SARC-ZORA", description="SARC-ZORA"),
    "SARC2-QZV-DKH2": BasisSet(name="SARC2-QZV-DKH2", description="SARC2-QZV-DKH2"),
    "SARC2-QZV-DKH2-JKFIT": BasisSet(
        name="SARC2-QZV-DKH2-JKFIT",
        description="JK fitting basis for use with SARC2-QZV-DKH2",
    ),
    "SARC2-QZV-ZORA": BasisSet(name="SARC2-QZV-ZORA", description="SARC2-QZV-ZORA"),
    "SARC2-QZV-ZORA-JKFIT": BasisSet(
        name="SARC2-QZV-ZORA-JKFIT",
        description="JK fitting basis for use with SARC2-QZV-ZORA",
    ),
    "SARC2-QZVP-DKH2": BasisSet(name="SARC2-QZVP-DKH2", description="SARC2-QZVP-DKH2"),
    "SARC2-QZVP-DKH2-JKFIT": BasisSet(
        name="SARC2-QZVP-DKH2-JKFIT",
        description="JK fitting basis for use with SARC2-QZVP-DKH2",
    ),
    "SARC2-QZVP-ZORA": BasisSet(
        name="SARC2-QZVP-ZORA",
        description="SARC2-QZVP-ZORA: Polarized Quadruple Z Valence",
    ),
    "SARC2-QZVP-ZORA-JKFIT": BasisSet(
        name="SARC2-QZVP-ZORA-JKFIT",
        description="JK fitting basis for use with SARC2-QZVP-ZORA",
    ),
    "SBKJC Polarized (p,2d) - LFK": BasisSet(
        name="SBKJC Polarized (p,2d) - LFK", description="SBKJC Polarized (p,2d) - LFK"
    ),
    "SBKJC-ECP": BasisSet(name="SBKJC-ECP", description="SBKJC ECP"),
    "SBKJC-VDZ": BasisSet(
        name="SBKJC-VDZ", description="VDZ Valence Double Zeta with ECP"
    ),
    "SBO4-DZ(d)-3G": BasisSet(
        name="SBO4-DZ(d)-3G",
        description="SBO4-DZ(d,p)-3G Double-zeta expansion of simplified box"
        " orbitals",
    ),
    "SBO4-DZ(d,p)-3G": BasisSet(
        name="SBO4-DZ(d,p)-3G",
        description="SBO4-DZ(d,p)-3G Double-zeta expansion of simplified box"
        " orbitals",
    ),
    "SBO4-SZ-3G": BasisSet(
        name="SBO4-SZ-3G",
        description="SBO4-SZ-3G Single-zeta expansion of simplified box " "orbitals",
    ),
    "Scaled MINI": BasisSet(name="Scaled MINI", description="Huzinaga Scaled MINI"),
    "STO-2G": BasisSet(
        name="STO-2G", description="STO-2G Minimal Basis (2 functions/AO)"
    ),
    "STO-3G": BasisSet(
        name="STO-3G", description="STO-3G Minimal Basis (3 functions/AO)"
    ),
    "STO-3G*": BasisSet(
        name="STO-3G*", description="MBP     Minimal Basis + Polarization on second row"
    ),
    "STO-4G": BasisSet(
        name="STO-4G", description="STO-4G Minimal Basis (4 functions/AO)"
    ),
    "STO-5G": BasisSet(
        name="STO-5G", description="STO-5G Minimal Basis (5 functions/AO)"
    ),
    "STO-6G": BasisSet(
        name="STO-6G", description="STO-6G Minimal Basis (6 functions/AO)"
    ),
    "Stuttgart RLC": BasisSet(
        name="Stuttgart RLC", description="Stuttgart RLC ECP + Valence basis"
    ),
    "Stuttgart RLC ECP": BasisSet(
        name="Stuttgart RLC ECP", description="Stuttgart RLC ECP"
    ),
    "Stuttgart RSC 1997": BasisSet(
        name="Stuttgart RSC 1997", description="Stuttgart RSC 1997 ECP + Valence basis"
    ),
    "Stuttgart RSC 1997 ECP": BasisSet(
        name="Stuttgart RSC 1997 ECP", description="Stuttgart RSC 1997 ECP"
    ),
    "Stuttgart RSC ANO": BasisSet(
        name="Stuttgart RSC ANO",
        description="Stuttgart RSC 1997 + Quadruple Zeta Basis Set designed "
        "for an ECP",
    ),
    "Stuttgart RSC Segmented + ECP": BasisSet(
        name="Stuttgart RSC Segmented + ECP",
        description="Stuttgart RSC 1997 + Quadruple Zeta Basis Set designed "
        "for an ECP",
    ),
    "SV (Dunning-Hay)": BasisSet(
        name="SV (Dunning-Hay)",
        description="VDZ     Valence Double Zeta: 2 Funct.'s/Valence AO",
    ),
    "SV + Double Rydberg (Dunning-Hay)": BasisSet(
        name="SV + Double Rydberg (Dunning-Hay)",
        description="VDZ2R   Valence Double Zeta + Double Rydberg Functions",
    ),
    "SV + Rydberg (Dunning-Hay)": BasisSet(
        name="SV + Rydberg (Dunning-Hay)",
        description="VDZ1R   Valence Double Zeta + Diffuse Rydberg Functions",
    ),
    "SVP (Dunning-Hay)": BasisSet(
        name="SVP (Dunning-Hay)",
        description="VDZP    Valence Double Zeta + Polarization on All Atoms",
    ),
    "SVP + Diffuse (Dunning-Hay)": BasisSet(
        name="SVP + Diffuse (Dunning-Hay)",
        description="VDZPD   Valence Double Zeta + Polarization + Diffuse",
    ),
    "SVP + Diffuse + Rydberg (Dunning-Hay)": BasisSet(
        name="SVP + Diffuse + Rydberg (Dunning-Hay)",
        description="VDZPD1R Valence Double Zeta + Polar. + Diffuse + " "Rydberg",
    ),
    "SVP + Rydberg (Dunning-Hay)": BasisSet(
        name="SVP + Rydberg (Dunning-Hay)",
        description="VDZP1R  Valence Double Zeta + Polarization + Rydberg",
    ),
    "TZ (Dunning-Hay)": BasisSet(
        name="TZ (Dunning-Hay)", description="TZ (Dunning-Hay)"
    ),
    "TZP-ZORA": BasisSet(
        name="TZP-ZORA",
        description="TZP-ZORA, all-electron triple-zeta basis for "
        "calculations with the ZORA approach",
    ),
    "UGBS": BasisSet(name="UGBS", description="Universal Gaussian Basis Set"),
    "un-ccemd-ref": BasisSet(
        name="un-ccemd-ref",
        description="un-ccemd-ref: uncontracted correlation consistent "
        "electron momentum density-ref",
    ),
    "un-pcemd-ref": BasisSet(
        name="un-pcemd-ref",
        description="un-pcemd-ref: uncontracted polarization consistent "
        "electron momentum density-ref",
    ),
    "Wachters+f": BasisSet(
        name="Wachters+f",
        description="VDZP    Valence Double Zeta + Polarization on All Atoms",
    ),
    "WTBS": BasisSet(name="WTBS", description="MB      Minimal Basis: 1 Function/AO"),
    "x2c-JFIT": BasisSet(name="x2c-JFIT", description="x2c coulomb fitting"),
    "x2c-JFIT-universal": BasisSet(
        name="x2c-JFIT-universal", description="x2c coulomb fitting"
    ),
    "x2c-QZVPall": BasisSet(
        name="x2c-QZVPall",
        description="All-electron relativistic polarized quadruple-zeta "
        "basis for two-component calculations",
    ),
    "x2c-QZVPall-2c": BasisSet(
        name="x2c-QZVPall-2c",
        description="All-electron relativistic polarized quadruple-zeta "
        "basis for one-component calculations",
    ),
    "x2c-QZVPall-2c-s": BasisSet(
        name="x2c-QZVPall-2c-s",
        description="All-electron relativistic polarized quadruple-zeta "
        "basis for one-component calculations "
        "of NMR shielding",
    ),
    "x2c-QZVPall-s": BasisSet(
        name="x2c-QZVPall-s",
        description="All-electron relativistic polarized quadruple-zeta "
        "basis for two-component calculations "
        "of NMR shielding",
    ),
    "x2c-QZVPPall": BasisSet(
        name="x2c-QZVPPall",
        description="All-electron relativistic doubly polarized quadruple-"
        "zeta basis for two-component "
        "calculations",
    ),
    "x2c-QZVPPall-2c": BasisSet(
        name="x2c-QZVPPall-2c",
        description="All-electron relativistic doubly polarized quadruple-"
        "zeta basis for one-component "
        "calculations",
    ),
    "x2c-QZVPPall-2c-s": BasisSet(
        name="x2c-QZVPPall-2c-s",
        description="All-electron relativistic doubly polarized quadruple-"
        "zeta basis for one-component "
        "calculations of NMR shielding",
    ),
    "x2c-QZVPPall-s": BasisSet(
        name="x2c-QZVPPall-s",
        description="All-electron relativistic doubly polarized quadruple-"
        "zeta basis for two-component "
        "calculations of NMR shielding",
    ),
    "x2c-SV(P)all": BasisSet(name="x2c-SV(P)all", description="x2c-SV(P)all"),
    "x2c-SV(P)all-2c": BasisSet(name="x2c-SV(P)all-2c", description="x2c-SV(P)all-2c"),
    "x2c-SV(P)all-s": BasisSet(
        name="x2c-SV(P)all-s",
        description="All-electron relativistic split-valence for NMR " "shielding",
    ),
    "x2c-SVPall": BasisSet(name="x2c-SVPall", description="x2c-SVPall"),
    "x2c-SVPall-2c": BasisSet(name="x2c-SVPall-2c", description="x2c-SVPall-2c"),
    "x2c-SVPall-s": BasisSet(
        name="x2c-SVPall-s",
        description="All-electron relativistic split-valence for NMR " "shielding",
    ),
    "x2c-TZVPall": BasisSet(name="x2c-TZVPall", description="x2c-TZVPall"),
    "x2c-TZVPall-2c": BasisSet(name="x2c-TZVPall-2c", description="x2c-TZVPall-2c"),
    "x2c-TZVPall-s": BasisSet(
        name="x2c-TZVPall-s",
        description="All-electron relativistic triple-zeta for NMR shielding",
    ),
    "x2c-TZVPPall": BasisSet(name="x2c-TZVPPall", description="x2c-TZVPPall"),
    "x2c-TZVPPall-2c": BasisSet(name="x2c-TZVPPall-2c", description="x2c-TZVPPall-2c"),
    "x2c-TZVPPall-s": BasisSet(
        name="x2c-TZVPPall-s",
        description="All-electron relativistic triple-zeta for NMR shielding",
    ),
}

BasisSet._warn_on_creation = False
