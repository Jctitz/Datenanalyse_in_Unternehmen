
"""
Dieses Modul enthält die Formeln/Funktionen zur Berechnung der Finanzkennzahlen in diesem Projekt.

Die Funktionen sind optimiert für die Berechnung einzelner Kennzahlen und
können direkt mit numpy-Arrays angewendet werden.
"""

import numpy as np
import pandas as pd
from scipy import stats
from typing import Union, Sequence, Tuple, Optional, Callable


def annualized_return(returns: np.ndarray) -> float:
    """
    Berechnet die annualisierte Rendite.

    Args:
        returns: Array der monatlichen Renditen (als Dezimalzahlen)

    Returns:
        Annualisierte Rendite als Dezimalzahl
    """
    returns = np.asarray(returns, dtype=np.float64)
    mask = ~np.isnan(returns)
    returns = returns[mask]
    
    if len(returns) == 0:
        return np.nan
    
    # Berechne kumuliertes Produkt aller (1 + Rendite)
    cum_return = np.prod(1 + returns)
    
    # Annualisiere die Rendite (für monatliche Daten)
    return (cum_return ** (12 / len(returns))) - 1


def volatility(returns: np.ndarray) -> float:
    """
    Berechnet die annualisierte Volatilität (Standardabweichung) der Renditen.

    Args:
        returns: Array der monatlichen Renditen

    Returns:
        Annualisierte Volatilität als Dezimalzahl
    """
    returns = np.asarray(returns, dtype=np.float64)
    return np.nanstd(returns, ddof=1) * np.sqrt(12)


def maximum_drawdown(returns: np.ndarray) -> float:
    """
    Berechnet den maximalen Drawdown.

    Args:
        returns: Array der monatlichen Renditen

    Returns:
        Maximaler Drawdown als Dezimalzahl (positiver Wert)

    """
    returns = np.asarray(returns, dtype=np.float64)
    if np.isnan(returns).all():
        return np.nan
    
    # Berechne kumulierte Renditen
    cum_returns = np.cumprod(1 + np.nan_to_num(returns, nan=0))
    
    # Berechne den gleitenden Maximalwert
    running_max = np.maximum.accumulate(cum_returns)
    
    # Berechne Drawdowns
    drawdowns = 1 - cum_returns / running_max
    
    # Gib den maximalen Drawdown zurück
    return np.nanmax(drawdowns)


def sharpe_ratio(returns: np.ndarray, risk_free_rate: Union[float, np.ndarray]) -> float:
    """
    Berechnet die Sharpe Ratio.

    Args:
        returns: Array der monatlichen Renditen
        risk_free_rate: Risikoloser Zinssatz (monatlich) als Skalar oder Array

    Returns:
        Sharpe Ratio (annualisiert)

    """
    returns = np.asarray(returns, dtype=np.float64)
    
    # Wenn risk_free_rate ein Array ist, berechne Überschussrenditen
    if isinstance(risk_free_rate, np.ndarray) or isinstance(risk_free_rate, list):
        risk_free_rate = np.asarray(risk_free_rate, dtype=np.float64)
        excess_returns = returns - risk_free_rate
        ann_excess_return = annualized_return(excess_returns)
        vol = volatility(excess_returns)
    else:
        # Für eine konstante risikolose Rendite
        ann_return = annualized_return(returns)
        ann_excess_return = ann_return - risk_free_rate
        vol = volatility(returns)
    
    if vol == 0 or np.isnan(vol):
        return np.nan
    
    return ann_excess_return / vol


def omega_ratio(returns: np.ndarray, threshold: float = 0.0) -> float:
    """
    Berechnet das Omega-Ratio, das die Wahrscheinlichkeit gewichteter Gewinne 
    zu gewichteten Verlusten relativ zu einem Schwellenwert misst.

    Args:
        returns: Array der monatlichen Renditen
        threshold: Rendite-Schwellenwert (Standard: 0)

    Returns:
        Omega Ratio
    """
    returns = np.asarray(returns, dtype=np.float64)
    returns = returns[~np.isnan(returns)]
    
    if len(returns) == 0:
        return np.nan
    
    # Berechne Überschüsse und Verluste relativ zum Schwellenwert
    gains = np.sum(np.maximum(returns - threshold, 0))
    losses = np.sum(np.maximum(threshold - returns, 0))
    
    if losses == 0:
        return 1000 # hohen Wert zurückgeben statt unendlich, damit Ränge gebildet werdne können
    
    return gains / losses

def worst_month(returns: np.ndarray) -> float:
    """
    Ermittelt die schlechteste monatliche Rendite.

    Args:
        returns: Array der monatlichen Renditen

    Returns:
        Schlechteste monatliche Rendite als Dezimalzahl
    """
    returns = np.asarray(returns, dtype=np.float64)
    
    if np.all(np.isnan(returns)):
        return np.nan
    
    return np.nanmin(returns)



def tracking_error(returns: np.ndarray, benchmark_returns: np.ndarray) -> float:
    """
    Berechnet den Tracking Error zwischen den Fondsrenditen und den Benchmark-Renditen.

    Args:
        returns: Array der monatlichen Fondsrenditen
        benchmark_returns: Array der monatlichen Benchmark-Renditen

    Returns:
        Tracking Error (annualisiert)
    """
    returns = np.asarray(returns, dtype=np.float64)
    benchmark_returns = np.asarray(benchmark_returns, dtype=np.float64)
    
    # Berechne die Differenz-Renditen (aktive Renditen)
    active_returns = returns - benchmark_returns
    
    # Entferne NaN-Werte
    active_returns = active_returns[~np.isnan(active_returns)]
    
    if len(active_returns) <= 1:
        return np.nan
    
    # Berechne die annualisierte Standardabweichung der aktiven Renditen
    return np.std(active_returns, ddof=1) * np.sqrt(12)


def beta(returns: np.ndarray, benchmark_returns: np.ndarray) -> float:
    """
    Berechnet das Beta (Maß für die Sensitivität gegenüber Marktbewegungen).

    Args:
        returns: Array der monatlichen Fondsrenditen
        benchmark_returns: Array der monatlichen Benchmark-Renditen

    Returns:
        Beta-Koeffizient
    """
    returns = np.asarray(returns, dtype=np.float64)
    benchmark_returns = np.asarray(benchmark_returns, dtype=np.float64)
    
    # Entferne NaN-Werte
    valid = ~(np.isnan(returns) | np.isnan(benchmark_returns))
    if valid.sum() <= 1:
        return np.nan
    
    returns_valid = returns[valid]
    benchmark_valid = benchmark_returns[valid]
    
    # Berechne die Kovarianz
    cov = np.cov(returns_valid, benchmark_valid, ddof=1)[0, 1]
    
    # Berechne die Varianz des Benchmarks
    var = np.var(benchmark_valid, ddof=1)
    
    if var == 0:
        return np.nan
    
    return cov / var


def r_squared(returns: np.ndarray, benchmark_returns: np.ndarray) -> float:
    """
    Berechnet das Bestimmtheitsmaß (R2) zwischen Fonds und Benchmark.

    Args:
        returns: Array der monatlichen Fondsrenditen
        benchmark_returns: Array der monatlichen Benchmark-Renditen

    Returns:
        R-Quadrat (Wert zwischen 0 und 1)
    """
    returns = np.asarray(returns, dtype=np.float64)
    benchmark_returns = np.asarray(benchmark_returns, dtype=np.float64)
    
    # Entferne NaN-Werte
    valid = ~(np.isnan(returns) | np.isnan(benchmark_returns))
    if valid.sum() <= 1:
        return np.nan
    
    returns_valid = returns[valid]
    benchmark_valid = benchmark_returns[valid]
    
    # Berechne die Korrelation
    corr = np.corrcoef(returns_valid, benchmark_valid)[0, 1]
    
    return corr ** 2


def up_correlation(returns: np.ndarray, benchmark_returns: np.ndarray) -> float:
    """
    Berechnet die Korrelation der Renditen, wenn der Benchmark positive Renditen aufweist.

    Args:
        returns: Array der monatlichen Fondsrenditen
        benchmark_returns: Array der monatlichen Benchmark-Renditen

    Returns:
        Up-Korrelation (Wert zwischen -1 und 1)
    """
    returns = np.asarray(returns, dtype=np.float64)
    benchmark_returns = np.asarray(benchmark_returns, dtype=np.float64)
    
    # Identifiziere Perioden mit positiven Benchmark-Renditen
    mask = benchmark_returns > 0
    
    # Entferne NaN-Werte
    valid = mask & ~(np.isnan(returns) | np.isnan(benchmark_returns))
    
    if valid.sum() <= 1:
        return np.nan
    
    returns_up = returns[valid]
    benchmark_up = benchmark_returns[valid]
    
    # Berechne die Korrelation
    return np.corrcoef(returns_up, benchmark_up)[0, 1]


def down_correlation(returns: np.ndarray, benchmark_returns: np.ndarray) -> float:
    """
    Berechnet die Korrelation der Renditen, wenn der Benchmark negative Renditen aufweist.

    Args:
        returns: Array der monatlichen Fondsrenditen
        benchmark_returns: Array der monatlichen Benchmark-Renditen
    """
    returns = np.asarray(returns, dtype=np.float64)
    benchmark_returns = np.asarray(benchmark_returns, dtype=np.float64)
    
    # Identifiziere Perioden mit negativen Benchmark-Renditen
    mask = benchmark_returns < 0
    
    # Entferne NaN-Werte
    valid = mask & ~(np.isnan(returns) | np.isnan(benchmark_returns))
    
    if valid.sum() <= 1:
        return np.nan
    
    returns_down = returns[valid]
    benchmark_down = benchmark_returns[valid]
    
    # Berechne die Korrelation
    return np.corrcoef(returns_down, benchmark_down)[0, 1]
