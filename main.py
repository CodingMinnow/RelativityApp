import tkinter as tk
from tkinter import filedialog
import os

paths = ()
directory = ''
paths_new = []
button_color = '#add8e6'
button_text_color = 'black'

# Change state of all buttons
def flip_btns(state):
    btn_preview.config(state=state)
    btn_preview.config(state=state)
    btn_change.config(state=state)

# Get Relativity exported files
def get_files():
    # Reset files count, directory, selection and preview displays, and preview button
    selection_count.config(text='Total Files: 0')
    selection_path.delete('1.0', 'end')
    selection_path.insert('insert', 'Not selected.')
    selected_listbox.delete(0, tk.END)
    preview_listbox.delete(0, tk.END)
    btn_preview.config(state='disabled')

    # get files
    global paths
    paths = filedialog.askopenfilenames(title="Select file(s)")

    # if files selected
    if len(paths):
        # delete any warnings
        selection_warning.config(text='')

        global directory
        directory = os.path.dirname(os.path.realpath(paths[0]))

        # update selection descriptions
        selection_count.config(text='Total Files: ' + str(len(paths)))
        selection_path.delete('1.0', 'end')
        selection_path.insert('insert', directory)

        # display selected files
        for file in paths:
            selected_listbox.insert('end', os.path.basename(file))

        # activate preview button
        btn_preview.config(state='normal')
    # if no files are selected
    else:
        selection_warning.config(text='You must select files.')


# Display preview changes
def preview():
    # inform user of start of progress
    preview_progress.config(text='In progress...')

    # dictionary of repeating filenames
    dict_filenames = {}

    # get new filenames
    global paths_new
    for file in paths:
        filename = os.path.basename(file)
        filename_new = filename
        split_result = filename.split('_', 1)

        # remove numerical prefix
        if len(split_result) > 1 and split_result[0].isnumeric():
            filename_new = split_result[1]

        # check dictionary for file name
        if filename_new in dict_filenames:
            # increase counter
            dict_filenames[filename_new] += 1

            # add numerical suffix to file name
            split_ext = os.path.splitext(filename_new)
            filename_new = split_ext[0] + ' (' + str(dict_filenames[filename_new]-1) + ')' + split_ext[1]
        else:
            dict_filenames[filename_new] = 1

        # if there were changes in the filename
        if filename == filename_new:
            # display
            preview_listbox.insert('end', 'No changes')
        else:
            # store new filename
            paths_new.append((file, filename_new))

            # display
            preview_listbox.insert('end', filename_new)

    # inform user that ready to preview
    preview_progress.config(text='Done! Proceed to preview.')

    # activate preview button
    btn_change.config(state='normal')


def apply_changes():
    # Disable all buttons
    flip_btns('disabled')

    # Inform user of start of progress
    change_progress.config(text='In progress...')

    # Rename filenames
    count_paths_change = len(paths_new)
    while count_paths_change > 0:
        (old, new) = paths_new[count_paths_change - 1]
        os.rename(old, directory + '\\' + new)
        count_paths_change -= 1

    # inform user that ready to preview
    change_progress.config(text='Done!')

    # Enable all buttons
    flip_btns('normal')

# Window object
root = tk.Tk()
root.title('Remove number prefixes from Relativity exports')
root.geometry('800x600')
root.minsize(800, 500)

# Frame 1: instructions
fr_inst = tk.Frame(root)
fr_inst.place(relx=0.5, rely=0.05, relwidth=0.7, height=60, anchor='n')

# Frame 2: starting point
fr_start = tk.Frame(root)
fr_start.place(relx=0.5, rely=0.2, width=250, height=100, anchor='n')

# Frame 3: main
fr_main = tk.Frame(root)
fr_main.place(relx=0.5, rely=0.4, relwidth=0.7, relheight=0.5, anchor='n')

# Frame 4: selected files display
fr_selected = tk.Frame(fr_main)
fr_selected.place(relx=0.20, relwidth=0.4, relheight=1, anchor='n')

# Frame 5: preview display
fr_preview = tk.Frame(fr_main)
fr_preview.place(relx=0.8, relwidth=0.4, relheight=1, anchor='n')

# Instructions for user
inst_txt = 'Instructions: Remove the numerical prefixes from Relativity exported documents.\nFirst, click on the ' \
           'button \'Select Files\' to select the exported Relativity files.\nThen, review the changes before ' \
           'clicking \'Change\' to implement the change. '
inst = tk.Label(fr_inst, text=inst_txt, font='Arial 10', justify='left')
inst.grid()

# Button to select files
btn_get_files = tk.Button(fr_start, text='Select Files', bg=button_color, fg=button_text_color, font='Arial 8 bold', command=get_files)
btn_get_files.place(relwidth=1, height=25)

# Warning to select files
selection_warning = tk.Label(fr_start, font='Arial 8 italic', justify='left')
selection_warning.place(y=30, height=15)

# Selected file(s) count
selection_count = tk.Label(fr_start, text='Total Files: 0', font='Arial 8', justify='left')
selection_count.place(y=45, height=15)

# Directory of selected file(s)
selection_path_label = tk.Label(fr_start, text='Folder: ', font='Arial 8')
selection_path_label.place(y=60, height=15)
selection_path = tk.Text(fr_start, wrap='char', font='Arial 8')
selection_path.insert('insert', 'Not selected.')
selection_path.place(x=50, y=65, relwidth=0.75, height=30)

# Selected file(s) display
selected_files_label = tk.Label(fr_selected, text='Selected File(s)', font='Arial 9 bold underline', justify='left')
selected_files_label.place(height=15)
selected_scrollbar = tk.Scrollbar(fr_selected)
selected_listbox = tk.Listbox(fr_selected, yscrollcommand=selected_scrollbar.set)
selected_listbox.place(y=20, relx=0, relwidth=0.95, relheight=0.75, anchor='nw')
selected_scrollbar.place(y=20, relx=1, relwidth=0.05, relheight=0.75, anchor='ne')
selected_scrollbar.config(command=selected_listbox.yview)

# Button to preview changes
btn_preview = tk.Button(fr_selected, text='See Preview', bg=button_color, fg=button_text_color, font='Arial 8 bold', state='disabled',
                        command=preview)
btn_preview.place(rely=1, relwidth=0.4, height=20, anchor='sw')

# Progress label for preview
preview_progress = tk.Label(fr_selected, font='Arial 8 italic')
preview_progress.place(relx=1, rely=1, relwidth=0.6, height=20, anchor='se')

# Arrow between displays
arrow = tk.Label(fr_main, text='========>>>', font='Arial 10 bold')
arrow.place(relx=0.5, rely=0.4, relheight=0.2, relwidth=0.2, anchor='n')

# Preview file(s) display
preview_files_label = tk.Label(fr_preview, text='Preview Change(s)', font='Arial 9 bold underline', justify='left')
preview_files_label.place(height=15)
preview_scrollbar = tk.Scrollbar(fr_preview)
preview_listbox = tk.Listbox(fr_preview, yscrollcommand=preview_scrollbar.set)
preview_listbox.place(y=20, relx=0, relwidth=0.95, relheight=0.75, anchor='nw')
preview_scrollbar.place(y=20, relx=1, relwidth=0.05, relheight=0.75, anchor='ne')
preview_scrollbar.config(command=preview_listbox.yview)

# Button to apply changes
btn_change = tk.Button(fr_preview, text='Apply Changes', bg=button_color, fg=button_text_color, font='Arial 8 bold',
                       state='disabled', command=apply_changes)
btn_change.place(rely=1, relwidth=0.4, height=20, anchor='sw')

# Progress label for changes
change_progress = tk.Label(fr_preview, font='Arial 8 italic')
change_progress.place(relx=1, rely=1, relwidth=0.6, height=20, anchor='se')

root.mainloop()
