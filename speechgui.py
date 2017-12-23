import Tkinter as tk
import ttk
import ScrolledText
import tkFileDialog
from threading import Thread

from transcriber import WAVTranscriber

#Language choice
LANGUAGES = ['en-US', 'hi-IN', 'en-IN']

root = tk.Tk(className="speech transcriber")

#All the logs will be written in this text area
logPad = ScrolledText.ScrolledText(root, width=70, height=20)

v = tk.IntVar()
tk.Label(root, text="Choose the speech language", justify = tk.LEFT, padx=20).pack()
tk.Radiobutton(root, text="US English", padx=20, variable=v, value=0).pack(anchor=tk.W)
tk.Radiobutton(root, text="Hindi", padx=20, variable=v, value=1).pack(anchor=tk.W)
tk.Radiobutton(root, text="Indian English", padx=20, variable=v, value=2).pack(anchor=tk.W)

#Text box for file address.
filebrowse = tk.Frame(height=2, bd=1, relief=tk.SUNKEN)
filebrowse.pack(fill=tk.X, padx=5, pady=5)
tk.Label(filebrowse, text = "Input File", justify = tk.LEFT, padx=20).pack()
namelabel = tk.Text(filebrowse, height = 2, width=60)
namelabel.pack(side=tk.LEFT)

def fileCallback():
    filename = tkFileDialog.askopenfile(parent=root, mode="rb", title="Select a file")
    if filename:
        namelabel.delete("1.0", tk.END)
        namelabel.insert(tk.END, filename.name)

namebutton = tk.Button(filebrowse, text="Browse", command=fileCallback)
namebutton.pack(side=tk.RIGHT)

progress = ttk.Progressbar(root, mode="determinate", length=400, orient=tk.HORIZONTAL, maximum=100)
progress.pack()
logPad.pack()

def wavtranscribe():
    outfile = tkFileDialog.asksaveasfilename(parent=root, title="Select output file")
    if not outfile:
        outfile = "output.txt"
    try:
        infile = namelabel.get("1.0", "end-1c")
        transcriber = WAVTranscriber(infile, LANGUAGES[int(v.get())])
    except AttributeError as err:
        logPad.insert(tk.END, str(err) + "\n")
        root.update_idletasks()
        return
    logPad.insert(tk.END, "File is OK, now starting transcription\n")
    root.update_idletasks()
    def threadtarget():
        with open(outfile, "w") as op:
            for result in transcriber:
                op.write(result)
                op.write("\n\n")
                # Update progress bar here
                percent = transcriber.getelapsedpercentage()
                progress["value"] = percent
                root.update_idletasks()
        logPad.insert(tk.END, "Transcription Completed!!\n")
        root.update_idletasks()

    thread = Thread(target=threadtarget)
    thread.start()

transcribe = tk.Button(root, text="Transcribe!", command=wavtranscribe)
transcribe.pack()
root.mainloop()
