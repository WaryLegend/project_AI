import streamlit as st
import matplotlib.pyplot as plt
from shortest_path import find_shortest_path

def plot_map(southern_vietnam, output, path=None):
    color_map = {
        'Light Pink': '#ffb6c1',
        'Light Green': '#90ee90',
        'Light Blue': '#add8e6',
        'Light Yellow': '#fffacd',
        'Light Orange': '#ffcc99'
    }
    fig, ax = plt.subplots(figsize=(9, 9))
    southern_vietnam.boundary.plot(ax=ax, linewidth=1, color='grey')

    for province, color_key in output.items():
        province_shape = southern_vietnam[southern_vietnam['NAME_1'] == province]
        color = color_map.get(color_key, '#ffb6c1')
        province_shape.plot(ax=ax, color=color)
        coords = province_shape.geometry.centroid
        ax.text(coords.x.iloc[0], coords.y.iloc[0], province, fontsize=8, ha='center', color='black')

    if path:
        coords = [southern_vietnam[southern_vietnam['NAME_1'] == p].geometry.centroid.iloc[0] for p in path]
        x, y = zip(*[(c.x, c.y) for c in coords])
        ax.plot(x, y, color='blue', linewidth=2, marker='o')

    ax.set_title("Bản đồ miền Nam Việt Nam", fontsize=16)
    return fig

def create_ui(southern_provinces, graph, southern_vietnam, output):
    st.sidebar.subheader("Tìm đường ngắn nhất")
    start = st.sidebar.selectbox("Chọn điểm bắt đầu", southern_provinces)
    end = st.sidebar.selectbox("Chọn điểm đến", southern_provinces)
    
    # Tạo nút "tìm đường đi" và nút "reset"
    col1, col2 = st.sidebar.columns([3, 2])
    path = []
    with col1:
        if st.button("Tìm đường đi"):
            path = find_shortest_path(graph, start, end)
            if path:
                st.sidebar.success(f"Đường đi: {' -> '.join(path)}")
            else:
                st.sidebar.error("Không có đường đi giữa hai tỉnh này!")

    with col2:
        if st.button("Reset"):
            path = []
            st.sidebar.info("Bản đồ đã được reset.")

    fig = plot_map(southern_vietnam, output, path)
    st.pyplot(fig)
