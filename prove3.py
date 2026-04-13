def count_vertical(A):

    counter = 0
    for i in range(0,len(A),2):
        for j in range(i +2, len(A),2):
            if A[i] ==A[j]:
                counter +=1

    return counter



def count_horizontal(A):
    for i in range(1,len(A),2):
        for j in range(i +2, len(A),2):
            if A[i] ==A[j]:
                counter +=1


def intersection(A):
    x_limits = {}  # Dizionario per i segmenti verticali
    y_limits = {}  # Dizionario per i segmenti orizzontali

    for i in range(0, len(A), 2):
        x, y = A[i], A[i+1] # Prendo un punto (es. X=5, Y=8)
    
    if x not in x_limits:
        # È la prima volta che vedo questa X!
        # Creo la pagina nel taccuino e scrivo [8, 8]
        x_limits[x] = [y, y] 
    else:
        # Avevo già visto questa X. Guardo cosa c'è scritto sul taccuino.
        # bounds[0] è il minimo attuale, bounds[1] è il massimo attuale
        
        if y < x_limits[x][0]: 
            x_limits[x][0] = y  # Ho trovato un punto più in basso! Aggiorno il minimo.
            
        if y > x_limits[x][1]: 
            x_limits[x][1] = y  # Ho trovato un punto più in alto! Aggiorno il massimo.

        if y not in y_limits:
            y_limits[y] = [x, x]

        else:
            if x < y_limits[y][0]: y_limits[y][0] = x
            if x > y_limits[y][1]: y_limits[y][1] = x

    # PASSO 2: Isolare solo i segmenti validi (cioè dove ci sono almeno 2 punti)
    # Un segmento è valido se il minimo è strettamente minore del massimo
    v_segments = []
    for x, bounds in x_limits.items():
        if bounds[0] < bounds[1]:  
            v_segments.append((x, bounds[0], bounds[1])) # (X, Y_min, Y_max)
            
    h_segments = []
    for y, bounds in y_limits.items():
        if bounds[0] < bounds[1]:
            h_segments.append((y, bounds[0], bounds[1])) # (Y, X_min, X_max)

    # Prendo un segmento verticale alla volta...
    for v_x, v_ymin, v_ymax in v_segments:
    
    # ...e lo confronto con tutti i segmenti orizzontali
        for h_y, h_xmin, h_xmax in h_segments:
        
        # Questa è la Condizione 1 e la Condizione 2 del widget!
            if (h_xmin <= v_x <= h_xmax) and (v_ymin <= h_y <= v_ymax):
                return True # Incrocio trovato!



