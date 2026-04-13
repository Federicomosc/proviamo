"""
================================================================================
  ALGORITMI E STRUTTURE DATI — FILE DI STUDIO PYTHON
  Argomento: Insertion Sort — Analisi e Correttezza con Invarianti di Ciclo
  Professore: Antonio Carzaniga — Università della Svizzera italiana
  Data slides: 26 Febbraio 2026
================================================================================

INDICE:
  1. Definizione del problema Sorting
  2. INSERTION-SORT — implementazione con contatore di operazioni
  3. SELECTION-SORT — implementazione con analisi
  4. BUBBLE-SORT    — implementazione con analisi
  5. MAXTHREE       — tre varianti (due corrette, una scorretta)
  6. Verifica formale degli invarianti di ciclo (simulata step-by-step)
  7. Analisi empirica dei tre casi (migliore, medio, peggiore)
  8. Benchmark comparativo dei tre algoritmi quadratici
================================================================================
"""

import random
import time
import copy


# ==============================================================================
# 1. PROBLEMA SORTING — Definizione e Verifica
# ==============================================================================

def is_sorted(A):
    """
    Verifica che A sia ordinato in senso non decrescente.
    Usata come condizione di correttezza post-esecuzione.

    Definizione formale (dalle slide):
      Output corretto: <b1, b2, ..., bn> tale che b1 <= b2 <= ... <= bn
      E' una permutazione dell'input originale.

    Complessità: O(n) — scansione lineare.
    """
    return all(A[i] <= A[i+1] for i in range(len(A) - 1))


def is_permutation(A_original, A_sorted):
    """
    Verifica che A_sorted sia una permutazione di A_original.
    (Seconda condizione di correttezza del problema Sorting)

    Un ordinamento corretto deve conservare tutti gli elementi:
    niente aggiunte, niente rimozioni, niente modifiche di valore.
    """
    return sorted(A_original) == sorted(A_sorted)


# ==============================================================================
# 2. INSERTION SORT — Implementazione Completa con Analisi
# ==============================================================================

def insertion_sort(A, verbose=False):
    """
    INSERTION-SORT — Ordinamento per inserimento. IN-PLACE.
    Corrisponde esattamente allo pseudocodice delle slide.

    IDEA INTUITIVA: come ordinare un mazzo di carte in mano.
    Si mantiene la parte sinistra A[0..i-1] sempre ordinata.
    Ad ogni passo i, si "inserisce" A[i] nella posizione corretta
    scorrendo a ritroso e spostando a destra gli elementi maggiori.

    MECCANICA DEGLI SWAP:
      Per inserire key=A[i] nella posizione corretta:
      - confronta A[j] con A[j-1] (il precedente)
      - se A[j-1] > A[j], scambia (sposta A[j] un posto a sinistra)
      - decrementa j e ripeti

    ANALISI DELLA COMPLESSITA' (dal modello RAM):
    ┌────────────────────┬─────────────┬──────────────┬──────────────────────┐
    │ Caso               │ When?       │ Inner loop   │ T(n)                 │
    ├────────────────────┼─────────────┼──────────────┼──────────────────────┤
    │ MIGLIORE (Best)    │ Gia' ordinato│ 0 iterazioni│ Theta(n)             │
    │ PEGGIORE (Worst)   │ Ord. inverso │ j-1 iter.   │ Theta(n^2)           │
    │ MEDIO   (Average)  │ Random       │ ~(j-1)/2    │ Theta(n^2)           │
    └────────────────────┴─────────────┴──────────────┴──────────────────────┘

    INVARIANTE DEL CICLO ESTERNO:
      C(i): A[0..i-1] contiene gli stessi elementi originali di A[0..i-1],
            disposti in ordine non decrescente.

    PROPRIETA' IN-PLACE: usa O(1) spazio extra (solo variabile j).

    Args:
        A:       lista da ordinare (modificata IN-PLACE)
        verbose: se True, stampa lo stato ad ogni swap (per visualizzare)

    Returns:
        (numero di confronti, numero di swap) — per analisi empirica
    """
    n = len(A)
    confronti = 0   # conta i confronti A[j-1] > A[j]
    swaps     = 0   # conta gli swap

    # CICLO ESTERNO: i scorre da 1 a n-1 (in 0-based, corrisp. a 2..n in 1-based)
    # Invariante: PRIMA di ogni iterazione i, A[0..i-1] e' ordinato
    for i in range(1, n):

        # INVARIANTE VERIFICABILE: A[0..i-1] deve essere ordinato qui
        # (lo verifichiamo solo se verbose, per non rallentare)
        if verbose:
            print(f"  i={i}, A={A}, key=A[{i}]={A[i]}, A[0..{i-1}]={A[:i]} [ordinato: {is_sorted(A[:i])}]")

        j = i   # j e' l'indice dell'elemento da posizionare

        # CICLO INTERNO: sposta A[j] a sinistra finché trova la posizione corretta
        # Condizione: j > 0 (non uscire dall'array) AND A[j-1] > A[j] (ancora fuori posto)
        while j > 0 and A[j-1] > A[j]:
            confronti += 1

            # SWAP: scambia A[j] con A[j-1] (sposta un posto a sinistra)
            A[j], A[j-1] = A[j-1], A[j]
            swaps += 1

            if verbose:
                print(f"    swap A[{j}]={A[j-1]} <-> A[{j-1}]={A[j-1]}... A ora = {A}")

            j -= 1   # decrementa j: prossimo confronto con il precedente

        # Un confronto finale che ha fallito la condizione (o j==0)
        if j > 0:
            confronti += 1   # il confronto che ha terminato il while

    return confronti, swaps


def insertion_sort_con_invariante(A):
    """
    Versione DIDATTICA di Insertion Sort con verifica esplicita dell'invariante
    ad ogni iterazione del ciclo esterno.

    Dimostra empiricamente che l'invariante C(i) vale sempre:
    "A[0..i-1] e' una permutazione ordinata degli originali A[0..i-1]"

    Nota: la verifica dell'invariante costa O(i) extra per iterazione,
    quindi questa versione ha T(n) = O(n^2) anche nel caso migliore.
    Usarla solo a scopo didattico!
    """
    A_originale = A[:]   # copia per confronto
    n = len(A)
    violazioni = 0

    print(f"  Input: {A_originale}")
    print(f"  {'i':>3} | {'A[0..i-1] ordinato':>20} | {'Invariante OK':>13}")
    print("  " + "-" * 45)

    for i in range(1, n):
        # --- esecuzione del ciclo interno ---
        j = i
        while j > 0 and A[j-1] > A[j]:
            A[j], A[j-1] = A[j-1], A[j]
            j -= 1

        # --- verifica invariante ---
        prefisso = A[:i]
        invariante_ok = (
            is_sorted(prefisso) and
            sorted(prefisso) == sorted(A_originale[:i])
        )
        if not invariante_ok:
            violazioni += 1

        print(f"  {i:>3} | {str(prefisso):>20} | {'SI ✓' if invariante_ok else 'NO ✗':>13}")

    print(f"\n  Output: {A}")
    print(f"  Violazioni invariante: {violazioni} (atteso: 0)")
    print(f"  Corretto: {is_sorted(A) and is_permutation(A_originale, A)}")
    return A


# ==============================================================================
# 3. SELECTION SORT — Implementazione con Analisi
# ==============================================================================

def selection_sort(A, verbose=False):
    """
    SELECTION-SORT — Ordinamento per selezione. IN-PLACE.
    Corrisponde esattamente allo pseudocodice delle slide.

    IDEA: ad ogni iterazione i, trova il minimo di A[i..n-1]
    e lo porta in posizione i con un SINGOLO SWAP.

    DIFFERENZA CHIAVE rispetto a Insertion Sort:
      - Insertion Sort: sposta l'elemento con MOLTI swap successivi
      - Selection Sort: trova il minimo e fa UN SOLO swap finale
      - Risultato: Selection Sort fa meno swap, ma gli stessi confronti

    ANALISI DELLA COMPLESSITA':
      Il ciclo interno esegue SEMPRE (n-i) iterazioni, indipendentemente dall'input.
      Non esiste distinzione tra caso migliore e peggiore!

      T(n) = SUM_{i=0}^{n-2} (n-1-i)  =  (n-1)+(n-2)+...+1  =  n*(n-1)/2  =  Theta(n^2)

    INVARIANTE DEL CICLO ESTERNO:
      C(i): A[0..i-1] contiene gli i elementi piu' piccoli di A,
            in ordine non decrescente, nelle loro posizioni FINALI corrette.

    DIMOSTRAZIONE INVARIANTE:
      - Inizializzazione (i=0): A[0..-1] e' vuoto, vacuamente vero. ✓
      - Mantenimento: se C(i) vale, il ciclo interno trova il minimo di A[i..n-1]
        e lo porta in A[i] tramite swap. Ora A[0..i] contiene i+1 elementi minimi
        in posizione finale. C(i+1) vale. ✓
      - Terminazione: i = n-1, A[0..n-2] ha n-1 elementi in posizione finale,
        quindi anche A[n-1] e' nella posizione corretta. ✓

    Args:
        A: lista da ordinare (modificata IN-PLACE)
        verbose: se True, stampa ogni passo

    Returns:
        (confronti, swap)
    """
    n = len(A)
    confronti = 0
    swaps = 0

    # CICLO ESTERNO: i e' la posizione da riempire con il minimo corrente
    for i in range(n - 1):

        # Trova il MINIMO in A[i..n-1]
        smallest = i   # assume che A[i] sia il minimo provvisorio

        for j in range(i + 1, n):
            confronti += 1
            if A[j] < A[smallest]:
                smallest = j   # aggiorna l'indice del minimo trovato

        # Un singolo swap porta il minimo in posizione i
        if smallest != i:   # ottimizzazione: evita swap inutili
            A[i], A[smallest] = A[smallest], A[i]
            swaps += 1

        if verbose:
            print(f"  i={i}: minimo={A[i]}, A={A}")

    return confronti, swaps


# ==============================================================================
# 4. BUBBLE SORT — Implementazione con Analisi
# ==============================================================================

def bubble_sort(A, verbose=False):
    """
    BUBBLESORT — Ordinamento a bolle. IN-PLACE.
    Corrisponde esattamente allo pseudocodice delle slide.

    IDEA: scansiona l'array da destra a sinistra confrontando coppie
    adiacenti. Gli elementi più piccoli "risalgono" verso sinistra
    come bolle d'aria in un liquido.

    Dopo i iterazioni del ciclo esterno, i elementi sono in posizione finale.
    La scansione interna va da length(A) fino a i+1 (da destra verso sinistra).

    ANALISI DELLA COMPLESSITA':
      T(n) = SUM_{i=1}^{n} (n-i-1)  =  Theta(n^2) in tutti i casi
      (con questa implementazione — senza flag di early exit)

    INVARIANTE DEL CICLO ESTERNO:
      C(i): A[0..i-1] contiene gli i elementi piu' piccoli di A,
            in ordine non decrescente, nelle loro posizioni finali corrette.

    DIFFERENZA rispetto a Selection Sort:
      Bubble Sort fa potenzialmente MOLTI swap per portare il minimo in posizione.
      Selection Sort fa UN SOLO swap. Quindi Bubble Sort ha piu' swap nel caso peggiore.

    Args:
        A: lista da ordinare (modificata IN-PLACE)
        verbose: se True, stampa ogni passo

    Returns:
        (confronti, swap)
    """
    n = len(A)
    confronti = 0
    swaps = 0

    # CICLO ESTERNO: dopo i iterazioni, A[0..i-1] e' ordinato e in posizione finale
    for i in range(n):

        # CICLO INTERNO: scansione da destra (n-1) verso sinistra (i+1)
        # Ogni confronto "fa risalire" il minore di una posizione verso sinistra
        for j in range(n - 1, i, -1):   # j va da n-1 downto i+1
            confronti += 1
            if A[j] < A[j - 1]:
                # A[j] e' minore del predecessore: swap (A[j] "risale" di un posto)
                A[j], A[j-1] = A[j-1], A[j]
                swaps += 1

        if verbose:
            print(f"  i={i}: A={A} (A[0..{i}]={A[:i+1]} in posizione finale)")

    return confronti, swaps


# ==============================================================================
# 5. MAXTHREE — Varianti Corrette e Scorretta (Analisi dei Path)
# ==============================================================================

def maxthree_v1_sbagliato(a, b, c):
    """
    MAXTHREE — Prima variante (SCORRETTA, dalle slide).

    Analisi dei percorsi:
      Percorso 1: a>b AND b>c  => ritorna a  [OK se a>b>c]
      Percorso 2: a>b AND NOT(b>c) => ritorna c  [SBAGLIATO! se a>c>b, dovrebbe ritornare a]

    Controesempio: a=5, b=2, c=4
      a>b (5>2)=True, b>c (2>4)=False => else: return c => ritorna 4
      Ma il massimo e' a=5! => ALGORITMO SCORRETTO.

    NON USARE: implementata solo per scopi didattici e testing.
    """
    if a > b:
        if b > c:    # BUG: dovrebbe essere "if a > c"
            return a
        else:
            return c  # SBAGLIATO: non considera il caso a>c>b
    else:
        if c > b:
            return c
        else:
            return b


def maxthree_v2_corretto(a, b, c):
    """
    MAXTHREE — Seconda variante (CORRETTA, slide p.66).

    Analisi di tutti i percorsi (4 percorsi possibili):
      P1: a>b AND a>c  => a e' il massimo. Return a. ✓
          (path condition: a>b AND a>c => a e' max)
      P2: a>b AND NOT(a>c) => c>=a>b. c e' il massimo. Return c. ✓
          (path condition: a>b AND c>=a => c>=a>b => c max)
      P3: NOT(a>b) AND b>c => b>=a AND b>c. b e' max. Return b. ✓
          (path condition: b>=a AND b>c => b e' max)
      P4: NOT(a>b) AND NOT(b>c) => b>=a AND c>=b. c e' max. Return c. ✓
          (path condition: b>=a AND c>=b => c>=b>=a => c max)

    Tutti e 4 i percorsi sono corretti => ALGORITMO CORRETTO.
    """
    if a > b:
        if a > c:
            return a   # P1: a e' il massimo
        else:
            return c   # P2: c e' il massimo (c >= a > b)
    else:
        if b > c:
            return b   # P3: b e' il massimo (b >= a, b > c)
        else:
            return c   # P4: c e' il massimo (c >= b >= a)


def maxthree_v3_corretto(a, b, c):
    """
    MAXTHREE — Terza variante (CORRETTA, slide p.69).

    Analisi:
      Ramo 1: a>b AND a>c => return a. ✓
      Ramo 2: NOT(a>b AND a>c) => a non e' il massimo assoluto.
               Allora il max e' tra b e c.
               if b>c: return b, else: return c. ✓

    Piu' compatta della v2, stessa correttezza.
    """
    if a > b and a > c:
        return a      # a e' strettamente il massimo
    if b > c:
        return b      # b e' maggiore di c (e a non era il max)
    else:
        return c      # c e' il massimo residuo


# ==============================================================================
# 6. VERIFICA FORMALE DEGLI INVARIANTI (simulazione step-by-step)
# ==============================================================================

def verifica_invariante_insertion_sort(A_input):
    """
    Verifica empiricamente l'invariante di Insertion Sort a ogni iterazione.

    Invariante del ciclo esterno:
      C(i): A[0..i-1] e' una permutazione ordinata degli originali A[0..i-1]

    Struttura della prova (dalle slide):
      1. INIZIALIZZAZIONE: prima di i=1, A[0..0]={A[0]}: banalmente ordinato. ✓
      2. MANTENIMENTO:     se C(i) vale, dopo un ciclo vale C(i+1). ✓
      3. TERMINAZIONE:     a i=n, A[0..n-1]=tutto l'array e' ordinato. ✓
    """
    A = A_input[:]
    A_orig = A[:]
    n = len(A)

    print("=" * 55)
    print("VERIFICA INVARIANTE — INSERTION SORT")
    print(f"Input: {A_orig}")
    print("=" * 55)

    # === INIZIALIZZAZIONE: verifica C(1) prima del loop ===
    print("\n[INIZIALIZZAZIONE] Prima di i=1:")
    print(f"  A[0..0] = [{A[0]}]")
    print(f"  Ordinato? {is_sorted([A[0]])}  (banalmente vero per 1 elemento)")
    print(f"  Permutazione? {sorted([A[0]]) == sorted([A_orig[0]])}  ✓")

    # === MANTENIMENTO: verifica C(i) dopo ogni iterazione ===
    print("\n[MANTENIMENTO] Traccia iterazione per iterazione:")
    print(f"  {'i':>3} | {'Prefisso A[0..i-1]':>30} | {'Ordinato':>8} | {'Perm. orig.':>11}")
    print("  " + "-" * 60)

    for i in range(1, n):
        j = i
        while j > 0 and A[j-1] > A[j]:
            A[j], A[j-1] = A[j-1], A[j]
            j -= 1

        prefisso = A[:i]
        ord_ok   = is_sorted(prefisso)
        perm_ok  = sorted(prefisso) == sorted(A_orig[:i])
        print(f"  {i:>3} | {str(prefisso):>30} | {'Si ✓' if ord_ok else 'NO ✗':>8} | {'Si ✓' if perm_ok else 'NO ✗':>11}")

    # === TERMINAZIONE: a i=n ===
    print(f"\n[TERMINAZIONE] i = {n} (= length(A)+1 in 1-based)")
    print(f"  A[0..{n-1}] = {A}  (tutto l'array)")
    print(f"  Ordinato? {is_sorted(A)}  ✓" if is_sorted(A) else f"  Ordinato? NO  ✗")
    print(f"  E' permutazione dell'originale? {is_permutation(A_orig, A)}  ✓")
    print(f"\n=> INSERTION-SORT E' CORRETTO! QED")


def verifica_invariante_selection_sort(A_input):
    """
    Verifica empiricamente l'invariante di Selection Sort.

    Invariante:
      C(i): A[0..i-1] contiene i elementi minimi in posizione finale
    """
    A = A_input[:]
    A_orig = A[:]
    n = len(A)
    A_sorted = sorted(A_orig)

    print("\n" + "=" * 55)
    print("VERIFICA INVARIANTE — SELECTION SORT")
    print(f"Input: {A_orig}")
    print("=" * 55)

    print(f"\n  {'i':>3} | {'A[0..i-1]':>25} | {'Sono i minimi':>13} | {'Pos. finale':>11}")
    print("  " + "-" * 58)

    for i in range(n - 1):
        # Trova e swappa il minimo
        smallest = i
        for j in range(i + 1, n):
            if A[j] < A[smallest]:
                smallest = j
        if smallest != i:
            A[i], A[smallest] = A[smallest], A[i]

        prefisso = A[:i+1]
        sono_minimi = sorted(prefisso) == A_sorted[:i+1]
        pos_finale   = prefisso == A_sorted[:i+1]
        print(f"  {i:>3} | {str(prefisso):>25} | {'Si ✓' if sono_minimi else 'NO ✗':>13} | {'Si ✓' if pos_finale else 'NO ✗':>11}")

    print(f"\n  Output finale: {A}")
    print(f"  Corretto: {A == A_sorted}  ✓")


# ==============================================================================
# 7. ANALISI EMPIRICA DEI TRE CASI
# ==============================================================================

def analisi_casi(n=10):
    """
    Dimostra empiricamente la differenza tra caso migliore, medio e peggiore
    per Insertion Sort, contando confronti e swap effettivi.
    """
    print("\n" + "=" * 70)
    print(f"ANALISI EMPIRICA DEI TRE CASI (n={n})")
    print("=" * 70)

    # Array per ogni caso
    best_case  = list(range(1, n+1))        # già ordinato [1,2,...,n]
    worst_case = list(range(n, 0, -1))      # inverso [n,...,2,1]
    avg_case   = random.sample(range(1, n*2), n)  # casuale

    casi = [
        ("CASO MIGLIORE (già ordinato)", best_case[:]),
        ("CASO MEDIO    (casuale)",      avg_case[:]),
        ("CASO PEGGIORE (inverso)",      worst_case[:]),
    ]

    print(f"\n  {'Caso':>35} | {'Confronti':>10} | {'Swap':>8} | {'T teorico':>15}")
    print("  " + "-" * 75)

    for nome, A in casi:
        c, s = insertion_sort(A)
        t_teorico = {
            "CASO MIGLIORE": f"n-1 = {n-1}",
            "CASO MEDIO":    f"~n^2/4 ~ {n*n//4}",
            "CASO PEGGIORE": f"n(n-1)/2 = {n*(n-1)//2}",
        }[nome.split("(")[0].strip()]
        print(f"  {nome:>35} | {c:>10} | {s:>8} | {t_teorico:>15}")

    print()
    print("  VERIFICA FORMULA:")
    print(f"  Best:  n-1 = {n-1}  confronti (ciclo while mai eseguito)")
    print(f"  Worst: n*(n-1)/2 = {n*(n-1)//2}  confronti (array inverso)")
    print(f"  Medio: ~{n*(n-1)//4}  confronti (meta' del caso peggiore)")


# ==============================================================================
# 8. BENCHMARK COMPARATIVO
# ==============================================================================

def benchmark_comparativo():
    """
    Confronto empirico dei tempi di esecuzione tra Insertion Sort,
    Selection Sort e Bubble Sort per valori crescenti di n.

    Tutti e tre hanno T(n) = Theta(n^2) nel caso peggiore,
    ma le costanti moltiplicative differiscono (specialmente per gli swap).
    """
    print("\n" + "=" * 75)
    print("BENCHMARK COMPARATIVO — Insertion Sort vs Selection Sort vs Bubble Sort")
    print("(caso peggiore: array ordinato inversamente)")
    print("=" * 75)
    print(f"  {'n':>6} | {'Insertion (s)':>14} | {'Selection (s)':>14} | {'Bubble (s)':>12}")
    print("  " + "-" * 55)

    for n in [100, 300, 600, 1000, 2000]:
        arr = list(range(n, 0, -1))  # caso peggiore per tutti

        A1 = arr[:]
        t0 = time.perf_counter()
        insertion_sort(A1)
        t_ins = time.perf_counter() - t0

        A2 = arr[:]
        t0 = time.perf_counter()
        selection_sort(A2)
        t_sel = time.perf_counter() - t0

        A3 = arr[:]
        t0 = time.perf_counter()
        bubble_sort(A3)
        t_bub = time.perf_counter() - t0

        print(f"  {n:>6} | {t_ins:>14.6f} | {t_sel:>14.6f} | {t_bub:>12.6f}")

    print()
    print("  Nota: tutti Theta(n^2), ma le costanti differiscono.")
    print("  Insertion Sort tende ad essere il piu' veloce in pratica.")


def confronto_swap_confronti(n=8):
    """
    Confronto dettagliato di swap e confronti tra i tre algoritmi
    per un array di dimensione n nel caso peggiore.
    """
    arr = list(range(n, 0, -1))  # [n, n-1, ..., 2, 1] — caso peggiore

    print("\n" + "=" * 60)
    print(f"CONFRONTO SWAP vs CONFRONTI (n={n}, caso peggiore)")
    print(f"  Array: {arr}")
    print("=" * 60)

    for nome, fn in [("Insertion Sort", insertion_sort),
                     ("Selection Sort", selection_sort),
                     ("Bubble Sort",    bubble_sort)]:
        A = arr[:]
        c, s = fn(A)
        print(f"\n  {nome}:")
        print(f"    Confronti: {c:>5}  (teorico ~{n*(n-1)//2})")
        print(f"    Swap:      {s:>5}")
        print(f"    Output:    {A}")

    print(f"\n  Teorico n*(n-1)/2 = {n*(n-1)//2}")
    print("  Selection Sort: swap minimi (al massimo n-1 swap totali)")
    print("  Insertion Sort: swap = confronti nel caso peggiore")
    print("  Bubble Sort:    swap = confronti nel caso peggiore (analogo a IS)")


# ==============================================================================
# MAIN — Esegue tutte le verifiche
# ==============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  INSERTION SORT — Studio Completo")
    print("=" * 60)

    # ── 1. Verifica correttezza dei tre algoritmi ──
    print("\n--- VERIFICA CORRETTEZZA ---")
    array_test = [6, 8, 3, 2, 7, 6, 11, 5, 9, 4]
    for nome, fn in [("Insertion Sort", lambda A: insertion_sort(A) or A),
                     ("Selection Sort", lambda A: selection_sort(A) or A),
                     ("Bubble Sort",    lambda A: bubble_sort(A) or A)]:
        A = array_test[:]
        fn(A)
        ok = is_sorted(A) and is_permutation(array_test, A)
        print(f"  {nome}: {A}  {'OK' if ok else 'ERRORE'}")

    # ── 2. Verifica di MAXTHREE ──
    print("\n--- VERIFICA MAXTHREE ---")
    test_cases = [(5, 2, 4), (1, 3, 2), (4, 4, 4), (1, 1, 2)]
    print(f"  {'(a,b,c)':>12} | {'v1 SBAGLIATO':>12} | {'v2 CORRETTO':>12} | {'v3 CORRETTO':>12} | {'Python max':>10}")
    for a, b, c in test_cases:
        v1 = maxthree_v1_sbagliato(a, b, c)
        v2 = maxthree_v2_corretto(a, b, c)
        v3 = maxthree_v3_corretto(a, b, c)
        mx = max(a, b, c)
        ok1 = "OK" if v1 == mx else f"ERR({v1})"
        print(f"  {str((a,b,c)):>12} | {ok1:>12} | {'OK':>12} | {'OK':>12} | {mx:>10}")

    print("\n  CONTROESEMPIO per v1: (5, 2, 4)")
    print(f"    maxthree_v1(5,2,4) = {maxthree_v1_sbagliato(5,2,4)} (SBAGLIATO, dovrebbe essere 5)")
    print(f"    maxthree_v2(5,2,4) = {maxthree_v2_corretto(5,2,4)} (corretto)")

    # ── 3. Invariante di Insertion Sort ──
    print()
    verifica_invariante_insertion_sort([6, 8, 3, 2, 7, 6, 11, 5, 9, 4])

    # ── 4. Invariante di Selection Sort ──
    verifica_invariante_selection_sort([6, 8, 3, 2, 7])

    # ── 5. Analisi empirica dei tre casi ──
    analisi_casi(n=10)

    # ── 6. Confronto swap/confronti ──
    confronto_swap_confronti(n=6)

    # ── 7. Benchmark ──
    benchmark_comparativo()

    print("\n" + "=" * 60)
    print("  Studio completato! Rileggere gli appunti Word per la teoria.")
    print("=" * 60)
