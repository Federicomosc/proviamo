"""
================================================================================
  ALGORITMI E STRUTTURE DATI — FILE DI STUDIO PYTHON
  Argomento: Quick Sort, Binary Heap e Heap Sort
  Professore: Antonio Carzaniga — Università della Svizzera italiana
  Data slides: 11 Marzo 2026
================================================================================

INDICE:
  1.  PARTITION      — Partizione in-place attorno al pivot    O(n)
  2.  QUICKSORT      — Ordinamento D&C in-place               O(n log n) medio
  3.  BinaryMaxHeap  — Struttura dati heap su array           Classe completa
      3a. PARENT, LEFT, RIGHT  — navigazione O(1)
      3b. MAX-HEAPIFY          — ripristino proprietà O(log n)
      3c. BUILD-MAX-HEAP       — costruzione da array         O(n)
      3d. HEAP-EXTRACT-MAX     — estrazione del massimo       O(log n)
      3e. HEAP-INSERT          — inserimento                  O(log n)
  4.  HEAP-SORT      — Ordinamento con heap in-place          O(n log n)
  5.  Verifica correttezza di tutti gli algoritmi
  6.  Analisi empirica dei casi (Best/Average/Worst) per Quick Sort
  7.  Benchmark finale: tutti e 5 gli algoritmi di ordinamento a confronto
================================================================================
"""

import random
import time
import sys
sys.setrecursionlimit(10000)


# ==============================================================================
# 1. PARTITION — Partizione In-Place — Theta(n)
# ==============================================================================

def partition(A, begin, end):
    """
    PARTITION — Riorganizza A[begin..end] in-place attorno al pivot v=A[end].

    Corrisponde ESATTAMENTE allo pseudocodice delle slide.

    IDEA CON DUE ZONE:
      Mantiene due zone all'interno di A[begin..end]:
        Zone SINISTRA [begin..q-1]: elementi <= v  (inizialmente vuota)
        Zone DESTRA   [q..i-1]:     elementi > v   (inizialmente vuota)

      Scansiona da sinistra con i. Quando trova A[i] <= v:
        - lo porta nella zona sinistra con uno swap A[i] <-> A[q]
        - espande la zona sinistra: q += 1

    INVARIANTE DEL CICLO:
      - begin <= k < q  =>  A[k] <= v   (zona sinistra)
      - q <= k < i      =>  A[k] > v    (zona destra)

    Alla fine (i = end, ovvero quando si processa il pivot stesso):
      - lo swap porta il pivot v dalla posizione end alla posizione q
      - A[begin..q-1] <= v,  A[q] = v,  A[q+1..end] > v

    COMPLESSITÀ: Theta(n) — un solo ciclo for su end-begin+1 elementi.
    IN-PLACE: usa O(1) spazio extra.

    Args:
        A:     lista (modificata in-place)
        begin: indice iniziale (incluso)
        end:   indice finale (incluso), A[end] = pivot

    Returns:
        q: indice finale del pivot dopo la partizione
    """
    q = begin          # q = confine zona sinistra (inizia vuota)
    v = A[end]         # pivot = ultimo elemento

    # Scansione sinistra->destra, incluso il pivot stesso (i=end)
    # Quando i raggiunge end, A[end]=v <= v, quindi viene swappato in A[q]:
    # questo porta il pivot nella sua posizione corretta.
    for i in range(begin, end + 1):
        if A[i] <= v:                  # A[i] appartiene alla zona sinistra?
            A[i], A[q] = A[q], A[i]   # porta A[i] in zona sinistra
            q += 1                     # espandi la zona sinistra

    # Dopo il ciclo, q punta alla prima posizione DOPO il pivot.
    # Il pivot si trova ora in A[q-1].
    return q - 1   # indice del pivot


def partition_verbose(A, begin, end):
    """Versione DIDATTICA di PARTITION con stampa di ogni passo."""
    q = begin
    v = A[end]
    print(f"  Pivot v = A[{end}] = {v}")
    print(f"  {'i':>3} | {'q':>3} | {'A[i]':>6} | {'Azione':>20} | Array")
    print("  " + "-" * 70)

    for i in range(begin, end + 1):
        azione = "—"
        if A[i] <= v:
            if i != q:
                azione = f"swap A[{i}]<->A[{q}]"
            else:
                azione = "no swap (i==q)"
            A[i], A[q] = A[q], A[i]
            q += 1
        else:
            azione = f"A[{i}]={A[i]}>{v}, skip"
        print(f"  {i:>3} | {q-1 if A[i]<=v else q:>3} | {A[i] if i>=q else v:>6} | {azione:>20} | {A[begin:end+1]}")

    return q - 1


# ==============================================================================
# 2. QUICKSORT — Ordinamento D&C In-Place
# ==============================================================================

def quicksort(A, begin=None, end=None):
    """
    QUICKSORT — Ordinamento Divide-and-Conquer. IN-PLACE.
    Corrisponde esattamente allo pseudocodice delle slide.

    STRUTTURA D&C:
    ┌──────────┬────────────────────────────────────────────────────────────────┐
    │ DIVIDE   │ PARTITION: riorganizza A attorno al pivot. O(n). IN-PLACE.     │
    │          │ Risultato: A[begin..q-1] <= A[q] <= A[q+1..end]               │
    ├──────────┼────────────────────────────────────────────────────────────────┤
    │ CONQUER  │ Richiama QUICKSORT ricorsivamente su A[begin..q-1] e A[q+1..end]│
    ├──────────┼────────────────────────────────────────────────────────────────┤
    │ COMBINE  │ NULLA! Il pivot A[q] e' gia' in posizione finale.              │
    │          │ Differenza chiave con MERGESORT (che ha COMBINE costosa).      │
    └──────────┴────────────────────────────────────────────────────────────────┘

    ANALISI DELLA COMPLESSITA':
    ┌──────────────┬──────────────────┬─────────────────────────────────────────┐
    │ Caso         │ T(n)             │ Quando si verifica                      │
    ├──────────────┼──────────────────┼─────────────────────────────────────────┤
    │ Peggiore     │ Theta(n^2)       │ Array gia' ordinato, pivot=A[end]       │
    │              │ T(n)=T(n-1)+O(n) │ q sempre in posizione estrema           │
    ├──────────────┼──────────────────┼─────────────────────────────────────────┤
    │ Migliore     │ Theta(n log n)   │ Pivot sempre a meta' esatta             │
    │              │ T(n)=2T(n/2)+O(n)│ Come MergeSort                          │
    ├──────────────┼──────────────────┼─────────────────────────────────────────┤
    │ Medio        │ Theta(n log n)   │ Pivot casuale, analisi probabilistica   │
    └──────────────┴──────────────────┴─────────────────────────────────────────┘

    NOTA: con pivot randomizzato il caso peggiore diventa estremamente raro.

    Args:
        A:     lista da ordinare (modificata IN-PLACE)
        begin: indice iniziale (default: 0)
        end:   indice finale (default: len(A)-1)
    """
    if begin is None: begin = 0
    if end is None:   end   = len(A) - 1

    # CASO BASE: 0 o 1 elementi => gia' ordinato, non fare nulla
    if begin < end:
        # DIVIDE: partiziona A attorno al pivot, ottieni indice pivot
        q = partition(A, begin, end)

        # CONQUER: ordina ricorsivamente le due parti
        quicksort(A, begin, q - 1)   # parte sinistra: elementi <= pivot
        quicksort(A, q + 1, end)     # parte destra:   elementi >  pivot
        # COMBINE: nulla! A[q] e' gia' in posizione corretta.


def quicksort_random_pivot(A, begin=None, end=None):
    """
    QUICKSORT con pivot CASUALE — elimina il caso peggiore in pratica.

    Prima di chiamare PARTITION, scambia un elemento casuale con A[end].
    Questo garantisce che il pivot sia scelto uniformemente a caso,
    rendendo il caso peggiore Theta(n^2) estremamente improbabile
    (probabilita' 1/n! per un array di n elementi).

    Complessita' attesa: Theta(n log n) per tutti gli input.
    """
    if begin is None: begin = 0
    if end is None:   end   = len(A) - 1

    if begin < end:
        # RANDOMIZZAZIONE: sceglie il pivot a caso e lo porta in A[end]
        pivot_idx = random.randint(begin, end)
        A[pivot_idx], A[end] = A[end], A[pivot_idx]

        q = partition(A, begin, end)
        quicksort_random_pivot(A, begin, q - 1)
        quicksort_random_pivot(A, q + 1, end)


# ==============================================================================
# 3. BINARY MAX-HEAP — Struttura Dati Completa
# ==============================================================================

class BinaryMaxHeap:
    """
    Binary Max-Heap — implementazione completa su array.

    RAPPRESENTAZIONE:
      Un heap di n elementi e' memorizzato in A[1..n] (1-based).
      Usiamo A[0] come posizione 'inutilizzata' per semplicita'.
      In Python implementiamo con lista 0-based (indice 0 = radice),
      adattando le formule di navigazione.

    PROPRIETA' MAX-HEAP:
      Per ogni nodo i > 0:  A[PARENT(i)] >= A[i]
      => A[0] (la radice) contiene SEMPRE il massimo.

    NAVIGAZIONE (0-based, radice=0):
      PARENT(i) = (i - 1) // 2
      LEFT(i)   = 2*i + 1
      RIGHT(i)  = 2*i + 2

    COMPLESSITA' DELLE OPERAZIONI:
      BUILD-MAX-HEAP:    O(n)
      MAX-HEAPIFY:       O(log n)
      HEAP-EXTRACT-MAX:  O(log n)
      HEAP-INSERT:       O(log n)
      MAX:               O(1)     (radice = massimo)
    """

    def __init__(self, A=None):
        """
        Inizializza l'heap. Se A e' fornito, chiama BUILD-MAX-HEAP.

        Args:
            A: lista opzionale di valori iniziali
        """
        self.data      = []   # array interno dell'heap
        self.heap_size = 0    # numero di elementi nell'heap (puo' essere < len(data))

        if A is not None:
            self.build_max_heap(A)

    # ── Navigazione ──────────────────────────────────────────────────────

    @staticmethod
    def parent(i):
        """Indice del padre di i. PARENT(i) = floor((i-1)/2) in 0-based."""
        return (i - 1) // 2

    @staticmethod
    def left(i):
        """Indice del figlio sinistro di i. LEFT(i) = 2*i+1 in 0-based."""
        return 2 * i + 1

    @staticmethod
    def right(i):
        """Indice del figlio destro di i. RIGHT(i) = 2*i+2 in 0-based."""
        return 2 * i + 2

    # ── Operazioni core ──────────────────────────────────────────────────

    def max_heapify(self, i):
        """
        MAX-HEAPIFY — Ripristina la proprietà max-heap nel sottoalbero radicato in i.

        PRECONDIZIONE: i sottoalberi sinistro e destro di i sono max-heap validi.
        POSTCONDIZIONE: il sottoalbero radicato in i è un max-heap valido.

        LOGICA:
          1. Trova il maggiore tra il nodo i e i suoi figli (left, right)
          2. Se i non e' il massimo, scambia con il figlio massimo
          3. Richiama ricorsivamente sul figlio (il valore 'scende' di un livello)

        Il valore 'scende' lungo l'albero finche' trova la posizione corretta.

        COMPLESSITA': O(log n) — altezza dell'albero = floor(log2(n))
        """
        l = self.left(i)
        r = self.right(i)

        # Trova il massimo tra nodo i e i suoi figli (se esistono nell'heap)
        largest = i
        if l < self.heap_size and self.data[l] > self.data[largest]:
            largest = l    # figlio sinistro e' il massimo locale

        if r < self.heap_size and self.data[r] > self.data[largest]:
            largest = r    # figlio destro e' il massimo locale

        # Se il massimo NON e' il nodo corrente: scambia e ricorri
        if largest != i:
            self.data[i], self.data[largest] = self.data[largest], self.data[i]
            self.max_heapify(largest)   # il valore piccolo scende di un livello

    def build_max_heap(self, A):
        """
        BUILD-MAX-HEAP — Costruisce un max-heap da un array arbitrario.

        STRATEGIA BOTTOM-UP:
          - Le foglie (indici n//2 .. n-1) sono gia' heap validi (un nodo solo).
          - Partiamo dai nodi interni (indici n//2-1 .. 0) e chiamiamo MAX-HEAPIFY.
          - Procedendo da destra a sinistra (bottom-up), garantiamo che quando
            chiamiamo MAX-HEAPIFY(i), i sottoalberi di i siano gia' validi.

        COMPLESSITA': O(n) — analisi precisa (non O(n log n) come si potrebbe pensare).
          I nodi agli ultimi livelli fanno poco lavoro (altezza 0 o 1),
          quelli vicini alla radice sono pochi. La somma pesata e' O(n).

        Args:
            A: lista di valori da cui costruire l'heap
        """
        self.data      = list(A)   # copia dell'array
        self.heap_size = len(A)

        # Chiama MAX-HEAPIFY solo sui nodi INTERNI (quelli con almeno un figlio).
        # Il primo nodo interno dall'alto e' parent dell'ultimo nodo = (n-1-1)//2 = n//2-1
        for i in range(self.heap_size // 2 - 1, -1, -1):  # da n//2-1 downto 0
            self.max_heapify(i)

    def heap_extract_max(self):
        """
        HEAP-EXTRACT-MAX — Estrae e ritorna il massimo dell'heap.

        PROCEDURA:
          1. Salva la radice (= massimo): A[0]
          2. Sposta l'ultimo elemento dell'heap in radice: A[0] = A[heap_size-1]
          3. Riduci heap_size di 1 (rimuove l'ultimo elemento)
          4. Chiama MAX-HEAPIFY(0) per ripristinare la proprieta' max-heap

        Dopo il passo 2, i sottoalberi della radice sono ancora max-heap validi
        (non li abbiamo toccati), ma la nuova radice potrebbe violare la proprieta'.
        MAX-HEAPIFY la ripristina.

        COMPLESSITA': O(log n) — una chiamata a MAX-HEAPIFY.

        Returns:
            Il valore massimo rimosso dall'heap.

        Raises:
            IndexError se l'heap e' vuoto.
        """
        if self.heap_size == 0:
            raise IndexError("Heap vuoto: impossibile estrarre il massimo")

        max_val = self.data[0]                          # salva il massimo (radice)
        self.data[0] = self.data[self.heap_size - 1]   # porta l'ultimo in radice
        self.heap_size -= 1                             # riduce la dimensione
        self.max_heapify(0)                             # ripristina max-heap

        return max_val

    def heap_insert(self, key):
        """
        HEAP-INSERT — Inserisce key nell'heap.

        PROCEDURA:
          1. Aggiungi key in fondo all'heap (come foglia)
          2. Fai 'salire' key verso la radice finche' la proprieta' e' rispettata
             (operazione inversa di MAX-HEAPIFY: bubble-up invece di bubble-down)

        COMPLESSITA': O(log n) — key risale al massimo log2(n) livelli.

        Args:
            key: valore da inserire
        """
        if self.heap_size < len(self.data):
            self.data[self.heap_size] = key
        else:
            self.data.append(key)   # espande l'array se necessario
        self.heap_size += 1

        # BUBBLE-UP: fai salire key verso la radice
        i = self.heap_size - 1
        while i > 0 and self.data[self.parent(i)] < self.data[i]:
            # Il padre e' minore di key: viola la proprieta' => swap
            p = self.parent(i)
            self.data[i], self.data[p] = self.data[p], self.data[i]
            i = p   # sali di un livello

    def get_max(self):
        """Ritorna il massimo senza estrarlo. O(1) — e' sempre la radice."""
        if self.heap_size == 0:
            raise IndexError("Heap vuoto")
        return self.data[0]

    def is_valid_max_heap(self):
        """
        Verifica che la proprieta' max-heap sia rispettata per tutti i nodi.
        Usata per testing. O(n).
        """
        for i in range(1, self.heap_size):
            if self.data[self.parent(i)] < self.data[i]:
                return False
        return True

    def __repr__(self):
        return f"BinaryMaxHeap({self.data[:self.heap_size]})"

    def to_tree_string(self):
        """Visualizzazione dell'heap come albero (livelli)."""
        if self.heap_size == 0:
            return "(heap vuoto)"
        lines = []
        level_start = 0
        level_size  = 1
        while level_start < self.heap_size:
            level_end = min(level_start + level_size, self.heap_size)
            lines.append("  " + "  ".join(str(self.data[i]) for i in range(level_start, level_end)))
            level_start = level_end
            level_size  *= 2
        return "\n".join(lines)


# ==============================================================================
# 4. HEAP SORT — O(n log n) In-Place
# ==============================================================================

def heap_sort(A):
    """
    HEAP-SORT — Ordinamento in-place basato su max-heap.
    Corrisponde esattamente allo pseudocodice delle slide.

    IDEA:
      1. Costruisci un max-heap da A: O(n). La radice A[0] = massimo.
      2. Per i da n-1 downto 1:
         a. Scambia A[0] (massimo) con A[i] (mette il max in posizione finale)
         b. Riduci heap_size di 1 (A[i] non fa piu' parte dell'heap)
         c. Chiama MAX-HEAPIFY(A, 0) per ripristinare il max-heap ridotto

    ANALOGIA con Selection Sort:
      - Selection Sort: trova il max con O(n) confronti ogni volta => O(n^2) totale
      - Heap Sort:      trova il max con O(1) (e' sempre in A[0]), ripristina in O(log n) => O(n log n) totale

    COMPLESSITA':
      - BUILD-MAX-HEAP: O(n)
      - Loop: n iterazioni * MAX-HEAPIFY O(log n) = O(n log n)
      - Totale: O(n) + O(n log n) = O(n log n)
      - TUTTI i casi: Theta(n log n) (non dipende dall'ordine dell'input!)

    IN-PLACE: usa O(1) spazio extra. I valori estratti vengono posizionati
    nella parte 'morta' dell'array (A[heap_size..n-1]).

    Args:
        A: lista da ordinare (modificata IN-PLACE)
    """
    n = len(A)

    # PASSO 1: Costruisci il max-heap da A
    # (stessa logica di BUILD-MAX-HEAP, ma direttamente su A)
    heap_size = n
    for i in range(n // 2 - 1, -1, -1):
        _max_heapify_inplace(A, i, heap_size)

    # PASSO 2: Estrai il massimo n-1 volte
    for i in range(n - 1, 0, -1):
        # A[0] = massimo corrente: portalo in posizione finale
        A[0], A[i] = A[i], A[0]

        # L'elemento A[i] e' ora nella posizione corretta e definitiva.
        # Riduci l'heap (A[i] non e' piu' parte dell'heap)
        heap_size -= 1

        # Ripristina la proprieta' max-heap sulla nuova radice A[0]
        _max_heapify_inplace(A, 0, heap_size)


def _max_heapify_inplace(A, i, heap_size):
    """
    Versione interna di MAX-HEAPIFY per operare direttamente su un array.
    Usata da heap_sort() per evitare overhead della classe BinaryMaxHeap.

    Identica alla logica di BinaryMaxHeap.max_heapify(), ma prende
    heap_size come parametro (per operare su sottoinsiemi di A).
    """
    l = 2 * i + 1   # left child  (0-based)
    r = 2 * i + 2   # right child (0-based)
    largest = i

    if l < heap_size and A[l] > A[largest]:
        largest = l
    if r < heap_size and A[r] > A[largest]:
        largest = r

    if largest != i:
        A[i], A[largest] = A[largest], A[i]
        _max_heapify_inplace(A, largest, heap_size)


# ==============================================================================
# 5. VERIFICHE DI CORRETTEZZA
# ==============================================================================

def verifica_partition():
    """Verifica PARTITION con traccia dettagliata."""
    print("=" * 65)
    print("VERIFICA PARTITION")
    print("=" * 65)

    A = [36, 11, 5, 21, 1, 13, 2, 20, 5, 4, 8]
    print(f"\n  Input:  {A}  (pivot = A[{len(A)-1}] = {A[-1]})")
    A_copy = A[:]
    q = partition_verbose(A_copy, 0, len(A_copy)-1)
    print(f"\n  Output: {A_copy}")
    print(f"  Pivot posizionato in A[{q}] = {A_copy[q]}")
    print(f"  Zona sinistra A[0..{q-1}]  = {A_copy[:q]}  (tutti <= {A[-1]}?  {all(x<=A[-1] for x in A_copy[:q])})")
    print(f"  Zona destra   A[{q+1}..{len(A)-1}] = {A_copy[q+1:]}  (tutti > {A[-1]}?  {all(x>A[-1] for x in A_copy[q+1:])})")
    print()


def verifica_quicksort():
    """Verifica correttezza di QuickSort su vari casi."""
    print("=" * 65)
    print("VERIFICA QUICKSORT")
    print("=" * 65)

    test_cases = [
        ([6, 8, 3, 2, 7, 6, 11, 5, 9, 4],  "array generico"),
        ([1],                                "singolo elemento"),
        ([2, 1],                             "due elementi"),
        (list(range(10, 0, -1)),             "array inverso (caso peggiore deterministico)"),
        (list(range(1, 11)),                 "gia' ordinato (caso peggiore deterministico)"),
        ([5]*8,                              "tutti uguali"),
    ]

    for arr, desc in test_cases:
        A = arr[:]
        quicksort(A)
        ok = A == sorted(arr)
        print(f"  [{desc}]")
        print(f"    Input:  {arr}")
        print(f"    Output: {A}  {'OK' if ok else 'ERRORE'}")
    print()


def verifica_heap():
    """Verifica completa della struttura BinaryMaxHeap."""
    print("=" * 65)
    print("VERIFICA BINARY MAX-HEAP")
    print("=" * 65)

    # Test BUILD-MAX-HEAP
    A = [4, 1, 3, 2, 16, 9, 10, 14, 8, 7]
    print(f"\n  BUILD-MAX-HEAP da: {A}")
    h = BinaryMaxHeap(A)
    print(f"  Heap risultante:   {h.data[:h.heap_size]}")
    print(f"  Proprieta' valida: {h.is_valid_max_heap()}")
    print(f"  Massimo (radice):  {h.get_max()}")
    print(f"\n  Struttura ad albero:")
    print(h.to_tree_string())

    # Test HEAP-EXTRACT-MAX (simula Heap Sort)
    print(f"\n  Estrazione successiva del massimo:")
    while h.heap_size > 0:
        m = h.heap_extract_max()
        print(f"    Estratto: {m:>3}  |  Heap rimanente: {h.data[:h.heap_size]}")
        assert h.is_valid_max_heap(), "ERRORE: proprieta' violata dopo extract!"

    # Test HEAP-INSERT
    print(f"\n  Test HEAP-INSERT:")
    h2 = BinaryMaxHeap()
    for val in [5, 3, 8, 1, 9, 2, 7]:
        h2.heap_insert(val)
        print(f"    Insert {val}: heap = {h2.data[:h2.heap_size]}  (max={h2.get_max()}, valido={h2.is_valid_max_heap()})")
    print()


def verifica_heapsort():
    """Verifica correttezza di Heap Sort."""
    print("=" * 65)
    print("VERIFICA HEAP SORT")
    print("=" * 65)

    test_cases = [
        ([6, 8, 3, 2, 7, 6, 11, 5, 9, 4], "array generico"),
        ([1],                               "singolo elemento"),
        (list(range(10, 0, -1)),            "array inverso"),
        (list(range(1, 11)),                "gia' ordinato"),
        ([5]*6,                             "tutti uguali"),
    ]

    for arr, desc in test_cases:
        A = arr[:]
        heap_sort(A)
        ok = A == sorted(arr)
        print(f"  [{desc}]  {arr}  =>  {A}  {'OK' if ok else 'ERRORE'}")
    print()


# ==============================================================================
# 6. ANALISI EMPIRICA: TRE CASI DI QUICKSORT
# ==============================================================================

def analisi_quicksort(n=15):
    """
    Dimostra empiricamente i tre casi di Quick Sort contando le chiamate a PARTITION.
    """
    call_count = [0]   # lista per poter modificare dentro closure

    def partition_counted(A, begin, end):
        call_count[0] += 1
        return partition(A, begin, end)

    def qs_counted(A, begin, end):
        if begin < end:
            q = partition_counted(A, begin, end)
            qs_counted(A, begin, q - 1)
            qs_counted(A, q + 1, end)

    print("=" * 65)
    print(f"ANALISI EMPIRICA DEI CASI — QUICKSORT (n={n})")
    print("=" * 65)
    print(f"  {'Caso':>35} | {'Chiamate PARTITION':>18} | {'Teorico':>12}")
    print("  " + "-" * 72)

    casi = [
        ("MIGLIORE (pivot sempre centrale)", sorted(range(n))),  # ottimale con partition
        ("MEDIO (array casuale)",            random.sample(range(n), n)),
        ("PEGGIORE (gia' ordinato)",         list(range(n))),
        ("PEGGIORE (ordinato inverso)",      list(range(n, 0, -1))),
    ]

    for nome, arr in casi:
        call_count[0] = 0
        A = arr[:]
        qs_counted(A, 0, len(A)-1)
        teorico = {
            "MIGLIORE": f"~n log n = {int(n * __import__('math').log2(n))}",
            "MEDIO":    f"~n log n = {int(n * __import__('math').log2(n))}",
            "PEGGIORE": f"n*(n-1)/2 = {n*(n-1)//2}",
        }[nome.split(" ")[0]]
        print(f"  {nome:>35} | {call_count[0]:>18} | {teorico:>12}")
    print()


# ==============================================================================
# 7. BENCHMARK FINALE: TUTTI E 5 GLI ALGORITMI
# ==============================================================================

def benchmark_tutti():
    """
    Confronto empirico dei tempi di esecuzione di tutti gli algoritmi
    su array casuali (caso medio per Quick Sort, tutti gli altri invarianti).
    """
    # Importiamo gli algoritmi dalle lezioni precedenti (reimplementati qui per comodità)
    def insertion_sort(A):
        for i in range(1, len(A)):
            j = i
            while j > 0 and A[j-1] > A[j]:
                A[j], A[j-1] = A[j-1], A[j]
                j -= 1

    def mergesort(A):
        if len(A) <= 1: return A[:]
        m = len(A) // 2
        L = mergesort(A[:m])
        R = mergesort(A[m:])
        result, i, j = [], 0, 0
        while i < len(L) and j < len(R):
            if L[i] <= R[j]: result.append(L[i]); i += 1
            else:             result.append(R[j]); j += 1
        return result + L[i:] + R[j:]

    print("=" * 78)
    print("BENCHMARK FINALE — Tutti e 5 gli Algoritmi di Ordinamento")
    print("(array casuale = caso medio per tutti)")
    print("=" * 78)
    print(f"  {'n':>6} | {'Insertion':>10} | {'Merge':>10} | {'Quick':>10} | {'Quick(r)':>10} | {'Heap':>10}")
    print("  " + "-" * 66)

    for n in [100, 500, 1000, 3000]:
        arr = random.sample(range(n * 3), n)

        results = {}
        for nome, fn in [
            ("Insertion", lambda A: insertion_sort(A)),
            ("Merge",     lambda A: None),   # restituisce nuovo array
            ("Quick",     lambda A: quicksort(A)),
            ("Quick(r)",  lambda A: quicksort_random_pivot(A)),
            ("Heap",      lambda A: heap_sort(A)),
        ]:
            if nome == "Merge":
                A = arr[:]
                t0 = time.perf_counter()
                sorted_A = mergesort(A)
                results[nome] = time.perf_counter() - t0
            else:
                A = arr[:]
                t0 = time.perf_counter()
                fn(A)
                results[nome] = time.perf_counter() - t0

        print(f"  {n:>6} | {results['Insertion']:>10.5f} | {results['Merge']:>10.5f} | "
              f"{results['Quick']:>10.5f} | {results['Quick(r)']:>10.5f} | {results['Heap']:>10.5f}")

    print()
    print("  Legenda: Quick(r) = QuickSort con pivot randomizzato")
    print("  Nota: MergeSort NON e' in-place (usa array ausiliari)")
    print("  Nota: Heap Sort e' SEMPRE O(n log n), Quick Sort e' O(n^2) nel peggiore")


# ==============================================================================
# MAIN
# ==============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 65)
    print("  QUICK SORT, BINARY HEAP E HEAP SORT — Studio Completo")
    print("=" * 65 + "\n")

    verifica_partition()
    verifica_quicksort()
    verifica_heap()
    verifica_heapsort()
    analisi_quicksort(n=15)
    benchmark_tutti()

    print("=" * 65)
    print("  Studio completato! Rileggere gli appunti Word per la teoria.")
    print("=" * 65)
