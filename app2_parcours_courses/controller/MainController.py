from model.magasin import Magasin

class MainController:
    def __init__(self, view):
        self.view = view
        self.magasin = None
        self.view.load_btn.clicked.connect(self.charger_magasin)
        self.view.products_list.itemDoubleClicked.connect(self.ajouter_a_courses)
        self.view.generate_random_list_btn.clicked.connect(self.generer_liste_aleatoire)
        self.view.shortest_path_btn.clicked.connect(self.tracer_chemin_plus_court)
        self.view.courses_list.itemDoubleClicked.connect(self.retirer_de_courses)

    def charger_magasin(self):
        from PyQt5.QtWidgets import QFileDialog
        path, _ = QFileDialog.getOpenFileName(self.view, "Charger un magasin", "", "JSON (*.json)")
        if path:
            try:
                self.magasin = Magasin(path)
                self.view.afficher_plan_avec_grille(
                    self.magasin.image_path,
                    self.magasin.nb_cols,
                    self.magasin.nb_rows,
                    produits=self.magasin.products
                )
                self.view.products_list.clear()
                for prod in self.magasin.products:
                    nom = prod.get("label", "Produit sans nom")
                    self.view.products_list.addItem(nom)
            except Exception as e:
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.critical(self.view, "Erreur", f"Erreur lors du chargement : {e}")

    def ajouter_a_courses(self, item):
        self.view.courses_list.addItem(item.text())

    def retirer_de_courses(self, item):
        row = self.view.courses_list.row(item)
        self.view.courses_list.takeItem(row)

    def generer_liste_aleatoire(self):
        import random
        if not self.magasin or not self.magasin.products:
            return
        self.view.courses_list.clear()
        nb_produits = min(5, len(self.magasin.products))
        produits_aleatoires = random.sample(self.magasin.products, nb_produits)
        for prod in produits_aleatoires:
            nom = prod.get("label", "Produit sans nom")
            self.view.courses_list.addItem(nom)

    def tracer_chemin_plus_court(self):
        if not self.magasin or not self.magasin.products:
            return
        from PyQt5.QtGui import QImage, QColor
        import os

        start = (31, 31)  # updated start as per user request
        # Get product labels from shopping list
        shopping_list_labels = [self.view.courses_list.item(i).text() for i in range(self.view.courses_list.count())]
        # Map shopping list labels to product positions
        products_positions = []
        for label in shopping_list_labels:
            for prod in self.magasin.products:
                if prod.get("label", "") == label:
                    pos = (prod.get("col", 0), prod.get("row", 0))
                    products_positions.append(pos)
                    break

        # Load image to analyze walkable cells
        full_path = os.path.join("projets", self.magasin.image_path) if not os.path.isabs(self.magasin.image_path) else self.magasin.image_path
        image = QImage(full_path)
        if image.isNull():
            return

        # Build walkability grid: True if cell is mostly white
        walkable = [[False]*self.magasin.nb_rows for _ in range(self.magasin.nb_cols)]
        for col in range(self.magasin.nb_cols):
            for row in range(self.magasin.nb_rows):
                # Sample multiple pixels around center of cell (3x3 grid)
                cell_width = image.width() / self.magasin.nb_cols
                cell_height = image.height() / self.magasin.nb_rows
                center_x = int((col + 0.5) * cell_width)
                center_y = int((row + 0.5) * cell_height)
                white_found = False
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        x = min(max(center_x + dx, 0), image.width() - 1)
                        y = min(max(center_y + dy, 0), image.height() - 1)
                        color = QColor(image.pixel(x, y))
                        if color.red() > 180 and color.green() > 180 and color.blue() > 180:
                            white_found = True
                            break
                    if white_found:
                        break
                if white_found:
                    walkable[col][row] = True
        # Force start cell to be walkable
        start = (33, 31)
        walkable[start[0]][start[1]] = True

        # Mark forbidden cells as not walkable
        forbidden_cells = [(col, 31) for col in range(4, 27)]
        for cell in forbidden_cells:
            walkable[cell[0]][cell[1]] = False

        # Mark product cells as not walkable to avoid passing through them
        for pos in products_positions:
            walkable[pos[0]][pos[1]] = False
        # Debug print walkable count
        walkable_count = sum(sum(1 for cell in col if cell) for col in walkable)
        print(f"Walkable cells count: {walkable_count}")
        # Debug print walkability of start and product cells
        print(f"Start cell walkable: {walkable[start[0]][start[1]]}")
        for idx, prod in enumerate(self.magasin.products):
            pos = (prod.get("col", 0), prod.get("row", 0))
            print(f"Product {idx} at {pos} walkable: {walkable[pos[0]][pos[1]]}")

        self.walkable = walkable  # store for use in _get_neighbors

        full_path = []
        current_start = start
        remaining_products = products_positions.copy()
        while remaining_products:
            best_target = None
            best_segment = None
            best_adj = None
            best_length = None
            for target in remaining_products:
                adjacents = [(target[0] + dx, target[1] + dy) for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]]
                adjacents = [pos for pos in adjacents if 0 <= pos[0] < self.magasin.nb_cols and 0 <= pos[1] < self.magasin.nb_rows and walkable[pos[0]][pos[1]]]
                if not adjacents:
                    print(f"No adjacent walkable cell found for product at {target}")
                    continue
                for adj in adjacents:
                    segment = self._bfs_shortest_path(current_start, adj)
                    if segment is not None and (best_length is None or len(segment) < best_length):
                        best_segment = segment
                        best_target = target
                        best_adj = adj
                        best_length = len(segment)
            if best_segment is None:
                print(f"No path found from {current_start} to any remaining product")
                break
            if full_path and best_segment[0] == full_path[-1]:
                best_segment = best_segment[1:]
            full_path.extend(best_segment)
            current_start = best_adj
            remaining_products.remove(best_target)

        if full_path:
            print(f"Total path length: {len(full_path)}")
            path_points = [{"col": p[0], "row": p[1], "label": ""} for p in full_path]
            # Add red points for products to indicate collection
            red_points = [{"col": pos[0], "row": pos[1], "label": "", "color": "red"} for pos in products_positions]
            self.view.afficher_plan_avec_grille(
                self.magasin.image_path,
                self.magasin.nb_cols,
                self.magasin.nb_rows,
                produits=self.magasin.products + red_points,
                chemin=path_points
            )

    def _bfs_shortest_path(self, start, goal):
        from collections import deque
        # Queue holds tuples: (position, previous_direction, turn_count)
        queue = deque()
        queue.append((start, None, 0))
        visited = {start: (None, 0)}  # position: (parent, turn_count)

        while queue:
            current, prev_dir, turn_count = queue.popleft()
            if current == goal:
                break
            neighbors = self._get_neighbors(current)
            for neighbor in neighbors:
                if neighbor not in visited or visited[neighbor][1] > turn_count:
                    # Calculate direction from current to neighbor
                    dir = (neighbor[0] - current[0], neighbor[1] - current[1])
                    # Calculate new turn count
                    new_turn_count = turn_count
                    if prev_dir is not None and dir != prev_dir:
                        new_turn_count += 1
                    # Allow stepping on goal even if not walkable
                    if neighbor == goal or not (hasattr(self, "walkable") and not self.walkable[neighbor[0]][neighbor[1]]):
                        if neighbor not in visited or visited[neighbor][1] > new_turn_count:
                            visited[neighbor] = (current, new_turn_count)
                            queue.append((neighbor, dir, new_turn_count))

        if goal not in visited:
            return None

        # Reconstruct path
        path = []
        step = goal
        while step is not None:
            path.append(step)
            step = visited[step][0]
        path.reverse()
        return path

    def _get_neighbors(self, pos):
        col, row = pos
        neighbors = []
        for dcol, drow in [(-1,0),(1,0),(0,-1),(0,1)]:
            ncol, nrow = col + dcol, row + drow
            if 0 <= ncol < self.magasin.nb_cols and 0 <= nrow < self.magasin.nb_rows:
                # Check walkability
                if hasattr(self, "walkable") and not self.walkable[ncol][nrow]:
                    continue
                neighbors.append((ncol, nrow))
        return neighbors
