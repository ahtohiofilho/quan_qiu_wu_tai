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


def franca(name):
    modalidade = list(range(6))
    random.shuffle(modalidade)
    random.shuffle(modalidade)
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
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, 0, lt / 3, at))
            pg.draw.rect(superficie, cores[2], (lt / 3, 0, lt / 3, at))
            estrela(superficie, cores[3], (lt / 2, at / 2), lt / 9)
            return cores
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
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, 0, lt / 3, at))
            pg.draw.rect(superficie, cores[2], (lt / 3, 0, lt / 3, at))
            estrela(superficie, cores[1], (lt / 2, at / 2), lt / 9)
            return cores
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
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, 0, lt / 3, at))
            pg.draw.rect(superficie, cores[2], (lt / 3, 0, lt / 3, at))
            return cores
    else:
        if modalidade[0] == 4:
            p_cor = dic_cores[name]
            s_cor = cores_padrao[random.choice(basic_color)]
            while s_cor == p_cor:
                s_cor = cores_padrao[random.choice(basic_color)]
            cores = [p_cor, s_cor]
            random.shuffle(cores)
            random.shuffle(cores)
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (lt / 3, 0, lt / 3, at))
            estrela(superficie, cores[0], (lt / 2, at / 2), lt / 9)
            return cores
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
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (lt / 3, 0, lt / 3, at))
            estrela(superficie, cores[2], (lt / 2, at / 2), lt / 9)
            return cores
        else:
            p_cor = dic_cores[name]
            s_cor = cores_padrao[random.choice(basic_color)]
            while s_cor == p_cor:
                s_cor = cores_padrao[random.choice(basic_color)]
            cores = [p_cor, s_cor]
            random.shuffle(cores)
            random.shuffle(cores)
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (lt / 3, 0, lt / 3, at))
            return cores


def alemanha(name):
    modalidade = list(range(6))
    random.shuffle(modalidade)
    random.shuffle(modalidade)
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
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, 0, lt, at / 3))
            pg.draw.rect(superficie, cores[2], (0, at / 3, lt, at / 3))
            estrela(superficie, cores[3], (lt / 2, at / 2), lt / 6)
            return cores
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
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, 0, lt, at / 3))
            pg.draw.rect(superficie, cores[2], (0, at / 3, lt, at / 3))
            estrela(superficie, cores[1], (lt / 2, at / 2), lt / 12)
            return cores
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
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, 0, lt, at / 3))
            pg.draw.rect(superficie, cores[2], (0, at / 3, lt, at / 3))
            return cores
    else:
        if modalidade[0] == 4:
            p_cor = dic_cores[name]
            s_cor = cores_padrao[random.choice(basic_color)]
            while s_cor == p_cor:
                s_cor = cores_padrao[random.choice(basic_color)]
            cores = [p_cor, s_cor]
            random.shuffle(cores)
            random.shuffle(cores)
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, at / 3, lt, at / 3))
            estrela(superficie, cores[0], (lt / 2, at / 2), lt / 12)
            return cores
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
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, at / 3, lt, at / 3))
            estrela(superficie, cores[2], (lt / 2, at / 2), lt / 6)
            return cores
        else:
            p_cor = dic_cores[name]
            s_cor = cores_padrao[random.choice(basic_color)]
            while s_cor == p_cor:
                s_cor = cores_padrao[random.choice(basic_color)]
            cores = [p_cor, s_cor]
            random.shuffle(cores)
            random.shuffle(cores)
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, at / 3, lt, at / 3))
            return cores


def indonesia(name):
    modalidade = list(range(2))
    random.shuffle(modalidade)
    random.shuffle(modalidade)
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
        superficie.fill(cores[0])
        pg.draw.rect(superficie, cores[1], (0, 0, lt, at / 2))
        estrela(superficie, cores[2], (lt / 2, at / 2), lt / 6)
        return cores
    else:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        superficie.fill(cores[0])
        pg.draw.rect(superficie, cores[1], (0, 0, lt, at / 2))
        return cores


def argelia(name):
    modalidade = list(range(2))
    random.shuffle(modalidade)
    random.shuffle(modalidade)
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
        superficie.fill(cores[0])
        pg.draw.rect(superficie, cores[1], (0, 0, lt / 2, at))
        estrela(superficie, cores[2], (lt / 2, at / 2), lt / 6)
        return cores
    else:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        superficie.fill(cores[0])
        pg.draw.rect(superficie, cores[1], (0, 0, lt / 2, at))
        return cores


def japao(name):
    p_cor = dic_cores[name]
    s_cor = cores_padrao[random.choice(basic_color)]
    while s_cor == p_cor:
        s_cor = cores_padrao[random.choice(basic_color)]
    cores = [p_cor, s_cor]
    random.shuffle(cores)
    random.shuffle(cores)
    superficie = pg.Surface((lt, at))
    superficie.fill(cores[0])
    pg.draw.circle(superficie, cores[1], (lt / 2, at / 2), at / 4)
    return cores


def butao(name):
    modalidade = list(range(2))
    random.shuffle(modalidade)
    random.shuffle(modalidade)
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
        superficie.fill(cores[0])
        pg.draw.polygon(superficie, cores[1], ((0, at), (lt, 0), (lt, at)))
        estrela(superficie, cores[2], (lt / 2, at / 2), lt / 6)
        return cores
    else:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        superficie.fill(cores[0])
        pg.draw.polygon(superficie, cores[1], ((0, at), (lt, 0), (lt, at)))
        return cores


def butao_invertido(name):
    modalidade = list(range(2))
    random.shuffle(modalidade)
    random.shuffle(modalidade)
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
        superficie.fill(cores[0])
        pg.draw.polygon(superficie, cores[1], ((0, 0), (lt, at), (0, at)))
        estrela(superficie, cores[2], (lt / 2, at / 2), lt / 6)
        return cores
    else:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        superficie.fill(cores[0])
        pg.draw.polygon(superficie, cores[1], ((0, 0), (lt, at), (0, at)))
        return cores


def cuba(name):
    modalidade = list(range(3))
    random.shuffle(modalidade)
    random.shuffle(modalidade)
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
        superficie.fill(cores[0])
        pg.draw.rect(superficie, cores[1], (0, at / 5, lt, at / 5))
        pg.draw.rect(superficie, cores[1], (0, (at / 5) * 3, lt, at / 5))
        pg.draw.polygon(superficie, cores[2], ((0, 0), (lt / 3, at / 2), (0, at)))
        return cores
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
        superficie.fill(cores[0])
        pg.draw.rect(superficie, cores[1], (0, at / 5, lt, at / 5))
        pg.draw.rect(superficie, cores[1], (0, (at / 5) * 3, lt, at / 5))
        pg.draw.polygon(superficie, cores[2], ((0, 0), (lt / 3, at / 2), (0, at)))
        estrela(superficie, cores[3], (lt / 9, at / 2), lt / 9)
        return cores
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
        superficie.fill(cores[0])
        pg.draw.rect(superficie, cores[1], (0, at / 5, lt, at / 5))
        pg.draw.rect(superficie, cores[1], (0, (at / 5) * 3, lt, at / 5))
        pg.draw.polygon(superficie, cores[2], ((0, 0), (lt / 3, at / 2), (0, at)))
        estrela(superficie, cores[1], (lt / 9, at / 2), lt / 9)
        return cores


def jordania(name):
    modalidade = list(range(4))
    random.shuffle(modalidade)
    random.shuffle(modalidade)
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
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, 0, lt, at / 3))
            pg.draw.rect(superficie, cores[2], (0, at / 3, lt, at / 3))
            pg.draw.polygon(superficie, cores[3], ((0, 0), (lt / 3, at / 2), (0, at)))
            estrela(superficie, cores[2], (lt / 8.81, at / 2), lt / 9)
            return cores
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
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, 0, lt, at / 3))
            pg.draw.rect(superficie, cores[2], (0, at / 3, lt, at / 3))
            pg.draw.polygon(superficie, cores[3], ((0, 0), (lt / 3, at / 2), (0, at)))
            return cores
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
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, at / 3, lt, at / 3))
            pg.draw.polygon(superficie, cores[2], ((0, 0), (lt / 3, at / 2), (0, at)))
            estrela(superficie, cores[1], (lt / 8.81, at / 2), lt / 9)
            return cores
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
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, at / 3, lt, at / 3))
            pg.draw.polygon(superficie, cores[2], ((0, 0), (lt / 3, at / 2), (0, at)))
            return cores


def madagascar(name):
    modalidade = list(range(3))
    random.shuffle(modalidade)
    random.shuffle(modalidade)
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
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, 0, lt / 3, at))
            pg.draw.rect(superficie, cores[2], (lt / 3, 0, lt * 2 / 3, at / 2))
            estrela(superficie, cores[2], (lt / 6, at / 2), lt / 9)
            return cores
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
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, 0, lt / 3, at))
            pg.draw.rect(superficie, cores[2], (lt / 3, 0, lt * 2 / 3, at / 2))
            return cores
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
        superficie.fill(cores[0])
        pg.draw.rect(superficie, cores[1], (0, 0, lt / 3, at))
        pg.draw.rect(superficie, cores[2], (lt / 3, 0, lt * 2 / 3, at / 2))
        estrela(superficie, cores[3], (lt / 6, at / 2), lt / 9)
        return cores


def jamaica(name):
    modalidade = list(range(2))
    random.shuffle(modalidade)
    random.shuffle(modalidade)
    superficie = pg.Surface((lt, at))
    if modalidade[0] == 1:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        superficie.fill(cores[0])
        pg.draw.polygon(superficie, cores[1], ((0, lt / 12), (lt / 2 - lt / 6, at / 2), (0, at - lt / 12)))
        pg.draw.polygon(superficie, cores[1], ((lt / 6, 0), (lt - lt / 6, 0), (lt / 2, at / 2 - lt / 12)))
        pg.draw.polygon(superficie, cores[1], ((lt, lt / 12), (lt / 2 + lt / 6, at / 2), (lt, at - lt / 12)))
        pg.draw.polygon(superficie, cores[1], ((lt / 6, at), (lt - lt / 6, at), (lt / 2, at / 2 + lt / 12)))
        return cores
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
        superficie.fill(cores[0])
        pg.draw.polygon(superficie, cores[1], ((0, lt / 12), (lt / 2 - lt / 6, at / 2), (0, at - lt / 12)))
        pg.draw.polygon(superficie, cores[2], ((lt / 6, 0), (lt - lt / 6, 0), (lt / 2, at / 2 - lt / 12)))
        pg.draw.polygon(superficie, cores[1], ((lt, lt / 12), (lt / 2 + lt / 6, at / 2), (lt, at - lt / 12)))
        pg.draw.polygon(superficie, cores[2], ((lt / 6, at), (lt - lt / 6, at), (lt / 2, at / 2 + lt / 12)))
        return cores


def suecia(name):
    p_cor = dic_cores[name]
    s_cor = cores_padrao[random.choice(basic_color)]
    while s_cor == p_cor:
        s_cor = cores_padrao[random.choice(basic_color)]
    cores = [p_cor, s_cor]
    random.shuffle(cores)
    random.shuffle(cores)
    superficie = pg.Surface((lt, at))
    superficie.fill(cores[0])
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
    return cores


def china(name):
    modalidade = list(range(2))
    random.shuffle(modalidade)
    random.shuffle(modalidade)
    superficie = pg.Surface((lt, at))
    if modalidade[0] == 1:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        superficie.fill(cores[0])
        estrela(superficie, cores[1], (lt / 2, at / 2), lt / 6)
        return cores
    else:
        p_cor = dic_cores[name]
        superficie.fill(p_cor)
        return [p_cor]


def samoa(name):
    modalidade = list(range(2))
    random.shuffle(modalidade)
    random.shuffle(modalidade)
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
        superficie.fill(cores[0])
        pg.draw.rect(superficie, cores[1], (0, 0, lt / 4, lt / 4))
        estrela(superficie, cores[2], (lt / 8, lt / 8), lt / 12)
        return cores
    else:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        superficie.fill(cores[0])
        pg.draw.rect(superficie, cores[1], (0, 0, lt / 4, lt / 4))
        return cores


def eua(name):
    modalidade = list(range(5))
    random.shuffle(modalidade)
    random.shuffle(modalidade)
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
        superficie.fill(cores[0])
        pg.draw.rect(superficie, cores[1], (0, at / 7, lt, at / 7))
        pg.draw.rect(superficie, cores[1], (0, at * 3 / 7, lt, at / 7))
        pg.draw.rect(superficie, cores[1], (0, at * 5 / 7, lt, at / 7))
        pg.draw.rect(superficie, cores[2], (0, 0, at * 3 / 7, at * 3 / 7))
        estrela(superficie, cores[3], (at * 3 / 14, at * 3 / 14), at / 7)
        return cores
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
        superficie.fill(cores[0])
        pg.draw.rect(superficie, cores[1], (0, at / 7, lt, at / 7))
        pg.draw.rect(superficie, cores[1], (0, at * 3 / 7, lt, at / 7))
        pg.draw.rect(superficie, cores[1], (0, at * 5 / 7, lt, at / 7))
        pg.draw.rect(superficie, cores[2], (0, 0, at * 3 / 7, at * 3 / 7))
        estrela(superficie, cores[1], (at * 3 / 14, at * 3 / 14), at / 7)
        return cores
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
        superficie.fill(cores[0])
        pg.draw.rect(superficie, cores[1], (0, at / 7, lt, at / 7))
        pg.draw.rect(superficie, cores[1], (0, at * 3 / 7, lt, at / 7))
        pg.draw.rect(superficie, cores[1], (0, at * 5 / 7, lt, at / 7))
        pg.draw.rect(superficie, cores[2], (0, 0, at * 3 / 7, at * 3 / 7))
        return cores
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
        superficie.fill(cores[0])
        pg.draw.rect(superficie, cores[1], (0, at / 7, lt, at / 7))
        pg.draw.rect(superficie, cores[1], (0, at * 3 / 7, lt, at / 7))
        pg.draw.rect(superficie, cores[1], (0, at * 5 / 7, lt, at / 7))
        pg.draw.rect(superficie, cores[0], (0, 0, at * 3 / 7, at * 3 / 7))
        estrela(superficie, cores[2], (at * 3 / 14, at * 3 / 14), at / 7)
        return cores
    else:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        superficie.fill(cores[0])
        pg.draw.rect(superficie, cores[1], (0, at / 7, lt, at / 7))
        pg.draw.rect(superficie, cores[1], (0, at * 3 / 7, lt, at / 7))
        pg.draw.rect(superficie, cores[1], (0, at * 5 / 7, lt, at / 7))
        pg.draw.rect(superficie, cores[0], (0, 0, at * 3 / 7, at * 3 / 7))
        return cores


def tanzania(name):
    modalidade = list(range(4))
    random.shuffle(modalidade)
    random.shuffle(modalidade)
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
        superficie.fill(cores[0])
        pg.draw.polygon(superficie, cores[1], ((0, 0), (lt - lt / 6, 0), (0, at - lt / 12)))
        pg.draw.polygon(superficie, cores[2], ((lt / 6, at), (lt, lt / 12), (lt, at)))
        estrela(superficie, cores[3], (lt / 5, at / 4), at / 6)
        return cores
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
        superficie.fill(cores[0])
        pg.draw.polygon(superficie, cores[1], ((0, 0), (lt - lt / 6, 0), (0, at - lt / 12)))
        pg.draw.polygon(superficie, cores[1], ((lt / 6, at), (lt, lt / 12), (lt, at)))
        estrela(superficie, cores[2], (lt / 5, at / 4), at / 6)
        return cores
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
        superficie.fill(cores[0])
        pg.draw.polygon(superficie, cores[1], ((0, 0), (lt - lt / 6, 0), (0, at - lt / 12)))
        pg.draw.polygon(superficie, cores[2], ((lt / 6, at), (lt, lt / 12), (lt, at)))
        return cores
    else:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        superficie.fill(cores[0])
        pg.draw.polygon(superficie, cores[1], ((0, 0), (lt - lt / 6, 0), (0, at - lt / 12)))
        pg.draw.polygon(superficie, cores[1], ((lt / 6, at), (lt, lt / 12), (lt, at)))
        return cores


def tanzania_invertida(name):
    modalidade = list(range(4))
    random.shuffle(modalidade)
    random.shuffle(modalidade)
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
        superficie.fill(cores[0])
        pg.draw.polygon(superficie, cores[1], ((lt / 6, 0), (lt, 0), (lt, at - lt / 12)))
        pg.draw.polygon(superficie, cores[2], ((0, lt / 12), (lt - lt / 6, at), (0, at)))
        estrela(superficie, cores[3], (lt * 4 / 5, at / 4), at / 6)
        return cores
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
        superficie.fill(cores[0])
        pg.draw.polygon(superficie, cores[1], ((lt / 6, 0), (lt, 0), (lt, at - lt / 12)))
        pg.draw.polygon(superficie, cores[2], ((0, lt / 12), (lt - lt / 6, at), (0, at)))
        return cores
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
        superficie.fill(cores[0])
        pg.draw.polygon(superficie, cores[1], ((lt / 6, 0), (lt, 0), (lt, at - lt / 12)))
        pg.draw.polygon(superficie, cores[2], ((0, lt / 12), (lt - lt / 6, at), (0, at)))
        return cores
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
        superficie.fill(cores[0])
        pg.draw.polygon(superficie, cores[1], ((lt / 6, 0), (lt, 0), (lt, at - lt / 12)))
        pg.draw.polygon(superficie, cores[2], ((0, lt / 12), (lt - lt / 6, at), (0, at)))
        return cores


def republica_dominicana(name):
    modalidade = list(range(8))
    random.shuffle(modalidade)
    random.shuffle(modalidade)
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
            return cores
        else:
            estrela(superficie, cores[3], (lt / 2, at / 2), at / 6)
            return cores
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
            return cores
        elif modalidade[0] == 3:
            pg.draw.rect(superficie, cores[1], (0, 0, a, c))
            pg.draw.rect(superficie, cores[2], (b, 0, a, c))
            pg.draw.rect(superficie, cores[2], (0, d, a, c))
            pg.draw.rect(superficie, cores[1], (b, d, a, c))
            return cores
        elif modalidade[0] == 4:
            pg.draw.rect(superficie, cores[1], (0, 0, a, c))
            pg.draw.rect(superficie, cores[1], (b, 0, a, c))
            pg.draw.rect(superficie, cores[1], (0, d, a, c))
            pg.draw.rect(superficie, cores[1], (b, d, a, c))
            estrela(superficie, cores[2], (lt / 2, at / 2), at / 6)
            return cores
        else:
            pg.draw.rect(superficie, cores[1], (0, 0, a, c))
            pg.draw.rect(superficie, cores[2], (b, 0, a, c))
            pg.draw.rect(superficie, cores[2], (0, d, a, c))
            pg.draw.rect(superficie, cores[1], (b, d, a, c))
            estrela(superficie, cores[0], (a / 2, c / 2), at / 9)
            estrela(superficie, cores[0], (b + a / 2, c / 2), at / 9)
            estrela(superficie, cores[0], (a / 2, d + c / 2), at / 9)
            estrela(superficie, cores[0], (b + a / 2, d + c / 2), at / 9)
            return cores
    else:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        superficie.fill(cores[0])
        if modalidade[0] == 6:
            pg.draw.rect(superficie, cores[1], (0, 0, a, c))
            pg.draw.rect(superficie, cores[1], (b, 0, a, c))
            pg.draw.rect(superficie, cores[1], (0, d, a, c))
            pg.draw.rect(superficie, cores[1], (b, d, a, c))
            return cores
        else:
            pg.draw.rect(superficie, cores[1], (0, 0, a, c))
            pg.draw.rect(superficie, cores[1], (b, 0, a, c))
            pg.draw.rect(superficie, cores[1], (0, d, a, c))
            pg.draw.rect(superficie, cores[1], (b, d, a, c))
            estrela(superficie, cores[0], (a / 2, c / 2), at / 9)
            estrela(superficie, cores[0], (b + a / 2, c / 2), at / 9)
            estrela(superficie, cores[0], (a / 2, d + c / 2), at / 9)
            estrela(superficie, cores[0], (b + a / 2, d + c / 2), at / 9)
            return cores


def chile(name):
    modalidade = list(range(3))
    random.shuffle(modalidade)
    random.shuffle(modalidade)
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
        superficie.fill(cores[0])
        pg.draw.rect(superficie, cores[1], (0, 0, at / 2, at / 2))
        pg.draw.rect(superficie, cores[2], (0, at / 2, lt, at / 2))
        estrela(superficie, cores[3], (at / 4, at / 4), at / 6)
        return cores
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
        superficie.fill(cores[0])
        pg.draw.rect(superficie, cores[1], (0, 0, at / 2, at / 2))
        pg.draw.rect(superficie, cores[2], (0, at / 2, lt, at / 2))
        estrela(superficie, cores[0], (at / 4, at / 4), at / 6)
        return cores
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
        superficie.fill(cores[0])
        pg.draw.rect(superficie, cores[1], (0, 0, at / 2, at / 2))
        pg.draw.rect(superficie, cores[2], (0, at / 2, lt, at / 2))
        return cores


def eau(name):
    modalidade = list(range(4))
    random.shuffle(modalidade)
    random.shuffle(modalidade)
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
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, at / 3, lt, at / 3))
            pg.draw.rect(superficie, cores[2], (0, 0, lt / 4, at))
            estrela(superficie, cores[1], (lt / 8, at / 2), lt / 9)
            return cores
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
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, at / 3, lt, at / 3))
            pg.draw.rect(superficie, cores[2], (0, 0, lt / 4, at))
            return cores
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
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, 0, lt, at / 3))
            pg.draw.rect(superficie, cores[2], (0, at / 3, lt, at / 3))
            pg.draw.rect(superficie, cores[3], (0, 0, lt / 4, at))
            estrela(superficie, cores[2], (lt / 8, at / 2), lt / 9)
            return cores
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
            superficie.fill(cores[0])
            pg.draw.rect(superficie, cores[1], (0, 0, lt, at / 3))
            pg.draw.rect(superficie, cores[2], (0, at / 3, lt, at / 3))
            pg.draw.rect(superficie, cores[3], (0, 0, lt / 4, at))
            return cores


def filipinas(name):
    modalidade = list(range(3))
    random.shuffle(modalidade)
    random.shuffle(modalidade)
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
        superficie.fill(cores[0])
        pg.draw.rect(superficie, cores[1], (0, 0, lt, at / 2))
        pg.draw.polygon(superficie, cores[2], ((0, 0), (lt / 3, at / 2), (0, at)))
        estrela(superficie, cores[3], (lt / 7, at / 2), at / 6)
        return cores
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
        superficie.fill(cores[0])
        pg.draw.rect(superficie, cores[1], (0, 0, lt, at / 2))
        pg.draw.polygon(superficie, cores[2], ((0, 0), (lt / 3, at / 2), (0, at)))
        estrela(superficie, cores[1], (lt / 7, at / 2), at / 6)
        return cores
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
        superficie.fill(cores[0])
        pg.draw.rect(superficie, cores[1], (0, 0, lt, at / 2))
        pg.draw.polygon(superficie, cores[2], ((0, 0), (lt / 3, at / 2), (0, at)))
        return cores


def espanha(name):
    modalidade = list(range(4))
    random.shuffle(modalidade)
    random.shuffle(modalidade)
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
        superficie.fill(cores[0])
        pg.draw.rect(superficie, cores[1], (0, 0, lt, at / 5))
        pg.draw.rect(superficie, cores[2], (0, at * 4 / 5, lt, at / 4))
        estrela(superficie, cores[3], (lt / 2, at / 2), at / 4)
        return cores
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
        superficie.fill(cores[0])
        pg.draw.rect(superficie, cores[1], (0, 0, lt, at / 5))
        pg.draw.rect(superficie, cores[1], (0, at * 4 / 5, lt, at / 4))
        estrela(superficie, cores[2], (lt / 2, at / 2), at / 4)
        return cores
    elif modalidade[0] == 2:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        superficie.fill(cores[0])
        pg.draw.rect(superficie, cores[1], (0, 0, lt, at / 5))
        pg.draw.rect(superficie, cores[1], (0, at * 4 / 5, lt, at / 4))
        return cores
    else:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        superficie.fill(cores[0])
        pg.draw.rect(superficie, cores[1], (0, 0, lt, at / 5))
        pg.draw.rect(superficie, cores[1], (0, at * 4 / 5, lt, at / 4))
        estrela(superficie, cores[1], (lt / 2, at / 2), at / 4)
        return cores


def tailandia(name):
    modalidade = list(range(6))
    random.shuffle(modalidade)
    random.shuffle(modalidade)
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
        superficie.fill(cores[0])
        pg.draw.rect(superficie, cores[1], (0, 0, lt, at / 6))
        pg.draw.rect(superficie, cores[2], (0, at / 6, lt, at / 6))
        pg.draw.rect(superficie, cores[2], (0, at * 4 / 6, lt, at / 6))
        pg.draw.rect(superficie, cores[1], (0, at * 5 / 6, lt, at / 6))
        estrela(superficie, cores[3], (lt / 2, at / 2), at / 4)
        return cores
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
        superficie.fill(cores[0])
        pg.draw.rect(superficie, cores[0], (0, 0, lt, at / 6))
        pg.draw.rect(superficie, cores[1], (0, at / 6, lt, at / 6))
        pg.draw.rect(superficie, cores[1], (0, at * 4 / 6, lt, at / 6))
        pg.draw.rect(superficie, cores[0], (0, at * 5 / 6, lt, at / 6))
        estrela(superficie, cores[2], (lt / 2, at / 2), at / 9)
        return cores
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
        superficie.fill(cores[0])
        pg.draw.rect(superficie, cores[1], (0, 0, lt, at / 6))
        pg.draw.rect(superficie, cores[2], (0, at / 6, lt, at / 6))
        pg.draw.rect(superficie, cores[2], (0, at * 4 / 6, lt, at / 6))
        pg.draw.rect(superficie, cores[1], (0, at * 5 / 6, lt, at / 6))
        return cores
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
        superficie.fill(cores[0])
        pg.draw.rect(superficie, cores[1], (0, 0, lt, at / 6))
        pg.draw.rect(superficie, cores[2], (0, at / 6, lt, at / 6))
        pg.draw.rect(superficie, cores[2], (0, at * 4 / 6, lt, at / 6))
        pg.draw.rect(superficie, cores[1], (0, at * 5 / 6, lt, at / 6))
        estrela(superficie, cores[1], (lt / 2, at / 2), at / 7)
        return cores
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
        superficie.fill(cores[0])
        pg.draw.rect(superficie, cores[1], (0, 0, lt, at / 6))
        pg.draw.rect(superficie, cores[2], (0, at / 6, lt, at / 6))
        pg.draw.rect(superficie, cores[2], (0, at * 4 / 6, lt, at / 6))
        pg.draw.rect(superficie, cores[1], (0, at * 5 / 6, lt, at / 6))
        estrela(superficie, cores[2], (lt / 2, at / 2), at / 9)
        return cores
    else:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        superficie.fill(cores[0])
        pg.draw.rect(superficie, cores[0], (0, 0, lt, at / 6))
        pg.draw.rect(superficie, cores[1], (0, at / 6, lt, at / 6))
        pg.draw.rect(superficie, cores[1], (0, at * 4 / 6, lt, at / 6))
        pg.draw.rect(superficie, cores[0], (0, at * 5 / 6, lt, at / 6))
        return cores


def panama(name):
    modalidade = list(range(3))
    random.shuffle(modalidade)
    random.shuffle(modalidade)
    superficie = pg.Surface((lt, at))
    if modalidade[0] == 0:
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
        superficie.fill(cores[0])
        pg.draw.rect(superficie, cores[1], (0, 0, lt / 2, at / 2))
        pg.draw.rect(superficie, cores[1], (lt / 2, at / 2, lt / 2, at / 2))
        estrela(superficie, cores[2], (lt / 2, at / 2), at / 4)
        return cores
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
        superficie.fill(cores[0])
        pg.draw.rect(superficie, cores[1], (0, 0, lt / 2, at / 2))
        pg.draw.rect(superficie, cores[1], (lt / 2, at / 2, lt / 2, at / 2))
        estrela(superficie, cores[2], (lt / 4, at / 4), at / 6)
        estrela(superficie, cores[2], (lt * 3 / 4, at / 4), at / 6)
        estrela(superficie, cores[2], (lt / 4, at * 3 / 4), at / 6)
        estrela(superficie, cores[2], (lt * 3 / 4, at * 3 / 4), at / 6)
        return cores
    else:
        p_cor = dic_cores[name]
        s_cor = cores_padrao[random.choice(basic_color)]
        while s_cor == p_cor:
            s_cor = cores_padrao[random.choice(basic_color)]
        cores = [p_cor, s_cor]
        random.shuffle(cores)
        random.shuffle(cores)
        superficie.fill(cores[0])
        pg.draw.rect(superficie, cores[1], (0, 0, lt / 2, at / 2))
        pg.draw.rect(superficie, cores[1], (lt / 2, at / 2, lt / 2, at / 2))
        return cores


def bandeira(name, numero):
    if numero < 6:
        return franca(name)
    elif numero < 12:
        return alemanha(name)
    elif numero < 14:
        return indonesia(name)
    elif numero < 16:
        return argelia(name)
    elif numero < 17:
        return japao(name)
    elif numero < 19:
        return butao(name)
    elif numero < 21:
        return butao_invertido(name)
    elif numero < 24:
        return cuba(name)
    elif numero < 28:
        return jordania(name)
    elif numero < 31:
        return madagascar(name)
    elif numero < 33:
        return jamaica(name)
    elif numero < 34:
        return suecia(name)
    elif numero < 36:
        return china(name)
    elif numero < 38:
        return samoa(name)
    elif numero < 43:
        return eua(name)
    elif numero < 47:
        return tanzania(name)
    elif numero < 51:
        return tanzania_invertida(name)
    elif numero < 59:
        return republica_dominicana(name)
    elif numero < 62:
        return chile(name)
    elif numero < 66:
        return eau(name)
    elif numero < 69:
        return filipinas(name)
    elif numero < 74:
        return espanha(name)
    elif numero < 80:
        return tailandia(name)
    elif numero < 83:
        return panama(name)
    print("Número fora do alcance")
    return None
