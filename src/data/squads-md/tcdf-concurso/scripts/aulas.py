#!/usr/bin/env python3
"""Relaciona as aulas do Gran com o edital, no nivel do SUBTOPICO.

O rotulo de cada aula em gran.json ja diz o recorte que ela cobre — a aula 3 de
AFO e "1.4 Ciclo orcamentario. 1.5 Processo orcamentario". Daqui sai um mapa que
responde, para cada subtopico do edital, quais aulas o cobrem e com que precisao:

  EXATA   o rotulo da aula cita aquele subtopico (ou cita o topico inteiro sem
          recortar subtopico, caso em que a aula cobre todos eles)
  TOPICO  nenhuma aula cita este subtopico, mas o topico tem aulas — elas servem
          de referencia, sem garantia de que aquele pedaco esta la dentro

A distincao importa: com EXATA da para montar o filtro do Gran sabendo o que
entra; com TOPICO o candidato ainda precisa conferir a aula.

Uso como script: imprime a cobertura.
    python3 scripts/aulas.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

EXATA = "exata"
TOPICO = "topico"


def subtopicos_do_texto(n: str, texto: str) -> list[str]:
    """['1.1', '1.2', ...] declarados na ementa do topico n.

    O recorte evita numeros de lei (4.320, 14.133, 32.598) exigindo que o prefixo
    seja o proprio numero do topico e que o sufixo tenha no maximo dois digitos.
    """
    achados = re.findall(rf"(?<![\d.]){re.escape(n)}\.\d{{1,2}}(?![\d./])", texto)
    vistos = []
    for a in achados:
        if a not in vistos:
            vistos.append(a)
    return vistos


def _citados(rotulo: str) -> set[str]:
    return set(re.findall(r"(?<![\d.])\d{1,2}\.\d{1,2}(?![\d./])", rotulo or ""))


def mapa_de_aulas(gran: dict, materias: dict) -> dict:
    """{(materia, chave): {"aulas": [n], "precisao": EXATA|TOPICO}}.

    `chave` e o numero do topico ("3") ou do subtopico ("3.2").
    """
    saida: dict[tuple[str, str], dict] = {}
    for mid, aulas in gran["materias"].items():
        if mid not in materias:
            continue
        textos = {t["n"]: t["texto"] for t in materias[mid]["ementa"]}
        exatas: dict[str, list[int]] = {}
        por_topico: dict[str, list[int]] = {}

        for a in aulas:
            citados = _citados(a.get("rotulo", ""))
            for n in a["topicos"]:
                if n not in textos:
                    continue
                por_topico.setdefault(n, []).append(a["aula"])
                proprios = sorted(s for s in citados if s.split(".")[0] == n)
                alvos = proprios or subtopicos_do_texto(n, textos[n])
                for s in alvos:
                    exatas.setdefault(s, []).append(a["aula"])

        for n, lista in por_topico.items():
            saida[(mid, n)] = {"aulas": sorted(set(lista)), "precisao": EXATA}
        for t in materias[mid]["ementa"]:
            n = t["n"]
            for s in subtopicos_do_texto(n, t["texto"]):
                if s in exatas:
                    saida[(mid, s)] = {"aulas": sorted(set(exatas[s])), "precisao": EXATA}
                elif n in por_topico:
                    saida[(mid, s)] = {"aulas": sorted(set(por_topico[n])), "precisao": TOPICO}
    return saida


def carregar(raiz: Path = RAIZ) -> dict:
    ed = json.loads((raiz / "scripts/edital.json").read_text(encoding="utf-8"))
    gran = json.loads((raiz / "scripts/gran.json").read_text(encoding="utf-8"))
    return mapa_de_aulas(gran, {m["id"]: m for m in ed["materias"]})


def main() -> int:
    ed = json.loads((RAIZ / "scripts/edital.json").read_text(encoding="utf-8"))
    mats = {m["id"]: m for m in ed["materias"]}
    mapa = carregar()

    n_top = n_sub = exatos = herdados = orfaos = 0
    faltando = []
    for mid, info in mats.items():
        for t in info["ementa"]:
            n_top += 1
            for s in subtopicos_do_texto(t["n"], t["texto"]):
                n_sub += 1
                m = mapa.get((mid, s))
                if not m:
                    orfaos += 1
                    faltando.append(f"{info['nome']} {s}")
                elif m["precisao"] == EXATA:
                    exatos += 1
                else:
                    herdados += 1

    print(f"topicos: {n_top} · subtopicos: {n_sub}")
    print(f"  aula exata do subtopico: {exatos} ({exatos / n_sub:.0%})")
    print(f"  aula herdada do topico:  {herdados} ({herdados / n_sub:.0%})")
    print(f"  sem aula nenhuma:        {orfaos}")
    for x in faltando:
        print(f"    - {x}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
