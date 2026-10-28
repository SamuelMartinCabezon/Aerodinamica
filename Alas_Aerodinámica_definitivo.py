#MÃ©todo de mallas de torbellinos

import numpy as np
from numpy import sin, cos, tan, radians
import matplotlib.pyplot as plt
import pandas as pd
from openpyxl import load_workbook

#%% representacion 3D

def ala_3D (f, x_f, t, puntos, matriz_x, matriz_y_der, N_x, N_y, torsion, b_env):
    
    x_ba = matriz_x[::N_x, 0]
    x_bs = matriz_x[N_x - 1::N_x, -1]
    y_j = matriz_y_der[::N_x, 0]
    cuerda_j = x_bs - x_ba
    torsion_j = np.zeros ((N_y + 1))
    for j in range(0, N_y + 1):
        torsion_j[j] = ((np.pi * torsion *  matriz_y_der[j * N_x, 0]) / (90 * b_env))
    
    puntos_x = np.linspace(0, 1, puntos); z_linea_media = np.zeros ((puntos)); z_t = np.zeros((puntos))
    for i, x in enumerate(puntos_x):
        if x < x_f:
            z_linea_media[i] = (f / (x_f ** 2)) * (2 * x_f * x - x ** 2)
        else:
            z_linea_media[i] = (f / ((1 - x_f) ** 2)) * ((1 - 2 * x_f) + 2 * x_f * x - x ** 2)
    
        z_t [i] = (+ 5 * (t) * (0.2969 * x ** 0.5 - 0.126 * x - 0.3516 * x ** 2 + 0.2843 * x ** 3 - 0.1015 * x ** 4))
    z_extrados = z_linea_media + z_t
    z_intrados = z_linea_media - z_t
    
    
    x_perfil_j = np.zeros ((N_y + 1, puntos)); y_perfil_j = np.zeros((N_y + 1, puntos)); z_extrados_j = np.zeros ((N_y + 1, puntos)); z_intrados_j = np.zeros ((N_y + 1, puntos))
    x_ext_perfil_j = np.zeros ((N_y + 1, puntos)); x_int_perfil_j = np.zeros ((N_y + 1, puntos)); y_perfil_j = np.zeros((N_y + 1, puntos)); z_ext_perfil_j = np.zeros ((N_y + 1, puntos)); z_int_perfil_j = np.zeros ((N_y + 1, puntos))
    for j in range (0, N_y + 1):
        x_perfil_j [j,:] = np.linspace (x_ba[j], x_bs[j], puntos)
        y_perfil_j[j,:] = y_j [j]
        z_extrados_j[j,:] = z_extrados * cuerda_j[j]
        z_intrados_j[j,:] = z_intrados * cuerda_j[j]
        for punto in range (0, puntos):
            x_ext_perfil_j[j, punto] = x_perfil_j[j, 0] + (cuerda_j[j] * (1 - cos(torsion_j[j])) + (x_perfil_j[j, punto] - x_perfil_j[j, 0]) * cos(torsion_j[j])) + z_extrados_j[j, punto] * sin(torsion_j[j])
            x_int_perfil_j[j, punto] = x_perfil_j[j, 0] + (cuerda_j[j] * (1 - cos(torsion_j[j])) + (x_perfil_j[j, punto] - x_perfil_j[j, 0]) * cos(torsion_j[j])) + z_intrados_j[j, punto] * sin(torsion_j[j])    
            z_ext_perfil_j[j, punto] = (cuerda_j[j] - x_perfil_j[j, punto]) * sin(torsion_j[j]) + z_extrados_j[j, punto] * cos(torsion_j[j])
            z_int_perfil_j[j, punto] = (cuerda_j[j] - x_perfil_j[j, punto]) * sin(torsion_j[j]) + z_intrados_j[j, punto] * cos(torsion_j[j])
    y_perfil_izq_j = - y_perfil_j
    
    fig1 = plt.figure(1)
    ax = fig1.add_subplot(111, projection='3d')
    
    for i in range(N_y + 1):
        ax.plot(x_ext_perfil_j[i],     y_perfil_j[i],     z_ext_perfil_j[i], c='red')
        ax.plot(x_int_perfil_j[i],     y_perfil_j[i],     z_int_perfil_j[i], c='blue')
        ax.plot(x_ext_perfil_j[i],     y_perfil_izq_j[i], z_ext_perfil_j[i], c='red')
        ax.plot(x_int_perfil_j[i],     y_perfil_izq_j[i], z_int_perfil_j[i], c='blue')
    

    for j in range(puntos):
        for i in range(N_y):
            ax.plot(
                [x_ext_perfil_j[i][j], x_ext_perfil_j[i+1][j]],
                [y_perfil_j[i][j],     y_perfil_j[i+1][j]],
                [z_ext_perfil_j[i][j], z_ext_perfil_j[i+1][j]],
                c='red'
            )
            ax.plot(
                [x_int_perfil_j[i][j], x_int_perfil_j[i+1][j]],
                [y_perfil_j[i][j],     y_perfil_j[i+1][j]],
                [z_int_perfil_j[i][j], z_int_perfil_j[i+1][j]],
                c='blue'
            )
    
            ax.plot(
                [x_ext_perfil_j[i][j], x_ext_perfil_j[i+1][j]],
                [y_perfil_izq_j[i][j], y_perfil_izq_j[i+1][j]],
                [z_ext_perfil_j[i][j], z_ext_perfil_j[i+1][j]],
                c='red'
            )
            ax.plot(
                [x_int_perfil_j[i][j], x_int_perfil_j[i+1][j]],
                [y_perfil_izq_j[i][j], y_perfil_izq_j[i+1][j]],
                [z_int_perfil_j[i][j], z_int_perfil_j[i+1][j]],
                c='blue'
            )
    
    x_vals = np.concatenate([x_ext_perfil_j.flatten(), x_int_perfil_j.flatten()])
    y_vals = np.concatenate([y_perfil_j.flatten(), y_perfil_izq_j.flatten()])
    z_vals = np.concatenate([z_ext_perfil_j.flatten(), z_int_perfil_j.flatten()])
    
    max_range = np.array([
        x_vals.max() - x_vals.min(),
        y_vals.max() - y_vals.min(),
        z_vals.max() - z_vals.min()
    ]).max() / 2.0
    
    mid_x = (x_vals.max() + x_vals.min()) * 0.5
    mid_y = (y_vals.max() + y_vals.min()) * 0.5
    mid_z = (z_vals.max() + z_vals.min()) * 0.5
    
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)
    
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    
    # ax.set_xticks([])
    # ax.set_yticks([])
    # ax.set_zticks([])
    
    # ax.set_xticklabels([])
    # ax.set_yticklabels([])
    # ax.set_zticklabels([])
    
    # fig1.savefig('C:\Aerodinámica\Alas\Figuras/3D101p.svg')
    
    return

#%% derivada

def pendiente_3c4 (f, x_f, N_x, N_y):
    
    puntos_x = np.linspace(0, 1, N_x + 1); puntos_y = np.zeros ((N_x + 1)); pendiente_panel = np.zeros ((N_x))
    
    for i, x in enumerate(puntos_x):
        if x < x_f:
            puntos_y[i] = (f / (x_f ** 2)) * (2 * x_f * x - x ** 2)
        else:
            puntos_y[i] = (f / ((1 - x_f) ** 2)) * ((1 - 2 * x_f) + 2 * x_f * x - x ** 2)
    for i in range (0, N_x):
        pendiente_panel [i] = (puntos_y[i + 1] - puntos_y[i]) / (puntos_x[i + 1] - puntos_x[i])
    
    pendiente_todos_paneles = np.tile(pendiente_panel, N_y)
    
    return pendiente_todos_paneles


#%% Panelizacion

def panelizacion (estrechamiento, alargamiento, flecha, torsion, superficie_alar, N_x, N_y, completa, angulos):
    
    flecha_rad = np.radians(flecha)
    
    b_env = (alargamiento * superficie_alar) ** (0.5)
    # print (b_env)
    c_gm = superficie_alar / b_env
    # print (c_gm)
    c_r = (2 / (estrechamiento + 1)) * c_gm
    # print (c_r)
    c_t = c_r * estrechamiento
    # print (c_t)
    c_am = (2 * c_r * (1 + estrechamiento + estrechamiento ** 2)) / (3 * (1 + estrechamiento))
    # print (c_am)
    y_c_aw = (b_env / 2) * ((1 + 2 * estrechamiento) / (3 * (1 + estrechamiento)))
    # print (y_c_aw)
    x_c_aw = 0.25 * c_r + tan(flecha_rad) * y_c_aw
    # print (x_c_aw)
    
    
    paneles = np.zeros((N_x * N_y)); paneles_y = np.zeros ((N_y)); todos_paneles = np.zeros((2 * N_x * N_y)); todos_paneles_y = np.zeros ((2 * N_y))
    for j in range (0, N_y):
        paneles_y[j] = j + 1
        for i in range (0, N_x):
            paneles[j * N_x + i] = j * N_x + i + 1
    for j in range (0, 2 * N_y):
        todos_paneles_y[j] = j + 1
        for i in range (0, N_x):
            todos_paneles[j * N_x + i] = j * N_x + i + 1
    
    
    cr_0 = c_r / N_x
    matriz_x = np.zeros((N_x * (N_y +1), 5)); matriz_y_der = np.zeros((N_x * (N_y +1), 5)); cr_panel = np.zeros(N_y + 1)
    for j in range (0, N_y + 1):
        cr_j = (1 + (j * (estrechamiento - 1)) / (N_y)) * cr_0
        cr_panel[j] = cr_j
        # print (cr_panel)
        diagonal_j = (j * b_env) / (2 * N_y * cos(flecha_rad))
        # print (diagonal_j)
        for i in range (0, N_x):
            if j == 0:
                x_c4_perfil_ij = cr_j * (0.25 + i)
            else:
                x_c4_perfil_ij = (c_r * 0.25 *(1 - ((1 - 1 / N_x) * (1 + (j * (estrechamiento - 1)) / (N_y))))) + (cr_j * i) + ((diagonal_j ** 2 - ((b_env * j) / (2 * N_y)) ** 2)  ** (0.5))
            for k in range (0, 5):
                matriz_x[i + j * N_x, k] = x_c4_perfil_ij + (k - 1) * (cr_j / 4)
                matriz_y_der[i + j * N_x, k] = (b_env * j) / (2 * N_y)
    matriz_y_izq = matriz_y_der.copy(); matriz_y_izq = - matriz_y_izq
    # print (matriz_x)
    # print (matriz_y_der)
    # print (matriz_y_izq)
    
    
    ala_3D (0.04, 0.3, 0.12, 6, matriz_x, matriz_y_der, N_x, N_y, torsion, b_env)
    
    
    matriz_x_control = np.zeros ((2, N_x * N_y))
    matriz_y_control = np.zeros ((2, N_x * N_y))
    matriz_x_1 = np.zeros ((2, N_x * N_y))
    matriz_y_1 = np.zeros ((2, N_x * N_y))
    matriz_x_2 = np.zeros ((2, N_x * N_y))
    matriz_y_2 = np.zeros ((2, N_x * N_y))
    matriz_variables_der = np.zeros ((N_x * N_y, 11)); matriz_variables_izq = np.zeros ((N_x * N_y, 11)); matriz_variables_suma = np.zeros ((N_x * N_y, 11))

    fig2 = plt.figure(2, figsize=(10, 6))
    

    lista_matrices_y = [matriz_y_der, matriz_y_izq]
        
    contador_lados = - 1    
    for lado in lista_matrices_y:
        contador_lados += 1
        x_primero = matriz_x[::N_x, 0]
        y_primero = lado[::N_x, 0]
        x_ultimos = matriz_x[::1, -1]
        y_ultimos = lado[::1, -1]
        borde_ataque = np.array(list(zip(x_primero, y_primero)))
        x_ba, y_ba = borde_ataque[:, 0], borde_ataque[:, 1]
        
        vectores_c = np.array([[i * (N_y + 1) + j for j in range(N_y + 1)] for i in range(N_x)], dtype = object)
        for i in range(0, len(vectores_c)):
            for j in range(0, N_y + 1):
                vectores_c[i, j] = (x_ultimos[i + j * N_x], y_ultimos[i + j * N_x])
        
        for i, fila in enumerate(vectores_c):
            x_vals = [tupla[0] for tupla in fila]
            y_vals = [tupla[1] for tupla in fila]
            plt.plot(y_vals, x_vals, linestyle='-', color='black')
            # plt.plot(x_vals, y_vals, marker='o', linestyle='', color='green', markersize=3)
        plt.plot(y_ba, x_ba, linestyle='-', color='green', label = "Borde de ataque")
        # plt.plot(x_ba, y_ba, marker='o', linestyle='', color='blue', markersize=3)
        
        perfil_j = np.array([[i * (N_x + 1) + j for j in range(N_x + 1)] for i in range(N_y + 1)], dtype = object)   
        for i in range (0, len(perfil_j)):
            perfil_j[i, 0] = (x_primero[i], y_primero[i])
            for j in range (0, N_x):
                perfil_j[i, j + 1] = (x_ultimos[i * N_x + j], y_ultimos[i * N_x + j])

        for i, fila in enumerate(perfil_j):
            x_vals = [tupla[0] for tupla in fila]
            y_vals = [tupla[1] for tupla in fila]
            plt.plot(y_vals, x_vals, linestyle='-', color='black')
            # plt.plot(x_vals, y_vals, marker='o', linestyle='', color='blue', markersize=3)
        
        x_puntos_control = np.zeros((N_x * N_y)); y_puntos_control = np.zeros((N_x * N_y)); puntos_control = np.zeros(N_x * N_y, dtype = object)
        for i  in range (0, len(x_puntos_control)):
            x_puntos_control[i] = (matriz_x[i, 3] + matriz_x[i + N_x, 3]) / 2
            y_puntos_control[i] = (lado[i, 3] + lado[i + N_x, 3]) / 2
            puntos_control[i] = (x_puntos_control[i], y_puntos_control[i])
            matriz_x_control[contador_lados, i] = x_puntos_control[i]
            matriz_y_control[contador_lados, i] = y_puntos_control[i]
        plt.scatter(y_puntos_control, x_puntos_control, color='red', marker='o', s=9, label = "Punto de control")
        # print (x_puntos_control) 
        # print (y_puntos_control)
        
        esquina_1 = np.zeros(N_x * N_y, dtype = object); esquina_2 = np.zeros(N_x * N_y, dtype = object)
        x_1 = np.zeros(N_x * N_y, dtype = object); y_1 = np.zeros(N_x * N_y, dtype=object); x_2 = np.zeros(N_x * N_y, dtype=object); y_2 = np.zeros(N_x * N_y, dtype=object)
        for j in range (0, N_y):
            for i in range (0, N_x):
                if contador_lados == 0:
                    x_1[j * N_x + i] = matriz_x[j * N_x + i, 1]
                    y_1[j * N_x + i] = lado[j * N_x + i, 1]
                    x_2[j * N_x + i] = matriz_x[j * N_x + i + N_x, 1]
                    y_2[j * N_x + i] = lado[j * N_x + i + N_x, 1]
                    esquina_1[j * N_x + i] = (x_1[j * N_x + i], y_1[j * N_x + i])
                    esquina_2[j * N_x + i] = (x_2[j * N_x + i], y_2[j * N_x + i])
                    matriz_x_1 [contador_lados, j * N_x + i] = x_1[j * N_x + i]
                    matriz_y_1 [contador_lados, j * N_x + i] = y_1[j * N_x + i]
                    matriz_x_2 [contador_lados, j * N_x + i] = x_2[j * N_x + i]
                    matriz_y_2 [contador_lados, j * N_x + i] = y_2[j * N_x + i]
                else:
                    x_1[j * N_x + i] = matriz_x[j * N_x + i + N_x, 1]
                    y_1[j * N_x + i] = lado[j * N_x + i + N_x, 1]
                    x_2[j * N_x + i] = matriz_x[j * N_x + i, 1]
                    y_2[j * N_x + i] = lado[j * N_x + i, 1]
                    esquina_1[j * N_x + i] = (x_1[j * N_x + i], y_1[j * N_x + i])
                    esquina_2[j * N_x + i] = (x_2[j * N_x + i], y_2[j * N_x + i])
                    matriz_x_1 [contador_lados, j * N_x + i] = x_1[j * N_x + i]
                    matriz_y_1 [contador_lados, j * N_x + i] = y_1[j * N_x + i]
                    matriz_x_2 [contador_lados, j * N_x + i] = x_2[j * N_x + i]
                    matriz_y_2 [contador_lados, j * N_x + i] = y_2[j * N_x + i]
        # print (esquina_1)
        # print (esquina_2)
    
        plt.scatter(y_1, x_1, color= "#0072B2", marker='o', s=25, label = "Esquina 1 torbellino")
        plt.scatter(y_2, x_2, color='#E69F00', marker='o', s=9, label = "Esquina 2 torbellino")
    
    plt.title("Panelización con Nx =" + str(N_x) + " y Ny =" + str(N_y)); plt.xlabel("Eje y cuerpo"); plt.ylabel("Eje x cuerpo"); plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    handles, labels = plt.gca().get_legend_handles_labels()
    unique = dict()
    for h, l in zip(handles, labels):
        if l not in unique:
            unique[l] = h
    plt.legend(unique.values(), unique.keys(), loc='lower center')
    plt.xlim(-2.5, 2.5); plt.gca().invert_yaxis(); plt.xticks(np.arange(-2.5, 3, 0.5)); plt.grid(True)
    plt.tight_layout()
    
    lados = [0 , 1]
    matriz_a_der = np.zeros ((N_x * N_y, N_x * N_y)); matriz_a_izq = np.zeros ((N_x * N_y, N_x * N_y)); matriz_a_suma = np.zeros ((N_x * N_y, N_x * N_y))
    matriz_b_der = np.zeros ((N_x * N_y, N_x * N_y)); matriz_b_izq = np.zeros ((N_x * N_y, N_x * N_y)); matriz_b_suma = np.zeros ((N_x * N_y, N_x * N_y))
    matriz_c_der = np.zeros ((N_x * N_y, N_x * N_y)); matriz_c_izq = np.zeros ((N_x * N_y, N_x * N_y)); matriz_c_suma = np.zeros ((N_x * N_y, N_x * N_y))
    matriz_d_der = np.zeros ((N_x * N_y, N_x * N_y)); matriz_d_izq = np.zeros ((N_x * N_y, N_x * N_y)); matriz_d_suma = np.zeros ((N_x * N_y, N_x * N_y))
    matriz_e_der = np.zeros ((N_x * N_y, N_x * N_y)); matriz_e_izq = np.zeros ((N_x * N_y, N_x * N_y)); matriz_e_suma = np.zeros ((N_x * N_y, N_x * N_y))
    matriz_f_der = np.zeros ((N_x * N_y, N_x * N_y)); matriz_f_izq = np.zeros ((N_x * N_y, N_x * N_y)); matriz_f_suma = np.zeros ((N_x * N_y, N_x * N_y))
    matriz_g_der = np.zeros ((N_x * N_y, N_x * N_y)); matriz_g_izq = np.zeros ((N_x * N_y, N_x * N_y)); matriz_g_suma = np.zeros ((N_x * N_y, N_x * N_y))
    matriz_h_der = np.zeros ((N_x * N_y, N_x * N_y)); matriz_h_izq = np.zeros ((N_x * N_y, N_x * N_y)); matriz_h_suma = np.zeros ((N_x * N_y, N_x * N_y))
    matriz_k_der = np.zeros ((N_x * N_y, N_x * N_y)); matriz_k_izq = np.zeros ((N_x * N_y, N_x * N_y)); matriz_k_suma = np.zeros ((N_x * N_y, N_x * N_y))
    matriz_l_der = np.zeros ((N_x * N_y, N_x * N_y)); matriz_l_izq = np.zeros ((N_x * N_y, N_x * N_y)); matriz_l_suma = np.zeros ((N_x * N_y, N_x * N_y))
    matriz_v_ij_der = np.zeros ((N_x * N_y, N_x * N_y)); matriz_v_ij_izq = np.zeros ((N_x * N_y, N_x * N_y)); matriz_v_ij_suma = np.zeros ((N_x * N_y, N_x * N_y))
    vector_b_libre = np.zeros((N_x * N_y, 1))
    for element in lados:
        for j in range (0, N_y):
            for i in range (0, N_x):
                x_control_panel_ij = matriz_x_control[0, j * N_x + i]
                y_control_panel_ij = matriz_y_control[0, j * N_x + i]
                for panel in range (0, N_x * N_y):
                    a = x_control_panel_ij - matriz_x_1[element, panel]
                    b = y_control_panel_ij - matriz_y_1[element, panel]
                    c = x_control_panel_ij - matriz_x_2[element, panel]
                    d = y_control_panel_ij - matriz_y_2[element, panel]
                    e = (a ** 2 + b ** 2) ** (0.5)
                    f = (c ** 2 + d ** 2) ** (0.5)
                    g = matriz_x_2[element, panel] - matriz_x_1[element, panel]
                    h = matriz_y_2[element, panel] - matriz_y_1[element, panel]
                    k = (((g * a + h * b) / e) - ((g * c + h * d) / f))
                    l = (((- 1 / b) * (1 + a / e)) + ((1 / d) * (1 + c / f)))
                    v_ij = (k / ((4 * np.pi) * (a * d - c * b))) + (l / (4 * np.pi))
                    if element == 0:
                        matriz_a_der[j * N_x + i, panel] = a
                        matriz_b_der[j * N_x + i, panel] = b
                        matriz_c_der[j * N_x + i, panel] = c
                        matriz_d_der[j * N_x + i, panel] = d
                        matriz_e_der[j * N_x + i, panel] = e
                        matriz_f_der[j * N_x + i, panel] = f
                        matriz_g_der[j * N_x + i, panel] = g
                        matriz_h_der[j * N_x + i, panel] = h 
                        matriz_k_der[j * N_x + i, panel] = k
                        matriz_l_der[j * N_x + i, panel] = l
                        matriz_v_ij_der[j * N_x + i, panel] = v_ij
                    else:
                        matriz_a_izq[j * N_x + i, panel] = a
                        matriz_b_izq[j * N_x + i, panel] = b
                        matriz_c_izq[j * N_x + i, panel] = c
                        matriz_d_izq[j * N_x + i, panel] = d
                        matriz_e_izq[j * N_x + i, panel] = e
                        matriz_f_izq[j * N_x + i, panel] = f
                        matriz_g_izq[j * N_x + i, panel] = g
                        matriz_h_izq[j * N_x + i, panel] = h 
                        matriz_k_izq[j * N_x + i, panel] = k
                        matriz_l_izq[j * N_x + i, panel] = l
                        matriz_v_ij_izq[j * N_x + i, panel] = v_ij
    # matriz_a_suma = matriz_a_der + matriz_a_izq
    # matriz_b_suma = matriz_b_der + matriz_b_izq
    # matriz_c_suma = matriz_c_der + matriz_c_izq
    # matriz_d_suma = matriz_d_der + matriz_d_izq
    # matriz_e_suma = matriz_e_der + matriz_e_izq
    # matriz_f_suma = matriz_f_der + matriz_f_izq
    # matriz_g_suma = matriz_g_der + matriz_g_izq
    # matriz_h_suma = matriz_h_der + matriz_h_izq
    # matriz_k_suma = matriz_k_der + matriz_k_izq
    # matriz_l_suma = matriz_l_der + matriz_l_izq
    matriz_v_ij_suma = matriz_v_ij_der + matriz_v_ij_izq
    # print (matriz_v_ij_suma)
    # print (matriz_b_izq)
    # print (vector_b_libre)
    
    
    angulos_grafica = np.zeros ((len(angulos)))
    cls_ala = np.zeros ((len(angulos))); cdTs_ala = np.zeros ((len(angulos))); cm0ys_ala = np.zeros ((len(angulos))); cmacs = np.zeros ((len(angulos)))
    for i in range(0, len(angulos)):
        angulos_grafica[i] = angulos[i]
        
    
    der_3c4_todos = pendiente_3c4 (0.04, 0.3, N_x, N_y)
    # print (der_3c4_todos)
    b_ij = (b_env / (2 * N_y))    
    c_ij = np.zeros (N_y * N_x); c_j = np.zeros (N_y); s_ij = np.zeros (N_y * N_x); s_j = np.zeros (N_y)
    for j in range (0, N_y):
        for i in range (0, N_x):
            c_ij[j * N_x + i] = (cr_panel[j] + cr_panel[j + 1]) / 2
            c_j[j] += c_ij[j * N_x + i]
            s_ij[j * N_x + i] = b_ij * c_ij[j * N_x + i]
            s_j[j] += s_ij[j * N_x + i]
    # print (c_ij)
    # print (c_j)
    # print (s_ij)
    # print (s_j)
    
    d_x_14 = np.zeros ((N_x * N_y))
    for j in range (N_x * N_y):
        d_x_14[j] = matriz_x_control[0, j] - (c_ij[j] / 2)
    # print (d_x_14)
    y_cj_y2 = np. copy (matriz_d_der).T; y_cj_y1 = np. copy (matriz_b_izq).T
    w_libre_t_der = 1 / (2 * np.pi * y_cj_y2)
    w_libre_t_izq = - 1 / (2 * np.pi * y_cj_y1)
    # print (w_libre_t_der)
    # print (w_libre_t_izq)
    
    angulos_barridos = -1
    for alpha in angulos:
        angulos_barridos += 1
        alpha = np.radians(alpha)
        for j in range(0, N_x * N_y):
            torsion_j = ((np.pi * torsion *  matriz_y_control[0,j]) / (90 * b_env))
            # print (torsion_j)
            der_3c4_j = der_3c4_todos [j]
            # der_3c4_j = 0
            vector_b_libre[j, 0] = - (alpha + torsion_j - der_3c4_j)
        # print (vector_b_libre)

        gamma = np.linalg.solve(matriz_v_ij_suma, vector_b_libre)
        gamma = gamma.reshape(1, -1)
        # print (gamma)
    
        w_neto = np.zeros ((N_x * N_y))
        for j in range (0, N_y):
            for i in range (0, N_x):
                if j == (N_y - 1):
                    w_neto[N_y * i + j] = gamma[0, j * N_x + i]
                else:
                    w_neto[N_y * i + j] = gamma[0, j * N_x + i] - gamma[0, N_x * (j + 1) + i]
        suma_w_libre = w_libre_t_der + w_libre_t_izq
        # print(suma_w_libre)
        alpha_i_inf = np.dot(w_neto, suma_w_libre)
        alpha_i_cero = alpha_i_inf / 2
        # print (w_neto)
        # print (alpha_i_cero)
    
        cl_ij_todos = np.zeros ((N_x * N_y)); cm0y_ij_todos = np.zeros((N_x * N_y)); cdT_j_todos = np.zeros((N_x * N_y))
        cl_j = np.zeros((N_y)); cm0y_j = np.zeros((N_y)); cdT_j = np.zeros((N_y))
        sumatorio_cl = 0; sumatorio_cm0y = 0; sumatorio_cd = 0
        
        for j in range (0, N_y):
            sumatorio_cl_j = 0; sumatorio_cm0y_j = 0
            for i in range (0, N_x):
                cl_ij = 2 * gamma[0, j * N_x + i] / c_ij[j * N_x + i]
                cl_ij_todos[j * N_x + i] = cl_ij
                cm0y_ij = - cl_ij * d_x_14[j * N_x + i] / c_ij[j * N_x + i]
                cm0y_ij_todos[j * N_x + i] = cm0y_ij
                sumatorio_cl_j += (cl_ij * c_ij[j * N_x + i])
                sumatorio_cm0y_j += cm0y_ij * s_ij [j * N_x + i] * c_ij [j * N_x + i]
            cl_j[j] = sumatorio_cl_j / c_j[j]
            cm0y_j[j] = sumatorio_cm0y_j / (s_j[j] * c_j[j])
            sumatorio_cl += cl_j[j] * c_j[j] * b_ij
            sumatorio_cm0y += cm0y_j[j] * s_j[j] * c_j[j]
        cl_ala = 2 * sumatorio_cl / superficie_alar
        cm0y_ala = 2 * sumatorio_cm0y / (superficie_alar * c_am)
        cmac = cm0y_ala + cl_ala * (x_c_aw / c_am)
        
        for k in range (0, N_x * N_y):
            cdT_j = - cl_ij_todos[k] * alpha_i_cero[k]
            sumatorio_cd += cdT_j * s_ij[k]
            cdT_j_todos[k] = cdT_j
        cdT_ala = 2 * sumatorio_cd / superficie_alar
        
        cls_ala[angulos_barridos] = cl_ala
        cdTs_ala[angulos_barridos] = cdT_ala
        cm0ys_ala[angulos_barridos] = cm0y_ala
        cmacs[angulos_barridos] = cmac
        
        # print (cl_ij_todos)
        # print (cl_j)
        # print (cl_ala)
        # print (cm0y_ij_todos)
        # print (cm0y_j)
        # print (cm0y_ala)
        # print (cmac)
        # print (cdT_j)
        # print (cdT_j_todos)
        # print (cdT_ala)
        
        
        colores = ["red", "blue", "green", "orange", "purple"]
        
        
        
        cl_ij_ala = np.zeros ((2 * N_x * N_y))
        cl_ij_ala[N_x * N_y:] = cl_ij_todos
        cl_ij_ala[:N_x * N_y] = cl_ij_todos[::-1]
        cl_j_ala = np.zeros ((2 * N_y))
        cl_j_ala[N_y:] = cl_j             
        cl_j_ala[:N_y] = cl_j[::-1]
        cm0y_ij_ala = np.zeros ((2 * N_x * N_y))
        cm0y_ij_ala[N_x * N_y:] = cm0y_ij_todos
        cm0y_ij_ala[:N_x * N_y] = cm0y_ij_todos[::-1]
        cm0y_j_ala = np.zeros ((2 * N_y))
        cm0y_j_ala[N_y:] = cm0y_j             
        cm0y_j_ala[:N_y] = cm0y_j[::-1]
        cdT_j_ala = np.zeros ((2 * N_x * N_y))
        cdT_j_ala[N_x * N_y:] = cdT_j_todos
        cdT_j_ala[:N_x * N_y] = cdT_j_todos[::-1]
        
        
   
        if completa == "0":
            paneles_grafica = paneles
            paneles_grafica_y = paneles_y
            cl_ij_grafica = cl_ij_todos
            cl_j_grafica = cl_j
            cm0y_ij_grafica = cm0y_ij_todos
            cm0y_j_grafica = cm0y_j
            cdT_j_grafica = cdT_j_todos
            
        else:
            paneles_grafica = todos_paneles
            paneles_grafica_y = todos_paneles_y
            cl_ij_grafica = cl_ij_ala
            cl_j_grafica = cl_j_ala
            cm0y_ij_grafica = cm0y_ij_ala
            cm0y_j_grafica = cm0y_j_ala
            cdT_j_grafica = cdT_j_ala
            
        
        # df = pd.DataFrame(cdT_j_todos)
        # archivo_excel = r'C:\Aerodinámica\Alas\Excel\Trabajo de alas mio.xlsx'
        # book = load_workbook(archivo_excel)
        # with pd.ExcelWriter(archivo_excel, engine='openpyxl', mode='a', if_sheet_exists='new') as writer:
        #     df.to_excel(writer, sheet_name='MatrizNueva', index=False, header=False)
        
        
        fig3 = plt.figure(3)
        plt.plot(paneles_grafica[:N_x * N_y], cl_ij_grafica[:N_x * N_y], marker="o", linestyle="-", color=colores[angulos_barridos])
        plt.plot(paneles_grafica[N_x * N_y:], cl_ij_grafica[N_x * N_y:], marker="o", linestyle="-", color=colores[angulos_barridos], label= "α = " + str(round(np.degrees(alpha), 1)) + "º")
        plt.title("cl en cada panel"); plt.xlabel("panel"); plt.ylabel("cl panel"); plt.grid(True); plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.tight_layout()
        
        fig4 = plt.figure(4)
        plt.plot(paneles_grafica_y[:N_y], cl_j_grafica[:N_y], marker="o", linestyle="-", color=colores[angulos_barridos])
        plt.plot(paneles_grafica_y[N_y:], cl_j_grafica[N_y:], marker="o", linestyle="-", color=colores[angulos_barridos], label= "α = " + str(round(np.degrees(alpha), 1)) + "º")
        plt.title("Cl en cada perfil"); plt.xlabel("perfil"); plt.ylabel("Cl perfil"); plt.grid(True); plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.tight_layout()
        
        fig5 = plt.figure(5)
        plt.plot(paneles_grafica[:N_x * N_y], cm0y_ij_grafica[:N_x * N_y], marker="o", linestyle="-", color=colores[angulos_barridos])
        plt.plot(paneles_grafica[N_x * N_y:], cm0y_ij_grafica[N_x * N_y:], marker="o", linestyle="-", color=colores[angulos_barridos], label= "α = " + str(round(np.degrees(alpha), 1)) + "º")
        plt.title("cm0y en cada panel"); plt.xlabel("panel"); plt.ylabel("cm0y panel"); plt.grid(True); plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.tight_layout()
        
        fig6 = plt.figure(6)
        plt.plot(paneles_grafica_y[:N_y], cm0y_j_grafica[:N_y], marker="o", linestyle="-", color=colores[angulos_barridos])
        plt.plot(paneles_grafica_y[N_y:], cm0y_j_grafica[N_y:], marker="o", linestyle="-", color=colores[angulos_barridos], label= "α = " + str(round(np.degrees(alpha), 1)) + "º")
        plt.title("Cm0y en cada perfil"); plt.xlabel("perfil"); plt.ylabel("Cm0y perfil"); plt.grid(True); plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.tight_layout()
        
        fig7 = plt.figure(7)
        plt.plot(paneles_grafica[:N_x * N_y], cdT_j_grafica[:N_x * N_y], marker="o", linestyle="-", color=colores[angulos_barridos])
        plt.plot(paneles_grafica[N_x * N_y:], cdT_j_grafica[N_x * N_y:], marker="o", linestyle="-", color=colores[angulos_barridos], label= "α = " + str(round(np.degrees(alpha), 1)) + "º")
        plt.title("cd Trefft en cada perfil"); plt.xlabel("perfil"); plt.ylabel("cd perfil"); plt.grid(True); plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.tight_layout()
       
    fig8 = plt.figure(8)
    plt.plot(angulos_grafica, cls_ala, marker="o", linestyle="-", color= "blue")
    plt.title("CL en función de α"); plt.xlabel("α (º)"); plt.ylabel("CL"); plt.grid(True)
    plt.tight_layout()
    
    fig9 = plt.figure(9)
    plt.plot(angulos_grafica, cdTs_ala, marker="o", linestyle="-", color= "green")
    plt.title("CD Trefft en función de α"); plt.xlabel("α (º)"); plt.ylabel("CD Trefft"); plt.grid(True)
    plt.tight_layout()
    
    fig10 = plt.figure(10)
    plt.plot(angulos_grafica, cm0ys_ala, marker="o", linestyle="-", color= "purple", label = "CM0y")
    plt.plot(angulos_grafica, cmacs, marker="o", linestyle="-", color= "red", label = "CMac")
    plt.title("CM0y y CMac en función de α"); plt.xlabel("α (º)"); plt.ylabel("CM0y, Cmac"); plt.grid(True)
    plt.legend(loc='upper right'); plt.tight_layout()
    
    fig11 = plt.figure(11)
    plt.plot(angulos_grafica, cmacs, marker="o", linestyle="-", color= "red", label = "CMac")
    plt.title("CMac en función de α"); plt.xlabel("α (º)"); plt.grid(True)
    plt.tight_layout()
    
    
    # if completa == "0":
    #     fig3.savefig('C:\Aerodinámica\Alas\Figuras/clpanelNx1.svg')
    #     fig4.savefig('C:\Aerodinámica\Alas\Figuras/clperfilNx1.svg')
    #     fig5.savefig('C:\Aerodinámica\Alas\Figuras/cm0ypanelNx1.svg')
    #     fig6.savefig('C:\Aerodinámica\Alas\Figuras/cm0yperfilNx1.svg')
    #     fig7.savefig('C:\Aerodinámica\Alas\Figuras/cdTperfilNx1.svg')
    # else:
    #     fig3.savefig('C:\Aerodinámica\Alas\Figuras/clpanelNx1ala.svg')
    #     fig4.savefig('C:\Aerodinámica\Alas\Figuras/clperfilNx1ala.svg')
    #     fig5.savefig('C:\Aerodinámica\Alas\Figuras/cm0ypanelNx1ala.svg')
    #     fig6.savefig('C:\Aerodinámica\Alas\Figuras/cm0yperfilNx1ala.svg')
    #     fig7.savefig('C:\Aerodinámica\Alas\Figuras/cdTperfilNx1ala.svg')
    
    # fig2.savefig('C:\Aerodinámica\Alas\Figuras/PanelizacionNx1.svg')    
    # fig8.savefig('C:\Aerodinámica\Alas\Figuras/CLNx1.svg')
    # fig9.savefig('C:\Aerodinámica\Alas\Figuras/CDTNx1.svg')
    # fig10.savefig('C:\Aerodinámica\Alas\Figuras/CM0yNx1_CMacNx1.svg')
    # fig11.savefig('C:\Aerodinámica\Alas\Figuras/CMacNx1.svg')

    
        
    
    plt.show()
    
    
    return




#%% Ejecutables
lista_alpha = [-12, -6, 0, 6, 12]

panelizacion (0.4, 16, 10, -4, 1, 4, 12, "0", lista_alpha)