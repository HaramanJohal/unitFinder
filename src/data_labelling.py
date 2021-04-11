import os
import tkinter as tk


class Labeller:
    def __init__(self, label_path):
        self.label_path = label_path
        self.labels = self.load_labels(label_path)
        self.exit = False
        self.delete = False

    def load_labels(self, label_path):
        labels = []
        with open(label_path, "r") as f:
            for label in f.readlines():
                labels.append(label.rstrip())
        return labels

    def handle_select_label(self, label):
        self.label = label
        self.window.destroy()

    def make_label_button(self, label, color, frame):
        return tk.Button(
            text=label,
            width=25,
            height=5,
            bg=color,
            fg="white",
            command=lambda: self.label_data(label),
            master=frame
        )

    def handle_confirm_new_label(self, new_label):
        with open(label_path, "a") as f:
            f.write(f"\n{new_label}")
        self.labels.append(new_label)
        self.label = new_label
        self.window.destroy()

    def exit_labeller(self):
        self.exit = True
        self.label = None
        self.window.destroy()

    def delete_entry(self):
        self.label = None
        self.delete = True
        self.window.destroy()

    def get_label(self, index, number, text):
        self.delete = False
        self.window = tk.Tk()

        tk.Label(text=f"{number}").grid(row=0, column=0, pady=5, columnspan=len(self.labels))
        tk.Label(text=f"'{text}'", wraplength=1500).grid(row=1,column=0, columnspan=len(self.labels))
        
        entry = tk.Entry()
        entry.insert(0, "New label")
        entry.grid(row=2, column=0, columnspan=len(self.labels))
        tk.Button(
            text="confirm",
            command=lambda: self.handle_confirm_new_label(entry.get())
        ).grid(row=2, column=1, columnspan=len(self.labels))

        tk.Button(
            text="delete",
            command=self.delete_entry
        ).grid(row=3, column=0, columnspan=len(self.labels))

        tk.Button(
            text="save and quit",
            command=self.exit_labeller
        ).grid(row=4, column=0, columnspan=len(self.labels))
        
        
        colors = ["green", "orange", "red", "purple", "blue"]
        for i, label in enumerate(self.labels):
            tk.Button(
                text=label,
                width=25,
                height=5,
                bg=colors[i % 5],
                fg="white",
                command=lambda label=label: self.handle_select_label(label),
            ).grid(row=5+(i//7),column=i%7)
            

        self.window.mainloop()
        return self.label, self.exit, self.delete


if __name__ == "__main__":
    delimiter = os.environ["DATA_DELIMITER"]

    label_path = "data/labels.txt"
    labeller = Labeller(label_path)


    lines_to_delete = []
    with open("data/scrapedData.txt", "r") as fin:
        lines = list(fin.readlines())
        with open("data/labelledData.txt", "a") as fout:
            for line in lines:
                (index, number, text) = line.split(delimiter)
                label, exit, delete = labeller.get_label(index, number, text)

                if exit:
                    break

                lines_to_delete.append(line)

                if delete:
                    print(f"deleting irrelevant entry : {line}")
                    continue

                print(f"labelling example as {label}")
                fout.write(f"{label}{delimiter}{index}{delimiter}{number}{delimiter}{text}")
    
    with open("data/scrapedData.txt", "w") as f:
        f.write("".join([line for line in lines if line not in lines_to_delete]))
