#Aerodinámica de perfiles
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import quad
from scipy.optimize import fsolve
import pandas as pd
import re

#%% Perfil

def NACA(persona1, persona2, persona3, DNI1, DNI2, DNI3):
    
    Abecedario={"a":0, "b":1, "c":2, "d":3, "e":4, "f":5,
                "g":6, "h":7, "i":8, "j":9, "k":10, "l":11,
                "m":12, "n":13, "ñ":14, "o":15, "p":16, "q":17,
                "r":18, "s":19, "t":20, "u":21, "v":22, "w":23,
                "x":24, "y":25, "z":26}
    Apellidos = [persona1, persona2, persona3]; Primera_apellido =[]; Segunda_apellido =[]; Apellidos_descarte=[]; DNI_perfil =[]
    
    for i in Apellidos:
        for j in range (0,2):
            if j == 0:
                Primera_apellido.append(Abecedario[i[j]])
            else:
                Segunda_apellido.append(Abecedario[i[j]])

    for i in Primera_apellido:
        if i == min(Primera_apellido):
            Apellidos_descarte.append(i)
        else:
            Apellidos_descarte.append(30)
            
    Posiciones_minimo = [i for i, valor in enumerate(Apellidos_descarte) if valor == min(Apellidos_descarte)]
    if len(Posiciones_minimo)>1:
        if Segunda_apellido[Posiciones_minimo[0]] < Segunda_apellido[Posiciones_minimo[1]]:
            Apellidos_descarte[Posiciones_minimo[1]] = 30; Apellido_perfil = int(Apellidos_descarte[Posiciones_minimo[0]]) 
        else:
            Apellidos_descarte[Posiciones_minimo[0]] = 30; Apellido_perfil = int(Apellidos_descarte[Posiciones_minimo[1]])
    else:
        Apellido_perfil = (Apellidos_descarte[Posiciones_minimo[0]])
        
    Posicion_DNI_perfil = Apellidos_descarte.index(Apellido_perfil)
    if Posicion_DNI_perfil == 0:
        DNI_perfil.append(DNI1)
    elif Posicion_DNI_perfil == 1:
        DNI_perfil.append(DNI2)
    else:
        DNI_perfil.append(DNI3)
        
        
    V = int(DNI_perfil[0][3]); W = int(DNI_perfil[0][4]); X = int(DNI_perfil[0][5]); Y = int(DNI_perfil[0][6]); Z = int(DNI_perfil[0][7])
    f = (1 + int(0.375 * V)); x_f = (20 + 10 * int(0.25 * W)); t = (12 + int (8 * X / 9))
    # print("El perfil es NACA" + str(f) + str(int(x_f/10)) + str(t))
    c_a = (20 + 5 * int(0.375 * Y)); d_a = (5 + 5 * int(0.25 * Z)); d_a_rad = (d_a * np.pi / 180)
    
    
    x_f_y_c = (x_f/100); f_y_c = (f/100); y_c = []; y_ext = []; y_int = []
    x = np.linspace(0, 1, 1001)
    y_t = (+ 5 * (t / 100) * (0.2969 * x ** 0.5 - 0.126 * x - 0.3516 * x ** 2 + 0.2843 * x ** 3 - 0.1015 * x ** 4))
    y_c = np.where(x <= x_f_y_c, 
                   (f_y_c / x_f_y_c ** 2) * (2 * x_f_y_c * x - x ** 2),
                   (f_y_c / (1 - x_f_y_c) ** 2) * ((1 - 2 * x_f_y_c) + 2 * x_f_y_c * x - x ** 2))
    y_ext = y_c + y_t; y_int = y_c - y_t


    plt.figure(figsize=(16, 4)) 
    plt.figure(1)
    plt.plot(x,y_ext, linestyle='-', color = "black", label = "Extradós")
    plt.plot(x,y_int, linestyle='-', color = "blue", label = "Intradós")
    plt.plot(x,y_c, linestyle='--', color = "red", label = "Línea media")
    plt.plot(x, np.zeros_like(x), linestyle='-', color = "green", label = "Cuerda")
    plt.axis("equal")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xlabel("x/c"); plt.ylabel("z/c"); plt.title("NACA " + str(f) + str(int(x_f/10)) + str(t)); plt.legend()


    inicio_timon = 1 - c_a / 100
    y_c_timon = np.copy(y_c)
    y_c_timon = np.where(x >= inicio_timon, y_c_timon - d_a * (np.pi / 180) * (x - (1 - c_a / 100)), y_c_timon)
    y_ext_timon = y_c_timon + y_t; y_int_timon = y_c_timon - y_t

    plt.figure(figsize=(16, 4))
    plt.figure(2)
    plt.plot(x,y_c_timon, linestyle='--', color = "red", label = "Línea media")
    plt.plot(x,y_ext_timon, linestyle='-', color = "black", label = "Extradós")
    plt.plot(x,y_int_timon, linestyle='-', color = "blue", label = "Intradós")
    plt.axis("equal")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xlabel("x/c"); plt.ylabel("z/c"); plt.title("NACA " + str(f) + str(int(x_f/10)) + str(t) + " con" +" timón c_a =" + str(c_a / 100) + " δ_a =" + str(d_a) +"º")
    plt.legend()
    
    plt.figure(figsize=(16, 4))
    plt.figure(3)
    plt.plot(x,y_ext, linestyle='-', color = "black", label = "Extradós")
    plt.plot(x,y_int, linestyle='-', color = "blue", label = "Intradós")
    plt.plot(x,y_c, linestyle='-', color = "red", label = "Línea media")
    plt.plot(x,y_c_timon, linestyle='--', color = "red", label = "Línea media con timón")
    plt.plot(x,y_ext_timon, linestyle='--', color = "black", label = "Extradós con timón")
    plt.plot(x,y_int_timon, linestyle='--', color = "blue", label = "Intradós con timón")
    plt.axis("equal")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xlabel("x/c"); plt.ylabel("z/c"); plt.title("NACA " + str(f) + str(int(x_f/10)) + str(t) + " con y sin timón"); plt.legend()
  
    
    return t, x_f_y_c, f_y_c, inicio_timon, d_a_rad

#%% Theodorsen

def derivada_epsilon (a_1, a_2, phi_01, phi_02, phi):
        
    der_epsilon = (a_1 * np.cos(phi) + 2 * a_2 * np.cos(2 * phi))/(1 - (a_1 * np.cos(phi) + 2 * a_2 * np.cos(2 * phi)))
        
    return der_epsilon


def derivada_psi (a_1, a_2, phi_01, phi_02, phi):
        
    der_psi = (- a_1 * np.sin(phi) - 2 * a_2 * np.sin(2 * phi))/(1 - (a_1 * np.cos(phi) + 2 * a_2 * np.cos(2 * phi)))
        
    return der_psi


def Theodorsen (alpha, t):
    
    phi = np.linspace (0, 360 * np.pi / 180, 361); alpha = alpha * np.pi / 180
    A_1 = 0.005 * t + 0.005; A_2 = - 0.00028 * t - 0.00252; psi_0 = 0.00913 * t - 0.00458; phi_01 = 0; phi_02 = 0
    print("-" * 60); print ("A1 Theodorsen =",A_1, "A2 Theodorsen =", A_2, "Ψ0 =", psi_0)   
    epsilon = A_1 * np.sin(phi - phi_01) + A_2 * np.sin(2 * phi - phi_02); epsilon_bs = epsilon [180]
    psi = A_1 * np.cos(phi - phi_01) + A_2 * np.cos(2 * phi - phi_02) + psi_0
    theta = phi - epsilon
    a = 0.5 / ((np.cosh(psi[0]) * np.cos(theta[0])) - (np.cosh(psi[180]) * np.cos(theta[180])))
    x = 2 * a * np.cosh(psi) * np.cos(theta); x_Theodorsen = (1 - (x - min(x)))
    y = 2 * a * np.sinh(psi) * np.sin(theta)
    der_epsilon = derivada_epsilon (A_1, A_2, phi_01, phi_02, phi)
    der_psi = derivada_psi (A_1, A_2, phi_01, phi_02, phi)
    # print (a)
    print (epsilon_bs)
    
    v_vinf = ((np.sin(alpha + phi)) + np.sin(alpha + epsilon_bs)) * (((1 + der_epsilon) * np.exp(psi_0)) / (((np.sinh(psi) ** 2 + np.sin(theta) ** 2) * (1 + der_psi ** 2)) ** 0.5))
    C_p_Theodorsen = (1 - (v_vinf) ** 2)
    C_l_Theodorsen = (2 * np.pi * np.exp(psi_0) * (alpha + epsilon_bs))
    # print("Cl Theodorsen =", C_l)
    C_l_alpha_Theodorsen = 2 * np.pi * np.exp (psi_0)
    print("Cl α Theodorsen =",C_l_alpha_Theodorsen) 


    plt.figure(figsize=(16, 4))
    plt.figure(3); plt.plot(x_Theodorsen, y, linestyle='-', color = "black", label = "Z perfil")
    plt.axis("equal")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xlabel("x/c"); plt.ylabel("z/c"); plt.title("NACA" + " 00" + str(t) + " por Theodorsen"); plt.legend()
    
    plt.figure(4)
    plt.plot(phi,psi, linestyle='-', color = "red", label = "ψ")
    plt.plot(phi,epsilon, linestyle='-', color = "green", label = "ε")
    plt.grid(True, linestyle='--', alpha=0.5); plt.xlabel("φ"); plt.title("ψ, ε"); plt.legend()
    
    plt.figure(5)
    plt.plot(phi, der_psi, linestyle='-', color = "red", label = "ψ")
    plt.plot(phi,der_epsilon, linestyle='-', color = "green", label = "ε")
    plt.grid(True, linestyle='--', alpha=0.5); plt.xlabel("φ"); plt.title(" Derivdas de ψ, ε"); plt.legend()
    
    plt.figure(6)
    # plt.plot(x_Theodorsen[:180], C_p_Theodorsen[:180], linestyle='-', color = "blue", label = "Cp"); plt.gca().invert_yaxis()
    plt.plot(x_Theodorsen, C_p_Theodorsen, linestyle='-', color = "blue", label = "Cp"); plt.gca().invert_yaxis()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xlabel("x/c"); plt.ylabel("Cp"); plt.title("Cp del espesor por Theodorsen para α = " +str(alpha * 180 / np.pi) +"º"); plt.legend()
    
    plt.figure(7)
    plt.plot(x_Theodorsen[:180], C_p_Theodorsen[:180], linestyle='-', color = "black", label = "Extradós")
    plt.plot(x_Theodorsen[180:], C_p_Theodorsen[180:], linestyle='-', color = "blue", label = "Intradós")
    plt.gca().invert_yaxis()
    plt.grid(True, linestyle='--', alpha=0.5); plt.xlabel("x/c")
    plt.ylabel("Cp"); plt.title("Cp del espesor por Theodorsen para α = " +str(alpha * 180 / np.pi) +"º"); plt.legend()


    return C_l_Theodorsen, C_l_alpha_Theodorsen, x_Theodorsen, C_p_Theodorsen
    
#%% Glauert

def coeficientes_Glauert (x_f, f, inicio_timon, delta_timon, n):
    
    theta_xf = np.arccos (2 * x_f - 1); theta_timon = np.arccos (2 * inicio_timon - 1); A_n = []; A_n_timon = []
    for i in range (0, n + 1):
        integral_yc1, _ = quad(lambda x: (((2 * x_f - (1 + np.cos(x))) * (f / x_f ** 2)) * np.cos(i * x)), theta_xf, np.pi)
        integral_yc2, _ = quad(lambda x: (((2 * x_f - (1 + np.cos(x))) * (f / (1 - x_f) ** 2)) * np.cos(i * x)), 0, theta_xf)
        j = 1 if i == 0 else 2
        A_i = (- j / np.pi) * (integral_yc1 + integral_yc2); A_n.append(A_i)
    
    for i in range (0, n + 1):
        integral_yc3, _ = quad(lambda x: (( - delta_timon) * np.cos(i * x)), 0, theta_timon)
        j = 1 if i == 0 else 2
        A_i = (- j / np.pi) * (integral_yc3); A_n_timon.append(A_i)
    
    A_n = np.array(A_n); A_n_timon = np.array(A_n_timon); A_n_totales = A_n + A_n_timon
    
    N = []
    for i in range (0, n + 1):
        N.append(i)
    plt.figure(8)
    plt.plot(N, A_n_totales, linestyle='-', color = "red")
    plt.grid(True, linestyle='--', alpha=0.5); plt.xlabel("n"); plt.ylabel("An"); plt.title("Valor de An totales vs n")

    print("-" * 60); print("Coeficientes de Glauert:"); print ("A0 =", A_n[0], "A1 =", A_n[1], "A2 =", A_n[2])
    print("Coeficientes de Glauert solo timón:"); print ("A0 =", A_n_timon[0], "A1 =", A_n_timon[1], "A2 =", A_n_timon[2])
    print("Coeficientes de Glauert totales con timón:"); print ("A0 =", A_n_totales[0], "A1 =", A_n_totales[1], "A2 =", A_n_totales[2]); print("-" * 60)
    
    
    return A_n, A_n_timon, A_n_totales, theta_timon

#%% TPL

def TPL(A_n_sin, A_n_con, A_n_total, x_theodorsen, theta_timon, alpha):
    
    A_n = A_n_sin; A_n_timon = A_n_con; A_n_totales = A_n_total
    
    Cl_TPL_alpha = 2 * np.pi * (A_n[0] + A_n[1] / 2) + 2 * np.pi * (alpha * np.pi / 180)
    alpha_ideal_radianes = - A_n [0]; alpha_ideal_grados = (- A_n [0] * 180 / np.pi)
    Cl_ideal = np.pi * A_n[1]
    Cm_c4_sin = (- np.pi / 4) * (A_n[1] + A_n[2])
    
  
    x_Theodorsen = np.copy(x_theodorsen); theta_Theodorsen_rad = np.arccos(2 * x_Theodorsen - 1)
    
    Sumatorio_An_senos = np.sum([A_n[n] * np.sin(n * theta_Theodorsen_rad) for n in range(201)], axis=0)
    Cl_TPL_theta_alpha = 4 * ((alpha * np.pi / 180 + A_n[0]) *np.tan(theta_Theodorsen_rad / 2) + Sumatorio_An_senos)
    Cp_TPL_theta_alpha = (- Cl_TPL_theta_alpha / 2)
    Cl_TPL_theta_alphaideal = 4 * Sumatorio_An_senos
    Cp_TPL_theta_alphaideal = (- Cl_TPL_theta_alphaideal / 2)
    Integral_Cl_charnela_sin, _ = quad(lambda x: ((4 * ((alpha * np.pi / 180 + A_n[0]) *np.tan(x / 2) + np.sum([A_n[n] * np.sin(n * x) for n in range(201)], axis=0))) * (np.cos(x) - np.cos(theta_timon)) * np.sin(x)), 0, theta_timon)
    M_charnela_sin_defectar = 0.25 * Integral_Cl_charnela_sin
    
    
    Cl_TPL_alpha_timon = 2 * np.pi * (A_n_timon[0] + A_n_timon[1] / 2) + 2 * np.pi * (alpha * np.pi / 180)
    alpha_ideal_timon_radianes = - A_n_totales [0]; alpha_ideal_timon_grados = (- A_n_totales [0] * 180 / np.pi)
    Cl_ideal_timon = np.pi * A_n_timon[1]
    Cm_c4_timon = (- np.pi / 4) * (A_n_timon[1] + A_n_timon[2])
    
    
    Cl_total = 2 * np.pi * (A_n_totales[0] + A_n_totales[1] / 2) + 2 * np.pi * (alpha * np.pi / 180)
    Cm_c4_total = (- np.pi / 4) * (A_n_totales[1] + A_n_totales[2])
    
    
    Sumatorio_An_senos_timon = np.sum([A_n_totales[n] * np.sin(n * theta_Theodorsen_rad) for n in range(201)], axis=0)
    Cl_TPL_theta_alpha_timon = 4 * ((alpha * np.pi / 180 + A_n_totales[0]) *np.tan(theta_Theodorsen_rad / 2) + Sumatorio_An_senos_timon)
    Cp_TPL_theta_alpha_timon = (- Cl_TPL_theta_alpha_timon / 2)
    Cl_TPL_theta_alphaideal_timon = 4 * Sumatorio_An_senos_timon
    Cp_TPL_theta_alphaideal_timon = (- Cl_TPL_theta_alphaideal_timon / 2)
    Integral_Cl_charnela_con, _ = quad(lambda x: ((4 * ((alpha * np.pi / 180 + A_n_totales[0]) *np.tan(x / 2) + np.sum([A_n_totales[n] * np.sin(n * x) for n in range(201)], axis=0))) * (np.cos(x) - np.cos(theta_timon)) * np.sin(x)), 0, theta_timon)
    M_charnela_con_defectar = 0.25 * Integral_Cl_charnela_con

    
    Cp_total_alpha = Cp_TPL_theta_alpha + Cp_TPL_theta_alpha_timon
    Cp_total_alphaideal = Cp_TPL_theta_alphaideal + Cp_TPL_theta_alphaideal_timon
    
    print ("α ideal sin timón =", alpha_ideal_radianes, "rad =", alpha_ideal_grados, "º")
    print ("Cl_ideal sin timón =", Cl_ideal)
    print ("Cl TPL sin timón =", Cl_TPL_alpha)
    print ("Cmc4 sin timón =", Cm_c4_sin)
    print ("Momento de charnela sin defectar el timón =", M_charnela_sin_defectar)
    print ("Cl_ideal solo timón =", Cl_ideal_timon)
    print ("Cl TPL solo timón = incremento Cl =", Cl_TPL_alpha_timon)
    print ("Cmc4 solo timón = incremento Cmc4 =", Cm_c4_timon)
    print ("α ideal con timón =", alpha_ideal_timon_radianes, "rad =", alpha_ideal_timon_grados, "º")
    print ("Cl total con timón =", Cl_total)
    print ("Cmc4 total con timón =", Cm_c4_total)
    print ("Momento de charnela deflectando el timón =", M_charnela_con_defectar)
    
    plt.figure(9)
    plt.plot(x_Theodorsen, Cp_TPL_theta_alphaideal, linestyle='-', color = "blue", label = "Cp α ideal")
    plt.plot(x_Theodorsen, Cp_TPL_theta_alphaideal_timon, linestyle='-', color = "red", label = "Cp timón α ideal")
    # plt.plot(x_Theodorsen, Cp_total_alphaideal, linestyle='-', color = "green", label = "Cp total α ideal")
    plt.plot(x_Theodorsen, Cp_TPL_theta_alpha, linestyle=':', color = "blue", label = "Cp α = " + str(alpha) + "º")
    plt.plot(x_Theodorsen, Cp_TPL_theta_alpha_timon, linestyle=':', color = "red", label = "Cp timón α = " + str(alpha) + "º")
    # plt.plot(x_Theodorsen, Cp_total_alpha, linestyle=':', color = "green", label = "Cp total α = " + str(alpha) + "º")
    plt.ylim(-0.5, 0)
    plt.gca().invert_yaxis(); plt.grid(True, linestyle='--', alpha=0.5); plt.xlabel("x/c"); plt.ylabel("Cp"); plt.title("Cp de la curvatura para α por TPL"); plt.legend()
    
    
    return Cp_TPL_theta_alphaideal, Cp_TPL_theta_alphaideal_timon, Cp_TPL_theta_alpha, Cp_TPL_theta_alpha_timon, Cm_c4_sin


#%% TPL + Theodorsen

def TPL_Theodorsen (A_n_sin, A_n_con, cl_alpha_theodorsen, x_theodorsen, c_p_theodorsen, cp_TPL_theta_ideal, cp_TPL_theta_ideal_timon, cp_TPL_theta_alpha, cp_TPL_theta_alpha_timon, cm_c4_sin, alpha):
    
    A_n = A_n_sin
    
    alpha_0_TPL = (- A_n[0] - A_n[1] / 2); Cl_0_TPL = 2 * np.pi * (+ A_n[0] + A_n[1] / 2)
    Cl_0_Clalpha_Theodorsen = - cl_alpha_theodorsen * alpha_0_TPL
    Cl_TPL_Theodorsen = Cl_0_Clalpha_Theodorsen + cl_alpha_theodorsen * (alpha * np.pi / 180)
    
    print("-" * 60)
    print("α0 =", alpha_0_TPL * 180 / np.pi, "º")
    print ("Cl0 por TPL =", Cl_0_TPL)
    print ("Cl0 con la pendiente de Theodorsen =", Cl_0_Clalpha_Theodorsen)
    print ("Clα del perfil completo =", cl_alpha_Theodorsen)
    print ("xca =", 0.25)
    print ("Cmca = Cmc4 =", cm_c4_sin, "para TPL")
    print("-" * 60)
    
    x = np.linspace(alpha_0_TPL * 180 / np.pi, 15, 100)
    
    Cl_TPL_Theodorsen_x = Cl_0_Clalpha_Theodorsen + cl_alpha_theodorsen * (x * np.pi / 180)
    Cl_TPL_x = 2 * np.pi * (A_n[0] + A_n[1] / 2) + 2 * np.pi * (x * np.pi / 180)
    Cl_Theodorsen_x = cl_alpha_theodorsen * (x * np.pi / 180)
    
    
    plt.figure(10)
    plt.plot(x, Cl_TPL_Theodorsen_x, linestyle='-', color = "blue", label = "TPL + Clα Theodorsen")
    plt.plot(x, Cl_TPL_x, linestyle='-', color = "red", label = "TPL (α + curvatura)")
    plt.plot(x, Cl_Theodorsen_x, linestyle='-', color = "green", label = "Theodorsen espesor")
    plt.ylim(0, 2.5); plt.grid(True, linestyle='--', alpha=0.5); plt.xlabel("α (º)"); plt.ylabel("Cl"); plt.title("Cl vs α"); plt.legend()
    
    
    
    cp_perfil_ideal = np.zeros(361); cp_perfil_ideal_con_timon = np.zeros(361)
    cp_perfil_ideal[:180] = c_p_theodorsen[:180] + cp_TPL_theta_ideal[:180]
    cp_perfil_ideal[180:] = c_p_theodorsen[180:] - cp_TPL_theta_ideal[180:]
    cp_perfil_ideal_con_timon[:180] = c_p_theodorsen[:180] + cp_TPL_theta_ideal_timon[:180]
    cp_perfil_ideal_con_timon[180:] = c_p_theodorsen[180:] - cp_TPL_theta_ideal_timon[180:]
    
    cp_perfil_alpha = np.zeros(361); cp_perfil_alpha_con_timon = np.zeros(361)
    cp_perfil_alpha[:180] = c_p_theodorsen[:180] + cp_TPL_theta_alpha[:180]
    cp_perfil_alpha[180:] = c_p_theodorsen[180:] - cp_TPL_theta_alpha[180:]
    cp_perfil_alpha_con_timon[:180] = c_p_theodorsen[:180] + cp_TPL_theta_alpha_timon[:180]
    cp_perfil_alpha_con_timon[180:] = c_p_theodorsen[180:] - cp_TPL_theta_alpha_timon[180:]

    
    plt.figure(11)
    plt.plot(x_Theodorsen[:180], cp_perfil_ideal[:180], linestyle='-', color = "blue", label = "Extradós α ideal")
    plt.plot(x_Theodorsen[180:], cp_perfil_ideal[180:], linestyle='-', color = "red", label = "Intradós α ideal")
    plt.plot(x_Theodorsen[:180], cp_perfil_alpha[:180], linestyle=':', color = "blue", label = "Extradós α =" + str(alpha) + "º")
    plt.plot(x_Theodorsen[180:], cp_perfil_alpha[180:], linestyle=':', color = "red", label = "Intradós α =" + str(alpha) + "º")
    plt.ylim(-1.5, 1); plt.gca().invert_yaxis(); plt.grid(True, linestyle='--', alpha=0.5); plt.xlabel("x/c")
    plt.ylabel("Cp"); plt.title("Cp del perfil sin timón"); plt.legend()   
    
    plt.figure(12)
    plt.plot(x_Theodorsen[:180], cp_perfil_ideal_con_timon[:180], linestyle='-', color = "blue", label = "Extradós α ideal")
    plt.plot(x_Theodorsen[180:], cp_perfil_ideal_con_timon[180:], linestyle='-', color = "red", label = "Intradós α ideal")
    plt.plot(x_Theodorsen[:180], cp_perfil_alpha_con_timon[:180], linestyle=':', color = "blue", label = "Extradós α =" + str(alpha) + "º")
    plt.plot(x_Theodorsen[180:], cp_perfil_alpha_con_timon[180:], linestyle=':', color = "red", label = "Intradós α =" + str(alpha) + "º")
    plt.ylim(-1.5, 1); plt.gca().invert_yaxis(); plt.grid(True, linestyle='--', alpha=0.5); plt.xlabel("x/c")
    plt.ylabel("Cp"); plt.title("Cp del perfil con timón"); plt.legend()
    
    plt.figure(13)
    plt.plot(x_Theodorsen[:180], cp_perfil_ideal[:180], linestyle='-', color = "blue", label = "Extradós sin timón")
    plt.plot(x_Theodorsen[180:], cp_perfil_ideal[180:], linestyle='-', color = "red", label = "Intradós sin timón")
    plt.plot(x_Theodorsen[:180], cp_perfil_ideal_con_timon[:180], linestyle=':', color = "blue", label = "Extradós con timón")
    plt.plot(x_Theodorsen[180:], cp_perfil_ideal_con_timon[180:], linestyle=':', color = "red", label = "Intradós con timón")
    plt.ylim(-1.5, 1); plt.gca().invert_yaxis(); plt.grid(True, linestyle='--', alpha=0.5); plt.xlabel("x/c"); plt.ylabel("Cp")
    plt.title("Cp del perfil para α ideal"); plt.legend()
    
    plt.figure(14)
    plt.plot(x_Theodorsen[:180], cp_perfil_alpha[:180], linestyle='-', color = "blue", label = "Extradós sin timón")
    plt.plot(x_Theodorsen[180:], cp_perfil_alpha[180:], linestyle='-', color = "red", label = "Intradós sin timón")
    plt.plot(x_Theodorsen[:180], cp_perfil_alpha_con_timon[:180], linestyle=':', color = "blue", label = "Extradós con timón")
    plt.plot(x_Theodorsen[180:], cp_perfil_alpha_con_timon[180:], linestyle=':', color = "red", label = "Intradós con timón")
    plt.ylim(-1.5, 1); plt.gca().invert_yaxis(); plt.grid(True, linestyle='--', alpha=0.5); plt.xlabel("x/c"); plt.ylabel("Cp")
    plt.title("Cp del perfil para α =" + str(alpha) + "º"); plt.legend()
    
    # fig = plt.figure(11)
    # fig.savefig("C:/Aerodinámica/naca4312.svg", format="svg")
        
    
    return cp_perfil_ideal, cp_perfil_alpha_con_timon

#%%Paneles

def paneles (v_infinito, alpha, N, t_perfil, x_f_y_c, f_y_c, inicio_timon, d_a, var_boleana):
    
    alpha = alpha * np.pi / 180
    beta = np.linspace(0, 2 * np.pi, N + 1)
    x = 0.5 * (1 + np.cos(beta))
    
    z_t = (+ 5 * (t_perfil / 100) * (0.2969 * (x ** 0.5) - 0.126 * x - 0.3516 * (x ** 2) + 0.2843 * (x ** 3) - 0.1015 * (x ** 4)))
    
    def timon (boleana, x):
        if boleana == "0":
            y_c = np.where(x <= x_f_y_c, 
                            (f_y_c / x_f_y_c ** 2) * (2 * x_f_y_c * x - x ** 2),
                            (f_y_c / (1 - x_f_y_c) ** 2) * ((1 - 2 * x_f_y_c) + 2 * x_f_y_c * x - x ** 2))
            return y_c
        
        elif boleana == "1":
            y_c = np.where(x <= x_f_y_c, 
                            (f_y_c / x_f_y_c ** 2) * (2 * x_f_y_c * x - x ** 2),
                            (f_y_c / (1 - x_f_y_c) ** 2) * ((1 - 2 * x_f_y_c) + 2 * x_f_y_c * x - x ** 2))
            y_c = np.where(x >= inicio_timon, y_c - d_a * (x - (inicio_timon)), y_c)
            return y_c
        
    y_c = timon (var_boleana, x)
    y_int = y_c - z_t
    y_ext = y_c + z_t
    altura_perfil = np.concatenate((y_int[:int(N / 2 + 1)], y_ext[int(N / 2 + 1):]))
    x_perfil = np.concatenate((x[:int(N / 2 + 1)], x[int(N / 2 + 1):]))
    inc_x = (x_perfil[1:] - x_perfil[:-1])
    inc_z = (altura_perfil[1:] - altura_perfil[:-1])
    # print (inc_x)
    # print (inc_z)
    # print (x_perfil)
    # print (altura_perfil)
    theta_i_rad = np.arctan2(inc_z, inc_x)
    theta_i_grados = theta_i_rad * (180 / np.pi)
    # print (theta_i_rad)
    # print (theta_i_grados)
    cuerda_i = (inc_x) * np.cos(theta_i_rad) + (inc_z) * np.sin(theta_i_rad)
    # print (cuerda_i)
    x_control_i = ((x_perfil[1:] + x_perfil[:-1]) / 2)
    z_control_i = ((altura_perfil[1:] + altura_perfil[:-1]) / 2)
    # print (x_control_i)
    # print (z_control_i)
    
    normal_i = np.column_stack((-np.sin(theta_i_rad), np.cos(theta_i_rad)))
    tangente_i = np.column_stack((np.cos(theta_i_rad), np.sin(theta_i_rad)))
    # print (normal_i)
    # print (tangente_i)
    v_inf_normal_i = v_infinito * (- np.cos(alpha) * np.sin(theta_i_rad) + np.sin(alpha) * np.cos(theta_i_rad))
    v_inf_tangente_i = v_infinito * (np.cos(alpha) * np.cos(theta_i_rad) + np.sin(alpha) * np.sin(theta_i_rad))
    # print (v_inf_normal_i)
    # print (v_inf_tangente_i)
    matriz_x_ij = np.zeros ((N, N))
    matriz_z_ij = np.zeros ((N, N))
    
    for i in range(0, N):
        for j in range (0, N):
            matriz_x_ij[i, j] = + (x_control_i[i] - x_perfil[j]) * np.cos(theta_i_rad[j]) + (z_control_i[i] - altura_perfil[j]) * np.sin(theta_i_rad[j])
    # print (matriz_x_ij)
    
    for i in range(0, N):
        for j in range (0, N):
            matriz_z_ij[i, j] = - (x_control_i[i] - x_perfil[j]) * np.sin(theta_i_rad[j]) + (z_control_i[i] - altura_perfil[j]) * np.cos(theta_i_rad[j])
    # print (matriz_z_ij)
    
    r_1 = (matriz_x_ij ** 2 + matriz_z_ij ** 2) ** (0.5)
    r_2 = ((matriz_x_ij - cuerda_i) ** 2 + matriz_z_ij ** 2) ** (0.5)
    theta_1 = np.arctan2(matriz_z_ij, matriz_x_ij)
    theta_2 = np.arctan2(matriz_z_ij, matriz_x_ij - cuerda_i)
    # print (r_1)
    # print (r_2)
    # print (theta_1)
    # print (theta_2)
    
    u_ast_q_ij = np.zeros((N, N)); w_ast_q_ij = np.zeros((N, N)); u_ast_gamma_ij = np.zeros((N, N)); w_ast_gamma_ij = np.zeros((N, N))
    u_q_ij = np.zeros((N, N)); w_q_ij = np.zeros((N, N)); u_gamma_ij = np.zeros((N, N)); w_gamma_ij = np.zeros((N, N))
    for i in range (N):
        for j in range (N):
            u_ast_q_ij[i, j] = (- (1 / (2 * np.pi)) * np.log (r_2[i, j] / r_1[i, j]))
            w_ast_q_ij[i, j] = ((theta_2[i, j] - theta_1[i, j]) / (2 * np.pi))
            u_ast_gamma_ij[i, j] = ((theta_2[i, j] - theta_1[i, j]) / (2 * np.pi))
            w_ast_gamma_ij[i, j] = ((1 / (2 * np.pi)) * np.log (r_2[i][j] / r_1[i][j]))
            if i == j:
                u_ast_q_ij[i, j] = 0; w_ast_q_ij[i, j] = 0.5; u_ast_gamma_ij[i, j] = 0.5; w_ast_gamma_ij[i, j] = 0
            u_q_ij[i, j] = u_ast_q_ij[i, j] * np.cos(theta_i_rad[j]) - w_ast_q_ij[i, j] * np.sin(theta_i_rad[j])
            w_q_ij[i, j] = u_ast_q_ij[i, j] * np.sin(theta_i_rad[j]) + w_ast_q_ij[i, j] * np.cos(theta_i_rad[j])
            u_gamma_ij[i, j] = u_ast_gamma_ij[i, j] * np.cos(theta_i_rad[j]) - w_ast_gamma_ij[i, j] * np.sin(theta_i_rad[j])
            w_gamma_ij[i, j] = u_ast_gamma_ij[i, j] * np.sin(theta_i_rad[j]) + w_ast_gamma_ij[i, j] * np.cos(theta_i_rad[j])
            
    a_ij = np.zeros((N + 1, N + 1)); I = np.zeros((N + 1)); contribucion_gamma_ij = np.zeros((N, N)); contribucion_gamma_ij_N = np.zeros((N, N))
    for i in range (0, N):
        for j in range (0, N):
            a_ij[i, j] = - u_q_ij[i, j] * np.sin(theta_i_rad[i]) + w_q_ij[i, j] * np.cos(theta_i_rad[i])
            contribucion_gamma_ij[i, j] = - u_gamma_ij[i, j] * np.sin(theta_i_rad[i]) + w_gamma_ij[i, j] * np.cos(theta_i_rad[i])
            a_ij[i, N] = sum(contribucion_gamma_ij[i])
            I[i] = - v_inf_normal_i[i]
            a_ij[N, j] = u_q_ij[0, j] * np.cos(theta_i_rad[0]) + w_q_ij[0, j] * np.sin(theta_i_rad[0]) + u_q_ij[N - 1, j] * np.cos(theta_i_rad[N - 1]) + w_q_ij[N - 1, j] * np.sin(theta_i_rad[N - 1])
            contribucion_gamma_ij_N[i, j] = + u_gamma_ij[0, j] * np.cos(theta_i_rad[0]) + w_gamma_ij[0, j] * np.sin(theta_i_rad[0]) + u_gamma_ij[N - 1, j] * np.cos(theta_i_rad[N - 1]) + w_gamma_ij[N - 1, j] * np.sin(theta_i_rad[N - 1])
            a_ij[N,N] = sum(contribucion_gamma_ij_N[N - 1])
            I[N] = - v_infinito * (np.cos(alpha) * np.cos(theta_i_rad[0]) + np.sin(alpha) * np.sin(theta_i_rad[0]) + np.cos(alpha) * np.cos(theta_i_rad[N - 1]) + np.sin(alpha) * np.sin(theta_i_rad[N - 1]))
    # print (a_ij[40])
    # print(I)
    
    q_gamma = np.linalg.solve(a_ij, I)
    q_j = q_gamma[:N]
    gamma = q_gamma[N:]
    # print (γ)
    
    b_ij = np.zeros((N, N +1)); t_i = np.zeros ((N)); contribucion_gamma_ij_b = np.zeros((N, N)); contribucion_gamma_ij_b_N = np.zeros((N, N))
    for i in range (0, N):
        for j in range (0, N):
            b_ij[i, j] = u_q_ij[i, j] * np.cos(theta_i_rad[i]) + w_q_ij[i, j] * np.sin(theta_i_rad[i])
            contribucion_gamma_ij_b[i, j] = u_gamma_ij[i, j] * np.cos(theta_i_rad[i]) + w_gamma_ij[i, j] * np.sin(theta_i_rad[i])
            b_ij[i, N] = sum(contribucion_gamma_ij_b[i])
        t_i[i] = v_inf_tangente_i[i]
    # print (t_i)

    vel_i = np.matmul(b_ij, q_gamma) + t_i 
    Cp_i = 1 - (vel_i / v_infinito) ** 2
    Cl_i = -Cp_i * cuerda_i / 1 * np.cos(theta_i_rad - alpha)
    Cl_total = sum(Cl_i)
    Cm_c4_i = (Cp_i * (x_control_i - 0.25) * np.cos(theta_i_rad) + Cp_i * z_control_i * np.sin(theta_i_rad)) * cuerda_i
    Cm_c4_total = sum(Cm_c4_i)
    Cdp_i = Cp_i * cuerda_i / 1 * np.sin(theta_i_rad - alpha)
    Cdp_total = sum (Cdp_i)
    print ("Paneles con manantiales-torbellino para α = " + str(alpha * 180 / np.pi) + "º")
    print ("Cp mínimo =", min(Cp_i))
    # print (Cp_i)
    print ("Cl = " + str(alpha * 180 / np.pi) +"º =", Cl_total)
    print ("Cm_c4 =", Cm_c4_total)
    print ("Cdp =", Cdp_total)
    print("-" * 60)
    
    
    plt.figure(figsize=(16, 4))
    plt.figure(15)
    plt.plot(x_perfil, altura_perfil, linestyle ="-", markersize = 2, color = "blue", label = "Contorno del perfil")
    plt.plot(x_control_i, z_control_i, marker = "o", linestyle="none", markersize = 3, color = "red", label = "Punto de control")
    plt.axis("equal"); plt.grid(True, linestyle='--', alpha=0.5); plt.xlabel("x/c"); plt.ylabel("z/c"); plt.title("División en " + str(N) + " paneles"); plt.legend()
    
    paneles = []
    for i in range (1, N + 1):
        paneles.append(i)
    
    plt.figure(16)
    plt.plot (paneles,r_1[11], linestyle ="-", markersize = 3, color = "blue", marker = "o", label = "r1")
    plt.plot (paneles,r_2[11], linestyle ="-", markersize = 3, color = "red", marker = "o", label = "r2")
    plt.grid(True, linestyle='--', alpha=0.5); plt.xlabel("Panel j"); plt.title("r" + str(11) +" en coordenadas del panel j para " +str(N) + "paneles"); plt.legend()
    
    plt.figure(17)
    plt.plot (paneles,theta_1[11], linestyle ="-", markersize = 3, color = "blue", marker = "o", label = "θ1")
    plt.plot (paneles,theta_2[11], linestyle ="-", markersize = 3, color = "red", marker = "o", label = "θ2")
    plt.grid(True, linestyle='--', alpha=0.5); plt.xlabel("Panel j"); plt.title("θ" + str(11) +" en coordenadas del panel j para " +str(N) + "paneles"); plt.legend()
    
    plt.figure(18)
    plt.plot(x_control_i, q_j, marker = "o", markersize = 3, markerfacecolor = "red", markeredgecolor="red", linestyle ="-", label = "Punto de control", color = "blue")
    plt.grid(True, linestyle='--', alpha=0.5); plt.xlabel("x/c"); plt.ylabel("q-j"); plt.title("Intensidad de manantial para α = " + str(alpha * 180 / np.pi) + "º con " + str(N) + " paneles"); plt.legend()
    
    plt.figure(19)
    plt.plot(x_control_i, Cp_i, marker = "o",  markersize = 3, markerfacecolor = "red", markeredgecolor="red", linestyle ="-", label = "Punto de control", color = "blue")
    plt.grid(True, linestyle='--', alpha=0.5); plt.gca().invert_yaxis(); plt.xlabel("x/c"); plt.ylabel("Cp"); plt.title("Cp del perfil para α = " + str(alpha * 180 / np.pi) + "º con " + str(N) + " paneles"); plt.legend()
    
    plt.figure(20)
    plt.plot(x_control_i, Cl_i, marker = "o",  markersize = 3, markerfacecolor = "red", markeredgecolor="red", linestyle ="-", label = "Punto de control", color = "blue")
    plt.grid(True, linestyle='--', alpha=0.5); plt.xlabel("x/c"); plt.ylabel("Cl"); plt.title("Cl del perfil para α = " + str(alpha * 180 / np.pi) + "º con " + str(N) + " paneles"); plt.legend()
    
    plt.figure(21)
    plt.plot(x_control_i, Cm_c4_i, marker = "o",  markersize = 3, markerfacecolor = "red", markeredgecolor="red", linestyle ="-", label = "Punto de control", color = "blue")
    plt.grid(True, linestyle='--', alpha=0.5); plt.xlabel("x/c"); plt.ylabel("Cmc/4"); plt.title("Cmc/4 del perfil para α = " + str(alpha * 180 / np.pi) + "º con " + str(N) + " paneles"); plt.legend()
    
    plt.figure(22)
    plt.plot(x_control_i, Cdp_i, marker = "o",  markersize = 3, markerfacecolor = "red", markeredgecolor="red", linestyle ="-", label = "Punto de control", color = "blue")
    plt.grid(True, linestyle='--', alpha=0.5); plt.xlabel("x/c"); plt.ylabel("Cd"); plt.title("Cd del perfil para α = " + str(alpha * 180 / np.pi) + "º con " + str(N) + " paneles"); plt.legend()
    
    
    return min(Cp_i), Cl_total, alpha * 180 / np.pi

#%%

def Correcciones_compresible (cp_min_incompresible, M_inf, cl_incompresible, alpha):

    def Prandtl_Glauert (M_inf, cp_min_incompresible):
        
        izquierda = (1 / (0.7 * M_inf ** 2)) * (((5 + M_inf ** 2) / 6) ** (3.5) - 1)
        derecha = cp_min_incompresible / ((1 - M_inf ** 2) ** 0.5)

        return izquierda - derecha
    
    def Karman_Tsien ( M_inf, cp_min_incompresible):
        
        izquierda = (1 / (0.7 * M_inf ** 2)) * (((5 + M_inf ** 2) / 6) ** (3.5) - 1)
        derecha = cp_min_incompresible / (((1 - M_inf ** 2) ** 0.5) + (M_inf ** 2 * cp_min_incompresible) / (2 * (1 + ((1 - M_inf ** 2) ** 0.5))))
        
        return izquierda - derecha
    
    print ("Todo para α = " + str(alpha) + "º" +" = α de paneles")
    
    Cp_min_incompresible = cp_min_incompresible
    print ("Cp mínimo incompresible =", cp_min_incompresible)
    print ("Cl incompresible =", cl_incompresible)
    
    M_critico_PG = fsolve(Prandtl_Glauert, 0.9, args=(Cp_min_incompresible))
    print ("Mach crítico por Prandlt-Glauert =", M_critico_PG[0])
    Cp_min_compresible_PG = cp_min_incompresible / ((1 - M_critico_PG ** 2) ** 0.5)
    print ("Cp mínimo compresible corregido por Prandtl-Glauert =", Cp_min_compresible_PG[0])
    Cl_compresible_PG = cl_incompresible / ((1 - M_critico_PG ** 2) ** 0.5)
    print ("Cl compresible corregido por Prandtl-Glauert =", Cl_compresible_PG[0])
    
    M_critico_KT = fsolve(Karman_Tsien, 0.9, args=(Cp_min_incompresible))
    print ("Mach crítico por Karman-Tsien =", M_critico_KT[0])
    Cp_min_compresible_KT = cp_min_incompresible / ((1 - M_critico_KT ** 2) ** 0.5) + (M_critico_KT ** 2 * cp_min_incompresible) / (2 * (1 + ((1 - M_inf ** 2) ** 0.5)))
    print ("Cp mínimo compresible corregido por Karman-Tsien =", Cp_min_compresible_KT[0])
    Cl_Cp_min_compresible_KT = cl_incompresible / (((1 - M_critico_KT ** 2) ** 0.5) + (M_critico_KT ** 2 * cl_incompresible) / (2 * (1 + ((1 - M_critico_KT ** 2) ** 0.5))))
    print ("Cl compresible corregido por Karman-Tsien =", Cl_Cp_min_compresible_KT[0])
    
    return 
#%% Ejecutables

t_perfil, x_f_perfil, f_perfil, x_timon, delta_timon = NACA("ma","ma","ch","51542896","06602082","47587192")
cl_Theodorsen, cl_alpha_Theodorsen, x_Theodorsen, c_p_Theodorsen = Theodorsen(0, t_perfil)
A_n, A_n_timon, A_n_totales, theta_timon = coeficientes_Glauert(x_f_perfil, f_perfil, x_timon, delta_timon, 200)
Cp_TPL_theta_alphaideal, Cp_TPL_theta_alphaideal_timon, Cp_TPL_theta_alpha, Cp_TPL_theta_alpha_timon, Cm_c4_sin = TPL (A_n, A_n_timon, A_n_totales, x_Theodorsen, theta_timon, 10)
a = TPL_Theodorsen (A_n, A_n_timon, cl_alpha_Theodorsen, x_Theodorsen, c_p_Theodorsen, Cp_TPL_theta_alphaideal, Cp_TPL_theta_alphaideal_timon, Cp_TPL_theta_alpha, Cp_TPL_theta_alpha_timon, Cm_c4_sin, 10)
Cp_min_incompresible, Cl_Cp_min_incompresible, alpha_paneles = paneles (1, 0, 140, t_perfil, x_f_perfil, f_perfil, x_timon, delta_timon, "0")
Correcciones_compresible(Cp_min_incompresible, 0.9, Cl_Cp_min_incompresible, alpha_paneles)