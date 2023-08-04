from tkinter import ttk, filedialog, messagebox, IntVar
import tkinter as tk
import sv_ttk
import os, subprocess, shutil, shlex, threading, time
from subprocess import CREATE_NO_WINDOW

def copy_to_process():
  global path, destination_path
  path = get_entry_value(inputTextBox)
  destination_path = "video.mp4"
  shutil.copyfile(path, destination_path)

def startResamplingProcess():
  
  #PrepareValue
  resamplingStartButton.config(state='disable')
  fpsAmountTextBox.config(state='disable')
  crfValueTextBox.config(state='disable')

  time.sleep(1)

  fpsAmount = get_entry_value(fpsAmountTextBox)
  os.environ["fpsAmount"] = fpsAmount

  copy_to_process()

  #os.environ["filename"] = destination_path

  fpsAmount = int(fpsAmount)
  framesAmount = (fpsAmount / 60) - 1
  crfValue = get_entry_value(crfValueTextBox)
  gpu = '-preset ultrafast -c:v libx264 -movflags faststart'

  os.environ["framesAmount"] = str(int(framesAmount))
  #os.environ["crfValue"] = crfValue
  #os.environ["gpu"] = gpu

  os.system('echo LoadPlugin("ffms2.dll"^) > avsscript.avs')
  os.system('echo LoadPlugin("ClipBlend_x64.dll"^) >> avsscript.avs')
  os.system(f'echo FFMS2("{destination_path}"^) >> avsscript.avs')
  os.system('echo ClipBlend(delay=%framesAmount%^) >> avsscript.avs')
  os.system('echo changefps(60, linear=false^) >> avsscript.avs')

  time.sleep(3)

  #ffmpegProcessing
  def ffmpegResampleProcessing():
    command = shlex.split(f'ffmpeg -y -i avsscript.avs -v quiet -stats -i {destination_path} {gpu} -crf {crfValue} -c:a copy out/output-{fpsAmount}fps-resampled.mp4')
    subprocess.run(command, creationflags=subprocess.CREATE_NO_WINDOW)

    consoleTextBox.config(state='normal')
    consoleTextBox.delete("1.0", "end")
    consoleTextBox.insert('1.0', 'Clearing tmp file...')
    consoleTextBox.config(state='disable')

    os.system(f'DEL /F /Q {destination_path}.ffindex')
    os.system('DEL /F /Q avsscript.avs')
    os.system(f'DEL /F /Q {destination_path}')
    time.sleep(5)

    consoleTextBox.config(state='normal')
    consoleTextBox.delete("1.0", "end")
    consoleTextBox.insert('1.0', 'Stopped')
    consoleTextBox.config(state='disable')

    resamplingStartButton.config(state='normal')
    fpsAmountTextBox.config(state='normal')
    crfValueTextBox.config(state='normal')

    if os.path.exists('out') == False:
      messagebox.showerror('Error', 'Missing "out" dir!')
    else:
      messagebox.showinfo('Complete', 'Complete')

  Resamplingthread = threading.Thread(target=ffmpegResampleProcessing)
  Resamplingthread.start()
  consoleTextBox.config(state='normal')
  consoleTextBox.delete("1.0", "end")
  consoleTextBox.insert('1.0', 'Starting...')
  consoleTextBox.config(state='disable')
  
def selectInputFile():
    File = filedialog.askopenfilename(title='Choose a file', filetypes = (("Video file","*.mp4"),("All files","*.*")))
    inputTextBox.configure(state='normal')
    inputTextBox.delete(0, 'end')
    inputTextBox.insert(0, File)
    inputTextBox.configure(state='disabled')

def get_entry_value(entry):
  return entry.get()


root =tk.Tk()
root.geometry('500x450')
root.title('BS-GUI')
sv_ttk.set_theme("dark")

tab_control = ttk.Notebook(root)

#Input
inputLableFrame = ttk.LabelFrame(root, text='Input')
inputLableFrame.pack(fill="both", padx = 10, pady = 10)
inputTextBox = ttk.Entry(inputLableFrame, state='disable')
inputTextBox.pack(side= 'left', fill='x', expand='True', padx=10, pady=10)
browserFile = ttk.Button(inputLableFrame, text="Select...", command=selectInputFile)
browserFile.pack(side= 'left', fill='x', expand='False', padx=10, pady=10)

#================================Resampling================================#
tab1 = ttk.Frame(tab_control)
tab_control.add(tab1, text='Resampling')

#FPS
resamplingLableFrame_FPS = ttk.LabelFrame(tab1, text='FPS')
resamplingLableFrame_FPS.pack(fill='x', padx=10, pady=5)
fpsAmountTextBox = ttk.Entry(resamplingLableFrame_FPS)
fpsAmountTextBox.pack(fill='x', padx=10, pady=10)

#crfValue
resamplingLableFrame_crf = ttk.LabelFrame(tab1, text='crfValue')
resamplingLableFrame_crf.pack(fill='x', padx=10, pady=5)
crfValueTextBox = ttk.Entry(resamplingLableFrame_crf)
crfValueTextBox.pack(fill='x', padx=10, pady=10)

#Num Only
crfValueTextBox.config(validate="key", validatecommand=(crfValueTextBox.register(lambda x: x.isdigit()), "%P"))
fpsAmountTextBox.config(validate="key", validatecommand=(fpsAmountTextBox.register(lambda x: x.isdigit()), "%P"))

#StartButton
resamplingStartButton = ttk.Button(tab1, text='Start!', command=startResamplingProcess)
resamplingStartButton.pack(fill='x', padx=10, pady=10)



#================================END================================#


#================================ReduceFS================================#
tab2 = ttk.Frame(tab_control)
tab_control.add(tab2, text='Reduce Size')

#Quality Loss

reduceFSFrame_LossCRF = ttk.LabelFrame(tab2, text='Choose quality loss')
reduceFSFrame_LossCRF.pack(fill='x', padx=10, pady=5)

lossCRFOption = IntVar()

ttk.Radiobutton(reduceFSFrame_LossCRF, text='Low', variable=lossCRFOption, value=1).pack(side='left', padx=10, pady=10)
ttk.Radiobutton(reduceFSFrame_LossCRF, text='Medium', variable=lossCRFOption, value=2).pack(side='left', padx=10, pady=10)
ttk.Radiobutton(reduceFSFrame_LossCRF, text='High', variable=lossCRFOption, value=3).pack(side='left', padx=10, pady=10)
ttk.Radiobutton(reduceFSFrame_LossCRF, text='Insane', variable=lossCRFOption, value=4).pack(side='left', padx=10, pady=10)

#StartButton
reduceFSStartButton = ttk.Button(tab2, text='Start!')
reduceFSStartButton.pack(fill='x', padx=10, pady=10)






#================================END================================#
tab_control.pack(fill='both')

#Console
ConsoleEntry = ttk.LabelFrame(root, text='Status')
ConsoleEntry.pack(fill='x', padx=10, pady=5)
consoleTextBox = tk.Text(ConsoleEntry, state="disabled")
consoleTextBox.pack(padx=10, pady=10)
consoleTextBox.config(state='normal')
consoleTextBox.insert('1.0', 'Stopped')
consoleTextBox.config(state='disable')
root.mainloop()


#Test
print(lossCRFOption.get())