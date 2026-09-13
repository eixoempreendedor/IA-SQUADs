#!/usr/bin/env python3
"""Regras de dimensionamento do simulado de Nivel 2.

O tamanho do lote segue a quantidade de topicos do grupo, para que a cobertura
por topico fique parecida em todos os dias (~3,5 a 4,5 questoes por topico):

    ate 14 topicos  -> 50 questoes (meta 45)
    15 ou mais      -> 60 questoes (meta 54)

Dentro do lote, cada topico recebe no minimo COTA_MINIMA questoes e o restante
e distribuido na proporcao do peso, por maior resto. Sem isso, um topico de
peso 1 ficaria com menos de duas questoes e o grupo poderia ser aprovado sem
que ele fosse testado de verdade.
"""
from __future__ import annotations

COTA_MINIMA = 2
META = 0.90


def tamanho_do_lote(n_topicos: int) -> int:
    return 60 if n_topicos >= 15 else 50


def meta_do_lote(total: int) -> int:
    return round(total * META)


def topicos_do_grupo(grupo: dict, materias: dict) -> list[tuple[str, str, int]]:
    """[(materia_id, topico_n, peso)] na ordem em que aparecem no grupo."""
    saida = []
    for bloco in grupo["materias"]:
        pesos = {t["n"]: t["peso"] for t in materias[bloco["id"]]["ementa"]}
        for n in bloco["topicos"]:
            saida.append((bloco["id"], n, pesos[n]))
    return saida


def cotas_por_topico(grupo: dict, materias: dict) -> dict[tuple[str, str], int]:
    """Distribui o lote entre os topicos: minimo fixo + resto proporcional ao peso."""
    topicos = topicos_do_grupo(grupo, materias)
    total = tamanho_do_lote(len(topicos))
    resto = total - COTA_MINIMA * len(topicos)
    if resto < 0:
        raise ValueError(f"{grupo['id']}: {len(topicos)} topicos nao cabem em {total} questoes")

    peso_total = sum(p for _, _, p in topicos)
    exatos = [(mid, n, resto * p / peso_total) for mid, n, p in topicos]
    cotas = {(mid, n): COTA_MINIMA + int(v) for mid, n, v in exatos}
    sobra = total - sum(cotas.values())
    for mid, n, v in sorted(exatos, key=lambda e: -(e[2] - int(e[2])))[:sobra]:
        cotas[(mid, n)] += 1
    return cotas


def cotas_por_materia(grupo: dict, materias: dict) -> dict[str, int]:
    por_topico = cotas_por_topico(grupo, materias)
    saida: dict[str, int] = {}
    for (mid, _), q in por_topico.items():
        saida[mid] = saida.get(mid, 0) + q
    return saida


def resumo(grupo: dict, materias: dict) -> dict:
    topicos = topicos_do_grupo(grupo, materias)
    total = tamanho_do_lote(len(topicos))
    return {
        "topicos": len(topicos),
        "peso": sum(p for _, _, p in topicos),
        "total": total,
        "meta": meta_do_lote(total),
        "por_materia": cotas_por_materia(grupo, materias),
        "por_topico": cotas_por_topico(grupo, materias),
    }
