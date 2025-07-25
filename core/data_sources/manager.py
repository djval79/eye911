"""Unified Data Source Manager"""
from typing import Dict, Any
import asyncio
from .cad_firehose import PulsePoint, RapidDeploy
from .connected_car import Otonomo, Smartcar
from .alpr import RekorScout, VigilantLEARN
from .cell_location import LocationSmart, XMode
from .social_streams import TwitterDecahose, SnapMap
from .satellite import CapellaSpace, ICEYE
from .municipal_iot import NoTraffic, Iteris
from .people_graph import FullContact, TrestleIntelius
from .instagram import SocialLinks, PathSocial

class DataSourceManager:
    """Manages all data source integrations with unified interface"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize all data sources from config"""
        # 911 CAD Firehose
        self.pulsepoint = PulsePoint(config["pulsepoint_api_key"])
        self.rapiddeploy = RapidDeploy(config["rapiddeploy_webhook_url"])
        
        # Connected Car
        self.otonomo = Otonomo(
            config["otonomo_client_id"],
            config["otonomo_client_secret"]
        )
        self.smartcar = Smartcar(config["smartcar_access_token"])
        
        # ALPR
        self.rekor = RekorScout(config["rekor_api_key"])
        self.vigilant = VigilantLEARN(
            config["vigilant_agency_id"],
            config["vigilant_auth_token"]
        )
        
        # Cell Location
        self.locationsmart = LocationSmart(config["locationsmart_token"])
        self.xmode = XMode(config["xmode_sdk_key"])
        
        # Social Media
        self.twitter = TwitterDecahose(config["twitter_api_key"])
        self.snapchat = SnapMap(config["snapchat_auth_token"])
        
        # Satellite
        self.capella = CapellaSpace(config["capella_api_key"])
        self.iceye = ICEYE(
            config["iceye_client_id"],
            config["iceye_client_secret"]
        )
        
        # Municipal IoT
        self.notraffic = NoTraffic(config["notraffic_api_key"])
        self.iteris = Iteris(
            config["iteris_client_id"],
            config["iteris_client_secret"]
        )
        
        # People Graph
        self.fullcontact = FullContact(config["fullcontact_api_key"])
        self.trestle = TrestleIntelius(config["trestle_api_key"])
        
        # Instagram
        self.sociallinks = SocialLinks(config["sociallinks_api_key"])
        self.pathsocial = PathSocial(
            config["pathsocial_client_id"],
            config["pathsocial_client_secret"]
        )
    
    async def detect_crash_signals(self, location: Dict[str, float], radius: float):
        """Query all data sources for crash signals in area"""
        # Collect results from all relevant sources
        results = {
            "cad": await self._query_cad_sources(location, radius),
            "connected_car": await self._query_connected_car(location, radius),
            "alpr": await self._query_alpr(location, radius),
            "cell": await self._query_cell_data(location, radius),
            "social": await self._query_social(location, radius),
            "satellite": await self._query_satellite(location),
            "iot": await self._query_iot(location, radius)
        }
        return results
    
    async def enrich_identity(self, identifiers: Dict[str, str]):
        """Enrich identity using all available sources"""
        return {
            "people_graph": await self._query_people_graph(identifiers),
            "instagram": await self._query_instagram(identifiers)
        }
    
    async def _query_cad_sources(self, location, radius):
        """Query 911 CAD firehose sources"""
        return {
            "pulsepoint": await self.pulsepoint.get_live_incidents(),
            "rapiddeploy": {"status": "webhook_configured"}
        }

    async def _query_connected_car(self, location, radius):
        """Query connected car data sources"""
        return {
            "otonomo": await self.otonomo.get_crash_events(),
            "smartcar": {"status": "requires_vehicle_id"}
        }

    async def _query_alpr(self, location, radius):
        """Query ALPR data sources"""
        bbox = self._location_to_bbox(location, radius)
        return {
            "rekor": await self.rekor.get_plate_reads(bbox),
            "vigilant": {"status": "requires_plate_list"}
        }

    async def _query_cell_data(self, location, radius):
        """Query cell location data sources"""
        return {
            "locationsmart": {"status": "requires_cell_ids"},
            "xmode": {"status": "requires_device_ids"}
        }

    async def _query_social(self, location, radius):
        """Query social media data sources"""
        keywords = ["crash", "accident", "collision"]
        return {
            "twitter": [msg async for msg in self.twitter.stream_geo_keywords(keywords, self._location_to_bbox(location, radius))][:10],
            "snapchat": await self.snapchat.get_public_stories(location["lat"], location["lng"])
        }

    async def _query_satellite(self, location):
        """Query satellite data sources"""
        return {
            "capella": await self.capella.detect_vehicle_deformation([location]),
            "iceye": {"status": "requires_segment_id"}
        }

    async def _query_iot(self, location, radius):
        """Query municipal IoT data sources"""
        return {
            "notraffic": {"status": "requires_intersection_id"},
            "iteris": {"status": "requires_corridor_id"}
        }

    async def _query_people_graph(self, identifiers):
        """Query people graph APIs"""
        return {
            "fullcontact": await self.fullcontact.lookup_by_phone(identifiers.get("phone")),
            "trestle": await self.trestle.reverse_phone_lookup(identifiers.get("phone"))
        }

    async def _query_instagram(self, identifiers):
        """Query Instagram enrichment APIs"""
        return {
            "sociallinks": await self.sociallinks.lookup_handles([identifiers.get("phone")]),
            "pathsocial": await self.pathsocial.query_profile(identifiers.get("username", ""))
        }

    def _location_to_bbox(self, location, radius_km):
        """Convert location+radius to bounding box"""
        km_per_degree = 111.32
        delta = radius_km / km_per_degree
        return (
            location["lat"] - delta,
            location["lng"] - delta,
            location["lat"] + delta,
            location["lng"] + delta
        )
