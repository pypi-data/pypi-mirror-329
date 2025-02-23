# MNetwork.py
import geojson
from searoute import Marnet
from searoute.utils import distance
from shapely import LineString

class MNetwork(Marnet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_node_with_edges(self, node: tuple[float, float], threshold: float = 100.0):
        """
        새로운 노드를 추가하고 임계값 내의 기존 노드들과 자동으로 엣지를 생성합니다.
        :param node: 추가할 노드의 (longitude, latitude) 좌표
        :param threshold: 엣지를 생성할 거리 임계값(km)
        :return: 생성된 엣지들의 리스트 [(node1, node2, weight), ...]
        """
        if threshold <= 0 or not isinstance(threshold, (int, float)):
            raise ValueError("Threshold must be a positive number.")
        
        if not isinstance(node, tuple) or len(node) != 2:
            raise TypeError("Node must be a tuple of (longitude, latitude).")
        
        if node in self.nodes:
            return []
        # 노드 추가
        self.add_node(node)
        
        # 생성된 엣지들을 저장할 리스트
        created_edges = []
        
        # 기존 노드들과의 거리를 계산하고 임계값 이내인 경우 엣지 생성
        for existing_node in list(self.nodes):
            if existing_node == node:
                continue
                
            dist = distance(node, existing_node, units="km")
            if dist <= threshold:
                self.add_edge(node, existing_node, weight=dist)
                created_edges.append((node, existing_node, dist))
                
        for edge in created_edges:
            self.add_edge(edge[0], edge[1], weight=edge[2])
        return created_edges

    def add_nodes_with_edges(self, nodes: list[tuple[float, float]], threshold: float = 100.0):
        """
        여러 노드들을 추가하고 임계값 내의 모든 노드들(기존 + 새로운)과 자동으로 엣지를 생성합니다.

        :param nodes: 추가할 노드들의 [(longitude, latitude), ...] 좌표 리스트
        :param threshold: 엣지를 생성할 거리 임계값(km)
        :return: 생성된 엣지들의 리스트 [(node1, node2, weight), ...]
        """
        if not isinstance(nodes, list):
            raise TypeError("Nodes must be a list of tuples representing the coordinates.")
        if threshold <= 0 or not isinstance(threshold, (int, float)):
            raise ValueError("Threshold must be a positive number.")
        
        if any(not isinstance(node, tuple) or len(node) != 2 for node in nodes):
            raise TypeError("Each node must be a tuple of (longitude, latitude).")
        
        all_created_edges = []
        
        # 각 새로운 노드에 대해 처리
        for node in nodes:
            # 기존 노드들과의 엣지 생성
            edges = self.add_node_with_edges(node, threshold)
            all_created_edges.extend(edges)
            
            # 이미 추가된 새로운 노드들과의 엣지 생성
            for other_node in nodes:
                if other_node == node or other_node not in self.nodes:
                    continue
                    
                dist = distance(node, other_node, units="km")
                if dist <= threshold:
                    self.add_edge(node, other_node, weight=dist)
                    all_created_edges.append((node, other_node, dist))
                    
        for edge in all_created_edges:
            self.add_edge(edge[0], edge[1], weight=edge[2])
        print(f"Added {len(all_created_edges)} edges")

    def _extract_point_coordinates(self, point: geojson.Point):
        """
        GeoJSON Point 객체에서 좌표를 추출합니다.

        :param point: 좌표를 추출할 Point 객체
        :return: (longitude, latitude) 좌표
        """
        if isinstance(point, dict):
            coords = point["coordinates"]
        elif isinstance(point, geojson.Point):
            coords = point.coordinates
        else:
            raise TypeError("Invalid point type. Must be a geojson.Point or dict.")
        
        if not coords or len(coords) < 2:
            raise ValueError("Invalid point coordinates")
        
        return tuple(coords[:2])  # (longitude, latitude)
    
    def add_geojson_point(self, point, threshold: float = 100.0):
        """
        GeoJSON Point 객체를 노드로 추가하고 임계값 내의 노드들과 엣지를 생성합니다.
        :param point: 추가할 Point 객체
        :param threshold: 엣지를 생성할 거리 임계값(km)
        :return: 생성된 엣지들의 리스트
        """
        coords = self._extract_point_coordinates(point)
        return self.add_node_with_edges(coords, threshold)

    def add_geojson_multipoint(self, multipoint, threshold: float = 100.0):
        """
        GeoJSON MultiPoint 객체의 모든 점들을 노드로 추가하고 임계값 내의 노드들과 엣지를 생성합니다.
        :param multipoint: 추가할 MultiPoint 객체
        :param threshold: 엣지를 생성할 거리 임계값(km)
        :return: 생성된 엣지들의 리스트
        """
        #TODO: 최적화 필요
        if isinstance(multipoint, dict):
            coords = multipoint.get('coordinates', [])
        else:
            coords = multipoint.coordinates
            
        nodes = [tuple(coord[:2]) for coord in coords]
        return self.add_nodes_with_edges(nodes, threshold)

    def add_geojson_feature_collection(self, feature_collection, threshold: float = 100.0):
        """
        GeoJSON FeatureCollection의 Point 피처들을 노드로 추가하고 임계값 내의 노드들과 엣지를 생성합니다.
        :param feature_collection: Point 피처들을 포함한 FeatureCollection 객체
        :param threshold: 엣지를 생성할 거리 임계값(km)
        :return: 생성된 엣지들의 리스트
        """
        if isinstance(feature_collection, dict):
            features = feature_collection.get('features', [])
        else:
            features = feature_collection.features

        nodes = []
        for feature in features:
            if isinstance(feature, dict):
                geometry = feature.get('geometry', {})
                if geometry.get('type') == 'Point':
                    coords = geometry.get('coordinates')
                    if coords and len(coords) >= 2:
                        nodes.append(tuple(coords[:2]))
            else:
                geometry = feature.geometry
                if isinstance(geometry, geojson.Point):
                    coords = geometry.coordinates
                    if coords and len(coords) >= 2:
                        nodes.append(tuple(coords[:2]))
                        
        return self.add_nodes_with_edges(nodes, threshold)
    
    def to_geojson(self, file_path: str = None) -> geojson.FeatureCollection:
        """노드와 엣지를 GeoJSON 형식으로 내보냅니다."""
        features = []
        
        for u, v, attrs in self.edges(data=True):
            line = geojson.LineString([[u[0], u[1]], [v[0], v[1]]])
            feature = geojson.Feature(geometry=line, properties=attrs)
            features.append(feature)
            
        feature_collection = geojson.FeatureCollection(features)
        
        if file_path:
            with open(file_path, "w") as f:
                geojson.dump(feature_collection, f)
                
        return feature_collection
    
    def to_line_string(self) -> list[LineString]:
        """노드와 엣지를 LineString 객체로 내보냅니다."""
        linestrings = []
        for u, v, attrs in self.edges(data=True):
            linestrings.append(LineString([[u[0], u[1]], [v[0], v[1]]]))
        return linestrings


if __name__ == "__main__":
# 사용 예시
    marnet = MNetwork()
    marnet.load_geojson("apps/pathfinding/data/marnet/marnet_plus_100km.geojson")

    # 단일 노드 추가 및 엣지 자동 생성
    new_node = (129.165, 35.070)
    created_edges = marnet.add_node_with_edges(new_node, threshold=100.0)
    print(created_edges)

    # 여러 노드 추가 및 엣지 자동 생성
    new_nodes = [
        (129.170, 35.075),
        (129.180, 35.080),
        (129.175, 35.070)
    ]
    all_created_edges = marnet.add_nodes_with_edges(new_nodes, threshold=100.0)
    print(all_created_edges)
    
    marnet.print_graph_info()