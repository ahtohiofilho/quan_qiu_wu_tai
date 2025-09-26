import os
import pygame as pg
import random
import math

lt = 144
at = 89

dic_cores = {
    'Black': (16, 16, 16), 'Midnight Blue': (0, 0, 127), 'Blue': (0, 0, 255),
    'Dark Green': (0, 127, 0), 'Teal': (0, 127, 127), 'Sky Blue': (0, 127, 255),
    'Green': (0, 255, 0), 'Spring Green': (0, 255, 127), 'Cyan': (0, 223, 223),
    'Maroon': (127, 0, 0), 'Purple': (127, 0, 127), 'Violet': (127, 0, 255),
    'Olive': (127, 127, 0), 'Gray': (127, 127, 127), 'Lavender': (127, 127, 255),
    'Chartreuse': (127, 255, 0), 'Light Green': (127, 223, 127), 'Pale Cyan': (127, 255, 255),
    'Red': (234, 33, 37), 'Rose': (255, 0, 127), 'Magenta': (255, 0, 255),
    'Orange': (223, 127, 32), 'Salmon': (255, 127, 127), 'Orchid': (255, 127, 255),
    'Yellow': (255, 255, 0), 'Light Yellow': (255, 255, 127), 'White': (250, 255, 253)
}

basic_color = [
    'Black', 'Midnight Blue', 'Blue', 'Dark Green', 'Teal', 'Sky Blue',
    'Green', 'Spring Green', 'Cyan', 'Maroon', 'Purple', 'Violet',
    'Olive', 'Gray', 'Lavender', 'Chartreuse', 'Light Green', 'Pale Cyan',
    'Red', 'Rose', 'Magenta', 'Orange', 'Salmon', 'Orchid',
    'Yellow', 'Light Yellow', 'White'
]

cores_padrao = {
    'Black': (16, 16, 16), 'Midnight Blue': (0, 0, 127), 'Blue': (0, 0, 255),
    'Dark Green': (0, 127, 0), 'Teal': (0, 127, 127), 'Sky Blue': (0, 127, 255),
    'Green': (0, 255, 0), 'Spring Green': (0, 255, 127), 'Cyan': (0, 223, 223),
    'Maroon': (127, 0, 0), 'Purple': (127, 0, 127), 'Violet': (127, 0, 255),
    'Olive': (127, 127, 0), 'Gray': (127, 127, 127), 'Lavender': (127, 127, 255),
    'Chartreuse': (127, 255, 0), 'Light Green': (127, 223, 127), 'Pale Cyan': (127, 255, 255),
    'Red': (234, 33, 37), 'Rose': (255, 0, 127), 'Magenta': (255, 0, 255),
    'Orange': (223, 127, 32), 'Salmon': (255, 127, 127), 'Orchid': (255, 127, 255),
    'Yellow': (255, 255, 0), 'Light Yellow': (223, 223, 127), 'White': (250, 255, 253)
}


def estrela(surface, color, center, radius):
    points = []
    for i in range(10):
        angle = i * math.pi / 5
        radius_out = radius if i % 2 == 0 else radius / 2
        x = center[0] + radius_out * math.sin(angle)
        y = center[1] - radius_out * math.cos(angle)
        points.append((x, y))

    pg.draw.polygon(surface, color, points)


def franca(name, criar_arquivo=False):
    modalidade = list(range(6))
    random.shuffle(modalidade)
    random.shuffle(modalidade)

    # --- Inicializar superfície apenas se for necessário ---
    superficie = None
    if criar_arquivo:
        superficie = pg.Surface((lt, at))

    if modalidade[0] < 3:
        if modalidade[0] == 1:
            p_cor = dic_cores[name]
            s_cor = cores_padrao[random.choice(basic_color)]
            while s_cor == p_cor:
                s_cor = cores_padrao[random.choice(basic_color)]
            t_cor = cores_padrao[random.choice(basic_color)]
            while t_cor == p_cor or t_cor == s_cor:
                t_cor = cores_padrao[random.choice(basic_color)]
            q_cor = cores_padrao[random.choice(basic_color)]
            while q_cor == p_cor or q_cor == s_cor or q_cor == t_cor:
                q_cor = cores_padrao[random.choice(basic_color)]
            cores = [p_cor, s_cor, t_cor, q_cor]
            random.shuffle(cores)
            random.shuffle(cores)
            if criar_arquivo and superficie:
                superficie.fill(cores[0])
                pg.draw.rect(superficie, cores[1], (0, 0, lt / 3, at))
                pg.draw.rect(superficie, cores[2], (lt / 3, 0, lt / 3, at))
                estrela(superficie, cores[3], (lt / 2, at / 2), lt / 9)
        elif modalidade[0] == 2:
            p_cor = dic_cores[name]
            s_cor = cores_padrao[random.choice(basic_color)]
            while s_cor == p_cor:
                s_cor = cores_padrao[random.choice(basic_color)]
            t_cor = cores_padrao[random.choice(basic_color)]
            while t_cor == p_cor or t_cor == s_cor:
                t_cor = cores_padrao[random.choice(basic_color)]
            cores = [p_cor, s_cor, t_cor]
            random.shuffle(cores)
            random.shuffle(cores)
            if criar_arquivo and superficie:
                superficie.fill(cores[0])
                pg.draw.rect(superficie, cores[1], (0, 0, lt / 3, at))
                pg.draw.rect(superficie, cores[2], (lt / 3, 0, lt / 3, at))
                estrela(superficie, cores[1], (lt / 2, at / 2), lt / 9)
        else:
            p_cor = dic_cores[name]
            s_cor = cores_padrao[random.choice(basic_color)]
            while s_cor == p_cor:
                s_cor = cores_padrao[random.choice(basic_color)]
            t_cor = cores_padrao[random.choice(basic_color)]
            while t_cor == p_cor or t_cor == s_cor:
                t_cor = cores_padrao[random.choice(basic_color)]
            cores = [p_cor, s_cor, t_cor]
            random.shuffle(cores)
            random.shuffle(cores)
            if criar_arquivo and superficie:
                superficie.fill(cores[0])
                pg.draw.rect(superficie, cores[1], (0, 0, lt / 3, at))
                pg.draw.rect(superficie, cores[2], (lt / 3, 0, lt / 3, at))
    else:
        if modalidade[0] == 4:
            p_cor = dic_cores[name]
            s_cor = cores_padrao[random.choice(basic_color)]
            while s_cor == p_cor:
                s_cor = cores_padrao[random.choice(basic_color)]
            cores = [p_cor, s_cor]
            random.shuffle(cores)
            random.shuffle(cores)
            if criar_arquivo and superficie:
                superficie.fill(cores[0])
                pg.draw.rect(superficie, cores[1], (lt / 3, 0, lt / 3, at))
                estrela(superficie, cores[0], (lt / 2, at / 2), lt / 9)
        elif modalidade[0] == 5:
            p_cor = dic_cores[name]
            s_cor = cores_padrao[random.choice(basic_color)]
            while s_cor == p_cor:
                s_cor = cores_padrao[random.choice(basic_color)]
            t_cor = cores_padrao[random.choice(basic_color)]
            while t_cor == p_cor or t_cor == s_cor:
                t_cor = cores_padrao[random.choice(basic_color)]
            cores = [p_cor, s_cor, t_cor]
            random.shuffle(cores)
            random.shuffle(cores)
            if criar_arquivo and superficie:
                superficie.fill(cores[0])
                pg.draw.rect(superficie, cores[1], (lt / 3, 0, lt / 3, at))
                estrela(superficie, cores[2], (lt / 2, at / 2), lt / 9)
        else:
            p_cor = dic_cores[name]
            s_cor = cores_padrao[random.choice(basic_color)]
            while s_cor == p_cor:
                s_cor = cores_padrao[random.choice(basic_color)]
            cores = [p_cor, s_cor]
            random.shuffle(cores)
            random.shuffle(cores)
            if criar_arquivo and superficie:
                superficie.fill(cores[0])
                pg.draw.rect(superficie, cores[1], (lt / 3, 0, lt / 3, at))

    # --- Salvar a imagem apenas se criar_arquivo for True ---
    if criar_arquivo and superficie:
        # --- Definir o caminho para a pasta assets/flags ---
        nome_arquivo = f"bandeira_{name}_franca.png" # Nome do arquivo pode ser personalizado
        caminho_pasta_flags = "assets/flags"
        caminho_completo = os.path.join(caminho_pasta_flags, nome_arquivo)

        # --- Salvar a imagem ---
        pg.image.save(superficie, caminho_completo)
        print(f"🖼️ Bandeira 'franca' salva em: {caminho_completo}") # Mensagem de confirmação (opcional)

    return cores


def alemanha(name, criar_arquivo=False):
    modalidade = list(range(6))
    random.shuffle(modalidade)
    random.shuffle(modalidade)

    # --- Inicializar superfície apenas se for necessário ---
    superficie = None
    if criar_arquivo:
        superficie = pg.Surface((lt, at))

    if modalidade[0] < 3:
        if modalidade[0] == 1:
            p_cor = dic_cores[name]
            s_cor = cores_padrao[random.choice(basic_color)]
            while s_cor == p_cor:
                s_cor = cores_padrao[random.choice(basic_color)]
            t_cor = cores_padrao[random.choice(basic_color)]
            while t_cor == p_cor or t_cor == s_cor:
                t_cor = cores_padrao[random.choice(basic_color)]
            q_cor = cores_padrao[random.choice(basic_color)]
            while q_cor == p_cor or q_cor == s_cor or q_cor == t_cor:
                q_cor = cores_padrao[random.choice(basic_color)]
            cores = [p_cor, s_cor, t_cor, q_cor]
            random.shuffle(cores)
            random.shuffle(cores)
            if criar_arquivo and superficie:
                superficie.fill(cores[0])
                pg.draw.rect(superficie, cores[1], (0, 0, lt, at / 3))
                pg.draw.rect(superficie, cores[2], (0, at / 3, lt, at / 3))
                estrela(superficie, cores[3], (lt / 2, at / 2), lt / 6)
        elif modalidade[0] == 2:
            p_cor = dic_cores[name]
            s_cor = cores_padrao[random.choice(basic_color)]
            while s_cor == p_cor:
                s_cor = cores_padrao[random.choice(basic_color)]
            t_cor = cores_padrao[random.choice(basic_color)]
            while t_cor == p_cor or t_cor == s_cor:
                t_cor = cores_padrao[random.choice(basic_color)]
            cores = [p_cor, s_cor, t_cor]
            random.shuffle(cores)
            random.shuffle(cores)
            if criar_arquivo and superficie:
                superficie.fill(cores[0])
                pg.draw.rect(superficie, cores[1], (0, 0, lt, at / 3))
                pg.draw.rect(superficie, cores[2], (0, at / 3, lt, at / 3))
                estrela(superficie, cores[1], (lt / 2, at / 2), lt / 12)
        else:
            p_cor = dic_cores[name]
            s_cor = cores_padrao[random.choice(basic_color)]
            while s_cor == p_cor:
                s_cor = cores_padrao[random.choice(basic_color)]
            t_cor = cores_padrao[random.choice(basic_color)]
            while t_cor == p_cor or t_cor == s_cor:
                t_cor = cores_padrao[random.choice(basic_color)]
            cores = [p_cor, s_cor, t_cor]
            random.shuffle(cores)
            random.shuffle(cores)
            if criar_arquivo and superficie:
                superficie.fill(cores[0])
                pg.draw.rect(superficie, cores[1], (0, 0, lt, at / 3))
                pg.draw.rect(superficie, cores[2], (0, at / 3, lt, at / 3))
    else:
        if modalidade[0] == 4:
            p_cor = dic_cores[name]
            s_cor = cores_padrao[random.choice(basic_color)]
            while s_cor == p_cor:
                s_cor = cores_padrao[random.choice(basic_color)]
            cores = [p_cor, s_cor]
            random.shuffle(cores)
            random.shuffle(cores)
            if criar_arquivo and superficie:
                superficie.fill(cores[0])
                pg.draw.rect(superficie, cores[1], (0, at / 3, lt, at / 3))
                estrela(superficie, cores[0], (lt / 2, at / 2), lt / 12)
        elif modalidade[0] == 5:
            p_cor = dic_cores[name]
            s_cor = cores_padrao[random.choice(basic_color)]
            while s_cor == p_cor:
                s_cor = cores_padrao[random.choice(basic_color)]
            t_cor = cores_padrao[random.choice(basic_color)]
            while t_cor == p_cor or t_cor == s_cor:
                t_cor = cores_padrao[random.choice(basic_color)]
            cores = [p_cor, s_cor, t_cor]
            random.shuffle(cores)
            random.shuffle(cores)
            if criar_arquivo and superficie:
                superficie.fill(cores[0])
                pg.draw.rect(superficie, cores[1], (0, at / 3, lt, at / 3))
                estrela(superficie, cores[2], (lt / 2, at / 2), lt / 6)
        else:
            p_cor = dic_cores[name]
            s_cor = cores_padrao[random.choice(basic_color)]
            while s_cor == p_cor:
                s_cor = cores_padrao[random.choice(basic_color)]
            cores = [p_cor, s_cor]
            random.shuffle(cores)
            random.shuffle(cores)
            if criar_arquivo and superficie:
                superficie.fill(cores[0])
                pg.draw.rect(superficie, cores[1], (0, at / 3, lt, at / 3))

    # --- Salvar a imagem apenas se criar_arquivo for True ---
    if criar_arquivo and superficie:
        # --- Definir o caminho para a pasta assets/flags ---
        nome_arquivo = f"bandeira_{name}_alemanha.png" # Nome do arquivo pode ser personalizado
        caminho_pasta_flags = "assets/flags"
        caminho_completo = os.path.join(caminho_pasta_flags, nome_arquivo)

        # --- Salvar a imagem ---
        pg.image.save(superficie, caminho_completo)
        print(f"🖼️ Bandeira 'alemanha' salva em: {caminho_completo}") # Mensagem de confirmação (opcional)

    return cores


def indonesia(name, criar_arquivo=False):
    modalidade = list(range(2))
    random.shuffle(modalidade)
    random.shuffle(modalidade)

    # --- Inicializar superfície apenas se for necessário ---
    superficie = None
    if criar_arquivo:
        superficie = pg.Surface((lt, at))

    if modalidade[0] == 1:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        t_cor = cores_padrao[random.choice(basic_color)]
        while t_cor == p_cor or t_cor == s_cor:
            t_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor, t_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, 0, lt, at / 2))
            estrela(superficie, cores[2], (lt / 2, at / 2), lt / 6)
    else:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, 0, lt, at / 2))

    # --- Salvar a imagem apenas se criar_arquivo for True ---
    if criar_arquivo and superficie:
        # --- Definir o caminho para a pasta assets/flags ---
        nome_arquivo = f"bandeira_{name}_indonesia.png" # Nome do arquivo pode ser personalizado
        caminho_pasta_flags = "assets/flags"
        caminho_completo = os.path.join(caminho_pasta_flags, nome_arquivo)

        # --- Salvar a imagem ---
        pg.image.save(superficie, caminho_completo)
        print(f"🖼️ Bandeira 'indonesia' salva em: {caminho_completo}") # Mensagem de confirmação (opcional)

    return cores


def argelia(name, criar_arquivo=False):
    modalidade = list(range(2))
    random.shuffle(modalidade)
    random.shuffle(modalidade)

    # --- Inicializar superfície apenas se for necessário ---
    superficie = None
    if criar_arquivo:
        superficie = pg.Surface((lt, at))

    if modalidade[0] == 1:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        t_cor = cores_padrao[random.choice(basic_color)]
        while t_cor == p_cor or t_cor == s_cor:
            t_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor, t_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, 0, lt / 2, at))
            estrela(superficie, cores[2], (lt / 2, at / 2), lt / 6)
    else:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, 0, lt / 2, at))

    # --- Salvar a imagem apenas se criar_arquivo for True ---
    if criar_arquivo and superficie:
        # --- Definir o caminho para a pasta assets/flags ---
        nome_arquivo = f"bandeira_{name}_argelia.png" # Nome do arquivo pode ser personalizado
        caminho_pasta_flags = "assets/flags"
        caminho_completo = os.path.join(caminho_pasta_flags, nome_arquivo)

        # --- Salvar a imagem ---
        pg.image.save(superficie, caminho_completo)
        print(f"🖼️ Bandeira 'argelia' salva em: {caminho_completo}") # Mensagem de confirmação (opcional)

    return cores


def japao(name, criar_arquivo=False):
    p_cor = dic_cores[name]
    s_cor = cores_padrao[random.choice(basic_color)]
    while s_cor == p_cor:
        s_cor = cores_padrao[random.choice(basic_color)]
    cores = [p_cor, s_cor]
    random.shuffle(cores)
    random.shuffle(cores)

    # --- Inicializar superfície apenas se for necessário ---
    superficie = None
    if criar_arquivo:
        superficie = pg.Surface((lt, at))
        superficie.fill(cores[0])
        pg.draw.circle(superficie, cores[1], (lt / 2, at / 2), at / 4)

    # --- Salvar a imagem apenas se criar_arquivo for True ---
    if criar_arquivo and superficie:
        # --- Definir o caminho para a pasta assets/flags ---
        nome_arquivo = f"bandeira_{name}_japao.png" # Nome do arquivo pode ser personalizado
        caminho_pasta_flags = "assets/flags"
        caminho_completo = os.path.join(caminho_pasta_flags, nome_arquivo)

        # --- Salvar a imagem ---
        pg.image.save(superficie, caminho_completo)
        print(f"🖼️ Bandeira 'japao' salva em: {caminho_completo}") # Mensagem de confirmação (opcional)

    return cores


def butao(name, criar_arquivo=False):
    modalidade = list(range(2))
    random.shuffle(modalidade)
    random.shuffle(modalidade)

    # --- Inicializar superfície apenas se for necessário ---
    superficie = None
    if criar_arquivo:
        superficie = pg.Surface((lt, at))

    if modalidade[0] == 1:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        t_cor = cores_padrao[random.choice(basic_color)]
        while t_cor == p_cor or t_cor == s_cor:
            t_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor, t_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            pg.draw.polygon(superficie, cores[1], ((0, at), (lt, 0), (lt, at)))
            estrela(superficie, cores[2], (lt / 2, at / 2), lt / 6)
    else:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            pg.draw.polygon(superficie, cores[1], ((0, at), (lt, 0), (lt, at)))

    # --- Salvar a imagem apenas se criar_arquivo for True ---
    if criar_arquivo and superficie:
        # --- Definir o caminho para a pasta assets/flags ---
        nome_arquivo = f"bandeira_{name}_butao.png" # Nome do arquivo pode ser personalizado
        caminho_pasta_flags = "assets/flags"
        caminho_completo = os.path.join(caminho_pasta_flags, nome_arquivo)

        # --- Salvar a imagem ---
        pg.image.save(superficie, caminho_completo)
        print(f"🖼️ Bandeira 'butao' salva em: {caminho_completo}") # Mensagem de confirmação (opcional)

    return cores


def butao_invertido(name, criar_arquivo=False):
    modalidade = list(range(2))
    random.shuffle(modalidade)
    random.shuffle(modalidade)

    # --- Inicializar superfície apenas se for necessário ---
    superficie = None
    if criar_arquivo:
        superficie = pg.Surface((lt, at))

    if modalidade[0] == 1:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        t_cor = cores_padrao[random.choice(basic_color)]
        while t_cor == p_cor or t_cor == s_cor:
            t_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor, t_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            pg.draw.polygon(superficie, cores[1], ((0, 0), (lt, at), (0, at)))
            estrela(superficie, cores[2], (lt / 2, at / 2), lt / 6)
    else:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            pg.draw.polygon(superficie, cores[1], ((0, 0), (lt, at), (0, at)))

    # --- Salvar a imagem apenas se criar_arquivo for True ---
    if criar_arquivo and superficie:
        # --- Definir o caminho para a pasta assets/flags ---
        nome_arquivo = f"bandeira_{name}_butao_invertido.png" # Nome do arquivo pode ser personalizado
        caminho_pasta_flags = "assets/flags"
        caminho_completo = os.path.join(caminho_pasta_flags, nome_arquivo)

        # --- Salvar a imagem ---
        pg.image.save(superficie, caminho_completo)
        print(f"🖼️ Bandeira 'butao_invertido' salva em: {caminho_completo}") # Mensagem de confirmação (opcional)

    return cores


def cuba(name, criar_arquivo=False):
    modalidade = list(range(3))
    random.shuffle(modalidade)
    random.shuffle(modalidade)

    # --- Inicializar superfície apenas se for necessário ---
    superficie = None
    if criar_arquivo:
        superficie = pg.Surface((lt, at))

    if modalidade[0] == 1:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        t_cor = cores_padrao[random.choice(basic_color)]
        while t_cor == p_cor or t_cor == s_cor:
            t_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor, t_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, at / 5, lt, at / 5))
            pg.draw.rect(superficie, cores[1], (0, (at / 5) * 3, lt, at / 5))
            pg.draw.polygon(superficie, cores[2], ((0, 0), (lt / 3, at / 2), (0, at)))
    elif modalidade[0] == 2:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        t_cor = cores_padrao[random.choice(basic_color)]
        while t_cor == p_cor or t_cor == s_cor:
            t_cor = cores_padrao[random.choice(basic_color)]
        q_cor = cores_padrao[random.choice(basic_color)]
        while q_cor == p_cor or q_cor == s_cor or q_cor == t_cor:
            q_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor, t_cor, q_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, at / 5, lt, at / 5))
            pg.draw.rect(superficie, cores[1], (0, (at / 5) * 3, lt, at / 5))
            pg.draw.polygon(superficie, cores[2], ((0, 0), (lt / 3, at / 2), (0, at)))
            estrela(superficie, cores[3], (lt / 9, at / 2), lt / 9)
    else:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        t_cor = cores_padrao[random.choice(basic_color)]
        while t_cor == p_cor or t_cor == s_cor:
            t_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor, t_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, at / 5, lt, at / 5))
            pg.draw.rect(superficie, cores[1], (0, (at / 5) * 3, lt, at / 5))
            pg.draw.polygon(superficie, cores[2], ((0, 0), (lt / 3, at / 2), (0, at)))
            estrela(superficie, cores[1], (lt / 9, at / 2), lt / 9)

    # --- Salvar a imagem apenas se criar_arquivo for True ---
    if criar_arquivo and superficie:
        # --- Definir o caminho para a pasta assets/flags ---
        nome_arquivo = f"bandeira_{name}_cuba.png" # Nome do arquivo pode ser personalizado
        caminho_pasta_flags = "assets/flags"
        caminho_completo = os.path.join(caminho_pasta_flags, nome_arquivo)

        # --- Salvar a imagem ---
        pg.image.save(superficie, caminho_completo)
        print(f"🖼️ Bandeira 'cuba' salva em: {caminho_completo}") # Mensagem de confirmação (opcional)

    return cores


def jordania(name, criar_arquivo=False):
    modalidade = list(range(4))
    random.shuffle(modalidade)
    random.shuffle(modalidade)

    # --- Inicializar superfície apenas se for necessário ---
    superficie = None
    if criar_arquivo:
        superficie = pg.Surface((lt, at))

    if modalidade[0] < 2:
        if modalidade[0] == 1:
            p_cor = dic_cores[name]
            s_cor = cores_padrao[random.choice(basic_color)]
            while s_cor == p_cor:
                s_cor = cores_padrao[random.choice(basic_color)]
            t_cor = cores_padrao[random.choice(basic_color)]
            while t_cor == p_cor or t_cor == s_cor:
                t_cor = cores_padrao[random.choice(basic_color)]
            q_cor = cores_padrao[random.choice(basic_color)]
            while q_cor == p_cor or q_cor == s_cor or q_cor == t_cor:
                q_cor = cores_padrao[random.choice(basic_color)]
            cores = [p_cor, s_cor, t_cor, q_cor]
            random.shuffle(cores)
            random.shuffle(cores)
            if criar_arquivo and superficie:
                superficie.fill(cores[0])
                pg.draw.rect(superficie, cores[1], (0, 0, lt, at / 3))
                pg.draw.rect(superficie, cores[2], (0, at / 3, lt, at / 3))
                pg.draw.polygon(superficie, cores[3], ((0, 0), (lt / 3, at / 2), (0, at)))
                estrela(superficie, cores[2], (lt / 8.81, at / 2), lt / 9)
        else:
            p_cor = dic_cores[name]
            s_cor = cores_padrao[random.choice(basic_color)]
            while s_cor == p_cor:
                s_cor = cores_padrao[random.choice(basic_color)]
            t_cor = cores_padrao[random.choice(basic_color)]
            while t_cor == p_cor or t_cor == s_cor:
                t_cor = cores_padrao[random.choice(basic_color)]
            q_cor = cores_padrao[random.choice(basic_color)]
            while q_cor == p_cor or q_cor == s_cor or q_cor == t_cor:
                q_cor = cores_padrao[random.choice(basic_color)]
            cores = [p_cor, s_cor, t_cor, q_cor]
            random.shuffle(cores)
            random.shuffle(cores)
            if criar_arquivo and superficie:
                superficie.fill(cores[0])
                pg.draw.rect(superficie, cores[1], (0, 0, lt, at / 3))
                pg.draw.rect(superficie, cores[2], (0, at / 3, lt, at / 3))
                pg.draw.polygon(superficie, cores[3], ((0, 0), (lt / 3, at / 2), (0, at)))
    else:
        if modalidade[0] == 3:
            p_cor = dic_cores[name]
            s_cor = cores_padrao[random.choice(basic_color)]
            while s_cor == p_cor:
                s_cor = cores_padrao[random.choice(basic_color)]
            t_cor = cores_padrao[random.choice(basic_color)]
            while t_cor == p_cor or t_cor == s_cor:
                t_cor = cores_padrao[random.choice(basic_color)]
            cores = [p_cor, s_cor, t_cor]
            random.shuffle(cores)
            random.shuffle(cores)
            if criar_arquivo and superficie:
                superficie.fill(cores[0])
                pg.draw.rect(superficie, cores[1], (0, at / 3, lt, at / 3))
                pg.draw.polygon(superficie, cores[2], ((0, 0), (lt / 3, at / 2), (0, at)))
                estrela(superficie, cores[1], (lt / 8.81, at / 2), lt / 9)
        else:
            p_cor = dic_cores[name]
            s_cor = cores_padrao[random.choice(basic_color)]
            while s_cor == p_cor:
                s_cor = cores_padrao[random.choice(basic_color)]
            t_cor = cores_padrao[random.choice(basic_color)]
            while t_cor == p_cor or t_cor == s_cor:
                t_cor = cores_padrao[random.choice(basic_color)]
            cores = [p_cor, s_cor, t_cor]
            random.shuffle(cores)
            random.shuffle(cores)
            if criar_arquivo and superficie:
                superficie.fill(cores[0])
                pg.draw.rect(superficie, cores[1], (0, at / 3, lt, at / 3))
                pg.draw.polygon(superficie, cores[2], ((0, 0), (lt / 3, at / 2), (0, at)))

    # --- Salvar a imagem apenas se criar_arquivo for True ---
    if criar_arquivo and superficie:
        # --- Definir o caminho para a pasta assets/flags ---
        nome_arquivo = f"bandeira_{name}_jordania.png" # Nome do arquivo pode ser personalizado
        caminho_pasta_flags = "assets/flags"
        caminho_completo = os.path.join(caminho_pasta_flags, nome_arquivo)

        # --- Salvar a imagem ---
        pg.image.save(superficie, caminho_completo)
        print(f"🖼️ Bandeira 'jordania' salva em: {caminho_completo}") # Mensagem de confirmação (opcional)

    return cores


def madagascar(name, criar_arquivo=False):
    modalidade = list(range(3))
    random.shuffle(modalidade)
    random.shuffle(modalidade)

    # --- Inicializar superfície apenas se for necessário ---
    superficie = None
    if criar_arquivo:
        superficie = pg.Surface((lt, at))

    if modalidade[0] < 2:
        if modalidade[0] == 1:
            p_cor = dic_cores[name]
            s_cor = cores_padrao[random.choice(basic_color)]
            while s_cor == p_cor:
                s_cor = cores_padrao[random.choice(basic_color)]
            t_cor = cores_padrao[random.choice(basic_color)]
            while t_cor == p_cor or t_cor == s_cor:
                t_cor = cores_padrao[random.choice(basic_color)]
            cores = [p_cor, s_cor, t_cor]
            random.shuffle(cores)
            random.shuffle(cores)
            if criar_arquivo and superficie:
                superficie.fill(cores[0])
                pg.draw.rect(superficie, cores[1], (0, 0, lt / 3, at))
                pg.draw.rect(superficie, cores[2], (lt / 3, 0, lt * 2 / 3, at / 2))
                estrela(superficie, cores[2], (lt / 6, at / 2), lt / 9)
        else:
            p_cor = dic_cores[name]
            s_cor = cores_padrao[random.choice(basic_color)]
            while s_cor == p_cor:
                s_cor = cores_padrao[random.choice(basic_color)]
            t_cor = cores_padrao[random.choice(basic_color)]
            while t_cor == p_cor or t_cor == s_cor:
                t_cor = cores_padrao[random.choice(basic_color)]
            cores = [p_cor, s_cor, t_cor]
            random.shuffle(cores)
            random.shuffle(cores)
            if criar_arquivo and superficie:
                superficie.fill(cores[0])
                pg.draw.rect(superficie, cores[1], (0, 0, lt / 3, at))
                pg.draw.rect(superficie, cores[2], (lt / 3, 0, lt * 2 / 3, at / 2))
    else:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        t_cor = cores_padrao[random.choice(basic_color)]
        while t_cor == p_cor or t_cor == s_cor:
            t_cor = cores_padrao[random.choice(basic_color)]
        q_cor = cores_padrao[random.choice(basic_color)]
        while q_cor == p_cor or q_cor == s_cor:
            q_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor, t_cor, q_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, 0, lt / 3, at))
            pg.draw.rect(superficie, cores[2], (lt / 3, 0, lt * 2 / 3, at / 2))
            estrela(superficie, cores[3], (lt / 6, at / 2), lt / 9)

    # --- Salvar a imagem apenas se criar_arquivo for True ---
    if criar_arquivo and superficie:
        # --- Definir o caminho para a pasta assets/flags ---
        nome_arquivo = f"bandeira_{name}_madagascar.png" # Nome do arquivo pode ser personalizado
        caminho_pasta_flags = "assets/flags"
        caminho_completo = os.path.join(caminho_pasta_flags, nome_arquivo)

        # --- Salvar a imagem ---
        pg.image.save(superficie, caminho_completo)
        print(f"🖼️ Bandeira 'madagascar' salva em: {caminho_completo}") # Mensagem de confirmação (opcional)

    return cores


def jamaica(name, criar_arquivo=False):
    modalidade = list(range(2))
    random.shuffle(modalidade)
    random.shuffle(modalidade)

    # --- Inicializar superfície apenas se for necessário ---
    superficie = None
    if criar_arquivo:
        superficie = pg.Surface((lt, at))

    if modalidade[0] == 1:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            pg.draw.polygon(superficie, cores[1], ((0, lt / 12), (lt / 2 - lt / 6, at / 2), (0, at - lt / 12)))
            pg.draw.polygon(superficie, cores[1], ((lt / 6, 0), (lt - lt / 6, 0), (lt / 2, at / 2 - lt / 12)))
            pg.draw.polygon(superficie, cores[1], ((lt, lt / 12), (lt / 2 + lt / 6, at / 2), (lt, at - lt / 12)))
            pg.draw.polygon(superficie, cores[1], ((lt / 6, at), (lt - lt / 6, at), (lt / 2, at / 2 + lt / 12)))
    else:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        t_cor = cores_padrao[random.choice(basic_color)]
        while t_cor == p_cor or t_cor == s_cor:
            t_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor, t_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            pg.draw.polygon(superficie, cores[1], ((0, lt / 12), (lt / 2 - lt / 6, at / 2), (0, at - lt / 12)))
            pg.draw.polygon(superficie, cores[2], ((lt / 6, 0), (lt - lt / 6, 0), (lt / 2, at / 2 - lt / 12)))
            pg.draw.polygon(superficie, cores[1], ((lt, lt / 12), (lt / 2 + lt / 6, at / 2), (lt, at - lt / 12)))
            pg.draw.polygon(superficie, cores[2], ((lt / 6, at), (lt - lt / 6, at), (lt / 2, at / 2 + lt / 12)))

    # --- Salvar a imagem apenas se criar_arquivo for True ---
    if criar_arquivo and superficie:
        # --- Definir o caminho para a pasta assets/flags ---
        nome_arquivo = f"bandeira_{name}_jamaica.png" # Nome do arquivo pode ser personalizado
        caminho_pasta_flags = "assets/flags"
        caminho_completo = os.path.join(caminho_pasta_flags, nome_arquivo)

        # --- Salvar a imagem ---
        pg.image.save(superficie, caminho_completo)
        print(f"🖼️ Bandeira 'jamaica' salva em: {caminho_completo}") # Mensagem de confirmação (opcional)

    return cores


def suecia(name, criar_arquivo=False):
    p_cor = dic_cores[name]
    s_cor = cores_padrao[random.choice(basic_color)]
    while s_cor == p_cor:
        s_cor = cores_padrao[random.choice(basic_color)]
    cores = [p_cor, s_cor]
    random.shuffle(cores)
    random.shuffle(cores)

    # --- Inicializar superfície apenas se for necessário ---
    superficie = None
    if criar_arquivo:
        superficie = pg.Surface((lt, at))
        l1 = 0
        l2 = lt / 3 - lt / 12
        l3 = lt / 3 + lt / 12
        l4 = lt
        a1 = 0
        a2 = at / 2 - lt / 12
        a3 = at / 2 + lt / 12
        a4 = at
        superficie.fill(cores[0])
        pg.draw.polygon(superficie, cores[1], ((l1, a2), (l2, a2), (l2, a1), (l3, a1), (l3, a2), (l4, a2), (l4, a3),
                                               (l3, a3), (l3, a4), (l2, a4), (l2, a3), (l1, a3)))

    # --- Salvar a imagem apenas se criar_arquivo for True ---
    if criar_arquivo and superficie:
        # --- Definir o caminho para a pasta assets/flags ---
        nome_arquivo = f"bandeira_{name}_suecia.png" # Nome do arquivo pode ser personalizado
        caminho_pasta_flags = "assets/flags"
        caminho_completo = os.path.join(caminho_pasta_flags, nome_arquivo)

        # --- Salvar a imagem ---
        pg.image.save(superficie, caminho_completo)
        print(f"🖼️ Bandeira 'suecia' salva em: {caminho_completo}") # Mensagem de confirmação (opcional)

    return cores


def china(name, criar_arquivo=False):
    modalidade = list(range(2))
    random.shuffle(modalidade)
    random.shuffle(modalidade)

    # --- Inicializar superfície apenas se for necessário ---
    superficie = None
    if criar_arquivo:
        superficie = pg.Surface((lt, at))

    if modalidade[0] == 1:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            estrela(superficie, cores[1], (lt / 2, at / 2), lt / 6)
    else:
        p_cor = dic_cores[name]
        cores = [p_cor]
        if criar_arquivo and superficie:
            superficie.fill(p_cor)

    # --- Salvar a imagem apenas se criar_arquivo for True ---
    if criar_arquivo and superficie:
        # --- Definir o caminho para a pasta assets/flags ---
        nome_arquivo = f"bandeira_{name}_china.png" # Nome do arquivo pode ser personalizado
        caminho_pasta_flags = "assets/flags"
        caminho_completo = os.path.join(caminho_pasta_flags, nome_arquivo)

        # --- Salvar a imagem ---
        pg.image.save(superficie, caminho_completo)
        print(f"🖼️ Bandeira 'china' salva em: {caminho_completo}") # Mensagem de confirmação (opcional)

    return cores


def samoa(name, criar_arquivo=False):
    modalidade = list(range(2))
    random.shuffle(modalidade)
    random.shuffle(modalidade)

    # --- Inicializar superfície apenas se for necessário ---
    superficie = None
    if criar_arquivo:
        superficie = pg.Surface((lt, at))

    if modalidade[0] == 1:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        t_cor = cores_padrao[random.choice(basic_color)]
        while t_cor == p_cor or t_cor == s_cor:
            t_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor, t_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, 0, lt / 4, lt / 4))
            estrela(superficie, cores[2], (lt / 8, lt / 8), lt / 12)
    else:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, 0, lt / 4, lt / 4))

    # --- Salvar a imagem apenas se criar_arquivo for True ---
    if criar_arquivo and superficie:
        # --- Definir o caminho para a pasta assets/flags ---
        nome_arquivo = f"bandeira_{name}_samo.png" # Nome do arquivo pode ser personalizado
        caminho_pasta_flags = "assets/flags"
        caminho_completo = os.path.join(caminho_pasta_flags, nome_arquivo)

        # --- Salvar a imagem ---
        pg.image.save(superficie, caminho_completo)
        print(f"🖼️ Bandeira 'samo' salva em: {caminho_completo}") # Mensagem de confirmação (opcional)

    return cores


def eua(name, criar_arquivo=False):
    modalidade = list(range(5))
    random.shuffle(modalidade)
    random.shuffle(modalidade)

    # --- Inicializar superfície apenas se for necessário ---
    superficie = None
    if criar_arquivo:
        superficie = pg.Surface((lt, at))

    if modalidade[0] == 0:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        t_cor = cores_padrao[random.choice(basic_color)]
        while t_cor == p_cor or t_cor == s_cor:
            t_cor = cores_padrao[random.choice(basic_color)]
        q_cor = cores_padrao[random.choice(basic_color)]
        while q_cor == p_cor or q_cor == s_cor:
            q_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor, t_cor, q_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, at / 7, lt, at / 7))
            pg.draw.rect(superficie, cores[1], (0, at * 3 / 7, lt, at / 7))
            pg.draw.rect(superficie, cores[1], (0, at * 5 / 7, lt, at / 7))
            pg.draw.rect(superficie, cores[2], (0, 0, at * 3 / 7, at * 3 / 7))
            estrela(superficie, cores[3], (at * 3 / 14, at * 3 / 14), at / 7)
    elif modalidade[0] == 1:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        t_cor = cores_padrao[random.choice(basic_color)]
        while t_cor == p_cor or t_cor == s_cor:
            t_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor, t_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, at / 7, lt, at / 7))
            pg.draw.rect(superficie, cores[1], (0, at * 3 / 7, lt, at / 7))
            pg.draw.rect(superficie, cores[1], (0, at * 5 / 7, lt, at / 7))
            pg.draw.rect(superficie, cores[2], (0, 0, at * 3 / 7, at * 3 / 7))
            estrela(superficie, cores[1], (at * 3 / 14, at * 3 / 14), at / 7)
    elif modalidade[0] == 2:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        t_cor = cores_padrao[random.choice(basic_color)]
        while t_cor == p_cor or t_cor == s_cor:
            t_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor, t_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, at / 7, lt, at / 7))
            pg.draw.rect(superficie, cores[1], (0, at * 3 / 7, lt, at / 7))
            pg.draw.rect(superficie, cores[1], (0, at * 5 / 7, lt, at / 7))
            pg.draw.rect(superficie, cores[2], (0, 0, at * 3 / 7, at * 3 / 7))
    elif modalidade[0] == 3:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        t_cor = cores_padrao[random.choice(basic_color)]
        while t_cor == p_cor or t_cor == s_cor:
            t_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor, t_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, at / 7, lt, at / 7))
            pg.draw.rect(superficie, cores[1], (0, at * 3 / 7, lt, at / 7))
            pg.draw.rect(superficie, cores[1], (0, at * 5 / 7, lt, at / 7))
            pg.draw.rect(superficie, cores[0], (0, 0, at * 3 / 7, at * 3 / 7))
            estrela(superficie, cores[2], (at * 3 / 14, at * 3 / 14), at / 7)
    else: # modalidade[0] == 4
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, at / 7, lt, at / 7))
            pg.draw.rect(superficie, cores[1], (0, at * 3 / 7, lt, at / 7))
            pg.draw.rect(superficie, cores[1], (0, at * 5 / 7, lt, at / 7))
            pg.draw.rect(superficie, cores[0], (0, 0, at * 3 / 7, at * 3 / 7))

    # --- Salvar a imagem apenas se criar_arquivo for True ---
    if criar_arquivo and superficie:
        # --- Definir o caminho para a pasta assets/flags ---
        nome_arquivo = f"bandeira_{name}_eua.png" # Nome do arquivo pode ser personalizado
        caminho_pasta_flags = "assets/flags"
        caminho_completo = os.path.join(caminho_pasta_flags, nome_arquivo)

        # --- Salvar a imagem ---
        pg.image.save(superficie, caminho_completo)
        print(f"🖼️ Bandeira 'eua' salva em: {caminho_completo}") # Mensagem de confirmação (opcional)

    return cores


def tanzania(name, criar_arquivo=False):
    modalidade = list(range(4))
    random.shuffle(modalidade)
    random.shuffle(modalidade)

    # --- Inicializar superfície apenas se for necessário ---
    superficie = None
    if criar_arquivo:
        superficie = pg.Surface((lt, at))

    if modalidade[0] == 0:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        t_cor = cores_padrao[random.choice(basic_color)]
        while t_cor == p_cor or t_cor == s_cor:
            t_cor = cores_padrao[random.choice(basic_color)]
        q_cor = cores_padrao[random.choice(basic_color)]
        while q_cor == p_cor or q_cor == s_cor or q_cor == t_cor:
            q_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor, t_cor, q_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            pg.draw.polygon(superficie, cores[1], ((0, 0), (lt - lt / 6, 0), (0, at - lt / 12)))
            pg.draw.polygon(superficie, cores[2], ((lt / 6, at), (lt, lt / 12), (lt, at)))
            estrela(superficie, cores[3], (lt / 5, at / 4), at / 6)
    elif modalidade[0] == 1:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        t_cor = cores_padrao[random.choice(basic_color)]
        while t_cor == p_cor or t_cor == s_cor:
            t_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor, t_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            pg.draw.polygon(superficie, cores[1], ((0, 0), (lt - lt / 6, 0), (0, at - lt / 12)))
            pg.draw.polygon(superficie, cores[1], ((lt / 6, at), (lt, lt / 12), (lt, at)))
            estrela(superficie, cores[2], (lt / 5, at / 4), at / 6)
    elif modalidade[0] == 2:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        t_cor = cores_padrao[random.choice(basic_color)]
        while t_cor == p_cor or t_cor == s_cor:
            t_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor, t_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            pg.draw.polygon(superficie, cores[1], ((0, 0), (lt - lt / 6, 0), (0, at - lt / 12)))
            pg.draw.polygon(superficie, cores[2], ((lt / 6, at), (lt, lt / 12), (lt, at)))
    else: # modalidade[0] == 3
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            pg.draw.polygon(superficie, cores[1], ((0, 0), (lt - lt / 6, 0), (0, at - lt / 12)))
            pg.draw.polygon(superficie, cores[1], ((lt / 6, at), (lt, lt / 12), (lt, at)))

    # --- Salvar a imagem apenas se criar_arquivo for True ---
    if criar_arquivo and superficie:
        # --- Definir o caminho para a pasta assets/flags ---
        nome_arquivo = f"bandeira_{name}_tanzania.png" # Nome do arquivo pode ser personalizado
        caminho_pasta_flags = "assets/flags"
        caminho_completo = os.path.join(caminho_pasta_flags, nome_arquivo)

        # --- Salvar a imagem ---
        pg.image.save(superficie, caminho_completo)
        print(f"🖼️ Bandeira 'tanzania' salva em: {caminho_completo}") # Mensagem de confirmação (opcional)

    return cores


def tanzania_invertida(name, criar_arquivo=False):
    modalidade = list(range(4))
    random.shuffle(modalidade)
    random.shuffle(modalidade)

    # --- Inicializar superfície apenas se for necessário ---
    superficie = None
    if criar_arquivo:
        superficie = pg.Surface((lt, at))

    if modalidade[0] == 0:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        t_cor = cores_padrao[random.choice(basic_color)]
        while t_cor == p_cor or t_cor == s_cor:
            t_cor = cores_padrao[random.choice(basic_color)]
        q_cor = cores_padrao[random.choice(basic_color)]
        while q_cor == p_cor or q_cor == s_cor or q_cor == t_cor:
            q_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor, t_cor, q_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            pg.draw.polygon(superficie, cores[1], ((lt / 6, 0), (lt, 0), (lt, at - lt / 12)))
            pg.draw.polygon(superficie, cores[2], ((0, lt / 12), (lt - lt / 6, at), (0, at)))
            estrela(superficie, cores[3], (lt * 4 / 5, at / 4), at / 6)
    elif modalidade[0] == 1:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        t_cor = cores_padrao[random.choice(basic_color)]
        while t_cor == p_cor or t_cor == s_cor:
            t_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor, t_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            pg.draw.polygon(superficie, cores[1], ((lt / 6, 0), (lt, 0), (lt, at - lt / 12)))
            pg.draw.polygon(superficie, cores[2], ((0, lt / 12), (lt - lt / 6, at), (0, at)))
            estrela(superficie, cores[1], (lt * 4 / 5, at / 4), at / 6)
    elif modalidade[0] == 2:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        t_cor = cores_padrao[random.choice(basic_color)]
        while t_cor == p_cor or t_cor == s_cor:
            t_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor, t_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            pg.draw.polygon(superficie, cores[1], ((lt / 6, 0), (lt, 0), (lt, at - lt / 12)))
            pg.draw.polygon(superficie, cores[2], ((0, lt / 12), (lt - lt / 6, at), (0, at)))
    else: # modalidade[0] == 3
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        t_cor = cores_padrao[random.choice(basic_color)]
        while t_cor == p_cor or t_cor == s_cor:
            t_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor, t_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            pg.draw.polygon(superficie, cores[1], ((lt / 6, 0), (lt, 0), (lt, at - lt / 12)))
            pg.draw.polygon(superficie, cores[2], ((0, lt / 12), (lt - lt / 6, at), (0, at)))

    # --- Salvar a imagem apenas se criar_arquivo for True ---
    if criar_arquivo and superficie:
        # --- Definir o caminho para a pasta assets/flags ---
        nome_arquivo = f"bandeira_{name}_tanzania_invertida.png" # Nome do arquivo pode ser personalizado
        caminho_pasta_flags = "assets/flags"
        caminho_completo = os.path.join(caminho_pasta_flags, nome_arquivo)

        # --- Salvar a imagem ---
        pg.image.save(superficie, caminho_completo)
        print(f"🖼️ Bandeira 'tanzania_invertida' salva em: {caminho_completo}") # Mensagem de confirmação (opcional)

    return cores


def republica_dominicana(name, criar_arquivo=False):
    modalidade = list(range(8))
    random.shuffle(modalidade)
    random.shuffle(modalidade)

    # --- Inicializar superfície apenas se for necessário ---
    superficie = None
    if criar_arquivo:
        superficie = pg.Surface((lt, at))

    a = lt / 2 - lt / 10
    b = lt / 2 + lt / 10
    c = at / 2 - lt / 12
    d = at / 2 + lt / 12

    if modalidade[0] < 2:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        t_cor = cores_padrao[random.choice(basic_color)]
        while t_cor == p_cor or t_cor == s_cor:
            t_cor = cores_padrao[random.choice(basic_color)]
        q_cor = cores_padrao[random.choice(basic_color)]
        while q_cor == p_cor or q_cor == s_cor or q_cor == t_cor:
            q_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor, t_cor, q_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            a = lt / 2 - lt / 10
            b = lt / 2 + lt / 10
            c = at / 2 - lt / 10
            d = at / 2 + lt / 10
            pg.draw.rect(superficie, cores[1], (0, 0, a, c))
            pg.draw.rect(superficie, cores[2], (b, 0, a, c))
            pg.draw.rect(superficie, cores[2], (0, d, a, c))
            pg.draw.rect(superficie, cores[1], (b, d, a, c))
            if modalidade[0] == 0:
                estrela(superficie, cores[3], (a / 2, c / 2), at / 9)
                estrela(superficie, cores[3], (b + a / 2, c / 2), at / 9)
                estrela(superficie, cores[3], (a / 2, d + c / 2), at / 9)
                estrela(superficie, cores[3], (b + a / 2, d + c / 2), at / 9)
            else:
                estrela(superficie, cores[3], (lt / 2, at / 2), at / 6)
    elif modalidade[0] < 6:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        t_cor = cores_padrao[random.choice(basic_color)]
        while t_cor == p_cor or t_cor == s_cor:
            t_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor, t_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            if modalidade[0] == 2:
                pg.draw.rect(superficie, cores[1], (0, 0, a, c))
                pg.draw.rect(superficie, cores[1], (b, 0, a, c))
                pg.draw.rect(superficie, cores[1], (0, d, a, c))
                pg.draw.rect(superficie, cores[1], (b, d, a, c))
                estrela(superficie, cores[2], (a / 2, c / 2), at / 9)
                estrela(superficie, cores[2], (b + a / 2, c / 2), at / 9)
                estrela(superficie, cores[2], (a / 2, d + c / 2), at / 9)
                estrela(superficie, cores[2], (b + a / 2, d + c / 2), at / 9)
            elif modalidade[0] == 3:
                pg.draw.rect(superficie, cores[1], (0, 0, a, c))
                pg.draw.rect(superficie, cores[2], (b, 0, a, c))
                pg.draw.rect(superficie, cores[2], (0, d, a, c))
                pg.draw.rect(superficie, cores[1], (b, d, a, c))
            elif modalidade[0] == 4:
                pg.draw.rect(superficie, cores[1], (0, 0, a, c))
                pg.draw.rect(superficie, cores[1], (b, 0, a, c))
                pg.draw.rect(superficie, cores[1], (0, d, a, c))
                pg.draw.rect(superficie, cores[1], (b, d, a, c))
                estrela(superficie, cores[2], (lt / 2, at / 2), at / 6)
            else: # modalidade[0] == 5
                pg.draw.rect(superficie, cores[1], (0, 0, a, c))
                pg.draw.rect(superficie, cores[2], (b, 0, a, c))
                pg.draw.rect(superficie, cores[2], (0, d, a, c))
                pg.draw.rect(superficie, cores[1], (b, d, a, c))
                estrela(superficie, cores[0], (a / 2, c / 2), at / 9)
                estrela(superficie, cores[0], (b + a / 2, c / 2), at / 9)
                estrela(superficie, cores[0], (a / 2, d + c / 2), at / 9)
                estrela(superficie, cores[0], (b + a / 2, d + c / 2), at / 9)
    else: # modalidade[0] >= 6
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            if modalidade[0] == 6:
                pg.draw.rect(superficie, cores[1], (0, 0, a, c))
                pg.draw.rect(superficie, cores[1], (b, 0, a, c))
                pg.draw.rect(superficie, cores[1], (0, d, a, c))
                pg.draw.rect(superficie, cores[1], (b, d, a, c))
            else: # modalidade[0] == 7
                pg.draw.rect(superficie, cores[1], (0, 0, a, c))
                pg.draw.rect(superficie, cores[1], (b, 0, a, c))
                pg.draw.rect(superficie, cores[1], (0, d, a, c))
                pg.draw.rect(superficie, cores[1], (b, d, a, c))
                estrela(superficie, cores[0], (a / 2, c / 2), at / 9)
                estrela(superficie, cores[0], (b + a / 2, c / 2), at / 9)
                estrela(superficie, cores[0], (a / 2, d + c / 2), at / 9)
                estrela(superficie, cores[0], (b + a / 2, d + c / 2), at / 9)

    # --- Salvar a imagem apenas se criar_arquivo for True ---
    if criar_arquivo and superficie:
        # --- Definir o caminho para a pasta assets/flags ---
        nome_arquivo = f"bandeira_{name}_republica_dominicana.png" # Nome do arquivo pode ser personalizado
        caminho_pasta_flags = "assets/flags"
        caminho_completo = os.path.join(caminho_pasta_flags, nome_arquivo)

        # --- Salvar a imagem ---
        pg.image.save(superficie, caminho_completo)
        print(f"🖼️ Bandeira 'republica_dominicana' salva em: {caminho_completo}") # Mensagem de confirmação (opcional)

    return cores


def chile(name, criar_arquivo=False):
    modalidade = list(range(3))
    random.shuffle(modalidade)
    random.shuffle(modalidade)

    # --- Inicializar superfície apenas se for necessário ---
    superficie = None
    if criar_arquivo:
        superficie = pg.Surface((lt, at))

    if modalidade[0] == 0:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        t_cor = cores_padrao[random.choice(basic_color)]
        while t_cor == p_cor or t_cor == s_cor:
            t_cor = cores_padrao[random.choice(basic_color)]
        q_cor = cores_padrao[random.choice(basic_color)]
        while q_cor == p_cor or q_cor == s_cor or q_cor == t_cor:
            q_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor, t_cor, q_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, 0, at / 2, at / 2))
            pg.draw.rect(superficie, cores[2], (0, at / 2, lt, at / 2))
            estrela(superficie, cores[3], (at / 4, at / 4), at / 6)
    elif modalidade[0] == 1:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        t_cor = cores_padrao[random.choice(basic_color)]
        while t_cor == p_cor or t_cor == s_cor:
            t_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor, t_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, 0, at / 2, at / 2))
            pg.draw.rect(superficie, cores[2], (0, at / 2, lt, at / 2))
            estrela(superficie, cores[0], (at / 4, at / 4), at / 6)
    else: # modalidade[0] == 2
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        t_cor = cores_padrao[random.choice(basic_color)]
        while t_cor == p_cor or t_cor == s_cor:
            t_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor, t_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, 0, at / 2, at / 2))
            pg.draw.rect(superficie, cores[2], (0, at / 2, lt, at / 2))

    # --- Salvar a imagem apenas se criar_arquivo for True ---
    if criar_arquivo and superficie:
        # --- Definir o caminho para a pasta assets/flags ---
        nome_arquivo = f"bandeira_{name}_chile.png" # Nome do arquivo pode ser personalizado
        caminho_pasta_flags = "assets/flags"
        caminho_completo = os.path.join(caminho_pasta_flags, nome_arquivo)

        # --- Salvar a imagem ---
        pg.image.save(superficie, caminho_completo)
        print(f"🖼️ Bandeira 'chile' salva em: {caminho_completo}") # Mensagem de confirmação (opcional)

    return cores


def eau(name, criar_arquivo=False):
    modalidade = list(range(4))
    random.shuffle(modalidade)
    random.shuffle(modalidade)

    # --- Inicializar superfície apenas se for necessário ---
    superficie = None
    if criar_arquivo:
        superficie = pg.Surface((lt, at))

    if modalidade[0] < 2:
        if modalidade[0] == 1:
            p_cor = dic_cores[name]
            s_cor = cores_padrao[random.choice(basic_color)]
            while s_cor == p_cor:
                s_cor = cores_padrao[random.choice(basic_color)]
            t_cor = cores_padrao[random.choice(basic_color)]
            while t_cor == p_cor or t_cor == s_cor:
                t_cor = cores_padrao[random.choice(basic_color)]
            cores = [p_cor, s_cor, t_cor]
            random.shuffle(cores)
            random.shuffle(cores)
            if criar_arquivo and superficie:
                superficie.fill(cores[0])
                pg.draw.rect(superficie, cores[1], (0, at / 3, lt, at / 3))
                pg.draw.rect(superficie, cores[2], (0, 0, lt / 4, at))
                estrela(superficie, cores[1], (lt / 8, at / 2), lt / 9)
        else:
            p_cor = dic_cores[name]
            s_cor = cores_padrao[random.choice(basic_color)]
            while s_cor == p_cor:
                s_cor = cores_padrao[random.choice(basic_color)]
            t_cor = cores_padrao[random.choice(basic_color)]
            while t_cor == p_cor or t_cor == s_cor:
                t_cor = cores_padrao[random.choice(basic_color)]
            cores = [p_cor, s_cor, t_cor]
            random.shuffle(cores)
            random.shuffle(cores)
            if criar_arquivo and superficie:
                superficie.fill(cores[0])
                pg.draw.rect(superficie, cores[1], (0, at / 3, lt, at / 3))
                pg.draw.rect(superficie, cores[2], (0, 0, lt / 4, at))
    else:
        if modalidade[0] == 3:
            p_cor = dic_cores[name]
            s_cor = cores_padrao[random.choice(basic_color)]
            while s_cor == p_cor:
                s_cor = cores_padrao[random.choice(basic_color)]
            t_cor = cores_padrao[random.choice(basic_color)]
            while t_cor == p_cor or t_cor == s_cor:
                t_cor = cores_padrao[random.choice(basic_color)]
            q_cor = cores_padrao[random.choice(basic_color)]
            while q_cor == p_cor or q_cor == s_cor or q_cor == t_cor:
                q_cor = cores_padrao[random.choice(basic_color)]
            cores = [p_cor, s_cor, t_cor, q_cor]
            random.shuffle(cores)
            random.shuffle(cores)
            if criar_arquivo and superficie:
                superficie.fill(cores[0])
                pg.draw.rect(superficie, cores[1], (0, 0, lt, at / 3))
                pg.draw.rect(superficie, cores[2], (0, at / 3, lt, at / 3))
                pg.draw.rect(superficie, cores[3], (0, 0, lt / 4, at))
                estrela(superficie, cores[2], (lt / 8, at / 2), lt / 9)
        else:
            p_cor = dic_cores[name]
            s_cor = cores_padrao[random.choice(basic_color)]
            while s_cor == p_cor:
                s_cor = cores_padrao[random.choice(basic_color)]
            t_cor = cores_padrao[random.choice(basic_color)]
            while t_cor == p_cor or t_cor == s_cor:
                t_cor = cores_padrao[random.choice(basic_color)]
            q_cor = cores_padrao[random.choice(basic_color)]
            while q_cor == p_cor or q_cor == s_cor or q_cor == t_cor:
                q_cor = cores_padrao[random.choice(basic_color)]
            cores = [p_cor, s_cor, t_cor, q_cor]
            random.shuffle(cores)
            random.shuffle(cores)
            if criar_arquivo and superficie:
                superficie.fill(cores[0])
                pg.draw.rect(superficie, cores[1], (0, 0, lt, at / 3))
                pg.draw.rect(superficie, cores[2], (0, at / 3, lt, at / 3))
                pg.draw.rect(superficie, cores[3], (0, 0, lt / 4, at))

    # --- Salvar a imagem apenas se criar_arquivo for True ---
    if criar_arquivo and superficie:
        # --- Definir o caminho para a pasta assets/flags ---
        nome_arquivo = f"bandeira_{name}_eau.png" # Nome do arquivo pode ser personalizado
        caminho_pasta_flags = "assets/flags"
        caminho_completo = os.path.join(caminho_pasta_flags, nome_arquivo)

        # --- Salvar a imagem ---
        pg.image.save(superficie, caminho_completo)
        print(f"🖼️ Bandeira 'eau' salva em: {caminho_completo}") # Mensagem de confirmação (opcional)

    return cores


def filipinas(name, criar_arquivo=False):
    modalidade = list(range(3))
    random.shuffle(modalidade)
    random.shuffle(modalidade)

    # --- Inicializar superfície apenas se for necessário ---
    superficie = None
    if criar_arquivo:
        superficie = pg.Surface((lt, at))

    if modalidade[0] == 0:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        t_cor = cores_padrao[random.choice(basic_color)]
        while t_cor == p_cor or t_cor == s_cor:
            t_cor = cores_padrao[random.choice(basic_color)]
        q_cor = cores_padrao[random.choice(basic_color)]
        while q_cor == p_cor or q_cor == s_cor or q_cor == t_cor:
            q_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor, t_cor, q_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, 0, lt, at / 2))
            pg.draw.polygon(superficie, cores[2], ((0, 0), (lt / 3, at / 2), (0, at)))
            estrela(superficie, cores[3], (lt / 7, at / 2), at / 6)
    elif modalidade[0] == 1:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        t_cor = cores_padrao[random.choice(basic_color)]
        while t_cor == p_cor or t_cor == s_cor:
            t_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor, t_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, 0, lt, at / 2))
            pg.draw.polygon(superficie, cores[2], ((0, 0), (lt / 3, at / 2), (0, at)))
            estrela(superficie, cores[1], (lt / 7, at / 2), at / 6)
    else: # modalidade[0] == 2
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        t_cor = cores_padrao[random.choice(basic_color)]
        while t_cor == p_cor or t_cor == s_cor:
            t_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor, t_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, 0, lt, at / 2))
            pg.draw.polygon(superficie, cores[2], ((0, 0), (lt / 3, at / 2), (0, at)))

    # --- Salvar a imagem apenas se criar_arquivo for True ---
    if criar_arquivo and superficie:
        # --- Definir o caminho para a pasta assets/flags ---
        nome_arquivo = f"bandeira_{name}_filipinas.png" # Nome do arquivo pode ser personalizado
        caminho_pasta_flags = "assets/flags"
        caminho_completo = os.path.join(caminho_pasta_flags, nome_arquivo)

        # --- Salvar a imagem ---
        pg.image.save(superficie, caminho_completo)
        print(f"🖼️ Bandeira 'filipinas' salva em: {caminho_completo}") # Mensagem de confirmação (opcional)

    return cores


def espanha(name, criar_arquivo=False):
    modalidade = list(range(4))
    random.shuffle(modalidade)
    random.shuffle(modalidade)

    # --- Inicializar superfície apenas se for necessário ---
    superficie = None
    if criar_arquivo:
        superficie = pg.Surface((lt, at))

    if modalidade[0] == 0:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        t_cor = cores_padrao[random.choice(basic_color)]
        while t_cor == p_cor or t_cor == s_cor:
            t_cor = cores_padrao[random.choice(basic_color)]
        q_cor = cores_padrao[random.choice(basic_color)]
        while q_cor == p_cor or q_cor == s_cor or q_cor == t_cor:
            q_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor, t_cor, q_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, 0, lt, at / 5))
            pg.draw.rect(superficie, cores[2], (0, at * 4 / 5, lt, at / 4))
            estrela(superficie, cores[3], (lt / 2, at / 2), at / 4)
    elif modalidade[0] == 1:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        t_cor = cores_padrao[random.choice(basic_color)]
        while t_cor == p_cor or t_cor == s_cor:
            t_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor, t_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, 0, lt, at / 5))
            pg.draw.rect(superficie, cores[1], (0, at * 4 / 5, lt, at / 4))
            estrela(superficie, cores[2], (lt / 2, at / 2), at / 4)
    elif modalidade[0] == 2:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, 0, lt, at / 5))
            pg.draw.rect(superficie, cores[1], (0, at * 4 / 5, lt, at / 4))
    else: # modalidade[0] == 3
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, 0, lt, at / 5))
            pg.draw.rect(superficie, cores[1], (0, at * 4 / 5, lt, at / 4))
            estrela(superficie, cores[1], (lt / 2, at / 2), at / 4)

    # --- Salvar a imagem apenas se criar_arquivo for True ---
    if criar_arquivo and superficie:
        # --- Definir o caminho para a pasta assets/flags ---
        nome_arquivo = f"bandeira_{name}_espanha.png" # Nome do arquivo pode ser personalizado
        caminho_pasta_flags = "assets/flags"
        caminho_completo = os.path.join(caminho_pasta_flags, nome_arquivo)

        # --- Salvar a imagem ---
        pg.image.save(superficie, caminho_completo)
        print(f"🖼️ Bandeira 'espanha' salva em: {caminho_completo}") # Mensagem de confirmação (opcional)

    return cores


def tailandia(name, criar_arquivo=False):
    modalidade = list(range(6))
    random.shuffle(modalidade)
    random.shuffle(modalidade)

    # --- Inicializar superfície apenas se for necessário ---
    superficie = None
    if criar_arquivo:
        superficie = pg.Surface((lt, at))

    if modalidade[0] == 0:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        t_cor = cores_padrao[random.choice(basic_color)]
        while t_cor == p_cor or t_cor == s_cor:
            t_cor = cores_padrao[random.choice(basic_color)]
        q_cor = cores_padrao[random.choice(basic_color)]
        while q_cor == p_cor or q_cor == s_cor or q_cor == t_cor:
            q_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor, t_cor, q_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, 0, lt, at / 6))
            pg.draw.rect(superficie, cores[2], (0, at / 6, lt, at / 6))
            pg.draw.rect(superficie, cores[2], (0, at * 4 / 6, lt, at / 6))
            pg.draw.rect(superficie, cores[1], (0, at * 5 / 6, lt, at / 6))
            estrela(superficie, cores[3], (lt / 2, at / 2), at / 4)
    elif modalidade[0] == 1:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        t_cor = cores_padrao[random.choice(basic_color)]
        while t_cor == p_cor or t_cor == s_cor:
            t_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor, t_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, 0, lt, at / 6))
            pg.draw.rect(superficie, cores[1], (0, at / 6, lt, at / 6))
            pg.draw.rect(superficie, cores[1], (0, at * 4 / 6, lt, at / 6))
            pg.draw.rect(superficie, cores[1], (0, at * 5 / 6, lt, at / 6))
            estrela(superficie, cores[2], (lt / 2, at / 2), at / 9)
    elif modalidade[0] == 2:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        t_cor = cores_padrao[random.choice(basic_color)]
        while t_cor == p_cor or t_cor == s_cor:
            t_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor, t_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, 0, lt, at / 6))
            pg.draw.rect(superficie, cores[2], (0, at / 6, lt, at / 6))
            pg.draw.rect(superficie, cores[2], (0, at * 4 / 6, lt, at / 6))
            pg.draw.rect(superficie, cores[1], (0, at * 5 / 6, lt, at / 6))
    elif modalidade[0] == 3:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        t_cor = cores_padrao[random.choice(basic_color)]
        while t_cor == p_cor or t_cor == s_cor:
            t_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor, t_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, 0, lt, at / 6))
            pg.draw.rect(superficie, cores[2], (0, at / 6, lt, at / 6))
            pg.draw.rect(superficie, cores[2], (0, at * 4 / 6, lt, at / 6))
            pg.draw.rect(superficie, cores[1], (0, at * 5 / 6, lt, at / 6))
            estrela(superficie, cores[1], (lt / 2, at / 2), at / 7)
    elif modalidade[0] == 4:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        t_cor = cores_padrao[random.choice(basic_color)]
        while t_cor == p_cor or t_cor == s_cor:
            t_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor, t_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, 0, lt, at / 6))
            pg.draw.rect(superficie, cores[2], (0, at / 6, lt, at / 6))
            pg.draw.rect(superficie, cores[2], (0, at * 4 / 6, lt, at / 6))
            pg.draw.rect(superficie, cores[1], (0, at * 5 / 6, lt, at / 6))
            estrela(superficie, cores[2], (lt / 2, at / 2), at / 9)
    else: # modalidade[0] == 5
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        if criar_arquivo and superficie:
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[0], (0, 0, lt, at / 6))
            pg.draw.rect(superficie, cores[1], (0, at / 6, lt, at / 6))
            pg.draw.rect(superficie, cores[1], (0, at * 4 / 6, lt, at / 6))
            pg.draw.rect(superficie, cores[0], (0, at * 5 / 6, lt, at / 6))

    # --- Salvar a imagem apenas se criar_arquivo for True ---
    if criar_arquivo and superficie:
        # --- Definir o caminho para a pasta assets/flags ---
        nome_arquivo = f"bandeira_{name}_tailandia.png" # Nome do arquivo pode ser personalizado
        caminho_pasta_flags = "assets/flags"
        caminho_completo = os.path.join(caminho_pasta_flags, nome_arquivo)

        # --- Salvar a imagem ---
        pg.image.save(superficie, caminho_completo)
        print(f"🖼️ Bandeira 'tailandia' salva em: {caminho_completo}") # Mensagem de confirmação (opcional)

    return cores


def panama(name, criar_arquivo=False):
    modalidade = list(range(3))
    random.shuffle(modalidade)
    random.shuffle(modalidade)

    # --- Inicializar superfície apenas se for necessário ---
    superficie = None
    if criar_arquivo:
        superficie = pg.Surface((lt, at))

    p_cor = dic_cores[name]
    s_cor = cores_padrao[random.choice(basic_color)]
    while s_cor == p_cor:
        s_cor = cores_padrao[random.choice(basic_color)]

    t_cor = cores_padrao[random.choice(basic_color)]
    while t_cor == p_cor or t_cor == s_cor:
        t_cor = cores_padrao[random.choice(basic_color)]

    cores = [p_cor, s_cor, t_cor]
    random.shuffle(cores)
    random.shuffle(cores)

    # --- Desenhar e salvar apenas se criar_arquivo for True ---
    if criar_arquivo and superficie:
        superficie.fill(cores[0])
        pg.draw.rect(superficie, cores[1], (0, 0, lt / 2, at / 2))
        pg.draw.rect(superficie, cores[1], (lt / 2, at / 2, lt / 2, at / 2))

        if modalidade[0] == 0:
            estrela(superficie, cores[2], (lt / 2, at / 2), at / 4)
        elif modalidade[0] == 1:
            estrela(superficie, cores[2], (lt / 4, at / 4), at / 6)
            estrela(superficie, cores[2], (lt * 3 / 4, at / 4), at / 6)
            estrela(superficie, cores[2], (lt / 4, at * 3 / 4), at / 6)
            estrela(superficie, cores[2], (lt * 3 / 4, at * 3 / 4), at / 6)

        # --- Definir o caminho para a pasta assets/flags ---
        # Certifique-se de que a pasta 'assets/flags' exista no seu projeto
        nome_arquivo = f"bandeira_{name}.png"
        caminho_pasta_flags = "assets/flags"
        caminho_completo = os.path.join(caminho_pasta_flags, nome_arquivo)

        # --- Salvar a imagem ---
        pg.image.save(superficie, caminho_completo)
        print(f"🖼️ Bandeira salva em: {caminho_completo}") # Mensagem de confirmação (opcional)

    return cores


def bandeira(name, numero, criar_arquivo=False):
    if numero < 6:
        return franca(name, criar_arquivo)
    elif numero < 12:
        return alemanha(name, criar_arquivo)
    elif numero < 14:
        return indonesia(name, criar_arquivo)
    elif numero < 16:
        return argelia(name, criar_arquivo)
    elif numero < 17:
        return japao(name, criar_arquivo)
    elif numero < 19:
        return butao(name, criar_arquivo)
    elif numero < 21:
        return butao_invertido(name, criar_arquivo)
    elif numero < 24:
        return cuba(name, criar_arquivo)
    elif numero < 28:
        return jordania(name, criar_arquivo)
    elif numero < 31:
        return madagascar(name, criar_arquivo)
    elif numero < 33:
        return jamaica(name, criar_arquivo)
    elif numero < 34:
        return suecia(name, criar_arquivo)
    elif numero < 36:
        return china(name, criar_arquivo)
    elif numero < 38:
        return samoa(name, criar_arquivo)
    elif numero < 43:
        return eua(name, criar_arquivo)
    elif numero < 47:
        return tanzania(name, criar_arquivo)
    elif numero < 51:
        return tanzania_invertida(name, criar_arquivo)
    elif numero < 59:
        return republica_dominicana(name, criar_arquivo)
    elif numero < 62:
        return chile(name, criar_arquivo)
    elif numero < 66:
        return eau(name, criar_arquivo)
    elif numero < 69:
        return filipinas(name, criar_arquivo)
    elif numero < 74:
        return espanha(name, criar_arquivo)
    elif numero < 80:
        return tailandia(name, criar_arquivo)
    elif numero < 83:
        return panama(name, criar_arquivo)
    print("Número fora do alcance")
    return None
