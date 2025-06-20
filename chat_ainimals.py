import tkinter as tk
from tkinter import ttk
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = ">>INSERISCI QUI LA KEY<<"

class MainFrame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI Animal Chat")
        self.root.config(bg="#2B2B2B")
        self.root.geometry("500x600")

        # Regole per i vari animali
        self.rules_dict = {
        "Cane": "Sei un cane molto amichevole ed energico. Parli come un cane che sa parlare, descrivendo scodinzolii, ansimare e azioni giocose. Ami l'attenzione e vuoi rendere felice l'utente.",
        "Gatto": "Sei un gatto calmo ed elegante. Di tanto in tanto fai le fusa, ti stiri o ti mostri indifferente. Parli con mistero e classe.",
        "Volpe": "Sei una volpe astuta e curiosa. Parli con arguzia e agilità. Descrivi movimenti furtivi o rapidi.",
        "Pappagallo": "Sei un pappagallo intelligente, giocherellone. Ti piace scherzare e a volte ti capita di ripetere le parole. Ti muovi in modo giocoso ed energico."
        }

        self.selected_animal = None
        self.chat_history = []

        self.create_interface()
        self.chiedi_animale()


    def create_interface(self):
        self.chat_frame = tk.Frame(self.root, bg="#1E1E1E")
        self.chat_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.chat_frame, bg="#1E1E1E")

        style= ttk.Style()
        style.theme_use('classic')
        style.configure(
            "Vertical.TScrollbar",
            gripcount=0,
            background="#6D6D6D",
            troughcolor="#1E1E1E",
            bordercolor="#444444",
            arrowcolor="#6D6D6D"
        )

        self.scrollbar = ttk.Scrollbar(
            self.chat_frame,
            orient="vertical",
            command=self.canvas.yview,
            style="Vertical.TScrollbar"
        )
        self.scrollable_frame = tk.Frame(self.canvas, bg="#1E1E1E")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion= self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window= self.scrollable_frame, anchor= "nw")
        self.canvas.configure(yscrollcommand= self.scrollbar.set)

        self.canvas.pack(side= "left", fill= "both", expand= True)
        self.scrollbar.pack(side= "right", fill= "y")

        # Entry + Button
        self.entry = tk.Entry(self.root, width=80, bg= "#444444")
        self.entry.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)
        self.entry.bind("<Return>", self.chat_domanda_event)

        self.send_button = tk.Button(self.root, text="Invia", command=self.chat_domanda, bg= "#6D6D6D")
        self.send_button.pack(side=tk.RIGHT, padx=10)

    def chiedi_animale(self):
        popup = tk.Toplevel(self.root)
        popup.title("Scegli animale")
        popup.geometry("300x200")
        tk.Label(popup, text="Seleziona il tuo animale:", font=("Arial", 12)).pack(pady=10)

        for animale in self.rules_dict:
            btn = tk.Button(popup, text=animale.capitalize(), width=20,
                            command=lambda a=animale: self.set_animale(a, popup))
            btn.pack(pady=5)

    def set_animale(self, animale, popup):
        self.selected_animal = animale
        system_prompt = {"role": "system", "content": self.rules_dict[animale]}
        self.chat_history = [system_prompt]
        popup.destroy()
        self.aggiungi_messaggio(f"Stai parlando con {animale}.", lato="left", colore_bordo="#6D96FF", bg="#444444")

    def chat_domanda_event(self, event):
        self.chat_domanda()

    def chat_domanda(self):
        domanda = self.entry.get().strip()
        if not domanda:
            return
        self.entry.delete(0, tk.END)

        self.aggiungi_messaggio(f"You: {domanda}", lato="right", colore_bordo="#777777", bg="#444444")
        risposta = self.chat_risposta(domanda)
        self.aggiungi_messaggio(f"{self.selected_animal.capitalize()}: {risposta}", lato="left", colore_bordo="#6D96FF", bg="#222")

    def chat_risposta(self, domanda):
        try:
            self.chat_history.append({"role": "user", "content": domanda})
            risposta = openai.chat.completions.create(
                model="gpt-4.1-nano",
                messages=self.chat_history,
                max_tokens=150,
                temperature=0.8
            )
            contenuto = risposta.choices[0].message.content.strip()
            self.chat_history.append({"role": "assistant", "content": contenuto})
            return contenuto
        except Exception as e:
            return f"Errore: {str(e)}"

    def aggiungi_messaggio(self, testo, lato="left", colore_bordo="blue", bg="#444444"):
        box = tk.Frame(self.scrollable_frame, bg="#1E1E1E", bd=2, relief=tk.RIDGE)
        label = tk.Label(box, text=testo, wraplength=400, justify="left", bg=bg, fg="white", padx=10, pady=5,
                         font=("Arial", 10), bd=2, relief="solid", highlightbackground= colore_bordo,
                         highlightthickness=2)
        label.pack()
        box.pack(anchor="e" if lato == "right" else "w", pady=5, padx=10)
        self.root.update_idletasks()
        self.canvas.yview_moveto(1.0)

if __name__ == "__main__":
    app = MainFrame()
    app.root.mainloop()