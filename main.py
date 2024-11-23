from load_map import load_vietnam_map, filter_southern_provinces
from coloring import solve_coloring_problem
from shortest_path import create_province_graph
from ui import create_ui

def main(shapefile_path):
    southern_provinces = [
        'Đồng Nai', 'Bình Dương', 'Bà Rịa - Vũng Tàu', 'Tây Ninh',
        'Bình Phước', 'Hồ Chí Minh', 'Long An', 'Tiền Giang', 'Bến Tre', 'Trà Vinh',
        'Vĩnh Long', 'Đồng Tháp', 'An Giang', 'Cần Thơ', 'Hậu Giang', 'Kiên Giang',
        'Sóc Trăng', 'Bạc Liêu', 'Cà Mau'
    ]
    # Các tỉnh liền kề = đường đi/ cặp tỉnh/ cạnh
    adjacency_list = [

        ('Đồng Nai', 'Bình Dương'), 
        ('Đồng Nai', 'Bà Rịa - Vũng Tàu'), 
        ('Đồng Nai', 'Bình Phước'), 
        ('Đồng Nai', 'Hồ Chí Minh'), 

        ('Hồ Chí Minh', 'Bà Rịa - Vũng Tàu'), 
        ('Hồ Chí Minh', 'Bình Dương'), 
        ('Hồ Chí Minh', 'Long An'), 
        ('Hồ Chí Minh', 'Tiền Giang'), 
        ('Hồ Chí Minh', 'Tây Ninh'), 

        ('Bình Dương', 'Bình Phước'), 
        ('Bình Dương', 'Tây Ninh'), 

        ('Tây Ninh', 'Bình Phước'), 
        ('Tây Ninh', 'Long An'), 

        ('Long An', 'Tiền Giang'), 
        ('Long An', 'Đồng Tháp'), 

        ('Tiền Giang', 'Bến Tre'), 
        ('Tiền Giang', 'Vĩnh Long'), 
        ('Tiền Giang', 'Đồng Tháp'), 

        ('Vĩnh Long', 'Đồng Tháp'), 
        ('Vĩnh Long', 'Bến Tre'), 
        ('Vĩnh Long', 'Cần Thơ'), 
        ('Vĩnh Long', 'Trà Vinh'), 
        ('Vĩnh Long', 'Sóc Trăng'), 
        ('Vĩnh Long', 'Hậu Giang'), 

        ('Bến Tre', 'Trà Vinh'), 

        ('Cần Thơ', 'An Giang'), 
        ('Cần Thơ', 'Đồng Tháp'), 
        ('Cần Thơ', 'Hậu Giang'), 
        ('Cần Thơ', 'Kiên Giang'),

        ('An Giang', 'Đồng Tháp'),

        ('Kiên Giang', 'Hậu Giang'), 
        ('Kiên Giang', 'An Giang'), 
        ('Kiên Giang', 'Cà Mau'), 

        ('Hậu Giang', 'Sóc Trăng'), 
        ('Hậu Giang', 'Bạc Liêu'), 

        ('Sóc Trăng', 'Bạc Liêu'), 
        ('Sóc Trăng', 'Trà Vinh'), 

        ('Bạc Liêu', 'Kiên Giang'), 
        ('Bạc Liêu', 'Cà Mau'),
    ]

    # Load and process map data
    vietnam = load_vietnam_map(shapefile_path)
    southern_vietnam = filter_southern_provinces(vietnam, southern_provinces)
    output = solve_coloring_problem(southern_provinces, adjacency_list)

    # Tạo đồ thị, đường đi giữa các tỉnh
    graph = create_province_graph(southern_vietnam, southern_provinces, adjacency_list)

    # Tạo bản đồ, UI
    create_ui(southern_provinces, graph, southern_vietnam, output)

if __name__ == "__main__":
    shapefile_path = "gadm41_VNM_shp/gadm41_VNM_1.shp"
    main(shapefile_path)

