import streamlit as st
import pandas as pd
import geojson
import heapq
from collections import defaultdict
from math import radians, sin, cos, asin, sqrt
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Rute Bidan", page_icon="🗺️", layout="wide")

# ===== Utility fungsi =====
def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = radians(lat2 - lat1); dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    return 2 * R * asin(sqrt(a))

def load_graph_from_geojson(path):
    with open(path, "r", encoding="utf-8") as f:
        gj = geojson.load(f)
    features = gj["features"]

    # Bounding box Jakarta
    min_lon, max_lon = 106.6, 107.0
    min_lat, max_lat = -6.4, -6.05

    def inside_jakarta(lon, lat):
        return (min_lon <= lon <= max_lon) and (min_lat <= lat <= max_lat)

    nodes, rev_nodes, adj = {}, {}, defaultdict(list)

    def get_id(lat, lon):
        key = (round(lat,6), round(lon,6))
        if key not in nodes:
            idx = len(nodes); nodes[key] = idx; rev_nodes[idx] = key
        return nodes[key]

    for feat in features:
        geom = feat["geometry"]; coords = geom["coordinates"]
        if geom["type"] == "LineString":
            for i in range(len(coords)-1):
                lon1, lat1 = coords[i][:2]
                lon2, lat2 = coords[i+1][:2]
                if not (inside_jakarta(lon1, lat1) and inside_jakarta(lon2, lat2)):
                    continue
                u, v = get_id(lat1, lon1), get_id(lat2, lon2)
                w = haversine_km(lat1, lon1, lat2, lon2)
                adj[u].append((v,w)); adj[v].append((u,w))
        elif geom["type"] == "MultiLineString":
            for line in coords:
                for i in range(len(line)-1):
                    lon1, lat1 = line[i][:2]
                    lon2, lat2 = line[i+1][:2]
                    if not (inside_jakarta(lon1, lat1) and inside_jakarta(lon2, lat2)):
                        continue
                    u, v = get_id(lat1, lon1), get_id(lat2, lon2)
                    w = haversine_km(lat1, lon1, lat2, lon2)
                    adj[u].append((v,w)); adj[v].append((u,w))

    return nodes, rev_nodes, adj

def nearest_node(lat, lon, rev_nodes):
    best, best_d = None, float("inf")
    for idx, (nlat,nlon) in rev_nodes.items():
        d = haversine_km(lat, lon, nlat, nlon)
        if d < best_d: best, best_d = idx, d
    return best

def dijkstra(adj, source, target):
    pq = [(0.0, source)]
    dist, prev, visited = {source:0.0}, {}, set()
    while pq:
        d,u = heapq.heappop(pq)
        if u in visited: continue
        visited.add(u)
        if u == target: break
        for v,w in adj.get(u, []):
            nd = d + w
            if v not in dist or nd < dist[v]:
                dist[v] = nd; prev[v] = u
                heapq.heappush(pq,(nd,v))
    if target not in dist: return float("inf"), []
    # reconstruct path
    path=[target]
    while path[-1] != source:
        path.append(prev[path[-1]])
    return dist[target], list(reversed(path))

# ===== Init session_state =====
if "graph" not in st.session_state:
    st.session_state["graph"] = load_graph_from_geojson("Jaringan_jalanan_indonesia.geojson")
if "bidan_df" not in st.session_state:
    st.session_state["bidan_df"] = pd.read_csv("bidan_points.csv")
if "last_route" not in st.session_state:
    st.session_state["last_route"] = None

nodes, rev_nodes, adj = st.session_state["graph"]
bidan_df = st.session_state["bidan_df"]

# ===== Input lokasi user =====
st.sidebar.header("Lokasi Anda")
user_lat = st.sidebar.number_input("Latitude", value=-6.2, format="%.6f")
user_lon = st.sidebar.number_input("Longitude", value=106.8, format="%.6f")

# ===== Pilih Bidan Tujuan =====
st.sidebar.header("Pilih Tujuan")
bidan_names = bidan_df["name"].tolist()
selected_bidan = st.sidebar.selectbox("Bidan Tujuan", bidan_names)

# ===== Hitung route hanya kalau input berubah =====
current_key = (round(user_lat,6), round(user_lon,6), selected_bidan)

if st.session_state["last_route"] is None or st.session_state["last_route"]["key"] != current_key:
    s_id = nearest_node(user_lat, user_lon, rev_nodes)
    dest_row = bidan_df[bidan_df["name"] == selected_bidan].iloc[0]
    t_id = nearest_node(dest_row.lat, dest_row.lon, rev_nodes)

    dist_km, path_ids = dijkstra(adj, s_id, t_id)
    st.session_state["last_route"] = {
        "key": current_key,
        "dist_km": dist_km,
        "path_ids": path_ids,
        "dest_row": dest_row
    }

# Ambil hasil dari session_state
dist_km = st.session_state["last_route"]["dist_km"]
path_ids = st.session_state["last_route"]["path_ids"]
dest_row = st.session_state["last_route"]["dest_row"]

# ===== Peta Folium =====
m = folium.Map(location=[user_lat, user_lon], zoom_start=14)

# Marker asal
folium.Marker([user_lat, user_lon], popup="Anda", icon=folium.Icon(color="blue")).add_to(m)
# Marker tujuan
folium.Marker([dest_row.lat, dest_row.lon], popup=dest_row.name, icon=folium.Icon(color="red")).add_to(m)

# Gambar polyline sesuai jaringan
if path_ids:
    route_coords = [(rev_nodes[nid][0], rev_nodes[nid][1]) for nid in path_ids]
    folium.PolyLine([(lat, lon) for lat, lon in route_coords], color="green", weight=5).add_to(m)

st_folium(m, width=800, height=600)

st.success(f"🚗 Rute ke {dest_row.name} — {dist_km:.2f} km via jaringan jalan (Jakarta).")
