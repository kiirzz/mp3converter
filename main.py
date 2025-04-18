import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import re
import sys

current_process = None

def get_ffmpeg_path():
    if getattr(sys, 'frozen', False):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
        return os.path.join(base_path, 'Resources', 'ffmpeg', 'ffmpeg') 
    else:
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ffmpeg', 'ffmpeg') 

def convert_multiple_files():
    input_paths = filedialog.askopenfilenames(
        title="Chọn các file WAV hoặc MP4",
        filetypes=[("Audio/Video files", "*.wav *.mp4"), ("All files", "*.*")]
    )
    if not input_paths:
        return

    log_text.delete("1.0", tk.END)

    success_count = 0
    fail_count = 0

    ffmpeg_executable = get_ffmpeg_path()

    for input_path in input_paths:
        base, _ = os.path.splitext(input_path)
        output_path = base + ".mp3"

        ffmpeg_args = [ffmpeg_executable, "-i", input_path, "-vn", "-codec:a", "libmp3lame", "-b:a", "192k", output_path]

        if os.path.exists(output_path):
            overwrite = messagebox.askyesno(
                "Ghi đè file?",
                f"File '{os.path.basename(output_path)}' đã tồn tại.\nBạn có muốn ghi đè không?"
            )
            if not overwrite:
                log_text.insert(tk.END, f"⚠️ Bỏ qua (đã tồn tại): {os.path.basename(input_path)}\n")
                continue
            else:
                ffmpeg_args.insert(1, "-y")

        log_text.insert(tk.END, f"🔄 Bắt đầu chuyển đổi: {os.path.basename(input_path)}\n")
        root.update()

        try:
            process = subprocess.Popen(
                ffmpeg_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                bufsize=1,
                encoding="utf-8",
                errors="replace"
            )

            progress_regex = re.compile(r"size=.*time=.*bitrate=.*speed=.*")

            for line in process.stderr:
                if progress_regex.search(line):
                    log_text.insert(tk.END, line)
                    log_text.see(tk.END)
                    root.update()

            process.wait()
            if process.returncode == 0:
                success_count += 1
                log_text.insert(tk.END, f"✅ Hoàn tất: {os.path.basename(input_path)}\n\n")
            else:
                fail_count += 1
                log_text.insert(tk.END, f"❌ Lỗi: {os.path.basename(input_path)}\n\n")

        except Exception as e:
            fail_count += 1
            log_text.insert(tk.END, f"❌ Lỗi hệ thống khi xử lý {os.path.basename(input_path)}: {str(e)}\n\n")

        root.update()

    log_text.insert(tk.END, f"\n🎉 Tổng kết:\n✔️ Thành công: {success_count}\n❌ Thất bại: {fail_count}\n")
    root.update()

# Giao diện
root = tk.Tk()
root.title("MP3 Converter")

root.minsize(500, 500)

btn = tk.Button(root, text="Chọn file", command=convert_multiple_files, padx=20, pady=10)
btn.pack(pady=20)

log_text = tk.Text(root, height=20, width=60, wrap="word")
log_text.pack(pady=10)

def on_close():
    global current_process
    if current_process and current_process.poll() is None:
        if messagebox.askyesno("Đang xử lý", "Đang chuyển đổi file. Bạn có chắc muốn thoát?"):
            try:
                current_process.terminate()
            except Exception:
                pass
            root.destroy()
    else:
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
