import pygame
from src.graph import Graph
import sys


def draw(screen, graph: Graph):
    for vertex in graph.vertices:  # edges
        x, y = vertex.position()
        for connected in vertex.connected_to:
            con_x, con_y = graph.vertices[connected].position()
            pygame.draw.line(screen, (0, 0, 0), start_pos=(x, y), end_pos=(con_x, con_y), width=2)

    for vertex in graph.vertices:  # vertices
        x, y = vertex.position()
        pygame.draw.circle(screen, vertex.colour, center=(x, y), radius=8, width=0)
        pygame.draw.circle(screen, (0, 0, 0), center=(x, y), radius=8, width=2)


def delete_edge(g: Graph, mouse_pos_x: int, mouse_pos_y: int):
    for (f_idx, f_vert) in enumerate(g.vertices, 1):
        for s_idx in f_vert.connected_to:
            s_vert = g.vertices[s_idx]
            length = ((f_vert.x - s_vert.x) ** 2 + (f_vert.y - s_vert.y) ** 2) ** 0.5

            cos_1 = ((f_vert.x - mouse_pos_x) * (f_vert.x - s_vert.x) + (
                    f_vert.y - mouse_pos_y) * (f_vert.y - s_vert.y)) / length / (
                            (f_vert.x - mouse_pos_x) ** 2 + (
                             f_vert.y - mouse_pos_y) ** 2) ** 0.5
            if cos_1 < 0:
                continue
            cos_2 = ((mouse_pos_x - s_vert.x) * (f_vert.x - s_vert.x) + (
                    mouse_pos_y - s_vert.y) * (f_vert.y - s_vert.y)) / length / (
                            (mouse_pos_x - s_vert.x) ** 2 + (
                             mouse_pos_y - s_vert.y) ** 2) ** 0.5
            if cos_2 < 0:
                continue

            if (1 - cos_1 ** 2) ** 0.5 * length < 12:
                g.disconnect(f_idx, s_idx + 1)
                break


def main():
    g = Graph()

    pygame.init()

    screen = pygame.display.set_mode((1000, 800))
    mode = "VERT"
    to_connect = 0
    to_move = 0

    while True:
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_c]:
                    mode = "CONN"
                    to_connect = 0
                if pygame.key.get_pressed()[pygame.K_v]:
                    mode = "VERT"
                    to_move = 0

                if pygame.key.get_pressed()[pygame.K_f]:
                    g.colour()
                if pygame.key.get_pressed()[pygame.K_r]:
                    g.reset()

                if pygame.key.get_pressed()[pygame.K_d]:
                    g.clear()

            if event.type == pygame.MOUSEBUTTONUP:
                to_move = 0

            if to_move:
                g.vertices[to_move - 1].x = mouse_pos_x
                g.vertices[to_move - 1].y = mouse_pos_y

            if event.type == pygame.MOUSEBUTTONDOWN:
                match mode:
                    case "VERT":
                        if pygame.mouse.get_pressed() == (1, 0, 0):
                            for (idx, vert) in enumerate(g.vertices, 1):
                                if (vert.x > mouse_pos_x - 16) and (
                                        vert.x < mouse_pos_x + 16) and (
                                        vert.y > mouse_pos_y - 16) and (
                                        vert.y < mouse_pos_y + 16):
                                    to_move = idx
                                    break
                            else:
                                g.add(*pygame.mouse.get_pos())

                        if pygame.mouse.get_pressed() == (0, 0, 1):
                            for (idx, vert) in enumerate(g.vertices, 1):
                                if (vert.x > mouse_pos_x - 16) and (vert.x < mouse_pos_x + 16) and (
                                        vert.y > mouse_pos_y - 16) and (
                                        vert.y < mouse_pos_y + 16):
                                    g.delete(idx)

                    case "CONN":
                        if pygame.mouse.get_pressed() == (0, 0, 1):
                            if to_connect:
                                to_connect = 0
                            else:
                                delete_edge(g, mouse_pos_x, mouse_pos_y)

                        if pygame.mouse.get_pressed() == (1, 0, 0):
                            for (idx, vert) in enumerate(g.vertices, 1):
                                if (vert.x > mouse_pos_x - 16) and (vert.x < mouse_pos_x + 16) and (
                                        vert.y > mouse_pos_y - 16) and (
                                        vert.y < mouse_pos_y + 16):
                                    if to_connect and (idx != to_connect):
                                        g.connect(idx, to_connect)
                                        to_connect = 0
                                    else:
                                        to_connect = idx

        screen.fill((255, 255, 255))
        if to_connect:
            pygame.draw.line(screen, (0, 0, 0), start_pos=(g.vertices[to_connect - 1].x, g.vertices[to_connect - 1].y),
                             end_pos=(mouse_pos_x, mouse_pos_y), width=2)
        draw(screen, g)

        font = pygame.font.SysFont('couriernew', 40)
        text = font.render(f"{mode}", True, (0, 0, 0))
        screen.blit(text, (50, 750))

        font = pygame.font.SysFont('couriernew', 15)
        text = font.render("V - switch to CONN, C - switch to VERT, D - clear graph", True, (0, 0, 0))
        screen.blit(text, (200, 700))
        text = font.render("F - colour graph, R - reset all vertices to white colour", True, (0, 0, 0))
        screen.blit(text, (200, 725))
        text = font.render("VERT: LMB - create a vertex, RMB - delete a vertex, LMB(hold and drag) - move a vertex",
                           True, (0, 0, 0))
        screen.blit(text, (200, 750))
        text = font.render("CONN: LMB - connect a vertex, RMB(while connecting) - cancel, RMB - delete an edge",
                           True, (0, 0, 0))
        screen.blit(text, (200, 775))

        pygame.display.flip()


if __name__ == "__main__":
    main()
