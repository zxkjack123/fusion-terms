#!/usr/bin/env python3
"""Batch 51 — P0 new concepts (28) + enrichment aliases for 6 existing concepts.

Subdomains:
  Transport / micro-instabilities  (4 new)
  MHD stability                    (7 new)
  SOL / divertor physics           (6 new)
  Fuel cycle                       (10 new + 1 material)

Also enriches: kink-mode, internal-kink-mode, kbm, rsae, sol-width, divertor-target
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent
REG = ROOT / "terms" / "registry"


# ── helpers ─────────────────────────────────────────────────────────
def write_tsv_rows(path: Path, rows: list[tuple]):
    with open(path, "a", encoding="utf-8", newline="") as fh:
        for row in rows:
            fh.write("\t".join(row) + "\n")


TODAY = "2026-03-23"

# ── NEW CONCEPTS (28) ──────────────────────────────────────────────
concepts: list[tuple] = [
    ("# ==== Batch 51 P0: Transport / micro-instabilities ====",),
    (
        "gyro-bohm-scaling",
        "concept",
        "旋回Bohm标度",
        "gyro-Bohm scaling",
        "",
        "active",
        "Turbulent transport scaling stronger than Bohm (gyro-radius dependent)",
    ),
    (
        "turbulent-diffusion",
        "concept",
        "湍流扩散输运",
        "turbulent diffusion",
        "",
        "active",
        "Enhanced particle/heat diffusion due to plasma turbulence",
    ),
    (
        "particle-pinch",
        "concept",
        "粒子箍缩",
        "particle pinch",
        "",
        "active",
        "Inward convective particle transport in tokamak plasmas",
    ),
    (
        "thermodiffusion",
        "concept",
        "热扩散",
        "thermodiffusion",
        "",
        "active",
        "Temperature-gradient-driven particle flux (Soret effect in plasmas)",
    ),
    ("# ==== Batch 51 P0: MHD stability ====",),
    (
        "external-kink",
        "concept",
        "外扭曲模",
        "external kink mode",
        "",
        "active",
        "Current-driven kink instability outside the plasma boundary",
    ),
    (
        "sausage-instability",
        "concept",
        "腊肠不稳定性",
        "sausage instability",
        "",
        "active",
        "m=0 axisymmetric MHD instability in a Z-pinch",
    ),
    (
        "pressure-driven-mode",
        "concept",
        "压力驱动模",
        "pressure-driven mode",
        "",
        "active",
        "MHD mode driven by pressure gradient (e.g. ballooning)",
    ),
    (
        "current-driven-mode",
        "concept",
        "电流驱动模",
        "current-driven mode",
        "",
        "active",
        "MHD mode driven by current density gradient (e.g. kink, tearing)",
    ),
    (
        "ideal-mhd-stability",
        "concept",
        "理想MHD稳定性",
        "ideal MHD stability",
        "",
        "active",
        "MHD stability analysis ignoring resistive effects",
    ),
    (
        "resistive-instability",
        "concept",
        "电阻不稳定性",
        "resistive instability",
        "",
        "active",
        "MHD instability requiring finite plasma resistivity (tearing, resistive kink)",
    ),
    (
        "global-alfven-eigenmode",
        "concept",
        "全局Alfvén本征模",
        "global Alfvén eigenmode",
        "GAE",
        "active",
        "Shear-Alfvén gap eigenmode with global structure",
    ),
    ("# ==== Batch 51 P0: SOL / divertor physics ====",),
    (
        "parallel-heat-flux",
        "metric",
        "平行热流",
        "parallel heat flux",
        "",
        "active",
        "Heat flux density along magnetic field lines toward divertor",
    ),
    (
        "filament",
        "concept",
        "等离子体丝状体",
        "filament",
        "",
        "active",
        "Coherent field-aligned density structure in SOL (also called blob)",
    ),
    (
        "divertor-leg",
        "concept",
        "偏滤器腿",
        "divertor leg",
        "",
        "active",
        "Magnetic flux path from X-point to divertor target (inner/outer)",
    ),
    (
        "flux-tube",
        "concept",
        "磁通管",
        "flux tube",
        "",
        "active",
        "Tube-shaped region bounded by magnetic field lines",
    ),
    (
        "connection-length",
        "metric",
        "连接长度",
        "connection length",
        "",
        "active",
        "Field-line length from outboard midplane to divertor target",
    ),
    (
        "wetted-area",
        "metric",
        "湿润面积",
        "wetted area",
        "",
        "active",
        "Divertor target area receiving significant heat flux",
    ),
    ("# ==== Batch 51 P0: Fuel cycle ====",),
    (
        "fuel-cycle",
        "concept",
        "燃料循环",
        "fuel cycle",
        "",
        "active",
        "Closed loop of fuel supply, burn, exhaust, and reprocessing in a fusion plant",
    ),
    (
        "isotope-separation",
        "concept",
        "同位素分离",
        "isotope separation",
        "",
        "active",
        "Process to separate hydrogen isotopes (H, D, T)",
    ),
    (
        "hydrogen-isotope",
        "concept",
        "氢同位素",
        "hydrogen isotope",
        "",
        "active",
        "Isotopes of hydrogen: protium H, deuterium D, tritium T",
    ),
    (
        "protium",
        "concept",
        "氕",
        "protium",
        "H",
        "active",
        "Lightest hydrogen isotope (mass number 1)",
    ),
    (
        "tritium-storage",
        "system",
        "氚储存",
        "tritium storage",
        "",
        "active",
        "Systems for safe containment and inventory of tritium",
    ),
    (
        "tritium-recovery",
        "concept",
        "氚回收",
        "tritium recovery",
        "",
        "active",
        "Extraction of tritium from blanket breeder or plasma exhaust",
    ),
    (
        "tritium-processing",
        "concept",
        "氚处理",
        "tritium processing",
        "",
        "active",
        "Purification, isotope separation, and preparation of tritium for re-fueling",
    ),
    (
        "palladium-membrane",
        "material",
        "钯膜",
        "palladium membrane",
        "",
        "active",
        "Pd-based selective membrane for hydrogen isotope permeation/separation",
    ),
    (
        "getter-bed",
        "system",
        "吸气剂床",
        "getter bed",
        "",
        "active",
        "Metal getter (U, Zr-alloy) bed for reversible tritium storage",
    ),
    (
        "glovebox",
        "system",
        "手套箱",
        "glovebox",
        "",
        "active",
        "Sealed enclosure with inert atmosphere for tritium handling",
    ),
]

# ── NEW ALIASES (for 28 new concepts) ─────────────────────────────
aliases: list[tuple] = [
    ("# ==== Batch 51 P0: Transport / micro-instabilities ====",),
    # gyro-bohm-scaling
    ("gyro-Bohm scaling", "gyro-bohm-scaling", "en", "preferred", ""),
    ("旋回Bohm标度", "gyro-bohm-scaling", "zh", "preferred", "preferred zh"),
    ("gyroBohm scaling", "gyro-bohm-scaling", "en", "alias", "no-hyphen variant"),
    (
        "gyro-Bohm transport scaling",
        "gyro-bohm-scaling",
        "en",
        "alias",
        "expanded form",
    ),
    (
        "旋回玻姆标度",
        "gyro-bohm-scaling",
        "zh",
        "alias",
        "full-Chinese transliteration",
    ),
    # turbulent-diffusion
    ("turbulent diffusion", "turbulent-diffusion", "en", "preferred", ""),
    (
        "湍流扩散输运",
        "turbulent-diffusion",
        "zh",
        "preferred",
        "preferred zh (distinguishes from 湍流扩展)",
    ),
    ("turbulent diffusivity", "turbulent-diffusion", "en", "alias", "coefficient form"),
    # particle-pinch
    ("particle pinch", "particle-pinch", "en", "preferred", ""),
    ("粒子箍缩", "particle-pinch", "zh", "preferred", "preferred zh"),
    ("inward particle pinch", "particle-pinch", "en", "alias", "directional form"),
    ("particle pinch velocity", "particle-pinch", "en", "alias", "velocity quantity"),
    ("内向粒子输运", "particle-pinch", "zh", "alias", "directional zh"),
    # thermodiffusion
    ("thermodiffusion", "thermodiffusion", "en", "preferred", ""),
    ("热扩散", "thermodiffusion", "zh", "preferred", "preferred zh"),
    (
        "temperature screening",
        "thermodiffusion",
        "en",
        "alias",
        "tokamak-specific term",
    ),
    ("thermal diffusion", "thermodiffusion", "en", "alias", "general physics form"),
    ("Soret effect", "thermodiffusion", "en", "alias", "named after Charles Soret"),
    ("温度屏蔽", "thermodiffusion", "zh", "alias", "temperature screening zh"),
    ("# ==== Batch 51 P0: MHD stability ====",),
    # external-kink
    ("external kink mode", "external-kink", "en", "preferred", ""),
    ("外扭曲模", "external-kink", "zh", "preferred", "preferred zh"),
    ("external kink", "external-kink", "en", "alias", "short form"),
    ("external kink instability", "external-kink", "en", "alias", "instability form"),
    ("外扭曲不稳定性", "external-kink", "zh", "alias", "instability zh form"),
    # sausage-instability
    ("sausage instability", "sausage-instability", "en", "preferred", ""),
    ("腊肠不稳定性", "sausage-instability", "zh", "preferred", "preferred zh"),
    ("sausage mode", "sausage-instability", "en", "alias", "mode form"),
    ("m=0 instability", "sausage-instability", "en", "alias", "mode number form"),
    ("m=0 mode", "sausage-instability", "en", "alias", "mode number shorthand"),
    ("腊肠模", "sausage-instability", "zh", "alias", "mode zh form"),
    ("香肠不稳定性", "sausage-instability", "zh", "alias", "alt zh transliteration"),
    # pressure-driven-mode
    ("pressure-driven mode", "pressure-driven-mode", "en", "preferred", ""),
    ("压力驱动模", "pressure-driven-mode", "zh", "preferred", "preferred zh"),
    (
        "pressure driven instability",
        "pressure-driven-mode",
        "en",
        "alias",
        "instability form",
    ),
    ("压力驱动不稳定性", "pressure-driven-mode", "zh", "alias", "instability zh"),
    # current-driven-mode
    ("current-driven mode", "current-driven-mode", "en", "preferred", ""),
    ("电流驱动模", "current-driven-mode", "zh", "preferred", "preferred zh"),
    (
        "current driven instability",
        "current-driven-mode",
        "en",
        "alias",
        "instability form",
    ),
    ("电流驱动不稳定性", "current-driven-mode", "zh", "alias", "instability zh"),
    # ideal-mhd-stability
    ("ideal MHD stability", "ideal-mhd-stability", "en", "preferred", ""),
    ("理想MHD稳定性", "ideal-mhd-stability", "zh", "preferred", "preferred zh"),
    ("ideal MHD stability limit", "ideal-mhd-stability", "en", "alias", "limit form"),
    ("理想磁流体稳定性", "ideal-mhd-stability", "zh", "alias", "full Chinese form"),
    # resistive-instability
    ("resistive instability", "resistive-instability", "en", "preferred", ""),
    ("电阻不稳定性", "resistive-instability", "zh", "preferred", "preferred zh"),
    ("resistive mode", "resistive-instability", "en", "alias", "mode form"),
    ("电阻模", "resistive-instability", "zh", "alias", "mode zh form"),
    # global-alfven-eigenmode
    ("global Alfvén eigenmode", "global-alfven-eigenmode", "en", "preferred", ""),
    ("全局Alfvén本征模", "global-alfven-eigenmode", "zh", "preferred", "preferred zh"),
    ("GAE", "global-alfven-eigenmode", "abbr", "preferred", "canonical abbr"),
    (
        "global Alfven eigenmode",
        "global-alfven-eigenmode",
        "en",
        "alias",
        "no-accent form",
    ),
    (
        "全局阿尔芬本征模",
        "global-alfven-eigenmode",
        "zh",
        "alias",
        "full-Chinese transliteration",
    ),
    ("# ==== Batch 51 P0: SOL / divertor physics ====",),
    # parallel-heat-flux
    ("parallel heat flux", "parallel-heat-flux", "en", "preferred", ""),
    ("平行热流", "parallel-heat-flux", "zh", "preferred", "preferred zh"),
    ("q_parallel", "parallel-heat-flux", "en", "alias", "symbol (ASCII)"),
    ("q∥", "parallel-heat-flux", "mixed", "alias", "symbol (Unicode parallel)"),
    ("平行热流密度", "parallel-heat-flux", "zh", "alias", "density explicit form"),
    # filament
    ("filament", "filament", "en", "preferred", "SOL filament / blob structure"),
    ("等离子体丝状体", "filament", "zh", "preferred", "preferred zh"),
    ("SOL filament", "filament", "en", "alias", "SOL context"),
    ("plasma filament", "filament", "en", "alias", "plasma context"),
    ("丝状体", "filament", "zh", "alias", "short zh form"),
    # divertor-leg
    ("divertor leg", "divertor-leg", "en", "preferred", ""),
    ("偏滤器腿", "divertor-leg", "zh", "preferred", "preferred zh"),
    ("inner divertor leg", "divertor-leg", "en", "alias", "inner leg"),
    ("outer divertor leg", "divertor-leg", "en", "alias", "outer leg"),
    ("偏滤器内腿", "divertor-leg", "zh", "alias", "inner leg zh"),
    ("偏滤器外腿", "divertor-leg", "zh", "alias", "outer leg zh"),
    # flux-tube
    ("flux tube", "flux-tube", "en", "preferred", ""),
    ("磁通管", "flux-tube", "zh", "preferred", "preferred zh"),
    ("flux-tube", "flux-tube", "en", "alias", "hyphenated form"),
    # connection-length
    ("connection length", "connection-length", "en", "preferred", ""),
    ("连接长度", "connection-length", "zh", "preferred", "preferred zh"),
    ("L_c", "connection-length", "en", "alias", "symbol"),
    ("场线连接长度", "connection-length", "zh", "alias", "full zh form"),
    # wetted-area
    ("wetted area", "wetted-area", "en", "preferred", ""),
    ("湿润面积", "wetted-area", "zh", "preferred", "preferred zh"),
    ("wetted surface area", "wetted-area", "en", "alias", "expanded form"),
    ("# ==== Batch 51 P0: Fuel cycle ====",),
    # fuel-cycle
    ("fuel cycle", "fuel-cycle", "en", "preferred", ""),
    ("燃料循环", "fuel-cycle", "zh", "preferred", "preferred zh"),
    ("fusion fuel cycle", "fuel-cycle", "en", "alias", "fusion-specific"),
    ("DT fuel cycle", "fuel-cycle", "en", "alias", "DT context"),
    ("聚变燃料循环", "fuel-cycle", "zh", "alias", "fusion context zh"),
    # isotope-separation
    ("isotope separation", "isotope-separation", "en", "preferred", ""),
    ("同位素分离", "isotope-separation", "zh", "preferred", "preferred zh"),
    ("hydrogen isotope separation", "isotope-separation", "en", "alias", "H-specific"),
    ("氢同位素分离", "isotope-separation", "zh", "alias", "H-specific zh"),
    # hydrogen-isotope
    ("hydrogen isotope", "hydrogen-isotope", "en", "preferred", ""),
    ("氢同位素", "hydrogen-isotope", "zh", "preferred", "preferred zh"),
    ("hydrogen isotopes", "hydrogen-isotope", "en", "alias", "plural form"),
    # protium
    ("protium", "protium", "en", "preferred", ""),
    ("氕", "protium", "zh", "preferred", "preferred zh"),
    ("H", "protium", "abbr", "preferred", "element symbol"),
    ("light hydrogen", "protium", "en", "alias", "descriptive name"),
    # tritium-storage
    ("tritium storage", "tritium-storage", "en", "preferred", ""),
    ("氚储存", "tritium-storage", "zh", "preferred", "preferred zh"),
    ("tritium storage system", "tritium-storage", "en", "alias", "system form"),
    ("氚贮存", "tritium-storage", "zh", "alias", "variant zh char"),
    # tritium-recovery
    ("tritium recovery", "tritium-recovery", "en", "preferred", ""),
    ("氚回收", "tritium-recovery", "zh", "preferred", "preferred zh"),
    ("tritium extraction", "tritium-recovery", "en", "alias", "extraction context"),
    ("氚提取", "tritium-recovery", "zh", "alias", "extraction zh"),
    # tritium-processing
    ("tritium processing", "tritium-processing", "en", "preferred", ""),
    ("氚处理", "tritium-processing", "zh", "preferred", "preferred zh"),
    ("tritium cleanup", "tritium-processing", "en", "alias", "cleanup context"),
    ("氚纯化", "tritium-processing", "zh", "alias", "purification zh"),
    # palladium-membrane
    ("palladium membrane", "palladium-membrane", "en", "preferred", ""),
    ("钯膜", "palladium-membrane", "zh", "preferred", "preferred zh"),
    ("Pd membrane", "palladium-membrane", "en", "alias", "element-symbol form"),
    ("钯合金膜", "palladium-membrane", "zh", "alias", "alloy variant"),
    # getter-bed
    ("getter bed", "getter-bed", "en", "preferred", ""),
    ("吸气剂床", "getter-bed", "zh", "preferred", "preferred zh"),
    ("getter", "getter-bed", "en", "alias", "short form"),
    ("metal getter", "getter-bed", "en", "alias", "material context"),
    ("金属吸气剂", "getter-bed", "zh", "alias", "material context zh"),
    # glovebox
    ("glovebox", "glovebox", "en", "preferred", ""),
    ("手套箱", "glovebox", "zh", "preferred", "preferred zh"),
    ("glove box", "glovebox", "en", "alias", "two-word variant"),
    ("tritium glovebox", "glovebox", "en", "alias", "tritium context"),
    ("# ==== Batch 51 P0: Enrichment aliases for existing concepts ====",),
    # kink-mode enrichment
    ("kink instability", "kink-mode", "en", "alias", "instability form"),
    # internal-kink-mode enrichment
    ("internal kink", "internal-kink-mode", "en", "alias", "short form"),
    (
        "internal kink instability",
        "internal-kink-mode",
        "en",
        "alias",
        "instability form",
    ),
    # sol-width enrichment
    ("λ_q", "sol-width", "mixed", "alias", "Greek symbol"),
    ("power fall-off length", "sol-width", "en", "alias", "synonym"),
    ("功率衰减长度", "sol-width", "zh", "alias", "synonym zh"),
    ("热流衰减宽度", "sol-width", "zh", "alias", "heat flux width zh"),
    # divertor-target enrichment
    ("target plate", "divertor-target", "en", "alias", "short form"),
    ("靶板", "divertor-target", "zh", "alias", "short zh form"),
]

# ── EVIDENCE (28 new concepts) ─────────────────────────────────────
evidence: list[tuple] = [
    ("# ==== Batch 51 P0 ====",),
    (
        "gyro-bohm-scaling",
        "https://en.wikipedia.org/wiki/Bohm_diffusion",
        "",
        "",
        TODAY,
    ),
    (
        "turbulent-diffusion",
        "internal:fusion-transport:turbulent-diffusion",
        "",
        "",
        TODAY,
    ),
    ("particle-pinch", "internal:fusion-transport:particle-pinch", "", "", TODAY),
    ("thermodiffusion", "internal:fusion-transport:thermodiffusion", "", "", TODAY),
    ("external-kink", "internal:mhd-stability:external-kink", "", "", TODAY),
    (
        "sausage-instability",
        "https://en.wikipedia.org/wiki/Pinch_(plasma_physics)",
        "",
        "",
        TODAY,
    ),
    ("pressure-driven-mode", "internal:mhd-stability:pressure-driven", "", "", TODAY),
    ("current-driven-mode", "internal:mhd-stability:current-driven", "", "", TODAY),
    ("ideal-mhd-stability", "internal:mhd-stability:ideal-mhd", "", "", TODAY),
    ("resistive-instability", "internal:mhd-stability:resistive-instab", "", "", TODAY),
    ("global-alfven-eigenmode", "internal:mhd-alfven-eigenmode:gae", "", "", TODAY),
    ("parallel-heat-flux", "internal:sol-divertor:parallel-heat-flux", "", "", TODAY),
    ("filament", "internal:sol-divertor:filament", "", "", TODAY),
    ("divertor-leg", "internal:sol-divertor:divertor-leg", "", "", TODAY),
    ("flux-tube", "internal:sol-divertor:flux-tube", "", "", TODAY),
    ("connection-length", "internal:sol-divertor:connection-length", "", "", TODAY),
    ("wetted-area", "internal:sol-divertor:wetted-area", "", "", TODAY),
    ("fuel-cycle", "internal:fuel-cycle:overview", "", "", TODAY),
    ("isotope-separation", "internal:fuel-cycle:isotope-separation", "", "", TODAY),
    (
        "hydrogen-isotope",
        "https://en.wikipedia.org/wiki/Isotopes_of_hydrogen",
        "",
        "",
        TODAY,
    ),
    ("protium", "https://en.wikipedia.org/wiki/Hydrogen-1", "", "", TODAY),
    ("tritium-storage", "internal:fuel-cycle:tritium-storage", "", "", TODAY),
    ("tritium-recovery", "internal:fuel-cycle:tritium-recovery", "", "", TODAY),
    ("tritium-processing", "internal:fuel-cycle:tritium-processing", "", "", TODAY),
    ("palladium-membrane", "internal:fuel-cycle:palladium-membrane", "", "", TODAY),
    ("getter-bed", "internal:fuel-cycle:getter-bed", "", "", TODAY),
    ("glovebox", "internal:fuel-cycle:glovebox", "", "", TODAY),
]

# ── EXECUTE ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    write_tsv_rows(REG / "concepts.tsv", concepts)
    print(
        f"✓ Appended {sum(1 for r in concepts if not r[0].startswith('#'))} concept rows"
    )

    write_tsv_rows(REG / "aliases.tsv", aliases)
    print(
        f"✓ Appended {sum(1 for r in aliases if not r[0].startswith('#'))} alias rows"
    )

    write_tsv_rows(REG / "evidence.tsv", evidence)
    print(
        f"✓ Appended {sum(1 for r in evidence if not r[0].startswith('#'))} evidence rows"
    )

    print("Done — run validate_registry next.")
