import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
from shortest_path import find_shortest_path, plot_shortest_path

# Biến dùng cho việc lưu trữ tạm shortest_path trước đó
current_path_line = None

def create_ui(southern_provinces, graph, southern_vietnam, output):

    # Initialize Tkinter window
    root = tk.Tk()
    root.title("Bản đồ miền Nam Việt Nam - Tìm đường đi ngắn nhất")

    # Create the main frame
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Left frame for the map
    left_frame = tk.Frame(main_frame)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Right frame for user interaction
    right_frame = tk.Frame(main_frame)
    right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=15, pady=15)

    # Create a matplotlib figure
    fig = Figure(figsize=(8, 8))
    ax = fig.add_subplot(111)

    # Plot the map initially
    plot_map(ax, southern_vietnam, output)

    # Embed the matplotlib figure in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=left_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)
    
    # Variables to track panning
    pan_start = [0, 0]
    
    def on_mouse_press(event):
        """Capture the starting point for panning."""
        if event.button == 1:  # Left mouse button
            pan_start[0], pan_start[1] = event.x, event.y

    def on_mouse_drag(event):
        """Pan the map by adjusting the axis limits."""
        if event.button == 1:  # Left mouse button
            xlim = ax.get_xlim()
            ylim = ax.get_ylim()
        
            dx = (pan_start[0] - event.x) * (xlim[1] - xlim[0]) / canvas_widget.winfo_width()
            dy = (pan_start[1] - event.y) * (ylim[1] - ylim[0]) / canvas_widget.winfo_height()

            ax.set_xlim(xlim[0] + dx, xlim[1] + dx)
            ax.set_ylim(ylim[0] + dy, ylim[1] + dy)
            pan_start[0], pan_start[1] = event.x, event.y
            canvas.draw()

    def on_scroll(event):
        """Zoom in or out based on the scroll wheel."""
        base_scale = 1.2
        cur_xlim = ax.get_xlim()
        cur_ylim = ax.get_ylim()
        xdata = event.xdata
        ydata = event.ydata

        if event.button == 'up':  # lăn chuột lên zoom in
            scale_factor = 1 / base_scale
        elif event.button == 'down':  # lăn chuột xuống zoom out
            scale_factor = base_scale
        else:
            scale_factor = 1

        new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
        new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor
        relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0])
        rely = (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_ylim[0])

        ax.set_xlim([xdata - new_width * (1 - relx), xdata + new_width * relx])
        ax.set_ylim([ydata - new_height * (1 - rely), ydata + new_height * rely])
        canvas.draw()

    # Connect the events to the canvas
    canvas.mpl_connect("button_press_event", on_mouse_press)
    canvas.mpl_connect("motion_notify_event", on_mouse_drag)
    canvas.mpl_connect("scroll_event", on_scroll)

    # Add widgets to the right frame
    tk.Label(right_frame, text="Bắt đầu:").pack(pady=5)
    start_var = tk.StringVar()
    start_combobox = ttk.Combobox(right_frame, textvariable=start_var, values=southern_provinces)
    start_combobox.pack(pady=5)

    tk.Label(right_frame, text="Điểm đến:").pack(pady=5)
    end_var = tk.StringVar()
    end_combobox = ttk.Combobox(right_frame, textvariable=end_var, values=southern_provinces)
    end_combobox.pack(pady=5)

    # Tạo một frame cho nút "Tìm đường đi" và "Reset"
    frame_buttons = tk.Frame(right_frame)
    frame_buttons.pack(pady=20)

    def on_run_button_click():
        global current_path_line

        start = start_var.get()
        end = end_var.get()
        if not start or not end:
            tk.messagebox.showerror("Lỗi", "Vui lòng chọn cả điểm bắt đầu và điểm đến!")
            return
        # Kiểm tra đường cũ có tồn tại
        if current_path_line:
            for line in current_path_line:
                line.remove()
        # Tìm và Vẽ shortest path mới sau khi xóa đường đi cũ
        path = find_shortest_path(graph, start, end)
        current_path_line = plot_shortest_path(ax, graph, path)
        canvas.draw()
        
    run_button = tk.Button(frame_buttons, text="Tìm đường đi", command=on_run_button_click)
    run_button.grid(row=0, column=0, padx=5)

    def on_reset_button_click():
        """Xóa đường đi đã vẽ và reset lại bản đồ."""
        ax.cla()  # Xóa mọi thứ trong biểu đồ
        plot_map(ax, southern_vietnam, output)  # Vẽ lại bản đồ gốc
        canvas.draw()  # Cập nhật lại giao diện
    # Tạo nút Reset
    reset_icon = Image.open("images/reset_icon.png").resize((16, 16))  # Thay đổi kích thước icon
    reset_photo = ImageTk.PhotoImage(reset_icon)
    reset_button = tk.Button(frame_buttons, image=reset_photo, command=on_reset_button_click)
    reset_button.image = reset_photo  # Lưu tham chiếu ảnh để tránh bị xóa bởi garbage collector
    reset_button.grid(row=0, column=1, padx=5)

    root.mainloop()

def plot_map(ax, southern_vietnam, output):
    color_map = {
        'Light Pink': '#ffb6c1',
        'Light Green': '#90ee90',
        'Light Blue': '#add8e6',
        'Light Yellow': '#fffacd',
        'Light Orange': '#ffcc99'
    }
    southern_vietnam.boundary.plot(ax=ax, linewidth=1, color='grey')

    for province, color_key in output.items():
        province_shape = southern_vietnam[southern_vietnam['NAME_1'] == province]
        color = color_map.get(color_key, '#ffb6c1')
        province_shape.plot(ax=ax, color=color)
        coords = province_shape.geometry.centroid
        ax.text(coords.x.iloc[0], coords.y.iloc[0], province, fontsize=8, ha='center', color='black')

    ax.set_title("Map of Southern Vietnam")
