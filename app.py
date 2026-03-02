# YouTube Video Downloader - With Progress

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import yt_dlp
import os

def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, folder)

def start_download():
    url = url_var.get().strip()
    
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL")
        return
    
    if not url.startswith("http"):
        messagebox.showerror("Error", "Invalid URL")
        return
    
    save_path = path_var.get()
    if not os.path.isdir(save_path):
        messagebox.showerror("Error", "Invalid save path")
        return
    
    # Disable button
    download_btn.config(state=tk.DISABLED, bg="#a5d6a7", text="Downloading...")
    progress_bar['value'] = 0
    status_var.set("Starting download...")
    
    def download():
        try:
            # FFmpeg location
            ffmpeg_path = r'C:\temp\ffmpeg-master-latest-win64-gpl\bin'
            
            ydl_opts = {
                'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
                'progress_hooks': [progress_hook],
                'quiet': False,
                'ffmpeg_location': ffmpeg_path,
                # Add proxy if needed
                'proxy': 'http://127.0.0.1:6789',
                # Retry settings
                'retries': 3,
                'fragment_retries': 3,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'video')
                status_var.set(f"Downloading: {title[:30]}...")
                ydl.download([url])
            
            status_var.set("Download complete!")
            messagebox.showinfo("Success", "Download complete!")
        except Exception as e:
            error_msg = str(e)
            status_var.set("Error: " + error_msg[:50])
            messagebox.showerror("Error", error_msg)
        
        download_btn.config(state=tk.NORMAL, bg="#4CAF50", text="DOWNLOAD")
        progress_bar['value'] = 0
    
    def progress_hook(d):
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            downloaded = d.get('downloaded_bytes', 0)
            if total > 0:
                pct = (downloaded / total) * 100
                progress_bar['value'] = pct
                root.update_idletasks()
        elif d['status'] == 'finished':
            progress_bar['value'] = 100
            status_var.set("Processing...")
    
    threading.Thread(target=download, daemon=True).start()

# Create window
root = tk.Tk()
root.title("YouTube Downloader")
root.geometry("550x350")
root.configure(bg="#f0f0f0")

# Title
tk.Label(root, text="YouTube Video Downloader", font=("Arial", 16, "bold"), 
         bg="#f0f0f0", fg="#333").pack(pady=15)

# URL
tk.Label(root, text="Video URL:", bg="#f0f0f0", font=("Arial", 10)).pack()
url_var = tk.StringVar()
url_entry = tk.Entry(root, textvariable=url_var, width=55, font=("Arial", 10))
url_entry.pack(pady=5)

# Path
tk.Label(root, text="Save to:", bg="#f0f0f0", font=("Arial", 10)).pack()
path_frame = tk.Frame(root, bg="#f0f0f0")
path_frame.pack(pady=5)

path_var = tk.StringVar(value=os.path.join(os.path.expanduser("~"), "Desktop"))
path_entry = tk.Entry(path_frame, textvariable=path_var, width=40, font=("Arial", 10))
path_entry.pack(side=tk.LEFT)

tk.Button(path_frame, text="Browse", command=browse_folder, bg="#ddd", 
          font=("Arial", 9)).pack(side=tk.LEFT, padx=5)

# Progress Bar
tk.Label(root, text="Progress:", bg="#f0f0f0", font=("Arial", 10)).pack(pady=(15,0))
progress_bar = ttk.Progressbar(root, length=400, mode='determinate')
progress_bar.pack(pady=5)

# Status
status_var = tk.StringVar(value="Ready")
tk.Label(root, textvariable=status_var, bg="#f0f0f0", fg="#666", font=("Arial", 9)).pack(pady=5)

# Download Button - BIG GREEN BUTTON
download_btn = tk.Button(root, text="DOWNLOAD", 
                        command=start_download,
                        width=20, height=2,
                        bg="#4CAF50", fg="white",
                        font=("Arial", 14, "bold"),
                        bd=0, cursor="hand2")
download_btn.pack(pady=20)

root.mainloop()
