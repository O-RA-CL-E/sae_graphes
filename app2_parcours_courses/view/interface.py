import tkinter as tk
from tkinter import messagebox

class Interface:
    def __init__(self, controleur):
        self.controleur = controleur
        self.fenetre = tk.Tk()
        self.fenetre.title("App Courses")
    
    def afficher_menu_principal(self):
        tk.Label(self.fenetre, text="Choisir un magasin:").pack()
        
        tk.Button(
            self.fenetre,
            text="Charger",
            command=self.charger_magasin
        ).pack()
        
        self.fenetre.mainloop()
    
    def charger_magasin(self):
        if self.controleur.charger_projet("projets/mon_magasin"):
            messagebox.showinfo("Succès", "Magasin chargé!")
        else:
            messagebox.showerror("Erreur", "Échec du chargement")
