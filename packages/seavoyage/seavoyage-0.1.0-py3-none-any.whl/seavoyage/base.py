from searoute import searoute
from seavoyage.classes import MNetwork
from seavoyage.utils import get_m_network_20km

def seavoyage(start: tuple[float, float], end: tuple[float, float], **kwargs):
    """
    선박 경로 계산

    Args:
        start (tuple[float, float]): 출발 좌표
        end (tuple[float, float]): 종점 좌표

    Returns:
        geojson.FeatureCollection(dict): 경로 정보
    """
    if not kwargs.get("M"):
        kwargs["M"] = get_m_network_20km()
    return searoute(start, end, **kwargs)
