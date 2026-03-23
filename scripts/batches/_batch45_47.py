#!/usr/bin/env python3
"""Append Batch 45-47 terms to the registry with proper TSV formatting."""

import pathlib

REG = pathlib.Path("terms/registry")
T = "\t"

CONCEPTS = [
    # Batch 45: Magnetic Helicity, Reconnection & Relaxation Physics
    ("# ==== Batch 45: Magnetic Helicity, Reconnection & Relaxation Physics ====",),
    ("magnetic-helicity", "concept", "磁螺旋度", "magnetic helicity", "", "active", "Conserved quantity describing magnetic field topology and twist"),
    ("helicity-injection", "method", "螺旋度注入", "helicity injection", "HI", "active", "Injecting magnetic helicity to sustain plasma current"),
    ("coaxial-helicity-injection", "method", "同轴螺旋度注入", "coaxial helicity injection", "CHI", "active", "Coaxial gun helicity injection for spheromak/ST sustainment"),
    ("taylor-relaxation", "concept", "Taylor弛豫", "Taylor relaxation", "", "active", "Plasma relaxation to minimum-energy state at constant helicity"),
    ("taylor-state", "concept", "Taylor态", "Taylor state", "", "active", "Force-free minimum-energy equilibrium state (curl B = lambda B)"),
    ("magnetic-reconnection", "concept", "磁重联", "magnetic reconnection", "", "active", "Topological rearrangement of magnetic field lines releasing energy"),
    ("magnetic-self-organization", "concept", "磁自组织", "magnetic self-organization", "", "active", "Spontaneous plasma relaxation to ordered equilibrium state"),
    ("force-free-equilibrium", "concept", "无力平衡", "force-free equilibrium", "", "active", "Plasma equilibrium satisfying J cross B equals zero"),
    ("tilt-instability", "concept", "倾斜不稳定性", "tilt instability", "", "active", "Global CT/spheromak MHD instability of magnetic axis tilt"),
    ("flux-amplification", "concept", "磁通放大", "flux amplification", "", "active", "Dynamo-driven poloidal flux amplification in spheromak"),
    # Batch 46: Spheromak/CT Devices & Formation Technologies
    ("# ==== Batch 46: Spheromak/CT Devices & Formation Technologies ====",),
    ("sspx", "device", "SSPX", "SSPX", "", "active", "LLNL Sustained Spheromak Physics Experiment"),
    ("coaxial-plasma-gun", "system", "同轴等离子体枪", "coaxial plasma gun", "", "active", "Coaxial magnetized gun for spheromak/CT formation"),
    ("spheromak-merging", "concept", "球马克并合", "spheromak merging", "", "active", "Counter-helicity spheromak merging"),
    ("flux-conserver", "system", "磁通守恒器", "flux conserver", "", "active", "Close-fitting conducting shell for CT flux conservation"),
    ("plasma-sustainment", "concept", "等离子体维持", "plasma sustainment", "", "active", "Non-inductive current and confinement sustainment"),
    ("pinch-parameter", "metric", "箍缩参数", "pinch parameter", "", "active", "Theta parameter characterizing RFP/spheromak state"),
    ("exl-50u", "device", "EXL-50U", "EXL-50U", "", "active", "ENN upgraded spherical tokamak"),
    # Batch 47: Proton-Boron Fusion & Advanced Fuel Physics
    ("# ==== Batch 47: Proton-Boron Fusion & Advanced Fuel Physics ====",),
    ("ignition-temperature", "metric", "点火温度", "ignition temperature", "", "active", "Minimum temperature required for self-sustaining fusion burn"),
    ("three-alpha-reaction", "concept", "三α反应", "three-alpha reaction", "", "active", "p + 11B -> 3 alpha + 8.7 MeV reaction channel"),
    ("side-reaction", "concept", "副反应", "side reaction", "", "active", "Parasitic neutron-producing reaction channel in advanced fuels"),
    ("radiation-dominated-regime", "concept", "辐射主导区间", "radiation-dominated regime", "", "active", "High-temperature regime where radiation loss exceeds fusion power"),
    ("laser-boron-fusion", "concept", "激光硼聚变", "laser-boron fusion", "", "active", "Laser-driven p-11B fusion scheme"),

    ("hb11-energy", "organization", "HB11 Energy", "HB11 Energy", "", "active", "Australian laser p-B11 fusion company"),
    ("lpp-fusion", "organization", "LPP Fusion", "LPP Fusion", "", "active", "US dense plasma focus p-B11 fusion company"),
    ("fusion-product-spectrum", "concept", "聚变产物能谱", "fusion product spectrum", "", "active", "Energy distribution spectrum of fusion reaction products"),
    ("power-density", "metric", "功率密度", "power density", "", "active", "Fusion power per unit volume"),
]

ALIASES = [
    # Batch 45: Magnetic Helicity, Reconnection & Relaxation Physics
    ("# ==== Batch 45: Magnetic Helicity, Reconnection & Relaxation Physics ====",),
    ("magnetic helicity", "magnetic-helicity", "en", "preferred", ""),
    ("磁螺旋度", "magnetic-helicity", "zh", "preferred", ""),
    ("helicity injection", "helicity-injection", "en", "preferred", ""),
    ("HI", "helicity-injection", "abbr", "preferred", ""),
    ("螺旋度注入", "helicity-injection", "zh", "preferred", ""),
    ("coaxial helicity injection", "coaxial-helicity-injection", "en", "preferred", ""),
    ("CHI", "coaxial-helicity-injection", "abbr", "preferred", ""),
    ("同轴螺旋度注入", "coaxial-helicity-injection", "zh", "preferred", ""),
    ("Taylor relaxation", "taylor-relaxation", "en", "preferred", ""),
    ("Taylor弛豫", "taylor-relaxation", "zh", "preferred", ""),
    ("Taylor state", "taylor-state", "en", "preferred", ""),
    ("Taylor态", "taylor-state", "zh", "preferred", ""),
    ("magnetic reconnection", "magnetic-reconnection", "en", "preferred", ""),
    ("磁重联", "magnetic-reconnection", "zh", "preferred", ""),
    ("磁场重联", "magnetic-reconnection", "zh", "alias", ""),
    ("magnetic self-organization", "magnetic-self-organization", "en", "preferred", ""),
    ("磁自组织", "magnetic-self-organization", "zh", "preferred", ""),
    ("force-free equilibrium", "force-free-equilibrium", "en", "preferred", ""),
    ("无力平衡", "force-free-equilibrium", "zh", "preferred", ""),
    ("tilt instability", "tilt-instability", "en", "preferred", ""),
    ("倾斜不稳定性", "tilt-instability", "zh", "preferred", ""),
    ("tilt mode", "tilt-instability", "en", "alias", ""),
    ("flux amplification", "flux-amplification", "en", "preferred", ""),
    ("磁通放大", "flux-amplification", "zh", "preferred", ""),
    # Batch 46: Spheromak/CT Devices & Formation Technologies
    ("# ==== Batch 46: Spheromak/CT Devices & Formation Technologies ====",),
    ("SSPX", "sspx", "en", "preferred", ""),
    ("Sustained Spheromak Physics Experiment", "sspx", "en", "alias", ""),
    ("coaxial plasma gun", "coaxial-plasma-gun", "en", "preferred", ""),
    ("同轴等离子体枪", "coaxial-plasma-gun", "zh", "preferred", ""),
    ("Marshall gun", "coaxial-plasma-gun", "en", "alias", ""),
    ("spheromak merging", "spheromak-merging", "en", "preferred", ""),
    ("球马克并合", "spheromak-merging", "zh", "preferred", ""),
    ("counter-helicity merging", "spheromak-merging", "en", "alias", ""),
    ("flux conserver", "flux-conserver", "en", "preferred", ""),
    ("磁通守恒器", "flux-conserver", "zh", "preferred", ""),
    ("plasma sustainment", "plasma-sustainment", "en", "preferred", ""),
    ("等离子体维持", "plasma-sustainment", "zh", "preferred", ""),
    ("current sustainment", "plasma-sustainment", "en", "alias", ""),
    ("pinch parameter", "pinch-parameter", "en", "preferred", ""),
    ("箍缩参数", "pinch-parameter", "zh", "preferred", ""),
    ("EXL-50U", "exl-50u", "en", "preferred", ""),
    ("EXL50U", "exl-50u", "en", "alias", ""),
    # Batch 47: Proton-Boron Fusion & Advanced Fuel Physics
    ("# ==== Batch 47: Proton-Boron Fusion & Advanced Fuel Physics ====",),
    ("ignition temperature", "ignition-temperature", "en", "preferred", ""),
    ("点火温度", "ignition-temperature", "zh", "preferred", ""),
    ("three-alpha reaction", "three-alpha-reaction", "en", "preferred", ""),
    ("三α反应", "three-alpha-reaction", "zh", "preferred", ""),
    ("3-alpha reaction", "three-alpha-reaction", "en", "alias", ""),
    ("side reaction", "side-reaction", "en", "preferred", ""),
    ("副反应", "side-reaction", "zh", "preferred", ""),
    ("parasitic reaction", "side-reaction", "en", "alias", ""),
    ("radiation-dominated regime", "radiation-dominated-regime", "en", "preferred", ""),
    ("辐射主导区间", "radiation-dominated-regime", "zh", "preferred", ""),
    ("laser-boron fusion", "laser-boron-fusion", "en", "preferred", ""),
    ("激光硼聚变", "laser-boron-fusion", "zh", "preferred", ""),
    ("laser p-B11 fusion", "laser-boron-fusion", "en", "alias", ""),
    ("plasma focus", "dense-plasma-focus", "en", "alias", ""),
    ("PF", "dense-plasma-focus", "abbr", "alias", ""),
    ("等离子体聚焦装置", "dense-plasma-focus", "zh", "alias", ""),
    ("HB11 Energy", "hb11-energy", "en", "preferred", ""),
    ("LPP Fusion", "lpp-fusion", "en", "preferred", ""),
    ("Focus Fusion", "lpp-fusion", "en", "alias", ""),
    ("fusion product spectrum", "fusion-product-spectrum", "en", "preferred", ""),
    ("聚变产物能谱", "fusion-product-spectrum", "zh", "preferred", ""),
    ("power density", "power-density", "en", "preferred", ""),
    ("功率密度", "power-density", "zh", "preferred", ""),
]

EVIDENCE = [
    ("magnetic-helicity", "internal:expansion:batch-45", "Magnetic topology conserved quantity", "copilot", "2026-03-19"),
    ("helicity-injection", "internal:expansion:batch-45", "Helicity injection sustainment", "copilot", "2026-03-19"),
    ("coaxial-helicity-injection", "internal:expansion:batch-45", "CHI for spheromak/ST", "copilot", "2026-03-19"),
    ("taylor-relaxation", "internal:expansion:batch-45", "Minimum energy relaxation", "copilot", "2026-03-19"),
    ("taylor-state", "internal:expansion:batch-45", "Force-free equilibrium state", "copilot", "2026-03-19"),
    ("magnetic-reconnection", "internal:expansion:batch-45", "Field line reconnection", "copilot", "2026-03-19"),
    ("magnetic-self-organization", "internal:expansion:batch-45", "Spontaneous self-organization", "copilot", "2026-03-19"),
    ("force-free-equilibrium", "internal:expansion:batch-45", "JxB=0 equilibrium", "copilot", "2026-03-19"),
    ("tilt-instability", "internal:expansion:batch-45", "CT global tilt mode", "copilot", "2026-03-19"),
    ("flux-amplification", "internal:expansion:batch-45", "Dynamo poloidal flux amplification", "copilot", "2026-03-19"),
    ("sspx", "internal:expansion:batch-46", "LLNL spheromak experiment", "copilot", "2026-03-19"),
    ("coaxial-plasma-gun", "internal:expansion:batch-46", "CT formation gun", "copilot", "2026-03-19"),
    ("spheromak-merging", "internal:expansion:batch-46", "Counter-helicity merging", "copilot", "2026-03-19"),
    ("flux-conserver", "internal:expansion:batch-46", "Conducting shell for CT", "copilot", "2026-03-19"),
    ("plasma-sustainment", "internal:expansion:batch-46", "Non-inductive sustainment", "copilot", "2026-03-19"),
    ("pinch-parameter", "internal:expansion:batch-46", "Theta parameter", "copilot", "2026-03-19"),
    ("exl-50u", "internal:expansion:batch-46", "ENN upgraded ST", "copilot", "2026-03-19"),
    ("ignition-temperature", "internal:expansion:batch-47", "Min self-sustaining temp", "copilot", "2026-03-19"),
    ("three-alpha-reaction", "internal:expansion:batch-47", "p-11B three alpha channel", "copilot", "2026-03-19"),
    ("side-reaction", "internal:expansion:batch-47", "Parasitic neutron reactions", "copilot", "2026-03-19"),
    ("radiation-dominated-regime", "internal:expansion:batch-47", "Radiation>fusion power zone", "copilot", "2026-03-19"),
    ("laser-boron-fusion", "internal:expansion:batch-47", "Laser driven p-B11", "copilot", "2026-03-19"),

    ("hb11-energy", "internal:expansion:batch-47", "Australian laser p-B11 co.", "copilot", "2026-03-19"),
    ("lpp-fusion", "internal:expansion:batch-47", "US DPF p-B11 company", "copilot", "2026-03-19"),
    ("fusion-product-spectrum", "internal:expansion:batch-47", "Reaction product energy dist", "copilot", "2026-03-19"),
    ("power-density", "internal:expansion:batch-47", "Fusion power per volume", "copilot", "2026-03-19"),
]


def write_tsv_rows(path, rows):
    with open(path, "a", encoding="utf-8") as f:
        for row in rows:
            if len(row) == 1:
                f.write(row[0] + "\n")
            else:
                f.write(T.join(row) + "\n")


if __name__ == "__main__":
    write_tsv_rows(REG / "concepts.tsv", CONCEPTS)
    n_c = sum(1 for r in CONCEPTS if len(r) > 1)
    print(f"Appended {n_c} concepts")

    write_tsv_rows(REG / "aliases.tsv", ALIASES)
    n_a = sum(1 for r in ALIASES if len(r) > 1)
    print(f"Appended {n_a} aliases")

    write_tsv_rows(REG / "evidence.tsv", EVIDENCE)
    print(f"Appended {len(EVIDENCE)} evidence rows")
