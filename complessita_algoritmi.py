"""
================================================================================
  ALGORITMI E STRUTTURE DATI — FILE DI STUDIO PYTHON
  Argomento: Modello RAM, Analisi di Complessità e Notazione Asintotica
  Professore: Antonio Carzaniga — Università della Svizzera italiana
  Data slides: 23 Febbraio 2026
================================================================================

INDICE:
  1. Il modello RAM e la funzione di costo T(n)
  2. Algoritmo PINGALA (versione lenta, esponenziale)
  3. Algoritmo PINGALA-INC (versione veloce, lineare) + analisi T(n)
  4. Algoritmo FIND (ricerca lineare)
  5. Algoritmo FINDEQUALS (ricerca duplicati, quadratico)
  6. Verifica empirica della notazione asintotica (O, Omega, Theta)
  7. Dimostrazione pratica dei limiti per le notazioni o e omega
  8. Comparazione delle classi di crescita (ordine canonico)
  9. Calcolo e plot dell'ordine di crescita (con matplotlib)
================================================================================
"""

import time
import math
import sys


# ==============================================================================
# 1. MODELLO RAM — Contatore di operazioni elementari
# ==============================================================================

class ContatorePastiRAM:
    """
    Simulazione del modello RAM.

    Nel modello RAM, ogni 'passo elementare' (assegnamento, aritmetica,
    confronto, chiamata a funzione) ha costo COSTANTE = 1.
    Questa classe permette di contare manualmente i passi eseguiti
    da una funzione, dimostrando empiricamente la complessità teorica.

    Uso:
        contatore = ContatorePastiRAM()
        contatore.step()  # registra un passo elementare
        print(contatore.totale)
    """

    def __init__(self):
        self.totale = 0  # contatore globale di passi eseguiti

    def step(self, n=1):
        """
        Registra n passi elementari (default: 1).
        Nel modello RAM ogni operazione base conta come 1 passo.
        """
        self.totale += n

    def reset(self):
        """Azzera il contatore per una nuova esecuzione."""
        self.totale = 0


# Istanza globale del contatore (usata negli algoritmi qui sotto)
ram = ContatorePastiRAM()


# ==============================================================================
# 2. PINGALA — Versione lenta (esponenziale)
# ==============================================================================

def pingala(n, contatore=None):
    """
    Calcola il numero di Pingala (Fibonacci) di indice n.
    Versione RICORSIVA DIRETTA — complessità ESPONENZIALE.

    Analisi di complessità nel modello RAM:
    - Caso base (n <= 2): O(1) — un confronto e un return
    - Caso ricorsivo: T(n) = T(n-1) + T(n-2) + O(1)
      => questa ricorrenza ha soluzione T(n) = Theta(phi^n)
         dove phi = (1 + sqrt(5)) / 2 ≈ 1.618 (rapporto aureo)
      => Theta(2^n) come upper bound semplificato

    PERCHÉ È LENTO: ad ogni chiamata, il problema viene diviso in DUE
    sottoproblemi sovrapposti — pingala(n-1) ricalcola pingala(n-2),
    che era già stato calcolato nel ramo parallelo. Lavoro duplicato!

    Args:
        n: indice del numero di Pingala (n >= 1)
        contatore: istanza di ContatorePastiRAM (opzionale)

    Returns:
        Il numero di Pingala in posizione n (equivalente a Fibonacci(n))
    """
    if contatore:
        contatore.step()  # conta il confronto (passo di branch)

    # CASO BASE: per n <= 2, ritorniamo n direttamente
    # P(1) = 1, P(2) = 2  (sequenza di Pingala/Fibonacci 1-indicizzata)
    if n <= 2:
        if contatore:
            contatore.step()  # conta il return
        return n

    # CASO RICORSIVO: P(n) = P(n-1) + P(n-2)
    # Questo genera un albero di ricorsione con ~2^n foglie!
    if contatore:
        contatore.step()  # conta la somma
    return pingala(n - 1, contatore) + pingala(n - 2, contatore)


# ==============================================================================
# 3. PINGALA-INC — Versione veloce (lineare)
# ==============================================================================

def pingala_inc(n, contatore=None):
    """
    Calcola il numero di Pingala (Fibonacci) di indice n.
    Versione ITERATIVA INCREMENTALE — complessità LINEARE Theta(n).

    Analisi dettagliata nel modello RAM (dalla slide 18):
    ┌─────────────────────────────────────────────────┬──────┬─────────┐
    │ Riga di codice                                  │ Costo│  Volte  │
    ├─────────────────────────────────────────────────┼──────┼─────────┤
    │ 1: if n <= 2                                    │  c1  │    1    │
    │ 2: return n  (solo se n<=2, else non eseguita)  │  c2  │    0    │
    │ 3: pprev = 1                                    │  c3  │    1    │
    │ 4: prev = 2                                     │  c4  │    1    │
    │ 5: for i = 3 to n  (header del ciclo)           │  c5  │   n-1   │
    │ 6:   P = prev + pprev                           │  c6  │   n-2   │
    │ 7:   pprev = prev                               │  c7  │   n-2   │
    │ 8:   prev = P                                   │  c8  │   n-2   │
    │ 9: return P                                     │  c9  │    1    │
    └─────────────────────────────────────────────────┴──────┴─────────┘

    T(n) = c1 + c3 + c4 + c9 + c5*(n-1) + (c6+c7+c8)*(n-2)
    T(n) = n*C1 + C2    dove C1=(c5+c6+c7+c8), C2=costanti
    =>  T(n) = Theta(n)  — funzione LINEARE di n!

    PERCHÉ È VELOCE: invece di ricalcolare, manteniamo solo i due
    valori precedenti (pprev e prev), aggiornandoli ad ogni passo.
    Nessun lavoro duplicato.

    Args:
        n: indice del numero di Pingala (n >= 1)
        contatore: istanza di ContatorePastiRAM (opzionale)

    Returns:
        Il numero di Pingala in posizione n
    """
    if contatore:
        contatore.step()  # passo 1: confronto if n <= 2

    # CASO BASE: per n <= 2, ritorniamo n direttamente (O(1))
    if n <= 2:
        if contatore:
            contatore.step()  # passo 2: return
        return n

    # INIZIALIZZAZIONE: i primi due valori della sequenza
    # P(1) = 1, P(2) = 2
    pprev = 1   # penultimo valore (inizialmente P(1))
    prev = 2    # ultimo valore (inizialmente P(2))
    if contatore:
        contatore.step()  # passo 3: pprev = 1
        contatore.step()  # passo 4: prev = 2

    # CICLO PRINCIPALE: calcola P(i) per i da 3 a n
    # Ad ogni iterazione:
    #   - P è il nuovo valore calcolato come somma dei due precedenti
    #   - aggiorniamo pprev e prev per il prossimo passo
    P = None
    for i in range(3, n + 1):
        if contatore:
            contatore.step()  # passo 5: header del for (confronto e incremento)

        P = prev + pprev      # P(i) = P(i-1) + P(i-2)
        pprev = prev          # aggiorna penultimo: ora P(i-1) diventa il nuovo pprev
        prev = P              # aggiorna ultimo: ora P(i) diventa il nuovo prev

        if contatore:
            contatore.step()  # passo 6: P = prev + pprev
            contatore.step()  # passo 7: pprev = prev
            contatore.step()  # passo 8: prev = P

    if contatore:
        contatore.step()  # passo 9: return P
    return P


# ==============================================================================
# 4. FIND — Ricerca lineare (complessità Theta(n) nel caso peggiore)
# ==============================================================================

def find(A, x, contatore=None):
    """
    Data una sequenza A = [a1, a2, ..., an] e un valore x,
    restituisce True se A contiene x, False altrimenti.

    Algoritmo FIND dalle slide — Ricerca Lineare.

    Analisi di complessità:
    - Caso migliore: O(1) — x è il primo elemento
    - Caso peggiore: Theta(n) — x non è presente (si scorre tutto l'array)
    - Complessità nel caso peggiore: T(n) = C*n = Theta(n)

    Il 'n' qui è la dimensione dell'input misurata come numero di elementi.
    In termini di bit, se ogni elemento occupa b bit, n_bit = n*b,
    ma asintoticamente resta Theta(n_elementi).

    Args:
        A: lista/sequenza da cercare
        x: valore da trovare
        contatore: istanza di ContatorePastiRAM (opzionale)

    Returns:
        True se x è presente in A, False altrimenti
    """
    # CICLO: scansiona ogni elemento dell'array
    for i in range(len(A)):
        if contatore:
            contatore.step()  # passo 1: header del for

        if contatore:
            contatore.step()  # passo 2: confronto A[i] == x

        if A[i] == x:
            if contatore:
                contatore.step()  # passo 3: return TRUE
            return True  # trovato! uscita anticipata (best case)

    if contatore:
        contatore.step()  # passo 4: return FALSE
    return False  # non trovato: caso peggiore, si è scorso tutto


# ==============================================================================
# 5. FINDEQUALS — Ricerca duplicati (complessità Theta(n^2))
# ==============================================================================

def findequals(A, contatore=None):
    """
    Data una sequenza A = [a1, a2, ..., an], restituisce True se
    esistono due indici i != j tali che A[i] == A[j].

    Algoritmo FINDEQUALS dalle slide — Doppio ciclo annidato.

    Analisi di complessità (caso peggiore: nessun duplicato):
    - Il ciclo esterno esegue n-1 iterazioni
    - Il ciclo interno esegue (n-i) iterazioni per ogni i esterno
    - Totale confronti: (n-1) + (n-2) + ... + 1 = n*(n-1)/2

    T(n) = C * n*(n-1)/2 = C/2 * n^2 - C/2 * n = Theta(n^2)

    Ignorando il termine -C/2*n (ordine inferiore) e la costante C/2,
    otteniamo il termine dominante n^2 => Theta(n^2).

    Args:
        A: lista/sequenza da analizzare
        contatore: istanza di ContatorePastiRAM (opzionale)

    Returns:
        True se A contiene almeno due elementi uguali
    """
    n = len(A)

    # CICLO ESTERNO: fissa il primo elemento (indice i)
    for i in range(n - 1):                    # da 0 a n-2 incluso
        if contatore:
            contatore.step()  # header ciclo esterno

        # CICLO INTERNO: confronta A[i] con tutti gli elementi successivi
        # Partiamo da i+1 per evitare di confrontare un elemento con se stesso
        # e per non ripetere confronti già fatti (A[i]==A[j] è uguale a A[j]==A[i])
        for j in range(i + 1, n):             # da i+1 a n-1 incluso
            if contatore:
                contatore.step()  # header ciclo interno
                contatore.step()  # confronto A[i] == A[j]

            if A[i] == A[j]:
                if contatore:
                    contatore.step()  # return TRUE
                return True  # trovato un duplicato!

    if contatore:
        contatore.step()  # return FALSE
    return False  # nessun duplicato trovato (caso peggiore)


# ==============================================================================
# 6. VERIFICA EMPIRICA DELLA NOTAZIONE ASINTOTICA
# ==============================================================================

def is_big_o(f, g, n_test=1000, c_max=1000):
    """
    Verifica EMPIRICAMENTE se f(n) = O(g(n)).

    Definizione: f(n) = O(g(n)) se ESISTONO c > 0, n0 > 0 tali che
    f(n) <= c * g(n) per ogni n >= n0.

    Strategia: cerca un valore di c tale che f(n) <= c*g(n) per tutti
    gli n nel range [1, n_test]. Non è una prova formale, ma è utile
    per intuire la relazione.

    Args:
        f, g: funzioni da confrontare (callable: int -> float)
        n_test: range di n da testare
        c_max: costante massima da provare

    Returns:
        (bool, float): (True se sembra O, costante c trovata)
    """
    # Troviamo il valore massimo del rapporto f(n)/g(n) per n > 0
    max_ratio = 0
    for n in range(1, n_test + 1):
        g_val = g(n)
        if g_val <= 0:
            continue
        ratio = f(n) / g_val
        if ratio > max_ratio:
            max_ratio = ratio

    # Se il rapporto è limitato, f = O(g) con c = max_ratio + 1
    if max_ratio < c_max:
        return True, math.ceil(max_ratio) + 1
    else:
        return False, float('inf')


def is_theta(f, g, n_test=1000):
    """
    Verifica EMPIRICAMENTE se f(n) = Theta(g(n)).

    Definizione: f(n) = Theta(g(n)) se esistono c1, c2 > 0, n0 > 0
    tali che c1*g(n) <= f(n) <= c2*g(n) per ogni n >= n0.

    Equivalentemente: f = Theta(g) <=> f = O(g) AND f = Omega(g)
    <=> il rapporto f(n)/g(n) è limitato sia superiormente che inferiormente.

    Args:
        f, g: funzioni da confrontare
        n_test: range di n da testare

    Returns:
        (bool, float, float): (True se sembra Theta, c1 stimato, c2 stimato)
    """
    ratios = []
    for n in range(10, n_test + 1):  # partiamo da 10 per evitare edge cases
        g_val = g(n)
        if g_val <= 0:
            continue
        ratios.append(f(n) / g_val)

    if not ratios:
        return False, 0, 0

    min_ratio = min(ratios)
    max_ratio = max(ratios)

    # Per Theta, vogliamo che il rapporto converga (non diverga a 0 o infinito)
    # Soglia empirica: se max/min < 100, consideriamo il bound stretto
    is_tight = (min_ratio > 0) and (max_ratio / min_ratio < 100)
    return is_tight, min_ratio * 0.5, max_ratio * 2


# ==============================================================================
# 7. DIMOSTRAZIONE DELLE CINQUE NOTAZIONI
# ==============================================================================

def dimostra_notazioni():
    """
    Dimostra empiricamente le cinque notazioni asintotiche con esempi
    tratti direttamente dalle slide del professore.

    Esempi dimostrati:
    - n*log(n) = O(n^2)  [upper bound non stretto]
    - n^2 - n + 10 = O(n^2) [upper bound stretto]
    - T(n) di PINGALA-INC = Theta(n)
    - FINDEQUALS = Theta(n^2)
    - n*log(n) != Theta(n^2) [non è un bound stretto]
    """
    print("=" * 70)
    print("DIMOSTRAZIONE EMPIRICA DELLE NOTAZIONI ASINTOTICHE")
    print("=" * 70)

    # --- Definizioni delle funzioni dalle slide ---

    # f1(n) = n^2 + 10n + 100  => Theta(n^2)
    def f1(n): return n**2 + 10*n + 100
    def n2(n): return n**2

    # f2(n) = n + 10*log2(n)  => Theta(n)
    def f2(n): return n + 10 * math.log2(n) if n > 0 else 0
    def n_lin(n): return n

    # f3(n) = n*log(n) + n*sqrt(n)  => Theta(n*sqrt(n))
    def f3(n): return n * math.log2(n) + n * math.sqrt(n) if n > 0 else 0
    def n_sqrt(n): return n * math.sqrt(n)

    # Funzione di FINDEQUALS: T(n) = n*(n-1)/2
    def t_findequals(n): return n * (n - 1) / 2

    # Funzione di PINGALA-INC: T(n) ~ C*n (approssimiamo con n)
    def t_pingala_inc(n): return 4 * n + 3  # approssimazione con costanti reali

    esempi = [
        ("n^2 + 10n + 100", "n^2",       f1, n2,    "Theta(n^2)"),
        ("n + 10*log(n)",   "n",          f2, n_lin, "Theta(n)"),
        ("n*log(n)+n*sqrt(n)", "n*sqrt(n)", f3, n_sqrt, "Theta(n*sqrt(n))"),
        ("T(n) FINDEQUALS", "n^2",        t_findequals, n2, "Theta(n^2)"),
        ("T(n) PINGALA-INC","n",          t_pingala_inc, n_lin, "Theta(n)"),
    ]

    for nome_f, nome_g, f, g, atteso in esempi:
        ok, c1, c2 = is_theta(f, g, n_test=500)
        simbolo = "Theta" if ok else "NON Theta"
        print(f"\n  {nome_f} = {simbolo}({nome_g})")
        print(f"    Atteso: {atteso}")
        print(f"    c1 stimato: {c1:.4f},  c2 stimato: {c2:.4f}")
        if ok:
            print(f"    => f(n) e' asintoticamente STRETTA a {nome_g}")
        else:
            print(f"    => Il rapporto f(n)/g(n) NON e' limitato in entrambe le direzioni")

    print()


# ==============================================================================
# 8. COMPARAZIONE DELLE CLASSI DI CRESCITA
# ==============================================================================

def tabella_crescita(n_values=None):
    """
    Stampa una tabella comparativa delle principali classi di crescita
    per valori crescenti di n.

    L'ordine canonico delle classi di crescita (dal più lento al più veloce):
    O(1) < O(log n) < O(sqrt(n)) < O(n) < O(n log n) < O(n^1.5) < O(n^2) < O(2^n) < O(3^n)

    Questo è l'ordine che compare nelle ultime slide della presentazione.
    """
    if n_values is None:
        n_values = [1, 2, 5, 10, 20, 50, 100]

    print("=" * 90)
    print("TABELLA DELLE CLASSI DI CRESCITA")
    print("(tutte le funzioni ignorate le costanti, visualizzate per n crescente)")
    print("=" * 90)

    # Header
    header = f"{'n':>6} | {'1':>8} | {'log n':>8} | {'sqrt(n)':>8} | {'n':>8} | {'n log n':>10} | {'n^2':>10} | {'2^n':>12}"
    print(header)
    print("-" * 90)

    for n in n_values:
        log_n  = math.log2(n) if n > 0 else 0
        sqrt_n = math.sqrt(n)
        nlogn  = n * math.log2(n) if n > 0 else 0
        n2     = n ** 2
        two_n  = 2 ** n if n <= 30 else float('inf')  # evita overflow

        # Formattazione: usiamo inf per valori troppo grandi
        def fmt(x):
            if x == float('inf') or x > 1e15:
                return "     >10^15"
            return f"{x:>10.1f}"

        print(f"{n:>6} | {1:>8} | {log_n:>8.2f} | {sqrt_n:>8.2f} | {n:>8} | {nlogn:>10.2f} | {n2:>10} | {fmt(two_n)}")

    print()
    print("ORDINE DI DOMINANZA (da sinistra a destra, ognuno domina il precedente):")
    print("  1  <<  log(n)  <<  sqrt(n)  <<  n  <<  n*log(n)  <<  n^2  <<  2^n  <<  3^n")
    print()


# ==============================================================================
# 9. ANALISI TEMPORALE EMPIRICA (misurazione con time.time)
# ==============================================================================

def benchmark_pingala():
    """
    Confronto empirico dei tempi di esecuzione tra PINGALA (esponenziale)
    e PINGALA-INC (lineare) per valori crescenti di n.

    ATTENZIONE: per n > 30, PINGALA diventa estremamente lento.
    Questo dimostra empiricamente la differenza tra Theta(n) e Theta(2^n).
    """
    print("=" * 60)
    print("BENCHMARK EMPIRICO: PINGALA vs PINGALA-INC")
    print("=" * 60)
    print(f"{'n':>6} | {'PINGALA (s)':>12} | {'PINGALA-INC (s)':>16} | {'Ratio':>10}")
    print("-" * 60)

    valori_n = [5, 10, 15, 20, 25, 30, 35]

    for n in valori_n:
        # Benchmark PINGALA lento (esponenziale)
        if n <= 35:
            inizio = time.perf_counter()
            pingala(n)
            t_lento = time.perf_counter() - inizio
        else:
            t_lento = float('inf')  # troppo lento

        # Benchmark PINGALA-INC veloce (lineare)
        inizio = time.perf_counter()
        for _ in range(1000):  # ripetiamo 1000 volte per misurare meglio
            pingala_inc(n)
        t_veloce = (time.perf_counter() - inizio) / 1000

        ratio = t_lento / t_veloce if t_veloce > 0 else float('inf')
        print(f"{n:>6} | {t_lento:>12.6f} | {t_veloce:>16.8f} | {ratio:>10.1f}x")

    print("\n  => La differenza cresce esponenzialmente: questo E' il significato di Theta(2^n) vs Theta(n)!")
    print()


def analisi_passi_ram():
    """
    Conta i passi RAM eseguiti da PINGALA-INC per valori diversi di n,
    e confronta con la formula teorica T(n) = n*C1 + C2.

    Questo dimostra che T(n) è ESATTAMENTE lineare nel modello RAM.
    """
    print("=" * 70)
    print("ANALISI DEI PASSI RAM — PINGALA-INC")
    print("Confronto tra passi effettivi e formula teorica T(n) = a*n + b")
    print("=" * 70)
    print(f"{'n':>6} | {'Passi RAM':>10} | {'Passi/n':>10} | {'Verifica lineare':>20}")
    print("-" * 70)

    valori_n = [3, 5, 10, 20, 50, 100, 500]
    passi_list = []

    for n in valori_n:
        ram.reset()
        pingala_inc(n, ram)
        passi = ram.totale
        passi_list.append((n, passi))
        ratio = passi / n
        print(f"{n:>6} | {passi:>10} | {ratio:>10.3f} | T(n)/n ~ {ratio:.2f} (costante)")

    # Verifichiamo la linearità: il rapporto T(n)/n deve essere circa costante
    ratios = [p/n for n, p in passi_list]
    variazione = max(ratios) - min(ratios)
    print(f"\n  Variazione del rapporto T(n)/n: {variazione:.3f}")
    print(f"  => Piu' il rapporto e' costante, piu' la crescita e' Theta(n)")
    print()


# ==============================================================================
# MAIN — Esegue tutte le dimostrazioni
# ==============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  STUDIO DI ALGORITMI E STRUTTURE DATI")
    print("  Modello RAM e Crescita delle Funzioni")
    print("=" * 70 + "\n")

    # ── 1. Verifica che gli algoritmi producano risultati corretti ──
    print("VERIFICA CORRETTEZZA ALGORITMI:")
    print("-" * 40)
    for n in range(1, 11):
        p_lento = pingala(n)
        p_veloce = pingala_inc(n)
        assert p_lento == p_veloce, f"ERRORE: pingala({n})={p_lento} != pingala_inc({n})={p_veloce}"
        print(f"  P({n:>2}) = {p_lento:>5}  [PINGALA == PINGALA-INC: OK]")

    print()

    # ── 2. Test FIND e FINDEQUALS ──
    print("TEST FIND e FINDEQUALS:")
    print("-" * 40)
    A = [3, 1, 4, 1, 5, 9, 2, 6]
    print(f"  Array A = {A}")
    print(f"  FIND(A, 5) = {find(A, 5)}   (atteso: True)")
    print(f"  FIND(A, 7) = {find(A, 7)}  (atteso: False)")
    print(f"  FINDEQUALS(A) = {findequals(A)}   (atteso: True, A[1]==A[3]==1)")

    B = [1, 2, 3, 4, 5]
    print(f"\n  Array B = {B} (tutti distinti)")
    print(f"  FINDEQUALS(B) = {findequals(B)}  (atteso: False)")
    print()

    # ── 3. Analisi passi RAM ──
    analisi_passi_ram()

    # ── 4. Tabella di crescita ──
    tabella_crescita([1, 5, 10, 20, 30])

    # ── 5. Verifica notazioni asintotiche ──
    dimostra_notazioni()

    # ── 6. Benchmark temporale ──
    benchmark_pingala()

    print("=" * 70)
    print("  STUDIO COMPLETATO! Rileggere gli appunti Word per la teoria.")
    print("=" * 70)
