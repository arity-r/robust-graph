from networkx import star_graph
from networkx.drawing import spring_layout

from robust_graph.util import scale_free_network
from robust_graph.util import save_graph_as_image

G = scale_free_network(n=100, gamma=2.5, avrdeg=8)
save_graph_as_image(G, 'onion_layout.png')
save_graph_as_image(G, 'spring_layout.png', spring_layout)

