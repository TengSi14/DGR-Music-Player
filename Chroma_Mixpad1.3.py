import tkinter as tkr
import sqlite3
from pygame import mixer
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image


def browsefile(msc_key, lbl_key):
    if mode_now == 'create':
        file_path = tkr.filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("OGG files", ".ogg"),("all files", ".*")))
        get_fname = (file_path.split('/')[::-1])    # for reverse printing of filepath
        fname = get_fname[0]
        lbl_key['text'] = fname
        song_dict.update({msc_key:{'file':file_path, 'fname':fname}})
    else:
        file_path = tkr.filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("OGG files", ".ogg"),("all files", ".*")))
        get_fname = (file_path.split('/')[::-1])    # for reverse printing of filepath
        fname = get_fname[0]
        lbl_key['text'] = fname
        mod_pl_dict.update({msc_key:{'file':file_path, 'fname':fname}})


def play_msc(ply_msc_key):
    song=song_dict[ply_msc_key]['file']
    mixer.music.load(song)
    mixer.music.play()


def resume_msc():
    mixer.music.unpause()


def pause_msc():
    mixer.music.pause()


def stop_msc():
    mixer.music.stop()


def logout():
    lo_response = tkr.messagebox.askyesno('Exit', 'Are you sure you want to exit?')
    if lo_response:
        mainscrn.destroy()
        exit(0)
    else:
        pass


def cancel_btn():
    prof_scrn.destroy()


def save_new_playlist():
    for i in song_dict:
        save_fpath = song_dict[i]['file']
        save_fname = song_dict[i]['fname']
        cn = sqlite3.connect('dgr.db')
        c = cn.cursor()
        c.execute('INSERT INTO playlist VALUES(:mkey, :path, :fname)',
            {
                'mkey': i,
                'path': save_fpath,
                'fname': save_fname
            })
        cn.commit()
        cn.close()
    tkr.messagebox.showinfo('Successfully Created!', 'Playlist is Ready!')
    prof_scrn.destroy()


def mod_playlist():
    cn = sqlite3.connect('dgr.db')
    c = cn.cursor()
    for mod_song in mod_pl_dict:
        edit_msc_key = mod_song
        edit_path = mod_pl_dict[mod_song]['file']
        edit_fname = mod_pl_dict[mod_song]['fname']
        c.execute('UPDATE playlist SET path = :fpath, filename = :fname WHERE msc_key = :mkey',
            {
            'fpath': edit_path,
            'fname': edit_fname,
            'mkey': edit_msc_key
            })
    cn.commit()
    cn.close()
    tkr.messagebox.showinfo('Successfully Modified!', 'Playlist is Ready!')
    prof_scrn.destroy()
    mainscrn.destroy()
    mainWindow()
    auto_load_playlist()
    

def auth():
    cn = sqlite3.connect('dgr.db')
    c = cn.cursor()
    find_user = ('SELECT * FROM user WHERE username = ? AND password = ?')
    c.execute(find_user,[ent_uname.get(), ent_pass.get()])
    result = c.fetchall()
    if result:
        fetch_data()
        win.withdraw()
        mainWindow()
        auto_load_playlist()
    else:
        tkr.messagebox.showinfo('Error!', 'invalid credentials')
        ent_uname.delete(0, 'end')
        ent_pass.delete(0, 'end')
    cn.commit()
    cn.close()


def fetch_data():
    cn = sqlite3.connect('dgr.db')
    c = cn.cursor()
    c.execute('SELECT * from playlist')
    frm_playlist = c.fetchall()
    for song in frm_playlist: # importing of data from db to song_dict
        song_key = song[0]
        song_path = song[1]
        song_fname = song[2]
        song_dict.update({song_key:{'file':song_path, 'fname':song_fname}})


def auto_load_playlist():
    cn = sqlite3.connect('dgr.db')
    c = cn.cursor()
    fetch_data()
    """for auto loading of songnames on buttons"""
    empt_list_key=[]
    btn_list_main = [ptrm1, ptrm2, ptrm3, ptrm4, bt1, bt2, bt3, bt4, adh1, adh2, adh3, adh4, adl1, adl2, adl3, adl4,
        ads1, ads2, ads3, ads4, ada1, ada2, ada3, ada4, sfx1, sfx2, sfx3, sfx4, sfx5, sfx6, sfx7, sfx8, sfx9, sfx10, 
        sfx11, sfx12, sfx13, sfx14, sfx15, sfx16, sfx17, sfx18, sfx19, sfx20, sfx21, sfx22, sfx23, sfx24, sfx25, sfx26]     

    for emp_key in song_dict:                                   # for appending keys from dict to list for sequence mapping
        empt_list_key.append(emp_key)

    counter = 0                                                 # will be use for indexing empt_list_key 
    for btn in btn_list_main:
        for mkey in song_dict:
            try:
                if mkey == empt_list_key[counter]:              # for button key assignment
                    btn['text'] = song_dict[mkey]['fname']
                    counter += 1
                    break
            except IndexError:                                  # this is for the buttons without assigned keys
                btn['state'] = 'disabled'
                break
    cn.commit()
    cn.close()


""" =======================================  WINDOW AND TOPLEVEL SECTIONS  =============================================== """


def login_win():
    global win, ent_uname, ent_pass

    win = tkr.Tk()
    win_width = 400
    win_height = 200
    scrn_width = win.winfo_screenwidth()
    scrn_height = win.winfo_screenheight()
    x_cordinate = int((scrn_width/2) - (win_width/2))
    y_cordinate = int((scrn_height/2) - (win_height/2))
    win.geometry('{}x{}+{}+{}'.format(win_width, win_height, x_cordinate, y_cordinate))
    win.title('Log-in')
    
    #LOG-IN BUTTONS
    lframe_log=tkr.LabelFrame(win)
    lbl_uname=tkr.Label(lframe_log, text="Username:")
    ent_uname=tkr.Entry(lframe_log, width="28")
    lbl_pass=tkr.Label(lframe_log, text="Password:")
    ent_pass=tkr.Entry(lframe_log, width="28", show="*")
    btn_log=tkr.Button(lframe_log, text="Log-in", command=auth, width='15')

    #OUTPUT LOG-IN BUTTONS
    lframe_log.grid(padx=25, pady=25)
    lbl_uname.grid(row=0, column=0, padx=10, pady=10)
    ent_uname.grid(row=0, column=1, padx=10)
    lbl_pass.grid(row=1, column=0)
    ent_pass.grid(row=1, column=1)
    btn_log.grid(column=1,pady=10)

    win.mainloop()
    

def mainWindow():
    global img1, img2, img3, img4, img5, img6, ptrm1, ptrm2, ptrm3, ptrm4, bt1, bt2, bt3, bt4, adh1, adh2, adh3, adh4, adl1, adl2, adl3, adl4
    global ads1, ads2, ads3, ads4, ada1, ada2, ada3, ada4, sfx1, sfx2, sfx3, sfx4, sfx5, sfx6, sfx7, sfx8, sfx9, sfx10, sfx11, sfx12, sfx13
    global sfx14, sfx15, sfx16, sfx17, sfx18, sfx19, sfx20, sfx21, sfx22, sfx23, sfx24, sfx25, sfx26
    global mainscrn
    mainscrn = tkr.Toplevel(win)
    win_width = 1170
    win_height = 360
    scrn_width = mainscrn.winfo_screenwidth()
    scrn_height = mainscrn.winfo_screenheight()
    x_cordinate = int((scrn_width/2) - (win_width/2))
    y_cordinate = int((scrn_height/2) - (win_height/2))
    mainscrn.geometry('{}x{}+{}+{}'.format(win_width, win_height, x_cordinate, y_cordinate))
    mainscrn.title('DGR Music Player')    


    separator_frame = tkr.LabelFrame(mainscrn)
    separator_frame.grid(row=0, column=0, padx=5)

    #main frame for ptrm and bt
    main_frame = tkr.LabelFrame(mainscrn, text="Events")
    main_frame.grid(row=0, column=1, rowspan=40, sticky="nw", padx=3, pady=3)

    #Planetarium frame
    ptrm_frame = tkr.LabelFrame(main_frame, text="Planetarium", padx=3, pady=3)
    ptrm_frame.grid(row=0, column=0)

    ptrm1 = tkr.Button(ptrm_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('ptrm1'))
    ptrm2 = tkr.Button(ptrm_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('ptrm2'))
    ptrm3 = tkr.Button(ptrm_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('ptrm3'))
    ptrm4 = tkr.Button(ptrm_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('ptrm4'))
    ptrm1.grid(row=0, column=0)
    ptrm2.grid(row=0, column=1)
    ptrm3.grid(row=1, column=0)
    ptrm4.grid(row=1, column=1)

    #Balik-Tanaw frame
    bt_frame = tkr.LabelFrame(main_frame, text="Balik-tanaw", padx=3, pady=3)
    bt_frame.grid(row=0, column=1, padx=5, pady=5)

    bt1 = tkr.Button(bt_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('bt1'))
    bt2 = tkr.Button(bt_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('bt2'))
    bt3 = tkr.Button(bt_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('bt3'))
    bt4 = tkr.Button(bt_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('bt4'))
    bt1.grid(row=0, column=0)
    bt2.grid(row=0, column=1)
    bt3.grid(row=1, column=0)
    bt4.grid(row=1, column=1)

    separator_frame2 = tkr.LabelFrame(mainscrn)
    separator_frame2.grid(row=0, column=2, padx=5)

    #Adlib Musics frame
    adl_frame1 = tkr.LabelFrame(mainscrn, text="Adlib Musics")
    adl_frame1.grid(row=0, column=3, rowspan=40, sticky='nw', padx=3, pady=3)

    #forLove
    love_frame = tkr.LabelFrame(adl_frame1, text="Love", padx=3, pady=3)
    love_frame.grid(row=0, column=0, padx=5, pady=5)

    #buttons for love_frame
    adl1 = tkr.Button(love_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('adl1'))
    adl2 = tkr.Button(love_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('adl2'))
    adl3 = tkr.Button(love_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('adl3'))
    adl4 = tkr.Button(love_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('adl4'))
    adl1.grid(row=0, column=0)
    adl2.grid(row=0, column=1)
    adl3.grid(row=1, column=0)
    adl4.grid(row=1, column=1)

    #forHappy
    happy_frame = tkr.LabelFrame(adl_frame1, text="Happy", padx=3, pady=3)
    happy_frame.grid(row=0, column=1, padx=5, pady=5)

    #buttons for happy_frame
    adh1 = tkr.Button(happy_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('adh1'))
    adh2 = tkr.Button(happy_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('adh2'))
    adh3 = tkr.Button(happy_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('adh3'))
    adh4 = tkr.Button(happy_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('adh4'))
    adh1.grid(row=0, column=0)
    adh2.grid(row=0, column=1)
    adh3.grid(row=1, column=0)
    adh4.grid(row=1, column=1)

    #forSad
    sad_frame = tkr.LabelFrame(adl_frame1, text="Sad", padx=3, pady=3)
    sad_frame.grid(row=0, column=2, padx=5, pady=5)

    #buttons for sad_frame
    ads1 = tkr.Button(sad_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('ads1'))
    ads2 = tkr.Button(sad_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('ads2'))
    ads3 = tkr.Button(sad_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('ads3'))
    ads4 = tkr.Button(sad_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('ads4'))
    ads1.grid(row=0, column=0)
    ads2.grid(row=0, column=1)
    ads3.grid(row=1, column=0)
    ads4.grid(row=1, column=1)

    #forAngry
    angry_frame = tkr.LabelFrame(adl_frame1, text="Angry", padx=3, pady=3)
    angry_frame.grid(row=0, column=3, padx=5, pady=5)

    #buttons for angry_frame
    ada1 = tkr.Button(angry_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('ada1'))
    ada2 = tkr.Button(angry_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('ada2'))
    ada3 = tkr.Button(angry_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('ada3'))
    ada4 = tkr.Button(angry_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('ada4'))
    ada1.grid(row=0, column=0)
    ada2.grid(row=0, column=1)
    ada3.grid(row=1, column=0)
    ada4.grid(row=1, column=1)

    #soundeffects
    sfx_frame = tkr.LabelFrame(mainscrn, text="Sound Effects", padx=3, pady=3)
    sfx_frame.grid(row=40, column=1, columnspan=3, rowspan=2, padx=5, pady=5)

    #buttons for soundeffects
    sfx1 = tkr.Button(sfx_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('sfx1'))
    sfx2 = tkr.Button(sfx_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('sfx2'))
    sfx3 = tkr.Button(sfx_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('sfx3'))
    sfx4 = tkr.Button(sfx_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('sfx4'))
    sfx5 = tkr.Button(sfx_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('sfx5'))
    sfx6 = tkr.Button(sfx_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('sfx6'))
    sfx7 = tkr.Button(sfx_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('sfx7'))
    sfx8 = tkr.Button(sfx_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('sfx8'))
    sfx9 = tkr.Button(sfx_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('sfx9'))
    sfx10 = tkr.Button(sfx_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('sfx10'))
    sfx11 = tkr.Button(sfx_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('sfx11'))
    sfx12 = tkr.Button(sfx_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('sfx12'))
    sfx13 = tkr.Button(sfx_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('sfx13'))
    sfx14 = tkr.Button(sfx_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('sfx14'))
    sfx15 = tkr.Button(sfx_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('sfx15'))
    sfx16 = tkr.Button(sfx_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('sfx16'))
    sfx17 = tkr.Button(sfx_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('sfx17'))
    sfx18 = tkr.Button(sfx_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('sfx18'))
    sfx19 = tkr.Button(sfx_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('sfx19'))
    sfx20 = tkr.Button(sfx_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('sfx20'))
    sfx21 = tkr.Button(sfx_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('sfx21'))
    sfx22 = tkr.Button(sfx_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('sfx22'))
    sfx23 = tkr.Button(sfx_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('sfx23'))
    sfx24 = tkr.Button(sfx_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('sfx24'))
    sfx25 = tkr.Button(sfx_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('sfx25'))
    sfx26 = tkr.Button(sfx_frame, width=5, height=3, wraplength=80, text='no music', command=lambda: play_msc('sfx26'))
    sfx1.grid(row=0, column=0)
    sfx2.grid(row=0, column=1)
    sfx3.grid(row=0, column=2)
    sfx4.grid(row=0, column=3)
    sfx5.grid(row=0, column=4)
    sfx6.grid(row=0, column=5)
    sfx7.grid(row=0, column=6)
    sfx8.grid(row=0, column=7)
    sfx9.grid(row=0, column=8)
    sfx10.grid(row=0, column=9)
    sfx11.grid(row=0, column=10)
    sfx12.grid(row=0, column=11)
    sfx13.grid(row=0, column=12)
    sfx14.grid(row=1, column=0)
    sfx15.grid(row=1, column=1)
    sfx16.grid(row=1, column=2)
    sfx17.grid(row=1, column=3)
    sfx18.grid(row=1, column=4)
    sfx19.grid(row=1, column=5)
    sfx20.grid(row=1, column=6)
    sfx21.grid(row=1, column=7)
    sfx22.grid(row=1, column=8)
    sfx23.grid(row=1, column=9)
    sfx24.grid(row=1, column=10)
    sfx25.grid(row=1, column=11)
    sfx26.grid(row=1, column=12)

    #separator for border
    separator_frame2 = tkr.LabelFrame(mainscrn)
    separator_frame2.grid(row=0, column=4, padx=8)

    #============== DESIGNS FOR "USER SECTION" =========================================================#
    #Fonts
    font1 = ('Serif', 12)
    font2 = ('Serif', 17, 'bold')

    #Images for buttons
    img_width = 10
    img_height = 10
    #img create_prof
    cp_img = Image.open('/home/vincentvcura/Documents/Prohibited/Tengs Creations/Projects/Python Projects/ChromaKey MixPad/img/create_doc.png')
    cp_img.resize((img_width, img_height), Image.ANTIALIAS)
    img1 = ImageTk.PhotoImage(cp_img)
    #img edit_prof
    ep_img = Image.open('/home/vincentvcura/Documents/Prohibited/Tengs Creations/Projects/Python Projects/ChromaKey MixPad/img/edit_doc.png')
    ep_img.resize((img_width, img_height), Image.ANTIALIAS)
    img2 = ImageTk.PhotoImage(ep_img)
    #img logout
    lo_img = Image.open('/home/vincentvcura/Documents/Prohibited/Tengs Creations/Projects/Python Projects/ChromaKey MixPad/img/logout.png')
    lo_img.resize((img_width, img_height), Image.ANTIALIAS)
    img3 = ImageTk.PhotoImage(lo_img)
    #img pause
    pause_img = Image.open('/home/vincentvcura/Documents/Prohibited/Tengs Creations/Projects/Python Projects/ChromaKey MixPad/img/pause.png')
    pause_img.resize((img_width, img_height), Image.ANTIALIAS)
    img4 = ImageTk.PhotoImage(pause_img)
    #img stop
    stop_img = Image.open('/home/vincentvcura/Documents/Prohibited/Tengs Creations/Projects/Python Projects/ChromaKey MixPad/img/stop.png')
    stop_img.resize((img_width, img_height), Image.ANTIALIAS)
    img5 = ImageTk.PhotoImage(stop_img)
    #img resume
    resume_img = Image.open('/home/vincentvcura/Documents/Prohibited/Tengs Creations/Projects/Python Projects/ChromaKey MixPad/img/resume.png')
    resume_img.resize((img_width, img_height), Image.ANTIALIAS)
    img6 = ImageTk.PhotoImage(resume_img)

    #USER SECTION
    #Label Greetings
    lbl_greet = tkr.Label(mainscrn, text='Hello,', font=font1)
    lbl_greet.grid(row=0, column=5, sticky='nw')

    user = ent_uname.get()
    lbl_user = tkr.Label(mainscrn, text=user, font=font2)
    lbl_user.grid(row=1, column=5, columnspan=3, sticky='n')

    #Buttons for Create, Edit and Logout
    btn_create = tkr.Button(mainscrn, image=img1, command=lambda:create_playlist_win('create'))
    btn_create.grid(row=2, column=5, padx=5)
    btn_edit = tkr.Button(mainscrn, image=img2, command=lambda:create_playlist_win('edit'))
    btn_edit.grid(row=2, column=6)
    btn_logout = tkr.Button(mainscrn, image=img3, command=logout)
    btn_logout.grid(row=2, column=7, padx=5)

    #Buttons for Pause, Stop and Resume
    btn_pause = tkr.Button(mainscrn, image=img4, padx=10, pady=20, command=pause_msc)
    btn_pause.grid(row=39, column=5, columnspan=3, ipadx=7, sticky='n')
    btn_stop = tkr.Button(mainscrn, image=img6, padx=10, pady=20, command=resume_msc)
    btn_stop.grid(row=40, column=5, columnspan=3, ipadx=7, pady=9, sticky='n')
    btn_resume = tkr.Button(mainscrn, image=img5, padx=10, pady=20, command=stop_msc)
    btn_resume.grid(row=41, column=5, columnspan=3, ipadx=7, pady=9, sticky='n')

#============================== Window for creating Playlist ========================================#
def create_playlist_win(mode_to_use):
    global prof_scrn, mode_now
    prof_scrn = tkr.Toplevel(win)
    win_width = 940
    win_height = 680
    scrn_width = prof_scrn.winfo_screenwidth()
    scrn_height = prof_scrn.winfo_screenheight()
    x_cordinate = int((scrn_width/2) - (win_width/2))
    y_cordinate = int((scrn_height/2) - (win_height/2))
    prof_scrn.geometry('{}x{}+{}+{}'.format(win_width, win_height, x_cordinate, y_cordinate))
    #for create/modify titlebar and save button
    if mode_to_use == 'create':
        prof_scrn.title('Creating your Playlist')
        mode_now = mode_to_use
    else:
        prof_scrn.title('Modifying your Playlist')
        mode_now = mode_to_use


    #prof_scrn margins
    left_margin = tkr.LabelFrame(prof_scrn)
    left_margin.grid(row=0, column=0, padx=5, pady=5)

    #LabelFrames
        #events frame files
    frame_events = tkr.LabelFrame(prof_scrn, text="Events", padx=3, pady=3)
    frame_events.grid(row=1, column=1, padx=5, pady=5, sticky='nw')
        #adlib frame files
    frame_adlib = tkr.LabelFrame(prof_scrn, text="Adlib", padx=3, pady=3)
    frame_adlib.grid(row=2, column=1, padx=5, pady=5, sticky='nw')
        #adlib2 continuation
    frame_adlib2 = tkr.LabelFrame(prof_scrn, text="Adlib", padx=3, pady=3)
    frame_adlib2.grid(row=1, column=2, padx=5, pady=5, sticky='nw')
        #SFX frame files
    frame_sfx = tkr.LabelFrame(prof_scrn, text="SFX", padx=3, pady=3)
    frame_sfx.grid(row=2, column=2, padx=5, pady=5, sticky='nw')
        #SFX continuation
    frame_sfx2 = tkr.LabelFrame(prof_scrn, text="SFX", padx=3, pady=3)
    frame_sfx2.grid(row=1, column=3, padx=5, pady=5, sticky='nw', rowspan=2, columnspan=2)

    #labels
        #Events Planetarium
    lbl_ptrm_name = tkr.Label(frame_events, text='Planetarium')
    lbl_ptrm1 = tkr.Label(frame_events, width=30, bg='white')
    lbl_ptrm2 = tkr.Label(frame_events, width=30, bg='white')
    lbl_ptrm3 = tkr.Label(frame_events, width=30, bg='white')
    lbl_ptrm4 = tkr.Label(frame_events, width=30, bg='white')
        #Events Balik-tanaw
    lbl_bt_name = tkr.Label(frame_events, text='Balik-tanaw')
    lbl_bt1 = tkr.Label(frame_events, width=30, bg='white')
    lbl_bt2 = tkr.Label(frame_events, width=30, bg='white')
    lbl_bt3 = tkr.Label(frame_events, width=30, bg='white')
    lbl_bt4 = tkr.Label(frame_events, width=30, bg='white')
        #Adlib Love
    lbl_adl_name = tkr.Label(frame_adlib, text='Love')
    lbl_adl1 = tkr.Label(frame_adlib, width=30, bg='white')
    lbl_adl2 = tkr.Label(frame_adlib, width=30, bg='white')
    lbl_adl3 = tkr.Label(frame_adlib, width=30, bg='white')
    lbl_adl4 = tkr.Label(frame_adlib, width=30, bg='white')
        #Adlib Happy
    lbl_adh_name = tkr.Label(frame_adlib, text='Happy')
    lbl_adh1 = tkr.Label(frame_adlib, width=30, bg='white')
    lbl_adh2 = tkr.Label(frame_adlib, width=30, bg='white')
    lbl_adh3 = tkr.Label(frame_adlib, width=30, bg='white')
    lbl_adh4 = tkr.Label(frame_adlib, width=30, bg='white')
        #Adlib Sad
    lbl_ads_name = tkr.Label(frame_adlib2, text='Sad')
    lbl_ads1 = tkr.Label(frame_adlib2, width=30, bg='white')
    lbl_ads2 = tkr.Label(frame_adlib2, width=30, bg='white')
    lbl_ads3 = tkr.Label(frame_adlib2, width=30, bg='white')
    lbl_ads4 = tkr.Label(frame_adlib2, width=30, bg='white')
        #Adlib Angry
    lbl_ada_name = tkr.Label(frame_adlib2, text='Angry')
    lbl_ada1 = tkr.Label(frame_adlib2, width=30, bg='white')
    lbl_ada2 = tkr.Label(frame_adlib2, width=30, bg='white')
    lbl_ada3 = tkr.Label(frame_adlib2, width=30, bg='white')
    lbl_ada4 = tkr.Label(frame_adlib2, width=30, bg='white')
        #SFX
    lbl_sfx_name = tkr.Label(frame_sfx, text='Sound Effects')
    lbl_sfx1 = tkr.Label(frame_sfx, width=30, bg='white')
    lbl_sfx2 = tkr.Label(frame_sfx, width=30, bg='white')
    lbl_sfx3 = tkr.Label(frame_sfx, width=30, bg='white')
    lbl_sfx4 = tkr.Label(frame_sfx, width=30, bg='white')
    lbl_sfx5 = tkr.Label(frame_sfx, width=30, bg='white')
    lbl_sfx6 = tkr.Label(frame_sfx, width=30, bg='white')
    lbl_sfx7 = tkr.Label(frame_sfx, width=30, bg='white')
    lbl_sfx8 = tkr.Label(frame_sfx, width=30, bg='white')
    lbl_sfx9 = tkr.Label(frame_sfx, width=30, bg='white')
    lbl_sfx10 = tkr.Label(frame_sfx2, width=30, bg='white')
    lbl_sfx11 = tkr.Label(frame_sfx2, width=30, bg='white')
    lbl_sfx12 = tkr.Label(frame_sfx2, width=30, bg='white')
    lbl_sfx13 = tkr.Label(frame_sfx2, width=30, bg='white')
    lbl_sfx14 = tkr.Label(frame_sfx2, width=30, bg='white')
    lbl_sfx15 = tkr.Label(frame_sfx2, width=30, bg='white')
    lbl_sfx16 = tkr.Label(frame_sfx2, width=30, bg='white')
    lbl_sfx17 = tkr.Label(frame_sfx2, width=30, bg='white')
    lbl_sfx18 = tkr.Label(frame_sfx2, width=30, bg='white')
    lbl_sfx19 = tkr.Label(frame_sfx2, width=30, bg='white')
    lbl_sfx20 = tkr.Label(frame_sfx2, width=30, bg='white')
    lbl_sfx21 = tkr.Label(frame_sfx2, width=30, bg='white')
    lbl_sfx22 = tkr.Label(frame_sfx2, width=30, bg='white')
    lbl_sfx23 = tkr.Label(frame_sfx2, width=30, bg='white')
    lbl_sfx24 = tkr.Label(frame_sfx2, width=30, bg='white')
    lbl_sfx25 = tkr.Label(frame_sfx2, width=30, bg='white')
    lbl_sfx26 = tkr.Label(frame_sfx2, width=30, bg='white')

    #labels grid
        #Events Planetarium
    lbl_ptrm_name.grid(row=0, column=0, sticky='nw')
    lbl_ptrm1.grid(row=1, column=0, pady=3)
    lbl_ptrm2.grid(row=2, column=0, pady=3)
    lbl_ptrm3.grid(row=3, column=0, pady=3)
    lbl_ptrm4.grid(row=4, column=0, pady=3)
        #Events Balik-tanaw
    lbl_bt_name.grid(row=5, column=0, sticky='nw')
    lbl_bt1.grid(row=6, column=0, pady=3)
    lbl_bt2.grid(row=7, column=0, pady=3)
    lbl_bt3.grid(row=8, column=0, pady=3)
    lbl_bt4.grid(row=9, column=0, pady=3)
        #Adlib Love
    lbl_adl_name.grid(row=10, column=0, sticky='nw')
    lbl_adl1.grid(row=11, column=0, pady=3)
    lbl_adl2.grid(row=12, column=0, pady=3)
    lbl_adl3.grid(row=13, column=0, pady=3)
    lbl_adl4.grid(row=14, column=0, pady=3)
        #Adlib Happy
    lbl_adh_name.grid(row=15, column=0, sticky='nw')
    lbl_adh1.grid(row=16, column=0, pady=3)
    lbl_adh2.grid(row=17, column=0, pady=3)
    lbl_adh3.grid(row=18, column=0, pady=3)
    lbl_adh4.grid(row=19, column=0, pady=3)
        #Adlib Sad
    lbl_ads_name.grid(row=0, column=0, sticky='nw')
    lbl_ads1.grid(row=1, column=0, pady=3)
    lbl_ads2.grid(row=2, column=0, pady=3)
    lbl_ads3.grid(row=3, column=0, pady=3)
    lbl_ads4.grid(row=4, column=0, pady=3)
        #Adlib Angry
    lbl_ada_name.grid(row=5, column=0, sticky='nw')
    lbl_ada1.grid(row=6, column=0, pady=3)
    lbl_ada2.grid(row=7, column=0, pady=3)
    lbl_ada3.grid(row=8, column=0, pady=3)
    lbl_ada4.grid(row=9, column=0, pady=3)
        #SFX
    lbl_sfx_name.grid(row=0, column=0, sticky='nw')
    lbl_sfx1.grid(row=1, column=0, pady=3)
    lbl_sfx2.grid(row=2, column=0, pady=3)
    lbl_sfx3.grid(row=3, column=0, pady=3)
    lbl_sfx4.grid(row=4, column=0, pady=3)
    lbl_sfx5.grid(row=5, column=0, pady=3)
    lbl_sfx6.grid(row=6, column=0, pady=3)
    lbl_sfx7.grid(row=7, column=0, pady=3)
    lbl_sfx8.grid(row=8, column=0, pady=3)
    lbl_sfx9.grid(row=9, column=0, pady=3)
    lbl_sfx10.grid(row=0, column=0, pady=3)
    lbl_sfx11.grid(row=1, column=0, pady=3)
    lbl_sfx12.grid(row=2, column=0, pady=3)
    lbl_sfx13.grid(row=3, column=0, pady=3)
    lbl_sfx14.grid(row=4, column=0, pady=3)
    lbl_sfx15.grid(row=5, column=0, pady=3)
    lbl_sfx16.grid(row=6, column=0, pady=3)
    lbl_sfx17.grid(row=7, column=0, pady=3)
    lbl_sfx18.grid(row=8, column=0, pady=3)
    lbl_sfx19.grid(row=9, column=0, pady=3)
    lbl_sfx20.grid(row=10, column=0, pady=3)
    lbl_sfx21.grid(row=11, column=0, pady=3)
    lbl_sfx22.grid(row=12, column=0, pady=3)
    lbl_sfx23.grid(row=13, column=0, pady=3)
    lbl_sfx24.grid(row=14, column=0, pady=3)
    lbl_sfx25.grid(row=15, column=0, pady=3)
    lbl_sfx26.grid(row=16, column=0, pady=3)

    #BUTTONS
        #Planetarium
    btn_brws_ptrm1 = tkr.Button(frame_events, text='...', command=lambda: browsefile('ptrm1', lbl_ptrm1))
    btn_brws_ptrm2 = tkr.Button(frame_events, text='...', command=lambda: browsefile('ptrm2', lbl_ptrm2))
    btn_brws_ptrm3 = tkr.Button(frame_events, text='...', command=lambda: browsefile('ptrm3', lbl_ptrm3))
    btn_brws_ptrm4 = tkr.Button(frame_events, text='...', command=lambda: browsefile('ptrm4', lbl_ptrm4))
        #Balik-tanaw
    btn_brws_bt1 = tkr.Button(frame_events, text='...', command=lambda: browsefile('bt1', lbl_bt1))
    btn_brws_bt2 = tkr.Button(frame_events, text='...', command=lambda: browsefile('bt2', lbl_bt2))
    btn_brws_bt3 = tkr.Button(frame_events, text='...', command=lambda: browsefile('bt3', lbl_bt3))
    btn_brws_bt4 = tkr.Button(frame_events, text='...', command=lambda: browsefile('bt4', lbl_bt4))
        #Adlib Love
    btn_adl1 = tkr.Button(frame_adlib, text='...', command=lambda: browsefile('adl1', lbl_adl1))
    btn_adl2 = tkr.Button(frame_adlib, text='...', command=lambda: browsefile('adl2', lbl_adl2))
    btn_adl3 = tkr.Button(frame_adlib, text='...', command=lambda: browsefile('adl3', lbl_adl3))
    btn_adl4 = tkr.Button(frame_adlib, text='...', command=lambda: browsefile('adl4', lbl_adl4))
        #Adlib Happy
    btn_adh1 = tkr.Button(frame_adlib, text='...', command=lambda: browsefile('adh1', lbl_adh1))
    btn_adh2 = tkr.Button(frame_adlib, text='...', command=lambda: browsefile('adh2', lbl_adh2))
    btn_adh3 = tkr.Button(frame_adlib, text='...', command=lambda: browsefile('adh3', lbl_adh3))
    btn_adh4 = tkr.Button(frame_adlib, text='...', command=lambda: browsefile('adh4', lbl_adh4))
        #Adlib Sad
    btn_ads1 = tkr.Button(frame_adlib2, text='...', command=lambda: browsefile('ads1', lbl_ads1))
    btn_ads2 = tkr.Button(frame_adlib2, text='...', command=lambda: browsefile('ads2', lbl_ads2))
    btn_ads3 = tkr.Button(frame_adlib2, text='...', command=lambda: browsefile('ads3', lbl_ads3))
    btn_ads4 = tkr.Button(frame_adlib2, text='...', command=lambda: browsefile('ads4', lbl_ads4))
        #Adlib Angry
    btn_ada1 = tkr.Button(frame_adlib2, text='...', command=lambda: browsefile('ada1', lbl_ada1))
    btn_ada2 = tkr.Button(frame_adlib2, text='...', command=lambda: browsefile('ada2', lbl_ada2))
    btn_ada3 = tkr.Button(frame_adlib2, text='...', command=lambda: browsefile('ada3', lbl_ada3))
    btn_ada4 = tkr.Button(frame_adlib2, text='...', command=lambda: browsefile('ada4', lbl_ada4))
        #SFX
    btn_sfx1 = tkr.Button(frame_sfx, text='...', command=lambda: browsefile('sfx1', lbl_sfx1))
    btn_sfx2 = tkr.Button(frame_sfx, text='...', command=lambda: browsefile('sfx2', lbl_sfx2))
    btn_sfx3 = tkr.Button(frame_sfx, text='...', command=lambda: browsefile('sfx3', lbl_sfx3))
    btn_sfx4 = tkr.Button(frame_sfx, text='...', command=lambda: browsefile('sfx4', lbl_sfx4))
    btn_sfx5 = tkr.Button(frame_sfx, text='...', command=lambda: browsefile('sfx5', lbl_sfx5))
    btn_sfx6 = tkr.Button(frame_sfx, text='...', command=lambda: browsefile('sfx6', lbl_sfx6))
    btn_sfx7 = tkr.Button(frame_sfx, text='...', command=lambda: browsefile('sfx7', lbl_sfx7))
    btn_sfx8 = tkr.Button(frame_sfx, text='...', command=lambda: browsefile('sfx8', lbl_sfx8))
    btn_sfx9 = tkr.Button(frame_sfx, text='...', command=lambda: browsefile('sfx9', lbl_sfx9))
    btn_sfx10 = tkr.Button(frame_sfx2, text='...', command=lambda: browsefile('sfx10', lbl_sfx10))
    btn_sfx11 = tkr.Button(frame_sfx2, text='...', command=lambda: browsefile('sfx11', lbl_sfx11))
    btn_sfx12 = tkr.Button(frame_sfx2, text='...', command=lambda: browsefile('sfx12', lbl_sfx12))
    btn_sfx13 = tkr.Button(frame_sfx2, text='...', command=lambda: browsefile('sfx13', lbl_sfx13))
    btn_sfx14 = tkr.Button(frame_sfx2, text='...', command=lambda: browsefile('sfx14', lbl_sfx14))
    btn_sfx15 = tkr.Button(frame_sfx2, text='...', command=lambda: browsefile('sfx15', lbl_sfx15))
    btn_sfx16 = tkr.Button(frame_sfx2, text='...', command=lambda: browsefile('sfx16', lbl_sfx16))
    btn_sfx17 = tkr.Button(frame_sfx2, text='...', command=lambda: browsefile('sfx17', lbl_sfx17))
    btn_sfx18 = tkr.Button(frame_sfx2, text='...', command=lambda: browsefile('sfx18', lbl_sfx18))
    btn_sfx19 = tkr.Button(frame_sfx2, text='...', command=lambda: browsefile('sfx19', lbl_sfx19))
    btn_sfx20 = tkr.Button(frame_sfx2, text='...', command=lambda: browsefile('sfx20', lbl_sfx20))
    btn_sfx21 = tkr.Button(frame_sfx2, text='...', command=lambda: browsefile('sfx21', lbl_sfx21))
    btn_sfx22 = tkr.Button(frame_sfx2, text='...', command=lambda: browsefile('sfx22', lbl_sfx22))
    btn_sfx23 = tkr.Button(frame_sfx2, text='...', command=lambda: browsefile('sfx23', lbl_sfx23))
    btn_sfx24 = tkr.Button(frame_sfx2, text='...', command=lambda: browsefile('sfx24', lbl_sfx24))
    btn_sfx25 = tkr.Button(frame_sfx2, text='...', command=lambda: browsefile('sfx25', lbl_sfx25))
    btn_sfx26 = tkr.Button(frame_sfx2, text='...', command=lambda: browsefile('sfx26', lbl_sfx26))

    #buttons grid
        # Planetarium
    btn_brws_ptrm1.grid(row=1, column=1)
    btn_brws_ptrm2.grid(row=2, column=1)
    btn_brws_ptrm3.grid(row=3, column=1)
    btn_brws_ptrm4.grid(row=4, column=1)
        #balik-tanaw
    btn_brws_bt1.grid(row=6, column=1)
    btn_brws_bt2.grid(row=7, column=1)
    btn_brws_bt3.grid(row=8, column=1)
    btn_brws_bt4.grid(row=9, column=1)
        #Adlib Love
    btn_adl1.grid(row=11, column=1)
    btn_adl2.grid(row=12, column=1)
    btn_adl3.grid(row=13, column=1)
    btn_adl4.grid(row=14, column=1)
        #Adlib Happy
    btn_adh1.grid(row=16, column=1)
    btn_adh2.grid(row=17, column=1)
    btn_adh3.grid(row=18, column=1)
    btn_adh4.grid(row=19, column=1)
        #Adlib Sad
    btn_ads1.grid(row=1, column=1)
    btn_ads2.grid(row=2, column=1)
    btn_ads3.grid(row=3, column=1)
    btn_ads4.grid(row=4, column=1)
        #Adlib Angry
    btn_ada1.grid(row=6, column=1)
    btn_ada2.grid(row=7, column=1)
    btn_ada3.grid(row=8, column=1)
    btn_ada4.grid(row=9, column=1)
        #SFX
    btn_sfx1.grid(row=1, column=1)
    btn_sfx2.grid(row=2, column=1)
    btn_sfx3.grid(row=3, column=1)
    btn_sfx4.grid(row=4, column=1)
    btn_sfx5.grid(row=5, column=1)
    btn_sfx6.grid(row=6, column=1)
    btn_sfx7.grid(row=7, column=1)
    btn_sfx8.grid(row=8, column=1)
    btn_sfx9.grid(row=9, column=1)
    btn_sfx10.grid(row=0, column=1)
    btn_sfx11.grid(row=1, column=1)
    btn_sfx12.grid(row=2, column=1)
    btn_sfx13.grid(row=3, column=1)
    btn_sfx14.grid(row=4, column=1)
    btn_sfx15.grid(row=5, column=1)
    btn_sfx16.grid(row=6, column=1)
    btn_sfx17.grid(row=7, column=1)
    btn_sfx18.grid(row=8, column=1)
    btn_sfx19.grid(row=9, column=1)
    btn_sfx20.grid(row=10, column=1)
    btn_sfx21.grid(row=11, column=1)
    btn_sfx22.grid(row=12, column=1)
    btn_sfx23.grid(row=13, column=1)
    btn_sfx24.grid(row=14, column=1)
    btn_sfx25.grid(row=15, column=1)
    btn_sfx26.grid(row=16, column=1)

    #Buttons for Save and Cancel
    btn_save = tkr.Button(prof_scrn, text='Save', width=10)
    btn_save.grid(row=2, column=3, sticky='w', pady=260, padx=20)

    btn_cancel = tkr.Button(prof_scrn, text='Cancel', width=10, command=cancel_btn)
    btn_cancel.grid(row=2, column=4, sticky='w')

    try:
        if mode_to_use == 'create':
            btn_save['command'] = save_new_playlist
        else:
            btn_save['command'] = mod_playlist
            lbl_ptrm1['text'] = song_dict['ptrm1']['fname']
            lbl_ptrm2['text'] = song_dict['ptrm2']['fname']
            lbl_ptrm3['text'] = song_dict['ptrm3']['fname']
            lbl_ptrm4['text'] = song_dict['ptrm4']['fname']
            lbl_bt1['text'] = song_dict['bt1']['fname']
            lbl_bt2['text'] = song_dict['bt2']['fname']
            lbl_bt3['text'] = song_dict['bt3']['fname']
            lbl_bt4['text'] = song_dict['bt4']['fname']
            lbl_adl1['text'] = song_dict['adl1']['fname']
            lbl_adl2['text'] = song_dict['adl2']['fname']
            lbl_adl3['text'] = song_dict['adl3']['fname']
            lbl_adl4['text'] = song_dict['adl4']['fname']
            lbl_adh1['text'] = song_dict['adh1']['fname']
            lbl_adh2['text'] = song_dict['adh2']['fname']
            lbl_adh3['text'] = song_dict['adh3']['fname']
            lbl_adh4['text'] = song_dict['adh4']['fname']
            lbl_ads1['text'] = song_dict['ads1']['fname']
            lbl_ads2['text'] = song_dict['ads2']['fname']
            lbl_ads3['text'] = song_dict['ads3']['fname']
            lbl_ads4['text'] = song_dict['ads4']['fname']
            lbl_ada1['text'] = song_dict['ada1']['fname']
            lbl_ada2['text'] = song_dict['ada2']['fname']
            lbl_ada3['text'] = song_dict['ada3']['fname']
            lbl_ada4['text'] = song_dict['ada4']['fname']
            lbl_sfx1['text'] = song_dict['sfx1']['fname']
            lbl_sfx2['text'] = song_dict['sfx2']['fname']
            lbl_sfx3['text'] = song_dict['sfx3']['fname']
            lbl_sfx4['text'] = song_dict['sfx4']['fname']
            lbl_sfx5['text'] = song_dict['sfx5']['fname']
            lbl_sfx6['text'] = song_dict['sfx6']['fname']
            lbl_sfx7['text'] = song_dict['sfx7']['fname']
            lbl_sfx8['text'] = song_dict['sfx8']['fname']
            lbl_sfx9['text'] = song_dict['sfx9']['fname']
            lbl_sfx10['text'] = song_dict['sfx10']['fname']
            lbl_sfx11['text'] = song_dict['sfx11']['fname']
            lbl_sfx12['text'] = song_dict['sfx12']['fname']
            lbl_sfx13['text'] = song_dict['sfx13']['fname']
            lbl_sfx14['text'] = song_dict['sfx14']['fname']
            lbl_sfx15['text'] = song_dict['sfx15']['fname']
            lbl_sfx16['text'] = song_dict['sfx16']['fname']
            lbl_sfx17['text'] = song_dict['sfx17']['fname']
            lbl_sfx18['text'] = song_dict['sfx18']['fname']
            lbl_sfx19['text'] = song_dict['sfx19']['fname']
            lbl_sfx20['text'] = song_dict['sfx20']['fname']
            lbl_sfx21['text'] = song_dict['sfx21']['fname']
            lbl_sfx22['text'] = song_dict['sfx22']['fname']
            lbl_sfx23['text'] = song_dict['sfx23']['fname']
            lbl_sfx24['text'] = song_dict['sfx24']['fname']
            lbl_sfx25['text'] = song_dict['sfx25']['fname']
            lbl_sfx26['text'] = song_dict['sfx26']['fname']
    except KeyError:
        pass

mixer.init()
song_dict={}
mod_pl_dict={}
login_win()